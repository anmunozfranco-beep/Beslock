# Knowledge Health Monitoring

## Indicators

| id | severity | detection |
|---|---|---|
| `stale-procedure` | medium | promoted artifact unchanged > review-cycle and no recent OEM source |
| `orphan-entity` | medium | entity referenced by no procedure / workflow / capability |
| `unresolved-reference` | high | reference target id not present in canonical set |
| `maturity-inconsistency` | medium | promoted artifact whose dependencies are still semantic-candidate |
| `duplicated-semantic` | high | two canonical artifacts with overlapping intent (synonym/bilingual collision) |
| `governance-conflict` | high | two doctrine docs assert contradictory rules in the same authority area |
| `ontology-fragmentation` | high | domain referenced with diverging field shapes across products |
| `low-confidence-overload` | medium | ratio of ocr-derived/inferred content above per-product threshold |
| `lineage-break` | critical | deprecated/superseded artifact missing successor link |
| `promotion-without-evidence` | critical | verified-truth artifact missing source provenance |

## Thresholds

- `low_confidence_ratio_max`: 0.35
- `stale_procedure_review_cycle_days`: 365
- `orphan_entity_grace_days`: 90
- `lineage_break_tolerance`: 0
- `promotion_without_evidence_tolerance`: 0
