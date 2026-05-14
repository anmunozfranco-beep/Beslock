# Orchestration Supervision Model

Supervised by default. Boundaries, oversight checkpoints, approval gates, escalation checkpoints, unsafe-runtime interruption rules, and supervision-required states.

## Supervision boundaries

- Every destructive decision crosses a supervision boundary; no exception.
- Every escalation ≥ tier 3 crosses a supervision boundary.
- Every override of a simplifying adaptation is logged; safety-preserving adaptations cannot be overridden.
- Every handoff to a non-runtime receiver (human / OEM channel) is supervised.
- Every contradiction with verified-truth is supervised before any action proceeds.
- Every promotion-like signal is supervised and out-of-band — never realised at runtime.

## Oversight checkpoints

- pre-destructive (must observe explicit-action receipt)
- pre-handoff (must observe escalation package + receiver identity when declared)
- post-interruption (must observe restoration plan before resume)
- post-degradation-into-L3+ (must observe operator acknowledgement)
- pre-completion-with-open-warning (must observe operator decision)

## Approval gates

- `explicit-action-gate` — blocks: destructive transition — input: operator identity + explicit action token
- `irreversibility-gate` — blocks: irreversible operation — input: operator identity + irreversibility acknowledgement
- `oem-handoff-gate` — blocks: tier-4/5 escalation — input: OEM channel contract (when modelled)
- `warning-acknowledgement-gate` — blocks: completion-with-open-warning — input: operator decision record
- `schema-pin-gate` — blocks: runtime initialization with mismatched schema — input: verified schema pin

## Escalation checkpoints

- tier-1 → operator notification (no orchestration pause required)
- tier-2 → orchestration pause for operator review
- tier-3 → orchestration pause + supervised resume
- tier-4 → handoff to declared external channel (OEM when modelled)
- tier-5 → terminal handoff; orchestration may not resume

## Unsafe-runtime interruption rules

- destructive-in-flight + interrupt → MUST halt, MUST checkpoint, MUST NOT auto-resume
- ambiguity-detected + uncertain-confidence → MUST escalate, MUST NOT pick silently
- contradiction-with-verified-truth → MUST escalate, MUST NOT proceed
- validation-predicate-failed → MUST degrade or escalate, MUST NOT bypass
- explicit-action-timeout → MUST block, MUST NOT proceed under assumed consent

## Supervision-required states

- awaiting-explicit-action
- executing-supervised
- interrupted
- restoring (when destructive was in flight)
- degraded (L3 or higher)
- escalating
