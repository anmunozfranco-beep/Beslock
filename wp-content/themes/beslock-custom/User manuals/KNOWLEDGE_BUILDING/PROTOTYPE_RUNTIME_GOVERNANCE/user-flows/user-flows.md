# First Executable User Flows

Six declared prototype flows around onboarding + troubleshooting + escalation.

## Flows

- `onboarding-flow` (onboarding) — supervision: supervised end-to-end — in scope: True
- `first-pairing-flow` (onboarding) — supervision: supervised end-to-end — in scope: True
- `fingerprint-enrollment-flow` (onboarding) — supervision: supervised end-to-end — in scope: True
- `troubleshooting-lookup-flow` (troubleshooting) — supervision: supervised end-to-end — in scope: True
- `battery-recovery-flow` (recovery) — supervision: supervised end-to-end — in scope: True
- `escalation-handling-flow` (escalation) — supervision: supervised end-to-end — in scope: True

## Rules

- All prototype flows are read-only; destructive operations are out of scope.
- Flows declare steps and evidence keys; unobserved evidence invalidates the run.
- Flows emit guidance only after the operator has reviewed the assembly-package.
- Flows that cannot satisfy mandatory warnings cannot emit guidance.
- Flows respect confidence tiers; uncertain outputs are gated and labeled.
