# Knowledge relationship graph

_Schema: `knowledge-center/1.0` · canonical relationship-graph specification · generated 2026-05-13T16:54:29Z._

## Purpose

Express explicit, machine-readable relationships between products, entities,
procedures, components, operational flows, warnings, visual-support
requirements and troubleshooting dependencies. The intent is a product
intelligence graph that downstream systems (chatbot, RAG, troubleshooting
assistant, onboarding) can traverse.

## Node types

- `product` — a single Beslock product (e-flex, e-nova, e-orbit, e-prime, e-shield, e-touch).
- `entity` — a hardware component or named conceptual object.
- `procedure` — a user-facing task expressed as ordered steps.
- `workflow` — a longer multi-procedure flow (installation, onboarding, recovery).
- `warning` — a hazard, caution or operational caveat.
- `capability` — an externally visible feature.
- `specification` — a measurable property.
- `terminology-entry` — a canonical term.
- `visual-intent` — a delivery-surface visual descriptor.
- `procedural-semantics` — semantic annotation of one procedure step.
- `publication-target` — `{channel, format}` pair.
- `oem-evidence` — a span of an OEM document.

## Edge types

- `product.has-entity` (product → entity)
- `product.has-capability` (product → capability)
- `product.has-procedure` (product → procedure)
- `procedure.composes` (workflow → procedure)
- `procedure.touches-entity` (procedure → entity)
- `procedure.requires-capability` (procedure → capability)
- `procedure.warns` (procedure → warning)
- `procedure.illustrated-by` (procedure → visual-intent)
- `procedure.troubleshoots` (procedure → procedure)
- `entity.contains-entity` (entity → entity)
- `visual-intent.depicts-entity` (visual-intent → entity)
- `visual-intent.targets` (visual-intent → publication-target)
- `artifact.derived-from` (any node → oem-evidence)

## Storage layout

Relationship records live next to the artifacts they describe:

- per-product edges: `ext-images/<slug>/knowledge-core/semantic/relationships/`
- cross-product edges: `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/cross-product-edges.json`
- shared-concept membership: `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-graph/shared-concept-membership.json`

## Traversal contracts

1. **Identification query**: given a product, return its capabilities,
   procedures, warnings and the visual intents that depict it.
2. **Procedure query**: given a procedure, return the workflow it composes,
   the entities it touches, the warnings it triggers, the visual intents that
   illustrate it and the OEM evidence that justifies it.
3. **Troubleshooting query**: given a symptom, return the candidate
   procedures, the entities they touch, and the publication targets that
   explain them.
4. **Cross-product query**: given a shared concept, return every product that
   instantiates it and every per-product specialisation.

## Acceptance criteria

- Every edge carries a maturity tier.
- Every edge carries a provenance pointer back to OEM evidence (or to the
  semantic interpretation that derived it).
- No edge crosses domain boundaries silently — visual semantics may reference
  canonical knowledge, but canonical knowledge may not depend on visual
  semantics.
