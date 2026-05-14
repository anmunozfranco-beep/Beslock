#!/usr/bin/env python3
"""
Phase 58 executor — reviewer operational ergonomics, guided runtime workflows
& production usability closure (constitutional layer 51).

Request envelope: governed-fs-operation-request/1.0
CLI: --kind <dispatch> --request <envelope.json> --confirm

Convergence-oriented: pointer-only artifacts that bind reviewers to existing
governance state. Reviewer-authoritative, append-only, deterministic.

NO new semantic / convergence / extraction / publication / replay families.
NO autonomous agents / autonomous prioritization / autonomous activation.
NO behavior tracking / analytics / telemetry / dashboards.
NO presentation / rendering systems. NO operational automation.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA = "governed-fs-operation-request/1.0"
LAYER_SCHEMA = "reviewer-operational-ergonomics-convergence/1.0"
LAYER = 51

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"

# Phase 58 isolated storage tree
RO_ROOT = OC_ROOT / "reviewer-operational-runtime"
GUIDED_WORKFLOWS = RO_ROOT / "guided-workflows"
ONBOARDING_SEQUENCES = RO_ROOT / "onboarding-sequences"
DEPLOYMENT_CHECKLISTS = RO_ROOT / "deployment-checklists"
OPERATIONAL_DIAGNOSTICS = RO_ROOT / "operational-diagnostics"
NAVIGATION_INDEXES = RO_ROOT / "runtime-navigation-indexes"
REVIEW_QUEUES = RO_ROOT / "corpus-review-queues"
CONFIDENCE_SUMMARIES = RO_ROOT / "operational-confidence-summaries"
REPRODUCIBILITY_PROOFS = RO_ROOT / "reproducibility-proofs"
SESSION_RECORDS = RO_ROOT / "reviewer-session-records"
HANDOFF_RECORDS = RO_ROOT / "production-handoff-records"

# Upstream READ-ONLY trees
SC_ROOT = OC_ROOT / "semantic-convergence-runtime"
SC_CANONICAL_ENTITIES = SC_ROOT / "canonical-entities"
SC_CANONICAL_PROCEDURES = SC_ROOT / "canonical-procedures"
SC_CONFLICTS = SC_ROOT / "conflict-surfacings"
SC_ARBITRATION = SC_ROOT / "arbitration-decisions"
SC_STABILIZATIONS = SC_ROOT / "export-stabilizations"

PC_ROOT = OC_ROOT / "production-closure-runtime"
PC_DRIFT = PC_ROOT / "canonical-drift-records"
PC_GUARANTEES = PC_ROOT / "export-stability-guarantees"
PC_AUDITS = PC_ROOT / "readiness-audit-records"
PC_ML_TABLES = PC_ROOT / "multilingual-normalization-tables"
PC_ROBUSTNESS = PC_ROOT / "robustness-records"

PACKAGING_RUNTIME = OC_ROOT / "manual-semantic-packaging-runtime"
PACKAGES_DIR = PACKAGING_RUNTIME / "manual-packages"

MR_ROOT = OC_ROOT / "manual-runtime-closure"
EXPORT_FINALIZATIONS = MR_ROOT / "export-finalizations"

OD_ROOT = OC_ROOT / "operational-deployment-runtime"
DEPLOYMENT_PACKAGES = OD_ROOT / "deployment-packages"
DEPLOYMENT_VERIFICATIONS = OD_ROOT / "deployment-verifications"
ACTIVATION_LIFECYCLE = OD_ROOT / "activation-lifecycle-records"

# Event stores (Phase 58)
ES_WORKFLOW = RUNTIME_MANIFESTS_ROOT / "reviewer-guided-workflow-events" / "_event-store.json"
ES_ONBOARDING = RUNTIME_MANIFESTS_ROOT / "onboarding-sequence-events" / "_event-store.json"
ES_CHECKLIST = RUNTIME_MANIFESTS_ROOT / "deployment-checklist-events" / "_event-store.json"
ES_DIAGNOSTICS = RUNTIME_MANIFESTS_ROOT / "operational-diagnostics-events" / "_event-store.json"
ES_NAV = RUNTIME_MANIFESTS_ROOT / "runtime-navigation-index-events" / "_event-store.json"
ES_QUEUE = RUNTIME_MANIFESTS_ROOT / "corpus-review-queue-events" / "_event-store.json"
ES_CONFIDENCE = RUNTIME_MANIFESTS_ROOT / "operational-confidence-events" / "_event-store.json"
ES_REPRO = RUNTIME_MANIFESTS_ROOT / "reproducibility-proof-events" / "_event-store.json"
ES_SESSION = RUNTIME_MANIFESTS_ROOT / "reviewer-session-events" / "_event-store.json"
ES_HANDOFF = RUNTIME_MANIFESTS_ROOT / "production-handoff-events" / "_event-store.json"
ES_AUDIT = RUNTIME_MANIFESTS_ROOT / "audit-events" / "_event-store.json"

# Upstream event stores referenced for ordering / latest-state lookups
ES_PACKAGING_LIFECYCLE = RUNTIME_MANIFESTS_ROOT / "packaging-lifecycle-events" / "_event-store.json"
ES_ACTIVATION = RUNTIME_MANIFESTS_ROOT / "production-activation-events" / "_event-store.json"

# Enums
WORKFLOW_KINDS = {
    "deployment-walkthrough", "rollback-walkthrough", "readiness-audit-walkthrough",
    "verification-walkthrough", "portfolio-review-walkthrough", "handoff-walkthrough",
}
ONBOARDING_KINDS = {
    "operator-onboarding", "reviewer-onboarding", "deployment-onboarding", "recovery-onboarding",
}
CHECKLIST_KINDS = {
    "pre-activation", "activation", "post-activation", "rollback",
}
DIAGNOSTICS_SCOPES = {"package", "manual", "corpus"}
QUEUE_KINDS = {
    "readiness-audit-pending", "deployment-verification-pending", "rollback-pending",
    "handoff-pending", "drift-triage-pending", "conflict-triage-pending",
}
CONFIDENCE_DIMENSIONS = {
    "readiness-audit-coverage", "deployment-verification-coverage",
    "export-stability-coverage", "robustness-coverage",
    "multilingual-normalization-coverage",
}
REPRODUCIBILITY_TARGETS = {
    "stable-export-hash", "deployment-package-hash", "readiness-audit-hash",
}
SESSION_KINDS = {
    "operator-shift", "deployment-walkthrough-session", "onboarding-session",
    "handoff-session", "diagnostics-review-session",
}
ACTIVATION_STATES = {
    "production-candidate", "production-approved", "production-active",
    "superseded", "rollback-candidate",
}

# Forbidden overwrite prefixes — accumulate ALL prior phases including Phase 57.
FORBIDDEN_OVERWRITE_PREFIXES = (
    "operational-deployment-runtime/",
    "production-closure-runtime/",
    "semantic-convergence-runtime/",
    "manual-runtime-closure/",
    "manual-semantic-packaging-runtime/",
    "semantic-extraction-runtime/",
    "publication-composition-runtime/",
    "visual-generation-runtime/",
    "knowledge-grounding-runtime/",
    "knowledge-synthesis-runtime/",
    "execution-engine/",
    "assets/exec/",
    "wp-content/themes/",
    "wp-includes/",
    "wp-admin/",
)

FORBIDDEN_PRESENTATION_KEYS = {
    "css", "class", "classname", "style", "styles", "inline_style",
    "breakpoint", "breakpoints", "screen_size", "screen_width", "viewport",
    "layout", "grid", "flex", "column_count", "column_width",
    "typography", "font", "font_size", "font_family", "font_weight",
    "color", "background", "background_color",
    "padding", "margin",
    "responsive", "responsive_rules", "media_query", "media_queries",
    "rendering_hint", "render_hint", "ui_framework", "theme",
}

FORBIDDEN_PROBABILISTIC_KEYS = {
    "embedding", "embeddings", "vector", "vectors",
    "similarity_score", "semantic_score", "cosine_similarity",
    "ml_model", "model_inference", "probabilistic", "probability",
    "autonomous_decision", "autonomous_arbitration", "autonomous_activation",
    "autonomous_prioritization", "autonomous_priority",
    "ai_priority", "ml_priority", "ranking_score", "rank_score",
    "priority_score", "auto_priority", "scored_priority",
}

FORBIDDEN_TRANSLATION_KEYS = {
    "machine_translation", "llm_translation", "mt_model",
    "language_model_inference", "autodetect_language", "language_inference",
    "neural_translation", "translation_score", "translation_confidence",
}

FORBIDDEN_TELEMETRY_KEYS = {
    "telemetry", "telemetry_endpoint", "telemetry_stream",
    "dashboard", "dashboard_widget", "metric_stream",
    "streaming", "live_stream", "websocket", "webhook",
    "deployment_daemon", "auto_deploy", "autonomous_deployment",
    "analytics", "analytics_event", "tracking_pixel",
    "behavior_tracking", "user_tracking", "session_tracking",
    "telemetry_beacon", "engagement_score",
}


# ============================================================================
# Helpers
# ============================================================================
def _now() -> str:
    return _dt.datetime.now(_dt.UTC).strftime("%Y%m%dT%H%M%SZ")


def _iso_now() -> str:
    return _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    sys.stderr.write(f"FAIL-CLOSED: {msg}\n")
    sys.exit(2)


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def find_forbidden_key(obj: Any, forbidden: set[str], path: str = "$") -> tuple[str, str] | None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.lower() in forbidden:
                return (path + "." + k, k.lower())
            sub = find_forbidden_key(v, forbidden, path + "." + (k if isinstance(k, str) else "?"))
            if sub:
                return sub
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            sub = find_forbidden_key(v, forbidden, path + "[" + str(i) + "]")
            if sub:
                return sub
    return None


def reject_presentation(payload: dict, rule_id: str) -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_PRESENTATION_KEYS)
    if hit:
        fail(f"presentation key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


def reject_probabilistic(payload: dict, rule_id: str = "RO-PROB") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_PROBABILISTIC_KEYS)
    if hit:
        fail(f"probabilistic/embedding/autonomous-prioritization key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


def reject_translation(payload: dict, rule_id: str = "RO-TRANS") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_TRANSLATION_KEYS)
    if hit:
        fail(f"translation/language-inference key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


def reject_telemetry(payload: dict, rule_id: str = "RO-TELE") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_TELEMETRY_KEYS)
    if hit:
        fail(f"telemetry/dashboard/streaming/analytics/behavior-tracking key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


def assert_target_path(payload: dict) -> None:
    tp = payload.get("target_path")
    if isinstance(tp, str) and tp:
        norm = tp.replace("\\", "/")
        for prefix in FORBIDDEN_OVERWRITE_PREFIXES:
            if prefix in norm:
                fail(f"target_path falls under a forbidden prefix '{prefix}'")


def write_json(p: Path, data: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def append_event(store_path: Path, event: dict) -> None:
    store_path.parent.mkdir(parents=True, exist_ok=True)
    if store_path.exists():
        data = read_json(store_path)
    else:
        data = {"schema": LAYER_SCHEMA, "store": store_path.parent.name, "append_only": True, "events": []}
    if not isinstance(data.get("events"), list):
        data["events"] = []
    data["events"].append(event)
    write_json(store_path, data)


def append_audit(kind: str, reviewer: str, payload: dict) -> None:
    append_event(ES_AUDIT, {
        "audit_event_id": f"a58-{kind}-{_now()}",
        "occurred_at_iso": _iso_now(),
        "kind": kind,
        "reviewer": reviewer,
        "layer": LAYER,
        "schema": LAYER_SCHEMA,
        "append_only": True,
        "payload": payload,
    })


def _scan_for_id(d: Path, id_field: str, target_id: str) -> dict | None:
    if not d.exists():
        return None
    for p in sorted(d.glob("*.json")):
        try:
            data = read_json(p)
        except Exception:
            continue
        if data.get(id_field) == target_id:
            return data
    return None


def _scan_all(d: Path) -> list[dict]:
    out: list[dict] = []
    if not d.exists():
        return out
    for p in sorted(d.glob("*.json")):
        try:
            out.append(read_json(p))
        except Exception:
            continue
    return out


# Cross-phase finders
def find_package(pid: str) -> dict | None:
    return _scan_for_id(PACKAGES_DIR, "package_id", pid)


def find_stabilization(sid: str) -> dict | None:
    return _scan_for_id(SC_STABILIZATIONS, "stabilization_id", sid)


def find_readiness_audit(aid: str) -> dict | None:
    return _scan_for_id(PC_AUDITS, "audit_id", aid)


def find_deployment_package(dpid: str) -> dict | None:
    return _scan_for_id(DEPLOYMENT_PACKAGES, "deployment_package_id", dpid)


def find_deployment_verification(vid: str) -> dict | None:
    return _scan_for_id(DEPLOYMENT_VERIFICATIONS, "verification_id", vid)


def find_export_stability_guarantee(gid: str) -> dict | None:
    return _scan_for_id(PC_GUARANTEES, "guarantee_id", gid)


def find_normalization_table(tid: str) -> dict | None:
    return _scan_for_id(PC_ML_TABLES, "table_id", tid)


def find_robustness_record(rid: str) -> dict | None:
    return _scan_for_id(PC_ROBUSTNESS, "robustness_id", rid)


def latest_activation_state(activation_id: str) -> str | None:
    """Most-recent to_state for activation_id from append-only event store."""
    if not ES_ACTIVATION.exists():
        return None
    try:
        events = read_json(ES_ACTIVATION).get("events", [])
    except Exception:
        return None
    last = None
    for e in events:
        if e.get("activation_id") == activation_id and e.get("to_state"):
            last = e["to_state"]
    return last


def package_lifecycle_state(package_id: str) -> str | None:
    if not ES_PACKAGING_LIFECYCLE.exists():
        return None
    try:
        events = read_json(ES_PACKAGING_LIFECYCLE).get("events", [])
    except Exception:
        return None
    last = None
    for e in events:
        pid = e.get("package_id") or e.get("payload", {}).get("package_id")
        ts = e.get("to_state") or e.get("payload", {}).get("to_state")
        if pid == package_id and ts:
            last = ts
    return last


# Self-layer finders
def find_workflow(wid: str) -> dict | None:
    return _scan_for_id(GUIDED_WORKFLOWS, "workflow_id", wid)


def find_onboarding_sequence(sid: str) -> dict | None:
    return _scan_for_id(ONBOARDING_SEQUENCES, "sequence_id", sid)


def find_checklist(cid: str) -> dict | None:
    return _scan_for_id(DEPLOYMENT_CHECKLISTS, "checklist_id", cid)


def find_diagnostics(did: str) -> dict | None:
    return _scan_for_id(OPERATIONAL_DIAGNOSTICS, "diagnostics_id", did)


def find_navigation_index(nid: str) -> dict | None:
    return _scan_for_id(NAVIGATION_INDEXES, "index_id", nid)


def find_review_queue(qid: str) -> dict | None:
    return _scan_for_id(REVIEW_QUEUES, "queue_id", qid)


def find_confidence_summary(cid: str) -> dict | None:
    return _scan_for_id(CONFIDENCE_SUMMARIES, "confidence_id", cid)


def find_reproducibility_proof(pid: str) -> dict | None:
    return _scan_for_id(REPRODUCIBILITY_PROOFS, "proof_id", pid)


def find_session_record(sid: str) -> dict | None:
    return _scan_for_id(SESSION_RECORDS, "session_id", sid)


def find_handoff_record(hid: str) -> dict | None:
    return _scan_for_id(HANDOFF_RECORDS, "handoff_id", hid)


# ============================================================================
# Dispatch handlers
# ============================================================================
def _validate_steps(steps: Any, rule_id: str, extra_required: tuple[str, ...] = ()) -> list[dict]:
    if not isinstance(steps, list) or not steps:
        fail(f"steps must be a non-empty list ({rule_id})")
    out: list[dict] = []
    seen = set()
    for i, s in enumerate(steps):
        if not isinstance(s, dict):
            fail(f"steps[{i}] must be a dict ({rule_id})")
        sid = s.get("step_id")
        action = s.get("action")
        outcome = s.get("expected_outcome")
        if not isinstance(sid, str) or not sid.strip():
            fail(f"steps[{i}].step_id required ({rule_id})")
        if sid in seen:
            fail(f"steps[{i}].step_id {sid!r} duplicate ({rule_id})")
        seen.add(sid)
        if not isinstance(action, str) or not action.strip():
            fail(f"steps[{i}].action required ({rule_id})")
        if not isinstance(outcome, str) or not outcome.strip():
            fail(f"steps[{i}].expected_outcome required ({rule_id})")
        norm = {"step_index": i + 1, "step_id": sid, "action": action, "expected_outcome": outcome}
        for key in extra_required:
            v = s.get(key)
            if not isinstance(v, str) or not v.strip():
                fail(f"steps[{i}].{key} required ({rule_id})")
            norm[key] = v
        out.append(norm)
    return out


def _runtime_path_exists(rel_path: str) -> bool:
    """A runtime_path is valid iff it exists under OC_ROOT (file or dir)."""
    if not isinstance(rel_path, str) or not rel_path.strip():
        return False
    norm = rel_path.replace("\\", "/").lstrip("/")
    if ".." in norm.split("/"):
        return False
    return (OC_ROOT / norm).exists()


def handle_reviewer_guided_workflow(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "RG-5")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    workflow_id = payload.get("workflow_id")
    workflow_kind = payload.get("workflow_kind")
    steps = payload.get("steps")
    notes = payload.get("notes", "")
    if not workflow_id:
        fail("payload.workflow_id required (RG-1)")
    if find_workflow(workflow_id):
        fail(f"workflow_id {workflow_id!r} already exists (RG-1)")
    if workflow_kind not in WORKFLOW_KINDS:
        fail(f"workflow_kind {workflow_kind!r} not in {sorted(WORKFLOW_KINDS)} (RG-2)")
    norm_steps = _validate_steps(steps, "RG-3", extra_required=("runtime_reference",))
    for i, s in enumerate(norm_steps):
        ref = s["runtime_reference"]
        if not _runtime_path_exists(ref):
            fail(f"steps[{i}].runtime_reference {ref!r} does not resolve to an existing path under operational-console/ (RG-4)")

    wf_payload = {
        "workflow_id": workflow_id,
        "workflow_kind": workflow_kind,
        "steps": norm_steps,
        "notes": notes,
    }
    workflow_sha256 = sha256_text(canonical_json(wf_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **wf_payload,
        "workflow_sha256": workflow_sha256,
        "step_count": len(norm_steps),
        "pointer_only": True,
        "presentation_neutral": True,
        "no_orchestration_execution": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(GUIDED_WORKFLOWS / f"{workflow_id}-{_now()}.json", record)
    append_event(ES_WORKFLOW, {
        "occurred_at_iso": _iso_now(),
        "kind": "reviewer-guided-workflow",
        "workflow_id": workflow_id,
        "workflow_kind": workflow_kind,
        "step_count": len(norm_steps),
        "workflow_sha256": workflow_sha256,
        "reviewer": reviewer,
    })
    append_audit("reviewer-guided-workflow", reviewer,
                 {"workflow_id": workflow_id, "workflow_kind": workflow_kind})
    return {"workflow_id": workflow_id, "workflow_sha256": workflow_sha256, "step_count": len(norm_steps)}


def handle_onboarding_sequence_publish(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "ON-5")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    sequence_id = payload.get("sequence_id")
    sequence_kind = payload.get("sequence_kind")
    modules = payload.get("modules")
    prior_sequence_id = payload.get("prior_sequence_id")
    notes = payload.get("notes", "")
    if not sequence_id:
        fail("payload.sequence_id required (ON-1)")
    if find_onboarding_sequence(sequence_id):
        fail(f"sequence_id {sequence_id!r} already exists; supersede via prior_sequence_id (ON-6)")
    if sequence_kind not in ONBOARDING_KINDS:
        fail(f"sequence_kind {sequence_kind!r} not in {sorted(ONBOARDING_KINDS)} (ON-2)")
    if not isinstance(modules, list) or not modules:
        fail("modules must be a non-empty list (ON-3)")
    norm_modules = []
    seen = set()
    for i, m in enumerate(modules):
        if not isinstance(m, dict):
            fail(f"modules[{i}] must be a dict (ON-3)")
        mid = m.get("module_id")
        title = m.get("title")
        refs = m.get("references")
        if not isinstance(mid, str) or not mid.strip():
            fail(f"modules[{i}].module_id required (ON-3)")
        if mid in seen:
            fail(f"modules[{i}].module_id {mid!r} duplicate (ON-3)")
        seen.add(mid)
        if not isinstance(title, str) or not title.strip():
            fail(f"modules[{i}].title required (ON-3)")
        if not isinstance(refs, list) or not refs:
            fail(f"modules[{i}].references must be a non-empty list (ON-3)")
        for j, r in enumerate(refs):
            if not isinstance(r, str) or not r.strip():
                fail(f"modules[{i}].references[{j}] must be a non-empty string (ON-4)")
            norm = r.replace("\\", "/").lstrip("/")
            if ".." in norm.split("/"):
                fail(f"modules[{i}].references[{j}] contains forbidden path component '..' (ON-4)")
            # Allow paths under OC_ROOT or under KNOWLEDGE_BUILDING/.
            oc_target = OC_ROOT / norm
            kb_target = THEME_ROOT / norm  # references like "KNOWLEDGE_BUILDING/..." resolve under THEME_ROOT
            if not (oc_target.exists() or kb_target.exists()):
                fail(f"modules[{i}].references[{j}] {r!r} does not resolve under operational-console/ or KNOWLEDGE_BUILDING/ (ON-4)")
        norm_modules.append({
            "module_index": i + 1,
            "module_id": mid,
            "title": title,
            "references": list(refs),
        })
    if prior_sequence_id and not find_onboarding_sequence(prior_sequence_id):
        fail(f"prior_sequence_id {prior_sequence_id!r} not found (ON-6)")

    seq_payload = {
        "sequence_id": sequence_id,
        "sequence_kind": sequence_kind,
        "modules": norm_modules,
        "prior_sequence_id": prior_sequence_id,
        "notes": notes,
    }
    sequence_sha256 = sha256_text(canonical_json(seq_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **seq_payload,
        "sequence_sha256": sequence_sha256,
        "module_count": len(norm_modules),
        "pointer_only": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(ONBOARDING_SEQUENCES / f"{sequence_id}-{_now()}.json", record)
    append_event(ES_ONBOARDING, {
        "occurred_at_iso": _iso_now(),
        "kind": "onboarding-sequence-publish",
        "sequence_id": sequence_id,
        "sequence_kind": sequence_kind,
        "module_count": len(norm_modules),
        "sequence_sha256": sequence_sha256,
        "reviewer": reviewer,
    })
    append_audit("onboarding-sequence-publish", reviewer,
                 {"sequence_id": sequence_id, "sequence_kind": sequence_kind})
    return {"sequence_id": sequence_id, "sequence_sha256": sequence_sha256,
            "module_count": len(norm_modules)}


def _resolve_governance_reference(kind: str, ref_id: str) -> dict | None:
    resolvers = {
        "readiness-audit": find_readiness_audit,
        "deployment-verification": find_deployment_verification,
        "deployment-package": find_deployment_package,
        "export-stabilization": find_stabilization,
        "manual-package": find_package,
        "export-stability-guarantee": find_export_stability_guarantee,
        "normalization-table": find_normalization_table,
        "robustness-record": find_robustness_record,
    }
    resolver = resolvers.get(kind)
    if not resolver:
        return None
    return resolver(ref_id)


def handle_deployment_checklist_publish(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "DC-6")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    checklist_id = payload.get("checklist_id")
    checklist_kind = payload.get("checklist_kind")
    package_id = payload.get("package_id")
    items = payload.get("items")
    notes = payload.get("notes", "")
    if not checklist_id:
        fail("payload.checklist_id required (DC-1)")
    if find_checklist(checklist_id):
        fail(f"checklist_id {checklist_id!r} already exists (DC-1)")
    if checklist_kind not in CHECKLIST_KINDS:
        fail(f"checklist_kind {checklist_kind!r} not in {sorted(CHECKLIST_KINDS)} (DC-2)")
    pkg = find_package(package_id) if package_id else None
    if not pkg:
        fail(f"package_id {package_id!r} not found (DC-3)")
    if not isinstance(items, list) or not items:
        fail("items must be a non-empty list (DC-4)")
    norm_items = []
    seen = set()
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            fail(f"items[{i}] must be a dict (DC-4)")
        iid = it.get("item_id")
        req = it.get("requirement")
        gov = it.get("governance_reference")
        if not isinstance(iid, str) or not iid.strip():
            fail(f"items[{i}].item_id required (DC-4)")
        if iid in seen:
            fail(f"items[{i}].item_id {iid!r} duplicate (DC-4)")
        seen.add(iid)
        if not isinstance(req, str) or not req.strip():
            fail(f"items[{i}].requirement required (DC-4)")
        if not isinstance(gov, dict):
            fail(f"items[{i}].governance_reference must be a {{kind, id}} dict (DC-4)")
        gkind = gov.get("kind")
        gid = gov.get("id")
        if not isinstance(gkind, str) or not isinstance(gid, str):
            fail(f"items[{i}].governance_reference requires string kind and id (DC-4)")
        resolved = _resolve_governance_reference(gkind, gid)
        if not resolved:
            fail(f"items[{i}].governance_reference {gkind}:{gid} not resolvable (DC-5)")
        norm_items.append({
            "item_index": i + 1,
            "item_id": iid,
            "requirement": req,
            "governance_reference": {"kind": gkind, "id": gid},
        })

    cl_payload = {
        "checklist_id": checklist_id,
        "checklist_kind": checklist_kind,
        "package_id": package_id,
        "items": norm_items,
        "notes": notes,
    }
    checklist_sha256 = sha256_text(canonical_json(cl_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **cl_payload,
        "checklist_sha256": checklist_sha256,
        "item_count": len(norm_items),
        "pointer_only": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(DEPLOYMENT_CHECKLISTS / f"{checklist_id}-{_now()}.json", record)
    append_event(ES_CHECKLIST, {
        "occurred_at_iso": _iso_now(),
        "kind": "deployment-checklist-publish",
        "checklist_id": checklist_id,
        "checklist_kind": checklist_kind,
        "package_id": package_id,
        "item_count": len(norm_items),
        "checklist_sha256": checklist_sha256,
        "reviewer": reviewer,
    })
    append_audit("deployment-checklist-publish", reviewer,
                 {"checklist_id": checklist_id, "package_id": package_id})
    return {"checklist_id": checklist_id, "checklist_sha256": checklist_sha256,
            "item_count": len(norm_items)}


def handle_operational_diagnostics_summary(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "OD-6")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    diagnostics_id = payload.get("diagnostics_id")
    scope = payload.get("scope")
    package_id = payload.get("package_id")
    manual_id = payload.get("manual_id")
    notes = payload.get("notes", "")
    if not diagnostics_id:
        fail("payload.diagnostics_id required (OD-1)")
    if find_diagnostics(diagnostics_id):
        fail(f"diagnostics_id {diagnostics_id!r} already exists (OD-1)")
    if scope not in DIAGNOSTICS_SCOPES:
        fail(f"scope {scope!r} not in {sorted(DIAGNOSTICS_SCOPES)} (OD-2)")
    if scope == "package":
        if not package_id or not find_package(package_id):
            fail(f"scope='package' requires resolvable package_id (OD-3)")
    if scope == "manual":
        if not isinstance(manual_id, str) or not manual_id.strip():
            fail(f"scope='manual' requires non-empty manual_id (OD-3)")
        # Verify manual_id appears on at least one package.
        if not any(p.get("manual_id") == manual_id for p in _scan_all(PACKAGES_DIR)):
            fail(f"manual_id {manual_id!r} not present on any package (OD-3)")

    # Deterministic snapshot — counts of upstream artifacts filtered by scope.
    def _filter(records: list[dict], scope_key: str) -> list[dict]:
        if scope == "package":
            return [r for r in records if r.get(scope_key) == package_id]
        if scope == "manual":
            return [r for r in records if r.get(scope_key) == manual_id]
        return records

    drift = _filter(_scan_all(PC_DRIFT), "package_id")
    conflicts = _scan_all(SC_CONFLICTS)
    arb_accepted = {a.get("conflict_id") for a in _scan_all(SC_ARBITRATION) if a.get("decision") == "accept"}
    unresolved_conflicts = [c for c in conflicts if c.get("conflict_id") not in arb_accepted]
    audits = _filter(_scan_all(PC_AUDITS), "package_id")
    verifications = _filter(_scan_all(DEPLOYMENT_VERIFICATIONS), "package_id")
    deployment_packages_list = _filter(_scan_all(DEPLOYMENT_PACKAGES), "package_id")
    activations = _filter(_scan_all(ACTIVATION_LIFECYCLE), "package_id")

    snapshot = {
        "diagnostics_id": diagnostics_id,
        "scope": scope,
        "package_id": package_id if scope == "package" else None,
        "manual_id": manual_id if scope == "manual" else None,
        "counts": {
            "drift_records": len(drift),
            "conflicts": len(conflicts),
            "unresolved_conflicts": len(unresolved_conflicts),
            "readiness_audits": len(audits),
            "deployment_verifications": len(verifications),
            "deployment_packages": len(deployment_packages_list),
            "activation_lifecycle_records": len(activations),
        },
        "drift_severity_breakdown": _severity_breakdown(drift),
        "audit_status_breakdown": _status_breakdown(audits, "status"),
        "verification_status_breakdown": _status_breakdown(verifications, "status"),
        "notes": notes,
    }
    diagnostics_sha256 = sha256_text(canonical_json(snapshot))
    record = {
        "schema": LAYER_SCHEMA,
        **snapshot,
        "diagnostics_sha256": diagnostics_sha256,
        "deterministic_snapshot": True,
        "no_streaming": True,
        "no_dashboards": True,
        "no_telemetry": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(OPERATIONAL_DIAGNOSTICS / f"{diagnostics_id}-{_now()}.json", record)
    append_event(ES_DIAGNOSTICS, {
        "occurred_at_iso": _iso_now(),
        "kind": "operational-diagnostics-summary",
        "diagnostics_id": diagnostics_id,
        "scope": scope,
        "diagnostics_sha256": diagnostics_sha256,
        "reviewer": reviewer,
    })
    append_audit("operational-diagnostics-summary", reviewer,
                 {"diagnostics_id": diagnostics_id, "scope": scope})
    return {"diagnostics_id": diagnostics_id, "diagnostics_sha256": diagnostics_sha256, "scope": scope}


def _severity_breakdown(records: list[dict]) -> dict:
    out: dict[str, int] = {}
    for r in records:
        sev = r.get("severity")
        if isinstance(sev, str):
            out[sev] = out.get(sev, 0) + 1
    return dict(sorted(out.items()))


def _status_breakdown(records: list[dict], key: str) -> dict:
    out: dict[str, int] = {}
    for r in records:
        v = r.get(key)
        if isinstance(v, str):
            out[v] = out.get(v, 0) + 1
    return dict(sorted(out.items()))


def handle_runtime_navigation_index(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "NI-5")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    index_id = payload.get("index_id")
    entries = payload.get("entries")
    notes = payload.get("notes", "")
    if not index_id:
        fail("payload.index_id required (NI-1)")
    if find_navigation_index(index_id):
        fail(f"index_id {index_id!r} already exists (NI-1)")
    if not isinstance(entries, list) or not entries:
        fail("entries must be a non-empty list (NI-2)")
    norm_entries = []
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            fail(f"entries[{i}] must be a dict (NI-2)")
        label = e.get("label")
        rp = e.get("runtime_path")
        kind = e.get("kind")
        if not isinstance(label, str) or not label.strip():
            fail(f"entries[{i}].label required (NI-2)")
        if not isinstance(rp, str) or not rp.strip():
            fail(f"entries[{i}].runtime_path required (NI-2)")
        if not isinstance(kind, str) or not kind.strip():
            fail(f"entries[{i}].kind required (NI-2)")
        if not _runtime_path_exists(rp):
            fail(f"entries[{i}].runtime_path {rp!r} does not exist under operational-console/ (NI-3)")
        norm_entries.append({"entry_index": i + 1, "label": label, "runtime_path": rp, "kind": kind})

    idx_payload = {
        "index_id": index_id,
        "entries": norm_entries,
        "notes": notes,
    }
    index_sha256 = sha256_text(canonical_json(idx_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **idx_payload,
        "index_sha256": index_sha256,
        "entry_count": len(norm_entries),
        "pointer_only": True,
        "no_mirroring": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(NAVIGATION_INDEXES / f"{index_id}-{_now()}.json", record)
    append_event(ES_NAV, {
        "occurred_at_iso": _iso_now(),
        "kind": "runtime-navigation-index",
        "index_id": index_id,
        "entry_count": len(norm_entries),
        "index_sha256": index_sha256,
        "reviewer": reviewer,
    })
    append_audit("runtime-navigation-index", reviewer,
                 {"index_id": index_id, "entry_count": len(norm_entries)})
    return {"index_id": index_id, "index_sha256": index_sha256, "entry_count": len(norm_entries)}


def _resolve_governing_artifact_pointer(kind: str, art_id: str) -> dict | None:
    resolvers = {
        "readiness-audit": find_readiness_audit,
        "deployment-verification": find_deployment_verification,
        "deployment-package": find_deployment_package,
        "export-stabilization": find_stabilization,
        "manual-package": find_package,
        "drift-record": lambda i: _scan_for_id(PC_DRIFT, "drift_id", i),
        "conflict-surfacing": lambda i: _scan_for_id(SC_CONFLICTS, "conflict_id", i),
        "robustness-record": find_robustness_record,
    }
    resolver = resolvers.get(kind)
    if not resolver:
        return None
    return resolver(art_id)


def handle_corpus_review_queue(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "CQ-6")
    reject_probabilistic(payload, "CQ-5")
    reject_translation(payload)
    reject_telemetry(payload)
    queue_id = payload.get("queue_id")
    queue_kind = payload.get("queue_kind")
    entries = payload.get("entries")
    notes = payload.get("notes", "")
    if not queue_id:
        fail("payload.queue_id required (CQ-1)")
    if find_review_queue(queue_id):
        fail(f"queue_id {queue_id!r} already exists (CQ-1)")
    if queue_kind not in QUEUE_KINDS:
        fail(f"queue_kind {queue_kind!r} not in {sorted(QUEUE_KINDS)} (CQ-2)")
    if not isinstance(entries, list) or not entries:
        fail("entries must be a non-empty list (CQ-3)")
    norm_entries = []
    seen = set()
    forbidden_ordering_keys = {"score", "rank", "priority", "weight", "ranking", "ordering_score"}
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            fail(f"entries[{i}] must be a dict (CQ-3)")
        # explicit reject on shallow priority / score / rank keys at entry level.
        for k in e.keys():
            if isinstance(k, str) and k.lower() in forbidden_ordering_keys:
                fail(f"entries[{i}].{k} forbidden — reviewer-supplied ordering only, no automatic prioritization (CQ-5)")
        eid = e.get("entry_id")
        pid = e.get("package_id")
        reason = e.get("reason")
        gp = e.get("governing_artifact_pointer")
        if not isinstance(eid, str) or not eid.strip():
            fail(f"entries[{i}].entry_id required (CQ-3)")
        if eid in seen:
            fail(f"entries[{i}].entry_id {eid!r} duplicate (CQ-3)")
        seen.add(eid)
        if not isinstance(pid, str) or not pid.strip():
            fail(f"entries[{i}].package_id required (CQ-4)")
        if not find_package(pid):
            fail(f"entries[{i}].package_id {pid!r} not found (CQ-4)")
        if not isinstance(reason, str) or not reason.strip():
            fail(f"entries[{i}].reason required (CQ-3)")
        if not isinstance(gp, dict):
            fail(f"entries[{i}].governing_artifact_pointer must be a {{kind, id}} dict (CQ-4)")
        gkind = gp.get("kind")
        gid = gp.get("id")
        if not isinstance(gkind, str) or not isinstance(gid, str):
            fail(f"entries[{i}].governing_artifact_pointer requires string kind and id (CQ-4)")
        if not _resolve_governing_artifact_pointer(gkind, gid):
            fail(f"entries[{i}].governing_artifact_pointer {gkind}:{gid} not resolvable (CQ-4)")
        norm_entries.append({
            "entry_index": i + 1,
            "entry_id": eid,
            "package_id": pid,
            "reason": reason,
            "governing_artifact_pointer": {"kind": gkind, "id": gid},
        })

    queue_payload = {
        "queue_id": queue_id,
        "queue_kind": queue_kind,
        "entries": norm_entries,
        "notes": notes,
    }
    queue_sha256 = sha256_text(canonical_json(queue_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **queue_payload,
        "queue_sha256": queue_sha256,
        "entry_count": len(norm_entries),
        "reviewer_supplied_ordering_only": True,
        "no_automatic_prioritization": True,
        "no_probabilistic_ranking": True,
        "no_ai_scoring": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(REVIEW_QUEUES / f"{queue_id}-{_now()}.json", record)
    append_event(ES_QUEUE, {
        "occurred_at_iso": _iso_now(),
        "kind": "corpus-review-queue",
        "queue_id": queue_id,
        "queue_kind": queue_kind,
        "entry_count": len(norm_entries),
        "queue_sha256": queue_sha256,
        "reviewer": reviewer,
    })
    append_audit("corpus-review-queue", reviewer,
                 {"queue_id": queue_id, "queue_kind": queue_kind})
    return {"queue_id": queue_id, "queue_sha256": queue_sha256, "entry_count": len(norm_entries)}


def handle_operational_confidence_summary(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "CF-5")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    confidence_id = payload.get("confidence_id")
    package_id = payload.get("package_id")
    notes = payload.get("notes", "")
    if not confidence_id:
        fail("payload.confidence_id required (CF-1)")
    if find_confidence_summary(confidence_id):
        fail(f"confidence_id {confidence_id!r} already exists (CF-1)")
    pkg = find_package(package_id) if package_id else None
    if not pkg:
        fail(f"package_id {package_id!r} not found (CF-2)")

    def _refs(records: list[dict], id_field: str, hash_field: str | None) -> list[dict]:
        out = []
        for r in records:
            if r.get("package_id") != package_id:
                continue
            entry = {"id": r.get(id_field)}
            if hash_field and r.get(hash_field):
                entry["sha256_pointer"] = r[hash_field]
            out.append(entry)
        out.sort(key=lambda x: (x.get("id") or ""))
        return out

    audits = _refs(_scan_all(PC_AUDITS), "audit_id", "audit_sha256")
    verifications = _refs(_scan_all(DEPLOYMENT_VERIFICATIONS), "verification_id", "verification_sha256")
    guarantees = _refs(_scan_all(PC_GUARANTEES), "guarantee_id", "guarantee_sha256")
    robustness = _refs(_scan_all(PC_ROBUSTNESS), "robustness_id", "robustness_sha256")
    norm_tables = _refs(_scan_all(PC_ML_TABLES), "table_id", "table_sha256")

    summary_payload = {
        "confidence_id": confidence_id,
        "package_id": package_id,
        "manual_id": pkg.get("manual_id"),
        "aggregates": {
            "readiness-audit-coverage": audits,
            "deployment-verification-coverage": verifications,
            "export-stability-coverage": guarantees,
            "robustness-coverage": robustness,
            "multilingual-normalization-coverage": norm_tables,
        },
        "notes": notes,
    }
    confidence_sha256 = sha256_text(canonical_json(summary_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **summary_payload,
        "confidence_sha256": confidence_sha256,
        "pointer_only": True,
        "presentation_neutral": True,
        "no_dashboards": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(CONFIDENCE_SUMMARIES / f"{confidence_id}-{_now()}.json", record)
    append_event(ES_CONFIDENCE, {
        "occurred_at_iso": _iso_now(),
        "kind": "operational-confidence-summary",
        "confidence_id": confidence_id,
        "package_id": package_id,
        "confidence_sha256": confidence_sha256,
        "reviewer": reviewer,
    })
    append_audit("operational-confidence-summary", reviewer,
                 {"confidence_id": confidence_id, "package_id": package_id})
    return {"confidence_id": confidence_id, "confidence_sha256": confidence_sha256,
            "package_id": package_id}


def handle_reproducibility_proof(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "RP-5")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    proof_id = payload.get("proof_id")
    package_id = payload.get("package_id")
    declared = payload.get("declared_hashes")
    notes = payload.get("notes", "")
    if not proof_id:
        fail("payload.proof_id required (RP-1)")
    if find_reproducibility_proof(proof_id):
        fail(f"proof_id {proof_id!r} already exists (RP-1)")
    pkg = find_package(package_id) if package_id else None
    if not pkg:
        fail(f"package_id {package_id!r} not found (RP-2)")
    if not isinstance(declared, dict) or not declared:
        fail("declared_hashes must be a non-empty dict {target: hash} (RP-3)")
    for k in declared.keys():
        if k not in REPRODUCIBILITY_TARGETS:
            fail(f"declared_hashes target {k!r} not in {sorted(REPRODUCIBILITY_TARGETS)} (RP-3)")

    # Re-derive upstream hashes for this package.
    rederived: dict[str, str | None] = {}
    # stable-export-hash: pull from any stabilization with package_id.
    stab_match = next((s for s in _scan_all(SC_STABILIZATIONS) if s.get("package_id") == package_id), None)
    rederived["stable-export-hash"] = stab_match.get("stable_export_sha256") if stab_match else None
    # deployment-package-hash: pull from any deployment-package with package_id.
    dp_match = next((d for d in _scan_all(DEPLOYMENT_PACKAGES) if d.get("package_id") == package_id), None)
    rederived["deployment-package-hash"] = dp_match.get("deployment_package_sha256") if dp_match else None
    # readiness-audit-hash: pull from any readiness audit with package_id.
    aud_match = next((a for a in _scan_all(PC_AUDITS) if a.get("package_id") == package_id), None)
    rederived["readiness-audit-hash"] = aud_match.get("audit_sha256") if aud_match else None

    comparisons: list[dict] = []
    status = "confirmed"
    for target, declared_hash in sorted(declared.items()):
        actual = rederived.get(target)
        if not isinstance(declared_hash, str) or not declared_hash.strip():
            fail(f"declared_hashes[{target}] must be a non-empty string (RP-3)")
        if actual is None:
            fail(f"upstream hash for target {target!r} on package {package_id!r} not found — cannot reproduce (RP-3)")
        match = (declared_hash == actual)
        if not match:
            status = "divergent"
        comparisons.append({
            "target": target,
            "declared_hash": declared_hash,
            "rederived_hash": actual,
            "match": match,
        })

    if status == "divergent":
        # Hard fail-closed on divergence for proof publication: a divergent proof
        # means the declared hashes do not match upstream — reviewer must investigate
        # before recording a proof.
        fail(f"reproducibility proof divergent for package {package_id!r}: {comparisons} (RP-3)")

    # Hash content slice — exclude proof_id so re-derivation across reruns yields
    # identical sha256 for the same {package_id, declared, comparisons}.
    content_slice = {
        "package_id": package_id,
        "declared_hashes": dict(sorted(declared.items())),
        "comparisons": comparisons,
        "status": status,
    }
    proof_sha256 = sha256_text(canonical_json(content_slice))

    record = {
        "schema": LAYER_SCHEMA,
        "proof_id": proof_id,
        "package_id": package_id,
        "declared_hashes": dict(sorted(declared.items())),
        "comparisons": comparisons,
        "status": status,
        "proof_sha256": proof_sha256,
        "informational_only": True,
        "reviewer_authoritative": True,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(REPRODUCIBILITY_PROOFS / f"{proof_id}-{_now()}.json", record)
    append_event(ES_REPRO, {
        "occurred_at_iso": _iso_now(),
        "kind": "reproducibility-proof",
        "proof_id": proof_id,
        "package_id": package_id,
        "status": status,
        "proof_sha256": proof_sha256,
        "reviewer": reviewer,
    })
    append_audit("reproducibility-proof", reviewer,
                 {"proof_id": proof_id, "package_id": package_id, "status": status})
    return {"proof_id": proof_id, "proof_sha256": proof_sha256, "status": status,
            "comparison_count": len(comparisons)}


def handle_reviewer_session_record(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "RS-5")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload, "RS-4")
    session_id = payload.get("session_id")
    session_kind = payload.get("session_kind")
    notes = payload.get("notes", "")
    references = payload.get("references", [])
    if not session_id:
        fail("payload.session_id required (RS-1)")
    if find_session_record(session_id):
        fail(f"session_id {session_id!r} already exists (RS-1)")
    if session_kind not in SESSION_KINDS:
        fail(f"session_kind {session_kind!r} not in {sorted(SESSION_KINDS)} (RS-2)")
    if not isinstance(notes, str):
        fail("notes must be a string (RS-3)")
    if not isinstance(references, list):
        fail("references must be a list (RS-3)")
    norm_refs = []
    for i, r in enumerate(references):
        if not isinstance(r, dict):
            fail(f"references[{i}] must be a dict {{kind, id}} (RS-3)")
        kind = r.get("kind")
        rid = r.get("id")
        if not isinstance(kind, str) or not isinstance(rid, str):
            fail(f"references[{i}] requires string kind and id (RS-3)")
        norm_refs.append({"kind": kind, "id": rid})
    norm_refs.sort(key=lambda x: (x["kind"], x["id"]))

    sess_payload = {
        "session_id": session_id,
        "session_kind": session_kind,
        "notes": notes,
        "references": norm_refs,
    }
    session_sha256 = sha256_text(canonical_json(sess_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **sess_payload,
        "session_sha256": session_sha256,
        "ref_count": len(norm_refs),
        "observational_only": True,
        "no_behavior_tracking": True,
        "no_analytics": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(SESSION_RECORDS / f"{session_id}-{_now()}.json", record)
    append_event(ES_SESSION, {
        "occurred_at_iso": _iso_now(),
        "kind": "reviewer-session-record",
        "session_id": session_id,
        "session_kind": session_kind,
        "ref_count": len(norm_refs),
        "session_sha256": session_sha256,
        "reviewer": reviewer,
    })
    append_audit("reviewer-session-record", reviewer,
                 {"session_id": session_id, "session_kind": session_kind})
    return {"session_id": session_id, "session_sha256": session_sha256, "ref_count": len(norm_refs)}


def handle_production_handoff_record(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "PH-5")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    handoff_id = payload.get("handoff_id")
    from_reviewer = payload.get("from_reviewer")
    to_reviewer = payload.get("to_reviewer")
    package_id = payload.get("package_id")
    stabilization_id = payload.get("stabilization_id")
    deployment_package_id = payload.get("deployment_package_id")
    readiness_audit_id = payload.get("readiness_audit_id")
    activation_id = payload.get("activation_id")
    declared_state = payload.get("activation_state")
    notes = payload.get("notes", "")
    if not handoff_id:
        fail("payload.handoff_id required (PH-1)")
    if find_handoff_record(handoff_id):
        fail(f"handoff_id {handoff_id!r} already exists (PH-1)")
    if not isinstance(from_reviewer, str) or not from_reviewer.strip():
        fail("from_reviewer required (PH-2)")
    if not isinstance(to_reviewer, str) or not to_reviewer.strip():
        fail("to_reviewer required (PH-2)")
    pkg = find_package(package_id) if package_id else None
    if not pkg:
        fail(f"package_id {package_id!r} not found (PH-3)")
    stab = find_stabilization(stabilization_id) if stabilization_id else None
    if not stab:
        fail(f"stabilization_id {stabilization_id!r} not found (PH-3)")
    dp = find_deployment_package(deployment_package_id) if deployment_package_id else None
    if not dp:
        fail(f"deployment_package_id {deployment_package_id!r} not found (PH-3)")
    aud = find_readiness_audit(readiness_audit_id) if readiness_audit_id else None
    if not aud:
        fail(f"readiness_audit_id {readiness_audit_id!r} not found (PH-3)")
    if not isinstance(activation_id, str) or not activation_id.strip():
        fail("activation_id required (PH-4)")
    current_state = latest_activation_state(activation_id)
    if current_state is None:
        fail(f"activation_id {activation_id!r} has no recorded state (PH-4)")
    if declared_state not in ACTIVATION_STATES:
        fail(f"activation_state {declared_state!r} not in {sorted(ACTIVATION_STATES)} (PH-4)")
    if declared_state != current_state:
        fail(f"declared activation_state {declared_state!r} does not match latest recorded state {current_state!r} for activation_id {activation_id!r} (PH-4)")

    handoff_payload = {
        "handoff_id": handoff_id,
        "from_reviewer": from_reviewer,
        "to_reviewer": to_reviewer,
        "package_id": package_id,
        "stabilization_id": stabilization_id,
        "deployment_package_id": deployment_package_id,
        "readiness_audit_id": readiness_audit_id,
        "activation_id": activation_id,
        "activation_state": declared_state,
        "notes": notes,
    }
    handoff_sha256 = sha256_text(canonical_json(handoff_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **handoff_payload,
        "handoff_sha256": handoff_sha256,
        "lineage_pointers": {
            "package_id": package_id,
            "stabilization_id": stabilization_id,
            "deployment_package_id": deployment_package_id,
            "readiness_audit_id": readiness_audit_id,
            "activation_id": activation_id,
            "stable_export_sha256": stab.get("stable_export_sha256"),
            "deployment_package_sha256": dp.get("deployment_package_sha256"),
            "audit_sha256": aud.get("audit_sha256"),
        },
        "append_only": True,
        "no_overwrite_semantics": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(HANDOFF_RECORDS / f"{handoff_id}-{_now()}.json", record)
    append_event(ES_HANDOFF, {
        "occurred_at_iso": _iso_now(),
        "kind": "production-handoff-record",
        "handoff_id": handoff_id,
        "from_reviewer": from_reviewer,
        "to_reviewer": to_reviewer,
        "package_id": package_id,
        "activation_id": activation_id,
        "activation_state": declared_state,
        "handoff_sha256": handoff_sha256,
        "reviewer": reviewer,
    })
    append_audit("production-handoff-record", reviewer,
                 {"handoff_id": handoff_id, "from": from_reviewer, "to": to_reviewer,
                  "activation_state": declared_state})
    return {"handoff_id": handoff_id, "handoff_sha256": handoff_sha256,
            "activation_state": declared_state}


# ============================================================================
# Dispatch table & CLI
# ============================================================================
DISPATCH = {
    "reviewer-guided-workflow": handle_reviewer_guided_workflow,
    "onboarding-sequence-publish": handle_onboarding_sequence_publish,
    "deployment-checklist-publish": handle_deployment_checklist_publish,
    "operational-diagnostics-summary": handle_operational_diagnostics_summary,
    "runtime-navigation-index": handle_runtime_navigation_index,
    "corpus-review-queue": handle_corpus_review_queue,
    "operational-confidence-summary": handle_operational_confidence_summary,
    "reproducibility-proof": handle_reproducibility_proof,
    "reviewer-session-record": handle_reviewer_session_record,
    "production-handoff-record": handle_production_handoff_record,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 58 reviewer operational ergonomics convergence executor")
    parser.add_argument("--kind", required=True, choices=sorted(DISPATCH.keys()))
    parser.add_argument("--request", required=True, help="Path to JSON request envelope")
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args(argv)

    if not args.confirm:
        fail("--confirm required")
    req_path = Path(args.request)
    if not req_path.exists():
        fail(f"request file not found: {req_path}")
    try:
        envelope = json.loads(req_path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"request file not valid JSON: {e}")

    if envelope.get("schema") != SCHEMA:
        fail(f"request schema must be '{SCHEMA}' (got {envelope.get('schema')!r})")
    reviewer = envelope.get("reviewer")
    if not reviewer or not isinstance(reviewer, str):
        fail("reviewer attribution required")
    payload = envelope.get("payload")
    if not isinstance(payload, dict):
        fail("payload must be a dict")
    assert_target_path(payload)

    handler = DISPATCH[args.kind]
    result = handler(reviewer, payload)
    sys.stdout.write(json.dumps({"kind": args.kind, "result": result}, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
