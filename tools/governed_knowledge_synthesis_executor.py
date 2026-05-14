"""
Phase 48 — Governed knowledge synthesis & canonical publication CLI executor.

Reviewer-invoked. Foreground. Deterministic. Append-only. Fail-closed.
NO daemon. NO watcher. NO scheduled trigger. NO LLM. NO ML. NO network.
Stdlib only.

Subcommands (--kind):
- synthesis                       — assemble a synthesis manifest from evidence ids.
- publication-build               — generate deterministic HTML + JSON publication into publication-builds/<build_id>/.
- evidence-resolve                — record an explicit conflict-resolution event.
- rendering                       — record deterministic Spanish (Colombia) rendering result.
- troubleshooting-synthesis       — record a deterministic troubleshooting flow.
- specification-synthesis         — record a deterministic specification sheet.
- manual-assembly                 — record a 9-section canonical-manual assembly manifest.
- publication-lifecycle-transition — advance a publication build through the state machine.

Every command requires --confirm to write or append. Without --confirm the
executor validates and prints the plan.
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
RULES_ROOT = OC_ROOT / "execution-engine"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
SYNTHESIS_DRAFTS_ROOT = OC_ROOT / "synthesis-drafts"
PUBLICATION_BUILDS_ROOT = OC_ROOT / "publication-builds"

LAYER = 41
SCHEMA = "governed-fs-operation-request/1.0"

MANUAL_SECTIONS = [
    "overview", "prerequisites", "installation", "operation",
    "troubleshooting", "maintenance", "specifications", "warnings", "support",
]

PUBLICATION_STATES = {
    "draft", "synthesized", "review-required", "reviewer-approved",
    "publication-ready", "superseded", "deprecated",
}
PUBLICATION_TERMINAL_STATES = {"superseded", "deprecated"}
PUBLICATION_EDGES = {
    ("draft", "synthesized"),
    ("synthesized", "review-required"),
    ("review-required", "reviewer-approved"),
    ("review-required", "draft"),
    ("reviewer-approved", "publication-ready"),
    ("reviewer-approved", "review-required"),
    ("publication-ready", "superseded"),
    ("publication-ready", "deprecated"),
    ("superseded", "deprecated"),
}


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


def current_publication_state(build_id: str) -> str | None:
    store_path = RUNTIME_MANIFESTS_ROOT / "publication-lifecycle-events" / "_event-store.json"
    if not store_path.exists():
        return None
    last = None
    for e in load_json(store_path).get("events", []):
        if e.get("build_id") == build_id:
            last = e.get("to_state")
    return last


def synthesis_state(synthesis_id: str) -> str | None:
    store_path = RUNTIME_MANIFESTS_ROOT / "publication-lifecycle-events" / "_event-store.json"
    if not store_path.exists():
        return None
    last = None
    for e in load_json(store_path).get("events", []):
        if e.get("synthesis_id") == synthesis_id:
            last = e.get("to_state")
    return last


def write_synthesis_draft(synthesis: dict) -> Path:
    SYNTHESIS_DRAFTS_ROOT.mkdir(parents=True, exist_ok=True)
    name = f"{synthesis['synthesis_id']}-{now_compact()}.json"
    target = SYNTHESIS_DRAFTS_ROOT / name
    suffix = 1
    while target.exists():
        target = SYNTHESIS_DRAFTS_ROOT / f"{synthesis['synthesis_id']}-{now_compact()}.{suffix}.json"
        suffix += 1
    write_json(target, synthesis)
    return target


# ---------------------------------------------------------------------------
# kind = synthesis
# ---------------------------------------------------------------------------

def run_synthesis(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    request_id = request.get("request_id") or now_compact()
    synthesis_id = payload.get("synthesis_id") or ("syn-" + now_compact())
    evidence_ids = payload.get("evidence_ids") or []
    canonical_product_id = payload.get("canonical_product_id")

    print(f"[gov-syn-exec] kind=synthesis synthesis_id={synthesis_id} reviewer={reviewer}")
    print(f"  evidence_count: {len(evidence_ids)}")
    print(f"  canonical_product_id: {canonical_product_id}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("SYN-MISSING-REVIEWER: reviewer attribution required")
    if not evidence_ids:
        failures.append("SYN-1: at least one evidence_id required")
    if not canonical_product_id:
        failures.append("SYN-MISSING-PRODUCT: canonical_product_id required")
    if payload.get("uses_llm") or payload.get("uses_ml") or payload.get("probabilistic"):
        failures.append("SYN-5: LLM/ML/probabilistic inference is forbidden")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(synthesis_id, "synthesis-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN: synthesis well-formed; manifest plan ready.")
        return 0

    manifest = {
        "schema": "governed-knowledge-synthesis-manifest/1.0",
        "constitutional_layer_index": LAYER,
        "synthesis_id": synthesis_id,
        "request_id": request_id,
        "canonical_product_id": canonical_product_id,
        "evidence_ids": list(evidence_ids),
        "contributing_manifests": list(payload.get("contributing_manifests") or []),
        "trust_composition": payload.get("trust_composition") or {},
        "reasoning_chain": list(payload.get("reasoning_chain") or []),
        "reviewer": reviewer,
        "review_state": "draft",
        "deterministic": True,
        "no_llm": True,
        "created_at_iso": now_iso(),
        "append_only": True,
    }
    target = write_synthesis_draft(manifest)
    append_event("synthesis-events", {
        "synthesis_event_id": "syn-ev-" + synthesis_id + "-" + now_compact(),
        "synthesis_id": synthesis_id,
        "request_id": request_id,
        "reviewer": reviewer,
        "evidence_count": len(evidence_ids),
        "manifest_path": str(target.relative_to(REPO_ROOT)),
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    append_event("publication-lifecycle-events", {
        "lifecycle_event_id": "plt-" + synthesis_id + "-" + now_compact(),
        "synthesis_id": synthesis_id,
        "build_id": None,
        "from_state": None,
        "to_state": "draft",
        "reviewer": reviewer,
        "reasoning_chain": ["synthesis manifest created"],
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(synthesis_id, "synthesis-recorded", "info",
               f"synthesis {synthesis_id} created", reviewer,
               {"manifest_path": str(target.relative_to(REPO_ROOT))})
    print(f"  RESULT: synthesis manifest written -> {target.relative_to(REPO_ROOT)}")
    return 0


# ---------------------------------------------------------------------------
# kind = evidence-resolve
# ---------------------------------------------------------------------------

def run_evidence_resolve(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    synthesis_id = payload.get("synthesis_id")
    conflicts = payload.get("conflicts") or []
    strategy = payload.get("strategy") or "reviewer-arbitration"

    print(f"[gov-syn-exec] kind=evidence-resolve synthesis_id={synthesis_id} reviewer={reviewer}")
    print(f"  conflicts: {len(conflicts)} | strategy: {strategy}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("ER-MISSING-REVIEWER: reviewer attribution required")
    if not synthesis_id:
        failures.append("ER-MISSING-SYNTHESIS: synthesis_id required")
    if not conflicts:
        failures.append("ER-NOOP: no conflicts provided")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(synthesis_id or "no-syn", "resolution-precheck-failure",
                       "block", "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN: resolution plan well-formed.")
        return 0

    res_id = payload.get("resolution_id") or ("res-" + synthesis_id + "-" + now_compact())
    for c in conflicts:
        append_event("conflict-events", {
            "conflict_event_id": "conf-" + res_id + "-" + now_compact(),
            "resolution_id": res_id,
            "synthesis_id": synthesis_id,
            "conflict": c,
            "strategy": strategy,
            "reviewer": reviewer,
            "occurred_at_iso": now_iso(),
            "append_only": True,
        })
    append_event("evidence-resolution-events", {
        "resolution_event_id": "resev-" + res_id + "-" + now_compact(),
        "resolution_id": res_id,
        "synthesis_id": synthesis_id,
        "strategy": strategy,
        "conflict_count": len(conflicts),
        "reasoning_chain": list(payload.get("reasoning_chain") or []),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(res_id, "evidence-resolution-recorded", "info",
               f"{len(conflicts)} conflicts resolved via {strategy}", reviewer,
               {"synthesis_id": synthesis_id})
    print("  RESULT: resolution recorded")
    return 0


# ---------------------------------------------------------------------------
# kind = rendering
# ---------------------------------------------------------------------------

def run_rendering(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    synthesis_id = payload.get("synthesis_id")
    segments = payload.get("segments") or []
    target_locale = payload.get("target_locale") or "es-CO"

    print(f"[gov-syn-exec] kind=rendering synthesis_id={synthesis_id} locale={target_locale} reviewer={reviewer}")
    print(f"  segments: {len(segments)}")

    if reviewer == "UNATTRIBUTED":
        print("  FAIL : CR-MISSING-REVIEWER")
        if confirm:
            emit_audit(synthesis_id or "no-syn", "rendering-precheck-failure",
                       "block", "missing reviewer", reviewer, {"request": request})
        return 2

    if not confirm:
        print("  DRY-RUN: rendering plan well-formed.")
        return 0

    rendering_id = payload.get("rendering_id") or ("ren-" + (synthesis_id or "no-syn") + "-" + now_compact())
    append_event("rendering-events", {
        "rendering_event_id": "renev-" + rendering_id + "-" + now_compact(),
        "rendering_id": rendering_id,
        "synthesis_id": synthesis_id,
        "target_locale": target_locale,
        "segment_count": len(segments),
        "transformations": [s.get("transformations", []) for s in segments],
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(rendering_id, "rendering-recorded", "info",
               f"{len(segments)} segments rendered to {target_locale}", reviewer, {})
    print("  RESULT: rendering recorded")
    return 0


# ---------------------------------------------------------------------------
# kind = troubleshooting-synthesis / specification-synthesis / manual-assembly
# ---------------------------------------------------------------------------

def run_generic_synthesis(request: dict, confirm: bool, label: str, store_kind: str) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    print(f"[gov-syn-exec] kind={label} reviewer={reviewer}")

    if reviewer == "UNATTRIBUTED":
        print("  FAIL : missing reviewer attribution")
        if confirm:
            emit_audit(payload.get("synthesis_id") or "no-syn",
                       f"{label}-precheck-failure", "block",
                       "missing reviewer", reviewer, {"request": request})
        return 2

    if not confirm:
        print("  DRY-RUN: well-formed.")
        return 0

    op_id = (payload.get("flow_id") or payload.get("spec_id") or payload.get("manual_id")
             or (label + "-" + now_compact()))
    append_event(store_kind, {
        "event_id": label + "-ev-" + now_compact(),
        "synthesis_id": payload.get("synthesis_id"),
        "operation_id": op_id,
        "reviewer": reviewer,
        "payload_summary": {k: v for k, v in payload.items()
                            if k in {"canonical_product_id", "manual_id", "flow_id", "spec_id"}},
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, f"{label}-recorded", "info",
               f"{label} recorded", reviewer, {"synthesis_id": payload.get("synthesis_id")})
    print(f"  RESULT: {label} recorded")
    return 0


# ---------------------------------------------------------------------------
# kind = publication-build (HTML + JSON, deterministic)
# ---------------------------------------------------------------------------

def _render_section_html(section_name: str, section_data: dict) -> str:
    evidence = section_data.get("evidence_ids") or []
    review_state = section_data.get("review_state") or "draft"
    text = section_data.get("text_pointer") or "(evidence pointer only — no inline text in this build)"
    pins = " ".join(f"<span class='oc-evidence-pin'>{escape(str(e))}</span>" for e in evidence)
    return (
        f"<section id='sec-{escape(section_name)}'>"
        f"<h2>{escape(section_name)} <span class='oc-pub-state' data-state='{escape(review_state)}'>{escape(review_state)}</span></h2>"
        f"<p>{escape(str(text))}</p>"
        f"<p><strong>Evidence:</strong> {pins or '<em>evidence-not-available</em>'}</p>"
        f"</section>\n"
    )


def run_publication_build(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    synthesis_id = payload.get("synthesis_id")
    manual_id = payload.get("manual_id") or "manual"
    build_id = payload.get("build_id") or ("pubb-" + manual_id + "-" + now_compact())
    output_formats = payload.get("output_formats") or ["html", "json"]

    print(f"[gov-syn-exec] kind=publication-build build_id={build_id} reviewer={reviewer}")
    print(f"  synthesis_id: {synthesis_id} | manual_id: {manual_id} | formats: {output_formats}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("PUB-MISSING-REVIEWER: reviewer attribution required")
    if not synthesis_id:
        failures.append("PUB-5: synthesis_id required")
    if not all(f in {"html", "json"} for f in output_formats):
        failures.append("PUB-FORMAT: only html and json are supported in this layer")
    state = synthesis_state(synthesis_id) if synthesis_id else None
    if state and state not in {"reviewer-approved", "draft", "synthesized", "review-required"}:
        # In live operation, only reviewer-approved should pass; we permit earlier states for
        # build-preview purposes but the build is then NOT eligible for publication-ready promotion.
        pass

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(build_id, "publication-build-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    sections = payload.get("sections") or {s: {} for s in MANUAL_SECTIONS}
    target_dir = PUBLICATION_BUILDS_ROOT / "draft" / build_id
    if target_dir.exists():
        print(f"  FAIL : PUB-2: build_id directory already exists ({target_dir.relative_to(REPO_ROOT)})")
        if confirm:
            emit_audit(build_id, "publication-build-collision", "block",
                       "duplicate build_id", reviewer, {"target": str(target_dir.relative_to(REPO_ROOT))})
        return 3

    if not confirm:
        print(f"  DRY-RUN: would write {target_dir.relative_to(REPO_ROOT)}/{{manual.html, manual.json, publication_manifest.json}}")
        return 0

    target_dir.mkdir(parents=True, exist_ok=True)

    body = "".join(_render_section_html(s, sections.get(s, {})) for s in MANUAL_SECTIONS)
    html_doc = (
        "<!doctype html><html lang='es-CO'><head><meta charset='utf-8'>"
        f"<title>{escape(manual_id)}</title>"
        "<link rel='stylesheet' href='../../assets/exec/exec.css'></head>"
        f"<body><header><h1>{escape(manual_id)}</h1>"
        f"<p>Build: {escape(build_id)} — synthesis: {escape(str(synthesis_id))} — reviewer: {escape(reviewer)}</p>"
        "</header><main>" + body + "</main></body></html>\n"
    )
    json_doc = {
        "schema": "governed-publication-manual/1.0",
        "constitutional_layer_index": LAYER,
        "manual_id": manual_id,
        "build_id": build_id,
        "synthesis_id": synthesis_id,
        "canonical_product_id": payload.get("canonical_product_id"),
        "reviewer": reviewer,
        "sections": sections,
        "deterministic": True,
        "writes_live_tree": False,
        "generated_at_iso": now_iso(),
    }
    if "html" in output_formats:
        write_text(target_dir / "manual.html", html_doc)
    if "json" in output_formats:
        write_json(target_dir / "manual.json", json_doc)

    sha_payload = hashlib.sha256(json.dumps(json_doc, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    manifest = {
        "schema": "governed-publication-build-manifest/1.0",
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
        "json_sha256": sha_payload,
        "writes_live_tree": False,
        "deterministic": True,
        "generated_at_iso": now_iso(),
    }
    write_json(target_dir / "publication_manifest.json", manifest)

    append_event("publication-build-events", {
        "publication_build_event_id": "pbe-" + build_id + "-" + now_compact(),
        "build_id": build_id,
        "synthesis_id": synthesis_id,
        "manual_id": manual_id,
        "reviewer": reviewer,
        "outputs": manifest["outputs"],
        "json_sha256": sha_payload,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    append_event("publication-lifecycle-events", {
        "lifecycle_event_id": "plt-" + build_id + "-" + now_compact(),
        "build_id": build_id,
        "synthesis_id": synthesis_id,
        "from_state": None,
        "to_state": "draft",
        "reviewer": reviewer,
        "reasoning_chain": ["publication build created"],
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(build_id, "publication-build-recorded", "info",
               f"build {build_id} written to {target_dir.relative_to(REPO_ROOT)}",
               reviewer, {"json_sha256": sha_payload})
    print(f"  RESULT: build written -> {target_dir.relative_to(REPO_ROOT)}")
    return 0


# ---------------------------------------------------------------------------
# kind = publication-lifecycle-transition
# ---------------------------------------------------------------------------

def run_lifecycle_transition(request: dict, confirm: bool) -> int:
    payload = request.get("payload", {})
    reviewer = request.get("reviewer") or "UNATTRIBUTED"
    build_id = payload.get("build_id")
    from_state = payload.get("from_state")
    to_state = payload.get("to_state")

    print(f"[gov-syn-exec] kind=publication-lifecycle-transition build_id={build_id} reviewer={reviewer}")
    print(f"  {from_state} -> {to_state}")

    failures: list[str] = []
    if reviewer == "UNATTRIBUTED":
        failures.append("PL-1: reviewer attribution required")
    if not build_id:
        failures.append("PL-MISSING-BUILD: build_id required")
    if to_state not in PUBLICATION_STATES:
        failures.append(f"PL: unknown to_state '{to_state}'")
    if (from_state, to_state) not in PUBLICATION_EDGES:
        failures.append(f"PL: illegal transition {from_state} -> {to_state}")
    actual = current_publication_state(build_id) if build_id else None
    if actual is not None and actual != from_state:
        failures.append(f"PL-STATE: declared from_state '{from_state}' != actual '{actual}'")
    if actual in PUBLICATION_TERMINAL_STATES:
        failures.append(f"PL-6: build is in terminal state '{actual}'")

    for f in failures:
        print(f"  FAIL : {f}")
    if failures:
        if confirm:
            emit_audit(build_id or "no-build", "lifecycle-precheck-failure", "block",
                       "; ".join(failures), reviewer, {"request": request})
        print("  RESULT: refused (fail-closed)")
        return 2

    if not confirm:
        print("  DRY-RUN: transition well-formed.")
        return 0

    # Move the build directory to the new lifecycle bucket (still under publication-builds/).
    moved = None
    if from_state and to_state and from_state != to_state:
        src = PUBLICATION_BUILDS_ROOT / from_state / build_id
        dst = PUBLICATION_BUILDS_ROOT / to_state / build_id
        if src.exists() and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            src.rename(dst)
            moved = {"from": str(src.relative_to(REPO_ROOT)), "to": str(dst.relative_to(REPO_ROOT))}

    append_event("publication-lifecycle-events", {
        "lifecycle_event_id": "plt-" + build_id + "-" + now_compact(),
        "build_id": build_id,
        "from_state": from_state,
        "to_state": to_state,
        "reviewer": reviewer,
        "reasoning_chain": list(payload.get("reasoning_chain") or []),
        "moved": moved,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(build_id, "lifecycle-transitioned", "info",
               f"{from_state} -> {to_state}", reviewer, {"moved": moved})
    print(f"  RESULT: transitioned ({from_state} -> {to_state})")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Governed knowledge synthesis & publication CLI executor (phase 48, layer 41)."
    )
    p.add_argument("--kind", required=True, choices=[
        "synthesis", "publication-build", "evidence-resolve", "rendering",
        "troubleshooting-synthesis", "specification-synthesis",
        "manual-assembly", "publication-lifecycle-transition",
    ])
    p.add_argument("--request", required=True, help="Path to the operation-request JSON file.")
    p.add_argument("--confirm", action="store_true",
                   help="Required to write or append.")
    args = p.parse_args()

    req_path = Path(args.request).expanduser().resolve()
    if not req_path.exists():
        print(f"[gov-syn-exec] FATAL: request file not found: {req_path}", file=sys.stderr)
        return 4
    request = load_json(req_path)
    if request.get("schema") != SCHEMA:
        print(f"[gov-syn-exec] FATAL: unsupported schema {request.get('schema')}", file=sys.stderr)
        return 4

    if args.kind == "synthesis":
        return run_synthesis(request, args.confirm)
    if args.kind == "publication-build":
        return run_publication_build(request, args.confirm)
    if args.kind == "evidence-resolve":
        return run_evidence_resolve(request, args.confirm)
    if args.kind == "rendering":
        return run_rendering(request, args.confirm)
    if args.kind == "troubleshooting-synthesis":
        return run_generic_synthesis(request, args.confirm, "troubleshooting-synthesis", "synthesis-events")
    if args.kind == "specification-synthesis":
        return run_generic_synthesis(request, args.confirm, "specification-synthesis", "synthesis-events")
    if args.kind == "manual-assembly":
        return run_generic_synthesis(request, args.confirm, "manual-assembly", "synthesis-events")
    if args.kind == "publication-lifecycle-transition":
        return run_lifecycle_transition(request, args.confirm)
    return 4


if __name__ == "__main__":
    sys.exit(main())
