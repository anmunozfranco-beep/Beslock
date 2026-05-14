# Runtime Interoperability Contracts

Seven declared interoperability contracts; versioned, testable, reversible.

## Contracts

- `runtime-contract` — scope: retrieval ↔ orchestration; shape: `retrieve(product, query, kind) → {nodes[], manifest{extra.candidate_only?}}`
- `escalation-contract` — scope: orchestration ↔ escalation; shape: `_evaluate_escalation(packages) → triggers[{id, source, rule}]`
- `provenance-contract` — scope: any-module ↔ provenance; shape: `read: load(path) → JSON; write: governance-pipeline-only with manifest_id + source_files[].sha256`
- `replay-contract` — scope: replay ↔ runtime + observability; shape: `replay_run(run_id) → {deterministic: bool, drift?: details}`
- `retrieval-contract` — scope: retrieval ↔ provenance; shape: `read-only load of canonical knowledge-core JSON; scoring = Jaccard × CONFIDENCE_WEIGHTS[node.confidence]`
- `governance-contract` — scope: governance ↔ all modules; shape: `scope assignment / revocation / emergency intervention; dual-audited; append-only`
- `continuity-contract` — scope: orchestration ↔ continuity; shape: `checkpoint snapshot id + resume points; append-only continuity-trace events`

## Discipline

- every contract declares scope, shape, and an append-only event surface
- every contract is versioned; breaking changes require a governance action
- every contract refuses to suppress provenance, candidate-only, or supervision-receipt fields
- every contract is reversible: any party may withdraw; revocation is first-class
- every contract is testable: a substitute satisfying the contract is interchangeable
