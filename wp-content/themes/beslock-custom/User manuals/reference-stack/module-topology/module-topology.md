# Operational Module Topology

Declared module relationships, isolation boundaries, and topology invariants.

## Relationships

- `orchestration-runtime` → `retrieval-runtime` (synchronous-call) — retrieve(product, query, kind) → package
- `orchestration-runtime` → `escalation-runtime` (evaluation-call) — _evaluate_escalation(packages) → triggers[]
- `orchestration-runtime` → `observability-system` (append-only-emit) — orchestration-trace, retrieval-trace, escalation-trace events
- `retrieval-runtime` → `provenance-system` (read-only-load) — load knowledge-core JSON; never write
- `replay-system` → `observability-system` (read-only-tail) — consume orchestration-trace; emit replay-trace
- `replay-system` → `retrieval-runtime` (deterministic-re-call) — re-execute retrieve() with captured (product, query, kind)
- `reviewer-operations` → `observability-system` (read-only-tail + emit) — consume runtime events; emit review-decision events
- `reviewer-operations` → `provenance-system` (read-only-load) — render provenance for evidence-pull; no writes
- `governance-operations` → `reviewer-operations` (scope-assignment) — assign / revoke reviewer scope; dual-audited
- `governance-operations` → `provenance-system` (pipeline-write) — only governance pipeline appends to provenance
- `oem-ingestion-system` → `provenance-system` (staged-write) — checksum-verified ingest into staging; never directly to production
- `oem-ingestion-system` → `reviewer-operations` (dual-review-handoff) — binding handoff for OEM-reviewer dual-review
- `escalation-runtime` → `observability-system` (append-only-emit) — escalation-trace events; never silent

## Isolation boundaries

- retrieval ↔ provenance: retrieval reads provenance; never writes
- orchestration ↔ canonical knowledge-core: orchestration emits packages; never writes canonical JSON
- reviewer ↔ production write paths: reviewer surfaces stage decisions; never directly mutate production
- ingestion ↔ production: OEM ingestion writes only to staging; supersession requires governance pipeline
- replay ↔ live runtime: replay outputs go to a side channel; never to production emission paths
- observability ↔ all modules: observability is read-only consumer; no back-channel mutation

## Invariants

- every module relationship is declared; undeclared calls are forbidden
- every cross-module call satisfies a declared contract
- every cross-module call emits an observability event
- no cross-module call escalates trust silently
- no cross-module call bypasses an isolation boundary
