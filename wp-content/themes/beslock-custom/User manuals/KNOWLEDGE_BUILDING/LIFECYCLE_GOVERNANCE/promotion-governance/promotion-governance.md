# Semantic Promotion Governance

## Promotion levels

| rank | id | description |
|---|---|---|
| 0 | `evidence` | Raw OEM source or extracted artifact; not citable as truth. |
| 1 | `semantic-candidate` | Inferred semantic shape; speculative; never user-facing. |
| 2 | `normalized-artifact` | Conforms to ontology and id rules; safe for internal cross-reference. |
| 3 | `canonical-knowledge` | One authoritative representation; safe for retrieval indexing. |
| 4 | `verified-truth` | Human/OEM-verified; safe for safety-critical surfaces and onboarding. |

## Promotion criteria

- `evidence` → `semantic-candidate` requires: source-traceability, extraction-method-recorded
- `semantic-candidate` → `normalized-artifact` requires: ontology-conformance, id-format-valid, terminology-aligned
- `normalized-artifact` → `canonical-knowledge` requires: duplicate-resolution, synonym-merge, bilingual-merge, cross-product-collision-resolved
- `canonical-knowledge` → `verified-truth` requires: human-review-pass OR oem-confirmation, evidence-link, no-open-debt-of-blocking-class

## Authority

- `semantic-candidate` — automated-pipeline
- `normalized-artifact` — automated-pipeline + ontology-validator
- `canonical-knowledge` — automated-pipeline + canonicalization-resolver
- `verified-truth` — human-reviewer OR OEM-confirmation

## Lineage

Every promotion records: previous-level, evidence-link, reviewer (where applicable), timestamp.
