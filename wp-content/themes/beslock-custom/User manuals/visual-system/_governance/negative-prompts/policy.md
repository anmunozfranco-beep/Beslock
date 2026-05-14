# Consolidated negative-prompt registry

_Schema: `visual-governance/1.0` · canonical policy · generated 2026-05-13T16:14:38Z._

## Intent

All future negative prompts MUST resolve to component IDs in this registry. Inline, ad-hoc negative strings duplicated across product ai-image-prompts.md files are deprecated and will be migrated.

## Authoritative source documents

This policy is a CONSOLIDATION POINTER. The rules themselves remain in the source documents listed below. Editing this policy does NOT edit the sources; conflicts are reported in `_repository-governance/reports/visual-governance/`.

- `ext-images/<product>/visual-system/prompts/ai-image-prompts.md (all 6 products)`
- `KNOWLEDGE_BUILDING/COMFY_GENERATION_GOVERNANCE.md (§4 prompt lineage)`

## Components

- **neg.shared.anti-marketing**:
  - marketing glamor
  - cinematic drama
  - photorealistic lifestyle staging
  - neon lighting
  - plastic render look
  - low resolution
- **neg.shared.anti-human**:
  - full human figure
  - human face
  - body-led scene
  - photorealistic people
  - realistic hand photo
  - extra fingers
- **neg.shared.anti-text**:
  - invented UI text
  - fake labels
  - fake readable app UI
- **neg.shared.anti-geometry**:
  - wrong geometry
  - mixed interior and exterior hardware in one frame
  - wrong lock-edge mechanism
  - floating objects
  - cluttered background
- **neg.shared.anti-generic-lock**:
  - standard keypad lever lock silhouette
  - knob lock silhouette
  - fingerprint sensor on the front panel
  - missing upper sensor cluster
  - merged display and handle
  - missing interior screen
  - rim-lock box geometry

## Per Product Negatives Pointer

Product-specific additions remain in ext-images/<product>/visual-system/prompts/ai-image-prompts.md and must declare the shared component IDs they extend.

## Anti Contamination Rule

neg.shared.anti-generic-lock currently appears verbatim in 6/6 products despite different geometries. Future migration: each product must declare which sub-bullets apply and add product-specific negatives under neg.<product>.* component IDs.
