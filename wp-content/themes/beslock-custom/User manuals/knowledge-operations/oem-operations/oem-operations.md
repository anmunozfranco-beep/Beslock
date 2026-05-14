# OEM Ingestion Operations

Seven-stage governed flow for OEM artifact intake, OCR staging, reconciliation, and supersession.

## Stages

- `intake` — receive OEM artifact (PDF/screenshot); compute sha256; reject duplicates
- `ocr-staging` — run declared OCR pipeline version; emit ocr-fragment records (candidate state)
- `ingestion-validation` — schema + scope check; reject malformed payloads
- `duplicate-detection` — match sha256 + content fingerprint against existing source store
- `source-reconciliation` — if a near-duplicate exists, open a reconciliation review (do not auto-merge)
- `source-aging` — track source age vs supersession-window; flag stale sources for re-review
- `oem-replacement` — supersession of an OEM source: emit supersession event; fan out demotion to bound nodes

## Invariants

- no auto-binding from a new OEM source to existing nodes; binding requires reviewer action
- no merge of two OEM sources without a documented reconciliation review
- no OEM source is ever overwritten; new uploads create new source records
- every stage produces an append-only event
- ingestion respects the read-only posture over canonical knowledge-core

## OEM replacement flow

- 1. new OEM source ingested + sha256 pinned
- 2. supersession event proposed (old_sha256, new_sha256, rationale, reviewer)
- 3. dual-review of supersession
- 4. on approval: bound nodes demote to candidate-pending-rebinding
- 5. each demoted node enters candidate-review queue
