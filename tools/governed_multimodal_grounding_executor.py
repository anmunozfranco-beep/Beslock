"""
Phase 49 — Governed multimodal grounding & visual publication CLI executor (layer 42).

Reviewer-invoked. Foreground. Deterministic. Append-only. Fail-closed.
NO daemon. NO watcher. NO LLM. NO ML. NO probabilistic visual matching.
NO autonomous image generation. NO cloud / SaaS. Stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
GROUNDING_DRAFTS_ROOT = OC_ROOT / "grounding-drafts"
PROMPT_DRAFTS_ROOT = OC_ROOT / "prompt-drafts"
VISUAL_PUBLICATION_BUILDS_ROOT = OC_ROOT / "visual-publication-builds"
VISUAL_ASSET_LEDGER_ROOT = OC_ROOT / "visual-asset-ledger"

LAYER = 42
SCHEMA = "governed-fs-operation-request/1.0"

GROUNDING_KINDS = {
    "procedural-step", "troubleshooting-flow", "specification-field",
    "warning", "installation-sequence", "operational-state",
}
GROUNDING_CONFIDENCE = {"reviewer-approved", "review-required", "unresolved"}
IMAGE_ROLES = {
    "contextual", "procedural", "warning", "troubleshooting",
    "specification", "orientation", "escalation-support", "comparison-support",
}

VISUAL_ASSET_STATES = {
    "candidate", "grounded", "review-required", "reviewer-approved",
    "publication-ready", "superseded", "deprecated",
}
VISUAL_ASSET_TERMINAL = {"superseded", "deprecated"}
VISUAL_ASSET_EDGES = {
    ("candidate", "grounded"),
    ("grounded", "review-required"),
    ("review-required", "reviewer-approved"),
    ("review-required", "candidate"),
    ("reviewer-approved", "publication-ready"),
    ("reviewer-approved", "review-required"),
    ("publication-ready", "superseded"),
    ("publication-ready", "deprecated"),
    ("superseded", "deprecated"),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


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


def current_visual_asset_state(image_id: str) -> str | None:
    store_path = RUNTIME_MANIFESTS_ROOT / "visual-asset-lifecycle-events" / "_event-store.json"
    if not store_path.exists():
        return None
    last = None
    for e in load_json(store_path).get("events", []):
        if e.get("image_id") == image_id:
            last = e.get("to_state")
    return last


# ---------------------------------------------------------------------------
# kind = grounding
# ---------------------------------------------------------------------------

def run_grounding(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    grounding_id = payload.get("grounding_id") or ("grd-" + now_compact())
    image_ids = payload.get("image_ids") or []
    grounding_kind = payload.get("grounding_kind")
    confidence_state = payload.get("confidence_state") or "review-required"

    print(f"[gov-mm-exec] kind=grounding grounding_id={grounding_id} reviewer={reviewer}")
    print(f"  image_ids={len(image_ids)} kind={grounding_kind} confidence={confidence_state}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("GR-9: reviewer attribution required")
    if not image_ids:
        failures.append("GR-1: at least one image_id required")
    if not payload.get("grounded_target_id"):
        failures.append("GR-1: grounded_target_id required")
    if grounding_kind not in GROUNDING_KINDS:
        failures.append(f"GR-2: invalid grounding_kind '{grounding_kind}'")
    if not payload.get("synthesis_id"):
        failures.append("GR-7: synthesis_id required")
    if confidence_state not in GROUNDING_CONFIDENCE:
        failures.append(f"GR-6: invalid confidence_state '{confidence_state}'")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(grounding_id, "grounding-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN: grounding well-formed.")
        return 0

    manifest = {
        "schema": "multimodal-grounding-manifest/1.0",
        "constitutional_layer_index": LAYER,
        "grounding_id": grounding_id,
        "synthesis_id": payload.get("synthesis_id"),
        "canonical_product_id": payload.get("canonical_product_id"),
        "grounding_kind": grounding_kind,
        "grounded_target_id": payload.get("grounded_target_id"),
        "image_ids": list(image_ids),
        "evidence_ids": list(payload.get("evidence_ids") or []),
        "rationale": payload.get("rationale", ""),
        "confidence_state": confidence_state,
        "prior_grounding_id": payload.get("prior_grounding_id"),
        "reviewer": reviewer,
        "created_at_iso": now_iso(),
        "append_only": True,
    }
    target = write_collision_safe_json(GROUNDING_DRAFTS_ROOT, grounding_id, manifest)
    append_event("grounding-events", {
        "grounding_event_id": "grd-ev-" + grounding_id + "-" + now_compact(),
        "grounding_id": grounding_id,
        "synthesis_id": payload.get("synthesis_id"),
        "grounding_kind": grounding_kind,
        "image_count": len(image_ids),
        "confidence_state": confidence_state,
        "manifest_path": str(target.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(grounding_id, "grounding-recorded", "info",
               f"grounding {grounding_id} recorded", reviewer,
               {"manifest_path": str(target.relative_to(REPO_ROOT))})
    print(f"  RESULT: grounding manifest -> {target.relative_to(REPO_ROOT)}")
    return 0


# ---------------------------------------------------------------------------
# kind = supportive-image-mapping
# ---------------------------------------------------------------------------

def run_supportive_mapping(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    image_id = payload.get("image_id")
    role = payload.get("role")

    print(f"[gov-mm-exec] kind=supportive-image-mapping image_id={image_id} role={role} reviewer={reviewer}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("missing reviewer")
    if not image_id:
        failures.append("image_id required")
    if role not in IMAGE_ROLES:
        failures.append(f"SI-1: invalid role '{role}'")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(image_id or "no-img", "supportive-mapping-precheck-failure",
                       "block", "; ".join(failures), reviewer, {"request": request})
        return 2

    if not confirm:
        print("  DRY-RUN: mapping well-formed.")
        return 0

    mapping_id = payload.get("mapping_id") or ("map-" + image_id + "-" + now_compact())
    append_event("supportive-image-mapping-events", {
        "mapping_event_id": "map-ev-" + mapping_id + "-" + now_compact(),
        "mapping_id": mapping_id,
        "image_id": image_id,
        "role": role,
        "applies_to_sections": list(payload.get("applies_to_sections") or []),
        "canonical_product_ids": list(payload.get("canonical_product_ids") or []),
        "evidence_ids": list(payload.get("evidence_ids") or []),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(mapping_id, "supportive-mapping-recorded", "info",
               f"image {image_id} mapped to role {role}", reviewer, {})
    print("  RESULT: mapping recorded")
    return 0


# ---------------------------------------------------------------------------
# kind = prompt
# ---------------------------------------------------------------------------

def run_prompt(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    prompt_id = payload.get("prompt_id") or ("prm-" + now_compact())

    print(f"[gov-mm-exec] kind=prompt prompt_id={prompt_id} reviewer={reviewer}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("missing reviewer")
    if not payload.get("grounding_id"):
        failures.append("PG-3: grounding_id required (no detached prompts)")
    if not payload.get("canonical_product_id"):
        failures.append("PG-1: canonical_product_id required")
    if not payload.get("synthesis_id"):
        failures.append("PG-1: synthesis_id required")
    text = payload.get("prompt_text")
    if not isinstance(text, str) or not text.strip():
        failures.append("PG-5: prompt_text required (reviewer-authored)")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(prompt_id, "prompt-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        return 2

    if not confirm:
        print("  DRY-RUN: prompt well-formed.")
        return 0

    manifest = {
        "schema": "prompt-manifest/1.0",
        "constitutional_layer_index": LAYER,
        "prompt_id": prompt_id,
        "grounding_id": payload.get("grounding_id"),
        "canonical_product_id": payload.get("canonical_product_id"),
        "synthesis_id": payload.get("synthesis_id"),
        "intent": payload.get("intent", ""),
        "constraints": list(payload.get("constraints") or []),
        "prompt_text": text,
        "prior_prompt_id": payload.get("prior_prompt_id"),
        "reviewer": reviewer,
        "created_at_iso": now_iso(),
        "append_only": True,
    }
    target = write_collision_safe_json(PROMPT_DRAFTS_ROOT, prompt_id, manifest)
    append_event("prompt-events", {
        "prompt_event_id": "prm-ev-" + prompt_id + "-" + now_compact(),
        "prompt_id": prompt_id,
        "grounding_id": payload.get("grounding_id"),
        "manifest_path": str(target.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    if payload.get("prior_prompt_id"):
        append_event("prompt-revision-events", {
            "revision_event_id": "prr-" + prompt_id + "-" + now_compact(),
            "prompt_id": prompt_id,
            "prior_prompt_id": payload.get("prior_prompt_id"),
            "reviewer": reviewer,
            "occurred_at_iso": now_iso(),
            "append_only": True,
        })
    emit_audit(prompt_id, "prompt-recorded", "info",
               f"prompt {prompt_id} recorded", reviewer,
               {"manifest_path": str(target.relative_to(REPO_ROOT))})
    print(f"  RESULT: prompt manifest -> {target.relative_to(REPO_ROOT)}")
    return 0


# ---------------------------------------------------------------------------
# kind = visual-troubleshooting
# ---------------------------------------------------------------------------

def run_visual_troubleshooting(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    flow_id = payload.get("flow_id")

    print(f"[gov-mm-exec] kind=visual-troubleshooting flow_id={flow_id} reviewer={reviewer}")

    if reviewer == "UNATTRIBUTED" or not flow_id:
        print("  FAIL : missing reviewer or flow_id")
        if confirm:
            emit_audit(flow_id or "no-flow", "vt-precheck-failure", "block",
                       "missing reviewer/flow_id", reviewer, {"request": request})
        return 2

    if not confirm:
        print("  DRY-RUN: visual troubleshooting binding well-formed.")
        return 0

    binding_id = payload.get("binding_id") or ("vtb-" + flow_id + "-" + now_compact())
    append_event("visual-troubleshooting-events", {
        "vt_event_id": "vt-ev-" + binding_id + "-" + now_compact(),
        "binding_id": binding_id,
        "flow_id": flow_id,
        "synthesis_id": payload.get("synthesis_id"),
        "symptom_visuals": list(payload.get("symptom_visuals") or []),
        "escalation_visuals": list(payload.get("escalation_visuals") or []),
        "warning_visuals": list(payload.get("warning_visuals") or []),
        "visual_unresolved": bool(payload.get("visual_unresolved")),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(binding_id, "visual-troubleshooting-recorded", "info",
               f"flow {flow_id} bound to visuals", reviewer, {})
    print("  RESULT: visual troubleshooting recorded")
    return 0


# ---------------------------------------------------------------------------
# kind = procedural-continuity
# ---------------------------------------------------------------------------

def _detect_gaps(steps: list) -> list[int]:
    if not steps:
        return []
    max_idx = max((int(s.get("step_index") or 0)) for s in steps)
    present = {int(s["step_index"]) for s in steps if s.get("image_id") and s.get("step_index") is not None}
    return [i for i in range(1, max_idx + 1) if i not in present]


def run_continuity(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    publication_build_id = payload.get("publication_build_id")
    steps = payload.get("steps") or []
    orphans = list(payload.get("orphan_image_ids") or [])
    broken = list(payload.get("broken_lineage_image_ids") or [])
    accepted = set(payload.get("reviewer_accepted_gaps") or [])

    gaps = _detect_gaps(steps)
    blocking_gaps = [g for g in gaps if g not in accepted]
    blocking = bool(blocking_gaps or orphans or broken)

    print(f"[gov-mm-exec] kind=procedural-continuity build={publication_build_id} reviewer={reviewer}")
    print(f"  gaps={gaps} blocking_gaps={blocking_gaps} orphans={len(orphans)} broken_lineage={len(broken)}")

    if reviewer == "UNATTRIBUTED" or not publication_build_id:
        print("  FAIL : missing reviewer or publication_build_id")
        if confirm:
            emit_audit(publication_build_id or "no-build", "continuity-precheck-failure",
                       "block", "missing reviewer/build", reviewer, {"request": request})
        return 2

    if not confirm:
        print("  DRY-RUN: continuity check well-formed.")
        return 0

    continuity_id = payload.get("continuity_id") or ("cont-" + publication_build_id + "-" + now_compact())
    append_event("procedural-continuity-events", {
        "continuity_event_id": "cont-ev-" + continuity_id + "-" + now_compact(),
        "continuity_id": continuity_id,
        "publication_build_id": publication_build_id,
        "gaps": gaps,
        "blocking_gaps": blocking_gaps,
        "orphan_image_ids": orphans,
        "broken_lineage_image_ids": broken,
        "reviewer_accepted_gaps": sorted(accepted),
        "blocks_publication_ready": blocking,
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(continuity_id, "continuity-recorded",
               "block" if blocking else "info",
               f"continuity check (blocks_publication_ready={blocking})",
               reviewer, {"publication_build_id": publication_build_id})
    print(f"  RESULT: continuity recorded (blocks_publication_ready={blocking})")
    return 0


# ---------------------------------------------------------------------------
# kind = visual-publication-build
# ---------------------------------------------------------------------------

def _render_placement_html(p: dict) -> str:
    if not p.get("image_id"):
        return "<div class='oc-visual-missing' data-reason='visual-not-available'>visual-not-available</div>\n"
    role = p.get("role") or "contextual"
    trust = p.get("trust_tier") or ""
    grounding_id = p.get("grounding_id") or ""
    image_id = p.get("image_id")
    src = p.get("src") or ""
    alt = p.get("alt") or ""
    evidence = ",".join(p.get("evidence_ids") or [])
    return (
        f"<figure class='oc-visual' data-grounding-id='{escape(grounding_id)}' "
        f"data-image-id='{escape(image_id)}' data-role='{escape(role)}' "
        f"data-evidence='{escape(evidence)}'>"
        f"<img src='{escape(src)}' alt='{escape(alt)}' loading='lazy'>"
        f"<figcaption><span class='oc-visual-role'>{escape(role)}</span> "
        f"<span class='oc-visual-trust' data-tier='{escape(trust)}'>{escape(trust)}</span></figcaption>"
        f"</figure>\n"
    )


def run_visual_publication_build(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    synthesis_id = payload.get("synthesis_id")
    manual_id = payload.get("manual_id") or "manual"
    build_id = payload.get("build_id") or ("vpb-" + manual_id + "-" + now_compact())
    placements = payload.get("placements") or []
    output_formats = payload.get("output_formats") or ["html", "json"]

    print(f"[gov-mm-exec] kind=visual-publication-build build_id={build_id} reviewer={reviewer}")
    print(f"  synthesis_id={synthesis_id} manual_id={manual_id} placements={len(placements)} formats={output_formats}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("missing reviewer")
    if not synthesis_id:
        failures.append("VP-6: synthesis_id required")
    if not all(f in {"html", "json"} for f in output_formats):
        failures.append("VP-5: only html and json supported")
    target_dir = VISUAL_PUBLICATION_BUILDS_ROOT / "candidate" / build_id
    if target_dir.exists():
        failures.append(f"VP-2: build_id directory already exists ({target_dir.relative_to(REPO_ROOT)})")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(build_id, "visual-publication-build-precheck-failure",
                       "block", "; ".join(failures), reviewer, {"request": request})
        return 2

    if not confirm:
        print(f"  DRY-RUN: would write {target_dir.relative_to(REPO_ROOT)}/")
        return 0

    target_dir.mkdir(parents=True, exist_ok=True)
    body = "".join(_render_placement_html(p) for p in placements) or "<p><em>no placements</em></p>\n"
    html_doc = (
        "<!doctype html><html lang='es-CO'><head><meta charset='utf-8'>"
        f"<title>{escape(manual_id)}</title>"
        "<link rel='stylesheet' href='../../../assets/exec/exec.css'></head>"
        f"<body><header><h1>{escape(manual_id)}</h1>"
        f"<p>Visual build: {escape(build_id)} — synthesis: {escape(str(synthesis_id))} — reviewer: {escape(reviewer)}</p>"
        "</header><main>" + body + "</main></body></html>\n"
    )
    json_doc = {
        "schema": "visual-publication-manual/1.0",
        "constitutional_layer_index": LAYER,
        "manual_id": manual_id,
        "build_id": build_id,
        "synthesis_id": synthesis_id,
        "canonical_product_id": payload.get("canonical_product_id"),
        "reviewer": reviewer,
        "placements": placements,
        "deterministic": True,
        "writes_live_tree": False,
        "generated_at_iso": now_iso(),
    }
    if "html" in output_formats:
        write_text(target_dir / "manual.html", html_doc)
    if "json" in output_formats:
        write_json(target_dir / "manual.json", json_doc)

    sha = hashlib.sha256(json.dumps(json_doc, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    manifest = {
        "schema": "visual-publication-build-manifest/1.0",
        "constitutional_layer_index": LAYER,
        "build_id": build_id,
        "synthesis_id": synthesis_id,
        "manual_id": manual_id,
        "reviewer": reviewer,
        "output_formats": output_formats,
        "outputs": {
            "html": str((target_dir / "manual.html").relative_to(REPO_ROOT)) if "html" in output_formats else None,
            "json": str((target_dir / "manual.json").relative_to(REPO_ROOT)) if "json" in output_formats else None,
        },
        "json_sha256": sha,
        "placement_count": len(placements),
        "writes_live_tree": False,
        "deterministic": True,
        "generated_at_iso": now_iso(),
    }
    write_json(target_dir / "visual_publication_manifest.json", manifest)

    append_event("visual-publication-build-events", {
        "vpb_event_id": "vpb-ev-" + build_id + "-" + now_compact(),
        "build_id": build_id,
        "synthesis_id": synthesis_id,
        "manual_id": manual_id,
        "json_sha256": sha,
        "placement_count": len(placements),
        "outputs": manifest["outputs"],
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(build_id, "visual-publication-build-recorded", "info",
               f"build {build_id} written", reviewer, {"json_sha256": sha})
    print(f"  RESULT: visual publication build -> {target_dir.relative_to(REPO_ROOT)}")
    return 0


# ---------------------------------------------------------------------------
# kind = visual-asset-lifecycle-transition
# ---------------------------------------------------------------------------

def run_visual_lifecycle(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    image_id = payload.get("image_id")
    from_state = payload.get("from_state")
    to_state = payload.get("to_state")

    print(f"[gov-mm-exec] kind=visual-asset-lifecycle-transition image_id={image_id} reviewer={reviewer}")
    print(f"  {from_state} -> {to_state}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("VL-1: reviewer attribution required")
    if not image_id:
        failures.append("missing image_id")
    if to_state not in VISUAL_ASSET_STATES:
        failures.append(f"VL: unknown to_state '{to_state}'")
    if (from_state, to_state) not in VISUAL_ASSET_EDGES:
        failures.append(f"VL: illegal transition {from_state} -> {to_state}")
    actual = current_visual_asset_state(image_id) if image_id else None
    if actual is not None and actual != from_state:
        failures.append(f"VL-STATE: declared from_state '{from_state}' != actual '{actual}'")
    if actual in VISUAL_ASSET_TERMINAL:
        failures.append(f"VL-4: image is in terminal state '{actual}'")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(image_id or "no-img", "visual-lifecycle-precheck-failure",
                       "block", "; ".join(failures), reviewer, {"request": request})
        return 2

    if not confirm:
        print("  DRY-RUN: transition well-formed.")
        return 0

    append_event("visual-asset-lifecycle-events", {
        "lifecycle_event_id": "vl-" + image_id + "-" + now_compact(),
        "image_id": image_id,
        "from_state": from_state,
        "to_state": to_state,
        "reasoning_chain": list(payload.get("reasoning_chain") or []),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    # Append a per-image ledger entry too.
    ledger_dir = VISUAL_ASSET_LEDGER_ROOT / image_id
    ledger_dir.mkdir(parents=True, exist_ok=True)
    write_collision_safe_json(ledger_dir, "ledger", {
        "schema": "visual-asset-ledger-entry/1.0",
        "image_id": image_id,
        "from_state": from_state,
        "to_state": to_state,
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
    })
    emit_audit(image_id, "visual-lifecycle-transitioned", "info",
               f"{from_state} -> {to_state}", reviewer, {})
    print(f"  RESULT: transitioned ({from_state} -> {to_state})")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Governed multimodal grounding & visual publication CLI executor (phase 49, layer 42)."
    )
    p.add_argument("--kind", required=True, choices=[
        "grounding", "supportive-image-mapping", "prompt",
        "visual-publication-build", "visual-troubleshooting",
        "procedural-continuity", "visual-asset-lifecycle-transition",
    ])
    p.add_argument("--request", required=True)
    p.add_argument("--confirm", action="store_true")
    args = p.parse_args()

    req_path = Path(args.request).expanduser().resolve()
    if not req_path.exists():
        print(f"[gov-mm-exec] FATAL: request file not found: {req_path}", file=sys.stderr)
        return 4
    request = load_json(req_path)
    if request.get("schema") != SCHEMA:
        print(f"[gov-mm-exec] FATAL: unsupported schema {request.get('schema')}", file=sys.stderr)
        return 4

    dispatch = {
        "grounding": run_grounding,
        "supportive-image-mapping": run_supportive_mapping,
        "prompt": run_prompt,
        "visual-publication-build": run_visual_publication_build,
        "visual-troubleshooting": run_visual_troubleshooting,
        "procedural-continuity": run_continuity,
        "visual-asset-lifecycle-transition": run_visual_lifecycle,
    }
    return dispatch[args.kind](request, args.confirm)


if __name__ == "__main__":
    sys.exit(main())
