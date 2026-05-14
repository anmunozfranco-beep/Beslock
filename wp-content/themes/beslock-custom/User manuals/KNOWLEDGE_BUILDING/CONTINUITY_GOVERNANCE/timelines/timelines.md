# Operational Timelines

## Timeline Types

- **onboarding-timeline** — {"stages": ["unboxed", "physically-installed", "powered", "paired", "enrolled", "verified"]}
- **installation-timeline** — {"stages": ["site-survey", "mounting", "wiring", "power-up", "configuration", "verified-install"]}
- **troubleshooting-timeline** — {"stages": ["symptom-observed", "hypothesis-proposed", "diagnostic", "resolution-attempt", "outcome-evaluated"]}
- **recovery-timeline** — {"stages": ["failure-detected", "checkpoint-restored", "retry-or-rollback", "validation", "restored-or-escalated"]}
- **maintenance-timeline** — {"stages": ["scheduled-or-triggered", "battery-or-firmware-action", "verification", "logged"]}
- **escalation-timeline** — {"stages": ["tier-1", "tier-2", "tier-3", "tier-4-vendor", "tier-5-rma"]}
- **degraded-operation-timeline** — {"stages": ["entered-degradation", "fallback-active", "monitoring", "restoration-attempted", "restored-or-halted"]}

## Rules

- every timeline declares its stages and admissible transitions
- stage transitions carry timestamps + provenance + confidence
- no timeline may invent stages not declared in its model
- timelines reference EXECUTION_GOVERNANCE state transitions; they do not duplicate them
- concurrent timelines (e.g. troubleshooting during onboarding) are explicitly linked
- a closed timeline cannot be silently reopened (only via declared continuation)
