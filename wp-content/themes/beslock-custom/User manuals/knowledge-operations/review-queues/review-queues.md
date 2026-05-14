# Review Queue Systems

Seven append-only queues, each with declared source, SLA tier, and blocking semantics.

## Queues

- `candidate-review` — source: any node at state=candidate; SLA: standard; blocks runtime: False
- `ocr-review` — source: ocr-derived nodes pending reviewer-confirm; SLA: standard; blocks runtime: False
- `warning-review` — source: warnings/* pending promotion or stale; SLA: elevated; blocks runtime: False
- `troubleshooting-review` — source: troubleshooting/* pending promotion; SLA: standard; blocks runtime: False
- `irreversible-operation-review` — source: nodes tagged irreversible-operation; SLA: critical; blocks runtime: True
- `stale-knowledge-review` — source: nodes flagged by stale detector; SLA: standard; blocks runtime: False
- `disputed-knowledge-review` — source: nodes at state=disputed; SLA: critical; blocks runtime: True

## Queue discipline

- queues are append-only logs; consumed items are marked, not deleted
- items carry priority = (sla_tier, age, blocking_runtime)
- ownership is explicit: every claim is logged with reviewer_id + timestamp
- no auto-claim; reviewers must explicitly take ownership
- expired claims are released back to the queue with a release event
- queue back-pressure (length, age) feeds the health-monitoring dashboard
