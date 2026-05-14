# ComfyUI contracts (only authorised renderer)

_Schema: `visual-governance/1.0` · canonical policy · generated 2026-05-13T16:14:38Z._

## Intent

ComfyUI is the SOLE authorised visual orchestration engine. Every approved visual must be produced through a registered, hashed, approved ComfyUI workflow conditioned on the canonical PNG. No other generation engine, web UI, ad-hoc API call or one-off script may produce visuals promoted into a product nucleus.

## Authoritative source documents

This policy is a CONSOLIDATION POINTER. The rules themselves remain in the source documents listed below. Editing this policy does NOT edit the sources; conflicts are reported in `_repository-governance/reports/visual-governance/`.

- `KNOWLEDGE_BUILDING/COMFY_GENERATION_GOVERNANCE.md`
- `_repository-governance/manifests/visual-orchestration-doc/VISUAL_GENERATION_AUTOMATION.md`
- `tools/comfy/workflow_api.json.json`
- `tools/visual_generation.py`
- `ext-images/<product>/automation/orchestrators/orchestration-manifest.json`

## Registry Requirements

- stable workflow id + semver
- content-hash of the JSON
- explicit reviewer + approval timestamp
- purpose / inputs / outputs / required-conditioning / known-limitations
- anonymous or unregistered workflows MUST NOT run against canonical PNGs
- a workflow change is a NEW VERSION, not an in-place mutation

## Run Record Required Fields

- product slug
- canonical PNG path + hash
- workflow id + version + content hash
- prompt contract id
- seed
- sampler / steps / CFG / scheduler / model name + hash
- ControlNet / IPAdapter inputs (paths + hashes)
- output paths
- approval state / reviewer / timestamp

## Conditioning Rules

- all identity-affecting generation must be conditioned on the canonical PNG or its derivatives
- ControlNet preprocessors apply only to the canonical PNG or its component cutouts
- IPAdapter references limited to canonical PNG, OEM evidence in source-of-truth/visual-evidence/, or approved support visuals from the SAME product
- cross-product IPAdapter references are FORBIDDEN
- cross-product prompt copy-paste is FORBIDDEN

## Authoritative Tooling

- **runner**: tools/visual_generation.py
- **baseline_workflow**: tools/comfy/workflow_api.json.json (filename normalisation pending)
- **per_product_orchestration_manifest**: ext-images/<slug>/automation/orchestrators/orchestration-manifest.json
