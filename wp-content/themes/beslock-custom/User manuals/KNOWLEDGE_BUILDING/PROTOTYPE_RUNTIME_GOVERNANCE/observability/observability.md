# Prototype Observability

Six declared append-only channels enabling deterministic replay and operational audit.

## Channels

- `reasoning-trace` → chain-record (append-only ndjson)
- `retrieval-trace` → retrieval-package (append-only ndjson)
- `escalation-trace` → escalation-package (append-only ndjson)
- `continuity-trace` → checkpoint-record (append-only ndjson)
- `orchestration-trace` → run-id + slice-id (append-only ndjson)
- `operational-audit-log` → supervision-receipt (append-only ndjson)

## Rules

- All channels are append-only; mutation is unsafe.
- Every emission carries a provenance reference.
- Every channel binds to run-id + slice-id; cross-run aggregation is out of prototype scope.
- Replay must be deterministic from the captured channels alone.
- No channel may carry destructive operation logs (none are produced).
