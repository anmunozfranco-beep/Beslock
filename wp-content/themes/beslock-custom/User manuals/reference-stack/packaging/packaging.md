# Operational Packaging & Assembly

Six declared manifest standards; manifests are append-only and reproducible.

## Standards

- `runtime-package-manifest` — fields: package_id, manifest_id, source_files[], extra{candidate_only?, empty?}, supervision_receipt
- `module-assembly-manifest` — fields: composition_id, module_ids[], environment_id, trust_zone_id, supervision_level
- `deployment-manifest` — fields: deployment_id, composition_id, environment_id, started_at, started_by, scope
- `environment-manifest` — fields: environment_id, trust_level, supervision_level, isolation, lifecycle_state
- `governance-manifest` — fields: governance_event_id, actor, decision, rationale, dual_audit?, audit_co_signature?
- `operational-composition-manifest` — fields: composition_id, module_topology_hash, interop_contract_versions{}, trust_zone_map{}

## Invariants

- every manifest is append-only; manifests are never edited in place
- every manifest carries an id and a generated_at timestamp
- every manifest references the parent manifest it composes (if any)
- no manifest may omit provenance, candidate-only, or supervision fields when applicable
- manifests are the basis for replay; reproducibility depends on manifest fidelity
