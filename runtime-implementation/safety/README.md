# Safety

Continuous safety predicates evaluated over every assembly-package.

Implementation: [runtime/safety.py](../runtime/safety.py).

## Predicates

1. `hallucination-resistance` — every emitted node id exists in its source file.
2. `no-low-confidence-execution` — low-confidence nodes are gated by supervision.
3. `no-ambiguous-guidance` — ambiguity is surfaced via escalation triggers.
4. `no-provenance-loss` — assembly manifest must exist and carry an id.
5. `no-governance-bypass` — no node carries `deprecated` / `rejected` validation status.
6. `no-continuity-loss` — continuity state must be present (read-only is OK).
7. `no-unsafe-retrieval` — assembly blockers prevent guidance emission.
8. `no-escalation-failure` — escalation tier is recorded when triggered.
9. `no-supervision-loss` — enforced at supervision-receipt emission time.

Failure of any predicate **demotes** the slice; demotion is the safe response.
