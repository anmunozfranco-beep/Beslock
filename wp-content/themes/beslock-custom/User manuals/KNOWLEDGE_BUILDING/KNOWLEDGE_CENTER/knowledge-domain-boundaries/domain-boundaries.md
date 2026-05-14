# Knowledge domain boundaries

_Schema: `knowledge-center/1.0` · domain-boundary specification · generated 2026-05-13T16:54:29Z._

## Purpose

Formalise the distinction between source-of-truth, evidence, semantic
interpretation, canonical knowledge, governance, orchestration, visual
semantics and publication semantics. The boundaries below are the platform
contract; they prevent knowledge drift and semantic overlap.

## Boundaries

| Domain | Owner | Scope | Boundary |
|---|---|---|---|
| `source-of-truth` | ext-images/<slug>/source-of-truth/ | OEM PDFs, OEM manuals, OEM product PNGs. | Editorial content. Read-only outside ingest. |
| `evidence` | ext-images/<slug>/source-of-truth/manuals/, generated_manuals/<slug>/ | OCR text, page renders, raw extracted text. | Append-only. Never edited in place. |
| `semantic-interpretation` | ext-images/<slug>/knowledge-core/{entities,procedures,workflows,warnings,terminology,capabilities,specifications,troubleshooting}/ | Structured semantic interpretation of evidence. | Carries provenance pointers back to evidence. |
| `canonical-knowledge` | ext-images/<slug>/knowledge-core/ | Promoted, reviewed, indexed semantic artifacts. | Only canonical artifacts may be served downstream. |
| `visual-semantics` | ext-images/<slug>/knowledge-core/{visual-intent,visual-risk,component-visibility,publication-intent,procedural-semantics}/ | Semantic descriptors that condition future visual generation. | Authored from canonical knowledge; never invented at the visual layer. |
| `publication-semantics` | ext-images/<slug>/knowledge-core/publication-intent/ | Channel targets, formats, alt-text contracts. | Publication-specific concerns live here, not in entities. |
| `governance` | visual-system/_governance/ + KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/ | Policy and doctrine. | Governance never stores product knowledge. |
| `orchestration` | tools/visual_generation.py + tools/comfy/ + ext-images/<slug>/automation/ | Execution: workflows, runs, manifests. | Reads canonical and visual semantics; writes only run records. |

## Cross-boundary rules

1. A semantic interpretation MAY reference its evidence; it MUST NOT modify it.
2. Canonical knowledge MAY reference semantic interpretations; new fields enter
   only by promotion, not by editing in place.
3. Visual semantics MAY consume canonical knowledge; they MUST NOT invent new
   product attributes.
4. Publication semantics MAY constrain how canonical knowledge is delivered;
   they MUST NOT redefine it.
5. Governance MUST NOT contain product knowledge.
6. Orchestration MUST NOT alter governance, semantics, or canonical knowledge;
   it writes only run records.

## Anti-patterns (out of policy)

- A new entity that exists only inside a visual-intent file.
- A warning whose only source is a prompt.
- A procedure whose only evidence is a generated image.
- A canonical entry edited directly without a maturity-tier promotion.
- A governance document containing per-product specifications.
