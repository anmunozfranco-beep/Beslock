# Session-Aware Guidance

## Signals

- previous-failure-count
- prior-escalations
- repeated-troubleshooting-cycles
- operational-fatigue (measured-by retry density)
- incomplete-onboarding-flag
- degraded-trust (measured-by repeated validation-failures)
- open-warning-backlog

## Adaptations

- **elevate-warnings-after-repeated-failures** — {"trigger": "previous-failure-count >= 3", "effect": "warnings surfaced one level higher"}
- **suggest-escalation-after-cycles** — {"trigger": "repeated-troubleshooting-cycles >= 2", "effect": "surface escalation-recommendation"}
- **fatigue-aware-pruning** — {"trigger": "operational-fatigue=high", "effect": "compact non-essential steps; preserve safety-critical"}
- **onboarding-resume-on-incomplete** — {"trigger": "incomplete-onboarding-flag=true", "effect": "offer resume-from-stage when context is recoverable"}
- **degraded-trust-disclosure** — {"trigger": "degraded-trust=true", "effect": "increase evidence disclosure; downgrade claim strength"}
- **warning-backlog-block** — {"trigger": "open-warning-backlog > 0", "effect": "block destructive ops until warnings acknowledged"}

## Rules

- session adaptations may shape presentation but never weaken safeguards
- session-derived elevation is auditable (signal -> adaptation)
- session signals never silently elevate confidence
- incomplete-onboarding cannot be marked verified by session inference
- session adaptations are subordinate to ADAPTIVE_OPERATIONAL_GOVERNANCE precedence
