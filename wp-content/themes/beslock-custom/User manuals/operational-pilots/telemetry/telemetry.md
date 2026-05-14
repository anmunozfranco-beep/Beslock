# Operational Telemetry

Seven aggregate telemetry streams over retrieval confidence, runtime uncertainty, escalation propagation, replay frequency, reviewer workload, corpus weakness hotspots, and operational dead-ends.

## Streams

- `retrieval-confidence` — metric: distribution of top_score per (product, domain) per window; purpose: detect corpus weakness
- `runtime-uncertainty` — metric: fraction of decisions in escalate-band per session; purpose: detect ambiguity zones
- `escalation-propagation` — metric: depth and time-to-acknowledge of escalation chains; purpose: detect overloaded receivers
- `replay-frequency` — metric: replay invocations per session, per reviewer; purpose: detect over- or under-use of replay
- `reviewer-workload` — metric: candidates/day and time-to-decision per reviewer; purpose: detect reviewer fatigue
- `corpus-weakness-hotspots` — metric: joint (low retrieval-confidence × high escalation) per topic; purpose: prioritize corpus enrichment
- `operational-dead-ends` — metric: sessions terminated without resolution + topic clustering; purpose: detect missing flows

## Telemetry rules

- telemetry is aggregate; per-operator identification requires reviewer-of-scope authorization
- telemetry feeds are subordinate to layer-25 trust zones and layer-24 operator privacy
- no telemetry stream may auto-trigger runtime mutation
- telemetry retention is bounded; retention windows are governance-declared
- telemetry exposure outside the pilot env requires promotion + provenance
