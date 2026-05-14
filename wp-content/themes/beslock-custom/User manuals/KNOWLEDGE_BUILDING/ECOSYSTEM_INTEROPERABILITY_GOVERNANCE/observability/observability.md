# Ecosystem Observability

Declared trace kinds, fields, and audit + reasoning + continuity + escalation traceability rules across the federation.

## Trace kinds

- ecosystem-session-trace (one record per session open/close)
- federation-message-trace (one record per cross-runtime message)
- delegation-trace (one record per delegated step)
- handoff-trace (one record per escalation/handoff)
- shared-context-trace (one record per shared-context append or monotonic update)
- schema-pin-trace (one record per schema-pin verification)
- broadcast-trace (one record per ecosystem-broadcast)

## Trace fields

- ecosystem-session-id
- incident-id (when emitter exists)
- origin-runtime-id
- destination-runtime-id (when applicable)
- contract-id
- schema-version
- supervision-receipt-ref (when applicable)
- provenance-manifest-ref
- tier (for escalation-related traces)
- timestamp (UTC)

## Auditability

- Every cross-runtime message is auditable from declared inputs.
- Every delegated step carries a delegation-trace + supervision receipt.
- Every handoff carries a handoff-trace + 12-field escalation package ref + continuity snapshot ref.
- Every shared-context update carries an append-only shared-context-trace.
- Every schema-pin verification (success or failure) is logged.
- Audit records are append-only at the ecosystem level.

## Shared reasoning traces

- Chain-records cross runtime boundaries verbatim with origin-runtime-id stamp.
- Receiving runtime may append to the chain (declared edges only) but never edit prior steps.
- Hypothesis lifecycle stages are visible across the federation.
- Termination outcomes (concluded/inconclusive/escalated) are mandatory and immutable.

## Continuity observability

- Continuity records are visible read-only to all runtimes under the same incident-id.
- Restoration records reference source checkpoint and originating runtime.
- Non-inheritable signals are explicitly marked as filtered at boundary.

## Escalation trace federation

- Escalation traces are aggregated per incident-id across all involved runtimes.
- Tier monotonicity is observable end-to-end.
- Receiver acknowledgement (when receiver provides one) is mandatory.
