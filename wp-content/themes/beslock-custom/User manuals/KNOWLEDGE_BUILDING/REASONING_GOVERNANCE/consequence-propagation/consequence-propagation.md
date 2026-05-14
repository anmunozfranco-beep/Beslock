# Consequence Propagation

## Types

- **direct-effect** — {"scope": "the step's declared outcome"}
- **side-effect** — {"scope": "declared collateral effects of the step"}
- **downstream-consequence** — {"scope": "effects on subsequent procedures or surfaces"}
- **unsafe-continuation-effect** — {"scope": "consequences when an unsafe path is forced"}
- **interrupted-state-consequence** — {"scope": "effects of leaving a procedure mid-step"}
- **recovery-impact** — {"scope": "effects propagated by recovery (rollback, retry, reset)"}
- **escalation-impact** — {"scope": "operational implications of moving up an escalation tier"}

## Rules

- consequences are declared, not inferred from history
- destructive steps must declare both direct and downstream consequences
- unsafe-continuation effects must list the safeguards being violated
- recovery impact must list which checkpoints/state restorations are required
- escalation impact must list which authority tier and which provenance is attached
- consequence claims carry confidence (verified-truth / inferred / OEM-confirmed)
- no consequence may silently downgrade a warning declared by knowledge-core
