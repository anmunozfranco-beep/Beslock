# Orchestration Loops

Declared catalog of orchestration loops a runtime may execute. Loops are declared; ad-hoc loops are unsafe.

## Loops

- `retrieval-loop` — phase: retrieval — supervision: unsupervised (read-only) — destructive: False
- `contextual-assembly-loop` — phase: contextual-assembly — supervision: unsupervised (read-only) — destructive: False
- `reasoning-loop` — phase: reasoning — supervision: unsupervised (read-only outputs) — destructive: False
- `decisioning-loop` — phase: decisioning — supervision: destructive ⇒ supervised explicit-action required — destructive: True
- `escalation-loop` — phase: escalation — supervision: supervised (handoff target is human or declared channel) — destructive: False
- `continuity-restoration-loop` — phase: continuity-restoration — supervision: supervised when destructive activity was in flight — destructive: False
- `adaptive-guidance-loop` — phase: adaptive-guidance — supervision: unsupervised for simplifying; supervised for safety-relevant — destructive: False
- `runtime-completion-loop` — phase: runtime-completion — supervision: completion blocked unless prerequisites met — destructive: False

## Rules

- Loops are declared; no loop may be invented at runtime.
- Loops emit provenance at every step; an unobserved step is an invalid step.
- Loops respect upstream contracts and never insert undeclared operations.
- Loops with destructive surface require an explicit-action step before any destructive transition.
- Loops terminate only at declared exit states; ad-hoc termination is unsafe.
- Loops compose via the cognition-coordination contracts (Task 2) — never via implicit chaining.
