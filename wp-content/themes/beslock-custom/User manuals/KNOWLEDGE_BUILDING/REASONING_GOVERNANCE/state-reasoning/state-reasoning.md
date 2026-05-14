# State-Dependent Reasoning

## Dimensions

- operational-state
- recovery-status
- onboarding-stage
- degradation-level
- troubleshooting-stage
- confidence-level
- user-role
- evidence-completeness

## Rules

- the same input may resolve to different conclusions under different declared states
- state-dependent shifts must be explicitly declared (no implicit context drift)
- reasoning under degraded operation may use only fallback-eligible paths
- reasoning under recovery requires checkpoint anchors
- reasoning under low confidence downgrades all dependent conclusions
- reasoning under emergency-mode is restricted to safety-critical claims
- user-role gates conclusions that imply elevated authority

## Profiles

- **normal-operation** — {"applies_when": "operational-mode=normal", "default_chain_types": ["sequential", "deductive"]}
- **onboarding-reasoning** — {"applies_when": "operational-mode=onboarding", "default_chain_types": ["sequential", "dependent"]}
- **troubleshooting-reasoning** — {"applies_when": "operational-mode=troubleshooting", "default_chain_types": ["troubleshooting", "abductive"]}
- **recovery-reasoning** — {"applies_when": "operational-mode=recovery", "default_chain_types": ["recovery", "dependent"]}
- **degraded-reasoning** — {"applies_when": "operational-mode=degraded", "default_chain_types": ["sequential", "deductive"], "restrictions": ["fallback-eligible only"]}
- **emergency-reasoning** — {"applies_when": "operational-mode=emergency", "default_chain_types": ["deductive"], "restrictions": ["safety-critical only"]}
