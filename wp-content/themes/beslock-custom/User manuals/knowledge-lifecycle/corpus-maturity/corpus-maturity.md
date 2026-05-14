# Corpus Maturity Governance

Dimensions, score formulas, maturity tiers, runtime-trustworthiness inputs.

## Maturity dimensions

- `operational-readiness` — rolls up from: operation, workflows, procedural-semantics, install
- `troubleshooting-maturity` — rolls up from: troubleshooting, troubleshooting-expanded, causal-graphs
- `warning-maturity` — rolls up from: warnings, warnings-expanded
- `continuity-maturity` — rolls up from: continuity-checkpoints
- `retrieval-readiness` — rolls up from: all domains with at least one ocr-derived-or-higher record
- `runtime-trustworthiness` — rolls up from: operationally-proven node count + replay determinism rate

## Score formula

- per-domain coverage_score = #(ocr-derived-or-higher) / #(declared)
- per-domain trust_score    = mean(tier_weight) over declared records
- per-product maturity      = weighted mean of dimension scores
- weights are declared, not learned; declared per phase
- scores are reproducible: same inputs → same outputs (no clock, no random)

## Maturity tiers

- `nascent` (< 0.30) — runtime: supervised pilot only
- `emerging` (0.30-0.60) — runtime: supervised + mandatory escalation routes
- `operational` (0.60-0.85) — runtime: supervised primary
- `mature` (>= 0.85) — runtime: supervised + replay-validated primary

## Runtime-trustworthiness inputs

- share of retrieval packages whose top-K avg weight >= 0.85
- share of supervised runs that complete without demotion
- replay determinism rate over the last K runs
- share of escalation-trace events that were declared (not surprise)
