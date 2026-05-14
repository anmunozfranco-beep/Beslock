# Cognition Execution Lifecycle

## Stages

- **runtime-initialization** — {"activities": ["pin schema versions", "verify contracts available", "load declared dimensions/profiles"]}
- **context-acquisition** — {"activities": ["receive declared context vector", "fill missing dimensions with safest defaults", "record provenance of acquisition"]}
- **semantic-retrieval** — {"activities": ["resolve query intent", "fetch via knowledge-core-access-contract", "apply consumption gates"]}
- **reasoning-execution** — {"activities": ["build chain", "evaluate predicates + causal links", "track hypotheses", "propagate uncertainty"]}
- **decisioning** — {"activities": ["select among declared options at decision points", "respect prioritisation + tie-breakers", "emit decision provenance"]}
- **escalation** — {"activities": ["detect triggers", "build escalation package", "hand off (read-only)", "append history"]}
- **continuity-persistence** — {"activities": ["snapshot context", "append history", "preserve OEM-required flags", "respect non-inheritable destructive-confirmation"]}
- **runtime-completion** — {"activities": ["emit final provenance bundle", "close timelines", "release scoped context per declared expiry"]}

## Rules

- lifecycle stages are declared; runtime cannot skip a stage that produced state
- every stage emits provenance
- destructive activity may only occur after decisioning has selected a destructive option with explicit-action
- completion requires terminal state AND validation predicate (per EXECUTION_GOVERNANCE)
- runtime cannot exit while any open warning or unresolved escalation remains, except by escalation-handoff
