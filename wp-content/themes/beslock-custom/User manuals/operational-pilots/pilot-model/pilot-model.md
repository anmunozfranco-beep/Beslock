# Operational Pilot Model

Six supervised pilots covering onboarding, troubleshooting, reviewer workflows, OEM ingestion, escalation handling, and replay-assisted review.

## Pilot definitions

- `onboarding-pilot` — supervised onboarding flows for one product at a time; supervision: one accountable operator per session; receipts captured per layer-24 contract; thresholds: {'minimum_confidence': 0.6, 'escalate_below': 0.5, 'block_below': 0.3}
- `troubleshooting-pilot` — guided troubleshooting with replay-assisted reasoning; supervision: operator + reviewer-on-call; both receipts captured; thresholds: {'minimum_confidence': 0.65, 'escalate_below': 0.55, 'block_below': 0.35}
- `reviewer-workflow-pilot` — reviewer elevation of pending candidates (132 outstanding); supervision: scoped reviewer role per layer-23; revocation first-class; thresholds: {'single_reviewer_max_tier': 'internal', 'dual_review_required_for': ['external', 'production-shadow']}
- `oem-ingestion-pilot` — controlled OEM manual ingestion through the dual-review binding (layers 23 + 25); supervision: ingestion operator + content reviewer (cannot be same person); thresholds: {'entry_tier': 'candidate', 'promotion_requires': 'dual-review + reviewer-of-scope'}
- `escalation-handling-pilot` — controlled escalation path exercise across runtime → operator → reviewer; supervision: escalation receiver named per channel; SLA observed not enforced; thresholds: {'escalate_on_confidence_below': 0.5, 'escalate_on_continuity_break': True}
- `replay-assisted-review-pilot` — reviewers exercise replay (layer 22) to validate prior runtime decisions; supervision: reviewer-of-scope; replay receipts captured; thresholds: {'replay_divergence_alert_threshold': 0.1}

## Operator constraints

- `onboarding-pilot`: no autonomous progression; no skipped acknowledgements; no replay-bypass
- `troubleshooting-pilot`: must declare hypothesis before action; must record observed outcome; must invoke replay on uncertainty
- `reviewer-workflow-pilot`: one candidate at a time; decision rationale captured; no batch promotion
- `oem-ingestion-pilot`: provenance complete or reject; no merge into trusted corpus until promoted
- `escalation-handling-pilot`: acknowledge within observation window; record disposition
- `replay-assisted-review-pilot`: replay must complete before decision; discrepancies recorded as findings

## Safety boundaries

- `onboarding-pilot`: sandbox env (layer 25); candidate-only corpus surface; no production telemetry sinks
- `troubleshooting-pilot`: read-only against installed-base data; no remote actuation; session-scoped continuity only
- `reviewer-workflow-pilot`: dual-review env (layer 25) for trust-boundary changes; audit trail mandatory
- `oem-ingestion-pilot`: ingestion env only; candidate-tier on entry; no runtime exposure pre-promotion
- `escalation-handling-pilot`: no auto-escalation loops; termination after one operator hop
- `replay-assisted-review-pilot`: replay reads supplemental corpus only; skips synthetic empty packages; no live corpus mutation

## Pilot model rules

- every pilot is supervised; no autonomous pilot may run
- every pilot is sandboxed (layer-25 env tier appropriate to its scope)
- every pilot is candidate-corpus-only unless reviewer-promoted (layer 23)
- every pilot must produce supervision receipts (layer 24) before closing
- no pilot may bypass replay (layer 22) when confidence falls below its declared escalate threshold
- no pilot may auto-promote candidates; promotion is a separate reviewer act
