# Current-State Audit

## Purpose
This file defines the current operational boundaries of the manual-reconstruction and visual-production system after the visual-system upgrade scaffold was introduced.

## Active layers
- `../generated_manuals/`: OCR extraction artifacts and machine-structured outputs
- `../*.pdf`: source manuals
- `../*.md` at the User manuals root: legacy planning and editorial files that remain valid during migration
- `../ext-images/`: visual truth layer based on canonical product references
- `../visual-system/`: operational production layer for prompts, validation, and tracking

## System boundary
The visual-system layer does not redesign the editorial workflow.
It adds reusable controls that were previously missing:
- product visual profiles
- modular prompt components
- realism classification rules
- production tracking
- reusable interaction definitions

## Reference audits
The historical deep audits still live at the User manuals root:
- `../manual-standardization-current-state-audit.md`
- `../visual-system-current-state-audit.md`

Treat those files as baseline analysis and this directory as the stabilized architecture surface for future work.
