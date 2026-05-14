# Operational Causality

## Relation Types

- **causes** — {"description": "A directly produces B (deterministic)"}
- **enables** — {"description": "A makes B reachable but does not produce it"}
- **blocks** — {"description": "A prevents B"}
- **requires** — {"description": "B cannot occur without A"}
- **triggers** — {"description": "A initiates B as a side process"}
- **recovers-from** — {"description": "A restores a safe state after B"}
- **escalates-from** — {"description": "A is the escalation produced by B"}
- **confirms** — {"description": "A asserts B has occurred (validation predicate)"}
- **contradicts** — {"description": "A and B cannot both hold"}

## Domains

- actions
- states
- failures
- recoveries
- escalations
- confirmations
- interruptions

## Rules

- causal claims are declared, never inferred from co-occurrence
- every causal claim names its relation type and provenance
- deterministic 'causes' requires verified-truth evidence
- non-deterministic links use 'enables' or 'triggers' (never 'causes')
- absence of cause => the outcome cannot be asserted
- causality respects state transitions declared by EXECUTION_GOVERNANCE
- no causal link may bypass validation predicates
