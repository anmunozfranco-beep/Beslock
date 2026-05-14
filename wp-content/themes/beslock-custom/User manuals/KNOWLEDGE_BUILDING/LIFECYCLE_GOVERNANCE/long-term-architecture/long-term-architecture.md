# Long-Term Architecture Governance

## Principles

1. The knowledge-core is the single source of truth; all other layers are subordinate.
2. Constitutional layers are additive; new layers must declare their subordination to knowledge-core.
3. New products integrate by inheriting ontology + governance + lifecycle, never by forking them.
4. Multimodal systems (visual, retrieval, onboarding, troubleshooting) consume knowledge; they never originate it.
5. Governance expansion is revision-numbered; revisions never silently rewrite past doctrine.
6. Ontology coherence is maintained by: shared vocabulary, shared id format, shared promotion gates.
7. Every new system declares its read/write surface against the knowledge-core lifecycle states it depends on.
8. Lineage preservation is non-negotiable across product additions, ontology revisions, and layer expansions.

## New product integration

1. Allocate product-id and per-product knowledge-core/ folder.
2. Run discovery → extraction → ocr-derived (where applicable) → inferred pipeline.
3. Apply ontology + terminology vocabulary; produce normalized artifacts.
4. Run canonicalization with cross-product collision detection.
5. Open review checkpoints; promote in priority order (P0 → P5).
6. Register product in priority-assignments, onboarding-flows, troubleshooting tiers.
7. Emit change-impact-report scoped to additive change.

## Layer subordination

| layer | subordinate to | may originate | note |
|---|---|---|---|
| VISUAL_GOVERNANCE | knowledge-core | False |  |
| KNOWLEDGE_CENTER | knowledge-core | False | indexes, never authors |
| SEMANTIC_GOVERNANCE | knowledge-core | False |  |
| EXPERIENCE_GOVERNANCE | knowledge-core | False |  |
| LIFECYCLE_GOVERNANCE | knowledge-core | False | governs evolution, not content |
