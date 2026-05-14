# Canonical visual governance

_Schema: `visual-governance/1.0` · generated 2026-05-13T16:14:38Z by `tools/visual_governance_consolidate.py`._

This folder is the SINGLE CANONICAL ROOT for visual-generation governance. Each subfolder owns one policy domain. Every policy file is a CONSOLIDATION POINTER: the underlying rules live in the source documents listed in each `sources.json`.

## Domains

- [`visual-style-policy/policy.md`](visual-style-policy/policy.md) — Global visual style policy
- [`human-interaction-policy/policy.md`](human-interaction-policy/policy.md) — Human representation policy (hands-only)
- [`mechanical-consistency/policy.md`](mechanical-consistency/policy.md) — Mechanical consistency policy
- [`truth-source/policy.md`](truth-source/policy.md) — Truth-source PNG policy
- [`rendering-constraints/policy.md`](rendering-constraints/policy.md) — Rendering constraints
- [`comfy-contracts/policy.md`](comfy-contracts/policy.md) — ComfyUI contracts (only authorised renderer)
- [`negative-prompts/policy.md`](negative-prompts/policy.md) — Consolidated negative-prompt registry
- [`visual-risk/policy.md`](visual-risk/policy.md) — Visual risk model
- [`visual-validation/policy.md`](visual-validation/policy.md) — Visual validation contracts
- [`visual-lineage/policy.md`](visual-lineage/policy.md) — Visual lineage / provenance
- [`publication-constraints/policy.md`](publication-constraints/policy.md) — Publication-channel constraints (DRAFT — gap)

## Hard guarantees of this consolidation

- No source document was moved, copied, or rewritten.
- No prompt, manifest, or run record was modified.
- No image was generated.
- No ComfyUI workflow was altered.
- Conflicts are reported in `_repository-governance/reports/visual-governance/`, never silently resolved.

## Reports

- `_repository-governance/reports/visual-governance/01-discovered-artifacts.json`
- `_repository-governance/reports/visual-governance/02-consolidated-governance-map.json`
- `_repository-governance/reports/visual-governance/03-duplications-and-conflicts.json`
- `_repository-governance/reports/visual-governance/04-canonical-governance-structure.json`
- `_repository-governance/reports/visual-governance/05-new-governance-structure.json`
- `_repository-governance/reports/visual-governance/06-visual-policy-summary.json`
- `_repository-governance/reports/visual-governance/07-mechanical-consistency-summary.json`
- `_repository-governance/reports/visual-governance/08-human-representation-summary.json`
- `_repository-governance/reports/visual-governance/09-visual-risk-model-summary.json`
- `_repository-governance/reports/visual-governance/10-comfy-orchestration-readiness.json`
- `_repository-governance/reports/visual-governance/11-future-validation-opportunities.json`
- `_repository-governance/reports/visual-governance/12-unresolved-governance-gaps.json`
