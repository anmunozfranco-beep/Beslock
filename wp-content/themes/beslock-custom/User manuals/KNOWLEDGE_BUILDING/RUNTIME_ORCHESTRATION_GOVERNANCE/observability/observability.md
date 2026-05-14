# Orchestration Observability

What cannot be observed cannot be trusted. Declared trace kinds, fields, audit + transparency rules, reasoning + escalation + continuity traceability.

## Trace kinds

- loop-trace (one record per orchestration loop iteration)
- step-trace (one record per declared step within a loop)
- contract-trace (one record per cognition-coordination message)
- state-trace (one record per orchestration state transition)
- checkpoint-trace (one record per checkpoint emission)
- supervision-trace (one record per supervision-boundary crossing)
- escalation-trace (one record per escalation event)

## Trace fields

- incident-id (when emitter exists)
- session-id
- loop-id
- step-id
- from-state
- to-state
- contract-id (for contract-traces)
- provenance-manifest-ref
- confidence-tier (when applicable)
- supervision-receipt-ref (when applicable)
- timestamp (UTC)
- schema-version (pinned)

## Auditability requirements

- Every orchestration step is auditable from declared inputs.
- Every supervision-boundary crossing carries a supervision receipt.
- Every escalation carries a 12-field escalation package reference.
- Every destructive transition carries an explicit-action receipt reference.
- Every degradation transition carries a degradation-cause reference.
- Every completion carries a validation-predicate evaluation record.
- Audit records are append-only; no orchestration step may rewrite history.

## Transparency rules

- Confidence tiers are disclosed at the orchestration boundary; never silently elevated.
- Uncertainty is signaled, never suppressed; suppression is unsafe.
- Contradictions and ambiguities are surfaced verbatim with their sources.
- Adaptation decisions are visible (which precedence rule fired, which profile selected).
- Degradation cause is visible at the boundary; opaque degradation is unsafe.

## Reasoning trace propagation

- Reasoning chain-record is attached to every decision-record it produced.
- Hypothesis lifecycle stages are visible per chain.
- Causal edges traversed are listed (verbatim from declared edges; no invented edges).
- Termination outcome (concluded/inconclusive/escalated) is mandatory.
- Inconclusive reasoning never silently becomes a conclusion downstream.

## Escalation traceability

- Escalation tier + trigger + receiver identity are mandatory fields.
- Continuity snapshot reference is mandatory.
- Handoff status (handed-off | handoff-failed) is mandatory.
- Receiver acknowledgement reference (when receiver provides one) is mandatory.

## Continuity traceability

- Continuity records are append-only; updates produce a new record.
- Restoration records reference the source checkpoint id.
- Non-inheritable signals (e.g. destructive-confirmation) are explicitly marked.
- Resume restrictions (e.g. no-auto-resume-destructive) are visible at the boundary.
