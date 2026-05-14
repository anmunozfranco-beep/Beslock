# Human Supervision Model

Review checkpoints, escalation intervention, uncertainty surfacing, operator override, cognition supervision, unsafe-runtime interruption.

## Review checkpoints

- pre-emission (operator inspects retrieval-package + assembly-package before any guidance-package release)
- post-emission (operator reviews emitted guidance-package and chain-record)
- pre-handoff (operator approves any escalation handoff)
- pre-completion (operator confirms no open warnings, no unresolved escalations)
- post-anomaly (operator reviews anomaly + decides demotion)

## Escalation intervention

- operator may raise escalation tier at any review checkpoint
- operator may NOT lower escalation tier (monotonic)
- operator may demote the proof slice at any time
- operator may halt the slice on any open contract violation

## Uncertainty surfacing

- confidence tier is disclosed at the operator boundary; never silently elevated
- ambiguity surfaces with all candidate options + their declared sources
- contradictions surface verbatim with both source nodes
- uncertain-confidence outputs are labeled and gated

## Operator override

- operator may approve / reject / request more info / escalate / demote
- operator cannot override safety-preserving adaptations
- operator cannot downgrade irreversibility warnings
- operator overrides are recorded with identity (when declared) + provenance + timestamp

## Cognition supervision

- every cognition boundary inside the proof slice carries a supervision receipt
- every supervision receipt is append-only and provenance-signed
- missing supervision receipt = unsafe; the step is invalid

## Unsafe-runtime interruption

- operator-cancel → graceful return to last checkpointed state (read-only by default in proof)
- contract-violation → force escalating + halt slice
- validation-predicate-failed → force demotion or escalating
- ambiguity-unresolved → force escalating
- explicit-action-timeout → force blocked (proof has no destructive paths, so this is informational)
