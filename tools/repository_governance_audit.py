#!/usr/bin/env python3
"""Phase 4 — Repository asset intelligence + knowledge classification.

NON-DESTRUCTIVE governance pass. Walks the repository and produces a full
inventory + classification + knowledge-value scorecard + recommended (but
never automatic) ownership moves.

Hard rules honoured:
  * Does NOT delete anything.
  * Does NOT move anything.
  * Does NOT overwrite any source artifact.
  * Does NOT silently merge ambiguous assets.
  * Does NOT recreate the old manual-centric structure.

All output lives under
`wp-content/themes/beslock-custom/User manuals/_repository-governance/`.

Quarantine is a DOCUMENTED set of pointers, never a physical move. Ownership
recommendations are emitted as `recommended-moves.json` for a future, manual
cutover step.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content/themes/beslock-custom/User manuals"
GOV = USER_MANUALS / "_repository-governance"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SCHEMA = "repo-governance/1.0"

# Directories whose internals we DO NOT enumerate file-by-file (they are
# external/foreign to the Beslock product knowledge layer or sheer infra).
# We still record their existence in the inventory as a single bucket entry.
OPAQUE_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "wp-admin",
    "wp-includes",
    "wp-content/plugins",
    "wp-content/plugins_ZIP",
    "wp-content/upgrade",
    "wp-content/upgrade-temp-backup",
    "wp-content/uploads",
    "wp-content/cache",
    "wp-content/backuply",
    "wp-content/endurance-page-cache",
    "wp-content/speedycache-config",
    "wp-content/languages",
    "wp-content/mu-plugins",
    # Note: do NOT add "wp-content/themes" here; we want to descend into it so
    # the per-iteration rule below can drop non-beslock themes while keeping
    # `wp-content/themes/beslock-custom/`.
    "database",
    "docker/mysql-init",
    ".tmp",
    ".tmp-hero-startup",
    ".tmp-hero-startup-after",
    "test-results",
}

# Pinpoint additions: enumerate only beslock-custom inside wp-content/themes/.
PINPOINT_DIRS = {
    "wp-content/themes/beslock-custom",
}

# Canonical layers — anything inside these is already canonical and is recorded
# but NOT proposed for relocation. The `User manuals/` canonical area lives
# inside `wp-content/themes/beslock-custom/User manuals/`.
CANONICAL_PREFIXES = (
    "wp-content/themes/beslock-custom/User manuals/ext-images/",
    "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/",
    "wp-content/themes/beslock-custom/User manuals/visual-system/",
    "wp-content/themes/beslock-custom/User manuals/_repository-governance/",
    "wp-content/themes/beslock-custom/User manuals/review-previews/",
)

# Skip dotfiles / system files.
SKIP_NAMES = {".DS_Store"}

INTERESTING_EXTS = {
    ".md", ".json", ".txt", ".yaml", ".yml", ".csv", ".py", ".sh", ".php",
    ".xls", ".xlsx", ".pdf", ".png", ".jpg", ".jpeg", ".html",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def md5_of(path: Path, max_bytes: int = 64 * 1024 * 1024) -> str | None:
    try:
        if path.stat().st_size > max_bytes:
            # For very large files, hash the head to keep the audit fast but
            # still detect duplicates of identical blobs.
            h = hashlib.md5()
            with path.open("rb") as f:
                h.update(f.read(1 << 20))
            return "head1m:" + h.hexdigest()
        h = hashlib.md5()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def is_under(rel: str, prefixes: Iterable[str]) -> bool:
    return any(rel == p.rstrip("/") or rel.startswith(p) for p in prefixes)


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


# ---------------------------------------------------------------------------
# Walk
# ---------------------------------------------------------------------------
def discover_assets() -> list[dict]:
    """Walk the repo and return one record per asset. Folder rules:

    * For dirs in OPAQUE_DIRS: emit a single summary record (no recursion).
    * For dirs in CANONICAL_PREFIXES: enumerate but mark canonical=True.
    * Otherwise: enumerate fully.
    """
    records: list[dict] = []
    opaque_summary: dict[str, dict] = {}

    for root, dirs, files in os.walk(REPO):
        rel_root = Path(root).relative_to(REPO).as_posix()
        if rel_root == ".":
            rel_root = ""

        # Skip recursion into opaque dirs — record them once.
        if rel_root in OPAQUE_DIRS or any(
            rel_root.startswith(p + "/") for p in OPAQUE_DIRS
        ):
            owner = next(
                p for p in OPAQUE_DIRS
                if rel_root == p or rel_root.startswith(p + "/")
            )
            if owner not in opaque_summary:
                opaque_summary[owner] = {"file_count": 0, "byte_total": 0}
            for f in files:
                fp = Path(root) / f
                try:
                    opaque_summary[owner]["file_count"] += 1
                    opaque_summary[owner]["byte_total"] += fp.stat().st_size
                except Exception:
                    pass
            dirs[:] = []  # don't recurse further
            continue

        # Inside wp-content/themes but NOT beslock-custom → opaque.
        if rel_root.startswith("wp-content/themes/") and not rel_root.startswith(
            "wp-content/themes/beslock-custom"
        ):
            opaque_summary.setdefault(
                "wp-content/themes (other)", {"file_count": 0, "byte_total": 0}
            )
            for f in files:
                fp = Path(root) / f
                try:
                    opaque_summary["wp-content/themes (other)"]["file_count"] += 1
                    opaque_summary["wp-content/themes (other)"]["byte_total"] += fp.stat().st_size
                except Exception:
                    pass
            dirs[:] = []
            continue

        # Skip dotfile dirs nested deeper than root.
        dirs[:] = [d for d in dirs if not (d.startswith(".") and d not in (".gitignore",))]

        for f in files:
            if f in SKIP_NAMES:
                continue
            fp = Path(root) / f
            try:
                st = fp.stat()
            except FileNotFoundError:
                continue
            ext = fp.suffix.lower()
            relp = rel(fp)
            records.append(
                {
                    "path": relp,
                    "ext": ext,
                    "size_bytes": st.st_size,
                    "mtime_iso": datetime.fromtimestamp(st.st_mtime, timezone.utc)
                    .strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "is_canonical_layer": is_under(relp, CANONICAL_PREFIXES),
                    "md5": md5_of(fp) if ext in INTERESTING_EXTS else None,
                }
            )

    # Encode opaque summaries as inventory rows too.
    for owner, info in sorted(opaque_summary.items()):
        records.append(
            {
                "path": owner + "/",
                "ext": "(opaque-bucket)",
                "size_bytes": info["byte_total"],
                "mtime_iso": NOW,
                "is_canonical_layer": False,
                "md5": None,
                "opaque_bucket": True,
                "opaque_file_count": info["file_count"],
            }
        )

    return records


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------
# Categories:
#   A — CANONICAL KNOWLEDGE
#   B — SOURCE EVIDENCE
#   C — TRANSITIONAL SEMANTIC
#   D — ORCHESTRATION
#   E — GOVERNANCE
#   F — LEGACY / UNKNOWN
#   X — INFRASTRUCTURE (out-of-scope but kept in inventory)


def classify(rec: dict) -> tuple[str, str, str]:
    """Return (category_letter, sub_label, ownership_recommendation)."""
    p = rec["path"]
    ext = rec["ext"]

    # X — opaque infra buckets and WP infra files.
    if rec.get("opaque_bucket"):
        return "X", "infrastructure-bucket", "no-action (out of scope)"
    if p.startswith("wp-content/") and not p.startswith("wp-content/themes/beslock-custom"):
        return "X", "wordpress-infra", "no-action (out of scope)"
    # Disabled / archived theme variants — out of scope of the Beslock product
    # knowledge layer. Treated as infrastructure/legacy theme runtime.
    if p.startswith("wp-content/themes/beslock-custom-disabled/") or p.startswith(
        "wp-content/themes/beslock-custom-backup/"
    ):
        return "X", "wordpress-theme-disabled", "no-action (disabled theme variant)"
    # beslock-custom theme runtime (PHP templates, CSS, JS) — out of scope of
    # the Beslock product knowledge layer. The canonical Beslock layer lives
    # under `wp-content/themes/beslock-custom/User manuals/` and is handled by
    # the canonical-layer branch below.
    if p.startswith("wp-content/themes/beslock-custom/") and not p.startswith(
        "wp-content/themes/beslock-custom/User manuals/"
    ):
        return "X", "wordpress-theme-runtime", "no-action (theme runtime)"
    if p.startswith("wp-admin/") or p.startswith("wp-includes/"):
        return "X", "wordpress-core", "no-action (out of scope)"
    if p in (
        "wp-config-sample.php", "docker-compose.yml", "Makefile",
        ".gitignore", ".env", ".env.local",
    ):
        return "X", "infra-config", "no-action (infra)"
    if p.startswith("docker/") or p.startswith("database/"):
        return "X", "deployment-infra", "no-action (deployment)"
    if p.startswith("test-results/"):
        return "X", "test-results", "no-action (ephemeral)"

    # A — Canonical knowledge.
    if rec["is_canonical_layer"]:
        if "/knowledge-core/" in p:
            return "A", "knowledge-core", f"already-canonical: {p}"
        if "/structured-knowledge/" in p:
            return "A", "structured-knowledge-verified", f"already-canonical: {p}"
        if "/source-of-truth/" in p:
            return "B", "source-of-truth-evidence", f"already-canonical: {p}"
        if "/visual-system/" in p:
            return "D", "visual-orchestration", f"already-canonical: {p}"
        if "/KNOWLEDGE_BUILDING/" in p:
            return "E", "governance-reports", f"already-canonical: {p}"
        if "/_repository-governance/" in p:
            return "E", "governance", f"already-canonical: {p}"
        if "/review-previews/" in p:
            return "C", "transitional-review-previews", f"already-canonical: {p}"
        return "A", "canonical-other", f"already-canonical: {p}"

    # B — Source evidence (root-level OCR exports).
    if p.startswith("generated_manuals/") or p.startswith("generated_manuals_supplemental/"):
        return "B", "ocr-evidence-root", (
            "owned-by knowledge-core (already promoted via "
            "ext-images/<slug>/knowledge-core/semantic/extracted-text-supplemental/); "
            "keep as raw OCR evidence at repo root or move to "
            "_repository-governance/source-evidence/ocr-exports/ in a future cutover"
        )

    # D — Orchestration outputs from visual_generation.py.
    if p.startswith("output/visual-generation/"):
        return "D", "visual-orchestration-runs", (
            "future-relocate to "
            "wp-content/themes/beslock-custom/User manuals/visual-system/runs/"
            " in a future cutover (manual review required)"
        )
    if p.startswith("output/"):
        return "D", "orchestration-output", (
            "future-relocate to a `runtime/` root-level dir (per Task 8 cleanup goal)"
        )

    # D — Tooling.
    if p.startswith("tools/"):
        if p == "tools/knowledge_core_build.py":
            return "E", "phase-2-builder", f"already-tool: {p}"
        if p == "tools/knowledge_core_semantic_enrich.py":
            return "E", "phase-3-builder", f"already-tool: {p}"
        if p == "tools/phase2b_source_audit.py":
            return "E", "phase-2b-auditor", f"already-tool: {p}"
        if p.startswith("tools/comfy/") or "comfy" in p:
            return "D", "comfy-orchestration", f"already-tool: {p}"
        if p.startswith("tools/manual_ocr/"):
            return "B", "ocr-pipeline", f"already-tool: {p}"
        return "D", "tooling", f"already-tool: {p}"

    # Root-level helpers.
    if p == "process_manuals.py":
        return "B", "ocr-driver", "tool — keep at root or move to tools/ for consistency"
    if p == "visual_generation.py":
        return "D", "visual-orchestrator", "tool — keep at root or move to tools/ for consistency"

    # README / project meta.
    if p == "README.md":
        return "E", "project-readme", "keep at root"
    if p == "ARCHITECTURE.md" or p == "FRONTEND_ARCHITECTURE.md":
        return "E", "architecture", "future-relocate to _repository-governance/manifests/architecture/"
    if p == "BEM_GUIDELINES.md":
        return "E", "frontend-conventions", "future-relocate to _repository-governance/manifests/frontend/"
    if p == "CLEANUP_PLAN.md" or p == "COMPONENT_MIGRATION_PLAN.md":
        return "E", "migration-plan", "future-relocate to _repository-governance/migration-history/plans/"
    if p == "VISUAL_GENERATION_AUTOMATION.md":
        return "D", "visual-orchestration-doc", "future-relocate to visual-system/docs/"
    if re.match(r"^[A-Z_]+_SUMMARY\.md$", Path(p).name) or p == "WORKTREE_NORMALIZATION_SUMMARY.md":
        return "F", "frontend-migration-summary-legacy", (
            "future-relocate to _repository-governance/migration-history/frontend-summaries/ "
            "(NON-AUTOMATIC). These are historical migration receipts for the WordPress theme, "
            "not Beslock product knowledge."
        )
    if p == "data/products.json":
        return "C", "product-catalog-draft", (
            "ambiguous — quarantine pointer in _repository-governance/quarantine/data-products/ "
            "until ownership is clarified (legacy storefront vs. knowledge-core)"
        )

    # E / governance fallbacks for top-level .md not covered above.
    if ext == ".md" and "/" not in p:
        return "F", "root-markdown-unknown", "quarantine until classified manually"

    return "F", "unknown", "quarantine until classified manually"


def knowledge_value(rec: dict, category: str, sub_label: str) -> str:
    """Return HIGH | MEDIUM | LOW | INFRA."""
    if category == "X":
        return "INFRA"
    if category == "A":
        return "HIGH"
    if category == "B":
        # OCR evidence is high; OCR pipeline tooling is medium.
        if "ocr-pipeline" in sub_label or "ocr-driver" in sub_label:
            return "MEDIUM"
        return "HIGH"
    if category == "D":
        if sub_label in ("visual-orchestration", "visual-orchestrator", "comfy-orchestration"):
            return "HIGH"
        return "MEDIUM"
    if category == "E":
        if sub_label in ("phase-2-builder", "phase-3-builder", "phase-2b-auditor", "governance", "governance-reports", "architecture"):
            return "HIGH"
        return "MEDIUM"
    if category == "C":
        return "MEDIUM"
    if category == "F":
        if "frontend-migration-summary" in sub_label:
            return "LOW"
        return "LOW"
    return "LOW"


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------
def main() -> int:
    GOV.mkdir(parents=True, exist_ok=True)
    for sub in (
        "audits",
        "classification",
        "quarantine",
        "transitional",
        "unresolved",
        "manifests",
        "migration-history",
        "asset-intelligence",
        "deprecation",
        "reports",
    ):
        (GOV / sub).mkdir(parents=True, exist_ok=True)

    records = discover_assets()

    # Classify
    for r in records:
        cat, sub_label, recommendation = classify(r)
        r["category"] = cat
        r["sub_label"] = sub_label
        r["ownership_recommendation"] = recommendation
        r["knowledge_value"] = knowledge_value(r, cat, sub_label)

    # 1 — Repository asset inventory
    write_json(
        GOV / "audits" / "01-repository-asset-inventory.json",
        {
            "schema_version": SCHEMA,
            "generated_at": NOW,
            "total_records": len(records),
            "rule": "Inventory walks the workspace; opaque infrastructure dirs are summarised as single rows. Canonical Beslock product layers are enumerated and explicitly flagged is_canonical_layer=true.",
            "assets": records,
        },
    )

    # 2 — Classification report
    by_category: dict[str, list[dict]] = {}
    for r in records:
        by_category.setdefault(r["category"], []).append(
            {
                "path": r["path"],
                "sub_label": r["sub_label"],
                "knowledge_value": r["knowledge_value"],
                "ownership_recommendation": r["ownership_recommendation"],
                "size_bytes": r["size_bytes"],
            }
        )
    legend = {
        "A": "CANONICAL KNOWLEDGE — verified entities, validated workflows, promoted procedures",
        "B": "SOURCE EVIDENCE — OCR outputs, OEM mappings, scan artifacts",
        "C": "TRANSITIONAL SEMANTIC — drafts, partially normalized markdown, intermediate ETL",
        "D": "ORCHESTRATION — prompt packs, generation matrices, Comfy orchestration, visual runs",
        "E": "GOVERNANCE — schemas, architecture, provenance, lineage, builders, governance docs",
        "F": "LEGACY / UNKNOWN — ambiguous or historical migration remnants",
        "X": "INFRASTRUCTURE — WordPress core, deployment, env, ephemeral test outputs (out of scope)",
    }
    write_json(
        GOV / "classification" / "02-classification-report.json",
        {
            "schema_version": SCHEMA,
            "generated_at": NOW,
            "category_legend": legend,
            "category_counts": {k: len(v) for k, v in sorted(by_category.items())},
            "by_category": {k: sorted(v, key=lambda x: x["path"]) for k, v in by_category.items()},
        },
    )

    # 3 — Quarantine report (pointers, NEVER moves)
    quarantine = [
        {
            "path": r["path"],
            "category": r["category"],
            "sub_label": r["sub_label"],
            "size_bytes": r["size_bytes"],
            "mtime_iso": r["mtime_iso"],
            "reason": (
                "Ambiguous ownership or unclassified. Pointer recorded here; "
                "the asset itself was NOT moved or modified. Resolution requires "
                "human review."
            ),
            "ownership_recommendation": r["ownership_recommendation"],
        }
        for r in records
        if r["category"] == "F" or r["sub_label"] == "product-catalog-draft"
    ]
    write_json(
        GOV / "quarantine" / "03-quarantine-pointers.json",
        {
            "schema_version": SCHEMA,
            "generated_at": NOW,
            "policy": "Quarantine is a list of POINTERS. No file under any of these paths has been moved, copied, or modified by this audit. Quarantine != deletion.",
            "count": len(quarantine),
            "pointers": quarantine,
        },
    )
    # Per-asset quarantine receipts (for traceability, also non-destructive).
    for q in quarantine:
        eid = re.sub(r"[^a-z0-9]+", "-", q["path"].lower()).strip("-")
        write_json(
            GOV / "quarantine" / "items" / f"{eid}.json",
            {
                "schema_version": SCHEMA,
                "generated_at": NOW,
                "pointer": q,
                "physical_action_taken": "none",
                "reversible": True,
            },
        )

    # 4 — Duplicate analysis
    by_md5: dict[str, list[str]] = {}
    for r in records:
        if not r.get("md5") or r["md5"].startswith("head1m:"):
            continue
        by_md5.setdefault(r["md5"], []).append(r["path"])
    duplicates = [
        {"md5": k, "paths": sorted(v), "count": len(v)}
        for k, v in by_md5.items()
        if len(v) > 1
    ]
    duplicates.sort(key=lambda d: -d["count"])
    write_json(
        GOV / "audits" / "04-duplicate-analysis.json",
        {
            "schema_version": SCHEMA,
            "generated_at": NOW,
            "policy": "Duplicates are reported only — never silently merged. Conflicting manifests must be reconciled by a human.",
            "duplicate_groups": duplicates,
            "duplicate_group_count": len(duplicates),
        },
    )

    # 5 — Unresolved ownership report
    unresolved = [
        {
            "path": r["path"],
            "sub_label": r["sub_label"],
            "ownership_recommendation": r["ownership_recommendation"],
        }
        for r in records
        if r["category"] in ("C", "F")
        or (r["category"] == "D" and "future-relocate" in r["ownership_recommendation"])
        or (r["category"] == "E" and "future-relocate" in r["ownership_recommendation"])
    ]
    write_json(
        GOV / "unresolved" / "05-unresolved-ownership.json",
        {
            "schema_version": SCHEMA,
            "generated_at": NOW,
            "count": len(unresolved),
            "items": sorted(unresolved, key=lambda x: x["path"]),
        },
    )

    # 6 — Root cleanup proposal (per Task 8)
    target_root = ["ext-images/", "KNOWLEDGE_BUILDING/", "_repository-governance/", "shared/", "runtime/"]
    proposed_root_layout = {
        "ext-images/": "Symlink or move of `wp-content/themes/beslock-custom/User manuals/ext-images/` to repo root (DEFERRED — would require theme bootstrap update).",
        "KNOWLEDGE_BUILDING/": "Symlink or move of `wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/` to repo root (DEFERRED).",
        "_repository-governance/": "Symlink or move of `wp-content/themes/beslock-custom/User manuals/_repository-governance/` to repo root (DEFERRED).",
        "shared/": "New folder for cross-product shared assets (currently does not exist).",
        "runtime/": "New folder for ephemeral pipeline outputs (currently `output/`, `test-results/`, `.tmp*`, `generated_manuals*`).",
    }
    root_files_today = sorted({Path(r["path"]).parts[0] for r in records})
    write_json(
        GOV / "reports" / "06-root-cleanup-proposal.json",
        {
            "schema_version": SCHEMA,
            "generated_at": NOW,
            "target_root_directories": target_root,
            "proposed_root_layout": proposed_root_layout,
            "current_root_top_level": root_files_today,
            "policy": "This is a PROPOSAL. No file or directory has been moved by this audit. Cutover would require: (a) WordPress bootstrap path updates, (b) builder script path updates (knowledge_core_build.py, knowledge_core_semantic_enrich.py, etc.), (c) migration audit per moved artifact.",
        },
    )

    # 7 — Knowledge value scorecard
    value_counts: dict[str, int] = {}
    for r in records:
        value_counts[r["knowledge_value"]] = value_counts.get(r["knowledge_value"], 0) + 1
    sample_high = [r["path"] for r in records if r["knowledge_value"] == "HIGH"][:25]
    sample_low = [r["path"] for r in records if r["knowledge_value"] == "LOW"][:25]
    write_json(
        GOV / "asset-intelligence" / "07-knowledge-value-report.json",
        {
            "schema_version": SCHEMA,
            "generated_at": NOW,
            "value_counts": value_counts,
            "high_value_examples": sample_high,
            "low_value_examples": sample_low,
            "scoring_rules": {
                "HIGH": "category A canonical, category B source evidence, category D visual orchestration core, category E primary builders/architecture/governance",
                "MEDIUM": "category C transitional, secondary D/E (tooling, secondary docs)",
                "LOW": "category F legacy frontend-migration receipts and unclassified",
                "INFRA": "category X — WordPress / deployment / ephemeral",
            },
        },
    )

    # 8 — Recommended future deletions (NON-AUTOMATIC)
    deletions: list[dict] = []
    # Frontend migration summaries — only if the human confirms they are not needed for audit.
    for r in records:
        if r["sub_label"] == "frontend-migration-summary-legacy":
            deletions.append(
                {
                    "path": r["path"],
                    "category": r["category"],
                    "rationale": "Historical WordPress theme migration receipts; superseded by git history. Not Beslock product knowledge.",
                    "blockers_to_deletion": [
                        "human review required",
                        "archive copy must first be relocated to _repository-governance/migration-history/frontend-summaries/",
                    ],
                    "delete_action_taken": "none (proposal only)",
                }
            )
    # Duplicate OEM PDFs (already audited in Phase 2 inconsistencies report).
    for grp in duplicates:
        if any(p.endswith(".pdf") for p in grp["paths"]):
            deletions.append(
                {
                    "duplicate_group_md5": grp["md5"],
                    "paths": grp["paths"],
                    "rationale": "Byte-identical PDFs detected. Keep one canonical, archive the others as duplicate ledgers.",
                    "blockers_to_deletion": [
                        "human must designate the canonical copy",
                        "metadata/audit/duplicate-oem-sources.json must be created before deletion",
                    ],
                    "delete_action_taken": "none (proposal only)",
                }
            )
    write_json(
        GOV / "deprecation" / "08-recommended-deletions.json",
        {
            "schema_version": SCHEMA,
            "generated_at": NOW,
            "policy": "These are RECOMMENDATIONS. NO file has been deleted. Each item carries explicit blockers_to_deletion that must be cleared by a human before any removal.",
            "count": len(deletions),
            "recommendations": deletions,
        },
    )

    # 9 — Repository canonicalization status
    canon_count = sum(1 for r in records if r["is_canonical_layer"])
    non_canon_classified = sum(1 for r in records if r["category"] in ("A", "B", "C", "D", "E"))
    leftover = sum(1 for r in records if r["category"] == "F")
    infra = sum(1 for r in records if r["category"] == "X")
    total = len(records)
    write_json(
        GOV / "reports" / "09-canonicalization-status.json",
        {
            "schema_version": SCHEMA,
            "generated_at": NOW,
            "total_records": total,
            "canonical_layer_records": canon_count,
            "classified_non_canonical_records": non_canon_classified - canon_count,
            "legacy_or_unknown_records": leftover,
            "infrastructure_records": infra,
            "canonicalization_ratio": round(canon_count / max(1, total - infra), 3),
            "interpretation": (
                "Ratio of records inside canonical Beslock layers (ext-images, "
                "KNOWLEDGE_BUILDING, visual-system, _repository-governance, "
                "review-previews) over the non-infrastructure inventory."
            ),
        },
    )

    # 10 — Recommended (non-automatic) ownership moves
    moves = [
        {
            "from": r["path"],
            "category": r["category"],
            "sub_label": r["sub_label"],
            "ownership_recommendation": r["ownership_recommendation"],
        }
        for r in records
        if r["category"] in ("C", "D", "E", "F")
        and "future-relocate" in r.get("ownership_recommendation", "")
    ]
    write_json(
        GOV / "manifests" / "10-recommended-moves.json",
        {
            "schema_version": SCHEMA,
            "generated_at": NOW,
            "policy": "This is a MANIFEST. No file has been moved. Each entry is an ownership recommendation for a future, manually-triggered cutover.",
            "count": len(moves),
            "moves": sorted(moves, key=lambda m: m["from"]),
        },
    )

    # 00 — Summary
    summary_lines = [
        "# Phase 4 — Repository governance summary",
        "",
        f"_Generated {NOW} by `tools/repository_governance_audit.py`._",
        "",
        "## Hard guarantees",
        "",
        "- No file was moved.",
        "- No file was deleted.",
        "- No file was modified.",
        "- All actions are proposals or pointers under `_repository-governance/`.",
        "",
        "## Inventory at a glance",
        "",
        f"- Total records: **{total}** (includes {infra} infrastructure summaries).",
        f"- Canonical-layer records: **{canon_count}**.",
        f"- Legacy / unknown records: **{leftover}**.",
        f"- Canonicalisation ratio (excluding infra): **{round(canon_count / max(1, total - infra), 3)}**.",
        "",
        "## Category counts",
        "",
        "| Category | Description | Count |",
        "|---|---|---:|",
    ]
    for k in sorted(by_category):
        summary_lines.append(f"| {k} | {legend[k]} | {len(by_category[k])} |")
    summary_lines += [
        "",
        "## Knowledge-value distribution",
        "",
        "| Tier | Count |",
        "|---|---:|",
    ] + [f"| {k} | {v} |" for k, v in sorted(value_counts.items())]
    summary_lines += [
        "",
        "## Reports under this folder",
        "",
        "- `audits/01-repository-asset-inventory.json`",
        "- `classification/02-classification-report.json`",
        "- `quarantine/03-quarantine-pointers.json` (+ per-item receipts under `quarantine/items/`)",
        "- `audits/04-duplicate-analysis.json`",
        "- `unresolved/05-unresolved-ownership.json`",
        "- `reports/06-root-cleanup-proposal.json`",
        "- `asset-intelligence/07-knowledge-value-report.json`",
        "- `deprecation/08-recommended-deletions.json`",
        "- `reports/09-canonicalization-status.json`",
        "- `manifests/10-recommended-moves.json`",
        "",
        "## Critical rules honoured",
        "",
        "1. Did not delete any unknown files.",
        "2. Did not destroy provenance.",
        "3. Did not flatten lineage.",
        "4. Did not silently canonicalise ambiguous assets.",
        "5. Did not overwrite validated semantic artifacts.",
        "6. Did not recreate the manual-centric structure.",
        "7. Treated every asset as a potential knowledge artefact until proven otherwise.",
    ]
    (GOV / "00-SUMMARY.md").write_text("\n".join(summary_lines) + "\n")

    print(f"Repository governance audit complete: {len(records)} records.")
    print(f"  classified categories: { {k: len(v) for k, v in by_category.items()} }")
    print(f"  knowledge value: {value_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
