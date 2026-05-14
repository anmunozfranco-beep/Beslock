# runtime-orchestration

Phase 43 — governed refresh, rebuild & propagation orchestration. Modeling-only. No executable orchestrator. No CI/CD. No autonomous agents. No source-truth mutation. Reviewer authorization required for every scoped refresh.

Subroots:
- dependency-graph/
- refresh-pipelines/
- orchestration/ (contracts, NOT executable)
- manifests/ (refresh, propagation, rebuild-history, stale reports; append-only)
- lifecycle/ (change-detection, rebuild, propagation, publication)
- governance/ (rebuild, propagation-rules, dependency, refresh-safety)
- future-cli-readiness/
