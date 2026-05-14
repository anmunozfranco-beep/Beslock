# Knowledge Composition

## Primitives

- entity
- procedure
- workflow
- warning
- terminology
- capability
- specification
- troubleshooting-symptom
- procedural-semantics
- visual-intent
- visual-risk
- publication-intent
- component-visibility
- provenance
- guidance-trigger
- cognitive-load-assessment
- priority-assignment

## Operational packages

| id | purpose | primitives |
|---|---|---|
| installation-package | physical install end-to-end | procedure(install/*), warning, specification, visual-intent(physical-installation), component-visibility, provenance |
| onboarding-package | audience-scoped first-use flow | workflow, procedural-semantics, warning, guidance-trigger, cognitive-load-assessment, terminology, provenance |
| troubleshooting-package | symptom -> recovery path | troubleshooting-symptom, warning, procedure, escalation-tier, safety-constraint, provenance |
| administrator-setup-package | admin enrolment + policy setup | workflow(administrator-setup), procedure(user-enrolment), capability, warning, provenance |
| maintenance-package | battery + routine maintenance | procedure(battery-replacement), warning, specification, visual-intent, provenance |
| recovery-package | factory-reset / emergency-power | procedure(factory-reset), procedure(emergency-power), warning, guidance-trigger(hard-interrupt), provenance |

## Rules

- Every package declares: id, purpose, primitives, source_artifact_ids, maturity_floor, audience_scope, channel_targets.
- Packages are reproducible from per-product knowledge-core; no orphan content allowed.
- Packages compose primitives by reference (id), never by inlined copy of mutable content.
- Provenance from every primitive flows into the package; provenance-stripped packages are forbidden.
- Packages MUST honour all access-governance filters (maturity, deprecation, unresolved-isolation).
