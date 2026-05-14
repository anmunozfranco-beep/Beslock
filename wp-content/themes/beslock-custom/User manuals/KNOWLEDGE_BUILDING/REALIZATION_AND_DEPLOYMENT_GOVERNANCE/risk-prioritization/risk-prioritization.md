# Operational Risk Prioritization

Operational risk taxonomy with mitigation rules.

## Risks

- `unsafe-runtime-realization` (high) — block any candidate with blocking risks; never realize past prototype with destructive surface uncontracted
- `over-automation` (high) — supervised-by-default; no autonomous runtime modelled; explicit-action gate mandatory for destructive
- `cognition-drift` (high) — schema-pin enforcement; append-only history; no runtime-time promotion
- `governance-bypass` (high) — lifecycle P-tier gates enforced at every boundary; federation cannot widen authority
- `escalation-failure` (high) — tier-4/5 require declared receiver; queue + lock when absent; broadcast lock at tier-5
- `operational-hallucination` (high) — retrieval cannot emit nodes absent from knowledge-core; reasoning only on declared causal edges
- `deployment-sequencing-error` (high) — stages sequential; promotion requires evidence; demotion always allowed
- `premature-pilot-promotion` (high) — exit criteria with evidence required; soft risks degrade to safer stage
- `uncontrolled-destructive-surface` (high) — two-token irreversibility gate; never inheritable across continuity restoration; audit dedicated
- `supervision-receipt-loss` (high) — supervision receipts mandatory at every supervised boundary; missing receipt = unsafe
- `provenance-loss-at-boundary` (high) — cross-runtime provenance bus required; unattributable messages dropped
- `rollback-unavailability` (high) — checkpoint registry required for any stage past assisted-runtime
- `value-without-readiness` (medium) — value cannot dominate ranking; safety > readiness > value rule
- `cognition-to-product-leakage` (medium) — transition contracts narrow authority; never widen
- `operator-fatigue` (medium) — supervision boundaries declared; degraded modes prefer safest defaults to minimize unnecessary prompts
