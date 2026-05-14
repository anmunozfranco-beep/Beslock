# Orchestration Safety Boundaries

Hard boundaries on what orchestration may not do, unsafe combinations, escalation-required states, supervision-required states, irreversibility safeguards, uncertainty-aware limits.

## Prohibited orchestration actions

- Inventing an orchestration loop not declared by this layer.
- Inventing a coordination contract not declared by this layer.
- Bridging two cognition systems via an undeclared intermediary.
- Auto-resuming destructive execution after an interruption.
- Silently resolving a contradiction with verified-truth.
- Silently picking among ambiguous options under uncertain confidence.
- Elevating confidence tier to satisfy a decision threshold.
- Promoting a P-tier at runtime.
- Modifying any prior governance layer at runtime.
- Mutating knowledge-core at runtime.
- Producing visual outputs, PDFs, or any rendered artefact at runtime.
- Acting without a declared decision point.
- Suppressing an irreversibility warning.
- Completing while an open warning or unresolved escalation remains, except via handoff.
- Operating without provenance emission.

## Unsafe runtime combinations

- destructive-decision + missing-explicit-action receipt
- destructive-decision + low-confidence-tier
- destructive-decision + role-not-declared
- destructive-decision + interrupted-or-degraded state
- auto-resume + destructive-was-in-flight
- completion + open-warning-without-acknowledgement
- completion + unresolved-escalation
- handoff-receiver-undeclared + tier-4/5 escalation
- schema-pin-mismatch + any non-escalation transition
- ambiguity-detected + decision-emitted (must escalate instead)

## Escalation-required orchestration states

- ambiguity-detected with uncertain-confidence
- contradiction-with-verified-truth
- destructive-explicit-action-timeout
- restoration-failed
- validation-predicate-failed under destructive-in-flight
- L5 degradation

## Supervision-required runtime states

- awaiting-explicit-action
- executing-supervised
- interrupted
- restoring (when destructive was in flight)
- degraded (L3 or higher)
- escalating

## Irreversible-operation safeguards

- Irreversibility flag is immutable at runtime.
- Irreversibility warning is mandatory and cannot be downgraded by any override.
- Irreversibility requires explicit-action gate AND irreversibility-gate (two-token).
- Irreversibility is never inheritable across continuity restoration.
- Irreversibility events emit a dedicated audit record.

## Uncertainty-aware orchestration limits

- Uncertain-confidence decisions cannot select a destructive path; must escalate.
- Uncertain-confidence reasoning cannot terminate as concluded; must terminate as inconclusive or escalated.
- Uncertain-confidence retrieval surfaces uncertainty at the boundary; never asserts.
- Uncertain-confidence adaptive selections prefer safest default.
- Uncertain-confidence continuity restorations are read-only until supervised confirmation.
