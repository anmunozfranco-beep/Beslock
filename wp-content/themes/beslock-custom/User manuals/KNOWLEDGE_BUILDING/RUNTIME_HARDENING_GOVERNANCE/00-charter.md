# Charter — Runtime Hardening Governance

Declares principles + authority for the corpus + runtime hardening track.

## Principles

- This layer hardens the runtime; it does not extend the architecture.
- Hardening is additive and non-destructive over per-product knowledge-core.
- Operational density is increased through declared candidate records, never fabricated truth.
- Every candidate record carries `validation_status: candidate-pending-review` and `confidence: candidate`.
- Confidence weighting is declarative; candidate nodes cannot outrank verified nodes on equal token overlap.
- Replay is deterministic by node-id-set parity, not by timing or score arithmetic.
- Macro-governance expansion remains suspended; this is the second and final implementation-track layer of Phase 27.
- All hardening is subordinate to knowledge-core and to all twenty prior layers.

## Bound modules

- `runtime-implementation/runtime/config.py` — ALLOWED_DOMAINS extended; CONFIDENCE_WEIGHTS table added
- `runtime-implementation/runtime/retrieval.py` — KIND_DOMAINS extended; confidence-weighted scoring; candidate_only manifest field
- `runtime-implementation/runtime/assembly.py` — candidate-only escalation triggers wired in
- `runtime-implementation/runtime/replay.py` — new module — deterministic replay harness
- `runtime-implementation/cli.py` — new `replay` subcommand
- `runtime-implementation/testing/test_hardening.py` — new tests for domains, weights, candidate disclosure, replay determinism
- `runtime-implementation/runtime-hardening/retrieval-quality/README.md` — doctrine note for retrieval hardening
- `runtime-implementation/runtime-hardening/replay-validation/README.md` — doctrine note for replay validation
- `tools/corpus_enrichment.py` — additive supplemental corpus builder (idempotent)

## Bound corpus surfaces

- `ext-images/<product>/knowledge-core/troubleshooting-expanded/`
- `ext-images/<product>/knowledge-core/warnings-expanded/`
- `ext-images/<product>/knowledge-core/continuity-checkpoints/`
- `ext-images/<product>/knowledge-core/causal-graphs/`
- `ext-images/<product>/knowledge-core/confidence-tiers/`

## Hard Exclusions

- DO NOT mutate any canonical per-product knowledge-core JSON
- DO NOT auto-promote candidate records
- DO NOT spawn macro-governance mega-layers
- DO NOT introduce stochastic ranking, ML, or embeddings
- DO NOT build autonomous agents
- DO NOT deploy production systems
