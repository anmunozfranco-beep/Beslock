# Canonical Deployment Composition

Six declared compositions, each with environment, modules, supervision, and exclusions.

## Compositions

- `local-supervised-stack` — env: local-supervised-runtime; modules: retrieval-runtime, orchestration-runtime, escalation-runtime, provenance-system (read-only mount), observability-system
- `reviewer-stack` — env: reviewer-operation-environment; modules: reviewer-operations, observability-system (read-only tail), provenance-system (read-only mount)
- `ingestion-stack` — env: oem-ingestion-environment; modules: oem-ingestion-system, observability-system, provenance-system (staged-write only)
- `replay-stack` — env: local-supervised-runtime or staging; modules: replay-system, retrieval-runtime (re-call only), observability-system (read-only tail)
- `observability-stack` — env: any (read-only consumer); modules: observability-system
- `controlled-pilot-stack` — env: controlled-pilot; modules: retrieval-runtime, orchestration-runtime, escalation-runtime, provenance-system (read-only), observability-system, reviewer-operations (scoped)

## Invariants

- every deployment composition declares its environment, modules, supervision, and exclusions
- no composition includes a module not authorized for its environment's trust zone
- no composition silently widens its module set
- no composition shares mutable state with another composition
- every composition emits a composition-manifest at startup
