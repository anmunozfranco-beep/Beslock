# Executable Deployment Slices

Six declared slices, each bounded by composition + kinds + halt conditions.

## Slices

- `onboarding-only-runtime` — composition: local-supervised-stack; kinds: pairing, onboarding-prereqs; halts on: safety-demote
- `troubleshooting-runtime` — composition: local-supervised-stack; kinds: troubleshooting, warnings; halts on: candidate-only + irreversible-adjacent
- `reviewer-runtime` — composition: reviewer-stack; kinds: queue-claim, evidence-pull, decision; halts on: missing-binding
- `governance-runtime` — composition: controlled-pilot-stack (governance-scoped subset); kinds: scope-assign, revoke, emergency-intervention; halts on: dual-audit-disagreement
- `ingestion-runtime` — composition: ingestion-stack; kinds: fetch, checksum-verify, stage, dual-review; halts on: checksum-mismatch
- `replay-runtime` — composition: replay-stack; kinds: replay-run, drift-compare, finding-emit; halts on: replay-drift > floor

## Invariants

- every slice is bounded by composition + kinds + halt conditions
- every slice emits a slice-manifest at startup and at every halt
- no slice silently widens its kinds
- no slice resumes from a halt without an operator decision
- every slice is product-scoped; cross-product slices are forbidden
