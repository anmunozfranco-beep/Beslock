# Charter — Runtime Implementation Governance

Declares principles + authority for the first executable runtime track.

## Principles

- This layer binds the real executable runtime under `runtime-implementation/`.
- The runtime is read-only over knowledge-core; mutations are out of scope.
- The runtime is supervised by default; operator approval is mandatory at declared checkpoints.
- Every emitted package carries a provenance manifest with SHA-256 source hashes.
- Every cognition boundary emits a supervision receipt.
- Failure of any safety predicate demotes the slice; demotion is the safe response.
- The runtime cannot promote P-tier, elevate confidence, or alter prior governance layers.
- Hard exclusions bind the implementation: no autonomous agents, no production deployment, no images, no PDFs, no large frontend, no perf optimization.
- Macro-governance expansion is suspended; this is the implementation track.
- All implementation remains subordinate to the governed knowledge-core forever.

## Bound implementation

- `runtime-implementation/runtime/config.py` — paths, products, slice declaration, in-scope guard
- `runtime-implementation/runtime/provenance.py` — manifest builder, content hashing
- `runtime-implementation/runtime/retrieval.py` — scored retrieval over knowledge-core
- `runtime-implementation/runtime/assembly.py` — procedure + warnings + prerequisites + troubleshooting + continuity + adaptive merge
- `runtime-implementation/runtime/supervision.py` — review checkpoints, decisions, supervision receipts
- `runtime-implementation/runtime/safety.py` — continuous safety predicates
- `runtime-implementation/runtime/observability.py` — append-only NDJSON channels
- `runtime-implementation/runtime/flows.py` — six declared supervised flows
- `runtime-implementation/cli.py` — supervised CLI
- `runtime-implementation/testing/test_flows.py` — real unittest suite (14 tests)

## Hard Exclusions

- DO NOT expand macro-governance endlessly
- DO NOT create new universal cognition doctrines
- DO NOT create recursive architectural abstractions
- DO NOT build autonomous agents
- DO NOT deploy production systems
- DO NOT generate images / PDFs / large frontends
- DO NOT optimize scale / performance
