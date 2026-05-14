# KNOWLEDGE CORE PRINCIPLES

Status: Active governance.
Scope: Philosophy of the BESLOCK Product Knowledge Core.
Audience: Copilot, AI agents, developers, automation systems, future RAG pipelines.

---

## 1. Knowledge-first philosophy

BESLOCK does not produce manuals first. It produces **product knowledge** first. Manuals, web pages, support flows, and chatbot answers are downstream surfaces of that knowledge.

Implications:
- The canonical artifact is a product nucleus, not a PDF.
- Editorial deliverables are derived from structured knowledge, not the other way around.
- A change to a procedure, capability, or warning is made in the structured knowledge first; delivery surfaces re-render from it.
- A "manual" with no structured-knowledge backing is a legacy artifact, not a source of truth.

---

## 2. Multimodal platform vision

A product nucleus is multimodal:
- Text knowledge (manuals, glossary, validation).
- Structured semantic knowledge (capabilities, procedures, workflows, knowledge-graph).
- Visual knowledge (canonical PNG, OEM visual evidence, anchor maps).
- Generated visual derivatives (support visuals approved through ComfyUI).
- Operational knowledge (orchestration manifests, run records, QA trackers).
- Provenance and lineage (file, semantic, visual).

All modalities share one identity: the product slug, the canonical PNG, and the OEM evidence set. No modality may redefine the product on its own.

---

## 3. Future chatbot and RAG goals

The platform must be able to answer, from structured knowledge:
- How do I install this product?
- How do I configure access methods?
- What are the operational states?
- What are the warnings and safety notes?
- How do I troubleshoot a specific symptom?
- What capabilities does this product have?
- How does this product compare to another in the catalog?
- What does this product look like, and what are its visible components?
- What is the source of a given claim?

Required RAG-ready properties on every semantic object:
- stable object ID
- object type
- product slug
- summary
- normalized language (Colombian-Spanish canonical)
- validation status
- channel targets
- source references
- related workflow IDs
- related visual constraint IDs (when relevant)

RAG ingestion priority:
1. `structured-knowledge/` objects.
2. `metadata/manifests/product-domain-manifest.json`.
3. Normalized source manuals as fallback evidence.

Chatbot and API outputs must not depend on scraping freeform delivery markdown as their only knowledge input.

---

## 4. Semantic persistence principles

- Knowledge is persisted as structured JSON with stable IDs.
- IDs are stable across reorganizations; renaming a product slug is a deliberate, traced operation.
- Semantic objects are addressable, citable, and diffable.
- Persistence is machine-readable first; human-readable narratives are derived.
- The repository itself is the operational memory of the project. Conversations, chats, and ad-hoc notes are not authoritative.

---

## 5. Reusable knowledge principles

- Each semantic object is reusable across delivery surfaces (web, PDF, support, onboarding, chatbot, RAG, API, future video).
- Editing a semantic object once propagates the change to every surface that reads it.
- Surfaces do not duplicate knowledge; they project it.
- Granularity is chosen so that the smallest reusable unit (a procedure step, a capability, a warning) is independently citable.

Granularity layers:
- document level — provenance and archival recovery
- section level — editorial reuse
- procedure level — support, onboarding, chatbot actions
- capability level — comparison and feature support
- workflow level — app and operational sequences
- warning/troubleshooting step level — support resolution
- visual-constraint level — geometry preservation and image governance

---

## 6. Operational support philosophy

The Product Knowledge Core exists to make operational support correct, fast, and verifiable.

- Support agents (human or AI) read from structured knowledge, not from PDFs.
- Every support answer can cite its source.
- Every product-specific decision (installation, configuration, troubleshooting) is grounded in OEM evidence or the canonical PNG.
- Operational changes are traced; "we changed the wording" is recorded with who, when, and why.
- The system favors deterministic answers over plausible-sounding answers.

---

## 7. Product-truth philosophy

Product truth comes from two sources only:
1. OEM documentation.
2. The single canonical PNG.

Rules:
- Anything else is derivative.
- Generated visuals never become product truth.
- Editorial wording never invents product behavior.
- Inferred claims are explicitly marked, not silently promoted.
- When OEM and canonical PNG disagree, the disagreement is recorded in the validation ledger and resolved deliberately, not silently.
- When OEM evidence is missing, the gap is recorded as `blocked-pending-validation`, not papered over.

---

## 8. Deterministic-system philosophy

The platform behaves deterministically.

- Same inputs, same tools, same workflow → same outputs (subject to engine determinism).
- Visual generation is reproducible via run records.
- Knowledge derivation is reproducible via lineage manifests.
- Delivery rendering is reproducible from structured knowledge.
- Randomness in generation is constrained by recorded seeds and parameters.
- "Magic" is forbidden: every step is described, registered, and traceable.

This determinism is what makes the Product Knowledge Core trustworthy for support, onboarding, and future RAG/chatbot consumption.

---

## 9. Authority

This document is the philosophical foundation that all other governance files in `KNOWLEDGE_BUILDING/` enforce. When in doubt, the principles in this document outrank ad-hoc convenience.
