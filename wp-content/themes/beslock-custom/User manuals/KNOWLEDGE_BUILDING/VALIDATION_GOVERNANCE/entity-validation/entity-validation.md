# Entity Consistency Rules

## Rules

- Entities MUST have id matching `^[a-z0-9][a-z0-9-]*$` and at least one matched_surface_term.
- Cross-product entity-id collisions are only permitted when the entity represents a shared concept (must be declared).
