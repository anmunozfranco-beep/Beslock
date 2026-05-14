# Federated Orchestration

Declared orchestration roles, coordination patterns, and rules across runtimes.

## Roles

- `primary-runtime` — owns the active orchestration loop and is the source of truth for the current step
- `delegated-runtime` — executes a delegated step under the primary's supervision posture
- `observer-runtime` — consumes traces read-only; cannot mutate state
- `receiver-runtime` — receives handoff (escalation or delegation) and acquires read-only state until acknowledged
- `publication-runtime` — consumes packaging requests bound by lifecycle P-tier gates
- `continuity-runtime` — owns append-only continuity state and serves all runtimes read-only

## Patterns

- delegation (primary → delegated under preserved supervision)
- handoff (primary → receiver with read-only lock at source)
- broadcast (primary → all observers read-only)
- co-execution (two runtimes execute disjoint loops on a shared incident-id)
- escalation-handoff (primary → receiver under monotonic escalation contract)
- degraded-federation (one runtime is L3+; primary downgrades the federation to read-only-only)
- coexistence (multiple runtimes operate on disjoint scopes within one ecosystem-session)

## Rules

- Roles are declared per orchestration loop; runtime cannot self-promote a role.
- Delegation preserves supervision posture (supervised stays supervised).
- Co-execution requires disjoint scopes; overlapping scopes require declared arbitration.
- Degraded federation forces the federation level to the most degraded participant.
- Coexistence cannot share private cognition state; only declared shared-context kinds cross boundaries.
- Federated orchestration cannot create a destructive cross-runtime path.
- Federated completion requires all participating runtimes to satisfy their declared completion conditions.
