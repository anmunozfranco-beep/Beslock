# VALIDATION_GOVERNANCE

Constitutional layer governing **operational validation and semantic QA** of the
Beslock knowledge center.

- Schema: `validation-governance/1.0`
- Generated: 2026-05-13
- Subordinate to: `knowledge-core`, `LIFECYCLE_GOVERNANCE`
- Coexists with: `VISUAL_GOVERNANCE`, `KNOWLEDGE_CENTER`, `SEMANTIC_GOVERNANCE`,
  `EXPERIENCE_GOVERNANCE`, `LIFECYCLE_GOVERNANCE`

This layer is **read-only**. It does not modify per-product `knowledge-core/`
files. It runs validators, produces typed findings, and publishes scorecards.

## Authority areas
- procedural-integrity
- workflow-executability
- entity-consistency
- graph-validation
- experience-validation
- retrieval-validation
- maturity-validation
- health-scoring
- validation-philosophy
- future-system-safety

## Doctrine layout
- `00-charter.md` — principles + authority areas
- `procedural-integrity/` — step-chain & sequence rules
- `workflow-executability/` — operational completeness rules
- `entity-validation/` — entity id, surface, collision rules
- `graph-validation/` — connectivity, orphan, cycle rules
- `experience-validation/` — cross-reference to EXPERIENCE_GOVERNANCE
- `retrieval-validation/` — channel + summary + provenance rules
- `maturity-validation/` — status / confidence / ocr coherence rules
- `health-scorecards/` — per-product scoring methodology
- `validation-philosophy/` — read-only, idempotent, zero-tolerance principles
- `future-system-safety/` — downstream-consumer inheritance gates

Reports: `_repository-governance/reports/validation/01..10`.
