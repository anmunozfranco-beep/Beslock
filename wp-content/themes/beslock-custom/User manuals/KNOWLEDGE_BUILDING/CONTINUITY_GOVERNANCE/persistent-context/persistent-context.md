# Persistent Operational Context

## Fields

- session-id
- product-id
- active-procedure-id
- active-step-id
- active-state-vector
- active-intent
- active-hypotheses
- context-vector (adaptive layer)
- open-warnings
- open-escalations
- checkpoint-anchors
- evidence-tier-summary
- decision-trace-ref
- reasoning-chain-ref
- provenance

## Kinds

- **operational-session-context** — {"scope": "single user interaction"}
- **long-running-troubleshooting-context** — {"scope": "spans multiple sessions; bound to incident"}
- **onboarding-progression-context** — {"scope": "spans multiple sessions until verified"}
- **interrupted-workflow-context** — {"scope": "preserved between cancel/pause and resume"}
- **recovery-context** — {"scope": "preserved across recovery attempts"}
- **operational-session-inheritance** — {"scope": "child session inherits a declared subset of parent context"}

## Rules

- context is declared, scoped, and observable; no implicit globals
- context fields not in the declared schema are rejected
- destructive operations require fresh confirmation even if context says 'recently confirmed'
- context cannot elevate confidence; it can only carry the recorded tier
- context survives only as long as its declared scope; expiry is explicit
- OEM-required states cannot be cleared by context alone
