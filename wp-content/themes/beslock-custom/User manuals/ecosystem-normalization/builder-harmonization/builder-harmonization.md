# Builder Harmonization Audit

Audits every builder under tools/; declares conventions; flags non-conforming files.

## Builder conventions

- filename = `tools/<area>_governance.py` (snake_case area; suffix `_governance`)
- exposes a single top-level `build()` function and `if __name__ == '__main__': build()`
- declares `SCHEMA = '<area>-governance/<version>'` exactly once
- declares `SUBORDINATE_TO = [...]` listing knowledge-core + every prior layer
- uses the `write_pair(folder, slug, title, intro, sections, payload)` helper with paired `.md` + `.json`
- writes only under THREE roots: artifact folder + KNOWLEDGE_BUILDING/<LAYER>/ + reports/<slug>/
- is idempotent and non-destructive (re-running yields the same files)
- reads no per-product knowledge-core JSON
- prints a final summary line including the three written roots

## Builders inventoried

- `access_consumption.py` — schemas: access-and-consumption-governance/1.0; write_pair: False; subordinate_to: False; idempotent: True
- `adaptive_governance.py` — schemas: adaptive-operational-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `composition_governance.py` — schemas: composition-governance/1.0; write_pair: False; subordinate_to: False; idempotent: True
- `continuity_governance.py` — schemas: continuity-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `corpus_enrichment.py` — schemas: <none>; write_pair: False; subordinate_to: False; idempotent: True
- `decision_governance.py` — schemas: decision-intelligence-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `ecosystem_governance.py` — schemas: ecosystem-interoperability-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `ecosystem_normalization_governance.py` — schemas: ecosystem-normalization-governance/1.0; write_pair: True; subordinate_to: True; idempotent: True
- `environment_integration_governance.py` — schemas: environment-integration-governance/1.0; write_pair: True; subordinate_to: True; idempotent: True
- `execution_governance.py` — schemas: execution-governance/1.0; write_pair: False; subordinate_to: False; idempotent: True
- `experience_modeling.py` — schemas: experience-governance/1.0; write_pair: False; subordinate_to: False; idempotent: False
- `generate_reset_review_assets.py` — schemas: <none>; write_pair: False; subordinate_to: False; idempotent: False
- `human_operations_governance.py` — schemas: human-operations-governance/1.0; write_pair: True; subordinate_to: True; idempotent: True
- `knowledge_center_consolidate.py` — schemas: knowledge-center/1.0; write_pair: False; subordinate_to: False; idempotent: False
- `knowledge_core_build.py` — schemas: knowledge-core/1.0; write_pair: False; subordinate_to: False; idempotent: True
- `knowledge_core_semantic_enrich.py` — schemas: knowledge-core/1.1-semantic-enrichment; write_pair: False; subordinate_to: False; idempotent: False
- `knowledge_extraction.py` — schemas: <none>; write_pair: False; subordinate_to: False; idempotent: False
- `knowledge_lifecycle_governance.py` — schemas: knowledge-lifecycle-governance/1.0; write_pair: True; subordinate_to: True; idempotent: True
- `knowledge_normalize_audit.py` — schemas: semantic-governance/1.0; write_pair: False; subordinate_to: False; idempotent: False
- `knowledge_operations_governance.py` — schemas: knowledge-operations-governance/1.0; write_pair: True; subordinate_to: True; idempotent: True
- `knowledge_validation.py` — schemas: validation-governance/1.0; write_pair: False; subordinate_to: False; idempotent: True
- `lifecycle_governance.py` — schemas: lifecycle-governance/1.0; write_pair: False; subordinate_to: False; idempotent: True
- `orchestration_governance.py` — schemas: runtime-orchestration-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `phase1_cutover.py` — schemas: <none>; write_pair: False; subordinate_to: False; idempotent: True
- `phase2b_source_audit.py` — schemas: <none>; write_pair: False; subordinate_to: False; idempotent: False
- `proof_governance.py` — schemas: operational-proof-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `prototype_runtime_governance.py` — schemas: prototype-runtime-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `publish_review_drafts.py` — schemas: <none>; write_pair: False; subordinate_to: False; idempotent: False
- `realization_governance.py` — schemas: realization-and-deployment-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `reasoning_governance.py` — schemas: reasoning-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `reference_stack_governance.py` — schemas: reference-stack-governance/1.0; write_pair: True; subordinate_to: True; idempotent: True
- `render_manual_review_drafts.py` — schemas: <none>; write_pair: False; subordinate_to: False; idempotent: False
- `repository_governance_audit.py` — schemas: repo-governance/1.0; write_pair: False; subordinate_to: False; idempotent: False
- `root_canonicalize_md_json.py` — schemas: repo-governance/1.0; write_pair: False; subordinate_to: False; idempotent: False
- `runtime_governance.py` — schemas: runtime-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `runtime_hardening_governance.py` — schemas: runtime-hardening-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `runtime_implementation_governance.py` — schemas: runtime-implementation-governance/1.0; write_pair: True; subordinate_to: False; idempotent: True
- `visual_governance_consolidate.py` — schemas: visual-governance/1.0; write_pair: False; subordinate_to: False; idempotent: False
- `visual_governance_promote.py` — schemas: visual-constitution/1.0; write_pair: False; subordinate_to: False; idempotent: False

## Harmonization rules (forward)

- future builders MUST satisfy every builder convention listed above
- future builders MUST NOT introduce a second helper that diverges from `write_pair`
- future builders MUST NOT write outside the three declared roots
- future builders MUST NOT rename existing schemas; new MAJOR versions only
- future builders MUST NOT introduce new macro-governance mega-layers
