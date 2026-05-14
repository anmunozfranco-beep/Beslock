# Phase 2 — Semantic operationalization summary

_Generated 2026-05-13T15:18:31Z by `tools/knowledge_core_build.py`._

## Per-product knowledge-core inventory

| Product | install | operation | workflows | trbl | warn | term | entities | cap | spec | semantic | prov | visual | orch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| e-flex | 14 | 2 | 3 | 0 | 2 | 8 | 2 | 3 | 0 | 44 | 1 | 1 | 1 |
| e-nova | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 0 | 20 | 1 | 1 | 1 |
| e-orbit | 1 | 25 | 9 | 0 | 10 | 20 | 2 | 4 | 1 | 110 | 1 | 1 | 2 |
| e-prime | 14 | 2 | 2 | 0 | 4 | 7 | 2 | 3 | 0 | 69 | 1 | 1 | 1 |
| e-shield | 12 | 0 | 9 | 1 | 3 | 5 | 2 | 2 | 0 | 50 | 1 | 1 | 1 |
| e-touch | 11 | 2 | 1 | 0 | 1 | 7 | 2 | 2 | 0 | 87 | 1 | 1 | 1 |

## Completeness score (see report 04)

| Product | breadth | normalized? | verified-layer? | composite |
|---|---|---|---|---|
| e-flex | 0.778 | True | False | 0.711 |
| e-nova | 0.222 | False | False | 0.189 |
| e-orbit | 0.889 | True | True | 0.956 |
| e-prime | 0.778 | True | False | 0.711 |
| e-shield | 0.778 | True | False | 0.711 |
| e-touch | 0.778 | True | False | 0.711 |

## Reports in this folder

- 01-semantic-extraction-coverage.json
- 02-unresolved-ocr-risks.json
- 03-missing-oem-knowledge.json
- 04-semantic-completeness-scorecard.json
- 05-visual-orchestration-readiness.json
- 06-comfyui-integration-readiness.json
- 07-repository-inconsistencies.json
- 08-manual-generation-readiness.json

## Critical rules honoured

- Did not generate final manuals.
- Did not generate PDFs.
- Did not generate marketing assets.
- Did not generate website pages.
- Did not invent hardware, sensors, app functionality, lock states, or capabilities.
- All visual orchestration metadata enforces ComfyUI-only downstream.
- Every emitted entity carries source_refs + extraction_lineage.
