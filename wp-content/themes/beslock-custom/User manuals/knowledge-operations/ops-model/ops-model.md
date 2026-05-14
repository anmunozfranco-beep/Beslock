# Knowledge Operations Model

Operational domains, roles, and invariants that bound human knowledge operations.

## Operational domains

- `corpus-maintenance` — keep per-product knowledge-core healthy: stale review, supersession, retention
- `review-operations` — operate the review queues; assign, track, audit
- `promotion-operations` — execute promotion/demotion events through declared lifecycle gates
- `oem-ingestion` — intake OEM artifacts, stage OCR, attach bindings
- `runtime-maintenance` — monitor runtime channels, replay drift, escalation rate
- `governance-maintenance` — maintain reviewer registry, scope, revocation, audit-trail integrity

## Roles

- `reviewer` — per-domain, per-product approval
- `oem-reviewer` — binding artifact verification
- `operator` — supervised runtime execution
- `governance-operator` — registry, scope, revocation, emergency demotion
- `auditor` — read-only audit trail inspection

## Invariants

- every operation produces an append-only event
- no operation mutates canonical knowledge-core JSON in-place
- no operation may bypass declared lifecycle gates
- no operation may run autonomously without an actor identity
- every operation references a supervision-receipt
