# Ecosystem-Wide Escalation

Declared ecosystem escalation flows. Tier is monotonic across runtimes; receivers may raise but never lower.

## Flows

- `intra→inter` — trigger: tier-3 threshold crossed inside a runtime
- `runtime→runtime` — trigger: source runtime declares the receiver runtime as the next handler
- `ecosystem→OEM` — trigger: tier-4/5 reached and OEM channel contract exists
- `ecosystem→human` — trigger: tier-3+ with no declared receiver runtime
- `continuity-preserving` — trigger: any escalation
- `ecosystem-broadcast` — trigger: tier-5 with cross-runtime impact

## Rules

- Escalation tier is monotonic across runtimes; receivers may raise but never lower.
- Escalation crossings carry the 12-field escalation package + continuity snapshot ref.
- Tier-4/5 escalations require a declared receiver (OEM channel or human); otherwise queue + lock.
- Escalation events are append-only across the ecosystem.
- An ecosystem-broadcast at tier-5 locks every involved runtime to read-only.
- OEM federation requires the OEM channel contract; absent, escalations queue and orchestration locks.
