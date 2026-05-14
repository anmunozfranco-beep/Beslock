# Prototype Runtime Architecture

Six declared runtime layers with contracts, emissions, and supervision posture.

## Layers

- `retrieval-layer` — resolve query intent into a read-only retrieval-package over knowledge-core (supervision: operator-observed)
- `context-assembly-layer` — merge retrieval-package + warnings + prerequisites + continuity-state into an assembly-package (supervision: operator-observed)
- `operational-guidance-layer` — shape assembly-package into a supervised guidance-package per ADAPTIVE precedence (supervision: supervised)
- `escalation-layer` — evaluate escalation predicates and produce 12-field escalation packages (supervision: supervised)
- `continuity-layer` — load timeline + context vector and persist append-only checkpoint records (supervision: supervised)
- `supervision-layer` — host operator review checkpoints, override channel, and supervision receipts (supervision: operator-driven)

## Rules

- Layers are unidirectional: retrieval → assembly → guidance, with supervision/continuity/escalation as orthogonal observers.
- Every layer emits provenance; an unobserved emission invalidates the prototype run.
- No layer performs destructive operations during the prototype.
- No layer may bypass lifecycle P-tier gates or schema-pin enforcement.
- No layer may elevate confidence to compensate for missing inputs.
