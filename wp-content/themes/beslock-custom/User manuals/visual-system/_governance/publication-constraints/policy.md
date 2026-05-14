# Publication-channel constraints (DRAFT — gap)

_Schema: `visual-governance/1.0` · canonical policy · generated 2026-05-13T16:14:38Z._

## Intent

Per-channel publication constraints (resolution, aspect, color space, format, file-size, alt-text schema) are NOT yet defined. Today the channel targets are declared in publication-intent-map.json per product but the per-channel delivery spec is absent. This policy file is a placeholder marking the gap; it must be populated before mass Comfy orchestration begins.

## Authoritative source documents

This policy is a CONSOLIDATION POINTER. The rules themselves remain in the source documents listed below. Editing this policy does NOT edit the sources; conflicts are reported in `_repository-governance/reports/visual-governance/`.

- `ext-images/<product>/knowledge-core/publication-intent/publication-intent-map.json`
- `tools/visual_generation.py (FORMAT_DIMENSIONS hardcoded)`
- `visual-system/shared/visual-rules/app-ui-policy.md`

## Channels

- web
- pdf
- support
- onboarding
- chatbot
- rag
- api

## Format Dimensions Today

- **16:9**:
  - 1536
  - 864
- **4:3**:
  - 1408
  - 1056
- **4:5**:
  - 1024
  - 1280
- **1:1**:
  - 1024
  - 1024

## Open Questions

- color space and bit depth per channel
- file format + compression per channel
- required alt-text schema per channel
- load-time / bandwidth caps per channel
- dimension validation hook in visual_generation.py
