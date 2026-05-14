# Migration Risk Report

Generated: 2026-05-13T14:03:27Z

## Counts
- Moves executed this run: 197
- Duplicates encountered: 0
- Missing planned sources (already-migrated or absent): 64
- Errors: 0

## Known retained anomalies (provenance preservation)
- `ext-images/e-shield/source-of-truth/manuals/e-Shied_2.pdf` — OEM filename typo preserved verbatim per PHASE_1_IMPLEMENTATION.md §10. Validation ledger entry recorded.

## Transitional surfaces still present (allow-listed by REPOSITORY_BOUNDARIES.md §1)
- `manual-web-integration-manifest.json`, `manual-web-integration-matrix.md`, `manual-review-draft-index.md` (site-level delivery contracts; nucleus-only after Phase 2).
- `visual-system/` (shared rules and registries; product-specific subfolders evacuated).
- `review-previews/index.html` (multi-product index; per-product review previews migrated into nuclei).
- `installation-manual-template.md`, editorial standards, audits.

## Next cleanup priorities
1. Rewrite `manual-web-integration-manifest.json` to reference only nucleus paths (currently mixes legacy roots).
2. Update `tools/render_manual_review_drafts.py`, `tools/publish_review_drafts.py`, `tools/generate_reset_review_assets.py` to drop legacy-root fallbacks once all products are nucleus-resident.
3. Promote `KNOWLEDGE_BUILDING/legacy-architecture/*` content into the active governance set after diff review.
4. Populate each nucleus `structured-knowledge/` with normalized JSON per OEM_EXTRACTION_PIPELINE.md.
5. Replace per-nucleus `metadata/lineage/source-lineage.json` stub with full lineage entries linking to OCR staging artifacts under `generated_manuals/<slug>/`.
