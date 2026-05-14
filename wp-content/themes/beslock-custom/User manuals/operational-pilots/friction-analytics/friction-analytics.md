# Reviewer & Operator Friction Analytics

Six friction patterns covering reviewer fatigue, workflow friction, escalation overload, ambiguity density, navigation pain, and continuity restoration failures.

## Patterns

- `reviewer-fatigue` — indicator: time-to-decision rising over rolling window for a reviewer; mitigation: rotate reviewer-of-scope; reduce queue assignment
- `workflow-friction` — indicator: operator retraction rate or step-loop rate above baseline; mitigation: doctrine clarification (layer 24 ergonomics); console refinement
- `escalation-overload` — indicator: escalation receiver acknowledgement time exceeds declared envelope; mitigation: expand receiver pool; tighten escalation criteria
- `ambiguity-density` — indicator: topic cluster with high divergence-score across sessions; mitigation: corpus enrichment for that topic via layer-23 candidate flow
- `navigation-pain` — indicator: operator requests clarification on the same step across operators; mitigation: layer-24 explainability artifact + console copy refinement
- `continuity-restoration-failures` — indicator: checkpoint resume fails or operator restarts session; mitigation: review checkpoint contract; widen continuity scope (layer 14) without mutating runtime invariants

## Rules

- friction analytics inform reviewer + governance; never auto-mutate doctrine
- individual operator friction surfaces are scoped to that operator + their reviewer-of-scope
- friction findings flow into the candidate pipeline (layer 23); no shortcut into trusted corpus
