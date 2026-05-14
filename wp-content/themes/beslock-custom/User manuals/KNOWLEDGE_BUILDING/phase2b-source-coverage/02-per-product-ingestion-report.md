# Phase 2B — Per-product ingestion report

_Generated 2026-05-13T14:51:24Z_

## e-flex

**Sources on disk**

| Filename | Category | Kind | Pages / Size | Ingestion | OCR | Semantic |
|---|---|---|---|---|---|---|
| `e-Flex app manual.md` | manuals | normalized-markdown | 2544 B | ingested | not-applicable | entities-emitted |
| `e-Flex installation manual.md` | manuals | normalized-markdown | 5227 B | ingested | not-applicable | entities-emitted |
| `e-Flex user manual.pdf` *(dup)* | manuals | oem-pdf | 8 pages | ignored-by-design | ocr-completed | extracted-text-only |
| `e-Flex_1.pdf` *(dup)* | manuals | oem-pdf | 8 pages | ignored-by-design | ocr-not-attempted | no-entities-emitted |
| `e-Flex - supplemental source review.md` | specifications | normalized-markdown | 3915 B | missing | not-applicable | no-entities-emitted |

_PDF renders on disk_: e-flex-1: 9

**Extractor view**

- Sources used: 2
- Sources reported missing: []
- Sections seen: 26
- Entities emitted: 63
- Bucket counts: {'capabilities': 2, 'operation': 2, 'workflows': 3, 'warning': 2, 'installation': 14, 'terminology': 8, 'ocr-evidence': 32}
- Gaps: ['Missing normalized user manual under source-of-truth/manuals/.']
- Ambiguities: 2

**OCR fallback view**

- Method: `ocrmypdf`
- Pages: 8
- Avg confidence: 88.0
- Sections detected: 32
- Steps detected: 27
- App instructions detected: 5
- Warnings detected: 3

**Knowledge nucleus view**

- entities: 63
- procedures: 2
- workflows: 3
- warnings: 2
- terminology: 8
- troubleshooting: 0
- capabilities: 2
- installation_flows: 14
- configuration: 0
- faq: 0
- extracted_text: 32

**Quality scorecard**

- provenance_complete: 1.0
- non_duplicated: 1.0
- classification_meaningful: 1.0
- lineage_to_oem: 1.0
- procedure_step_completeness: 0.0
- knowledge_breadth: 0.67
- procedures_total: 2
- procedures_with_no_steps: 2
- rag_ready: 0.784
- duplicate_id_count: 0
- entities_missing_source_refs: 0
- misclassified_troubleshooting: 0

## e-nova

**Sources on disk**

| Filename | Category | Kind | Pages / Size | Ingestion | OCR | Semantic |
|---|---|---|---|---|---|---|
| `e-Nova user manual.pdf` | manuals | oem-pdf | 10 pages | ignored-by-design | ocr-completed | extracted-text-only |

**Extractor view**

- Sources used: 0
- Sources reported missing: ['wp-content/themes/beslock-custom/User manuals/ext-images/e-nova/source-of-truth/manuals']
- Sections seen: 0
- Entities emitted: 14
- Bucket counts: {'ocr-evidence': 14}
- Gaps: ['No normalized markdown manuals available under wp-content/themes/beslock-custom/User manuals/ext-images/e-nova/source-of-truth/manuals; only OCR fallback will be emitted.', 'Missing normalized user manual under source-of-truth/manuals/.', 'Missing normalized installation manual under source-of-truth/manuals/.', 'Missing normalized app manual under source-of-truth/manuals/.']
- Ambiguities: 0

**OCR fallback view**

- Method: `pytesseract`
- Pages: 10
- Avg confidence: 84.3
- Sections detected: 14
- Steps detected: 8
- App instructions detected: 9
- Warnings detected: 1

**Knowledge nucleus view**

- entities: 14
- procedures: 0
- workflows: 0
- warnings: 0
- terminology: 0
- troubleshooting: 0
- capabilities: 0
- installation_flows: 0
- configuration: 0
- faq: 0
- extracted_text: 14

**Quality scorecard**

- provenance_complete: 1.0
- non_duplicated: 1.0
- classification_meaningful: 1.0
- lineage_to_oem: 0.5
- procedure_step_completeness: 1.0
- knowledge_breadth: 0.0
- procedures_total: 0
- procedures_with_no_steps: 0
- rag_ready: 0.725
- duplicate_id_count: 0
- entities_missing_source_refs: 0
- misclassified_troubleshooting: 0

## e-orbit

**Sources on disk**

