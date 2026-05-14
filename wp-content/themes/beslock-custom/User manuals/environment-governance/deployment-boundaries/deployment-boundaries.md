# Deployment Boundary Governance

Seven declared deployment boundaries; every crossing is a contract and an observable event.

## Boundaries

- `runtime-boundary` — the runtime emits packages; it never writes canonical knowledge-core JSON
- `deployment-isolation` — each environment is a separate deployment unit; no shared mutable state across envs
- `cognition-isolation` — cognition (retrieval/assembly/escalation) runs only inside the runtime boundary; never inside ingestion or reviewer envs
- `reviewer-isolation` — reviewer surfaces never co-locate with the runtime emission path; reviewer writes target staging, not production
- `escalation-isolation` — escalation channels are append-only and live in their own boundary; demotions are events, not direct mutations
- `provenance-isolation` — provenance records (manifests, source SHAs, lineage) are write-once; any environment may read, only governance pipelines may append
- `operational-segmentation` — operational segments (runtime / reviewer / governance / ingestion / audit) are declared; cross-segment calls are forbidden unless declared by an integration contract

## Invariants

- no boundary is ever crossed implicitly; every crossing is a declared contract
- no boundary permits silent escalation of trust
- no boundary permits a higher-trust environment to read from a lower-trust environment without verification
- no boundary permits write paths from a lower-trust environment into a higher-trust environment
- every boundary crossing emits an observability event
