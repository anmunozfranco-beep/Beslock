# Mechanical consistency policy

_Schema: `visual-governance/1.0` · canonical policy · generated 2026-05-13T16:14:38Z._

## Intent

Every generated visual of a given product MUST preserve the same mechanical identity: bolt spacing, latch position, deadbolt geometry, mortise structure, sensor placement, keypad grid, handle proportions, camera-cluster layout and visible locking architecture. Tolerances are inherited from `PRODUCT_VISUAL_TRUTH.md`.

## Authoritative source documents

This policy is a CONSOLIDATION POINTER. The rules themselves remain in the source documents listed below. Editing this policy does NOT edit the sources; conflicts are reported in `_repository-governance/reports/visual-governance/`.

- `KNOWLEDGE_BUILDING/PRODUCT_VISUAL_TRUTH.md`
- `KNOWLEDGE_BUILDING/PRODUCT_NUCLEUS_RULES.md`
- `ext-images/<product>/visual-system/references/<product>-visual-profile.md`
- `ext-images/<product>/knowledge-core/component-visibility/component-visibility-map.json`
- `visual-system/shared/visual-rules/product-truth-policy.md`

## Immutable Attributes

- silhouette
- component-count and component-positions
- sensor positions and count
- keypad grid (rows, columns, spacing)
- screen position / size / aspect
- indicator-LED positions
- handle geometry and mounting orientation
- visible mounting hardware (screws, bezels, gaskets)
- material identity per visible region
- brand marks, logos, certifications visible in canonical PNG

## Tolerances

- **position_drift_px_at_1024_ref**: 4
- **rotation_drift_deg**: 1
- **scale_drift_pct**: 1
- **material_region_drift_px**: 0
