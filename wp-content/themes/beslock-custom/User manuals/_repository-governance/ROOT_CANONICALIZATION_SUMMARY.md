# Root canonicalization summary

_Generated 2026-05-13T15:59:53Z by `tools/root_canonicalize_md_json.py`._

## Scope

- Repository-root `.md` and `.json` only.
- Loose `.md` / `.json` directly inside `wp-content/themes/beslock-custom/User manuals/` only.
- All other assets, semantic layers, knowledge-core, orchestration, and Comfy systems were untouched.

## Hard guarantees

- No file deleted.
- No file overwritten (collisions abort the move).
- `git mv` used wherever possible to preserve rename history.
- Per-asset `.lineage.json` receipt written next to every relocated file.

## Counts

- Planned: **31**
- Executed: **31**
- Skipped: **0**
- Failed: **0**
- Cleanliness score: **1.0**

## Destinations used

- `_repository-governance/migration-history/frontend-summaries/` — 15 frontend WordPress migration receipts.
- `_repository-governance/manifests/architecture/` — `ARCHITECTURE.md`, `FRONTEND_ARCHITECTURE.md`.
- `_repository-governance/manifests/frontend-conventions/` — `BEM_GUIDELINES.md`.
- `_repository-governance/migration-history/plans/` — `CLEANUP_PLAN.md`, `COMPONENT_MIGRATION_PLAN.md`.
- `_repository-governance/manifests/visual-orchestration-doc/` — `VISUAL_GENERATION_AUTOMATION.md` (documentation only; pipeline untouched).
- `_repository-governance/quarantine/data-products/` — `data/products.json` (ambiguous ownership).
- `_repository-governance/transitional/manual-standards/` — loose `User manuals/manual-*.md` + `manual-web-integration-manifest.json` + `ai-project-context-export.md` + `installation-manual-template.md`.
- `_repository-governance/transitional/visual-system-audits/` — `visual-system-current-state-audit.md`.

## Reports emitted (under `_repository-governance/`)

1. `reports/executed-moves-report.json`
2. `unresolved/unresolved-assets-report.json`
3. `reports/canonical-root-status.json`
4. `reports/duplicate-resolution-report.json`
5. `reports/lineage-preservation-report.json`
6. `reports/repository-cleanliness-score.json`

## Remaining loose `.md` / `.json` at repo root: ['README.md']

Expected after this phase: `README.md` only.
