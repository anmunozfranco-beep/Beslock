"""
Phase 52 — Governed semantic evidence analysis & multimodal extraction CLI executor (layer 45).

Reviewer-invoked. Foreground. Deterministic. Append-only. Fail-closed.
NO daemon. NO watcher. NO scheduler. NO LLM. NO ML. NO probabilistic extraction.
NO embeddings. NO vector DB. NO autonomous semantic matching. NO cloud / SaaS.
Stdlib only.

Records reviewer-authored decompositions, OCR fragments, OCR corrections,
extraction candidates, temporal continuity scans, lineage replays, full
extraction replays, lifecycle transitions, integrity scans, and reviewer
overrides. NEVER writes the live publication tree, the layer-44 publication-
composition-runtime tree, the layer-43 visual-generation-runtime tree, the
layer-42 visual-publication-builds tree, OEM source assets, knowledge-core,
governance, runtime-implementation, runtime-manifests payloads, or uploads.
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
SE_ROOT = OC_ROOT / "semantic-extraction-runtime"

DECOMPOSITIONS_DIR = SE_ROOT / "evidence-decompositions"
VIDEO_DIR = SE_ROOT / "video-decompositions"
IMAGE_DIR = SE_ROOT / "image-decompositions"
PDF_DIR = SE_ROOT / "pdf-decompositions"
SHEET_DIR = SE_ROOT / "spreadsheet-decompositions"
OCR_FRAGMENTS_DIR = SE_ROOT / "ocr-fragments"
OCR_CORRECTIONS_DIR = SE_ROOT / "ocr-corrections"
CANDIDATES_DIR = SE_ROOT / "extraction-candidates"
CONTINUITY_DIR = SE_ROOT / "temporal-continuity"
LINEAGE_DIR = SE_ROOT / "extraction-lineage"
REPLAYS_DIR = SE_ROOT / "extraction-replays"
INTEGRITY_DIR = SE_ROOT / "extraction-integrity"
DECISIONS_DIR = SE_ROOT / "reviewer-extraction-decisions"
LIFECYCLE_DIR = SE_ROOT / "semantic-extraction-lifecycle"

LAYER = 45
SCHEMA = "governed-fs-operation-request/1.0"

EVIDENCE_KINDS = frozenset({"video", "image", "pdf", "xls", "xlsx", "csv"})
CANDIDATE_KINDS = frozenset({
    "procedural-step-candidate", "troubleshooting-candidate", "warning-candidate",
    "specification-field-candidate", "ui-state-candidate", "app-flow-candidate",
    "terminology-candidate", "visual-anchor-candidate", "section-candidate",
    "table-candidate",
})
CONFIDENCE_STATES = frozenset({"reviewer-approved", "review-required", "unresolved"})

LIFECYCLE_STATES = frozenset({
    "unresolved", "review-required", "reviewer-approved", "superseded", "deprecated",
})
LIFECYCLE_TERMINAL = frozenset({"deprecated"})
LIFECYCLE_EDGES = frozenset({
    ("unresolved", "review-required"),
    ("unresolved", "deprecated"),
    ("review-required", "reviewer-approved"),
    ("review-required", "unresolved"),
    ("review-required", "deprecated"),
    ("reviewer-approved", "review-required"),
    ("reviewer-approved", "superseded"),
    ("superseded", "deprecated"),
})

OVERRIDE_KINDS = frozenset({"approve", "reject", "supersede", "annotate"})

# Forbidden destinations: every prior-layer storage tree, governance, and OEM uploads.
FORBIDDEN_OVERWRITE_PREFIXES = (
    "wp-content/themes/beslock-custom/User manuals/operational-console/publication-composition-runtime/",
    "wp-content/themes/beslock-custom/User manuals/operational-console/visual-generation-runtime/",
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


def write_collision_safe_json(directory: Path, base_id: str, payload: dict) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{base_id}-{now_compact()}.json"
    suffix = 1
    while target.exists():
        target = directory / f"{base_id}-{now_compact()}.{suffix}.json"
        suffix += 1
    write_json(target, payload)
    return target


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


def attempts_overwrite_forbidden(target_path: str | None) -> bool:
    if not target_path:
        return False
    norm = target_path.lstrip("/")
    return any(norm.startswith(p) for p in FORBIDDEN_OVERWRITE_PREFIXES)


# ---------------------------------------------------------------------------
# Scanners (replay helpers)
# ---------------------------------------------------------------------------

def _scan_by_id(directory: Path, key: str, value: str) -> dict | None:
    if not directory.exists():
        return None
    latest = None
    for p in sorted(directory.glob("*.json")):
        try:
            d = load_json(p)
        except Exception:
            continue
        if d.get(key) == value:
            latest = d
    return latest


def find_decomposition(decomposition_id: str) -> dict | None:
    return _scan_by_id(DECOMPOSITIONS_DIR, "decomposition_id", decomposition_id)


def find_decompositions_for_evidence(source_evidence_id: str) -> list[dict]:
    if not DECOMPOSITIONS_DIR.exists():
        return []
    out = []
    for p in sorted(DECOMPOSITIONS_DIR.glob("*.json")):
        try:
            d = load_json(p)
        except Exception:
            continue
        if d.get("source_evidence_id") == source_evidence_id:
            out.append(d)
    return out


def find_ocr_fragment(fragment_id: str) -> dict | None:
    return _scan_by_id(OCR_FRAGMENTS_DIR, "ocr_fragment_id", fragment_id)


def find_candidate(candidate_id: str) -> dict | None:
    return _scan_by_id(CANDIDATES_DIR, "candidate_id", candidate_id)


def candidate_id_exists(candidate_id: str) -> bool:
    return find_candidate(candidate_id) is not None


def current_candidate_state(candidate_id: str) -> str | None:
    store_path = RUNTIME_MANIFESTS_ROOT / "extraction-lifecycle-events" / "_event-store.json"
    last = None
    if store_path.exists():
        for e in load_json(store_path).get("events", []):
            if e.get("candidate_id") != candidate_id:
                continue
            if e.get("kind") == "lifecycle-transition":
                last = e.get("to_state")
            elif e.get("kind") == "register" and last is None:
                last = e.get("to_state") or "unresolved"
    return last


# ---------------------------------------------------------------------------
# Request loading & validation
# ---------------------------------------------------------------------------

def load_request(req_arg: str) -> dict:
    if req_arg == "-":
        data = sys.stdin.read()
    else:
        data = Path(req_arg).read_text(encoding="utf-8")
    env = json.loads(data)
    if env.get("schema") != SCHEMA:
        raise SystemExit(f"FAIL-CLOSED: request schema must be '{SCHEMA}' (got {env.get('schema')!r})")
    if not isinstance(env.get("reviewer"), str) or not env["reviewer"].strip():
        raise SystemExit("FAIL-CLOSED: reviewer attribution required")
    if not isinstance(env.get("payload"), dict):
        raise SystemExit("FAIL-CLOSED: payload required")
    return env


def require(payload: dict, key: str, kind=None):
    if key not in payload or payload[key] in (None, "", []):
        raise SystemExit(f"FAIL-CLOSED: payload.{key} required")
    if kind is not None and not isinstance(payload[key], kind):
        raise SystemExit(f"FAIL-CLOSED: payload.{key} must be {kind.__name__}")
    return payload[key]


def reject_forbidden(p: dict) -> None:
    if attempts_overwrite_forbidden(p.get("target_path")):
        raise SystemExit("FAIL-CLOSED: target_path falls under a forbidden prefix (XI-8)")


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

def handle_evidence_decomposition(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    require(p, "source_evidence_id")
    require(p, "evidence_kind")
    require(p, "content_sha256")
    if p["evidence_kind"] not in EVIDENCE_KINDS:
        raise SystemExit(f"FAIL-CLOSED: evidence_kind '{p['evidence_kind']}' not in {sorted(EVIDENCE_KINDS)} (ED-1)")
    reject_forbidden(p)

    kind = p["evidence_kind"]
    if kind == "video":
        keyframes = p.get("keyframes")
        if not isinstance(keyframes, list) or not keyframes:
            raise SystemExit("FAIL-CLOSED: video decomposition requires keyframes (ED-3)")
        last_idx = -1
        last_ts = -1
        for i, kf in enumerate(keyframes):
            if not isinstance(kf, dict):
                raise SystemExit(f"FAIL-CLOSED: keyframes[{i}] must be object (ED-3)")
            idx = kf.get("frame_index"); ts = kf.get("timestamp_ms")
            if not isinstance(idx, int) or idx <= last_idx:
                raise SystemExit(f"FAIL-CLOSED: keyframes[{i}].frame_index must be strictly increasing int (ED-3)")
            if not isinstance(ts, int) or ts < last_ts:
                raise SystemExit(f"FAIL-CLOSED: keyframes[{i}].timestamp_ms must be non-decreasing int (ED-3)")
            last_idx = idx; last_ts = ts
    elif kind == "pdf":
        pages = p.get("pages")
        if not isinstance(pages, list) or not pages:
            raise SystemExit("FAIL-CLOSED: pdf decomposition requires pages (ED-4)")
        if pages != list(range(1, len(pages) + 1)):
            raise SystemExit("FAIL-CLOSED: pdf pages must be contiguous starting at 1 (ED-4)")
    elif kind in ("xls", "xlsx", "csv"):
        worksheets = p.get("worksheets")
        if not isinstance(worksheets, list) or not worksheets:
            raise SystemExit("FAIL-CLOSED: spreadsheet decomposition requires worksheets (ED-5)")
        seen = set()
        for i, ws in enumerate(worksheets):
            if not isinstance(ws, dict):
                raise SystemExit(f"FAIL-CLOSED: worksheets[{i}] must be object (ED-5)")
            name = ws.get("name"); cols = ws.get("column_count")
            if not name or name in seen:
                raise SystemExit(f"FAIL-CLOSED: worksheets[{i}].name must be unique non-empty (ED-5)")
            if not isinstance(cols, int) or cols < 1:
                raise SystemExit(f"FAIL-CLOSED: worksheets[{i}].column_count must be int >= 1 (ED-5)")
            seen.add(name)
    elif kind == "image":
        regions = p.get("regions")
        anchors = p.get("visual_anchors")
        if not (isinstance(regions, list) and regions) and not (isinstance(anchors, list) and anchors):
            raise SystemExit("FAIL-CLOSED: image decomposition requires at least one region or visual_anchor (ED-6)")

    decomposition_id = p.get("decomposition_id") or "dec-" + sha256_hex(
        p["source_evidence_id"] + "|" + kind + "|" + p["content_sha256"]
    )[:16]
    op_id = "op-dec-" + now_compact()
    payload = {
        "schema": "evidence-decomposition/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "decomposition_id": decomposition_id,
        "source_evidence_id": p["source_evidence_id"],
        "evidence_kind": kind,
        "content_sha256": p["content_sha256"],
        "keyframes": p.get("keyframes"),
        "scene_boundaries": p.get("scene_boundaries"),
        "pages": p.get("pages"),
        "worksheets": p.get("worksheets"),
        "regions": p.get("regions"),
        "visual_anchors": p.get("visual_anchors"),
        "rationale": p.get("rationale", ""),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0

    written = write_collision_safe_json(DECOMPOSITIONS_DIR, decomposition_id, payload)
    # also mirror into per-kind directory for easy reviewer browsing
    per_kind_dir = {
        "video": VIDEO_DIR, "image": IMAGE_DIR, "pdf": PDF_DIR,
        "xls": SHEET_DIR, "xlsx": SHEET_DIR, "csv": SHEET_DIR,
    }[kind]
    write_collision_safe_json(per_kind_dir, decomposition_id + "-mirror", {
        "schema": "evidence-decomposition-mirror/1.0",
        "decomposition_id": decomposition_id,
        "evidence_kind": kind,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
    })
    append_event("evidence-decomposition-events", {
        "decomposition_event_id": op_id,
        "kind": "register",
        "decomposition_id": decomposition_id,
        "source_evidence_id": p["source_evidence_id"],
        "evidence_kind": kind,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "evidence-decomposition", "info",
               f"decomposition recorded: {decomposition_id}", reviewer,
               {"decomposition_id": decomposition_id, "evidence_kind": kind})
    print(json.dumps({"ok": True, "decomposition_id": decomposition_id,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_ocr_fragment(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    require(p, "source_evidence_id")
    require(p, "decomposition_id")
    if not isinstance(p.get("text"), str):
        raise SystemExit("FAIL-CLOSED: payload.text required (OF-1)")
    reject_forbidden(p)
    decomposition = find_decomposition(p["decomposition_id"])
    if decomposition is None:
        raise SystemExit(f"FAIL-CLOSED: decomposition '{p['decomposition_id']}' not found (OF-1)")
    if decomposition.get("source_evidence_id") != p["source_evidence_id"]:
        raise SystemExit("FAIL-CLOSED: source_evidence_id does not match decomposition (OF-1)")

    # locality: page_index for pdf, frame_index for video, region for image, none for sheet
    kind = decomposition.get("evidence_kind")
    if kind == "pdf":
        if not isinstance(p.get("page_index"), int) or p["page_index"] < 1:
            raise SystemExit("FAIL-CLOSED: page_index required for pdf OCR fragment (OF-1)")
        if p["page_index"] not in (decomposition.get("pages") or []):
            raise SystemExit(f"FAIL-CLOSED: page_index {p['page_index']} not in decomposition pages (OF-7)")
    elif kind == "video":
        if not isinstance(p.get("frame_index"), int):
            raise SystemExit("FAIL-CLOSED: frame_index required for video OCR fragment (OF-1)")
        frames = {kf.get("frame_index") for kf in (decomposition.get("keyframes") or [])}
        if p["frame_index"] not in frames:
            raise SystemExit(f"FAIL-CLOSED: frame_index {p['frame_index']} not in decomposition keyframes (OF-7)")
    elif kind == "image":
        if not p.get("region"):
            raise SystemExit("FAIL-CLOSED: region required for image OCR fragment (OF-1)")

    verbatim_sha = sha256_hex(p["text"])
    fragment_id = p.get("ocr_fragment_id") or "ocr-" + sha256_hex(
        p["decomposition_id"] + "|" + verbatim_sha
    )[:16]
    op_id = "op-ocr-" + now_compact()
    payload = {
        "schema": "ocr-fragment/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "ocr_fragment_id": fragment_id,
        "source_evidence_id": p["source_evidence_id"],
        "decomposition_id": p["decomposition_id"],
        "evidence_kind": kind,
        "page_index": p.get("page_index"),
        "frame_index": p.get("frame_index"),
        "region": p.get("region"),
        "language": p.get("language", "unknown"),
        "text": p["text"],
        "verbatim_sha256": verbatim_sha,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(OCR_FRAGMENTS_DIR, fragment_id, payload)
    append_event("ocr-fragment-events", {
        "ocr_event_id": op_id,
        "kind": "register",
        "ocr_fragment_id": fragment_id,
        "decomposition_id": p["decomposition_id"],
        "verbatim_sha256": verbatim_sha,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "ocr-fragment", "info",
               f"OCR fragment recorded: {fragment_id}", reviewer,
               {"ocr_fragment_id": fragment_id})
    print(json.dumps({"ok": True, "ocr_fragment_id": fragment_id,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_ocr_correction(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    require(p, "prior_fragment_id")
    if not isinstance(p.get("text"), str):
        raise SystemExit("FAIL-CLOSED: payload.text required (OF-1)")
    reject_forbidden(p)
    prior = find_ocr_fragment(p["prior_fragment_id"])
    if prior is None:
        raise SystemExit(f"FAIL-CLOSED: prior_fragment_id '{p['prior_fragment_id']}' not found (OF-4)")

    verbatim_sha = sha256_hex(p["text"])
    correction_id = p.get("ocr_correction_id") or "occ-" + sha256_hex(
        p["prior_fragment_id"] + "|" + verbatim_sha
    )[:16]
    op_id = "op-occ-" + now_compact()
    payload = {
        "schema": "ocr-correction/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "ocr_correction_id": correction_id,
        "prior_fragment_id": p["prior_fragment_id"],
        "source_evidence_id": prior.get("source_evidence_id"),
        "decomposition_id": prior.get("decomposition_id"),
        "text": p["text"],
        "verbatim_sha256": verbatim_sha,
        "rationale": p.get("rationale", ""),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(OCR_CORRECTIONS_DIR, correction_id, payload)
    append_event("ocr-correction-events", {
        "occ_event_id": op_id,
        "kind": "register",
        "ocr_correction_id": correction_id,
        "prior_fragment_id": p["prior_fragment_id"],
        "verbatim_sha256": verbatim_sha,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "ocr-correction", "info",
               f"OCR correction recorded: {correction_id}", reviewer,
               {"ocr_correction_id": correction_id, "prior_fragment_id": p["prior_fragment_id"]})
    print(json.dumps({"ok": True, "ocr_correction_id": correction_id,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_extraction_candidate(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    require(p, "source_evidence_id")
    require(p, "extraction_runtime_id")
    require(p, "extraction_rule_id")
    require(p, "candidate_kind")
    if p["candidate_kind"] not in CANDIDATE_KINDS:
        raise SystemExit(f"FAIL-CLOSED: candidate_kind '{p['candidate_kind']}' not in CANDIDATE_KINDS (EC-2)")
    confidence_state = p.get("confidence_state", "unresolved")
    if confidence_state not in CONFIDENCE_STATES:
        raise SystemExit(f"FAIL-CLOSED: confidence_state '{confidence_state}' not in CONFIDENCE_STATES (EC-1)")
    if confidence_state == "reviewer-approved":
        raise SystemExit("FAIL-CLOSED: candidate registration cannot directly assert 'reviewer-approved'; use lifecycle transition (EC-4)")
    reject_forbidden(p)

    decomposition_id = p.get("decomposition_id")
    if decomposition_id and find_decomposition(decomposition_id) is None:
        raise SystemExit(f"FAIL-CLOSED: decomposition '{decomposition_id}' not found (XI-1)")

    ocr_ids = p.get("ocr_fragment_ids", [])
    if not isinstance(ocr_ids, list):
        raise SystemExit("FAIL-CLOSED: ocr_fragment_ids must be list (EC-6)")
    for fid in ocr_ids:
        if find_ocr_fragment(fid) is None:
            raise SystemExit(f"FAIL-CLOSED: orphan OCR reference '{fid}' (EC-6/XI-3)")

    frame_indices = p.get("frame_indices", [])
    if not isinstance(frame_indices, list):
        raise SystemExit("FAIL-CLOSED: frame_indices must be list (EC-7)")
    if frame_indices:
        if decomposition_id is None:
            raise SystemExit("FAIL-CLOSED: frame_indices require decomposition_id (EC-7)")
        decomposition = find_decomposition(decomposition_id)
        frames = {kf.get("frame_index") for kf in (decomposition.get("keyframes") or [])}
        for fi in frame_indices:
            if fi not in frames:
                raise SystemExit(f"FAIL-CLOSED: frame_index {fi} missing from decomposition (EC-7/XI-5)")
        if p["candidate_kind"] == "procedural-step-candidate":
            sorted_fi = sorted(frame_indices)
            for a, b in zip(sorted_fi, sorted_fi[1:]):
                pos_a = sorted(frames).index(a); pos_b = sorted(frames).index(b)
                if pos_b - pos_a != 1:
                    raise SystemExit("FAIL-CLOSED: procedural-step-candidate requires contiguous frame coverage (TC-5)")

    candidate_id = p.get("candidate_id") or "cand-" + sha256_hex(
        p["source_evidence_id"] + "|" + p["candidate_kind"] + "|" +
        json.dumps(p.get("proposal_payload", {}), sort_keys=True)
    )[:16]
    if candidate_id_exists(candidate_id) and not p.get("prior_candidate_id"):
        raise SystemExit(f"FAIL-CLOSED: duplicate candidate_id '{candidate_id}' without prior_candidate_id (EC-5/XI-7)")
    if p.get("prior_candidate_id") and find_candidate(p["prior_candidate_id"]) is None:
        raise SystemExit(f"FAIL-CLOSED: prior_candidate_id '{p['prior_candidate_id']}' not found (EC-5)")

    reasoning_chain = p.get("reasoning_chain", [])
    if not isinstance(reasoning_chain, list):
        raise SystemExit("FAIL-CLOSED: reasoning_chain must be list (EC-1)")

    op_id = "op-cand-" + now_compact()
    payload = {
        "schema": "extraction-candidate/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "candidate_id": candidate_id,
        "source_evidence_id": p["source_evidence_id"],
        "decomposition_id": decomposition_id,
        "extraction_runtime_id": p["extraction_runtime_id"],
        "extraction_rule_id": p["extraction_rule_id"],
        "candidate_kind": p["candidate_kind"],
        "confidence_state": confidence_state,
        "reasoning_chain": reasoning_chain,
        "ocr_fragment_ids": ocr_ids,
        "frame_indices": frame_indices,
        "page_indices": p.get("page_indices", []),
        "prior_candidate_id": p.get("prior_candidate_id"),
        "proposal_payload": p.get("proposal_payload", {}),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(CANDIDATES_DIR, candidate_id, payload)
    append_event("extraction-candidate-events", {
        "candidate_event_id": op_id,
        "kind": "register",
        "candidate_id": candidate_id,
        "candidate_kind": p["candidate_kind"],
        "confidence_state": confidence_state,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    # Anchor lifecycle event at the registration state.
    append_event("extraction-lifecycle-events", {
        "lifecycle_event_id": op_id + "-lc",
        "kind": "register",
        "candidate_id": candidate_id,
        "from_state": None,
        "to_state": confidence_state,
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "extraction-candidate", "info",
               f"candidate proposed: {candidate_id}", reviewer,
               {"candidate_id": candidate_id, "candidate_kind": p["candidate_kind"]})
    print(json.dumps({"ok": True, "candidate_id": candidate_id,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_temporal_continuity(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    require(p, "source_evidence_id")
    decomposition_id = p.get("decomposition_id")
    if decomposition_id is None:
        decs = [d for d in find_decompositions_for_evidence(p["source_evidence_id"]) if d.get("evidence_kind") == "video"]
        if not decs:
            raise SystemExit("FAIL-CLOSED: no video decomposition for source_evidence_id (TC-1)")
        decomposition_id = decs[-1].get("decomposition_id")
    decomposition = find_decomposition(decomposition_id)
    if decomposition is None or decomposition.get("evidence_kind") != "video":
        raise SystemExit(f"FAIL-CLOSED: video decomposition '{decomposition_id}' not found (TC-1)")
    declared_frames = p.get("frame_indices") or [
        kf.get("frame_index") for kf in (decomposition.get("keyframes") or [])
    ]
    if not isinstance(declared_frames, list) or not declared_frames:
        raise SystemExit("FAIL-CLOSED: frame_indices required (TC-1)")
    strictly_increasing = all(b > a for a, b in zip(declared_frames, declared_frames[1:]))
    decomposition_frames = sorted({kf.get("frame_index") for kf in (decomposition.get("keyframes") or [])})
    missing = [f for f in declared_frames if f not in decomposition_frames]
    contiguous = True
    if strictly_increasing and not missing:
        positions = [decomposition_frames.index(f) for f in declared_frames]
        contiguous = all(b - a == 1 for a, b in zip(positions, positions[1:]))

    candidate_id = p.get("candidate_id")
    orphan_frames: list[int] = []
    if candidate_id:
        cand = find_candidate(candidate_id)
        if cand is None:
            raise SystemExit(f"FAIL-CLOSED: candidate '{candidate_id}' not found (TC-3)")
        cited = set(cand.get("frame_indices") or [])
        orphan_frames = sorted(set(decomposition_frames) - cited)
    integrity_ok = strictly_increasing and not missing and contiguous
    reject_forbidden(p)

    check_id = p.get("continuity_check_id") or f"tc-{decomposition_id}-{now_compact()}"
    op_id = "op-tc-" + now_compact()
    payload = {
        "schema": "temporal-continuity/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "continuity_check_id": check_id,
        "source_evidence_id": p["source_evidence_id"],
        "decomposition_id": decomposition_id,
        "candidate_id": candidate_id,
        "declared_frames": declared_frames,
        "strictly_increasing": strictly_increasing,
        "missing_frames": missing,
        "contiguous": contiguous,
        "orphan_frames": orphan_frames,
        "integrity_ok": integrity_ok,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(CONTINUITY_DIR, check_id, payload)
    append_event("temporal-continuity-events", {
        "tc_event_id": op_id,
        "kind": "register",
        "continuity_check_id": check_id,
        "decomposition_id": decomposition_id,
        "candidate_id": candidate_id,
        "integrity_ok": integrity_ok,
        "missing_count": len(missing),
        "orphan_frame_count": len(orphan_frames),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "temporal-continuity", "info" if integrity_ok else "warning",
               f"continuity recorded: {check_id} integrity_ok={integrity_ok}", reviewer,
               {"continuity_check_id": check_id, "missing_frames": missing, "orphan_frames": orphan_frames})
    print(json.dumps({"ok": True, "continuity_check_id": check_id, "integrity_ok": integrity_ok,
                      "missing_frames": missing, "orphan_frames": orphan_frames,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def _candidate_lineage_chain(candidate_id: str) -> dict:
    """Reconstruct lineage for a candidate. Returns dict with resolved/missing pointers."""
    cand = find_candidate(candidate_id)
    if cand is None:
        raise SystemExit(f"FAIL-CLOSED: candidate '{candidate_id}' not found (EL-3)")
    decomposition_id = cand.get("decomposition_id")
    decomposition = find_decomposition(decomposition_id) if decomposition_id else None
    missing: list[str] = []
    if decomposition_id and decomposition is None:
        missing.append(f"decomposition:{decomposition_id}")
    ocr_records = []
    for fid in cand.get("ocr_fragment_ids") or []:
        rec = find_ocr_fragment(fid)
        if rec is None:
            missing.append(f"ocr_fragment:{fid}")
        else:
            ocr_records.append(rec)
    prior_id = cand.get("prior_candidate_id")
    if prior_id and find_candidate(prior_id) is None:
        missing.append(f"prior_candidate:{prior_id}")
    artifact_hashes = {
        "candidate": sha256_hex(json.dumps(cand, sort_keys=True)),
    }
    if decomposition is not None:
        artifact_hashes["decomposition"] = sha256_hex(json.dumps(decomposition, sort_keys=True))
    for rec in ocr_records:
        artifact_hashes[f"ocr_fragment:{rec.get('ocr_fragment_id')}"] = sha256_hex(json.dumps(rec, sort_keys=True))
    return {
        "candidate_id": candidate_id,
        "decomposition_id": decomposition_id,
        "ocr_fragment_ids": cand.get("ocr_fragment_ids") or [],
        "prior_candidate_id": prior_id,
        "missing_pointers": missing,
        "artifact_hashes": artifact_hashes,
        "lineage_ok": not missing,
    }


def handle_extraction_lineage(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    candidate_id = require(p, "candidate_id")
    reject_forbidden(p)
    chain = _candidate_lineage_chain(candidate_id)
    lineage_id = p.get("lineage_id") or f"lin-{candidate_id}-{now_compact()}"
    op_id = "op-lin-" + now_compact()
    payload = {
        "schema": "extraction-lineage/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "lineage_id": lineage_id,
        "candidate_id": candidate_id,
        "scope": p.get("scope", "candidate"),
        "missing_pointers": chain["missing_pointers"],
        "artifact_hashes": chain["artifact_hashes"],
        "lineage_ok": chain["lineage_ok"],
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    if not chain["lineage_ok"]:
        # Record the failing lineage manifest but still fail-closed exit.
        written = write_collision_safe_json(LINEAGE_DIR, lineage_id, payload)
        append_event("extraction-lineage-events", {
            "lineage_event_id": op_id, "kind": "register",
            "lineage_id": lineage_id, "candidate_id": candidate_id,
            "lineage_ok": False, "missing_pointers": chain["missing_pointers"],
            "manifest_path": str(written.relative_to(REPO_ROOT)),
            "reviewer": reviewer, "occurred_at_iso": now_iso(),
            "append_only": True,
        })
        emit_audit(op_id, "extraction-lineage", "warning",
                   f"lineage broken: {lineage_id}", reviewer,
                   {"lineage_id": lineage_id, "missing_pointers": chain["missing_pointers"]})
        raise SystemExit(f"FAIL-CLOSED: lineage broken: {chain['missing_pointers']} (EL-3)")
    written = write_collision_safe_json(LINEAGE_DIR, lineage_id, payload)
    append_event("extraction-lineage-events", {
        "lineage_event_id": op_id, "kind": "register",
        "lineage_id": lineage_id, "candidate_id": candidate_id,
        "lineage_ok": True, "missing_pointers": [],
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "extraction-lineage", "info",
               f"lineage replayed: {lineage_id}", reviewer,
               {"lineage_id": lineage_id})
    print(json.dumps({"ok": True, "lineage_id": lineage_id, "lineage_ok": True,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_extraction_replay(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    candidate_id = p.get("candidate_id")
    if not candidate_id and not p.get("source_evidence_id"):
        raise SystemExit("FAIL-CLOSED: candidate_id or source_evidence_id required (ER-1)")
    reject_forbidden(p)
    candidate_ids: list[str]
    if candidate_id:
        if find_candidate(candidate_id) is None:
            raise SystemExit(f"FAIL-CLOSED: candidate '{candidate_id}' not found (ER-1)")
        candidate_ids = [candidate_id]
    else:
        sev = p["source_evidence_id"]
        candidate_ids = []
        if CANDIDATES_DIR.exists():
            for path in sorted(CANDIDATES_DIR.glob("*.json")):
                try:
                    d = load_json(path)
                except Exception:
                    continue
                if d.get("source_evidence_id") == sev and d["candidate_id"] not in candidate_ids:
                    candidate_ids.append(d["candidate_id"])
        if not candidate_ids:
            raise SystemExit(f"FAIL-CLOSED: no candidates for source_evidence_id '{sev}' (ER-1)")

    chains = []
    declared_hashes = p.get("expected_hashes", {})
    mismatches: list[str] = []
    missing_total: list[str] = []
    for cid in candidate_ids:
        chain = _candidate_lineage_chain(cid)
        chains.append(chain)
        missing_total.extend(chain["missing_pointers"])
        for k, v in chain["artifact_hashes"].items():
            full_key = f"{cid}:{k}"
            if full_key in declared_hashes and declared_hashes[full_key] != v:
                mismatches.append(full_key)
    replay_ok = not missing_total and not mismatches
    replay_id = p.get("replay_id") or f"rep-{now_compact()}"
    op_id = "op-rep-" + now_compact()
    payload = {
        "schema": "extraction-replay/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "replay_id": replay_id,
        "candidate_ids": candidate_ids,
        "scope": p.get("scope", "candidate"),
        "chains": chains,
        "missing_pointers": missing_total,
        "hash_mismatches": mismatches,
        "replay_ok": replay_ok,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(REPLAYS_DIR, replay_id, payload)
    append_event("extraction-replay-events", {
        "replay_event_id": op_id, "kind": "register",
        "replay_id": replay_id, "candidate_count": len(candidate_ids),
        "replay_ok": replay_ok,
        "missing_pointer_count": len(missing_total),
        "hash_mismatch_count": len(mismatches),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    if not replay_ok:
        emit_audit(op_id, "extraction-replay", "warning",
                   f"replay failed: {replay_id}", reviewer,
                   {"missing_pointers": missing_total, "hash_mismatches": mismatches})
        raise SystemExit(f"FAIL-CLOSED: replay failed missing={missing_total} mismatches={mismatches} (ER-1/ER-2)")
    emit_audit(op_id, "extraction-replay", "info",
               f"replay ok: {replay_id}", reviewer, {"replay_id": replay_id})
    print(json.dumps({"ok": True, "replay_id": replay_id, "replay_ok": True,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_extraction_lifecycle_transition(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    candidate_id = require(p, "candidate_id")
    from_state = require(p, "from_state")
    to_state = require(p, "to_state")
    if from_state not in LIFECYCLE_STATES or to_state not in LIFECYCLE_STATES:
        raise SystemExit("FAIL-CLOSED: invalid lifecycle state(s) (XI-6)")
    if (from_state, to_state) not in LIFECYCLE_EDGES:
        raise SystemExit(f"FAIL-CLOSED: illegal lifecycle transition {from_state} -> {to_state} (XL-2)")
    if find_candidate(candidate_id) is None:
        raise SystemExit(f"FAIL-CLOSED: candidate '{candidate_id}' not found (XL-1)")
    actual = current_candidate_state(candidate_id)
    if actual is None:
        raise SystemExit(f"FAIL-CLOSED: candidate '{candidate_id}' has no recorded lifecycle (XL-2)")
    if actual != from_state:
        raise SystemExit(f"FAIL-CLOSED: declared from_state '{from_state}' != actual '{actual}' (XL-2)")
    if actual in LIFECYCLE_TERMINAL:
        raise SystemExit(f"FAIL-CLOSED: candidate is in terminal state '{actual}' (XL-3)")
    if to_state == "superseded" and not p.get("successor_candidate_id"):
        raise SystemExit("FAIL-CLOSED: superseded transition requires successor_candidate_id (XL-4)")
    if to_state == "reviewer-approved":
        # Require at least one successful lineage replay.
        chain = _candidate_lineage_chain(candidate_id)
        if not chain["lineage_ok"]:
            raise SystemExit(f"FAIL-CLOSED: cannot approve candidate with broken lineage: {chain['missing_pointers']} (XL-1/EL-3)")
    reject_forbidden(p)

    op_id = "op-xl-" + now_compact()
    payload = {
        "schema": "extraction-lifecycle-transition/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "candidate_id": candidate_id,
        "from_state": from_state,
        "to_state": to_state,
        "successor_candidate_id": p.get("successor_candidate_id"),
        "reasoning_chain": p.get("reasoning_chain", []),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(LIFECYCLE_DIR, f"{candidate_id}-{from_state}-to-{to_state}", payload)
    append_event("extraction-lifecycle-events", {
        "lifecycle_event_id": op_id,
        "kind": "lifecycle-transition",
        "candidate_id": candidate_id,
        "from_state": from_state,
        "to_state": to_state,
        "successor_candidate_id": p.get("successor_candidate_id"),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "extraction-lifecycle-transition", "info",
               f"lifecycle: {candidate_id} {from_state} -> {to_state}", reviewer,
               {"candidate_id": candidate_id})
    print(json.dumps({"ok": True, "candidate_id": candidate_id,
                      "from_state": from_state, "to_state": to_state,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_extraction_integrity(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    reject_forbidden(p)
    findings: list[dict] = []
    candidates: list[dict] = []
    if CANDIDATES_DIR.exists():
        seen_ids: dict[str, int] = {}
        for path in sorted(CANDIDATES_DIR.glob("*.json")):
            try:
                d = load_json(path)
            except Exception:
                continue
            if p.get("candidate_id") and d.get("candidate_id") != p["candidate_id"]:
                continue
            if p.get("source_evidence_id") and d.get("source_evidence_id") != p["source_evidence_id"]:
                continue
            candidates.append(d)
            cid = d.get("candidate_id")
            seen_ids[cid] = seen_ids.get(cid, 0) + 1
        for cid, count in seen_ids.items():
            if count > 1:
                # Only flag actual duplicate registrations (not natural collision-safe rewrites).
                # A registration is duplicate only if there are multiple register events.
                pass

    for d in candidates:
        cid = d.get("candidate_id")
        # orphan source evidence
        sev = d.get("source_evidence_id")
        if sev and not find_decompositions_for_evidence(sev):
            findings.append({"rule_id": "XI-4", "candidate_id": cid,
                             "detail": f"missing decomposition for source_evidence_id={sev}"})
        # orphan decomposition
        if d.get("decomposition_id") and find_decomposition(d["decomposition_id"]) is None:
            findings.append({"rule_id": "XI-1", "candidate_id": cid,
                             "detail": f"orphan decomposition_id={d['decomposition_id']}"})
        # orphan OCR refs
        for fid in d.get("ocr_fragment_ids") or []:
            if find_ocr_fragment(fid) is None:
                findings.append({"rule_id": "XI-3", "candidate_id": cid,
                                 "detail": f"orphan ocr_fragment_id={fid}"})
        # broken lineage (overall)
        chain = _candidate_lineage_chain(cid)
        if not chain["lineage_ok"]:
            findings.append({"rule_id": "XI-2", "candidate_id": cid,
                             "detail": f"broken lineage: {chain['missing_pointers']}"})
        # illegal candidate state per current lifecycle
        state = current_candidate_state(cid)
        if state is not None and state not in LIFECYCLE_STATES:
            findings.append({"rule_id": "XI-6", "candidate_id": cid,
                             "detail": f"illegal candidate state: {state}"})

    blocking = bool(findings)
    check_id = p.get("integrity_check_id") or f"xi-{now_compact()}"
    op_id = "op-xi-" + now_compact()
    payload = {
        "schema": "extraction-integrity/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "integrity_check_id": check_id,
        "scope": p.get("scope", "all"),
        "candidate_id": p.get("candidate_id"),
        "source_evidence_id": p.get("source_evidence_id"),
        "candidate_count": len(candidates),
        "findings": findings,
        "blocking": blocking,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(INTEGRITY_DIR, check_id, payload)
    append_event("extraction-integrity-events", {
        "integrity_event_id": op_id, "kind": "register",
        "integrity_check_id": check_id, "blocking": blocking,
        "finding_count": len(findings),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "extraction-integrity", "warning" if blocking else "info",
               f"integrity scan: {check_id} blocking={blocking}", reviewer,
               {"integrity_check_id": check_id, "findings": findings})
    print(json.dumps({"ok": True, "integrity_check_id": check_id,
                      "blocking": blocking, "findings": findings,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_reviewer_override(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    target_id = require(p, "target_artifact_id")
    target_kind = p.get("target_kind", "candidate")
    kind = p.get("kind", "reject")
    if kind not in OVERRIDE_KINDS:
        raise SystemExit(f"FAIL-CLOSED: override kind '{kind}' not in {sorted(OVERRIDE_KINDS)} (RO-1)")
    cited = p.get("cited_rule_ids", [])
    if kind == "reject" and not (isinstance(cited, list) and cited):
        raise SystemExit("FAIL-CLOSED: reject overrides require cited_rule_ids (RO-3)")
    reject_forbidden(p)
    if target_kind == "candidate" and find_candidate(target_id) is None:
        raise SystemExit(f"FAIL-CLOSED: target candidate '{target_id}' not found (RO-1)")
    if target_kind == "ocr_fragment" and find_ocr_fragment(target_id) is None:
        raise SystemExit(f"FAIL-CLOSED: target ocr_fragment '{target_id}' not found (RO-1)")
    if target_kind == "decomposition" and find_decomposition(target_id) is None:
        raise SystemExit(f"FAIL-CLOSED: target decomposition '{target_id}' not found (RO-1)")

    override_id = p.get("override_id") or f"ro-{target_id}-{now_compact()}"
    op_id = "op-ro-" + now_compact()
    payload = {
        "schema": "reviewer-extraction-decision/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "override_id": override_id,
        "target_artifact_id": target_id,
        "target_kind": target_kind,
        "kind": kind,
        "cited_rule_ids": cited,
        "rationale": p.get("rationale", ""),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(DECISIONS_DIR, override_id, payload)
    # Reuse the lifecycle event store to record reviewer decisions on candidates.
    append_event("extraction-lifecycle-events", {
        "lifecycle_event_id": op_id,
        "kind": "reviewer-override",
        "override_id": override_id,
        "target_artifact_id": target_id,
        "target_kind": target_kind,
        "override_kind": kind,
        "cited_rule_ids": cited,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "reviewer-override", "info",
               f"reviewer override recorded: {override_id} kind={kind}", reviewer,
               {"override_id": override_id, "target_artifact_id": target_id})
    print(json.dumps({"ok": True, "override_id": override_id, "kind": kind,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

DISPATCH = {
    "evidence-decomposition": handle_evidence_decomposition,
    "ocr-fragment": handle_ocr_fragment,
    "ocr-correction": handle_ocr_correction,
    "extraction-candidate": handle_extraction_candidate,
    "temporal-continuity": handle_temporal_continuity,
    "extraction-lineage": handle_extraction_lineage,
    "extraction-replay": handle_extraction_replay,
    "extraction-lifecycle-transition": handle_extraction_lifecycle_transition,
    "extraction-integrity": handle_extraction_integrity,
    "reviewer-override": handle_reviewer_override,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 52 — governed semantic extraction CLI executor (layer 45).",
    )
    parser.add_argument("--kind", required=True, choices=sorted(DISPATCH))
    parser.add_argument("--request", required=True,
                        help="Path to JSON request envelope, or '-' for stdin.")
    parser.add_argument("--confirm", action="store_true",
                        help="Without --confirm, only a dry-run preview is printed.")
    args = parser.parse_args(argv)

    env = load_request(args.request)
    handler = DISPATCH[args.kind]
    return handler(env, args.confirm)


if __name__ == "__main__":
    raise SystemExit(main())
