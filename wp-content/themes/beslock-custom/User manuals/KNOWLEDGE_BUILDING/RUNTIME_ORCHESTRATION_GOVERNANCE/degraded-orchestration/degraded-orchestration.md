# Degraded Orchestration

Degradation is a first-class state. Modes are declared per cause; safest defaults always apply.

## Modes

- `missing-context-vector` — L1-soft — destructive: False
- `missing-confidence-tier` — L2-partial — destructive: False
- `missing-checkpoint-registry` — L3-restricted — destructive: False
- `missing-fallback-registry` — L3-restricted — destructive: False
- `missing-incident-id-emitter` — L2-partial — destructive: False
- `missing-provenance-emitter` — L4-read-only-only — destructive: False
- `thin-troubleshooting-corpus` — L4-read-only-only — destructive: False
- `warning-corpus-gap` — L3-restricted — destructive: False
- `oem-channel-contract-missing` — L5-handoff-only — destructive: False
- `schema-pin-mismatch` — L5-handoff-only — destructive: False

## Rules

- Degradation is declared per cause; ad-hoc degradation is unsafe.
- Destructive surface is unavailable in any L2+ degradation.
- Degradation always emits a degradation-cause reference.
- Degradation never elevates confidence to compensate for missing inputs.
- Degradation prefers safest default over guess.
- Recovery from degradation is supervised when destructive activity was in flight.
- L5 degradation is terminal except via escalation handoff.
