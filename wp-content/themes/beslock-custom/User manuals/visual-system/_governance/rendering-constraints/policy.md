# Rendering constraints

_Schema: `visual-governance/1.0` · canonical policy · generated 2026-05-13T16:14:38Z._

## Intent

One hardware side per image (exterior, interior or edge). No mixed-side frames. App UI must use real captures or low-detail generated screens only — never invented labels or menu hierarchies. Generated text/numbers are not trustworthy and must not be cited as instructional proof.

## Authoritative source documents

This policy is a CONSOLIDATION POINTER. The rules themselves remain in the source documents listed below. Editing this policy does NOT edit the sources; conflicts are reported in `_repository-governance/reports/visual-governance/`.

- `visual-system/shared/visual-rules/manual-image-reset-policy.md`
- `visual-system/shared/visual-rules/app-ui-policy.md`
- `visual-system/shared/visual-rules/ai-limitations.md`
- `visual-system/shared/generation-guides/review-checklist.md`

## Constraints

- one-side-per-image (exterior | interior | edge)
- no mixed interior+exterior frame
- no generated readable text used as instruction
- no invented app-UI labels or menu hierarchies
- low-detail phone renders only when phone is contextual, not source-of-truth
- schematic fallback for wiring / installation / anatomy / reset
- background quiet, diagram-like or lightly contextual
- callouts/labels added in editorial composition, not baked into render
