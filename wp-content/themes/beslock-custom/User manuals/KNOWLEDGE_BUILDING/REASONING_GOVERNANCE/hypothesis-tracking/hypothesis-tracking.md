# Operational Hypothesis Tracking

## Lifecycle

- proposed
- under-test
- confirmed
- refuted
- abandoned
- escalated
- refined

## Fields

- id
- claim
- evidence-required
- evidence-collected
- predicate
- confidence-tier
- lifecycle-state
- parent-hypothesis (if refined)
- provenance

## Rules

- every troubleshooting/recovery chain attaches at least one hypothesis
- hypotheses are explicit; no chain may proceed on an undeclared assumption
- confirmation requires the declared validation predicate to evaluate true
- refutation closes the hypothesis with provenance (no silent retry)
- refined hypotheses must link to their parent (audit trail)
- abandoned hypotheses cannot be silently re-opened in the same incident
- hypothesis confidence cannot exceed evidence confidence

## Audit Requirements

- hypothesis state transitions are recorded
- evidence references are recorded
- predicate evaluation result is recorded
- linked decisions and branches are recorded
- linked escalations are recorded
