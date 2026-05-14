# Feedback Instrumentation

Seven observation-only signals capture retrieval failures, escalations, continuity breakdowns, operator confusion, reviewer friction, governance bottlenecks, and ambiguity hotspots.

## Signals

- `retrieval-failure` — when: retrieval returns 0 results or all results below escalate threshold; fields: query, product, domain, top_score, result_count, session_id
- `escalation-frequency` — when: session escalates to operator or reviewer; fields: session_id, trigger, from_role, to_role, confidence_at_escalation
- `continuity-breakdown` — when: session checkpoint cannot be resumed or context is lost; fields: session_id, checkpoint_id, break_reason
- `operator-confusion` — when: operator requests clarification, retracts an action, or loops on the same step; fields: session_id, step, loop_count, retraction
- `reviewer-friction` — when: reviewer defers, requests more provenance, or cannot decide; fields: candidate_id, reviewer_id, deferral_reason, missing_provenance_fields
- `governance-bottleneck` — when: candidates queue beyond a declared age threshold or one reviewer holds disproportionate load; fields: queue_depth, oldest_age_days, reviewer_load_distribution
- `ambiguity-hotspot` — when: same query/topic produces divergent retrievals across nearby sessions; fields: topic, divergence_score, sessions_observed

## Instrumentation rules

- all signals are observation-only; instrumentation MUST NOT alter runtime behavior
- all signals carry provenance (session_id, operator role, timestamp, trust-zone)
- no signal stores PII or operator-identifying free text beyond declared fields
- signal storage is sandbox-tier in pilot phase (layer 25)
- signal aggregation is reviewer-visible; raw signals are not auto-actioned
