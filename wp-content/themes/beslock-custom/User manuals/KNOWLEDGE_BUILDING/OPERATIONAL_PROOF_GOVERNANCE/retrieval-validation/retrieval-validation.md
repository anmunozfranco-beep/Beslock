# Retrieval Execution Validation

Declared retrieval validation predicates per retrieval kind.

## Predicates

- `semantic-precision-≥-threshold` (semantic) — fraction of retrieved nodes that match query intent
- `semantic-recall-≥-threshold` (semantic) — fraction of relevant nodes returned vs declared ground-truth set
- `contextual-coherence-no-contradiction` (contextual) — no chain of retrieved nodes contradicts knowledge-core verified-truth
- `guidance-completeness-mandatory-warnings` (guidance) — every mandatory warning attached to selected nodes is present in package
- `guidance-completeness-required-steps` (guidance) — every required step in declared workflow is present in package
- `onboarding-coverage` (onboarding) — every declared onboarding flow has retrievable bound nodes
- `troubleshooting-coverage-symptom` (troubleshooting) — for each symptom, ≥1 retrievable diagnostic node exists
- `troubleshooting-coverage-causal` (troubleshooting) — for each symptom, declared causal edges are traversable
- `escalation-retrievability` (escalation) — for every declared escalation predicate, retrievable handoff procedure exists
- `provenance-attachment` (all) — every retrieval-package carries a provenance manifest

## Rules

- Predicates are declared; ad-hoc validation is unsafe.
- Failure of any high-severity predicate blocks promotion of the slice past proof.
- Validation results are append-only and signed with provenance.
- Validation cannot mutate knowledge-core under any circumstance.
- Predicates are evaluated per product when scope is per-product.
