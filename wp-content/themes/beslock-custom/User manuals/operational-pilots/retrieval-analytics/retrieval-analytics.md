# Retrieval Failure Analytics

Six tracked failure modes from no-result retrievals to troubleshooting insufficiency, each routed to a reviewer action — never to direct corpus writes.

## Tracks

- `no-result-retrievals` — tracked: queries returning zero candidates; review action: topic queued for corpus enrichment
- `thin-corpus-escalations` — tracked: queries where only candidate-tier results are present; review action: candidate-elevation review prioritized
- `low-confidence-guidance` — tracked: guidance shown to operator while confidence is in escalate-band; review action: either improve corpus or tighten threshold
- `causal-graph-gaps` — tracked: reasoning (layer 12) cannot construct chain for a topic; review action: causal authoring task queued
- `warning-coverage-failures` — tracked: safety-relevant query without warning surfaced; review action: warning corpus gap — high priority
- `troubleshooting-insufficiency` — tracked: troubleshooting flow exhausts options without resolution; review action: flow extension via candidate authoring

## Rules

- retrieval analytics drive corpus enrichment requests, not direct corpus writes
- warning-coverage failures are HIGH priority and surface to reviewer-of-scope immediately
- no analytic may alter retrieval ranking; ranking remains governed by CONFIDENCE_WEIGHTS source-of-truth
