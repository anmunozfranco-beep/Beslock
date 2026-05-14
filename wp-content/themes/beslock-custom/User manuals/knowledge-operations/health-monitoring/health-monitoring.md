# Knowledge Health & Maintenance

Deterministic, append-only-log-derived indicators; never used for autonomous action.

## Health indicators

- `corpus-health-score` — inputs: mean tier_weight, stale ratio, candidate ratio
- `stale-knowledge-detection` — inputs: updated_at vs per-tier max_age, superseded source bindings
- `retrieval-degradation` — inputs: share of retrieval packages with no_results, share with candidate_only=True
- `warning-coverage-gap` — inputs: domains where warnings retrieval returns empty for declared canonical queries
- `troubleshooting-coverage-gap` — inputs: domains where troubleshooting retrieval is candidate-only or empty
- `runtime-reliability` — inputs: replay determinism rate, supervised-run demotion rate, escalation-trace declared-vs-surprise ratio
- `queue-back-pressure` — inputs: per-queue length, oldest-item age, claim-expiry rate

## Health discipline

- indicators are computed from append-only logs; they are reproducible
- indicators are not thresholds for autonomous action; they feed governance review
- indicators are exposed read-only; the dashboard layer is out of scope here
- indicators are scoped per product and per domain; no global single-number health

## Degradation response rules

- retrieval-degradation > declared floor → open governance-escalation
- warning-coverage-gap detected → open warning-review queue items + escalation
- queue back-pressure > declared ceiling → governance-operator notified, no auto-bypass
- runtime-reliability drop → halt supervised promotions until reviewed
