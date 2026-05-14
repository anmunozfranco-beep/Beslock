# Safe Human-in-the-Loop Patterns

Seven declared HITL patterns; HITL is the default and cannot be silently bypassed.

## Patterns

- `interruption` — trigger: operator-initiated halt; effect: slice halts at next safe checkpoint
- `approval-checkpoint` — trigger: declared checkpoint; effect: wait for approve|reject|demote
- `escalation-intervention` — trigger: escalation-trace event; effect: route to escalation-supervisor
- `unsafe-runtime-interruption` — trigger: safety predicate failure; effect: demote slice; halt; emit operational-audit-log
- `operator-override` — trigger: operator decision contradicting recommendation; effect: logged with rationale; never silent
- `reviewer-arbitration` — trigger: reviewer disagreement on a node; effect: open consensus review; cap node tier until resolved
- `governance-intervention` — trigger: governance-operator emergency action; effect: append-only event + 24h auditor co-signature

## Invariants

- no HITL pattern allows silent override
- no HITL pattern allows scope expansion
- every HITL action is reversible by an equal-or-higher decision
- every HITL action carries an operator identity + supervision-receipt
- HITL is the default; autonomous bypass does not exist at any operator surface
