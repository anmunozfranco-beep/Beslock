# Human ↔ Runtime Interaction Model

## Model

- **supervision-boundary** — {"rule": "destructive operations are supervised: explicit-action by an authorised human is mandatory"}
- **override-semantics** — {"rule": "human override may relax simplifying adaptations but never safety-preserving ones"}
- **escalation-handoff** — {"rule": "escalation handoff is human-receiving; the runtime cannot resolve OEM-required events"}
- **operator-intervention-points** — {"rule": "declared at: confirmation steps, ambiguity resolutions, recovery decisions, escalation tiers"}
- **approval-checkpoints** — {"rule": "destructive steps and irreversible operations require approval checkpoints with provenance"}
- **uncertainty-signaling** — {"rule": "runtime must signal confidence + disclosure to the human surface; never silently assert"}

## Rules

- the runtime is supervised by default; autonomous behaviour is not modelled here
- humans may approve, reject, request more information, or escalate
- human approval is recorded with identity (when declared) and provenance
- human override events feed knowledge-health intake
- no human override may downgrade an irreversibility warning
