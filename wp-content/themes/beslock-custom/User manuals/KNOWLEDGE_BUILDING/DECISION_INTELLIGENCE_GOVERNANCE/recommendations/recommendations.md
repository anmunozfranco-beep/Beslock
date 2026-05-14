# Adaptive Recommendation Intelligence

## Kinds

- **next-step-recommendation** — {"scope": "within an active procedure"}
- **recovery-recommendation** — {"scope": "after failure / interruption"}
- **alternative-path-recommendation** — {"scope": "when preferred path is blocked"}
- **safety-first-recommendation** — {"scope": "when severity >= warning"}
- **simplification-recommendation** — {"scope": "for beginner / operator roles"}
- **evidence-disclosure-recommendation** — {"scope": "when confidence < high"}
- **escalation-recommendation** — {"scope": "when ambiguity / irrecoverable / OEM-required"}

## Rules

- recommendations are derived from declared decision points and path classes (no opaque ranking)
- recommendations are not commands; they describe options with justifications
- safety-first ranking dominates simplification ranking
- recommendations carry confidence + provenance
- recommendations never invent steps absent from the canonical procedure
- destructive recommendations require explicit-action confirmation contract
- recommendations remain subordinate to knowledge-core and prior governance layers

## Prioritization

- safety > recovery > escalation > alternative > simplification > next-step
- high-confidence > low-confidence within the same kind
- role-eligible > role-gated within the same kind
- verified-truth > inferred within the same kind
