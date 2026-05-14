#!/usr/bin/env python3
"""Phase 5 — Root markdown/JSON canonicalization (NON-DESTRUCTIVE moves).

Scope: ONLY .md / .json assets at the repository root and loose .md / .json
inside `wp-content/themes/beslock-custom/User manuals/`. Nothing else is
touched.

Hard rules:
  * No file is deleted.
  * No file is overwritten — collisions abort that single move.
  * `git mv` is used when the source is tracked, preserving history; otherwise
    a plain filesystem move is used so the rename is still reversible.
  * A lineage manifest is recorded next to each destination AND a global
    `executed-moves-report.json` is written under `_repository-governance/`.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content/themes/beslock-custom/User manuals"
GOV = USER_MANUALS / "_repository-governance"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SCHEMA = "repo-governance/1.0"

# (relative_source, relative_destination, category, sub_label, rationale)
FRONTEND_SUMMARIES = [
    "ACTIVE_BOOTSTRAP_CONSOLIDATION_SUMMARY.md",
    "HEADER_CSS_CONSOLIDATION_SUMMARY.md",
    "HEADER_MIGRATION_SUMMARY.md",
    "HEADER_RUNTIME_CLEANUP_SUMMARY.md",
    "HOMEPAGE_SURFACE_MIGRATION_SUMMARY.md",
    "LEGACY_RUNTIME_AUDIT_SUMMARY.md",
    "MAIN_CSS_DECOMPOSITION_SUMMARY.md",
    "PRIMARY_BOOTSTRAP_CONSOLIDATION_SUMMARY.md",
    "PRODUCT_CARD_CONSOLIDATION_SUMMARY.md",
    "PRODUCT_CARD_MIGRATION_SUMMARY.md",
    "PRODUCT_CARD_PRESENTATION_OWNERSHIP_SUMMARY.md",
    "PRODUCT_CARD_RUNTIME_OWNERSHIP_SUMMARY.md",
    "STOREFRONT_OWNERSHIP_SUMMARY.md",
    "UTILITIES_MIGRATION_SUMMARY.md",
    "WORKTREE_NORMALIZATION_SUMMARY.md",
]

GOV_REL = GOV.relative_to(REPO).as_posix()

PLAN: list[tuple[str, str, str, str, str]] = []

# Frontend summaries → migration-history/frontend-summaries/
for name in FRONTEND_SUMMARIES:
    PLAN.append(
        (
            name,
            f"{GOV_REL}/migration-history/frontend-summaries/{name}",
            "F",
            "frontend-migration-summary-legacy",
            "Historical WordPress theme migration receipt; not Beslock product knowledge. Relocated to migration history per recommended-moves manifest.",
        )
    )

# Architecture / convention docs → manifests/
PLAN += [
    ("ARCHITECTURE.md",          f"{GOV_REL}/manifests/architecture/ARCHITECTURE.md",          "E", "architecture",          "Repository-wide architecture doc. Relocated to governance manifests."),
    ("FRONTEND_ARCHITECTURE.md", f"{GOV_REL}/manifests/architecture/FRONTEND_ARCHITECTURE.md", "E", "architecture",          "Frontend architecture doc. Relocated to governance manifests."),
    ("BEM_GUIDELINES.md",        f"{GOV_REL}/manifests/frontend-conventions/BEM_GUIDELINES.md","E", "frontend-conventions",  "Frontend convention doc. Relocated to governance manifests."),
    ("CLEANUP_PLAN.md",          f"{GOV_REL}/migration-history/plans/CLEANUP_PLAN.md",         "E", "migration-plan",        "Historical migration plan. Relocated to migration history."),
    ("COMPONENT_MIGRATION_PLAN.md", f"{GOV_REL}/migration-history/plans/COMPONENT_MIGRATION_PLAN.md", "E", "migration-plan", "Historical migration plan. Relocated to migration history."),
    # Documentation only — does NOT touch the visual pipeline itself.
    ("VISUAL_GENERATION_AUTOMATION.md", f"{GOV_REL}/manifests/visual-orchestration-doc/VISUAL_GENERATION_AUTOMATION.md", "D", "visual-orchestration-doc", "Documentation of the visual generation orchestrator. Relocated as a manifest reference only — no pipeline code is modified."),
]

# Quarantine: ambiguous storefront vs. knowledge-core asset.
PLAN.append(
    (
        "data/products.json",
        f"{GOV_REL}/quarantine/data-products/products.json",
        "C",
        "product-catalog-draft",
        "Ambiguous ownership (legacy storefront vs. knowledge-core product list). Quarantined pending human classification.",
    )
)

# `User manuals/` loose markdown standardisation drafts → transitional.
USER_MANUALS_REL = USER_MANUALS.relative_to(REPO).as_posix()
LOOSE_USER_MANUALS_TRANSITIONAL = [
    "ai-project-context-export.md",
    "installation-manual-template.md",
    "manual-document-package-maturity-matrix.md",
    "manual-document-package-standard.md",
    "manual-review-draft-index.md",
    "manual-standardization-current-state-audit.md",
    "manual-web-integration-matrix.md",
    "manual-web-integration-manifest.json",
]
for name in LOOSE_USER_MANUALS_TRANSITIONAL:
    PLAN.append(
        (
            f"{USER_MANUALS_REL}/{name}",
            f"{GOV_REL}/transitional/manual-standards/{name}",
            "C",
            "manual-standardization-draft",
            "Loose manual-standardisation draft inside the canonical area but not owned by any product nucleus. Marked transitional pending human ownership decision.",
        )
    )

# Loose visual-system audit doc → transitional (documentation only).
PLAN.append(
    (
        f"{USER_MANUALS_REL}/visual-system-current-state-audit.md",
        f"{GOV_REL}/transitional/visual-system-audits/visual-system-current-state-audit.md",
        "C",
        "visual-system-audit-draft",
        "Audit doc of the visual system. Relocated as transitional documentation only — no visual pipeline code is touched.",
    )
)


def is_tracked(path: Path) -> bool:
    try:
        subprocess.check_output(
            ["git", "ls-files", "--error-unmatch", str(path.relative_to(REPO))],
            cwd=REPO,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def execute() -> dict:
    moved: list[dict] = []
    skipped: list[dict] = []
    failures: list[dict] = []
    for src_rel, dst_rel, category, sub_label, rationale in PLAN:
        src = REPO / src_rel
        dst = REPO / dst_rel
        if not src.exists():
            skipped.append({"source": src_rel, "destination": dst_rel, "reason": "source-missing"})
            continue
        if dst.exists():
            skipped.append({"source": src_rel, "destination": dst_rel, "reason": "destination-exists (collision; not overwritten)"})
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        tracked = is_tracked(src)
        method = "git-mv" if tracked else "fs-mv"
        try:
            if tracked:
                subprocess.check_output(
                    ["git", "mv", str(src.relative_to(REPO)), str(dst.relative_to(REPO))],
                    cwd=REPO,
                    stderr=subprocess.STDOUT,
                )
            else:
                shutil.move(str(src), str(dst))
        except Exception as exc:  # noqa: BLE001
            failures.append({"source": src_rel, "destination": dst_rel, "method": method, "error": str(exc)})
            continue
        moved.append(
            {
                "source": src_rel,
                "destination": dst_rel,
                "method": method,
                "tracked_in_git": tracked,
                "category": category,
                "sub_label": sub_label,
                "rationale": rationale,
            }
        )
        # Per-asset lineage receipt next to the destination.
        receipt = dst.with_suffix(dst.suffix + ".lineage.json")
        if not receipt.exists():
            receipt.write_text(
                json.dumps(
                    {
                        "schema_version": SCHEMA,
                        "asset": dst_rel,
                        "previous_path": src_rel,
                        "moved_at": NOW,
                        "method": method,
                        "tracked_in_git_before_move": tracked,
                        "category": category,
                        "sub_label": sub_label,
                        "rationale": rationale,
                        "reversible": True,
                        "reversal_command": f"git mv {dst_rel!r} {src_rel!r}" if tracked else f"mv {dst_rel!r} {src_rel!r}",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
    return {"moved": moved, "skipped": skipped, "failures": failures}


def write_reports(result: dict) -> None:
    moved, skipped, failures = result["moved"], result["skipped"], result["failures"]

    # 1 — executed-moves-report
    (GOV / "reports").mkdir(parents=True, exist_ok=True)
    (GOV / "reports" / "executed-moves-report.json").write_text(
        json.dumps(
            {
                "schema_version": SCHEMA,
                "generated_at": NOW,
                "scope": "root markdown / json + loose User manuals/ markdown / json",
                "moved_count": len(moved),
                "skipped_count": len(skipped),
                "failure_count": len(failures),
                "moved": moved,
                "skipped": skipped,
                "failures": failures,
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    # 2 — unresolved-assets-report
    unresolved = [m for m in moved if m["category"] in ("C", "F")]
    (GOV / "unresolved" / "unresolved-assets-report.json").write_text(
        json.dumps(
            {
                "schema_version": SCHEMA,
                "generated_at": NOW,
                "definition": "Assets relocated to transitional/quarantine destinations awaiting human ownership decision.",
                "count": len(unresolved),
                "items": unresolved,
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    # 3 — canonical-root-status
    remaining_root = sorted(
        p.name for p in REPO.iterdir()
        if p.is_file() and p.suffix.lower() in (".md", ".json")
    )
    target_root = ["ext-images/", "KNOWLEDGE_BUILDING/", "_repository-governance/", "shared/", "runtime/"]
    (GOV / "reports" / "canonical-root-status.json").write_text(
        json.dumps(
            {
                "schema_version": SCHEMA,
                "generated_at": NOW,
                "target_root_directories": target_root,
                "remaining_root_md_or_json": remaining_root,
                "expected_remaining": ["README.md"],
                "is_clean": remaining_root == ["README.md"],
                "notes": (
                    "Target directories ext-images/, KNOWLEDGE_BUILDING/, _repository-governance/ "
                    "currently live under wp-content/themes/beslock-custom/User manuals/ (canonical "
                    "Beslock layer). shared/ and runtime/ are deferred to a separate phase and are "
                    "not created here."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    # 4 — duplicate-resolution-report (no md/json duplicates were resolved by
    # this phase; we only report what we observed and confirm none were merged)
    md_json_duplicates_handled: list[dict] = []
    (GOV / "reports" / "duplicate-resolution-report.json").write_text(
        json.dumps(
            {
                "schema_version": SCHEMA,
                "generated_at": NOW,
                "policy": "No duplicate markdown or JSON assets were silently merged. All moves in this phase were 1:1 relocations of unique files. Duplicate manifests detected by the Phase 4 audit (mostly visual-generation snapshots) are out of scope.",
                "handled_count": 0,
                "handled": md_json_duplicates_handled,
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    # 5 — lineage-preservation-report
    (GOV / "reports" / "lineage-preservation-report.json").write_text(
        json.dumps(
            {
                "schema_version": SCHEMA,
                "generated_at": NOW,
                "policy": "Every move preserves provenance via (a) git rename detection where the source was tracked, and (b) a per-asset .lineage.json receipt written next to the destination.",
                "git_mv_count": sum(1 for m in moved if m["method"] == "git-mv"),
                "fs_mv_count": sum(1 for m in moved if m["method"] == "fs-mv"),
                "lineage_receipts_emitted": [m["destination"] + ".lineage.json" for m in moved],
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    # 6 — repository-cleanliness-score
    total_planned = len(PLAN)
    moved_count = len(moved)
    score = round(moved_count / max(1, total_planned), 3)
    (GOV / "reports" / "repository-cleanliness-score.json").write_text(
        json.dumps(
            {
                "schema_version": SCHEMA,
                "generated_at": NOW,
                "planned_moves": total_planned,
                "executed_moves": moved_count,
                "skipped_moves": len(skipped),
                "failed_moves": len(failures),
                "remaining_loose_root_md_or_json": remaining_root,
                "score": score,
                "interpretation": (
                    "1.0 = every planned md/json move executed. <1.0 means some moves were "
                    "skipped (collision or source missing) and require manual review."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    # ROOT_CANONICALIZATION_SUMMARY.md (lives inside _repository-governance/, not root)
    lines = [
        "# Root canonicalization summary",
        "",
        f"_Generated {NOW} by `tools/root_canonicalize_md_json.py`._",
        "",
        "## Scope",
        "",
        "- Repository-root `.md` and `.json` only.",
        "- Loose `.md` / `.json` directly inside `wp-content/themes/beslock-custom/User manuals/` only.",
        "- All other assets, semantic layers, knowledge-core, orchestration, and Comfy systems were untouched.",
        "",
        "## Hard guarantees",
        "",
        "- No file deleted.",
        "- No file overwritten (collisions abort the move).",
        "- `git mv` used wherever possible to preserve rename history.",
        "- Per-asset `.lineage.json` receipt written next to every relocated file.",
        "",
        "## Counts",
        "",
        f"- Planned: **{total_planned}**",
        f"- Executed: **{moved_count}**",
        f"- Skipped: **{len(skipped)}**",
        f"- Failed: **{len(failures)}**",
        f"- Cleanliness score: **{score}**",
        "",
        "## Destinations used",
        "",
        "- `_repository-governance/migration-history/frontend-summaries/` — 15 frontend WordPress migration receipts.",
        "- `_repository-governance/manifests/architecture/` — `ARCHITECTURE.md`, `FRONTEND_ARCHITECTURE.md`.",
        "- `_repository-governance/manifests/frontend-conventions/` — `BEM_GUIDELINES.md`.",
        "- `_repository-governance/migration-history/plans/` — `CLEANUP_PLAN.md`, `COMPONENT_MIGRATION_PLAN.md`.",
        "- `_repository-governance/manifests/visual-orchestration-doc/` — `VISUAL_GENERATION_AUTOMATION.md` (documentation only; pipeline untouched).",
        "- `_repository-governance/quarantine/data-products/` — `data/products.json` (ambiguous ownership).",
        "- `_repository-governance/transitional/manual-standards/` — loose `User manuals/manual-*.md` + `manual-web-integration-manifest.json` + `ai-project-context-export.md` + `installation-manual-template.md`.",
        "- `_repository-governance/transitional/visual-system-audits/` — `visual-system-current-state-audit.md`.",
        "",
        "## Reports emitted (under `_repository-governance/`)",
        "",
        "1. `reports/executed-moves-report.json`",
        "2. `unresolved/unresolved-assets-report.json`",
        "3. `reports/canonical-root-status.json`",
        "4. `reports/duplicate-resolution-report.json`",
        "5. `reports/lineage-preservation-report.json`",
        "6. `reports/repository-cleanliness-score.json`",
        "",
        f"## Remaining loose `.md` / `.json` at repo root: {remaining_root}",
        "",
        "Expected after this phase: `README.md` only.",
    ]
    (GOV / "ROOT_CANONICALIZATION_SUMMARY.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    GOV.mkdir(parents=True, exist_ok=True)
    for sub in ("manifests/architecture", "manifests/frontend-conventions",
                "manifests/visual-orchestration-doc", "migration-history/frontend-summaries",
                "migration-history/plans", "quarantine/data-products",
                "transitional/manual-standards", "transitional/visual-system-audits",
                "unresolved", "reports"):
        (GOV / sub).mkdir(parents=True, exist_ok=True)
    result = execute()
    write_reports(result)
    print(f"Executed {len(result['moved'])} of {len(PLAN)} planned moves.")
    print(f"Skipped: {len(result['skipped'])}  Failures: {len(result['failures'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
