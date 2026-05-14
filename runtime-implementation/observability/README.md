# Observability

Six append-only NDJSON channels under [logs/](logs/).

Implementation: [runtime/observability.py](../runtime/observability.py).

## Channels

- `reasoning-trace.ndjson`        → assembly + safety reports
- `retrieval-trace.ndjson`        → every retrieval-package
- `escalation-trace.ndjson`       → escalation evaluations
- `continuity-trace.ndjson`       → continuity snapshots
- `orchestration-trace.ndjson`    → flow-start / flow-end
- `operational-audit-log.ndjson`  → supervision receipts + emitted guidance

## Inspect

```bash
.venv/bin/python runtime-implementation/cli.py channels
```
