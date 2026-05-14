# Confidence Disclosure Doctrine

Confidence is a declared tier; candidate-only retrieval is honestly surfaced.

## Principles

- Confidence is a tier, not a number-from-thin-air.
- Tiers are declared per product in `confidence-tiers/confidence-tier-manifest-<product>.json`.
- Runtime ranking weights confidence as a declarative multiplier over Jaccard.
- Candidate-only retrieval is honestly disclosed in the package manifest (`extra.candidate_only=True`).
