# Knowledge Governance Charter

_Schema: `semantic-governance/1.0` · semantic-governance constitution · generated 2026-05-13T17:11:48Z._

## Purpose

This charter is the constitutional layer of **knowledge governance**. It
defines who owns semantic content, how the ontology stays stable, how
terminology is canonicalised, how conflicts are resolved, how maturity is
governed, how lineage is preserved, and how retrieval stays consistent.

Knowledge governance is distinct from visual governance
(`KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/`) and from runtime governance
(`visual-system/_governance/`). The three layers cooperate; none subsumes the
others.

## Principles

1. **Semantic ownership lives with the knowledge core.** No surface owns
   semantics. A surface that needs new semantics requests them from the
   knowledge layer.
2. **Ontology is platform-wide and stable.** Shared concept IDs are
   immutable once published. Refinement happens via sub-ids, never by
   renaming.
3. **One canonical name per concept.** Synonyms are tracked and mapped, not
   tolerated as parallel canonicals.
4. **Conflicts are surfaced, never silenced.** Auto-resolution would erase
   editorial judgement; the system reports and waits.
5. **Maturity is a first-class field.** Every artifact carries a maturity
   tier; downstream systems filter by tier.
6. **Lineage is mandatory.** Every artifact carries a provenance pointer;
   no provenance == not eligible for promotion.
7. **Retrieval stability is a contract.** Identifier shapes, index sources,
   and served fields are governed; arbitrary changes break consumers.
8. **Cross-product reuse over duplication.** Reusable concepts are promoted
   to the shared ontology rather than copy-edited per product.
9. **Subordination of all surfaces.** Every consumer (web, PDF, chatbot,
   RAG, AR, video, future Comfy orchestration) is subordinate to the
   knowledge core.

## Authorities

| Concern | Authority | Location |
|---|---|---|
| Ontology + shared concepts        | Knowledge Center | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-ontology/` |
| Canonical terminology             | Semantic Governance (this folder) | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/canonical-terminology/` |
| Procedural normalization          | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/procedural-normalization/` |
| Identifier grammar                | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/semantic-identifiers/` |
| Maturity classification           | Knowledge Center  | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-maturity/` |
| Maturity governance / consistency | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/maturity-governance/` |
| Retrieval indexing strategy       | Knowledge Center  | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/retrieval-readiness/` |
| Retrieval governance              | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/retrieval-governance/` |
| Cross-product coherence           | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/cross-product-governance/` |
| Conflict detection + register     | Semantic Governance | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/semantic-conflicts/` |
| Visual policy                     | Visual Governance | `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/` |
| Runtime enforcement               | Runtime governance | `visual-system/_governance/` |

## Conflict-resolution philosophy

1. Detect.
2. Classify (severity, domain, product scope).
3. Surface (write to the conflict register).
4. Wait for editorial resolution.
5. Promote the resolution into canonical terminology / shared ontology.
6. Re-scan to confirm no regression.

The system never deletes artifacts to silence a conflict. Mergers and
deprecations happen in editorial, then reflect in the registry.

## Amendment policy

Changing this charter requires updating this folder first, then propagating
into the relevant runtime artifacts. Direct edits to per-product nuclei that
contradict the charter are out of policy and must be reverted.
