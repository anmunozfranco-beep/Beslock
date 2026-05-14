# Canonical Reference Stack

Nine declared modules composing the canonical operational stack.

## Modules

- `retrieval-runtime` — kind→domain routing, Jaccard scoring, confidence weighting, candidate-only marker (module: runtime-implementation/runtime/retrieval.py)
- `orchestration-runtime` — supervised flow composition, package assembly, escalation evaluation (module: runtime-implementation/runtime/flows.py + runtime/assembly.py)
- `escalation-runtime` — trigger evaluation, halt semantics, candidate-only routing (module: runtime-implementation/runtime/assembly.py (_evaluate_escalation) + escalation-trace channel)
- `provenance-system` — write-once provenance records; read-only into all sandboxes (module: ext-images/<product>/knowledge-core/**/*.json + manifest_id + source_files[].sha256)
- `replay-system` — deterministic re-execution against frozen orchestration-trace (module: runtime-implementation/runtime/replay.py + cli.py replay subcommand)
- `reviewer-operations` — queue, claim, evidence, decision, audit (module: knowledge-operations/reviewer-workbench/ + review-queues/ (design-only, layer 23))
- `governance-operations` — scope assignment, revocation, dual-audit, emergency intervention (module: knowledge-operations/governance-workflows/ + KNOWLEDGE_BUILDING/* (design-only))
- `oem-ingestion-system` — checksum-verified ingest, dual-review binding, supersession (module: knowledge-operations/oem-operations/ + ingestion env (design-only))
- `observability-system` — append-only event streams: orchestration, retrieval, escalation, continuity, replay, incident (module: runtime-implementation/runtime/channels.py (NDJSON channels))

## Invariants

- every module declares its responsibility, its inputs, and its outputs
- no module owns provenance writes except the governance pipeline
- no module emits effects outside its declared responsibility
- every module is traceable end-to-end via the observability system
- every module is replaceable by a substitute that satisfies the same contract
