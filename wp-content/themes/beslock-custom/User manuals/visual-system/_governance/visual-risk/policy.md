# Visual risk model

_Schema: `visual-governance/1.0` · canonical policy · generated 2026-05-13T16:14:38Z._

## Intent

Every visual artefact is classified by the consequence of getting it wrong: visuals that affect installation, operation, troubleshooting, pairing, safety or locking behaviour are HIGH visual risk. Risk drives stricter constraints, lower inference tolerance, stronger provenance grounding, and higher semantic validation.

## Authoritative source documents

This policy is a CONSOLIDATION POINTER. The rules themselves remain in the source documents listed below. Editing this policy does NOT edit the sources; conflicts are reported in `_repository-governance/reports/visual-governance/`.

- `ext-images/<product>/knowledge-core/visual-risk/risk-*.json (all 6 products)`
- `ext-images/<product>/knowledge-core/visual-intent/intent-*.json`
- `KNOWLEDGE_BUILDING/COMFY_GENERATION_GOVERNANCE.md`

## Severity Levels

- **critical**: hallucinated sensor; wrong keypad layout; geometry that misleads at unboxing or first install
- **high**: missing mechanical key; misplaced fingerprint zone; incorrect handle direction
- **medium**: wrong camera position; fake emergency port; wrong indicator placement
- **low**: non-critical visibility issues that do not affect identification or operation

## User Risk Levels

- low
- medium
- high
- critical

## Visual Assistance Priorities

- P1 critical-path
- P2 support
- P3 editorial

## Mitigation Template

ComfyUI workflow MUST anchor the listed trigger_components against the OEM PNG references and refuse to render the asset if anchors are missing.
