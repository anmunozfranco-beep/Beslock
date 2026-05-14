# Federated Runtime Contracts

Declared inter-runtime contracts. Violations are federation errors, not warnings.

## Contracts

- `inter-runtime-base` — kind: inter-runtime
- `context-exchange` — kind: context-exchange
- `escalation-exchange` — kind: escalation-exchange
- `reasoning-interoperability` — kind: reasoning
- `orchestration-federation` — kind: orchestration
- `shared-cognition-boundary` — kind: shared-cognition
- `continuity-exchange` — kind: continuity
- `visual-federation` — kind: visual
- `publication-federation` — kind: publication
- `schema-pin-federation` — kind: schema

## Rules

- Contracts are declared; runtimes cannot invent new contracts at runtime.
- Contract violations are federation errors, not warnings.
- Contracts preserve directionality (read-only / append-only / gated).
- Contracts are versioned; receivers verify schema compatibility before acceptance.
- Contracts cannot elevate confidence, promote P-tier, or reassign role across boundaries.
