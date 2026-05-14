# Orchestration State Management

Declared orchestration states, transitions, checkpoints, interruption + recovery + degradation + completion semantics.

## States

- `initialized` — entry (supervised: False, terminal: False)
- `context-acquiring` — preparation (supervised: False, terminal: False)
- `retrieving` — loop-active (supervised: False, terminal: False)
- `assembling` — loop-active (supervised: False, terminal: False)
- `reasoning` — loop-active (supervised: False, terminal: False)
- `deciding` — loop-active (supervised: False, terminal: False)
- `awaiting-explicit-action` — supervised-gate (supervised: True, terminal: False)
- `executing-supervised` — destructive-gated (supervised: True, terminal: False)
- `interrupted` — interruption (supervised: True, terminal: False)
- `checkpointed` — checkpoint (supervised: False, terminal: False)
- `restoring` — recovery (supervised: True, terminal: False)
- `degraded` — degradation (supervised: True, terminal: False)
- `escalating` — handoff (supervised: True, terminal: False)
- `handed-off` — terminal (supervised: True, terminal: True)
- `completed` — terminal (supervised: False, terminal: True)
- `blocked` — terminal-soft (supervised: True, terminal: True)
- `failed` — terminal (supervised: True, terminal: True)

## Transitions

- initialized → context-acquiring
- context-acquiring → retrieving
- context-acquiring → degraded
- retrieving → assembling
- retrieving → failed
- assembling → reasoning
- assembling → degraded
- reasoning → deciding
- reasoning → escalating
- deciding → awaiting-explicit-action
- deciding → completed
- deciding → escalating
- awaiting-explicit-action → executing-supervised
- awaiting-explicit-action → blocked
- executing-supervised → checkpointed
- executing-supervised → interrupted
- interrupted → checkpointed
- interrupted → escalating
- checkpointed → restoring
- checkpointed → completed
- restoring → retrieving
- restoring → degraded
- degraded → completed
- degraded → escalating
- escalating → handed-off

## Checkpoints

- post-retrieval (read-only snapshot of bound nodes + provenance)
- post-assembly (assembly-package + adaptation-record)
- post-reasoning (chain-record + termination outcome)
- pre-destructive (decision-record + explicit-action receipt)
- post-destructive-step (state delta + checkpoint id)
- pre-handoff (continuity snapshot + escalation package)

## Interruption states

- user-cancel (graceful, returns to last checkpointed state)
- context-loss (re-enter context-acquiring with safest defaults)
- upstream-contract-violation (force escalating)
- ambiguity-unresolved (force escalating)
- destructive-explicit-action-timeout (force blocked)
- validation-failure (force degraded or escalating)
- session-suspend (force checkpointed)

## Recovery states

- restored-from-checkpoint (full)
- restored-degraded (safest defaults applied for missing context)
- restoration-failed (force escalating)
- rebound-from-knowledge-core (read-only re-resolution)

## Degradation levels

- L0-nominal
- L1-soft (one missing context dimension; safest default applied)
- L2-partial (one cognition system unavailable; fallback contract used)
- L3-restricted (destructive surface disabled)
- L4-read-only-only (only retrieval-loop available)
- L5-handoff-only (escalation is the only legal next state)

## Completion states

- completed (terminal, validation predicate satisfied)
- handed-off (terminal, escalation closed by receiver)
- blocked (terminal-soft, awaiting external action)
- failed (terminal, contract violation or unrecoverable error)
