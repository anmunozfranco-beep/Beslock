# Dynamic Troubleshooting Branching

## Inputs

- observed-symptom
- failed-recovery-attempt-count
- current-operational-state
- user-role
- confidence-level
- unresolved-ambiguity
- environmental-conditions
- evidence-completeness

## Strategies

- **symptom-first** — {"trigger": "observed-symptom present", "effect": "branch to symptom-resolution path before procedural retry"}
- **retry-cap** — {"trigger": "failed-recovery-attempt-count >= threshold", "effect": "block further retries; escalate one tier per threshold rule"}
- **state-coherent-paths** — {"trigger": "current-operational-state declared", "effect": "only paths whose preconditions match the state are eligible"}
- **role-gated-paths** — {"trigger": "path requires elevated role", "effect": "filter out paths the current role cannot execute"}
- **confidence-gated-claims** — {"trigger": "confidence-level in {inferred,ocr-derived,ambiguous}", "effect": "downgrade resolution claims to 'likely-resolution' until verified by predicate"}
- **ambiguity-resolution-first** — {"trigger": "unresolved-ambiguity present", "effect": "ask disambiguating question (declarative) before progressing"}
- **environmental-fallback** — {"trigger": "environmental constraint blocks canonical path", "effect": "swap to registered fallback or escalate"}
- **evidence-disclosure-branch** — {"trigger": "evidence-completeness in {partial,missing,conflicting}", "effect": "annotate branch with disclosure; require explicit acknowledgement to proceed"}

## Rules

- all branches resolve from declared inputs (no opaque heuristics)
- no branch may bypass validation predicates of the underlying procedure
- branch eligibility must be deterministic given the context vector
- every branch carries provenance (which input(s) selected it)
- branch transitions never silently change user intent

## Retry Thresholds

- **validation-failure** — {"after": 3, "action": "escalate-to-tier-2"}
- **pairing-failure** — {"after": 3, "action": "escalate-to-tier-3"}
- **lockout-cycles** — {"after": 2, "action": "escalate-to-tier-3"}
- **battery-replacement-failure** — {"after": 1, "action": "escalate-to-tier-4-vendor"}
- **firmware-rollback-failure** — {"after": 1, "action": "escalate-to-tier-5-rma"}
