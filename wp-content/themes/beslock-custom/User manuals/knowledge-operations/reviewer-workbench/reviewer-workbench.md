# Reviewer Workbench

Thin operator surface — emits append-only events; never edits canonical JSON.

## Panels

- `side-by-side-oem` — show candidate node next to its bound OEM source artifact
- `ocr-fragment-inspector` — render OCR fragment + bbox + ocr_confidence + source page
- `provenance-inspector` — show full provenance manifest chain + sha256 verification status
- `promotion-approval` — execute declared transition with rationale + supervision-receipt
- `confidence-adjustment` — demote/hold confidence within declared tier ceiling; never raise unilaterally
- `evidence-attachment` — attach a new binding record (sha256-pinned) to a node
- `rollback-operations` — issue a demotion-event referencing a prior promotion-event

## Invariants

- the workbench is a thin operator surface, not an application: it emits events into the governed log
- the workbench cannot edit canonical knowledge-core JSON; it only emits append-only events
- the workbench cannot perform any action without a supervision-receipt
- the workbench cannot promote past a reviewer's declared tier_ceiling
- the workbench surfaces, but does not resolve, disagreement

## Out of scope

- no consumer-facing UI
- no chatbot interaction
- no autonomous suggestion engine
- no embedding/ML-driven match suggestions
