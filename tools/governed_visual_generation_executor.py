"""
Phase 50 — Governed visual generation & deterministic asset production CLI executor (layer 43).

Reviewer-invoked. Foreground. Deterministic. Append-only. Fail-closed.
NO daemon. NO watcher. NO scheduler. NO LLM. NO ML. NO probabilistic visual matching.
NO autonomous image generation. NO cloud / SaaS. NO autonomous selection.
Stdlib only.

The runtime DOES NOT generate images. It records reviewer-authored generation
requests, reviewer-supplied output bytes (with sha256 provenance), reviewer
comparisons, reviewer selections, reviewer-attributed lifecycle transitions,
and reviewer-led integrity checks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
VG_ROOT = OC_ROOT / "visual-generation-runtime"

GENERATION_REQUESTS_DIR = VG_ROOT / "generation-requests"
GENERATED_ASSETS_DIR = VG_ROOT / "generated-assets"
GENERATED_CANDIDATES_DIR = VG_ROOT / "generated-candidates"
REVIEW_COMPARISONS_DIR = VG_ROOT / "review-comparisons"
VISUAL_LINEAGE_DIR = VG_ROOT / "visual-lineage"
GENERATION_SESSIONS_DIR = VG_ROOT / "generation-sessions"
VISUAL_SUPERSEDENCE_DIR = VG_ROOT / "visual-supersedence"
PUBLICATION_VISUAL_SELECTIONS_DIR = VG_ROOT / "publication-visual-selections"
REVIEWER_APPROVALS_DIR = VG_ROOT / "reviewer-approvals"
REJECTED_ASSETS_DIR = VG_ROOT / "rejected-assets"
DEPRECATED_ASSETS_DIR = VG_ROOT / "deprecated-assets"

LAYER = 43
SCHEMA = "governed-fs-operation-request/1.0"

ASSET_KINDS = {
    "generated", "oem", "edited", "supportive",
    "procedural-sequence", "troubleshooting", "specification",
}

LIFECYCLE_STATES = {
    "candidate", "review-required", "reviewer-approved",
    "publication-selected", "superseded", "deprecated", "rejected",
}
LIFECYCLE_TERMINAL = {"deprecated", "rejected"}
LIFECYCLE_EDGES = {
    ("candidate", "review-required"),
    ("candidate", "rejected"),
    ("review-required", "reviewer-approved"),
    ("review-required", "rejected"),
    ("review-required", "candidate"),
    ("reviewer-approved", "publication-selected"),
    ("reviewer-approved", "review-required"),
    ("publication-selected", "superseded"),
    ("publication-selected", "deprecated"),
    ("superseded", "deprecated"),
}

SESSION_STATES = {"open", "frozen", "closed", "rejected"}
SESSION_TERMINAL = {"closed", "rejected"}
SESSION_EDGES = {
    ("open", "frozen"),
    ("open", "rejected"),
    ("frozen", "open"),
    ("frozen", "closed"),
    ("frozen", "rejected"),
}

COMPARISON_VERDICTS = {"prefer", "acceptable", "reject", "defer"}

# Forbidden destinations: OEM source roots, layer-42 visual publication builds,
# live publication tree, knowledge-core, governance, runtime-implementation, runtime-manifests payloads.
FORBIDDEN_OVERWRITE_PREFIXES = (
    "wp-content/themes/beslock-custom/User manuals/operational-console/visual-publication-builds/",
    "wp-content/themes/beslock-custom/User manuals/operational-console/visual-asset-ledger/",
    "wp-content/themes/beslock-custom/User manuals/operational-console/runtime-manifests/",
    "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/",
    "wp-content/themes/beslock-custom/User manuals/_repository-governance/",
    "runtime-implementation/",
    "wp-content/uploads/",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def write_collision_safe_json(directory: Path, base_id: str, payload: dict) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{base_id}-{now_compact()}.json"
    suffix = 1
    while target.exists():
        target = directory / f"{base_id}-{now_compact()}.{suffix}.json"
        suffix += 1
    write_json(target, payload)
    return target


def find_asset_record(asset_id: str) -> dict | None:
    """Scan asset manifests on disk for the given asset_id (latest)."""
    if not GENERATED_ASSETS_DIR.exists():
        return None
    latest = None
    for p in sorted(GENERATED_ASSETS_DIR.glob("*.json")):
        try:
            d = load_json(p)
        except Exception:
            continue
        if d.get("asset_id") == asset_id:
            latest = d
    return latest


def current_asset_state(asset_id: str) -> str | None:
    store_path = RUNTIME_MANIFESTS_ROOT / "variant-lineage-events" / "_event-store.json"
    last = None
    if store_path.exists():
        for e in load_json(store_path).get("events", []):
            if e.get("asset_id") == asset_id and e.get("kind") == "lifecycle-transition":
                last = e.get("to_state")
            if e.get("asset_id") == asset_id and e.get("kind") == "register" and last is None:
                last = "candidate"
    return last


def current_session_state(session_id: str) -> str | None:
    store_path = RUNTIME_MANIFESTS_ROOT / "generation-session-events" / "_event-store.json"
    if not store_path.exists():
        return None
    last = None
    for e in load_json(store_path).get("events", []):
        if e.get("session_id") == session_id:
            if e.get("kind") == "open" and last is None:
                last = "open"
            elif e.get("kind") == "transition":
                last = e.get("to_state")
    return last


def attempts_overwrite_forbidden(target_path: str) -> bool:
    norm = target_path.replace("\\", "/").lstrip("./")
    return any(norm.startswith(p) for p in FORBIDDEN_OVERWRITE_PREFIXES)


# ---------------------------------------------------------------------------
# kind = generation-request
# ---------------------------------------------------------------------------

def run_generation_request(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    grid = payload.get("generation_request_id") or ("gr-" + now_compact())
    print(f"[gov-vg-exec] kind=generation-request id={grid} reviewer={reviewer}")
    print(f"  asset_kind={payload.get('asset_kind')} variant_count={payload.get('variant_count')} "
          f"session={payload.get('session_id')}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("GR-1: reviewer attribution required")
    for f in ("grounding_id", "prompt_id", "synthesis_id", "canonical_product_id"):
        if not payload.get(f):
            failures.append(f"GR-2: {f} required")
    if payload.get("asset_kind") not in ASSET_KINDS:
        failures.append(f"GR-7: invalid asset_kind '{payload.get('asset_kind')}'")
    try:
        n = int(payload.get("variant_count"))
        if n < 1:
            failures.append("GR-6: variant_count must be >= 1")
    except (TypeError, ValueError):
        failures.append("GR-6: variant_count must be an integer >= 1")

    sid = payload.get("session_id")
    if sid:
        sstate = current_session_state(sid)
        if sstate is None:
            failures.append(f"GS-5: session '{sid}' is not open")
        elif sstate not in {"open"}:
            failures.append(f"GS-2: session '{sid}' state is '{sstate}', cannot accept new requests")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(grid, "generation-request-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN: generation-request well-formed.")
        return 0

    manifest = {
        "schema": "visual-generation-request-manifest/1.0",
        "constitutional_layer_index": LAYER,
        "generation_request_id": grid,
        "session_id": sid,
        "grounding_id": payload.get("grounding_id"),
        "prompt_id": payload.get("prompt_id"),
        "prompt_revision_id": payload.get("prompt_revision_id"),
        "synthesis_id": payload.get("synthesis_id"),
        "canonical_product_id": payload.get("canonical_product_id"),
        "asset_kind": payload.get("asset_kind"),
        "variant_count": int(payload.get("variant_count")),
        "constraints": list(payload.get("constraints") or []),
        "rationale": payload.get("rationale", ""),
        "reviewer": reviewer,
        "created_at_iso": now_iso(),
        "append_only": True,
    }
    out = write_collision_safe_json(GENERATION_REQUESTS_DIR, grid, manifest)
    append_event("visual-generation-events", {
        "event_id": "vge-" + now_compact(),
        "kind": "generation-request",
        "generation_request_id": grid,
        "session_id": sid,
        "reviewer": reviewer,
        "manifest_path": str(out.relative_to(REPO_ROOT)),
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    print(f"  RESULT: generation-request manifest -> {out.relative_to(REPO_ROOT)}")
    return 0


# ---------------------------------------------------------------------------
# kind = generated-asset-register
# ---------------------------------------------------------------------------

def run_generated_asset_register(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    grid = payload.get("generation_request_id")
    sha = payload.get("asset_sha256")
    vidx = payload.get("variant_index")
    asset_kind = payload.get("asset_kind") or "generated"
    print(f"[gov-vg-exec] kind=generated-asset-register reviewer={reviewer}")
    print(f"  generation_request_id={grid} variant_index={vidx} asset_kind={asset_kind} sha256={sha}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("VL-2: reviewer attribution required")
    if not grid:
        failures.append("VL-2: generation_request_id required")
    if not sha or len(sha) != 64:
        failures.append("VL-3: asset_sha256 (64-hex) required")
    if not isinstance(vidx, int):
        failures.append("VL-1: variant_index (int) required")
    if asset_kind not in ASSET_KINDS:
        failures.append(f"VL-6: invalid asset_kind '{asset_kind}'")
    if not payload.get("source_provenance"):
        failures.append("VL-2: source_provenance required")

    sp = payload.get("source_provenance") or {}
    if asset_kind == "oem":
        if sp.get("kind") != "oem-source":
            failures.append("VL-6: OEM asset MUST carry source_provenance.kind='oem-source'")
        if (payload.get("trust_tier") or "") != "OEM":
            failures.append("VL-6: OEM asset MUST carry trust_tier=OEM")
    if asset_kind == "edited":
        if not payload.get("parent_asset_id"):
            failures.append("VL-7: edited asset MUST cite parent_asset_id")
        if (payload.get("edit_kind") or "") == "watermark-removal":
            failures.append("VL-7: watermark-removal edits are FORBIDDEN")
    if asset_kind == "generated":
        if not payload.get("prompt_revision_id"):
            failures.append("IN-2: generated asset MUST cite prompt_revision_id")
        if not payload.get("grounding_id"):
            failures.append("IN-3: generated asset MUST cite grounding_id (grounding-preservation)")

    target_path = sp.get("target_path") or ""
    if target_path and attempts_overwrite_forbidden(target_path):
        failures.append(f"IN-5: source_provenance.target_path '{target_path}' attempts to write a forbidden destination")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(grid or "unknown", "asset-register-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    asset_id = payload.get("asset_id") or sha256_hex(f"{grid}|{vidx}|{sha}")[:32]
    print(f"  derived asset_id={asset_id}")

    if not confirm:
        print("  DRY-RUN: asset-register well-formed.")
        return 0

    manifest = {
        "schema": "generated-asset-manifest/1.0",
        "constitutional_layer_index": LAYER,
        "asset_id": asset_id,
        "generation_request_id": grid,
        "variant_index": vidx,
        "asset_sha256": sha,
        "asset_kind": asset_kind,
        "trust_tier": payload.get("trust_tier"),
        "source_provenance": sp,
        "prompt_revision_id": payload.get("prompt_revision_id"),
        "grounding_id": payload.get("grounding_id"),
        "synthesis_id": payload.get("synthesis_id"),
        "parent_asset_id": payload.get("parent_asset_id"),
        "edit_kind": payload.get("edit_kind"),
        "reviewer": reviewer,
        "lifecycle_state_initial": "candidate",
        "created_at_iso": now_iso(),
        "append_only": True,
    }
    out = write_collision_safe_json(GENERATED_ASSETS_DIR, asset_id, manifest)
    append_event("variant-lineage-events", {
        "event_id": "vle-" + now_compact(),
        "kind": "register",
        "asset_id": asset_id,
        "generation_request_id": grid,
        "variant_index": vidx,
        "asset_sha256": sha,
        "asset_kind": asset_kind,
        "reviewer": reviewer,
        "manifest_path": str(out.relative_to(REPO_ROOT)),
        "to_state": "candidate",
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    print(f"  RESULT: asset registered -> {out.relative_to(REPO_ROOT)}")
    return 0


# ---------------------------------------------------------------------------
# kind = review-comparison
# ---------------------------------------------------------------------------

def run_review_comparison(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    cid = payload.get("comparison_id") or ("cmp-" + now_compact())
    entries = payload.get("entries") or []
    print(f"[gov-vg-exec] kind=review-comparison id={cid} reviewer={reviewer}")
    print(f"  entries={len(entries)} dimension={payload.get('comparison_dimension')}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("RC-3: reviewer attribution required")
    if len(entries) < 2:
        failures.append("RC-1: at least two entries required")
    seen_assets: set[str] = set()
    for i, e in enumerate(entries):
        if not e.get("asset_id"):
            failures.append(f"RC-1: entry {i} missing asset_id")
            continue
        if e.get("asset_id") in seen_assets:
            failures.append(f"RC-1: duplicate asset_id in entry {i}")
        seen_assets.add(e.get("asset_id"))
        if e.get("verdict") not in COMPARISON_VERDICTS:
            failures.append(f"RC-3: entry {i} invalid verdict '{e.get('verdict')}'")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(cid, "review-comparison-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN: review-comparison well-formed.")
        return 0

    deterministic_entries = []
    for i, e in enumerate(entries):
        deterministic_entries.append({
            "asset_id": e.get("asset_id"),
            "display_order": i,
            "verdict": e.get("verdict"),
            "reviewer_score": e.get("reviewer_score"),
            "reviewer_notes": e.get("reviewer_notes", ""),
        })
    manifest = {
        "schema": "review-comparison-manifest/1.0",
        "constitutional_layer_index": LAYER,
        "comparison_id": cid,
        "comparison_dimension": payload.get("comparison_dimension") or "overall",
        "group_id": payload.get("group_id"),
        "prior_comparison_id": payload.get("prior_comparison_id"),
        "entries": deterministic_entries,
        "reviewer": reviewer,
        "created_at_iso": now_iso(),
        "append_only": True,
    }
    out = write_collision_safe_json(REVIEW_COMPARISONS_DIR, cid, manifest)
    append_event("review-comparison-events", {
        "event_id": "rce-" + now_compact(),
        "kind": "review-comparison",
        "comparison_id": cid,
        "asset_ids": sorted(seen_assets),
        "reviewer": reviewer,
        "manifest_path": str(out.relative_to(REPO_ROOT)),
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    print(f"  RESULT: comparison -> {out.relative_to(REPO_ROOT)}")
    return 0


# ---------------------------------------------------------------------------
# kind = publication-visual-selection
# ---------------------------------------------------------------------------

def run_publication_visual_selection(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    sid = payload.get("selection_id") or ("sel-" + now_compact())
    asset_id = payload.get("asset_id")
    print(f"[gov-vg-exec] kind=publication-visual-selection id={sid} reviewer={reviewer}")
    print(f"  asset_id={asset_id} build={payload.get('visual_publication_build_id')} "
          f"slot={payload.get('placement_slot_id')} grounding={payload.get('grounding_id')}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("SL-4: reviewer attribution required")
    if not asset_id:
        failures.append("SL-1: asset_id required")
    if not payload.get("visual_publication_build_id"):
        failures.append("SL-2: visual_publication_build_id required")
    if not payload.get("placement_slot_id"):
        failures.append("SL-2: placement_slot_id required")
    if not payload.get("grounding_id"):
        failures.append("SL-3: grounding_id required (grounding-preservation)")

    if asset_id and not failures:
        rec = find_asset_record(asset_id)
        if rec is None:
            failures.append(f"SL-1: asset_id '{asset_id}' not found in generated-assets")
        else:
            state = current_asset_state(asset_id)
            if state != "reviewer-approved":
                failures.append(f"SL-1/IN-4: asset '{asset_id}' lifecycle is '{state}', not 'reviewer-approved'")
            if rec.get("grounding_id") and payload.get("grounding_id") and \
               rec.get("grounding_id") != payload.get("grounding_id"):
                failures.append(
                    f"SL-3: grounding_id mismatch (asset.grounding_id='{rec.get('grounding_id')}' "
                    f"vs selection.grounding_id='{payload.get('grounding_id')}')"
                )

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(sid, "publication-selection-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN: publication-visual-selection well-formed.")
        return 0

    manifest = {
        "schema": "publication-visual-selection-manifest/1.0",
        "constitutional_layer_index": LAYER,
        "selection_id": sid,
        "asset_id": asset_id,
        "visual_publication_build_id": payload.get("visual_publication_build_id"),
        "placement_slot_id": payload.get("placement_slot_id"),
        "grounding_id": payload.get("grounding_id"),
        "prior_selection_id": payload.get("prior_selection_id"),
        "rationale": payload.get("rationale", ""),
        "reviewer": reviewer,
        "created_at_iso": now_iso(),
        "append_only": True,
    }
    out = write_collision_safe_json(PUBLICATION_VISUAL_SELECTIONS_DIR, sid, manifest)
    append_event("publication-selection-events", {
        "event_id": "pse-" + now_compact(),
        "kind": "publication-visual-selection",
        "selection_id": sid,
        "asset_id": asset_id,
        "visual_publication_build_id": payload.get("visual_publication_build_id"),
        "placement_slot_id": payload.get("placement_slot_id"),
        "grounding_id": payload.get("grounding_id"),
        "reviewer": reviewer,
        "manifest_path": str(out.relative_to(REPO_ROOT)),
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    append_event("selection-events", {
        "event_id": "sle-" + now_compact(),
        "kind": "selection",
        "selection_id": sid,
        "asset_id": asset_id,
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    print(f"  RESULT: selection recorded -> {out.relative_to(REPO_ROOT)}")
    return 0


# ---------------------------------------------------------------------------
# kind = visual-supersedence
# ---------------------------------------------------------------------------

def run_visual_supersedence(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    spid = payload.get("supersedence_id") or ("sps-" + now_compact())
    pred_id = payload.get("predecessor_asset_id")
    succ_id = payload.get("successor_asset_id")
    reason = payload.get("reason")
    grounding_shift = bool(payload.get("grounding_shift"))
    print(f"[gov-vg-exec] kind=visual-supersedence id={spid} reviewer={reviewer}")
    print(f"  predecessor={pred_id} successor={succ_id} grounding_shift={grounding_shift}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("SP-1: reviewer attribution required")
    if not pred_id:
        failures.append("SP-1: predecessor_asset_id required")
    if not succ_id:
        failures.append("SP-1: successor_asset_id required")
    if pred_id and succ_id and pred_id == succ_id:
        failures.append("SP-7: predecessor must differ from successor")
    if not reason:
        failures.append("SP-1: reason required")

    pred = find_asset_record(pred_id) if pred_id else None
    succ = find_asset_record(succ_id) if succ_id else None
    if pred_id and pred is None:
        failures.append(f"SP-1: predecessor '{pred_id}' not found")
    if succ_id and succ is None:
        failures.append(f"SP-1: successor '{succ_id}' not found")

    if pred is not None:
        pstate = current_asset_state(pred_id)
        if pstate not in {"publication-selected", "reviewer-approved"}:
            failures.append(f"SP-2: predecessor lifecycle is '{pstate}', must be publication-selected|reviewer-approved")
    if succ is not None:
        sstate = current_asset_state(succ_id)
        if sstate != "reviewer-approved":
            failures.append(f"SP-3: successor lifecycle is '{sstate}', must be reviewer-approved")

    if pred is not None and succ is not None and not grounding_shift:
        if pred.get("grounding_id") != succ.get("grounding_id"):
            failures.append(
                f"SP-4: grounding_id mismatch (predecessor='{pred.get('grounding_id')}' vs "
                f"successor='{succ.get('grounding_id')}'); set grounding_shift=true with attestation to override"
            )

    if pred is not None and succ is not None:
        if pred.get("asset_kind") == "oem" and succ.get("asset_kind") == "generated":
            if not payload.get("oem_to_generated_attestation"):
                failures.append("SP-5: OEM -> generated supersedence requires oem_to_generated_attestation (reviewer-attested)")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(spid, "supersedence-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN: visual-supersedence well-formed.")
        return 0

    manifest = {
        "schema": "visual-supersedence-manifest/1.0",
        "constitutional_layer_index": LAYER,
        "supersedence_id": spid,
        "predecessor_asset_id": pred_id,
        "successor_asset_id": succ_id,
        "reason": reason,
        "grounding_shift": grounding_shift,
        "oem_to_generated_attestation": payload.get("oem_to_generated_attestation"),
        "reviewer": reviewer,
        "created_at_iso": now_iso(),
        "append_only": True,
    }
    out = write_collision_safe_json(VISUAL_SUPERSEDENCE_DIR, spid, manifest)
    append_event("supersedence-events", {
        "event_id": "spe-" + now_compact(),
        "kind": "visual-supersedence",
        "supersedence_id": spid,
        "predecessor_asset_id": pred_id,
        "successor_asset_id": succ_id,
        "reviewer": reviewer,
        "manifest_path": str(out.relative_to(REPO_ROOT)),
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    print(f"  RESULT: supersedence recorded -> {out.relative_to(REPO_ROOT)}")
    return 0


# ---------------------------------------------------------------------------
# kind = generation-session
# ---------------------------------------------------------------------------

def run_generation_session(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    action = payload.get("action")
    sid = payload.get("session_id")
    print(f"[gov-vg-exec] kind=generation-session action={action} reviewer={reviewer}")
    print(f"  session_id={sid} from={payload.get('from_state')} to={payload.get('to_state')}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("GS-1: reviewer attribution required")
    if action not in {"open", "transition"}:
        failures.append("GS: action must be 'open' or 'transition'")

    if action == "open":
        sid = sid or ("ses-" + now_compact())
        existing = current_session_state(sid)
        if existing is not None:
            failures.append(f"GS: session '{sid}' already exists (state='{existing}')")
    elif action == "transition":
        if not sid:
            failures.append("GS: session_id required for transition")
        elif not payload.get("from_state") or not payload.get("to_state"):
            failures.append("GS: from_state and to_state required")
        else:
            edge = (payload.get("from_state"), payload.get("to_state"))
            if edge not in SESSION_EDGES:
                failures.append(f"GS: illegal transition {edge[0]} -> {edge[1]}")
            actual = current_session_state(sid)
            if actual is None:
                failures.append(f"GS: session '{sid}' not found")
            elif actual != payload.get("from_state"):
                failures.append(f"GS-STATE: declared from_state '{payload.get('from_state')}' != actual '{actual}'")
            if actual in SESSION_TERMINAL:
                failures.append(f"GS: terminal state '{actual}' is immutable")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(sid or "unknown", "session-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN: generation-session well-formed.")
        return 0

    if action == "open":
        manifest = {
            "schema": "generation-session-manifest/1.0",
            "constitutional_layer_index": LAYER,
            "session_id": sid,
            "canonical_product_id": payload.get("canonical_product_id"),
            "rationale": payload.get("rationale", ""),
            "reviewer": reviewer,
            "opened_at_iso": now_iso(),
            "initial_state": "open",
            "append_only": True,
        }
        out = write_collision_safe_json(GENERATION_SESSIONS_DIR, sid, manifest)
        append_event("generation-session-events", {
            "event_id": "gse-" + now_compact(),
            "kind": "open",
            "session_id": sid,
            "to_state": "open",
            "reviewer": reviewer,
            "manifest_path": str(out.relative_to(REPO_ROOT)),
            "occurred_at_iso": now_iso(),
            "append_only": True,
        })
        print(f"  RESULT: session opened -> {out.relative_to(REPO_ROOT)}")
        return 0

    # transition
    append_event("generation-session-events", {
        "event_id": "gse-" + now_compact(),
        "kind": "transition",
        "session_id": sid,
        "from_state": payload.get("from_state"),
        "to_state": payload.get("to_state"),
        "rationale": payload.get("rationale", ""),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    print(f"  RESULT: session transitioned ({payload.get('from_state')} -> {payload.get('to_state')})")
    return 0


# ---------------------------------------------------------------------------
# kind = asset-lifecycle-transition
# ---------------------------------------------------------------------------

def run_asset_lifecycle_transition(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    asset_id = payload.get("asset_id")
    fr = payload.get("from_state")
    to = payload.get("to_state")
    print(f"[gov-vg-exec] kind=asset-lifecycle-transition asset_id={asset_id} reviewer={reviewer}")
    print(f"  {fr} -> {to}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("LC-1: reviewer attribution required")
    if not asset_id:
        failures.append("LC: asset_id required")
    if (fr, to) not in LIFECYCLE_EDGES:
        failures.append(f"LC: illegal transition {fr} -> {to}")
    actual = current_asset_state(asset_id) if asset_id else None
    if asset_id and actual is None:
        failures.append(f"LC: asset '{asset_id}' has no recorded state (register first)")
    elif actual is not None and actual != fr:
        failures.append(f"LC-STATE: declared from_state '{fr}' != actual '{actual}'")
    if actual in LIFECYCLE_TERMINAL:
        failures.append(f"LC-2: terminal state '{actual}' is immutable")

    if asset_id and to == "publication-selected":
        rec = find_asset_record(asset_id)
        if rec is None:
            failures.append(f"LC-3: asset '{asset_id}' not found")
        else:
            if not rec.get("grounding_id"):
                failures.append("LC-3/IN-3: asset missing grounding_id (grounding-preservation)")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(asset_id or "unknown", "lifecycle-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN: lifecycle transition well-formed.")
        return 0

    append_event("variant-lineage-events", {
        "event_id": "vle-" + now_compact(),
        "kind": "lifecycle-transition",
        "asset_id": asset_id,
        "from_state": fr,
        "to_state": to,
        "reasoning_chain": list(payload.get("reasoning_chain") or []),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })

    if to == "rejected":
        write_collision_safe_json(REJECTED_ASSETS_DIR, asset_id, {
            "asset_id": asset_id, "rejected_at_iso": now_iso(), "reviewer": reviewer,
            "reasoning_chain": list(payload.get("reasoning_chain") or []),
        })
    elif to == "deprecated":
        write_collision_safe_json(DEPRECATED_ASSETS_DIR, asset_id, {
            "asset_id": asset_id, "deprecated_at_iso": now_iso(), "reviewer": reviewer,
            "reasoning_chain": list(payload.get("reasoning_chain") or []),
        })
    elif to == "reviewer-approved":
        write_collision_safe_json(REVIEWER_APPROVALS_DIR, asset_id, {
            "asset_id": asset_id, "approved_at_iso": now_iso(), "reviewer": reviewer,
            "reasoning_chain": list(payload.get("reasoning_chain") or []),
        })

    print(f"  RESULT: transitioned ({fr} -> {to})")
    return 0


# ---------------------------------------------------------------------------
# kind = visual-integrity
# ---------------------------------------------------------------------------

def run_visual_integrity(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    iid = payload.get("integrity_check_id") or ("intc-" + now_compact())
    target_ids = list(payload.get("target_asset_ids") or [])
    scope = payload.get("scope") or "all"
    print(f"[gov-vg-exec] kind=visual-integrity id={iid} reviewer={reviewer}")
    print(f"  scope={scope} targets={len(target_ids)}")

    if reviewer == "UNATTRIBUTED":
        print("  FAIL : IN: reviewer attribution required")
        if confirm:
            emit_audit(iid, "integrity-precheck-failure", "block",
                       "reviewer attribution required", reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    findings: list[dict] = []
    asset_ids: list[str] = []
    if scope == "all" and not target_ids:
        if GENERATED_ASSETS_DIR.exists():
            seen: set[str] = set()
            for p in sorted(GENERATED_ASSETS_DIR.glob("*.json")):
                try:
                    d = load_json(p)
                except Exception:
                    findings.append({"asset_id": None, "kind": "manifest-parse-error", "severity": "block",
                                     "message": f"unparseable manifest {p.name}"})
                    continue
                aid = d.get("asset_id")
                if aid and aid not in seen:
                    seen.add(aid)
                    asset_ids.append(aid)
    else:
        asset_ids = target_ids

    for aid in asset_ids:
        rec = find_asset_record(aid)
        if rec is None:
            findings.append({"asset_id": aid, "kind": "missing-record", "severity": "block",
                             "message": f"asset '{aid}' not found"})
            continue
        if not rec.get("asset_sha256") or len(rec.get("asset_sha256")) != 64:
            findings.append({"asset_id": aid, "kind": "missing-sha256", "severity": "block",
                             "message": "asset record missing valid sha256"})
        if rec.get("asset_kind") == "generated":
            if not rec.get("prompt_revision_id"):
                findings.append({"asset_id": aid, "kind": "missing-prompt-revision", "severity": "block",
                                 "message": "generated asset missing prompt_revision_id"})
            if not rec.get("grounding_id"):
                findings.append({"asset_id": aid, "kind": "missing-grounding", "severity": "block",
                                 "message": "generated asset missing grounding_id"})
        sp = rec.get("source_provenance") or {}
        tp = sp.get("target_path") or ""
        if tp and attempts_overwrite_forbidden(tp):
            findings.append({"asset_id": aid, "kind": "forbidden-target-path", "severity": "block",
                             "message": f"target_path '{tp}' attempts forbidden destination"})

    blocking = [f for f in findings if f.get("severity") == "block"]
    print(f"  findings: {len(findings)} ({len(blocking)} blocking)")

    if not confirm:
        print("  DRY-RUN: integrity check complete; no events appended.")
        return 0 if not blocking else 1

    append_event("visual-integrity-events", {
        "event_id": "ive-" + now_compact(),
        "kind": "visual-integrity",
        "integrity_check_id": iid,
        "scope": scope,
        "target_asset_ids": asset_ids,
        "findings": findings,
        "blocking_count": len(blocking),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    print("  RESULT: integrity event recorded")
    return 0 if not blocking else 1


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

DISPATCH = {
    "generation-request": run_generation_request,
    "generated-asset-register": run_generated_asset_register,
    "review-comparison": run_review_comparison,
    "publication-visual-selection": run_publication_visual_selection,
    "visual-supersedence": run_visual_supersedence,
    "generation-session": run_generation_session,
    "asset-lifecycle-transition": run_asset_lifecycle_transition,
    "visual-integrity": run_visual_integrity,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 50 — governed visual generation executor (layer 43).")
    parser.add_argument("--kind", required=True, choices=sorted(DISPATCH))
    parser.add_argument("--request", required=True, help="Path to a governed-fs-operation-request/1.0 JSON file. Use '-' or '/dev/stdin' to read stdin.")
    parser.add_argument("--confirm", action="store_true", help="Required to mutate. Without --confirm, runs in dry-run mode.")
    args = parser.parse_args(argv)

    raw = sys.stdin.read() if args.request in {"-", "/dev/stdin"} else Path(args.request).read_text(encoding="utf-8")
    try:
        request = json.loads(raw)
    except Exception as exc:
        print(f"FAIL: request JSON parse error: {exc}")
        return 2

    if request.get("schema") != SCHEMA:
        print(f"FAIL: request schema must be '{SCHEMA}' (got '{request.get('schema')}')")
        return 2

    handler = DISPATCH[args.kind]
    return handler(request, args.confirm)


if __name__ == "__main__":
    raise SystemExit(main())
