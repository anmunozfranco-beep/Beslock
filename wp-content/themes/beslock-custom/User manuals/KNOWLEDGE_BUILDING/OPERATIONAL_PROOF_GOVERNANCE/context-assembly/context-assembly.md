# Executable Context Assembly

Declared executable context-assembly flows with steps + evidence requirements per flow.

## Flows

- `retrieval-flow` — steps: 5 — evidence keys: retrieval-package-id, provenance-manifest-ref, query-intent-id
- `procedural-guidance-flow` — steps: 4 — evidence keys: guidance-package-id, adaptation-record-ref, profile-id
- `warning-surface-flow` — steps: 3 — evidence keys: warning-record-ref, severity, source-node-id
- `escalation-flow` — steps: 4 — evidence keys: escalation-package-ref, continuity-snapshot-ref, tier
- `continuity-flow` — steps: 4 — evidence keys: timeline-id, checkpoint-id, non-inheritable-filter-record
- `adaptive-guidance-flow` — steps: 4 — evidence keys: adaptation-record-ref, precedence-rule-id
- `reasoning-trace-flow` — steps: 4 — evidence keys: chain-record-ref, termination-outcome, edges-traversed[]

## Rules

- Flows are declared; no flow may be invented during a proof slice.
- Every flow emits provenance; an unobserved step invalidates the proof.
- Flows are read-only; destructive transitions are out of scope for proof-of-value.
- Mandatory warnings cannot be suppressed at any flow.
- Adaptive guidance never elevates confidence to compensate for missing inputs.
