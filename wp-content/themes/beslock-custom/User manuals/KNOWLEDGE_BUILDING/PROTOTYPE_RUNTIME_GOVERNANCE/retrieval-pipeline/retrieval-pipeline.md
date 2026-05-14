# Executable Retrieval Pipeline

Six declared retrieval kinds with predicate validation and a shared six-stage pipeline.

## Stages

- intent-bind
- access-pattern-resolve
- fetch-read-only
- validate-predicates
- attach-provenance-manifest
- emit-retrieval-package

## Kinds

- `operational-procedures` — predicates: completeness-required-steps, provenance-attachment
- `troubleshooting` — predicates: coverage-symptom, coverage-causal, provenance-attachment
- `warnings` — predicates: mandatory-warnings-attached, severity-stamped, provenance-attachment
- `onboarding` — predicates: coverage, provenance-attachment
- `escalation` — predicates: retrievability, 12-field-shape, provenance-attachment
- `adaptive-guidance` — predicates: precedence-respected, no-confidence-elevation, provenance-attachment

## Rules

- Pipeline is read-only; mutations are out of scope for the prototype.
- Predicate failures gate emission; ambiguity is surfaced, not silently resolved.
- Pipeline outputs bind to a run-id + slice-id and are append-only.
- Pipeline cannot retroactively alter prior emissions.
