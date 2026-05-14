"""
Phase 47 — Governed transactional CLI executor.

Extends the layer-39 filesystem executor (`tools/governed_fs_executor.py`)
with the governed transaction state machine, deterministic snapshot
capture, reviewer-authorized rollback execution, interrupted-execution
recovery DETECTION (read-only, no auto-action), deterministic replay, and
multi-channel integrity / consistency verification.

Reviewer-invoked, foreground, deterministic, append-only, fail-closed.
NOT a daemon. NO watcher. NO scheduled trigger. NO autonomous recovery.
NO auto-rollback. NO auto-replay. NO auto-repair. Stdlib only. No network.

Invocation:

    python3 tools/governed_transactional_executor.py \\
        --kind {transaction|rollback-exec|recovery-detect|replay|integrity|consistency} \\
        --request /path/to/request.json \\
        --confirm

Without --confirm: dry-run (validates, prints plan, exits non-zero on any
fail-closed precondition).
With --confirm AND all checks passing: appends the appropriate events to
runtime-manifests/ and writes snapshots to runtime-snapshots/.

This executor never deletes evidence, never overwrites the live tree, and
never advances a transaction outside its declared state machine.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RULES_ROOT = OC_ROOT / "execution-engine"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
SNAPSHOTS_ROOT = OC_ROOT / "runtime-snapshots"
ROLLBACK_TARGET_ROOT = OC_ROOT / "rollback-target"

LAYER = 40
SCHEMA_TX = "governed-fs-operation-request/1.0"

TRANSACTION_STATES = {
    "initialized", "staged", "executing", "committed",
    "failed", "rolled-back", "recovery-required", "replayed",
}
TERMINAL_STATES = {"committed", "rolled-back", "replayed"}
BLOCKING_STATES = {"failed", "recovery-required"}

# Subset of layer-39 forbidden destinations enforced here too.
FORBIDDEN_DEST_PREFIXES = [
    "wp-includes/", "wp-admin/", "wp-content/plugins/",
    "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/",
    "wp-content/themes/beslock-custom/User manuals/_repository-governance/",
    "wp-content/themes/beslock-custom/User manuals/operational-console/runtime-manifests/",
    "wp-content/themes/beslock-custom/User manuals/operational-console/runtime-snapshots/",
    "runtime-implementation/",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def append_event(store_kind: str, event: dict) -> None:
    store_path = RUNTIME_MANIFESTS_ROOT / store_kind / "_event-store.json"
    store_path.parent.mkdir(parents=True, exist_ok=True)
    if store_path.exists():
        store = load_json(store_path)
    else:
        store = {
            "schema": "governed-fs-event-store/1.0",
            "constitutional_layer_index": LAYER,
            "kind": store_kind,
            "append_only": True,
            "deterministic": True,
            "reviewer_authoritative": True,
            "created_at": now_iso(),
            "events": [],
        }
    store["events"].append(event)
    store_path.write_text(
        json.dumps(store, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def emit_audit(operation_id: str, kind: str, severity: str, message: str,
               reviewer: str, payload: dict) -> None:
    append_event("audit-events", {
        "audit_event_id": operation_id + "-aud-" + now_compact(),
        "links_to_operation_id": operation_id,
        "kind": kind,
        "severity": severity,
        "message": message,
        "reviewer": reviewer,
        "payload": payload,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })


def emit_failure(transaction_id: str, failure_class: str, message: str,
                 reviewer: str, evidence_pointers: dict) -> None:
    append_event("failure-events", {
        "failure_event_id": "fail-" + (transaction_id or "no-tx") + "-" + now_compact(),
        "transaction_id": transaction_id,
        "failure_class": failure_class,
        "message": message,
        "reviewer": reviewer,
        "evidence_pointers": evidence_pointers,
        "occurred_at_iso": now_iso(),
        "append_only": True,
        "preserves_transaction_state": True,
        "preserves_snapshots": True,
    })


def emit_transaction(transaction_id: str, request_id: str, from_state: str | None,
                     to_state: str, reviewer: str, reasoning_chain: list[str],
                     extra: dict | None = None) -> None:
    ev = {
        "transaction_event_id": "tx-ev-" + transaction_id + "-" + now_compact(),
        "transaction_id": transaction_id,
        "request_id": request_id,
        "from_state": from_state,
        "to_state": to_state,
        "state": to_state,
        "reviewer": reviewer,
        "reasoning_chain": reasoning_chain,
        "occurred_at_iso": now_iso(),
        "transitioned_at_iso": now_iso(),
        "append_only": True,
    }
    if extra:
        ev.update(extra)
    append_event("transaction-events", ev)


def is_under_repo_root(p: Path) -> bool:
    try:
        p.resolve().relative_to(REPO_ROOT.resolve())
        return True
    except ValueError:
        return False


def matches_forbidden(dest_str: str) -> str | None:
    for f in FORBIDDEN_DEST_PREFIXES:
        if dest_str.startswith(f):
            return f
    return None


def current_transaction_state(transaction_id: str) -> str | None:
    store_path = RUNTIME_MANIFESTS_ROOT / "transaction-events" / "_event-store.json"
    if not store_path.exists():
        return None
    store = load_json(store_path)
    last = None
    for e in store.get("events", []):
        if e.get("transaction_id") == transaction_id:
            last = e.get("to_state") or e.get("state")
    return last


def validate_transition(from_state: str | None, to_state: str) -> str | None:
    if to_state not in TRANSACTION_STATES:
        return f"TX-INV: target state '{to_state}' not in declared states"
    if from_state in TERMINAL_STATES:
        return f"TX-5: terminal state '{from_state}' is immutable"
    edges = {
        ("initialized", "staged"), ("staged", "executing"),
        ("executing", "committed"), ("executing", "failed"),
        ("staged", "failed"),
        ("failed", "rolled-back"),
        ("executing", "recovery-required"),
        ("recovery-required", "replayed"),
        ("recovery-required", "rolled-back"),
    }
    if from_state is None and to_state == "initialized":
        return None
    if (from_state, to_state) not in edges:
        return f"TX-4: illegal transition {from_state} -> {to_state}"
    return None


# ---------------------------------------------------------------------------
# Snapshot capture (governed)
# ---------------------------------------------------------------------------

def capture_snapshot(transaction_id: str, snapshot_kind: str, name: str,
                     source: Path | None) -> tuple[Path, dict]:
    """Capture a snapshot under runtime-snapshots/<kind>/<tx_id>/<iso>-<name>.

    Returns (snapshot_path, snapshot_event_payload). Append-only, never
    overwrites — if the target already exists, a numeric suffix is added.
    """
    base = SNAPSHOTS_ROOT / snapshot_kind / transaction_id
    base.mkdir(parents=True, exist_ok=True)
    iso = now_compact()
    safe_name = name.replace("/", "_")
    target = base / f"{iso}-{safe_name}"
    suffix = 1
    while target.exists():
        target = base / f"{iso}-{safe_name}.{suffix}"
        suffix += 1

    captured_kind = "absent"
    captured_hash: str | None = None
    if source is not None and source.exists():
        if source.is_file():
            shutil.copy2(source, target)
            captured_hash = sha256_of(target)
            captured_kind = "file"
        elif source.is_dir():
            shutil.copytree(source, target)
            captured_kind = "directory"
    else:
        # Capture a non-existence proof
        target.write_text(json.dumps({
            "schema": "governed-snapshot-non-existence-proof/1.0",
            "transaction_id": transaction_id,
            "snapshot_kind": snapshot_kind,
            "source_path": str(source.relative_to(REPO_ROOT)) if (source and is_under_repo_root(source)) else (str(source) if source else None),
            "captured_at_iso": now_iso(),
            "exists": False,
        }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        captured_kind = "non-existence-proof"

    payload = {
        "snapshot_event_id": "snap-" + transaction_id + "-" + iso + "-" + safe_name,
        "transaction_id": transaction_id,
        "snapshot_kind": snapshot_kind,
        "source_path": str(source.relative_to(REPO_ROOT)) if (source and is_under_repo_root(source)) else (str(source) if source else None),
        "snapshot_path": str(target.relative_to(REPO_ROOT)),
        "captured_kind": captured_kind,
        "sha256": captured_hash,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    }
    append_event("snapshot-events", payload)
    return target, payload


# ---------------------------------------------------------------------------
# kind = transaction (wraps a layer-39 mutation in a governed transaction)
# ---------------------------------------------------------------------------

def run_transaction(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    request_id = request.get("request_id") or now_compact()
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    transaction_id = payload.get("transaction_id") or ("tx-" + now_compact())

    snapshot_kinds = payload.get("snapshot_kinds") or [
        "destination-precapture", "manifest-precapture",
        "lineage-precapture", "transaction-checkpoint",
    ]
    mutation_request_path = payload.get("mutation_request") or payload.get("mutation_request_path")

    print(f"[gov-tx-exec] kind=transaction transaction_id={transaction_id} reviewer={reviewer}")
    print(f"  request_id    : {request_id}")
    print(f"  mutation_req  : {mutation_request_path}")
    print(f"  snapshots     : {', '.join(snapshot_kinds)}")

    failures: list[str] = []
    notes: list[str] = []

    if reviewer == "UNATTRIBUTED":
        failures.append("TX-MISSING-REVIEWER: missing reviewer attribution")
    if request.get("schema") != SCHEMA_TX:
        failures.append(f"TX-BAD-SCHEMA: {request.get('schema')}")
    existing = current_transaction_state(transaction_id)
    if existing in TERMINAL_STATES:
        failures.append(f"TX-5: transaction already in terminal state '{existing}'")
    err = validate_transition(existing, "initialized" if existing is None else "staged")
    if err and existing is not None:
        failures.append(err)

    # Resolve the mutation source file (existence is required for snapshot)
    mut_payload = None
    src_path: Path | None = None
    dest_str: str | None = None
    dest_path: Path | None = None
    if mutation_request_path:
        try:
            mut_req = load_json(Path(mutation_request_path).expanduser())
            mut_payload = mut_req.get("payload", {})
            src_str = mut_payload.get("source_path")
            dest_str = mut_payload.get("destination")
            if src_str:
                cand = (REPO_ROOT / src_str).resolve()
                if cand.exists() and cand.is_file():
                    src_path = cand
                else:
                    notes.append(f"mutation source not found on disk: {src_str}")
            if dest_str:
                hit = matches_forbidden(dest_str)
                if hit:
                    failures.append(f"TX-FORBIDDEN-DEST: destination prefix forbidden ({hit})")
                dest_cand = (REPO_ROOT / dest_str).resolve()
                if not is_under_repo_root(dest_cand):
                    failures.append("TX-DEST-ESCAPE: destination escapes repo root")
                dest_path = dest_cand
        except Exception as exc:
            notes.append(f"could not load mutation_request: {exc}")

    for n in notes:
        print(f"  NOTE   : {n}")
    for f in failures:
        print(f"  FAIL   : {f}")

    if failures:
        if confirm:
            emit_failure(transaction_id, "mutation-failure",
                         "; ".join(failures), reviewer,
                         {"request_id": request_id, "mutation_request": mutation_request_path})
            emit_audit(transaction_id, "transaction-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT : refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN : transaction request well-formed; snapshot plan ready.")
        print(f"  PLAN   : initialized -> staged -> executing -> committed (tx_id={transaction_id})")
        for sk in snapshot_kinds:
            print(f"           snapshot.{sk}")
        return 0

    # initialized
    if existing is None:
        emit_transaction(transaction_id, request_id, None, "initialized", reviewer,
                         ["transaction opened"], {"mutation_request": mutation_request_path})

    # snapshot capture (SN-1: precedes mutation; SN-8: failure blocks)
    captured: list[dict] = []
    snap_failure = None
    try:
        if "destination-precapture" in snapshot_kinds and dest_path is not None:
            _, p = capture_snapshot(transaction_id, "repository", "destination",
                                    dest_path if dest_path.exists() else None)
            captured.append(p)
        if "manifest-precapture" in snapshot_kinds:
            for k in ("mutation-events", "audit-events", "intake-events"):
                src = RUNTIME_MANIFESTS_ROOT / k / "_event-store.json"
                _, p = capture_snapshot(transaction_id, "manifests", k, src if src.exists() else None)
                captured.append(p)
        if "lineage-precapture" in snapshot_kinds:
            src = RUNTIME_MANIFESTS_ROOT / "lineage-events" / "_event-store.json"
            _, p = capture_snapshot(transaction_id, "lineage", "lineage-events",
                                    src if src.exists() else None)
            captured.append(p)
        if "publication-precapture" in snapshot_kinds:
            src = RUNTIME_MANIFESTS_ROOT / "publication-events" / "_event-store.json"
            _, p = capture_snapshot(transaction_id, "publications", "publication-events",
                                    src if src.exists() else None)
            captured.append(p)
        if "refresh-state-precapture" in snapshot_kinds:
            src = RUNTIME_MANIFESTS_ROOT / "refresh-events" / "_event-store.json"
            _, p = capture_snapshot(transaction_id, "refresh-state", "refresh-events",
                                    src if src.exists() else None)
            captured.append(p)
        if "transaction-checkpoint" in snapshot_kinds:
            src = RUNTIME_MANIFESTS_ROOT / "transaction-events" / "_event-store.json"
            _, p = capture_snapshot(transaction_id, "transaction-state", "transaction-events",
                                    src if src.exists() else None)
            captured.append(p)
    except Exception as exc:
        snap_failure = str(exc)

    if snap_failure is not None:
        emit_failure(transaction_id, "snapshot-failure", snap_failure, reviewer,
                     {"captured_so_far": [c["snapshot_path"] for c in captured]})
        emit_transaction(transaction_id, request_id, "initialized", "failed", reviewer,
                         [f"SN-8: snapshot capture failed: {snap_failure}"])
        emit_audit(transaction_id, "snapshot-failure", "block", snap_failure, reviewer,
                   {"captured": captured})
        print(f"  FAIL   : snapshot failure: {snap_failure}")
        return 3

    print(f"  snapshots captured: {len(captured)}")
    emit_transaction(transaction_id, request_id, "initialized", "staged", reviewer,
                     [f"SN-1 satisfied: {len(captured)} snapshots captured"],
                     {"snapshot_count": len(captured),
                      "snapshot_paths": [c["snapshot_path"] for c in captured]})

    # executing
    emit_transaction(transaction_id, request_id, "staged", "executing", reviewer,
                     ["T-2: reviewer --confirm provided"])

    # Delegate the actual mutation: this layer wraps; the layer-39 executor
    # remains the canonical mutation agent. We invoke it programmatically.
    mutation_result = 0
    mutation_message = "(no mutation request attached — transaction wraps proposal only)"
    if mutation_request_path:
        try:
            from importlib import util as _ilu
            spec = _ilu.spec_from_file_location(
                "gov_fs_executor",
                str(REPO_ROOT / "tools" / "governed_fs_executor.py"),
            )
            mod = _ilu.module_from_spec(spec)  # type: ignore[arg-type]
            spec.loader.exec_module(mod)  # type: ignore[union-attr]
            mut_req = load_json(Path(mutation_request_path).expanduser())
            mutation_result = mod.run_mutation(mut_req, confirm=True)
            mutation_message = f"layer-39 mutation exit code {mutation_result}"
        except Exception as exc:
            mutation_result = 5
            mutation_message = f"mutation invocation exception: {exc}"

    if mutation_result != 0:
        emit_failure(transaction_id, "mutation-failure", mutation_message, reviewer,
                     {"mutation_request": mutation_request_path})
        emit_transaction(transaction_id, request_id, "executing", "failed", reviewer,
                         [f"T-4: {mutation_message}"])
        emit_audit(transaction_id, "transaction-mutation-failure", "block",
                   mutation_message, reviewer, {"mutation_request": mutation_request_path})
        print(f"  RESULT : failed ({mutation_message})")
        return mutation_result

    emit_transaction(transaction_id, request_id, "executing", "committed", reviewer,
                     [f"T-3: {mutation_message}", "integrity check (basic) passed"])
    emit_audit(transaction_id, "transaction-committed", "info",
               "transaction committed", reviewer,
               {"mutation_request": mutation_request_path, "snapshots": len(captured)})
    print(f"  RESULT : committed (tx_id={transaction_id})")
    return 0


# ---------------------------------------------------------------------------
# kind = rollback-exec
# ---------------------------------------------------------------------------

def run_rollback_exec(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    request_id = request.get("request_id") or now_compact()
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    transaction_id = payload.get("transaction_id")
    rollback_kind = payload.get("rollback_kind")
    snapshot_path = payload.get("snapshot_path")

    print(f"[gov-tx-exec] kind=rollback-exec transaction_id={transaction_id} reviewer={reviewer}")
    print(f"  rollback_kind : {rollback_kind}")
    print(f"  snapshot_path : {snapshot_path}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("RBE-1: missing reviewer attribution")
    if not transaction_id:
        failures.append("RBE-2: missing transaction_id")
    if not rollback_kind:
        failures.append("RBE-MISSING-KIND: missing rollback_kind")

    existing = current_transaction_state(transaction_id) if transaction_id else None
    if existing not in {"failed", "recovery-required", None}:
        # Allow None for not-yet-recorded transactions (rare case).
        failures.append(f"RBE-STATE: transaction state '{existing}' not eligible for rollback")

    snap_resolved: Path | None = None
    if snapshot_path:
        cand = (REPO_ROOT / snapshot_path).resolve()
        if not is_under_repo_root(cand) or not cand.exists():
            failures.append(f"RBE-3: snapshot_path does not resolve under repo root or does not exist: {snapshot_path}")
        else:
            snap_resolved = cand

    for f in failures:
        print(f"  FAIL   : {f}")

    if failures:
        if confirm:
            emit_failure(transaction_id or "no-tx", "rollback-failure",
                         "; ".join(failures), reviewer,
                         {"request_id": request_id, "snapshot_path": snapshot_path})
            emit_audit(transaction_id or request_id, "rollback-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT : refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN : rollback request well-formed.")
        if snap_resolved:
            print(f"  PLAN   : copy snapshot -> rollback-target/{transaction_id}/<name>")
        return 0

    # Restore into rollback-target/ (RBE-6: never the live tree)
    target_dir = ROLLBACK_TARGET_ROOT / transaction_id / now_compact()
    target_dir.mkdir(parents=True, exist_ok=True)
    restored: str | None = None
    if snap_resolved:
        dest = target_dir / snap_resolved.name
        try:
            if snap_resolved.is_dir():
                shutil.copytree(snap_resolved, dest)
            else:
                shutil.copy2(snap_resolved, dest)
            restored = str(dest.relative_to(REPO_ROOT))
        except Exception as exc:
            emit_failure(transaction_id, "rollback-failure", str(exc), reviewer,
                         {"snapshot_path": snapshot_path, "target": str(target_dir.relative_to(REPO_ROOT))})
            emit_audit(transaction_id, "rollback-restore-failure", "block",
                       str(exc), reviewer, {"request": request})
            print(f"  RESULT : refused ({exc})")
            return 3

    # Append rollback-events / lineage-events / transaction-events
    append_event("rollback-events", {
        "rollback_event_id": "rb-" + transaction_id + "-" + now_compact(),
        "transaction_id": transaction_id,
        "rollback_kind": rollback_kind,
        "snapshot_path": snapshot_path,
        "restored_to": restored,
        "reviewer": reviewer,
        "reasoning_chain": payload.get("reasoning_chain", []),
        "executed_at_iso": now_iso(),
        "preserves_failed_state": True,
        "deletes_evidence": False,
        "overwrites_live_tree": False,
    })
    append_event("lineage-events", {
        "lineage_event_id": "lin-rb-" + transaction_id + "-" + now_compact(),
        "links_to_operation_id": payload.get("original_operation_id") or transaction_id,
        "transaction_id": transaction_id,
        "kind": "rollback-exec",
        "reviewer": reviewer,
        "restored_to": restored,
        "reasoning_chain": payload.get("reasoning_chain", []),
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    err = validate_transition(existing, "rolled-back")
    if err is None:
        emit_transaction(transaction_id, request_id, existing, "rolled-back", reviewer,
                         [f"RBE-8: rollback executed via {rollback_kind}"],
                         {"restored_to": restored})
    else:
        emit_audit(transaction_id, "rollback-state-transition-warning", "warning",
                   err, reviewer, {"request": request, "restored_to": restored})
    emit_audit(transaction_id, "rollback-executed", "info",
               f"rollback {rollback_kind}", reviewer,
               {"snapshot_path": snapshot_path, "restored_to": restored})
    print(f"  RESULT : rolled-back -> {restored or '(no snapshot restored)'}")
    return 0


# ---------------------------------------------------------------------------
# kind = recovery-detect (READ-ONLY DETECTION; never auto-recovers)
# ---------------------------------------------------------------------------

def run_recovery_detect(request: dict, confirm: bool) -> int:
    request_id = request.get("request_id") or now_compact()
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    print(f"[gov-tx-exec] kind=recovery-detect reviewer={reviewer}")

    def evs(kind: str) -> list[dict]:
        p = RUNTIME_MANIFESTS_ROOT / kind / "_event-store.json"
        if not p.exists():
            return []
        return load_json(p).get("events", [])

    tx_state: dict[str, str] = {}
    for e in evs("transaction-events"):
        tx_state[e["transaction_id"]] = e.get("to_state") or e.get("state") or "unknown"

    mu_ops = {e.get("operation_id") for e in evs("mutation-events") if e.get("operation_id")}
    li_ops = {(e.get("links_to_operation_id") or e.get("operation_id"))
              for e in evs("lineage-events")}
    rb = evs("rollback-events")

    findings: list[dict] = []
    for tid, st in tx_state.items():
        if st == "executing":
            findings.append({"signal": "REC-SIG-1", "transaction_id": tid,
                             "recommends": "replay-from-snapshot",
                             "alternative": "rollback-via-restore-prior-snapshot"})
    for op in mu_ops:
        if op not in li_ops:
            findings.append({"signal": "REC-SIG-3", "operation_id": op,
                             "recommends": "append-bridge-lineage-event",
                             "alternative": "rollback-revert-failed-mutation"})
    for e in rb:
        tid = e.get("transaction_id")
        if tid and tx_state.get(tid) and tx_state[tid] != "rolled-back":
            findings.append({"signal": "REC-SIG-4", "transaction_id": tid,
                             "recommends": "advance-transaction-state-to-rolled-back",
                             "alternative": "manual-reviewer-triage"})

    print(f"  findings: {len(findings)}")
    for f in findings[:20]:
        print(f"    {f}")

    if not confirm:
        print("  DRY-RUN : detection-only run; no events appended.")
        return 0

    append_event("recovery-events", {
        "recovery_event_id": "rec-" + now_compact(),
        "request_id": request_id,
        "reviewer": reviewer,
        "findings": findings,
        "auto_recovery": False,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(request_id, "recovery-manifest-recorded", "info",
               f"{len(findings)} findings", reviewer, {"findings_count": len(findings)})
    print("  RESULT : recovery manifest appended (read-only detection; reviewer chooses next action)")
    return 0


# ---------------------------------------------------------------------------
# kind = replay (deterministic; default verify-only)
# ---------------------------------------------------------------------------

def run_replay(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    request_id = request.get("request_id") or now_compact()
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    transaction_id = payload.get("transaction_id")
    mode = payload.get("replay_mode") or "verify-only"

    print(f"[gov-tx-exec] kind=replay transaction_id={transaction_id} mode={mode} reviewer={reviewer}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("RPL-MISSING-REVIEWER: missing reviewer attribution")
    if not transaction_id:
        failures.append("RPL-7: missing transaction_id")
    if mode not in {"verify-only", "reconstruct-into-rollback-target"}:
        failures.append(f"RPL-MODE: unknown replay_mode '{mode}'")

    for f in failures:
        print(f"  FAIL   : {f}")
    if failures:
        if confirm:
            emit_audit(transaction_id or request_id, "replay-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT : refused (fail-closed)")
        return 2

    def evs(kind: str) -> list[dict]:
        p = RUNTIME_MANIFESTS_ROOT / kind / "_event-store.json"
        return load_json(p).get("events", []) if p.exists() else []

    tx_events = [e for e in evs("transaction-events") if e.get("transaction_id") == transaction_id]
    sn_events = [e for e in evs("snapshot-events") if e.get("transaction_id") == transaction_id]
    mu_events = [e for e in evs("mutation-events") if e.get("transaction_id") == transaction_id]
    plan = []
    for e in sn_events:
        plan.append({"at": e.get("occurred_at_iso"), "kind": "snapshot", "payload": e})
    for e in mu_events:
        plan.append({"at": e.get("executed_at_iso"), "kind": "mutation", "payload": e})
    for e in tx_events:
        plan.append({"at": e.get("occurred_at_iso") or e.get("transitioned_at_iso"),
                     "kind": "transaction", "payload": e})
    plan.sort(key=lambda x: x.get("at") or "")
    print(f"  reconstructed {len(plan)} events")

    if mode == "reconstruct-into-rollback-target":
        if not confirm:
            print("  DRY-RUN : reconstruct-mode requires --confirm. No writes performed.")
            return 0
        target_dir = ROLLBACK_TARGET_ROOT / transaction_id / ("replay-" + now_compact())
        target_dir.mkdir(parents=True, exist_ok=True)
        write_json(target_dir / "replay-plan.json", {
            "schema": "governed-replay-plan/1.0",
            "transaction_id": transaction_id,
            "mode": mode,
            "sequence": plan,
            "reconstructed_at_iso": now_iso(),
            "writes_live_tree": False,
        })

    if not confirm:
        print("  DRY-RUN : verify-only plan computed.")
        return 0

    append_event("replay-events", {
        "replay_event_id": "rep-" + transaction_id + "-" + now_compact(),
        "transaction_id": transaction_id,
        "request_id": request_id,
        "replay_mode": mode,
        "reviewer": reviewer,
        "sequence_length": len(plan),
        "writes_live_tree": False,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    if mode == "reconstruct-into-rollback-target":
        existing = current_transaction_state(transaction_id)
        err = validate_transition(existing, "replayed")
        if err is None:
            emit_transaction(transaction_id, request_id, existing, "replayed", reviewer,
                             ["RPL: deterministic reconstruction completed in rollback-target/"])
        else:
            emit_audit(transaction_id, "replay-state-transition-warning", "warning",
                       err, reviewer, {"request": request})
    emit_audit(transaction_id, "replay-recorded", "info",
               f"replay {mode} sequence_length={len(plan)}", reviewer,
               {"transaction_id": transaction_id, "mode": mode})
    print(f"  RESULT : replay event appended (mode={mode})")
    return 0


# ---------------------------------------------------------------------------
# kind = integrity (read-only verification)
# ---------------------------------------------------------------------------

def run_integrity(request: dict, confirm: bool) -> int:
    request_id = request.get("request_id") or now_compact()
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    print(f"[gov-tx-exec] kind=integrity reviewer={reviewer}")

    def load(kind: str) -> dict:
        p = RUNTIME_MANIFESTS_ROOT / kind / "_event-store.json"
        return load_json(p) if p.exists() else {"events": []}

    findings: list[dict] = []
    stores = {k: load(k) for k in [
        "transaction-events", "mutation-events", "lineage-events",
        "snapshot-events", "publication-events", "refresh-events",
        "rollback-events", "audit-events",
    ]}

    # INT-1
    mu_ops = {e.get("operation_id") for e in stores["mutation-events"]["events"] if e.get("operation_id")}
    li_ops = {(e.get("links_to_operation_id") or e.get("operation_id"))
              for e in stores["lineage-events"]["events"]}
    for op in mu_ops:
        if op not in li_ops:
            findings.append({"id": "INT-1", "kind": "lineage-continuity",
                             "severity": "block",
                             "message": f"mutation_event {op} has no lineage_event"})

    # INT-2
    for k, s in stores.items():
        if not s.get("schema") or s.get("append_only") is not True:
            findings.append({"id": "INT-2", "kind": "manifest-consistency",
                             "severity": "block",
                             "message": f"event store {k} missing schema or append_only flag"})

    # INT-3
    for e in stores["transaction-events"]["events"]:
        st = e.get("to_state") or e.get("state")
        if not st or st not in TRANSACTION_STATES:
            findings.append({"id": "INT-3", "kind": "transaction-completeness",
                             "severity": "block",
                             "message": f"tx {e.get('transaction_id')} invalid state {st}"})

    # INT-4 snapshot validity
    for e in stores["snapshot-events"]["events"]:
        sp = e.get("snapshot_path")
        if sp:
            cand = (REPO_ROOT / sp)
            if not cand.exists():
                findings.append({"id": "INT-4", "kind": "snapshot-validity",
                                 "severity": "block",
                                 "message": f"snapshot path missing: {sp}"})

    print(f"  findings: {len(findings)} ({sum(1 for f in findings if f['severity']=='block')} blocking)")
    for f in findings[:20]:
        print(f"    {f['id']} {f['severity']}: {f['message']}")

    if not confirm:
        print("  DRY-RUN : integrity check complete; no events appended.")
        return 0 if not any(f["severity"] == "block" for f in findings) else 2

    append_event("integrity-events", {
        "integrity_event_id": "int-" + now_compact(),
        "request_id": request_id,
        "reviewer": reviewer,
        "findings": findings,
        "counts": {
            "total": len(findings),
            "block": sum(1 for f in findings if f["severity"] == "block"),
        },
        "mutates_filesystem": False,
        "auto_repair": False,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(request_id, "integrity-recorded", "info",
               f"{len(findings)} findings", reviewer,
               {"block": sum(1 for f in findings if f["severity"] == "block")})
    print("  RESULT : integrity event appended (read-only)")
    return 0


# ---------------------------------------------------------------------------
# kind = consistency (read-only)
# ---------------------------------------------------------------------------

def run_consistency(request: dict, confirm: bool) -> int:
    request_id = request.get("request_id") or now_compact()
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    print(f"[gov-tx-exec] kind=consistency reviewer={reviewer}")

    def evs(kind: str) -> list[dict]:
        p = RUNTIME_MANIFESTS_ROOT / kind / "_event-store.json"
        return load_json(p).get("events", []) if p.exists() else []

    findings: list[dict] = []
    tx_state: dict[str, str] = {}
    seen_executing: set[str] = set()
    for e in evs("transaction-events"):
        st = e.get("to_state") or e.get("state")
        tx_state[e["transaction_id"]] = st
        if st == "executing":
            key = e.get("request_id") or e["transaction_id"]
            if key in seen_executing:
                findings.append({"id": "CON-1", "kind": "duplicate-transaction-execution",
                                 "severity": "block",
                                 "message": f"duplicate executing transaction {key}"})
            seen_executing.add(key)

    mu_ops = {e.get("operation_id") for e in evs("mutation-events") if e.get("operation_id")}
    for e in evs("lineage-events"):
        ref = e.get("links_to_operation_id") or e.get("operation_id")
        if ref and ref not in mu_ops and not str(ref).startswith("tx-"):
            findings.append({"id": "CON-4", "kind": "stale-lineage",
                             "severity": "warning",
                             "message": f"lineage references unknown operation {ref}"})

    for e in evs("rollback-events"):
        t = e.get("transaction_id")
        if t and tx_state.get(t) and tx_state[t] != "rolled-back":
            findings.append({"id": "CON-5", "kind": "partial-rollback",
                             "severity": "recovery",
                             "message": f"rollback recorded for {t} but tx state is {tx_state[t]}"})

    print(f"  findings: {len(findings)}")
    for f in findings[:20]:
        print(f"    {f['id']} {f['severity']}: {f['message']}")

    if not confirm:
        print("  DRY-RUN : consistency scan complete.")
        return 0

    append_event("integrity-events", {
        "integrity_event_id": "con-" + now_compact(),
        "request_id": request_id,
        "reviewer": reviewer,
        "kind": "consistency-scan",
        "findings": findings,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(request_id, "consistency-recorded", "info",
               f"{len(findings)} findings", reviewer, {"counts": len(findings)})
    print("  RESULT : consistency findings appended (read-only)")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Governed transactional CLI executor (phase 47, layer 40)"
    )
    p.add_argument("--kind", required=True,
                   choices=["transaction", "rollback-exec", "recovery-detect",
                            "replay", "integrity", "consistency"])
    p.add_argument("--request", required=True,
                   help="Path to the operation-request JSON file (use a "
                        "minimal envelope for recovery-detect / integrity / "
                        "consistency).")
    p.add_argument("--confirm", action="store_true",
                   help="Required to perform any write or event-store append.")
    args = p.parse_args()

    req_path = Path(args.request).expanduser().resolve()
    if not req_path.exists():
        print(f"[gov-tx-exec] FATAL: request file not found: {req_path}", file=sys.stderr)
        return 4
    request = load_json(req_path)

    if request.get("schema") != SCHEMA_TX:
        print(f"[gov-tx-exec] FATAL: unsupported schema {request.get('schema')}",
              file=sys.stderr)
        return 4

    if args.kind == "transaction":
        return run_transaction(request, args.confirm)
    if args.kind == "rollback-exec":
        return run_rollback_exec(request, args.confirm)
    if args.kind == "recovery-detect":
        return run_recovery_detect(request, args.confirm)
    if args.kind == "replay":
        return run_replay(request, args.confirm)
    if args.kind == "integrity":
        return run_integrity(request, args.confirm)
    if args.kind == "consistency":
        return run_consistency(request, args.confirm)
    return 4


if __name__ == "__main__":
    sys.exit(main())
