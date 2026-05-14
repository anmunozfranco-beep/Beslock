# Ambiguity Resolution Semantics

## Types

- **missing-evidence** — {"trigger": "required evidence node absent"}
- **conflicting-evidence** — {"trigger": "two verified-truth claims disagree"}
- **incomplete-procedure** — {"trigger": "step missing precondition or validation predicate"}
- **unclear-troubleshooting-state** — {"trigger": "no eligible branch resolves from current context"}
- **uncertain-recovery** — {"trigger": "no checkpoint AND destructive-step started"}
- **ambiguous-intent** — {"trigger": "intent-clarity in {ambiguous,missing} for non-trivial action"}
- **shared-concept-collision** — {"trigger": "concept reused across products without canonical owner"}

## Rules

- ambiguity is named, not silently resolved
- destructive decisions never proceed under ambiguity
- ambiguity must select between: ask-disambiguation, withhold, or escalate
- default behavior under ambiguity = the safest of the three
- every ambiguity event is recorded for knowledge-health intake
- OEM-confirmation is the only resolver for verified-truth conflicts on P0 procedures

## Resolution Paths

- **ask-disambiguation** — {"when": "intent-clarity ambiguous AND non-destructive", "effect": "surface declarative question"}
- **withhold** — {"when": "evidence missing AND non-destructive", "effect": "decline to assert; expose disclosure"}
- **escalate** — {"when": "destructive OR irrecoverable OR conflicting verified-truth", "effect": "hand off to higher tier or OEM"}
