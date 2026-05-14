# Knowledge Lifecycle

## Stages

| order | id | terminal | description |
|---|---|---|---|
| 1 | `discovered` | False | Source material identified (OEM PDF, image, web), no semantic interpretation yet. |
| 2 | `extracted` | False | Raw content extracted from source (text, structure, references). |
| 3 | `ocr-derived` | False | Content obtained via OCR; explicitly flagged for confidence review. |
| 4 | `inferred` | False | Semantic shape inferred from extracted/OCR content; not yet normalized. |
| 5 | `normalized` | False | Conformed to ontology vocabulary, id format, and shared terminology. |
| 6 | `canonicalized` | False | Single authoritative representation chosen across duplicates/synonyms/bilingual variants. |
| 7 | `verified` | False | Reviewed by human/OEM checkpoint; lineage and evidence cross-validated. |
| 8 | `promoted` | False | Granted operational authority; usable by retrieval, onboarding, troubleshooting models. |
| 9 | `deprecated` | False | Marked for retirement; still readable; flagged not-for-new-use. |
| 10 | `superseded` | False | Replaced by a newer canonical artifact; lineage link to successor required. |
| 11 | `archived` | True | Removed from active surfaces; retained for audit/lineage; never re-promoted. |
| 12 | `unresolved` | False | Cannot progress without human/OEM input; tracked as knowledge debt. |

## Allowed transitions

- `discovered` → `extracted`
- `extracted` → `ocr-derived`
- `extracted` → `inferred`
- `ocr-derived` → `inferred`
- `inferred` → `normalized`
- `inferred` → `unresolved`
- `normalized` → `canonicalized`
- `normalized` → `unresolved`
- `canonicalized` → `verified`
- `canonicalized` → `unresolved`
- `verified` → `promoted`
- `verified` → `deprecated`
- `promoted` → `deprecated`
- `promoted` → `superseded`
- `deprecated` → `superseded`
- `deprecated` → `archived`
- `superseded` → `archived`
- `unresolved` → `normalized`
- `unresolved` → `archived`

Any transition not listed above is a governance violation.
