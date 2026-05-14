# Escalation Decisioning

## Tiers

- **self-service** — {"tier": 1, "audience": "end user"}
- **advanced-self-service** — {"tier": 2, "audience": "advanced/installer/administrator"}
- **support-required** — {"tier": 3, "audience": "vendor/dealer support"}
- **vendor-intervention** — {"tier": 4, "audience": "OEM technical support"}
- **rma-irrecoverable** — {"tier": 5, "audience": "OEM RMA / replacement"}

## Triggers

- **validation-failure-x3** — {"from": 1, "to": 2}
- **pairing-failed-x3** — {"from": 2, "to": 3}
- **lockout-cycles-ge-2** — {"from": 1, "to": 3}
- **battery-replacement-failure** — {"from": 2, "to": 4}
- **firmware-rollback-failure** — {"from": 4, "to": 5}
- **irrecoverable-failure** — {"from": "*", "to": 5}
- **conflicting-verified-truth** — {"from": "*", "to": 4}
- **destructive-under-ambiguity** — {"from": "*", "to": 3}

## Rules

- escalation is monotonic during a single incident (no silent demotion)
- escalation cannot return to tier 1 without verified recovery (predicate)
- irrecoverable failures emit RMA escalation; no 'retry' affordance
- OEM intervention required for: firmware-bricked, conflicting verified-truth on P0, irrecoverable mid-destructive
- escalation events carry provenance and operational state snapshot
