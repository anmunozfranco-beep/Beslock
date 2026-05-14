# Operational Navigation Systems

Six navigation systems bounded by declared edges; no ad-hoc jumps; product-scoped.

## Navigation systems

- `operational-traversal` — moving across declared workflow steps within a slice
- `workflow-progression` — advancing checkpoint-by-checkpoint with explicit decisions
- `continuity-restoration` — resuming from a declared continuity-checkpoint snapshot
- `troubleshooting-navigation` — walking causal-graph edges + candidate troubleshooting hits
- `escalation-navigation` — moving across escalation tiers along declared monotonic transitions
- `reviewer-navigation` — queue → claim → evidence → decision → audit, in declared order

## Invariants

- navigation is bounded by declared edges; ad-hoc jumps are forbidden
- navigation surfaces always show the current checkpoint and the next required decision
- navigation never silently skips a checkpoint
- navigation never silently rolls back; rollback is an explicit operator action
- navigation is product-scoped; cross-product navigation is forbidden
