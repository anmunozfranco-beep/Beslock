# Supervised Operational Guidance

Supervision posture, uncertainty surfacing, escalation triggers, unsafe-guidance interruption, review checkpoints, operator override.

## Supervised behavior

- every cognition boundary is supervised
- supervision posture is declared, not inferred
- supervision receipts are append-only and provenance-signed
- the prototype halts on missing supervision receipts

## Uncertainty surfacing

- confidence tier disclosed at the operator boundary
- ambiguity surfaced with all candidate options + sources
- contradictions surfaced verbatim with both source nodes
- uncertain-confidence outputs labeled and gated

## Escalation triggers

- validation predicate failure
- contract violation
- ambiguity unresolved within declared budget
- missing supervision receipt
- operator-raised tier

## Unsafe-guidance interruption

- unsafe-flow detected → halt slice + force escalating
- hallucination detected (node not in knowledge-core) → halt slice + demote
- irreversibility warning downgrade attempted → halt slice + demote
- governance bypass attempted → halt slice + demote

## Review checkpoints

- pre-emission
- post-emission
- pre-handoff
- pre-completion
- post-anomaly

## Operator override

- approve / reject / request-more-info / escalate / demote
- cannot relax safety-preserving adaptations
- cannot downgrade irreversibility warnings
- recorded with identity (when declared) + provenance + timestamp
