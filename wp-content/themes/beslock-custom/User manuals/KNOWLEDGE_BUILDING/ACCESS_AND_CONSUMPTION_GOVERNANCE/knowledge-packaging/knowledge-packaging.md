# Package Types

| id | purpose | shape |
|---|---|---|
| operational-bundle | single procedure with all dependencies | {procedure, prerequisites, warnings, entities, visuals?} |
| workflow-bundle | single workflow ready for sequencing | {workflow, actors, steps, dependencies, channel_targets} |
| troubleshooting-bundle | symptom -> resolution path | {symptom, tier, steps, escalation} |
| onboarding-bundle | ordered audience-scoped flow | {audience, ordered_artifacts, guidance_triggers} |
| publication-bundle | publication-neutral artifact set | {publication_intent, ordered_artifacts, deprecation_badges, lineage} |
| retrieval-bundle | RAG-safe semantic chunk | {chunk_text, ids, provenance, channel_targets} |
| visual-bundle | visual descriptors for future assistance | {visual_intent, visual_risk, component_visibility} |


## Rules

- Packages are publication-neutral: they describe content, never rendering.
- Every package declares: package_type, schema, generated_at, source_artifact_ids, maturity_floor.
- Packages MUST be reproducible from the per-product knowledge-core; no orphan content.
- Packages MUST NOT inline rendering instructions, fonts, layouts, or media binaries.
- Retrieval bundles MUST carry stable retrieval-safe ids and provenance for every chunk.
