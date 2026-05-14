# Executable Safety Validation

Declared safety predicates that must hold continuously throughout any proof slice.

## Predicates

- `no-unsafe-operational-flow` — no flow violates the declared safety-boundary set from RUNTIME_GOVERNANCE
- `no-hallucination` — every retrieved node is present in knowledge-core; no invented nodes; no invented steps
- `no-escalation-failure` — every triggered escalation reaches a declared receiver state (handed-off or queued+locked)
- `no-continuity-loss` — every interruption produces a checkpoint-or-degradation record; no silent loss
- `no-retrieval-ambiguity-silent` — ambiguity in retrieval is surfaced (never silently picked)
- `no-low-confidence-execution` — uncertain-confidence outputs do not advance to guidance emission without supervised review
- `no-governance-bypass` — no flow bypasses lifecycle P-tier gates, schema-pin, or any prior layer's contract
- `no-irreversibility-bypass` — irreversibility warnings are never downgraded; two-token gate is honored when destructive surfaces are touched (out of proof scope)
- `no-provenance-loss` — every emitted package carries a provenance manifest
- `no-supervision-loss` — every supervised boundary carries a supervision receipt

## Rules

- All safety predicates are mandatory for any proof slice.
- Failure of any safety predicate immediately demotes the slice.
- Safety validation results are append-only and signed.
- Safety predicates are evaluated continuously, not only at completion.
- Safety validation cannot be retroactively assigned.
