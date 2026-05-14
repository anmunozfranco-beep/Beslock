# Multi-Step Reasoning Chains

## Chain Types

- **sequential** — {"description": "linear deduction across declared steps"}
- **dependent** — {"description": "later inferences depend on earlier verified outcomes"}
- **branching** — {"description": "chain forks at a declared decision point"}
- **recovery** — {"description": "chain re-enters at a checkpoint after failure"}
- **troubleshooting** — {"description": "chain advances by symptom-resolution branches"}
- **deductive** — {"description": "from declared facts and predicates to a conclusion"}
- **abductive** — {"description": "best-fit hypothesis among declared alternatives (always downgraded)"}

## Rules

- every chain is reproducible from declared inputs (context vector + evidence)
- every chain step records: predicate, inputs, evidence tier, confidence
- chain steps cannot invent new procedure steps
- abductive steps must be presented as 'likely', never 'verified'
- chains terminate (no infinite reasoning; bounded by retry thresholds)
- a chain that crosses an unsafe transition must be halted and escalated
- chains preserve user intent; intent change requires a new chain with provenance link

## Termination Outcomes

- concluded-verified
- concluded-likely
- inconclusive
- blocked
- escalated
- abandoned
