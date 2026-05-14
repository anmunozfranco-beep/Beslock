# Visual lineage / provenance

_Schema: `visual-governance/1.0` · canonical policy · generated 2026-05-13T16:14:38Z._

## Intent

Visual lineage roots at the canonical PNG and flows through conditioning asset → ComfyUI workflow run → approved support visual → delivery placement. Run records are immutable and stored under `ext-images/<slug>/automation/runs/`. Delivery placements update the writeback trackers in `image-production-status.md` and `generated/selected-assets-register.md`.

## Authoritative source documents

This policy is a CONSOLIDATION POINTER. The rules themselves remain in the source documents listed below. Editing this policy does NOT edit the sources; conflicts are reported in `_repository-governance/reports/visual-governance/`.

- `KNOWLEDGE_BUILDING/PROVENANCE_AND_LINEAGE.md`
- `KNOWLEDGE_BUILDING/COMFY_GENERATION_GOVERNANCE.md (§3 reproducibility, §7 storage)`
- `_repository-governance/manifests/visual-orchestration-doc/VISUAL_GENERATION_AUTOMATION.md`
- `ext-images/<product>/automation/runs/`

## Lineage Chain

- canonical PNG
- conditioning asset (cutout / mask / depth / normal / line-art / IPAdapter ref)
- approved ComfyUI workflow (registry id + semver + content hash)
- run record (immutable, ext-images/<slug>/automation/runs/)
- approved support visual (with reviewer + timestamp)
- delivery placement (writeback to image-production-status / selected-assets-register)

## Immutability Rules

- no edits after approval; new findings require a new run record
- missing run record == not approved; cannot be promoted
- delivery placement must reference the run-record id
