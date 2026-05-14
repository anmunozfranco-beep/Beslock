# Visual validation contracts

_Schema: `visual-governance/1.0` · canonical policy · generated 2026-05-13T16:14:38Z._

## Intent

Every approved visual must pass (a) the shared review checklist, (b) per-product visual-validation.md passes, and (c) automated tolerance checks against the component-visibility-map of its product. Validation is mandatory before promotion to any product nucleus.

## Authoritative source documents

This policy is a CONSOLIDATION POINTER. The rules themselves remain in the source documents listed below. Editing this policy does NOT edit the sources; conflicts are reported in `_repository-governance/reports/visual-governance/`.

- `visual-system/shared/generation-guides/review-checklist.md`
- `ext-images/<product>/visual-system/validations/visual-validation.md`
- `ext-images/<product>/knowledge-core/component-visibility/component-visibility-map.json`
- `tools/visual_generation.py (score subcommand)`

## Manual Pass Conditions

- product unmistakably identified
- protected geometry matches visual-profile.md
- exactly one hardware side shown
- schematic or hybrid class
- no full human figure / face
- no generated technical text used as proof

## Automated Checks Today

- aspect-ratio mismatch
- undersized output
- low edge energy
- low contrast
- too dark / too bright
- SHA-256 duplication detection

## Automated Checks Required Next

- silhouette tolerance vs canonical PNG (≤2 px on 1024-ref)
- component-position tolerance per component-visibility-map
- sensor-count validation
- keypad-grid validation
- handle-orientation check
- cross-product contamination scan

## Qa Gate States

- pending
- approved
- rework
- reject
- blocked-pending-oem-validation
