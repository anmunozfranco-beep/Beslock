# Schema Normalization Audit

Audits all governance schema identifiers; canonicalizes families; resolves overlap without renaming.

## Canonical schema families

- `runtime` — rule: all runtime-related governance schemas use the `runtime-*` prefix; members: runtime-governance/1.0, runtime-orchestration-governance/1.0, runtime-implementation-governance/1.0, runtime-hardening-governance/1.0, prototype-runtime-governance/1.0
- `knowledge` — rule: all knowledge-evolution governance schemas use the `knowledge-*` prefix; members: knowledge-lifecycle-governance/1.0, knowledge-operations-governance/1.0
- `operational` — rule: all proof / measurement governance schemas use the `operational-*` prefix; members: operational-proof-governance/1.0
- `intelligence` — rule: cognition-related governance schemas keep their declared identifier; do not rename; members: adaptive-operational-governance/1.0, decision-intelligence-governance/1.0, reasoning-governance/1.0, continuity-governance/1.0
- `ecosystem` — rule: ecosystem-and-deployment governance schemas use the `ecosystem-*` / `environment-*` / `reference-*` prefix; members: ecosystem-interoperability-governance/1.0, environment-integration-governance/1.0, reference-stack-governance/1.0, ecosystem-normalization-governance/1.0
- `human` — rule: human-interaction governance schemas use the `human-*` prefix; members: human-operations-governance/1.0
- `platform` — rule: platform foundation schemas keep their declared identifiers; do not rename; members: composition-governance/1.0, execution-governance/1.0, lifecycle-governance/1.0, realization-and-deployment-governance/1.0, repo-governance/1.0, visual-governance/1.0, visual-constitution/1.0

## Detected schema identifiers (read from tools/)

- `access-and-consumption-governance/1.0` ← access_consumption.py
- `adaptive-operational-governance/1.0` ← adaptive_governance.py
- `composition-governance/1.0` ← composition_governance.py
- `continuity-governance/1.0` ← continuity_governance.py
- `decision-intelligence-governance/1.0` ← decision_governance.py
- `ecosystem-interoperability-governance/1.0` ← ecosystem_governance.py
- `ecosystem-normalization-governance/1.0` ← ecosystem_normalization_governance.py
- `environment-integration-governance/1.0` ← environment_integration_governance.py
- `execution-governance/1.0` ← execution_governance.py
- `experience-governance/1.0` ← experience_modeling.py
- `human-operations-governance/1.0` ← human_operations_governance.py
- `knowledge-center/1.0` ← knowledge_center_consolidate.py
- `knowledge-core/1.0` ← knowledge_core_build.py
- `knowledge-core/1.1-semantic-enrichment` ← knowledge_core_semantic_enrich.py
- `knowledge-lifecycle-governance/1.0` ← knowledge_lifecycle_governance.py
- `knowledge-operations-governance/1.0` ← knowledge_operations_governance.py
- `lifecycle-governance/1.0` ← lifecycle_governance.py
- `operational-proof-governance/1.0` ← proof_governance.py
- `prototype-runtime-governance/1.0` ← prototype_runtime_governance.py
- `realization-and-deployment-governance/1.0` ← realization_governance.py
- `reasoning-governance/1.0` ← reasoning_governance.py
- `reference-stack-governance/1.0` ← reference_stack_governance.py
- `repo-governance/1.0` ← repository_governance_audit.py, root_canonicalize_md_json.py
- `runtime-governance/1.0` ← runtime_governance.py
- `runtime-hardening-governance/1.0` ← runtime_hardening_governance.py
- `runtime-implementation-governance/1.0` ← runtime_implementation_governance.py
- `runtime-orchestration-governance/1.0` ← orchestration_governance.py
- `semantic-governance/1.0` ← knowledge_normalize_audit.py
- `validation-governance/1.0` ← knowledge_validation.py
- `visual-constitution/1.0` ← visual_governance_promote.py
- `visual-governance/1.0` ← visual_governance_consolidate.py

## Overlap findings

- `two-runtime-execution-axes` — runtime-governance/1.0 + execution-governance/1.0 + runtime-orchestration-governance/1.0 each model an execution axis → resolution: treat as layered (governance → orchestration → implementation); no schema merge; document in canonical-references
- `two-deployment-axes` — realization-and-deployment-governance/1.0 + environment-integration-governance/1.0 + reference-stack-governance/1.0 → resolution: realization=value/timing; environment=trust/boundaries; reference-stack=composition; layered, not duplicated
- `two-lifecycle-axes` — lifecycle-governance/1.0 (knowledge-core lifecycle) + knowledge-lifecycle-governance/1.0 (candidate→trusted) → resolution: lifecycle-governance owns content lifecycle; knowledge-lifecycle owns trust lifecycle; both retained, scopes documented
- `visual-dual-schema` — visual-governance/1.0 + visual-constitution/1.0 → resolution: constitution = doctrinal; governance = operational; retained as declared
- `two-ecosystem-axes` — ecosystem-interoperability-governance/1.0 + ecosystem-normalization-governance/1.0 → resolution: interoperability = cross-system contracts; normalization = internal coherence; layered, not duplicated

## Normalization rules

- every governance schema identifier is `<area>-governance/<MAJOR>.<MINOR>` or `<area>-constitution/<MAJOR>.<MINOR>`
- every schema is owned by exactly one builder file (one canonical author)
- schemas are never renamed in place; renames require a new MAJOR version
- schemas never duplicate fields owned by knowledge-core/1.0 (manifest_id, source_files, sha256, confidence, etc.)
- schemas never collapse layered concerns (runtime/orchestration/implementation, lifecycle/trust, etc.)
