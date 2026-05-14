# Operational Guidance Execution

Declared executable guidance surfaces, supervision postures, scope, and blockers.

## Surfaces

- `executable-onboarding` (onboarding) — supervision: supervised end-to-end — in scope: False
- `executable-troubleshooting` (troubleshooting) — supervision: supervised end-to-end — in scope: False
- `executable-recovery` (recovery) — supervision: supervised end-to-end — in scope: False
- `executable-contextual-assistance` (contextual) — supervision: operator-observed — in scope: True

## Rules

- Guidance surfaces declare supervision posture, scope, and blockers.
- Only surfaces with no blocking risks and no destructive surface are in scope for proof.
- Guidance surfaces emit guidance-packages bound to a retrieval-package + adaptation-record.
- Guidance surfaces never execute destructive operations during proof.
- Guidance surfaces respect lifecycle P-tier gates and may not release un-promoted content.
