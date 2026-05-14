# Phase 4 — Repository governance summary

_Generated 2026-05-13T15:46:30Z by `tools/repository_governance_audit.py`._

## Hard guarantees

- No file was moved.
- No file was deleted.
- No file was modified.
- All actions are proposals or pointers under `_repository-governance/`.

## Inventory at a glance

- Total records: **4337** (includes 449 infrastructure summaries).
- Canonical-layer records: **2476**.
- Legacy / unknown records: **24**.
- Canonicalisation ratio (excluding infra): **0.637**.

## Category counts

| Category | Description | Count |
|---|---|---:|
| A | CANONICAL KNOWLEDGE — verified entities, validated workflows, promoted procedures | 1693 |
| B | SOURCE EVIDENCE — OCR outputs, OEM mappings, scan artifacts | 238 |
| C | TRANSITIONAL SEMANTIC — drafts, partially normalized markdown, intermediate ETL | 14 |
| D | ORCHESTRATION — prompt packs, generation matrices, Comfy orchestration, visual runs | 1403 |
| E | GOVERNANCE — schemas, architecture, provenance, lineage, builders, governance docs | 516 |
| F | LEGACY / UNKNOWN — ambiguous or historical migration remnants | 24 |
| X | INFRASTRUCTURE — WordPress core, deployment, env, ephemeral test outputs (out of scope) | 449 |

## Knowledge-value distribution

| Tier | Count |
|---|---:|
| HIGH | 2592 |
| INFRA | 449 |
| LOW | 24 |
| MEDIUM | 1272 |

## Reports under this folder

- `audits/01-repository-asset-inventory.json`
- `classification/02-classification-report.json`
- `quarantine/03-quarantine-pointers.json` (+ per-item receipts under `quarantine/items/`)
- `audits/04-duplicate-analysis.json`
- `unresolved/05-unresolved-ownership.json`
- `reports/06-root-cleanup-proposal.json`
- `asset-intelligence/07-knowledge-value-report.json`
- `deprecation/08-recommended-deletions.json`
- `reports/09-canonicalization-status.json`
- `manifests/10-recommended-moves.json`

## Critical rules honoured

1. Did not delete any unknown files.
2. Did not destroy provenance.
3. Did not flatten lineage.
4. Did not silently canonicalise ambiguous assets.
5. Did not overwrite validated semantic artifacts.
6. Did not recreate the manual-centric structure.
7. Treated every asset as a potential knowledge artefact until proven otherwise.
