"""Provenance manifest emission and content hashing.

Every emitted package carries a provenance manifest. Manifests bind to the
run-id, the slice id, the source node ids, and the SHA-256 content hashes of
the source files.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def build_manifest(
    *,
    run_id: str,
    slice_id: str,
    package_kind: str,
    source_files: Iterable[Path],
    source_node_ids: Iterable[str],
    extra: dict | None = None,
) -> dict:
    sources = []
    for sf in source_files:
        try:
            sources.append({"path": str(sf), "sha256": file_sha256(sf)})
        except FileNotFoundError:
            sources.append({"path": str(sf), "sha256": None, "missing": True})
    manifest = {
        "manifest_id": new_id("prov"),
        "run_id": run_id,
        "slice_id": slice_id,
        "package_kind": package_kind,
        "emitted_at": now_iso(),
        "source_files": sources,
        "source_node_ids": list(source_node_ids),
        "schema": "runtime-provenance/1.0",
    }
    if extra:
        manifest["extra"] = extra
    return manifest


def freeze(payload: dict) -> str:
    """Deterministic JSON for hashing/replay."""
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
