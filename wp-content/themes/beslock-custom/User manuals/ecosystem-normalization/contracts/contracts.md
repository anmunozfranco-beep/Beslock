# Manifest & Contract Canonicalization

Single canonical authority per contract; canonical-references is the single source of truth.

## Canonical authorities

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

## Canonicalization rules

- every contract has exactly one authoritative declaring layer
- implementation modules cite the authoritative layer in their docstring (forward action)
- no contract is silently extended; extensions are governance actions
- no contract is silently versioned down; downgrades require a governance action
- canonical-references is the single source of truth for contract ownership
