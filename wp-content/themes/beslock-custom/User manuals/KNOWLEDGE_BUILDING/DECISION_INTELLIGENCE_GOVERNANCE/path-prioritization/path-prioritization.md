# Alternative Path Prioritization

## Path Classes

- **preferred** — {"description": "canonical path with verified-truth evidence and full safeguards"}
- **alternative** — {"description": "alternate canonical path also verified-truth (e.g. role-specific)"}
- **fallback** — {"description": "registered fallback when canonical unavailable"}
- **emergency** — {"description": "safety-only path under emergency operational mode"}
- **safe-minimal** — {"description": "smallest safe path that still asserts validation predicate"}
- **advanced** — {"description": "expanded path for advanced/installer/administrator/maintenance roles"}
- **degraded** — {"description": "operational path under reduced capability"}

## Rules

- preferred > alternative > fallback > degraded > emergency > escalation
- safety-preserving overrides simplifying or shorter
- verified-truth path beats inferred path of same shape
- role-eligible paths beat role-gated paths the user cannot execute
- registered fallback beats improvisation (improvisation is forbidden)
- irreversible operations always require an explicit administrator-flow path

## Tie-breakers

- shortest declared path among same-class candidates
- fewest cross-product collisions
- highest declared maturity level of underlying nodes
- fewest unresolved validation findings on the path
