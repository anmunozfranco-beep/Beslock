# Knowledge Debt Governance

## Debt classes

| id | blocking | description |
|---|---|---|
| `unresolved-gap` | False | Known missing knowledge area; tracked but not blocking promotion of unrelated artifacts. |
| `ocr-confidence-debt` | False | Content derived from OCR below confidence threshold; requires human pass. |
| `low-confidence-region` | False | Cluster of inferred artifacts in one domain; needs targeted review. |
| `missing-specification` | True | Procedure references a spec that does not exist; blocks promotion of dependents. |
| `unresolved-semantic` | True | Ambiguity escalation that did not resolve; blocks canonicalization. |
| `governance-todo` | False | Open governance principle / authority gap; tracked at doctrine level. |
| `blocked-domain` | True | Whole semantic domain blocked pending OEM input; blocks promotion within domain. |
| `lineage-debt` | True | Deprecated/superseded artifact missing successor link. |
| `maturity-debt` | False | Promoted artifact whose dependencies are not yet promoted. |

## Rules

- All debt items have: id, class, owner, opened-date, blocking-flag, related-artifact-ids.
- Blocking debt prevents promotion of dependent artifacts but never destroys lineage.
- Debt items are closed only by an explicit resolution event (resolved / wont-fix / superseded-by).
- Wont-fix debt MUST record rationale and reviewer.
