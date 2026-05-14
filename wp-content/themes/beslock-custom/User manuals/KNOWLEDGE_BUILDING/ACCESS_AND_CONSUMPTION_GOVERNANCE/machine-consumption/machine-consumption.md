# Stable Surfaces

| id | guarantee |
|---|---|
| artifact-id-surface | ids are stable across versions; supersession recorded via lineage |
| schema-surface | schemas are semver-versioned per LIFECYCLE_GOVERNANCE |
| provenance-surface | every artifact carries source_refs + extraction_lineage |
| context-bundle-surface | deterministic given (profile, inputs, knowledge-core snapshot) |
| retrieval-chunk-surface | stable chunk ids; chunk content reproducible from canonical artifact |
| channel-target-surface | channel_targets array declares opt-in surfaces (chatbot/rag/web/pdf/...) |


## Determinism rules

- Same inputs + same knowledge-core snapshot => byte-identical context bundle.
- Bundle generation records knowledge-core snapshot hash (future: integrate with lifecycle versioning).
- Non-deterministic enrichments (e.g. ML embeddings) live OUTSIDE the access layer.
- Lineage-safe: a bundle re-issued after artifact supersession explicitly references the new version + records the previous bundle hash.

## Consumption gates

| consumer | requires |
|---|---|
| RAG | maturity ≥ canonical, lineage-break tolerance = 0, channel_targets includes 'rag' |
| semantic-API | stable artifact-ids, schema-surface pinned, access-trace logging |
| vector-retrieval | retrieval-chunk-surface, deterministic chunk boundaries, provenance per chunk |
| contextual-assistant | context-bundle-surface, audience-scope mandatory, warning-injection enforced |
| multimodal-system | visual-bundle available, visual-risk classified, component-visibility declared |
| adaptive-onboarding | onboarding-bundle by audience, cognitive-load-map present, interruption budget honoured |
