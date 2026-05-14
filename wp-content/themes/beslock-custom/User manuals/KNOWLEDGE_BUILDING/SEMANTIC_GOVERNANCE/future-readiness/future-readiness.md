# Future readiness (semantic governance)

_Schema: `semantic-governance/1.0` · future readiness · generated 2026-05-13T17:11:48Z._

## Subordination

Every future surface — multilingual support, chatbot retrieval,
troubleshooting assistants, onboarding systems, semantic publication, visual
assistance, contextual rendering, RAG — is **subordinate to the knowledge
core** and bound by this charter.

## Multilingual support

- Baseline locale: `es-CO`.
- Localized variants append a BCP-47 tag to artifact IDs (e.g.
  `term-fingerprint.en-US`).
- Canonical terminology is locale-independent; localized labels live as
  variants of the canonical term.

## Chatbot / RAG

- Serve `verified` and `canonical` only by default.
- Surface provenance (OEM evidence id + span).
- Use synonym expansion via the canonical-terminology registry.
- Apply consumer-side maturity gates.

## Troubleshooting assistant

- Traverse procedure / warning / troubleshooting graph.
- Respect maturity gates; allow `inferred` with explicit confidence label.

## Onboarding

- Traverse workflow graph (pairing, enrolment, first-use).
- Serve only `canonical` / `verified`.

## Visual assistance / contextual rendering

- Bound by the visual constitution
  (`KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/`) and the runtime governance
  (`visual-system/_governance/`).
- Conditioned on the canonical PNG; never originates knowledge.

## Out of scope

- Generated images, Comfy execution, prompt generation, manual rendering,
  publication system construction. These belong to later phases and are
  bound by the visual + knowledge constitutions.
