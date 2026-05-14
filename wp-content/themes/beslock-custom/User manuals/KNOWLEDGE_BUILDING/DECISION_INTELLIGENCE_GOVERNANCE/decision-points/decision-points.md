# Operational Decision Points

## Decision Points

- **retry-vs-recovery** — {"context": "after validation-failure or step-failure", "options": ["retry-same-step", "enter-recovery"], "default": "retry-same-step (capped by retry-threshold)"}
- **reset-vs-troubleshooting** — {"context": "persistent failure with available troubleshooting paths", "options": ["troubleshoot-first", "factory-reset"], "default": "troubleshoot-first (factory-reset only as last resort, administrator-only)"}
- **administrator-vs-beginner-flow** — {"context": "step requires elevated authority", "options": ["beginner-flow", "administrator-flow"], "default": "role-gated (no silent elevation)"}
- **degraded-vs-escalation** — {"context": "environment or evidence prevents canonical path", "options": ["registered-fallback", "escalate"], "default": "registered-fallback if present; otherwise escalate"}
- **safe-continue-vs-interrupt** — {"context": "warning surfaced mid-procedure", "options": ["continue-with-acknowledgement", "interrupt-and-recover"], "default": "interrupt-and-recover when severity >= warning"}
- **local-recovery-vs-oem** — {"context": "irrecoverable or vendor-bound failure", "options": ["local-recovery", "oem-intervention"], "default": "oem-intervention for irrecoverable / firmware-bricked"}
- **manual-vs-electronic-path** — {"context": "electronic path unavailable AND manual fallback registered", "options": ["manual-fallback", "wait-and-retry"], "default": "manual-fallback when registered"}
- **verified-vs-inferred-claim** — {"context": "guidance must produce a claim", "options": ["assert-verified", "downgrade-to-likely", "withhold"], "default": "downgrade-to-likely or withhold based on confidence tier"}
- **cancel-vs-rollback** — {"context": "user-cancel mid-procedure", "options": ["cancel-no-state-change", "rollback-to-checkpoint"], "default": "rollback-to-checkpoint when checkpoints exist"}
- **single-attempt-vs-batch** — {"context": "non-destructive sequence with installer/admin role", "options": ["per-step", "batched"], "default": "batched only for non-destructive declared sequences"}
- **ask-disambiguation-vs-proceed** — {"context": "intent-clarity in {ambiguous,missing}", "options": ["ask-disambiguation", "proceed-with-default"], "default": "ask-disambiguation (no silent default for destructive ops)"}

## Rules

- every decision point declares its options, default, and selection predicate
- no decision point has an undeclared 'else' path
- destructive decisions require explicit-action; never selected silently
- decision outputs are observable and provenance-tagged
- decision points cannot bypass validation predicates of the underlying procedure
