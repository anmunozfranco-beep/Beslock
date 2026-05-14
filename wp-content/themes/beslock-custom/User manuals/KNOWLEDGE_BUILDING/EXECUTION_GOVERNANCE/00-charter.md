# 00 — Execution Governance Charter

## Principles
1. Execution is observed and modelled; the layer does not perform operations.
2. State transitions are explicit, validated, and provenance-attached.
3. Completion is positively asserted; absence of error is not completion.
4. Interruption is a first-class concept; recovery paths are declared, not improvised.
5. Failure classification is non-negotiable: recoverable vs unrecoverable.
6. Destructive operations require explicit-action confirmation and irreversibility warnings.
7. Unsafe sequences are blocked at composition time; the execution layer enforces the prohibition.
8. Execution governance is subordinate to knowledge-core, lifecycle, validation, access, composition.
9. Future execution consumers inherit execution contracts; contracts never bend to satisfy a consumer.

## Authority areas
- state-models
- flow-semantics
- interruption-recovery
- failure-states
- intent-progression
- confirmation-semantics
- safe-execution
- execution-governance
- execution-risks
- future-execution-readiness

## Hard guarantees
- Modeling-only. Builds no chatbots, PDFs, images, renderers, frontends, automation runtimes.
- Read-only. Mutates no per-product knowledge.
- Subordinate. Cannot override knowledge-core, lifecycle, validation, access, composition governance.
- Deterministic. Same starting state + inputs => reproducible execution traces.
