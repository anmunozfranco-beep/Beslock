# Governance Operator Workflows

Six declared workflows for escalation, intervention, audit, dispute, and emergency demotion.

## Workflows

- `governance-escalation` — trigger: blocking queue item or runtime escalation-trace event; actor: governance-operator
- `unsafe-knowledge-intervention` — trigger: node demoted by safety-predicate failure; actor: governance-operator
- `runtime-incident-review` — trigger: supervised run with safety demotion or replay drift; actor: governance-operator + reviewer
- `operational-audit-review` — trigger: scheduled or on-demand audit of review-audit log; actor: auditor
- `disputed-knowledge-handling` — trigger: node at state=disputed; actor: governance-operator + dual-review
- `emergency-demotion` — trigger: operational incident or contradiction detected; actor: governance-operator

## Emergency demotion rules

- emergency demotion is an append-only event with severity, scope, and rationale
- emergency demotion fans out via declared lineage edges only
- emergency demotion never deletes; it only changes future retrievals
- emergency demotion requires governance-operator + auditor co-signature within 24 hours
- emergency demotion is reviewable; reversal is a separate governed event

## Governance operator guardrails

- may not author or approve their own records
- may not extend their own scope or tier_ceiling
- all actions are co-indexed in review-audit + governance-audit logs
- all actions are reversible by governance review
