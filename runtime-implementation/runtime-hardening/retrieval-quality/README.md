# Retrieval Quality Hardening (Phase 27, Layer 21)

## What changed
- `runtime/config.py::ALLOWED_DOMAINS` extended to include the five
  Phase 27 supplemental domains: `troubleshooting-expanded`,
  `warnings-expanded`, `continuity-checkpoints`, `causal-graphs`,
  `confidence-tiers`. The runtime is still **read-only** with respect to
  per-product knowledge-core.
- `runtime/config.py::CONFIDENCE_WEIGHTS` introduces a finite, declarative
  weight table (verified-oem 1.0 → unresolved 0.10). Unknown confidence
  values fall back to 0.50 (declared, not silent).
- `runtime/retrieval.py::KIND_DOMAINS` now routes the `troubleshooting`,
  `warnings`, `escalation`, and `battery-recovery` kinds through both
  the canonical and supplemental folders, plus two new kinds:
  `continuity` and `causal`.
- Scoring is now `Jaccard(query, node) * CONFIDENCE_WEIGHTS[node.confidence]`.
  Candidate-only nodes can no longer outrank verified nodes on equal
  token overlap.
- A new manifest field `extra.candidate_only=True` is emitted by every
  retrieval-package whose top-K is composed entirely of `candidate` /
  `unresolved` nodes. This is consumed by `assembly.py` as two new
  escalation triggers: `procedure-candidate-only` and
  `troubleshooting-candidate-only`.

## What did **not** change
- No per-product knowledge-core JSON was mutated.
- No new ML, embeddings, vector index, or stochastic ranker.
- No autonomous recovery or auto-approval paths.
- The hard scope guard (`config.assert_in_scope`) and the read-only
  posture remain intact.

## Test coverage
- `testing/test_hardening.py::ConfigHardeningTests` — domain + weights.
- `testing/test_hardening.py::CandidateWeightingTests` — bounded scores
  + honest `candidate_only` manifest disclosure.
- Full suite: 19 tests, all pass.
