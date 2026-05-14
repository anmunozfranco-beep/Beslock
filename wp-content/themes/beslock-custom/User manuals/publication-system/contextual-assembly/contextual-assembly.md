# Contextual Publication Assembly

Seven contextual inputs (procedures, warnings, troubleshooting, escalation guidance, continuity checkpoints, confidence disclosure, provenance references) bound deterministically into structured publications.

## Inputs

- `procedures` — source: knowledge-core; binding: ordered steps with preconditions
- `warnings` — source: knowledge-core (safety domain); binding: rendered verbatim, never abridged
- `troubleshooting` — source: knowledge-core (troubleshooting); binding: symptom → diagnosis → remediation
- `escalation-guidance` — source: HUMAN_OPERATIONS (layer 24); binding: escalation receiver + criterion
- `continuity-checkpoints` — source: CONTINUITY (layer 14); binding: checkpoint markers between major sections
- `confidence-disclosure` — source: RUNTIME / DECISION_INTELLIGENCE; binding: per-section confidence band when assembled at runtime
- `provenance-references` — source: knowledge-core/1.0; binding: source-node ids cited at section close

## Assembly rules

- assembly is deterministic given the same inputs and manifest
- assembly MUST NOT invent content; missing input → section omitted with a declared placeholder
- warnings MUST appear adjacent to the procedure they govern
- continuity checkpoints MUST be placed at governance-declared boundaries, never injected ad hoc
- confidence disclosure is mandatory whenever any contributing node is candidate-tier
- provenance references are mandatory for every published section
