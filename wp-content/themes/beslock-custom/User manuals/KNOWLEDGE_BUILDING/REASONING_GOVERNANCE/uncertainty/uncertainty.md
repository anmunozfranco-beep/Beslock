# Uncertainty-Aware Reasoning

## Kinds

- **evidence-incomplete** — {"treatment": "downgrade conclusions; require explicit acknowledgement"}
- **evidence-missing** — {"treatment": "block dependent conclusion; surface disclosure"}
- **inferred-state** — {"treatment": "label state as inferred; do not drive destructive ops"}
- **ambiguous-input** — {"treatment": "ask-disambiguation or withhold"}
- **oem-required** — {"treatment": "withhold and escalate to OEM channel"}
- **low-confidence-path** — {"treatment": "present as alternative-path, not preferred"}
- **irreducible-uncertainty** — {"treatment": "surface explicitly; never hide as a guess"}

## Rules

- uncertainty is named, not hidden
- uncertainty propagates: a chain step's confidence cannot exceed its inputs
- destructive operations require high-confidence inputs along the entire chain
- uncertainty disclosure is non-suppressible by adaptive presentation
- OEM-required uncertainty cannot be resolved by inference
- uncertainty events are recorded for knowledge-health intake
