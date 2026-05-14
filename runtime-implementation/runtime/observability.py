"""Append-only NDJSON observability channels.

One file per channel under `runtime-implementation/observability/logs/`.
All writes are append-only; mutation of past entries is unsafe and unsupported.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import config, provenance

CHANNELS = (
    "reasoning-trace",
    "retrieval-trace",
    "escalation-trace",
    "continuity-trace",
    "orchestration-trace",
    "operational-audit-log",
)


def _channel_path(channel: str) -> Path:
    if channel not in CHANNELS:
        raise ValueError(f"unknown channel: {channel}")
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    return config.LOG_DIR / f"{channel}.ndjson"


def emit(channel: str, payload: dict) -> dict:
    record = {
        "event_id": provenance.new_id("evt"),
        "channel": channel,
        "timestamp": provenance.now_iso(),
        **payload,
    }
    line = json.dumps(record, ensure_ascii=False, sort_keys=True)
    with _channel_path(channel).open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return record


def read_all(channel: str) -> list[dict]:
    path = _channel_path(channel)
    if not path.exists():
        return []
    out: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out
