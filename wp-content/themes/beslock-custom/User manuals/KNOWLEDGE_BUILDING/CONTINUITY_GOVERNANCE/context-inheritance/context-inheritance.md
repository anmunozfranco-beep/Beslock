# Contextual Memory Inheritance

## Inheritable Kinds

- **troubleshooting-context** — {"inheritable": true, "constraints": ["only within same incident-id", "hypothesis confidence not elevated"]}
- **onboarding-state** — {"inheritable": true, "constraints": ["only within same product-id + same user identity"]}
- **recovery-assumptions** — {"inheritable": true, "constraints": ["only when checkpoint anchor still valid"]}
- **operational-hypotheses** — {"inheritable": true, "constraints": ["lifecycle-state preserved verbatim", "no silent re-confirmation"]}
- **warning-states** — {"inheritable": true, "constraints": ["acknowledgement flags preserved; cannot be silently cleared"]}
- **destructive-confirmation** — {"inheritable": false, "constraints": ["always re-confirm at the boundary"]}
- **oem-required-state** — {"inheritable": true, "constraints": ["cannot be cleared by inheritance"]}

## Rules

- inheritance is opt-in, by declared kind
- inheritance is bounded by scope (incident, product, user, session)
- inheritance never elevates confidence
- inheritance never clears unresolved warnings or escalations
- destructive-confirmation is non-inheritable by construction
- inheritance events carry provenance (parent context -> child context)
