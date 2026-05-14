"""Phase 1 — Repository Knowledge Core Cutover.

Migrates the legacy `User manuals/` flat structure into product-knowledge nuclei
under `User manuals/ext-images/<slug>/`, mirroring the canonical e-orbit layout
and obeying KNOWLEDGE_BUILDING governance documents.

Idempotent. Safe to re-run; already-moved files are reported, not re-moved.

Run from repo root:
    python tools/phase1_cutover.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANUAL_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
EXT_IMAGES = MANUAL_ROOT / "ext-images"

PRODUCTS = [
    # (slug, display, pdf_basenames_in_root)
    ("e-flex",   "e-Flex",   ["e-Flex_1.pdf"]),
    ("e-nova",   "e-Nova",   []),
    ("e-prime",  "e-Prime",  ["e-Prime_1.pdf", "e-Prime_2.pdf"]),
    ("e-shield", "e-Shield", ["e-Shield_1.pdf", "e-Shied_2.pdf"]),  # OEM typo preserved
    ("e-touch",  "e-Touch",  ["e-Touch_1.pdf"]),
]

# Six mandatory top-level folders + canonical subfolders mirroring e-orbit reference.
NUCLEUS_DIRS = [
    "source-of-truth/manuals",
    "source-of-truth/manuals/pdf-renders",
    "source-of-truth/specifications",
    "source-of-truth/product-images",
    "source-of-truth/visual-evidence",
    "structured-knowledge/features",
    "structured-knowledge/procedures",
    "structured-knowledge/semantic-relations",
    "visual-system/references",
    "visual-system/anchors",
    "visual-system/prompts",
    "visual-system/conditioning",
    "visual-system/qa",
    "visual-system/generation-matrices",
    "visual-system/validations",
    "visual-system/outputs/generated",
    "visual-system/outputs/review-draft",
    "visual-system/outputs/web-ready",
    "publishing/web/assets",
    "publishing/web/manuals",
    "publishing/web/review-previews",
    "publishing/pdf/drafts",
    "publishing/pdf/image-ready",
    "publishing/support",
    "automation/orchestrators",
    "automation/runs",
    "metadata/lineage",
    "metadata/manifests",
    "metadata/validation",
    "metadata/audit/legacy-flat-files",
    "metadata/audit/legacy-visual-system-product",
    "metadata/traceability",
]

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Migration log
moves: list[dict] = []
skipped: list[dict] = []
missing: list[dict] = []
duplicates: list[dict] = []
errors: list[dict] = []


def git_mv(src: Path, dst: Path) -> str:
    """Move src -> dst. Use git mv when both inside repo and src tracked; fall back to shutil."""
    if not src.exists():
        missing.append({"src": str(src.relative_to(REPO_ROOT))})
        return "missing"
    if dst.exists():
        # If identical content, treat src as duplicate -> remove src.
        try:
            if src.is_file() and dst.is_file() and src.read_bytes() == dst.read_bytes():
                duplicates.append({
                    "src": str(src.relative_to(REPO_ROOT)),
                    "dst": str(dst.relative_to(REPO_ROOT)),
                    "action": "duplicate-removed",
                })
                _git_rm(src)
                return "duplicate-removed"
        except Exception as e:  # noqa: BLE001
            errors.append({"op": "compare", "src": str(src), "dst": str(dst), "error": str(e)})
        duplicates.append({
            "src": str(src.relative_to(REPO_ROOT)),
            "dst": str(dst.relative_to(REPO_ROOT)),
            "action": "destination-exists-DIFFERENT-kept-both",
        })
        # Quarantine the source under audit
        slug = _slug_from_dst(dst)
        if slug:
            quarantine = EXT_IMAGES / slug / "metadata/audit/legacy-flat-files" / src.name
            quarantine.parent.mkdir(parents=True, exist_ok=True)
            try:
                _git_move(src, quarantine)
                duplicates[-1]["quarantined_to"] = str(quarantine.relative_to(REPO_ROOT))
                return "duplicate-quarantined"
            except Exception as e:  # noqa: BLE001
                errors.append({"op": "quarantine", "src": str(src), "error": str(e)})
        return "duplicate-kept"
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        _git_move(src, dst)
    except Exception as e:  # noqa: BLE001
        errors.append({"op": "mv", "src": str(src), "dst": str(dst), "error": str(e)})
        return "error"
    moves.append({
        "src": str(src.relative_to(REPO_ROOT)),
        "dst": str(dst.relative_to(REPO_ROOT)),
    })
    return "moved"


def _git_move(src: Path, dst: Path) -> None:
    # Try git mv first; fall back to shutil.move when src is untracked.
    res = subprocess.run(
        ["git", "mv", str(src), str(dst)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        # git mv failed (typically: source not tracked). Use plain move.
        if not src.exists():
            return
        shutil.move(str(src), str(dst))


def _git_rm(path: Path) -> None:
    res = subprocess.run(
        ["git", "rm", "-f", str(path)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    if res.returncode != 0 and path.exists():
        path.unlink()


def _slug_from_dst(dst: Path) -> str | None:
    try:
        rel = dst.relative_to(EXT_IMAGES)
        return rel.parts[0]
    except ValueError:
        return None


def ensure_nucleus_skeleton(slug: str) -> None:
    base = EXT_IMAGES / slug
    base.mkdir(parents=True, exist_ok=True)
    for d in NUCLEUS_DIRS:
        p = base / d
        p.mkdir(parents=True, exist_ok=True)
        keep = p / ".gitkeep"
        if not any(p.iterdir()) and not keep.exists():
            keep.write_text("")


def write_metadata_stubs(slug: str, display: str) -> None:
    base = EXT_IMAGES / slug
    lineage_path = base / "metadata/lineage/source-lineage.json"
    if not lineage_path.exists():
        lineage_path.write_text(json.dumps({
            "product_slug": slug,
            "product_display": display,
            "schema_version": "0.1.0",
            "generated_at": NOW,
            "phase": "phase-1-cutover",
            "entries": [
                {
                    "src": m["src"],
                    "dst": m["dst"],
                    "operation": "promoted",
                    "promoted_at": NOW,
                }
                for m in moves
                if f"/ext-images/{slug}/" in m["dst"]
            ],
        }, indent=2) + "\n")

    manifest_path = base / "metadata/manifests/product-domain-manifest.json"
    if not manifest_path.exists():
        manifest_path.write_text(json.dumps({
            "product_slug": slug,
            "product_display": display,
            "schema_version": "0.1.0",
            "generated_at": NOW,
            "canonical_png": f"ext-images/{slug}/source-of-truth/product-images/{display}.png",
            "approved_sources": _list_relative(base / "source-of-truth"),
            "publishing_surfaces": _list_relative(base / "publishing"),
            "visual_system": _list_relative(base / "visual-system"),
        }, indent=2) + "\n")

    validation_path = base / "metadata/validation/validation-ledger.json"
    if not validation_path.exists():
        ledger = {
            "product_slug": slug,
            "schema_version": "0.1.0",
            "generated_at": NOW,
            "open_items": [],
        }
        if slug == "e-shield":
            ledger["open_items"].append({
                "id": "oem-filename-typo",
                "severity": "info",
                "summary": "OEM-supplied PDF filename uses 'e-Shied_2.pdf' (missing 'l').",
                "policy": "Filename preserved verbatim under source-of-truth/manuals/ for provenance; normalized references use the slug 'e-shield'.",
                "source_ref": "ext-images/e-shield/source-of-truth/manuals/e-Shied_2.pdf",
                "recorded_at": NOW,
            })
        validation_path.write_text(json.dumps(ledger, indent=2) + "\n")

    orch_path = base / "automation/orchestrators/orchestration-manifest.json"
    if not orch_path.exists():
        orch_path.write_text(json.dumps({
            "product_slug": slug,
            "schema_version": "0.1.0",
            "generated_at": NOW,
            "phase": "phase-1-cutover",
            "starter_packs": _list_files(base / "automation/orchestrators", suffix=".md"),
            "runs": [],
        }, indent=2) + "\n")


def _list_relative(root: Path) -> list[str]:
    if not root.exists():
        return []
    out: list[str] = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name not in (".gitkeep", ".DS_Store"):
            out.append(str(p.relative_to(REPO_ROOT)))
    return out


def _list_files(root: Path, suffix: str) -> list[str]:
    if not root.exists():
        return []
    return sorted(
        str(p.relative_to(REPO_ROOT))
        for p in root.glob(f"*{suffix}")
    )


def migrate_product(slug: str, display: str, root_pdfs: list[str]) -> None:
    base = EXT_IMAGES / slug

    # 1. Root flat markdown files
    flat_root_map = {
        f"{display} - AI image prompts.md":            base / "visual-system/prompts" / f"{display} - AI image prompts.md",
        f"{display} - image generation matrix.md":     base / "visual-system/generation-matrices" / f"{display} - image generation matrix.md",
        f"{display} - implementation starter pack.md": base / "automation/orchestrators" / f"{display} - implementation starter pack.md",
        f"{display} - installation template standard.md": base / "automation/orchestrators" / f"{display} - installation template standard.md",
        f"{display} - supplemental source review.md":  base / "source-of-truth/specifications" / f"{display} - supplemental source review.md",
        f"{display} app manual.md":                    base / "source-of-truth/manuals" / f"{display} app manual.md",
        f"{display} installation manual.md":           base / "source-of-truth/manuals" / f"{display} installation manual.md",
        f"{display} user manual - image-ready.md":     base / "publishing/web/manuals" / f"{display} user manual - image-ready.md",
        f"{display} user manual - review-draft.md":    base / "publishing/web/manuals" / f"{display} user manual - review-draft.md",
        f"{display} user manual.pdf":                  base / "source-of-truth/manuals" / f"{display} user manual.pdf",
    }
    for name, dst in flat_root_map.items():
        src = MANUAL_ROOT / name
        git_mv(src, dst)

    # 2. OEM PDF variants
    for pdf_name in root_pdfs:
        git_mv(MANUAL_ROOT / pdf_name, base / "source-of-truth/manuals" / pdf_name)

    # 3. Compatibility PNG at ext-images root
    png_src = EXT_IMAGES / f"{display}.png"
    png_dst = base / "source-of-truth/product-images" / f"{display}.png"
    git_mv(png_src, png_dst)

    # 4. Pre-existing misplaced files inside the nucleus
    visual_profile = base / f"{slug}-visual-profile.md"
    git_mv(visual_profile, base / "visual-system/references" / f"{slug}-visual-profile.md")
    notes = base / "notes.md"
    git_mv(notes, base / "metadata/audit" / "legacy-pre-cutover-notes.md")

    # 5. Legacy visual-system/products/<slug>/
    legacy_vs = MANUAL_ROOT / "visual-system/products" / slug
    if legacy_vs.exists():
        vs_map = {
            "ai-image-prompts.md":           base / "visual-system/prompts" / "ai-image-prompts.md",
            "image-generation-matrix.md":    base / "visual-system/generation-matrices" / "image-generation-matrix.md",
            "visual-validation.md":          base / "visual-system/validations" / "visual-validation.md",
            "image-production-status.md":    base / "visual-system/qa" / "image-production-status.md",
            "README.md":                     base / "metadata/audit/legacy-visual-system-product" / "README.md",
        }
        for name, dst in vs_map.items():
            git_mv(legacy_vs / name, dst)
        # generated/
        gen_dir = legacy_vs / "generated"
        if gen_dir.exists():
            for child in sorted(gen_dir.iterdir()):
                if child.name.endswith(".webp"):
                    git_mv(child, base / "visual-system/outputs/generated" / child.name)
                elif child.name == "selected-assets-register.md":
                    git_mv(child, base / "metadata/traceability" / "selected-assets-register.md")
                elif child.name == "README.md":
                    git_mv(child, base / "metadata/audit/legacy-visual-system-product" / "generated-README.md")
                else:
                    git_mv(child, base / "metadata/audit/legacy-visual-system-product" / child.name)
            _rmdir_if_empty(gen_dir)
        _rmdir_if_empty(legacy_vs)

    # 6. Legacy assets/<slug>/
    legacy_assets = MANUAL_ROOT / "assets" / slug
    if legacy_assets.exists():
        # review-draft + web-ready -> publishing/web/assets/<slug>/{review-draft,web-ready}/
        for sub in ("review-draft", "web-ready"):
            sd = legacy_assets / sub
            if sd.exists():
                target = base / "publishing/web/assets" / slug / sub
                target.mkdir(parents=True, exist_ok=True)
                for f in sorted(sd.iterdir()):
                    if f.is_file():
                        git_mv(f, target / f.name)
                _rmdir_if_empty(sd)
        # pdf-renders -> source-of-truth/manuals/pdf-renders/
        pdfr = legacy_assets / "pdf-renders"
        if pdfr.exists():
            target = base / "source-of-truth/manuals/pdf-renders"
            for run_dir in sorted(pdfr.iterdir()):
                if run_dir.is_dir():
                    for f in sorted(run_dir.iterdir()):
                        if f.is_file():
                            git_mv(f, target / run_dir.name / f.name)
                    _rmdir_if_empty(run_dir)
            _rmdir_if_empty(pdfr)
        readme = legacy_assets / "README.md"
        git_mv(readme, base / "metadata/audit/legacy-flat-files" / "assets-README.md")
        _rmdir_if_empty(legacy_assets)

    # 7. review-previews/<slug>-user-manual-review-draft.html
    rp = MANUAL_ROOT / "review-previews" / f"{slug}-user-manual-review-draft.html"
    git_mv(rp, base / "publishing/web/review-previews" / f"{slug}-user-manual-review-draft.html")


def _rmdir_if_empty(p: Path) -> None:
    if p.exists() and p.is_dir():
        # Drop .DS_Store first
        ds = p / ".DS_Store"
        if ds.exists():
            try:
                ds.unlink()
            except OSError:
                pass
        try:
            p.rmdir()
        except OSError:
            pass


def relocate_architecture_dir() -> None:
    src = MANUAL_ROOT / "architecture"
    if not src.exists():
        return
    dst_root = MANUAL_ROOT / "KNOWLEDGE_BUILDING/legacy-architecture"
    dst_root.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.iterdir()):
        if f.is_file():
            git_mv(f, dst_root / f.name)
    _rmdir_if_empty(src)


def cleanup_emptied() -> None:
    for sub in ("assets", "review-previews", "visual-system/products"):
        p = MANUAL_ROOT / sub
        if p.exists() and p.is_dir():
            # Remove emptied per-product subfolders if present
            for child in list(p.iterdir()):
                if child.is_dir():
                    _rmdir_if_empty(child)
            _rmdir_if_empty(p)
    # Drop stale .DS_Store
    for ds in MANUAL_ROOT.rglob(".DS_Store"):
        try:
            ds.unlink()
        except OSError:
            pass


def write_reports() -> None:
    rep_dir = MANUAL_ROOT / "KNOWLEDGE_BUILDING/migrations/phase-1-cutover"
    rep_dir.mkdir(parents=True, exist_ok=True)

    # JSON master
    (rep_dir / "moved-files-inventory.json").write_text(
        json.dumps({"generated_at": NOW, "moves": moves}, indent=2) + "\n"
    )

    # Markdown moved-files inventory
    lines = ["# Moved Files Inventory", "", f"Generated: {NOW}", f"Total moves: {len(moves)}", ""]
    lines.append("| # | Source | Destination |")
    lines.append("|---|--------|-------------|")
    for i, m in enumerate(moves, 1):
        lines.append(f"| {i} | `{m['src']}` | `{m['dst']}` |")
    (rep_dir / "moved-files-inventory.md").write_text("\n".join(lines) + "\n")

    # Duplicates
    lines = ["# Duplicate Artifacts Report", "", f"Generated: {NOW}", f"Total: {len(duplicates)}", ""]
    if duplicates:
        lines.append("| # | Source | Destination | Action |")
        lines.append("|---|--------|-------------|--------|")
        for i, d in enumerate(duplicates, 1):
            quarantine = d.get("quarantined_to", "")
            action = d["action"]
            if quarantine:
                action = f"{action} → `{quarantine}`"
            lines.append(f"| {i} | `{d['src']}` | `{d['dst']}` | {action} |")
    else:
        lines.append("_None detected._")
    (rep_dir / "duplicate-artifacts.md").write_text("\n".join(lines) + "\n")

    # Missing
    lines = ["# Missing Source Files", "", f"Generated: {NOW}", f"Total: {len(missing)}", ""]
    if missing:
        for m in missing:
            lines.append(f"- `{m['src']}` (planned source not present; expected if previously migrated)")
    else:
        lines.append("_None._")
    (rep_dir / "missing-sources.md").write_text("\n".join(lines) + "\n")

    # Errors
    lines = ["# Migration Errors", "", f"Generated: {NOW}", f"Total: {len(errors)}", ""]
    if errors:
        for e in errors:
            lines.append(f"- {e}")
    else:
        lines.append("_None._")
    (rep_dir / "migration-errors.md").write_text("\n".join(lines) + "\n")

    # Remaining legacy root
    legacy_remaining: list[str] = []
    allow_files = {
        "ai-project-context-export.md",
        "installation-manual-template.md",
        "manual-document-package-maturity-matrix.md",
        "manual-document-package-standard.md",
        "manual-review-draft-index.md",
        "manual-standardization-current-state-audit.md",
        "manual-web-integration-manifest.json",
        "manual-web-integration-matrix.md",
        "visual-system-current-state-audit.md",
    }
    allow_dirs = {"KNOWLEDGE_BUILDING", "ext-images", "visual-system", "review-previews"}
    for child in sorted(MANUAL_ROOT.iterdir()):
        name = child.name
        if name == ".DS_Store":
            continue
        if child.is_file() and name in allow_files:
            continue
        if child.is_dir() and name in allow_dirs:
            continue
        legacy_remaining.append(str(child.relative_to(REPO_ROOT)))

    lines = ["# Remaining Legacy-Root Files", "", f"Generated: {NOW}", ""]
    if legacy_remaining:
        lines.append("Items still present at `User manuals/` root that are NOT in the allow-list:")
        lines.append("")
        for r in legacy_remaining:
            lines.append(f"- `{r}`")
    else:
        lines.append("_Root is clean per REPOSITORY_BOUNDARIES.md §1._")
    (rep_dir / "remaining-legacy-root.md").write_text("\n".join(lines) + "\n")

    # Orphans (per nucleus, files in unexpected positions)
    orphans: list[str] = []
    expected_top = {"source-of-truth", "structured-knowledge", "visual-system",
                    "publishing", "automation", "metadata"}
    for slug, _, _ in PRODUCTS:
        base = EXT_IMAGES / slug
        for child in base.iterdir():
            if child.is_dir() and child.name not in expected_top:
                orphans.append(str(child.relative_to(REPO_ROOT)))
            if child.is_file() and child.name not in {".gitkeep"}:
                orphans.append(str(child.relative_to(REPO_ROOT)))
    lines = ["# Orphaned / Non-Conforming Nucleus Members", "", f"Generated: {NOW}", ""]
    if orphans:
        for o in orphans:
            lines.append(f"- `{o}`")
    else:
        lines.append("_All nuclei conform to PRODUCT_NUCLEUS_RULES.md §1._")
    (rep_dir / "orphaned-files.md").write_text("\n".join(lines) + "\n")

    # Unresolved references — scan for likely-broken legacy paths in tracked text files
    unresolved: list[str] = []
    legacy_substrings = [
        "User manuals/assets/",
        "User manuals/visual-system/products/",
        "User manuals/review-previews/",
        "User manuals/architecture/",
    ]
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "node_modules", "wp-content/uploads", "vendor"}
               for part in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".json", ".php", ".py", ".js", ".html", ".txt"}:
            continue
        try:
            text = path.read_text(errors="ignore")
        except Exception:  # noqa: BLE001
            continue
        for needle in legacy_substrings:
            if needle in text:
                unresolved.append(f"{path.relative_to(REPO_ROOT)} → contains `{needle}`")
                break
    lines = ["# Unresolved References Report", "", f"Generated: {NOW}",
             f"Files referencing now-migrated legacy paths: {len(unresolved)}", ""]
    if unresolved:
        for u in unresolved:
            lines.append(f"- {u}")
    else:
        lines.append("_None._")
    (rep_dir / "unresolved-references.md").write_text("\n".join(lines) + "\n")

    # Migration risk report
    risk_lines = [
        "# Migration Risk Report",
        "",
        f"Generated: {NOW}",
        "",
        "## Counts",
        f"- Moves executed this run: {len(moves)}",
        f"- Duplicates encountered: {len(duplicates)}",
        f"- Missing planned sources (already-migrated or absent): {len(missing)}",
        f"- Errors: {len(errors)}",
        "",
        "## Known retained anomalies (provenance preservation)",
        "- `ext-images/e-shield/source-of-truth/manuals/e-Shied_2.pdf` — OEM filename typo preserved verbatim per PHASE_1_IMPLEMENTATION.md §10. Validation ledger entry recorded.",
        "",
        "## Transitional surfaces still present (allow-listed by REPOSITORY_BOUNDARIES.md §1)",
        "- `manual-web-integration-manifest.json`, `manual-web-integration-matrix.md`, `manual-review-draft-index.md` (site-level delivery contracts; nucleus-only after Phase 2).",
        "- `visual-system/` (shared rules and registries; product-specific subfolders evacuated).",
        "- `review-previews/index.html` (multi-product index; per-product review previews migrated into nuclei).",
        "- `installation-manual-template.md`, editorial standards, audits.",
        "",
        "## Next cleanup priorities",
        "1. Rewrite `manual-web-integration-manifest.json` to reference only nucleus paths (currently mixes legacy roots).",
        "2. Update `tools/render_manual_review_drafts.py`, `tools/publish_review_drafts.py`, `tools/generate_reset_review_assets.py` to drop legacy-root fallbacks once all products are nucleus-resident.",
        "3. Promote `KNOWLEDGE_BUILDING/legacy-architecture/*` content into the active governance set after diff review.",
        "4. Populate each nucleus `structured-knowledge/` with normalized JSON per OEM_EXTRACTION_PIPELINE.md.",
        "5. Replace per-nucleus `metadata/lineage/source-lineage.json` stub with full lineage entries linking to OCR staging artifacts under `generated_manuals/<slug>/`.",
    ]
    (rep_dir / "migration-risk-report.md").write_text("\n".join(risk_lines) + "\n")

    # Index
    (rep_dir / "README.md").write_text(
        "# Phase 1 Cutover — Reports\n\n"
        f"Generated: {NOW}\n\n"
        "- [moved-files-inventory.md](moved-files-inventory.md)\n"
        "- [duplicate-artifacts.md](duplicate-artifacts.md)\n"
        "- [missing-sources.md](missing-sources.md)\n"
        "- [orphaned-files.md](orphaned-files.md)\n"
        "- [remaining-legacy-root.md](remaining-legacy-root.md)\n"
        "- [unresolved-references.md](unresolved-references.md)\n"
        "- [migration-errors.md](migration-errors.md)\n"
        "- [migration-risk-report.md](migration-risk-report.md)\n"
        "- [moved-files-inventory.json](moved-files-inventory.json)\n"
    )


def main() -> None:
    print(f"Phase 1 cutover starting at {NOW}")
    # Build skeletons first
    for slug, _, _ in PRODUCTS:
        ensure_nucleus_skeleton(slug)
    # Migrate per product
    for slug, display, root_pdfs in PRODUCTS:
        print(f"  -> migrating {slug}")
        migrate_product(slug, display, root_pdfs)
    # Architecture relocation
    relocate_architecture_dir()
    # Cleanup emptied legacy parent dirs
    cleanup_emptied()
    # Write metadata stubs
    for slug, display, _ in PRODUCTS:
        write_metadata_stubs(slug, display)
    # Reports
    write_reports()
    print(f"Done. moves={len(moves)} dupes={len(duplicates)} missing={len(missing)} errors={len(errors)}")


if __name__ == "__main__":
    main()
