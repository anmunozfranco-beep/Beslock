# Access Filters

| id | default | stricter_for | override |
|---|---|---|---|
| maturity-floor | normalized | publication-bundle (verified), RAG (canonical-knowledge) |  |
| deprecation-filter | exclude |  | include_deprecated=true (records audit reason) |
| unresolved-isolation | exclude |  | include_unresolved=true (review-only surfaces) |
| low-confidence-veil | include-with-warning | safety-critical surfaces -> exclude |  |
| provenance-required | always |  |  |
| audience-scope | explicit |  |  |


## Rules

- Default access is safe-by-default; unsafe surfaces require explicit opt-in flags + audit trace.
- Deprecated knowledge is accessible only via override; surfaces MUST render a deprecation badge.
- Unresolved knowledge is isolated; never surfaces in retrieval-bundle by default.
- Low-confidence artifacts surfaced to safety-critical consumers MUST be excluded, not just warned.
- Every access call is loggable; access traces feed back into knowledge-health monitoring.
