# Phase 3 — Semantic enrichment + visual orchestration prep

_Generated 2026-05-13T15:40:35Z by `tools/knowledge_core_semantic_enrich.py`._

## Per-product enrichment inventory

| Product | proc-semantics | components | visual-intents | visual-risks | publication routing | comfy-ready |
|---|---:|---:|---:|---:|---:|:---:|
| e-flex | 9 | 7 | 6 | 4 | 66 | ✅ |
| e-nova | 0 | 1 | 1 | 1 | 17 | ❌ |
| e-orbit | 24 | 4 | 7 | 3 | 169 | ✅ |
| e-prime | 9 | 7 | 5 | 3 | 91 | ✅ |
| e-shield | 13 | 5 | 6 | 4 | 71 | ✅ |
| e-touch | 4 | 9 | 5 | 4 | 101 | ✅ |

## Visual orchestration score

| Product | score |
|---|---:|
| e-flex | 0.817 |
| e-nova | 0.069 |
| e-orbit | 0.738 |
| e-prime | 0.778 |
| e-shield | 0.757 |
| e-touch | 0.852 |

## Reports in this folder

- 01-semantic-enrichment-coverage.json
- 02-visual-orchestration-readiness.json
- 03-comfy-automation-opportunities.json
- 04-aggregate-semantic-gaps.json

## Critical rules honoured

- No manuals, PDFs, websites, marketing, or images generated.
- No invented hardware, sensors, components, or procedures.
- All enrichment vocabulary-anchored against existing knowledge-core entities.
- ComfyUI is the only authorised downstream visual generator (recorded in every visual-intent).
- Every emitted artifact carries source_refs + extraction_lineage.
- Gaps recorded explicitly per product in `semantic-gaps.json`.
