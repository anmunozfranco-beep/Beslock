# Beslock Knowledge Center — architecture

_Schema: `knowledge-center/1.0` · canonical architecture document · generated 2026-05-13T16:54:29Z._

## What this repository is

Beslock is **a multimodal product knowledge center**.

It is not a manual generator. It is not an image-generation pipeline. It is not
a prompt repository. It is not a marketing site. It is a structured, queryable,
provenance-bound description of a real family of products, expressed as
machine-readable semantic artifacts that any future surface (web, PDF, support,
onboarding, chatbot, RAG, API, AR, voice, video) can consume.

Visual generation is a future emergent capability of this knowledge center, not
its purpose. The visual constitution at `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/`
governs how that emergent capability is allowed to draw on the knowledge core.

## Knowledge-first principles

1. **Knowledge before delivery.** Every surface (web page, PDF, chatbot
   answer, generated image) descends from canonical knowledge. No surface
   originates knowledge.
2. **Provenance everywhere.** Every semantic artifact carries pointers back
   to the OEM evidence that justifies it.
3. **Schema before content.** New knowledge enters via a typed schema, not a
   freeform document.
4. **Federation over duplication.** Per-product knowledge stays in the
   product nucleus; cross-product intelligence references it, never copies it.
5. **Maturity is explicit.** Every artifact is classified (verified,
   canonical, ocr-derived, inferred, low-confidence, deprecated, unresolved,
   transitional). Downstream consumers may filter by tier.
6. **Boundaries are enforced.** Source-of-truth, evidence, semantic
   interpretation, canonical knowledge, visual semantics, publication
   semantics, governance and orchestration are separate domains with
   separate owners.
7. **Retrieval is a first-class output.** The knowledge core is designed to
   be queried — by humans, by chatbots, by RAG, by future agents.

## Semantic layering

| Layer | Location pattern | Role |
|---|---|---|
| L0 — OEM evidence | `ext-images/<slug>/source-of-truth/`, `generated_manuals/<slug>/` | Editorial / append-only OEM artifacts. |
| L1 — Semantic interpretation | `ext-images/<slug>/knowledge-core/{entities,procedures,workflows,warnings,terminology,capabilities,specifications,troubleshooting}/` | Typed extraction of L0. |
| L2 — Canonical knowledge | promoted artifacts within L1 with `maturity ∈ {verified, canonical}` | Single source consumed by downstream surfaces. |
| L3 — Visual / publication semantics | `ext-images/<slug>/knowledge-core/{visual-intent,visual-risk,component-visibility,publication-intent,procedural-semantics}/` | Conditioning for delivery surfaces. |
| L4 — Cross-product intelligence | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/cross-product-semantic-map/` | Shared concepts and platform-wide references. |
| L5 — Constitutional layer | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/` (this folder) and `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/` | Doctrine, ontology, boundaries, lineage rules. |

## Subordination rule

All present and future systems — websites, PDFs, chatbots, troubleshooting
assistants, onboarding flows, semantic search, contextual publication, visual
assistance, future Comfy orchestration — are **subordinate to the knowledge
core**. They consume it; they may not redefine it.

A surface that wants knowledge it cannot find may request it. It may not
invent it.
