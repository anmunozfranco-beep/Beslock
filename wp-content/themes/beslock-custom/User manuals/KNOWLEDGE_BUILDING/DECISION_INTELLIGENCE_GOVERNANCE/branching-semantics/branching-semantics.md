# Branching Semantics

## Branch Types

- **procedural** — {"description": "branch declared inside a canonical procedure"}
- **conditional** — {"description": "branch driven by a declared boolean predicate over context vector"}
- **context-driven** — {"description": "branch selected from observed context dimensions"}
- **failure-driven** — {"description": "branch entered after a declared failure class"}
- **recovery** — {"description": "branch entered to restore a safe state"}
- **escalation** — {"description": "branch that hands off to a higher tier or OEM"}
- **ambiguity-driven** — {"description": "branch entered to resolve an ambiguous input"}

## Rules

- branches are declared, not invented at runtime
- branch selection is deterministic given the context vector
- each branch carries provenance (which input(s) selected it)
- branches preserve safeguards from the parent procedure
- branch transitions never silently change user intent
- branches must terminate (no infinite loops; cap by retry thresholds)

## Outcomes

- completed
- alternative-completed
- fallback-completed
- interrupted
- blocked
- escalated
- abandoned
