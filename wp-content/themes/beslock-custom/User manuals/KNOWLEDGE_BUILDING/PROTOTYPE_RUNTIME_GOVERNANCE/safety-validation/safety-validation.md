# Operational Safety Validation

Nine declared safety predicates evaluated continuously throughout any prototype run.

## Predicates

- `hallucination-resistance` — every emitted node is present in knowledge-core; no invented nodes/steps/edges
- `no-unsafe-retrieval` — no retrieval crosses safety-boundary set declared by RUNTIME_GOVERNANCE
- `no-escalation-failure` — every triggered escalation reaches a declared receiver state
- `no-continuity-loss` — every interruption produces checkpoint or degradation record (no silent loss)
- `no-ambiguous-guidance` — ambiguity is surfaced with candidate set; never silently picked
- `no-low-confidence-execution` — uncertain-confidence outputs do not advance to guidance emission without supervised review
- `no-provenance-loss` — every emitted package carries a provenance manifest
- `no-supervision-loss` — every supervised boundary carries a supervision receipt
- `no-governance-bypass` — no flow bypasses lifecycle P-tier, schema-pin, or any prior contract

## Rules

- All safety predicates are mandatory throughout the prototype run.
- Failure of any predicate immediately demotes the slice.
- Validation results are append-only and signed.
- Predicates are evaluated continuously, not only at completion.
