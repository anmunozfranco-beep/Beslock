# Future extensibility (knowledge center)

_Schema: `knowledge-center/1.0` · future extensibility · generated 2026-05-13T16:54:29Z._

## Subordination rule

Every future system listed below is **subordinate to the knowledge core**.
None of them originates knowledge.

## Anticipated surfaces

- **PDFs**: rendered from canonical knowledge + publication-intent for the
  `pdf` channel.
- **Websites**: rendered from canonical knowledge + publication-intent for
  the `web` channel.
- **Chatbot systems**: query the indexes; serve canonical/verified content;
  surface provenance and maturity.
- **Troubleshooting assistants**: traverse the procedure / warning /
  troubleshooting graph; respect maturity gates.
- **Onboarding systems**: traverse the workflow graph; serve only canonical
  content.
- **Semantic search**: implements retrieval over the indexes defined in
  retrieval-readiness.
- **Contextual publication**: per-channel rendering using publication-intent
  contracts.
- **Visual assistance**: governed by `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/`;
  consumes visual semantics; conditioned on canonical PNG.
- **Future Comfy orchestration**: consumes the visual semantics; emits run
  records only; never edits knowledge.
- **AR overlays**: consume `component-visibility` anchors; respect mechanical
  consistency.
- **Voice assistance**: consumes terminology + procedural-semantics; renders
  canonical Colombian-Spanish phrasing.
- **Video guidance**: consumes workflow + procedural-semantics; bound by the
  visual constitution.

## Out of scope today

- Customer-uploaded photographs as evidence (different trust model).
- Live telemetry from installed locks (different schema, different lifecycle).
- Crowd-sourced procedure variants (no provenance authority).

## Extension protocol

Adding a future surface requires:

1. Declaring its publication channel in the channel registry.
2. Declaring its maturity threshold.
3. Declaring its retrieval contract (which indexes it consumes).
4. Declaring its provenance presentation (how it surfaces evidence).

A surface that cannot satisfy these four declarations does not ship.