| Filename | Category | Kind | Pages / Size | Ingestion | OCR | Semantic |
|---|---|---|---|---|---|---|
| `e-Orbit - implementation starter pack.md` | manuals | normalized-markdown | 5450 B | ingested | not-applicable | entities-emitted |
| `e-Orbit - supplemental source review.md` | manuals | normalized-markdown | 4551 B | ingested | not-applicable | entities-emitted |
| `e-Orbit app manual.md` | manuals | normalized-markdown | 4517 B | ingested | not-applicable | entities-emitted |
| `e-Orbit user manual.md` | manuals | normalized-markdown | 6848 B | ingested | not-applicable | entities-emitted |
| `e-Orbit user manual.pdf` | manuals | oem-pdf | 2 pages | ignored-by-design | ocr-completed | extracted-text-only |
| `e-Orbit_2.pdf` | manuals | oem-pdf | 17 pages | ignored-by-design | ocr-not-attempted | no-entities-emitted |
| `e-Orbit_1.xls` | specifications | oem-spreadsheet | 29696 B | ignored-by-design | not-applicable-binary-spreadsheet | no-entities-emitted |

_PDF renders on disk_: e-orbit-2: 18

**Extractor view**

- Sources used: 4
- Sources reported missing: []
- Sections seen: 91
- Entities emitted: 109
- Bucket counts: {'capabilities': 4, 'troubleshooting': 1, 'installation': 1, 'operation': 8, 'workflows': 3, 'configuration': 1, 'terminology': 11, 'ocr-evidence': 80}
- Gaps: ['Missing normalized installation manual under source-of-truth/manuals/.']
- Ambiguities: 1

**OCR fallback view**

- Method: `ocrmypdf`
- Pages: 2
- Avg confidence: 92.0
- Sections detected: 80
- Steps detected: 8
- App instructions detected: 10
- Warnings detected: 16

**Knowledge nucleus view**

- entities: 107
- procedures: 9
- workflows: 3
- warnings: 0
- terminology: 11
- troubleshooting: 1
- capabilities: 2
- installation_flows: 1
- configuration: 0
- faq: 0
- extracted_text: 80

**Quality scorecard**

- provenance_complete: 1.0
- non_duplicated: 0.982
- classification_meaningful: 0.0
- lineage_to_oem: 1.0
- procedure_step_completeness: 0.889
- knowledge_breadth: 0.78
- procedures_total: 9
- procedures_with_no_steps: 1
- rag_ready: 0.788
- duplicate_id_count: 1
- entities_missing_source_refs: 0
- misclassified_troubleshooting: 1

## e-prime

**Sources on disk**

| Filename | Category | Kind | Pages / Size | Ingestion | OCR | Semantic |
|---|---|---|---|---|---|---|
| `e-Prime app manual.md` | manuals | normalized-markdown | 2961 B | ingested | not-applicable | entities-emitted |
| `e-Prime installation manual.md` | manuals | normalized-markdown | 5456 B | ingested | not-applicable | entities-emitted |
| `e-Prime user manual.pdf` | manuals | oem-pdf | 8 pages | ignored-by-design | ocr-completed | extracted-text-only |
| `e-Prime_1.pdf` | manuals | oem-pdf | 6 pages | ignored-by-design | ocr-not-attempted | no-entities-emitted |
| `e-Prime_2.pdf` | manuals | oem-pdf | 7 pages | ignored-by-design | ocr-not-attempted | no-entities-emitted |
| `e-Prime - supplemental source review.md` | specifications | normalized-markdown | 4812 B | missing | not-applicable | no-entities-emitted |

_PDF renders on disk_: e-prime-1: 7, e-prime-2: 8

**Extractor view**

- Sources used: 2
- Sources reported missing: []
- Sections seen: 26
- Entities emitted: 65
- Bucket counts: {'capabilities': 2, 'operation': 2, 'workflows': 2, 'warning': 2, 'installation': 14, 'terminology': 7, 'ocr-evidence': 36}
- Gaps: ['Missing normalized user manual under source-of-truth/manuals/.']
- Ambiguities: 2

**OCR fallback view**

- Method: `ocrmypdf`
- Pages: 8
- Avg confidence: 92.0
- Sections detected: 36
- Steps detected: 27
- App instructions detected: 6
- Warnings detected: 3

**Knowledge nucleus view**

- entities: 65
- procedures: 2
- workflows: 2
- warnings: 2
- terminology: 7
- troubleshooting: 0
- capabilities: 2
- installation_flows: 14
- configuration: 0
- faq: 0
- extracted_text: 36

**Quality scorecard**

- provenance_complete: 1.0
- non_duplicated: 1.0
- classification_meaningful: 1.0
- lineage_to_oem: 1.0
- procedure_step_completeness: 0.0
- knowledge_breadth: 0.67
- procedures_total: 2
- procedures_with_no_steps: 2
- rag_ready: 0.784
- duplicate_id_count: 0
- entities_missing_source_refs: 0
- misclassified_troubleshooting: 0

