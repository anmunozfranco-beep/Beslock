# External Integration Contracts

Seven declared integration contracts; undeclared integrations are forbidden.

## Contracts

- `wordpress` — trust: render-only consumer of knowledge-core JSON; no write path back
- `retrieval-apis` — trust: read-only against runtime channels
- `oem-ingestion-systems` — trust: semi-trusted; mirrors OEM sources via checksum-verified ingest
- `observability-systems` — trust: read-only consumer of NDJSON channels
- `operational-consoles` — trust: operator-surfaces (layer 24); design-only here
- `future-copilots` — trust: supervised assistive surface; never autonomous
- `future-multimodal-runtimes` — trust: subordinate to runtime governance; new modalities are channels, not new architecture

## Invariants

- every integration is governed by a declared trust contract; undeclared integrations are forbidden
- no integration may write to canonical knowledge-core JSON
- no integration may bypass supervision-receipt emission
- no integration may suppress provenance or candidate-only markers for UX reasons
- every integration is reversible; revocation is a first-class governance action
