# Canonical References — Single Source of Truth

Maps every contract, doctrine stack, and canonical term to its authoritative layer.

## Contract authorities

- `runtime-package-manifest` → REFERENCE_STACK_GOVERNANCE (layer 26) — packaging/
- `runtime-contract (retrieve)` → REFERENCE_STACK_GOVERNANCE — interoperability/
- `escalation-contract` → REFERENCE_STACK_GOVERNANCE — interoperability/
- `provenance-contract` → knowledge-core/1.0 + REFERENCE_STACK_GOVERNANCE
- `replay-contract` → RUNTIME_HARDENING_GOVERNANCE (layer 21) + REFERENCE_STACK_GOVERNANCE
- `retrieval-contract (Jaccard×weight)` → RUNTIME_HARDENING_GOVERNANCE + REFERENCE_STACK_GOVERNANCE
- `governance-contract` → REFERENCE_STACK_GOVERNANCE
- `continuity-contract` → CONTINUITY_GOVERNANCE + REFERENCE_STACK_GOVERNANCE
- `deployment-manifest` → REFERENCE_STACK_GOVERNANCE — packaging/
- `environment-manifest` → ENVIRONMENT_AND_INTEGRATION_GOVERNANCE (layer 25)
- `integration-contracts (7)` → ENVIRONMENT_AND_INTEGRATION_GOVERNANCE
- `trust-zone mapping` → ENVIRONMENT_AND_INTEGRATION_GOVERNANCE
- `supervision-receipt` → HUMAN_OPERATIONS_GOVERNANCE (layer 24)
- `operator-identity field` → HUMAN_OPERATIONS_GOVERNANCE

## Doctrine ownership

- `execution-stack` — EXECUTION = abstract execution model; RUNTIME = realization strategy; RUNTIME_ORCHESTRATION = supervised loop; RUNTIME_IMPLEMENTATION = real Python package; PROTOTYPE_RUNTIME = prototype slice; RUNTIME_HARDENING = supplemental corpus + replay
- `knowledge-stack` — LIFECYCLE = content lifecycle; KNOWLEDGE_LIFECYCLE = trust lifecycle (candidate→trusted); KNOWLEDGE_OPERATIONS = operator tooling/workflows
- `deployment-stack` — REALIZATION = value/sequencing; ENVIRONMENT_AND_INTEGRATION = trust zones + integration contracts; REFERENCE_STACK = canonical module composition
- `ecosystem-stack` — INTEROPERABILITY = cross-system contracts; NORMALIZATION = internal coherence + dedup
- `human-stack` — single owner of operator UX, HITL, explainability, ergonomics
- `intelligence-stack` — ADAPTIVE = context adaptation; DECISION = branching/confidence; REASONING = causality/uncertainty; CONTINUITY = sessions/snapshots
- `platform-foundation` — foundational layers; each owns its declared scope; no overlap

## Canonical terms

- `package`
- `manifest`
- `node`
- `candidate`
- `supervision-receipt`
- `checkpoint`
- `trust-zone`
- `trust-tier`
- `slice`
- `composition`
- `operator`
- `channel`
