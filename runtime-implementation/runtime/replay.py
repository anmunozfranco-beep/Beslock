"""Deterministic replay harness.

Consumes the append-only NDJSON observability channels and replays declared
flow runs by re-executing retrieval against the same `(product, query, kind)`
inputs and comparing emitted `source_node_ids` between captured and replayed
retrieval-packages.

This is a real, deterministic validator — no clock, no network, no ML.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from . import flows, observability, retrieval


@dataclass
class FlowReplay:
    run_id: str
    flow: str
    product: str
    query: str
    captured_retrievals: list[dict] = field(default_factory=list)
    replayed_retrievals: list[dict] = field(default_factory=list)
    drift: list[dict] = field(default_factory=list)

    @property
    def deterministic(self) -> bool:
        return not self.drift


def _index_starts_by_run() -> dict[str, dict]:
    starts: dict[str, dict] = {}
    for ev in observability.read_all("orchestration-trace"):
        if ev.get("kind") != "flow-start":
            continue
        run_id = ev.get("run_id")
        if not run_id:
            continue
        starts[run_id] = ev
    return starts


def _index_retrievals_by_run() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for ev in observability.read_all("retrieval-trace"):
        run_id = ev.get("run_id")
        if not run_id:
            continue
        out.setdefault(run_id, []).append(ev)
    return out


def replay_run(run_id: str) -> FlowReplay | None:
    starts = _index_starts_by_run()
    if run_id not in starts:
        return None
    start = starts[run_id]
    flow = start.get("flow")
    product = start.get("product")
    query = start.get("query")
    if flow not in flows.FLOW_KINDS or not product or query is None:
        return None

    captured = _index_retrievals_by_run().get(run_id, [])

    # Re-execute retrieval for the captured (kind, product, query) tuples.
    replayed: list[dict] = []
    drift: list[dict] = []
    for ev in captured:
        pkg = ev.get("package", {})
        # Skip synthetic empty packages (flows fabricate these when a kind
        # slot is intentionally unused — they aren't real retrieve() calls).
        if (pkg.get("manifest", {}).get("extra") or {}).get("empty"):
            continue
        captured_kind = pkg.get("kind")
        captured_query = pkg.get("query")
        captured_product = pkg.get("product")
        captured_ids = sorted([n.get("id") for n in pkg.get("nodes", []) if n.get("id")])
        if not captured_kind or captured_query is None or not captured_product:
            continue
        try:
            redo = retrieval.retrieve(
                run_id=f"replay-{run_id}", slice_id=f"replay-{run_id}",
                product=captured_product, query=captured_query, kind=captured_kind,
            )
        except (ValueError, PermissionError) as exc:
            drift.append({"event_id": ev.get("event_id"), "kind": captured_kind,
                          "error": str(exc)})
            continue
        redone_ids = sorted([n.id for n in redo.nodes])
        rec = {
            "event_id": ev.get("event_id"),
            "kind": captured_kind,
            "captured_ids": captured_ids,
            "replayed_ids": redone_ids,
        }
        replayed.append(rec)
        if captured_ids != redone_ids:
            drift.append({**rec, "kind_of_drift": "node-id-set-mismatch"})

    return FlowReplay(
        run_id=run_id, flow=flow, product=product, query=query,
        captured_retrievals=[{"event_id": e.get("event_id"),
                              "kind": e.get("package", {}).get("kind"),
                              "node_ids": sorted([n.get("id") for n in e.get("package", {}).get("nodes", [])
                                                  if n.get("id")])}
                             for e in captured],
        replayed_retrievals=replayed,
        drift=drift,
    )


def replay_all() -> list[FlowReplay]:
    out: list[FlowReplay] = []
    for run_id in _index_starts_by_run():
        rp = replay_run(run_id)
        if rp:
            out.append(rp)
    return out


def summary(replays: Iterable[FlowReplay]) -> dict:
    items = list(replays)
    return {
        "schema": "runtime-replay/1.0",
        "runs": len(items),
        "deterministic_runs": sum(1 for r in items if r.deterministic),
        "drifted_runs": sum(1 for r in items if not r.deterministic),
        "drift_events": sum(len(r.drift) for r in items),
    }
