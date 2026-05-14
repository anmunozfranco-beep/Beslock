# Knowledge Access Patterns

| id | applies_to | shape | guarantees |
|---|---|---|---|
| by-id | all | (product, artifact_id) -> artifact | deterministic, lineage-attached |
| by-domain | all | (product, domain) -> [artifact] | domain-bounded, ordered-by-priority |
| by-entity | entities | (product, entity_id) -> {entity, references_in} | entity-graph-attached |
| by-procedure | procedures, install, operation | (product, procedure_id) -> {procedure, prerequisites, warnings} | prerequisite-expanded, warning-injected |
| by-workflow | workflows | (product, workflow_id) -> {workflow, actors, steps, dependencies} | actor-resolved, dependency-expanded |
| by-warning | warnings | (product, warning_id) -> {warning, scoped_procedures} | scope-resolved |
| by-troubleshooting | troubleshooting | (product, symptom) -> {tier, recovery_path, escalation} | tier-aware, escalation-attached |
| by-onboarding | workflows, procedural-semantics | (product, audience) -> ordered onboarding bundle | audience-scoped, cognitive-load-aware |
| by-visual-intent | visual-intent, visual-risk, component-visibility | (product, surface) -> visual descriptor | risk-classified, visibility-aware |
| by-governance | governance-doctrine | (layer, area) -> doctrine document | revision-tagged |
| by-provenance | all | artifact -> {source_refs, extraction_lineage, version} | read-only, complete-lineage |


## Rules

- All access is read-only at this layer; no mutation surface is exposed.
- Every access response carries provenance; provenance-stripped responses are forbidden.
- Access by id is the canonical primitive; all other patterns reduce to it.
- Access is scoped by (product, layer, audience) — global queries fan out, never collapse.
- Access never returns deprecated artifacts without an explicit `include_deprecated=true` flag.
- Access never returns unresolved-stage artifacts without an explicit `include_unresolved=true` flag.
