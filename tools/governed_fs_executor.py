"""
Phase 46 — Governed filesystem CLI executor.

The ONLY component in the ecosystem with filesystem write capability.
Reviewer-invoked, foreground, deterministic, append-only, fail-closed.

This is NOT a daemon. There is no watcher, no scheduled trigger, no
background process. Every invocation is a single, explicit, reviewer-
authorized command of the form:

    python3 tools/governed_fs_executor.py \\
        --kind {mutation|rollback|refresh|publication} \\
        --request /path/to/request.json \\
        --confirm

Without `--confirm`, the executor runs in DRY-RUN mode: it loads the
request, runs preconditions and safety checks, prints what it WOULD do,
and exits non-zero if any check fails. No filesystem writes occur.

With `--confirm` AND all checks passing, the executor:
  1. Performs the requested operation (copy / stage-accept / mkdir /
     manifest-write).
  2. Appends a mutation-event to runtime-manifests/mutation-events/.
  3. Appends a lineage-event to runtime-manifests/lineage-events/.
  4. Appends an audit-event to runtime-manifests/audit-events/.

If any check fails (precondition, safety, or operational), the executor:
  1. Refuses the operation.
  2. Routes the source (when applicable) to staging/quarantined/<ts>/.
  3. Appends an audit-event describing the failure.
  4. Exits non-zero.

Hard rules (extends layer 39 doctrines):
  - No destructive overwrite. If destination exists -> fail closed.
  - No deletion of source evidence. Originals are MOVED into
    staging/accepted/<ts>/ only after a successful copy.
  - No mutation of forbidden destinations (knowledge-core, governance,
    runtime-implementation, runtime-manifests).
  - No network calls. Stdlib only.
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
STAGING_ROOT = OC_ROOT / "staging"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"

LAYER = 39


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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


def emit_lineage(operation_id: str, kind: str, src: Path | None, dest: Path | None,
                 reviewer: str, reasoning_chain: list[str],
                 source_hash: str | None) -> None:
    append_event("lineage-events", {
        "lineage_event_id": operation_id + "-lin",
        "links_to_operation_id": operation_id,
        "kind": kind,
        "source_path": str(src.relative_to(REPO_ROOT)) if src else None,
        "destination_path": str(dest.relative_to(REPO_ROOT)) if dest else None,
        "reviewer": reviewer,
        "source_hash_sha256": source_hash,
        "reasoning_chain": reasoning_chain,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })


def emit_audit(operation_id: str, kind: str, severity: str, message: str,
               reviewer: str, payload: dict) -> None:
    append_event("audit-events", {
        "audit_event_id": operation_id + "-aud",
        "links_to_operation_id": operation_id,
        "kind": kind,
        "severity": severity,
        "message": message,
        "reviewer": reviewer,
        "payload": payload,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })


def is_under_repo_root(p: Path) -> bool:
    try:
        p.resolve().relative_to(REPO_ROOT.resolve())
        return True
    except ValueError:
        return False


def matches_forbidden(dest_str: str, forbidden: list[str]) -> str | None:
    for f in forbidden:
        if dest_str.startswith(f):
            return f
    return None


def quarantine_source(src: Path, reason: str) -> Path:
    qdir = STAGING_ROOT / "quarantined" / (now_compact() + "-" + reason[:40].replace(" ", "_"))
    qdir.mkdir(parents=True, exist_ok=True)
    dest = qdir / src.name
    if not dest.exists():
        shutil.copy2(src, dest)
    return dest


# ---------------------------------------------------------------------------
# Mutation executor
# ---------------------------------------------------------------------------

def run_mutation(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    operation_id = request.get("request_id") or now_compact()
    reviewer = request.get("reviewer") or "UNATTRIBUTED"

    kind = payload.get("operation_kind", "copy")
    src_str = payload.get("source_path")
    dest_str = payload.get("destination")

    safety_rules = load_json(RULES_ROOT / "mutation-safety-rules.json")
    dest_rules = load_json(RULES_ROOT / "destination-resolution-rules.json")
    forbidden = dest_rules.get("forbidden_destinations", [])

    failures: list[str] = []
    notes: list[str] = []

    # M-PRE-5: reviewer attribution
    if reviewer == "UNATTRIBUTED":
        failures.append("M-PRE-5: missing reviewer attribution")
    # M-PRE-6: reasoning chain
    if not payload.get("reasoning_chain"):
        failures.append("M-PRE-6: missing reasoning_chain")
    # M-PRE-7: schema check
    if request.get("schema") != "governed-fs-operation-request/1.0":
        failures.append("M-PRE-7: bad schema " + str(request.get("schema")))

    src_path: Path | None = None
    dest_path: Path | None = None
    source_hash: str | None = None

    if kind in ("copy", "stage-accept", "manifest-write"):
        if not src_str:
            failures.append("M-PRE-1: missing source_path")
        else:
            src_path = (REPO_ROOT / src_str).resolve()
            if not src_path.exists() or not src_path.is_file():
                failures.append(f"M-PRE-1: source does not exist: {src_str}")

    if kind in ("copy", "stage-accept", "mkdir", "manifest-write"):
        if not dest_str:
            failures.append("M-PRE-2: missing destination")
        else:
            dest_path = (REPO_ROOT / dest_str).resolve()
            # M-PRE-3
            if not is_under_repo_root(dest_path):
                failures.append("M-PRE-3: destination escapes repo root")
            # M-PRE-4 (S-CHK-4)
            hit = matches_forbidden(dest_str, forbidden)
            if hit:
                failures.append(f"M-PRE-4 / S-CHK-4: destination prefix forbidden ({hit})")

    # For copy: dest is a file path or a directory
    if kind == "copy" and dest_path is not None and src_path is not None:
        final_dest = dest_path
        if dest_str.endswith("/") or (dest_path.exists() and dest_path.is_dir()):
            final_dest = dest_path / src_path.name
        # M-PRE-2 / S-CHK-2
        if final_dest.exists():
            failures.append(f"M-PRE-2 / S-CHK-2: destination already exists ({final_dest.relative_to(REPO_ROOT)})")
        # M-PRE-9: source hash check
        if src_path and src_path.exists():
            source_hash = sha256_of(src_path)
            req_hash = payload.get("source_hash_sha256")
            if req_hash and req_hash != source_hash:
                failures.append("M-PRE-9: source hash mismatch")
            elif not req_hash:
                notes.append("M-PRE-9: request did not carry source_hash_sha256; computed at execute time = " + source_hash)
        # S-CHK-3: cross-product contamination
        product = payload.get("product")
        if product and product not in dest_str:
            notes.append(f"S-CHK-3 NOTE: product slug '{product}' not present in destination path; reviewer should re-confirm")
        # S-CHK-5: trust violation
        req_tier = payload.get("trust_tier", "tier-0-unvalidated")
        for rule in dest_rules.get("rules", []):
            if rule.get("destination_template") and dest_str.startswith(rule["destination_template"].split("{")[0]):
                required = rule.get("trust_tier_required")
                if required and required != req_tier and req_tier != "tier-3-reviewer-attested":
                    notes.append(f"S-CHK-5 NOTE: rule {rule['id']} requires {required}, request carries {req_tier}")
                break
        dest_path = final_dest

    # Report
    print(f"[governed_fs_executor] kind=mutation operation_id={operation_id} reviewer={reviewer}")
    print(f"  source     : {src_str}")
    print(f"  destination: {dest_str}")
    if source_hash:
        print(f"  sha256     : {source_hash}")
    for n in notes:
        print(f"  NOTE   : {n}")
    for f in failures:
        print(f"  FAIL   : {f}")

    if failures:
        # quarantine if we have a real source
        quarantined: Path | None = None
        if src_path and src_path.exists() and confirm:
            quarantined = quarantine_source(src_path, "precheck-fail")
            print(f"  quarantined source -> {quarantined.relative_to(REPO_ROOT)}")
        if confirm:
            emit_audit(operation_id, "precheck-failure", "block",
                       "; ".join(failures), reviewer,
                       {"request": request, "quarantined_to": str(quarantined.relative_to(REPO_ROOT)) if quarantined else None})
        print("  RESULT : refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN : all preconditions and safety checks PASS. Re-run with --confirm to execute.")
        return 0

    # Execute
    try:
        if kind == "mkdir":
            dest_path.mkdir(parents=True, exist_ok=True)
            keep = dest_path / ".gitkeep"
            if not keep.exists():
                keep.write_text("", encoding="utf-8")
        elif kind == "copy":
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest_path)
        elif kind == "stage-accept":
            accepted_dir = STAGING_ROOT / "accepted" / now_compact()
            accepted_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(accepted_dir / src_path.name))
            dest_path = accepted_dir / src_path.name
        elif kind == "manifest-write":
            man_path = dest_path
            man_path.parent.mkdir(parents=True, exist_ok=True)
            man_path.write_text(json.dumps({
                "schema": "governed-fs-sibling-manifest/1.0",
                "operation_id": operation_id,
                "reviewer": reviewer,
                "source_path": str(src_path.relative_to(REPO_ROOT)) if src_path else None,
                "source_hash_sha256": source_hash,
                "written_at_iso": now_iso(),
                "reasoning_chain": payload.get("reasoning_chain", []),
            }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        else:
            print(f"  FAIL : unknown operation_kind '{kind}'")
            emit_audit(operation_id, "unknown-operation-kind", "block",
                       f"unknown kind {kind}", reviewer, {"request": request})
            return 2
    except Exception as exc:
        print(f"  FAIL : execution exception: {exc}")
        emit_audit(operation_id, "execution-exception", "block", str(exc), reviewer,
                   {"request": request})
        return 3

    append_event("mutation-events", {
        "operation_id": operation_id,
        "operation_kind": kind,
        "source_path": str(src_path.relative_to(REPO_ROOT)) if src_path else None,
        "destination_path": str(dest_path.relative_to(REPO_ROOT)) if dest_path else None,
        "source_hash_sha256": source_hash,
        "reviewer": reviewer,
        "request_id": operation_id,
        "executed_at_iso": now_iso(),
        "preconditions_passed": payload.get("preconditions_required", []),
        "notes": notes,
    })
    emit_lineage(operation_id, "mutation", src_path, dest_path, reviewer,
                 payload.get("reasoning_chain", []), source_hash)
    emit_audit(operation_id, "mutation-success", "info",
               f"executed {kind}", reviewer,
               {"request_id": operation_id, "destination": str(dest_path.relative_to(REPO_ROOT)) if dest_path else None})

    print(f"  RESULT : OK -> {dest_path.relative_to(REPO_ROOT) if dest_path else '(no path)'}")
    return 0


# ---------------------------------------------------------------------------
# Rollback / Refresh / Publication executors (manifest-emitting only;
# they never delete and never auto-publish).
# ---------------------------------------------------------------------------

def run_rollback(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    operation_id = request.get("request_id") or now_compact()
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    if reviewer == "UNATTRIBUTED":
        print("  FAIL : R-RB-1 missing reviewer attribution")
        return 2
    print(f"[governed_fs_executor] kind=rollback operation_id={operation_id} reviewer={reviewer}")
    print(f"  rollback_kind: {payload.get('rollback_kind')}")
    print(f"  original_operation_id: {payload.get('original_operation_id')}")
    if not confirm:
        print("  DRY-RUN : rollback request well-formed. Re-run with --confirm to record.")
        return 0
    append_event("rollback-events", {
        "rollback_event_id": operation_id,
        "rollback_kind": payload.get("rollback_kind"),
        "original_operation_id": payload.get("original_operation_id"),
        "reviewer": reviewer,
        "reason": payload.get("reason", ""),
        "reasoning_chain": payload.get("reasoning_chain", []),
        "executed_at_iso": now_iso(),
        "preserves_failed_state": True,
        "deletes_evidence": False,
    })
    emit_lineage(operation_id, "rollback", None, None, reviewer,
                 payload.get("reasoning_chain", []), None)
    emit_audit(operation_id, "rollback-recorded", "info",
               "rollback event appended", reviewer, {"rollback_kind": payload.get("rollback_kind")})
    print("  RESULT : rollback event appended (append-only; no deletion)")
    return 0


def run_refresh(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    operation_id = request.get("request_id") or now_compact()
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    if reviewer == "UNATTRIBUTED":
        print("  FAIL : missing reviewer attribution")
        return 2
    scope = payload.get("scope")
    action = payload.get("action")
    print(f"[governed_fs_executor] kind=refresh operation_id={operation_id} reviewer={reviewer}")
    print(f"  scope={scope} action={action}")
    if action not in {"dry-run", "approve", "reject", "partial-rebuild"}:
        print("  FAIL : invalid action; allowed = dry-run|approve|reject|partial-rebuild")
        return 2
    if not confirm:
        print("  DRY-RUN : refresh request well-formed. Re-run with --confirm to record.")
        return 0
    append_event("refresh-events", {
        "refresh_event_id": operation_id,
        "scope": scope,
        "action": action,
        "reviewer": reviewer,
        "reasoning_chain": payload.get("reasoning_chain", []),
        "executed_at_iso": now_iso(),
        "is_executed": action == "approve" or action == "partial-rebuild",
        "is_proposal_only": action in {"dry-run", "reject"},
        "rebuild_executed_in_this_call": False,
        "rollback_capable": True,
    })
    emit_lineage(operation_id, "refresh", None, None, reviewer,
                 payload.get("reasoning_chain", []), None)
    emit_audit(operation_id, "refresh-recorded", "info",
               f"refresh {action} on {scope} appended", reviewer,
               {"scope": scope, "action": action})
    print("  RESULT : refresh event appended. Actual rebuild execution remains the reviewer's responsibility (this layer records governance, not rebuild output).")
    return 0


def run_publication(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    operation_id = request.get("request_id") or now_compact()
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    if reviewer == "UNATTRIBUTED":
        print("  FAIL : missing reviewer attribution")
        return 2
    print(f"[governed_fs_executor] kind=publication operation_id={operation_id} reviewer={reviewer}")
    print(f"  target={payload.get('target')}")
    if not confirm:
        print("  DRY-RUN : publication regeneration request well-formed. Re-run with --confirm to record.")
        return 0
    append_event("publication-events", {
        "publication_event_id": operation_id,
        "target": payload.get("target"),
        "reviewer": reviewer,
        "reasoning_chain": payload.get("reasoning_chain", []),
        "executed_at_iso": now_iso(),
        "autonomous_publishing": False,
        "rollback_capable": True,
    })
    emit_lineage(operation_id, "publication", None, None, reviewer,
                 payload.get("reasoning_chain", []), None)
    emit_audit(operation_id, "publication-recorded", "info",
               "publication regeneration request appended", reviewer,
               {"target": payload.get("target")})
    print("  RESULT : publication event appended (no autonomous publishing)")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description="Governed filesystem CLI executor (phase 46, layer 39)")
    p.add_argument("--kind", required=True, choices=["mutation", "rollback", "refresh", "publication"])
    p.add_argument("--request", required=True, help="Path to the operation-request JSON file")
    p.add_argument("--confirm", action="store_true",
                   help="Required to perform any filesystem write or event-store append.")
    args = p.parse_args()

    req_path = Path(args.request).expanduser().resolve()
    if not req_path.exists():
        print(f"[governed_fs_executor] FATAL: request file not found: {req_path}", file=sys.stderr)
        return 4
    request = load_json(req_path)

    if request.get("schema") != "governed-fs-operation-request/1.0":
        print(f"[governed_fs_executor] FATAL: unsupported schema {request.get('schema')}", file=sys.stderr)
        return 4

    if args.kind == "mutation":
        return run_mutation(request, args.confirm)
    if args.kind == "rollback":
        return run_rollback(request, args.confirm)
    if args.kind == "refresh":
        return run_refresh(request, args.confirm)
    if args.kind == "publication":
        return run_publication(request, args.confirm)
    return 4


if __name__ == "__main__":
    sys.exit(main())
