# Interruption Continuity

## Cases

- **user-pause** — {"resume_strategy": "resume-from-step", "requires_reconfirmation": false}
- **user-cancel** — {"resume_strategy": "rollback-to-checkpoint", "requires_reconfirmation": true}
- **session-timeout** — {"resume_strategy": "resume-from-checkpoint", "requires_reconfirmation": true}
- **device-disconnect** — {"resume_strategy": "rollback-or-escalate", "requires_reconfirmation": true}
- **power-loss-mid-step** — {"resume_strategy": "safe-restart-or-emergency-recovery", "requires_reconfirmation": true}
- **validation-failure** — {"resume_strategy": "retry-or-escalate", "requires_reconfirmation": true}
- **external-error** — {"resume_strategy": "retry-or-escalate", "requires_reconfirmation": true}

## Rules

- interruption preserves checkpoint anchors and provenance, never partial destructive state
- resume requires re-acknowledgement of any open warning
- destructive steps interrupted mid-execution require emergency-recovery, not auto-resume
- context restoration verifies state via validation predicate before continuing
- if no checkpoint exists, resume is forbidden; the procedure restarts from a declared safe state
- interruption events are recorded for knowledge-health intake

## Restoration Steps

- load declared context schema
- verify session-id and product-id
- re-evaluate validation predicate of last completed step
- re-acknowledge any open warnings/escalations
- verify checkpoint anchor (if applicable)
- rebind active hypotheses with current confidence tiers
- emit restoration provenance
