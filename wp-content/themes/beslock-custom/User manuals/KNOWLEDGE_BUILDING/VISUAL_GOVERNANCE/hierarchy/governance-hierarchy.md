# Governance hierarchy

_Schema: `visual-constitution/1.0` · generated 2026-05-13T16:25:41Z._

Visual governance flows top-down. Higher levels constrain lower levels; lower levels implement higher levels. Conflicts are resolved at the highest level the conflict touches.

| Level | Layer | Location | Authority over | Authority from |
|---:|---|---|---|---|
| 1 | Canonical doctrine | `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/` | Why visuals exist; architectural principles; future direction. | Platform leadership; this constitution. |
| 2 | Runtime governance | `visual-system/_governance/<domain>/` | What the operational rules are; how they are enforced; what the registry IDs are. | Doctrine + implementation experience. |
| 3 | Per-product implementation | `ext-images/<slug>/visual-system/`, `ext-images/<slug>/knowledge-core/` | Which slots a product has; what its prompts say; which components are visible; which procedures are illustrated. | Runtime governance + product nucleus rules. |
| 4 | Execution / orchestration | `tools/visual_generation.py`, `tools/comfy/`, `ext-images/<slug>/automation/` | How a specific run is executed and recorded. | Per-product implementation + Comfy contracts. |

## Resolution rules

1. A doctrine change requires editing Level 1, then Level 2, then Level 3, then Level 4.
2. A runtime rule that contradicts doctrine is out of policy and must be reverted.
3. A per-product implementation that contradicts the runtime rule is out of policy and must be reverted.
4. An execution-layer behaviour that contradicts the per-product implementation is a bug.

## Cross-cutting boundaries

- The constitution does NOT contain operational thresholds or registry IDs.
- The runtime governance does NOT contain philosophy.
- Per-product implementations do NOT redefine doctrine for themselves.
- The execution layer does NOT carry policy state outside run records.
