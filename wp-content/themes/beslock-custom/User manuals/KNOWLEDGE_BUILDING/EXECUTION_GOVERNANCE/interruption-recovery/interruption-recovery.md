# Interruption & Recovery

| id | user_initiated | safe | resume_strategy |
|---|---|---|---|
| user-pause | True | True | resume-from-last-step |
| user-cancel | True | True | rollback-to-checkpoint |
| session-timeout | False | True | resume-from-last-checkpoint |
| device-disconnect | False | False | rollback-to-checkpoint OR escalate |
| power-loss-mid-step | False | False | safe-restart-from-initial OR emergency-recovery |
| validation-failure | False | False | retry-step OR escalate |
| external-error | False | False | retry-or-escalate-with-cause |

## Recovery rules

- Every procedure declares ≥1 checkpoint as a safe re-entry anchor.
- Rollback never partially applies a destructive step; either the destructive step completes fully or it never began.
- Restart from initial state requires explicit user re-confirmation if any destructive step had previously begun.
- Recovery from `pairing-failed`, `enrollment-failed`, `lockout` returns to the prior safe state, never directly to a terminal state.
- Power-loss during destructive procedures (factory-reset, firmware-upgrade) requires emergency-recovery; never auto-resume.
- Recovery traces preserve provenance: original procedure id, interruption cause, recovery path taken.
