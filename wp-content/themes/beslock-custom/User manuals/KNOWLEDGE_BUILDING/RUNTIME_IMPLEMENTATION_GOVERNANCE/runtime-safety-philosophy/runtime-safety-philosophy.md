# Runtime Safety Philosophy

Safety predicates are continuous; failure demotes; hallucination halts.

## Principles

- Safety predicates are continuous, not terminal.
- Failure demotes; it does not silently pass.
- Hallucination (any node id absent from its source file) is a halt event.
- Irreversibility warnings cannot be downgraded.
- Governance bypass attempts halt the slice and demote.
