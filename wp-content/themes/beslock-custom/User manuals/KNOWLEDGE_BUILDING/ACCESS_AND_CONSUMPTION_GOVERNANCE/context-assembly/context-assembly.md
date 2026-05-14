# Assembly Profiles

| id | core | expands | filters |
|---|---|---|---|
| procedural-context | by-procedure | prerequisites, warnings, referenced-entities, visual-intent | maturity ≥ normalized, exclude deprecated |
| troubleshooting-context | by-troubleshooting | recovery-path, escalation-tier, related-warnings | maturity ≥ normalized, include verified preferred |
| onboarding-context | by-onboarding | learning-path, guidance-triggers, cognitive-load-map | audience-scoped, interruption-budget ≤ 2 |
| publication-context | by-domain | publication-intent, deprecation-badges, lineage | maturity ≥ verified, exclude unresolved |
| provenance-context | by-provenance | source_refs, extraction_lineage, version | read-only |


## Rules

- Every assembled context records: profile id, source artifact ids, applied filters, generation timestamp.
- Warnings scoped to a procedure MUST be injected into procedural-context.
- Prerequisites MUST be expanded transitively but capped at depth 3 to prevent runaway expansion.
- Maturity-aware filtering is mandatory; consumers cannot opt out of safety filters.
- Confidence-aware assembly: a context whose core artifact is `confidence=low` MUST emit a confidence-warning.
- Provenance-aware assembly: every included artifact carries its source_refs into the bundle.
