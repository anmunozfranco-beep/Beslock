# Fallback & Degraded Operation

## Degradation Levels

- **full** — {"description": "all capabilities available"}
- **reduced** — {"description": "non-essential capabilities suppressed"}
- **safety-only** — {"description": "only safety-critical actions and observation permitted"}
- **read-only** — {"description": "no state-changing actions; observation allowed"}
- **halted** — {"description": "no operation; escalate"}

## Fallback Patterns

- **manual-fallback** — {"trigger": "automation/electronic path unavailable", "effect": "expose declared manual procedure if registered"}
- **physical-key-fallback** — {"trigger": "electronic-unlock path unavailable AND device supports physical-key", "effect": "guide to physical-key procedure"}
- **offline-fallback** — {"trigger": "environmental=offline", "effect": "restrict to offline-safe procedures only"}
- **low-battery-fallback** — {"trigger": "environmental=low-battery", "effect": "block firmware/destructive ops; permit replacement and unlock"}
- **low-confidence-fallback** — {"trigger": "confidence-level in {inferred,ocr-derived,ambiguous}", "effect": "downgrade to 'likely-procedure' framing; require explicit acknowledgement"}
- **emergency-recovery** — {"trigger": "irrecoverable failure mid-destructive op", "effect": "halt and surface vendor/RMA escalation; never auto-resume"}

## Rules

- degradation may reduce capabilities but never weaken safeguards
- fallback procedures must themselves be governed (charters, predicates, provenance)
- absence of a registered fallback => block + escalate (never improvise)
- degraded-mode transitions are observable and recorded
- return to 'full' requires verified restoration (predicate, not assumption)
