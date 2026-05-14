# Runtime Explainability UX

Six explanation patterns, each sourced from append-only logs and reproducible.

## Explainability patterns

- `retrieval-reasoning` — shows: query tokens, matched node tokens, Jaccard score, confidence weight, final score
- `escalation-trigger` — shows: trigger id, underlying signal, rule that fired, next required actor
- `confidence-disclosure` — shows: per-node tier, tier weight, candidate_only flag, human-review status
- `provenance-inspection` — shows: manifest_id, source_files[].sha256, extract_lineage, binding chain
- `continuity-visualization` — shows: checkpoint timeline, current snapshot id, resume points, last continuity-trace event
- `operational-uncertainty` — shows: ambiguous=True, no-results, candidate-only, missing-prerequisite

## Invariants

- explanation is sourced from append-only logs, never from speculation
- explanation always precedes the recommendation in the operator surface
- explanation is reproducible: same logs → same explanation
- explanation does not editorialize: it surfaces declared fields, not narratives
- explanation never conceals uncertainty to improve operator UX
