# Failure States

| id | recoverable | requires | examples |
|---|---|---|---|
| blocked-state | True | tier-3 or tier-4 escalation | operational-state.blocked, admin-state.admin-locked-out |
| unsafe-state | True | warning acknowledgement + prerequisite restore | lock-state.lockout |
| unresolved-state | False | human/OEM intervention | pairing-failed (after N retries), enrollment-failed (after N retries) |
| irrecoverable-state | False | vendor RMA | depleted + battery-physically-damaged, firmware-bricked |
| escalation-required | True | tier-3..5 troubleshooting | repeated validation-failure across procedures |

## Unsafe sequences

| sequence | reason |
|---|---|
| unlocking, factory-reset | factory-reset during unlocking corrupts credential state |
| pairing, factory-reset | factory-reset during pairing leaves device in inconsistent network state |
| enrolling, battery-replacement | battery removal during enrollment loses captured credential |
| replacement-in-progress, factory-reset | factory-reset during battery swap can brick configuration |
| mounting, configured | skipping wired/power confirmation step before configuration |

## Rules

- Failure states classify recoverable vs unrecoverable; classification is non-negotiable.
- Unsafe sequences are blocked at composition time; assemblies cannot include them as adjacent steps.
- Escalation-required failures transition operational-state to `troubleshooting` and cannot return to `normal` without verified recovery.
- Irrecoverable failures emit a vendor-RMA escalation and never present a 'retry' affordance.