## e-shield

**Sources on disk**

| Filename | Category | Kind | Pages / Size | Ingestion | OCR | Semantic |
|---|---|---|---|---|---|---|
| `e-Shied_2.pdf` | manuals | oem-pdf | 1 pages | ignored-by-design | ocr-not-attempted | no-entities-emitted |
| `e-Shield app manual.md` | manuals | normalized-markdown | 5812 B | ingested | not-applicable | entities-emitted |
| `e-Shield installation manual.md` | manuals | normalized-markdown | 5695 B | ingested | not-applicable | entities-emitted |
| `e-Shield user manual.pdf` | manuals | oem-pdf | 20 pages | ignored-by-design | ocr-completed | extracted-text-only |
| `e-Shield_1.pdf` | manuals | oem-pdf | 2 pages | ignored-by-design | ocr-not-attempted | no-entities-emitted |
| `e-Shield - supplemental source review.md` | specifications | normalized-markdown | 3939 B | missing | not-applicable | no-entities-emitted |

_PDF renders on disk_: e-shield-1: 3, e-shield-2: 2

**Extractor view**

- Sources used: 2
- Sources reported missing: []
- Sections seen: 32
- Entities emitted: 62
- Bucket counts: {'capabilities': 1, 'workflows': 9, 'troubleshooting': 1, 'warning': 1, 'installation': 12, 'terminology': 5, 'ocr-evidence': 33}
- Gaps: ['Missing normalized user manual under source-of-truth/manuals/.']
- Ambiguities: 0

**OCR fallback view**

- Method: `pytesseract`
- Pages: 20
- Avg confidence: 84.9
- Sections detected: 33
- Steps detected: 3
- App instructions detected: 30
- Warnings detected: 2

**Knowledge nucleus view**

- entities: 62
- procedures: 0
- workflows: 9
- warnings: 1
- terminology: 5
- troubleshooting: 1
- capabilities: 1
- installation_flows: 12
- configuration: 0
- faq: 0
- extracted_text: 33

**Quality scorecard**

- provenance_complete: 1.0
- non_duplicated: 1.0
- classification_meaningful: 1.0
- lineage_to_oem: 1.0
- procedure_step_completeness: 1.0
- knowledge_breadth: 0.67
- procedures_total: 0
- procedures_with_no_steps: 0
- rag_ready: 0.934
- duplicate_id_count: 0
- entities_missing_source_refs: 0
- misclassified_troubleshooting: 0

## e-touch

**Sources on disk**

| Filename | Category | Kind | Pages / Size | Ingestion | OCR | Semantic |
|---|---|---|---|---|---|---|
| `e-Touch app manual.md` | manuals | normalized-markdown | 3986 B | ingested | not-applicable | entities-emitted |
| `e-Touch installation manual.md` | manuals | normalized-markdown | 4133 B | ingested | not-applicable | entities-emitted |
| `e-Touch user manual.pdf` *(dup)* | manuals | oem-pdf | 2 pages | ignored-by-design | ocr-completed | extracted-text-only |
| `e-Touch_1.pdf` *(dup)* | manuals | oem-pdf | 2 pages | ignored-by-design | ocr-not-attempted | no-entities-emitted |
| `e-Touch - supplemental source review.md` | specifications | normalized-markdown | 3505 B | missing | not-applicable | no-entities-emitted |

_PDF renders on disk_: e-touch-1: 3

**Extractor view**

- Sources used: 2
- Sources reported missing: []
- Sections seen: 24
- Entities emitted: 98
- Bucket counts: {'capabilities': 1, 'operation': 2, 'workflows': 1, 'warning': 1, 'installation': 11, 'terminology': 7, 'ocr-evidence': 75}
- Gaps: ['Missing normalized user manual under source-of-truth/manuals/.']
- Ambiguities: 2

**OCR fallback view**

- Method: `ocrmypdf`
- Pages: 2
- Avg confidence: 92.0
- Sections detected: 75
- Steps detected: 7
- App instructions detected: 39
- Warnings detected: 2

**Knowledge nucleus view**

- entities: 98
- procedures: 2
- workflows: 1
- warnings: 1
- terminology: 7
- troubleshooting: 0
- capabilities: 1
- installation_flows: 11
- configuration: 0
- faq: 0
- extracted_text: 75

**Quality scorecard**

- provenance_complete: 1.0
- non_duplicated: 1.0
- classification_meaningful: 1.0
- lineage_to_oem: 1.0
- procedure_step_completeness: 0.0
- knowledge_breadth: 0.67
- procedures_total: 2
- procedures_with_no_steps: 2
- rag_ready: 0.784
- duplicate_id_count: 0
- entities_missing_source_refs: 0
- misclassified_troubleshooting: 0
