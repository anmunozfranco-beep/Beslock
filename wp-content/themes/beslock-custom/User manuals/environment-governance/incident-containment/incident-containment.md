# Operational Incident Containment

Six containment patterns; every incident emits an event and is closed by a replay-validated finding.

## Patterns

- `runtime-incident-isolation` — trigger: safety predicate failure or replay drift > floor; containment: halt slice → quarantine sandbox → emit incident-trace event
- `escalation-containment` — trigger: escalation-trace event with no responder; containment: auto-route to escalation-supervisor; raise SLA tier; suspend dependent slices
- `rollback-containment` — trigger: operator-initiated rollback exceeding declared scope; containment: halt rollback; require governance + auditor co-sign before fan-out
- `provenance-breach-handling` — trigger: provenance hash mismatch or missing source binding; containment: demote affected node tier to candidate; halt emissions citing the node; escalation-supervisor notified
- `unsafe-runtime-shutdown` — trigger: unrecoverable safety failure; containment: shut down emission path in env; preserve append-only logs; quarantine env
- `replay-assisted-incident-review` — trigger: any incident closed; containment: replay frozen orchestration-trace; compare to live; emit replay-trace; auditor finding

## Invariants

- no incident is ever silently absorbed; every incident emits an event
- no incident response writes to canonical knowledge-core JSON
- no incident response bypasses the supervision-receipt
- every containment action is reversible by an equal-or-higher governance decision
- every incident closure is accompanied by a replay-validated finding
