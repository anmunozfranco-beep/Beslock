# Execution Flow Semantics

| id | rule |
|---|---|
| step-progression | Steps execute in declared order; out-of-order execution is a safety violation. |
| step-dependency | A step is enterable only when all declared preconditions are satisfied. |
| checkpoint | Procedures declare ≥1 checkpoint; checkpoints are safe restart anchors. |
| safe-transition | Transitions to unsafe states require explicit user confirmation + warning surface. |
| confirmation-required | Steps marked `confirmation_required=true` cannot be auto-completed by an assistant. |
| completion-condition | A procedure is complete only when its terminal state is reached AND its validation predicate passes. |
| no-implicit-completion | Absence of error is not completion; completion is positively asserted by validation predicate. |
| deterministic-execution | Given the same starting state + inputs, execution traces are reproducible. |

## Outcomes

- completed
- interrupted
- failed
- blocked
- escalated
- abandoned
