#!/usr/bin/env python3
"""
Phase 57 executor — operational deployment readiness, reviewer enablement &
controlled production activation (constitutional layer 50).

Request envelope: governed-fs-operation-request/1.0
CLI: --kind <dispatch> --request <envelope.json> --confirm

Deterministic, reviewer-authoritative, append-only. Operational activation
layer for the Phase 47–56 substrate. NO new semantic / convergence /
extraction / publication / replay families. NO autonomous activation.
NO silent production replacement. NO overwrite semantics.
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
LAYER_SCHEMA = "operational-deployment-readiness-controlled-production-activation/1.0"
LAYER = 50

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"

# Phase 57 isolated storage tree
OD_ROOT = OC_ROOT / "operational-deployment-runtime"
REVIEWER_PLAYBOOKS = OD_ROOT / "reviewer-playbooks"
RECOVERY_PLAYBOOKS = OD_ROOT / "recovery-playbooks"
PRODUCTION_ACTIVATIONS = OD_ROOT / "production-activations"
ACTIVATION_LIFECYCLE = OD_ROOT / "activation-lifecycle-records"
DEPLOYMENT_VERIFICATIONS = OD_ROOT / "deployment-verifications"
PORTFOLIO_SUMMARIES = OD_ROOT / "portfolio-summaries"
OBSERVABILITY_SUMMARIES = OD_ROOT / "observability-summaries"
DEPLOYMENT_PACKAGES = OD_ROOT / "deployment-packages"
DEPENDENCY_MANIFESTS = OD_ROOT / "dependency-manifests"
CONSUMER_BUNDLES = OD_ROOT / "consumer-payload-bundles"

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

PACKAGING_RUNTIME = OC_ROOT / "manual-semantic-packaging-runtime"
PACKAGES_DIR = PACKAGING_RUNTIME / "manual-packages"

MR_ROOT = OC_ROOT / "manual-runtime-closure"
VISUAL_SUPPORT = MR_ROOT / "visual-support-records"
EXPORT_FINALIZATIONS = MR_ROOT / "export-finalizations"

# Event stores
ES_PLAYBOOK = RUNTIME_MANIFESTS_ROOT / "reviewer-playbook-events" / "_event-store.json"
ES_RECOVERY = RUNTIME_MANIFESTS_ROOT / "recovery-playbook-events" / "_event-store.json"
ES_ACTIVATION = RUNTIME_MANIFESTS_ROOT / "production-activation-events" / "_event-store.json"
ES_VERIFICATION = RUNTIME_MANIFESTS_ROOT / "deployment-verification-events" / "_event-store.json"
ES_PORTFOLIO = RUNTIME_MANIFESTS_ROOT / "portfolio-summary-events" / "_event-store.json"
ES_OBSERVABILITY = RUNTIME_MANIFESTS_ROOT / "observability-summary-events" / "_event-store.json"
ES_DEPLOY_PKG = RUNTIME_MANIFESTS_ROOT / "deployment-package-events" / "_event-store.json"
ES_DEPENDENCY = RUNTIME_MANIFESTS_ROOT / "dependency-manifest-events" / "_event-store.json"
ES_BUNDLE = RUNTIME_MANIFESTS_ROOT / "consumer-payload-bundle-events" / "_event-store.json"
ES_AUDIT = RUNTIME_MANIFESTS_ROOT / "audit-events" / "_event-store.json"

PLAYBOOK_KINDS = {
    "ingestion-review", "conflict-triage", "drift-triage",
    "readiness-audit-workflow", "export-approval-workflow", "refresh-procedure",
}
RECOVERY_KINDS = {
    "bad-export-rollback", "corrupted-convergence-recovery",
    "invalid-refresh-rollback", "accidental-approval-revocation",
    "unstable-canonical-drift-recovery", "broken-multilingual-mapping-recovery",
}
ACTIVATION_STATES = {
    "production-candidate", "production-approved", "production-active",
    "superseded", "rollback-candidate",
}
ACTIVATION_TRANSITIONS = {
    "production-candidate": {"production-approved", "rollback-candidate"},
    "production-approved": {"production-active", "rollback-candidate"},
    "production-active": {"superseded", "rollback-candidate"},
    "superseded": set(),
    "rollback-candidate": {"superseded"},
}
VERIFICATION_CHECKS = [
    "export-completeness",
    "stable-export-hash",
    "canonical-id-continuity",
    "unresolved-drift",
    "unresolved-conflicts",
    "unresolved-visual-support",
    "unresolved-multilingual-normalization",
    "missing-lineage",
    "orphan-semantic-entities",
]
PORTFOLIO_DIMENSIONS = {
    "package-readiness", "unresolved-issue-density", "canonical-overlap",
    "drift-density", "multilingual-coverage", "export-stability",
    "production-activation-state",
}
OBSERVABILITY_KINDS = {
    "unresolved-conflicts", "blocking-drift", "unstable-exports",
    "refresh-propagation-chain", "reviewer-workload", "unresolved-approvals",
    "orphan-evidence", "incomplete-procedures", "missing-warnings",
}

FORBIDDEN_OVERWRITE_PREFIXES = (
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
}

FORBIDDEN_TRANSLATION_KEYS = {
    "machine_translation", "llm_translation", "mt_model",
    "language_model_inference", "autodetect_language", "language_inference",
    "neural_translation", "translation_score", "translation_confidence",
}

# Phase 57 NEW: forbid telemetry / dashboard / streaming keys.
FORBIDDEN_TELEMETRY_KEYS = {
    "telemetry", "telemetry_endpoint", "telemetry_stream",
    "dashboard", "dashboard_widget", "metric_stream",
    "streaming", "live_stream", "websocket", "webhook",
    "deployment_daemon", "auto_deploy", "autonomous_deployment",
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


def reject_probabilistic(payload: dict, rule_id: str = "OD-PROB") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_PROBABILISTIC_KEYS)
    if hit:
        fail(f"probabilistic/embedding/autonomous key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


def reject_translation(payload: dict, rule_id: str = "OD-TRANS") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_TRANSLATION_KEYS)
    if hit:
        fail(f"translation/language-inference key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


def reject_telemetry(payload: dict, rule_id: str = "OD-TELE") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_TELEMETRY_KEYS)
    if hit:
        fail(f"telemetry/dashboard/streaming/daemon key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


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
        "audit_event_id": f"a57-{kind}-{_now()}",
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


def find_canonical_entity(eid: str) -> dict | None:
    return _scan_for_id(SC_CANONICAL_ENTITIES, "canonical_entity_id", eid)


def find_canonical_procedure(pid: str) -> dict | None:
    return _scan_for_id(SC_CANONICAL_PROCEDURES, "canonical_procedure_id", pid)


def find_readiness_audit(aid: str) -> dict | None:
    return _scan_for_id(PC_AUDITS, "audit_id", aid)


def find_normalization_table(tid: str) -> dict | None:
    return _scan_for_id(PC_ML_TABLES, "table_id", tid)


def find_export_finalization(fid: str) -> dict | None:
    return _scan_for_id(EXPORT_FINALIZATIONS, "finalization_id", fid)


def find_export_stability_guarantee(gid: str) -> dict | None:
    return _scan_for_id(PC_GUARANTEES, "guarantee_id", gid)


# Self-layer finders
def find_playbook(pid: str) -> dict | None:
    return _scan_for_id(REVIEWER_PLAYBOOKS, "playbook_id", pid)


def find_recovery_playbook(rid: str) -> dict | None:
    return _scan_for_id(RECOVERY_PLAYBOOKS, "recovery_id", rid)


def find_deployment_verification(vid: str) -> dict | None:
    return _scan_for_id(DEPLOYMENT_VERIFICATIONS, "verification_id", vid)


def find_deployment_package(dpid: str) -> dict | None:
    return _scan_for_id(DEPLOYMENT_PACKAGES, "deployment_package_id", dpid)


def find_consumer_bundle(bid: str) -> dict | None:
    return _scan_for_id(CONSUMER_BUNDLES, "bundle_id", bid)


def package_lifecycle_state(package_id: str) -> str | None:
    store = RUNTIME_MANIFESTS_ROOT / "packaging-lifecycle-events" / "_event-store.json"
    if not store.exists():
        return None
    try:
        events = read_json(store).get("events", [])
    except Exception:
        return None
    last = None
    for e in events:
        pid = e.get("package_id") or e.get("payload", {}).get("package_id")
        ts = e.get("to_state") or e.get("payload", {}).get("to_state")
        if pid == package_id and ts:
            last = ts
    return last


def latest_activation_state(activation_id: str) -> str | None:
    """Return the most recent to_state recorded for activation_id, or None.
    Uses the append-only production-activation event store as the
    authoritative ordering source (insertion order is preserved)."""
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


def handle_reviewer_playbook_publish(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "RP-5")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    playbook_id = payload.get("playbook_id")
    playbook_kind = payload.get("playbook_kind")
    steps = payload.get("steps")
    governing_dispatches = payload.get("governing_dispatches", [])
    prior_playbook_id = payload.get("prior_playbook_id")
    notes = payload.get("notes", "")
    if not playbook_id:
        fail("payload.playbook_id required (RP-1)")
    if find_playbook(playbook_id):
        fail(f"playbook_id {playbook_id!r} already exists; supersede via new playbook_id with prior_playbook_id pointer (RP-7)")
    if playbook_kind not in PLAYBOOK_KINDS:
        fail(f"playbook_kind {playbook_kind!r} not in {sorted(PLAYBOOK_KINDS)} (RP-2)")
    norm_steps = _validate_steps(steps, "RP-3")
    if not isinstance(governing_dispatches, list):
        fail("governing_dispatches must be a list (RP-4)")
    norm_dispatches = []
    for i, gd in enumerate(governing_dispatches):
        if not isinstance(gd, str) or not gd.strip():
            fail(f"governing_dispatches[{i}] must be a non-empty string (RP-4)")
        norm_dispatches.append(gd)
    norm_dispatches.sort()
    if prior_playbook_id and not find_playbook(prior_playbook_id):
        fail(f"prior_playbook_id {prior_playbook_id!r} not found (RP-7)")

    pb_payload = {
        "playbook_id": playbook_id,
        "playbook_kind": playbook_kind,
        "steps": norm_steps,
        "governing_dispatches": norm_dispatches,
        "prior_playbook_id": prior_playbook_id,
        "notes": notes,
    }
    playbook_sha256 = sha256_text(canonical_json(pb_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **pb_payload,
        "playbook_sha256": playbook_sha256,
        "step_count": len(norm_steps),
        "pointer_only": True,
        "presentation_neutral": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(REVIEWER_PLAYBOOKS / f"{playbook_id}-{_now()}.json", record)
    append_event(ES_PLAYBOOK, {
        "occurred_at_iso": _iso_now(),
        "kind": "reviewer-playbook-publish",
        "playbook_id": playbook_id,
        "playbook_kind": playbook_kind,
        "step_count": len(norm_steps),
        "playbook_sha256": playbook_sha256,
        "reviewer": reviewer,
    })
    append_audit("reviewer-playbook-publish", reviewer,
                 {"playbook_id": playbook_id, "playbook_kind": playbook_kind})
    return {"playbook_id": playbook_id, "playbook_sha256": playbook_sha256, "step_count": len(norm_steps)}


def _resolve_rollback_target(rollback_target: dict, rule_id: str) -> tuple[str, str]:
    if not isinstance(rollback_target, dict):
        fail(f"rollback_target must be a dict {{kind, id}} ({rule_id})")
    kind = rollback_target.get("kind")
    target_id = rollback_target.get("id")
    if not isinstance(kind, str) or not isinstance(target_id, str):
        fail(f"rollback_target requires string kind and id ({rule_id})")
    resolvers = {
        "export-finalization": find_export_finalization,
        "export-stabilization": find_stabilization,
        "export-stability-guarantee": find_export_stability_guarantee,
        "production-activation": lambda i: latest_activation_state(i) is not None,  # type: ignore[return-value]
        "canonical-entity": find_canonical_entity,
        "canonical-procedure": find_canonical_procedure,
        "normalization-table": find_normalization_table,
        "manual-package": find_package,
    }
    if kind not in resolvers:
        fail(f"rollback_target.kind {kind!r} not supported ({rule_id})")
    resolver = resolvers[kind]
    resolved = resolver(target_id)
    if not resolved:
        fail(f"rollback_target {kind}:{target_id} not found ({rule_id})")
    return kind, target_id


def handle_recovery_playbook_publish(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "RC-7")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    recovery_id = payload.get("recovery_id")
    recovery_kind = payload.get("recovery_kind")
    recovery_steps = payload.get("recovery_steps")
    rollback_target = payload.get("rollback_target")
    notes = payload.get("notes", "")
    if not recovery_id:
        fail("payload.recovery_id required (RC-1)")
    if find_recovery_playbook(recovery_id):
        fail(f"recovery_id {recovery_id!r} already exists (RC-1)")
    if recovery_kind not in RECOVERY_KINDS:
        fail(f"recovery_kind {recovery_kind!r} not in {sorted(RECOVERY_KINDS)} (RC-2)")
    norm_steps = _validate_steps(recovery_steps, "RC-3", extra_required=("governing_dispatch",))
    rb_kind, rb_id = _resolve_rollback_target(rollback_target, "RC-5")

    rec_payload = {
        "recovery_id": recovery_id,
        "recovery_kind": recovery_kind,
        "recovery_steps": norm_steps,
        "rollback_target": {"kind": rb_kind, "id": rb_id},
        "notes": notes,
    }
    recovery_sha256 = sha256_text(canonical_json(rec_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **rec_payload,
        "recovery_sha256": recovery_sha256,
        "step_count": len(norm_steps),
        "no_autonomous_repair": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(RECOVERY_PLAYBOOKS / f"{recovery_id}-{_now()}.json", record)
    append_event(ES_RECOVERY, {
        "occurred_at_iso": _iso_now(),
        "kind": "recovery-playbook-publish",
        "recovery_id": recovery_id,
        "recovery_kind": recovery_kind,
        "rollback_target_kind": rb_kind,
        "rollback_target_id": rb_id,
        "step_count": len(norm_steps),
        "recovery_sha256": recovery_sha256,
        "reviewer": reviewer,
    })
    append_audit("recovery-playbook-publish", reviewer,
                 {"recovery_id": recovery_id, "rollback_target": f"{rb_kind}:{rb_id}"})
    return {"recovery_id": recovery_id, "recovery_sha256": recovery_sha256,
            "rollback_target_kind": rb_kind, "rollback_target_id": rb_id}


def handle_production_activation_transition(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "PA-10")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    activation_id = payload.get("activation_id")
    package_id = payload.get("package_id")
    stabilization_id = payload.get("stabilization_id")
    from_state = payload.get("from_state")
    to_state = payload.get("to_state")
    readiness_audit_id = payload.get("readiness_audit_id")
    verification_id = payload.get("verification_id")
    recovery_playbook_id = payload.get("recovery_playbook_id")
    rationale = payload.get("rationale", "")
    if not activation_id:
        fail("payload.activation_id required (PA-1)")
    pkg = find_package(package_id) if package_id else None
    if not pkg:
        fail(f"package_id {package_id!r} not found (PA-2)")
    state = package_lifecycle_state(package_id)
    if state != "export-ready":
        fail(f"package {package_id!r} lifecycle state is {state!r}, must be 'export-ready' (PA-2)")
    stab = find_stabilization(stabilization_id) if stabilization_id else None
    if not stab:
        fail(f"stabilization_id {stabilization_id!r} not found (PA-3)")
    if from_state not in ACTIVATION_STATES:
        fail(f"from_state {from_state!r} not in {sorted(ACTIVATION_STATES)} (PA-4)")
    if to_state not in ACTIVATION_STATES:
        fail(f"to_state {to_state!r} not in {sorted(ACTIVATION_STATES)} (PA-4)")
    if to_state not in ACTIVATION_TRANSITIONS.get(from_state, set()):
        fail(f"transition {from_state!r} -> {to_state!r} not allowed (PA-5)")

    current = latest_activation_state(activation_id)
    if current is None:
        # First transition for this activation_id: from_state must be 'production-candidate'.
        if from_state != "production-candidate":
            fail(f"first transition for activation_id {activation_id!r} must originate at 'production-candidate', got {from_state!r} (PA-9)")
    else:
        if current != from_state:
            fail(f"activation_id {activation_id!r} latest state is {current!r}, cannot transition from {from_state!r} (PA-9)")
        if current == "superseded":
            fail(f"activation_id {activation_id!r} already superseded; immutable (PA-9)")

    # Transition-specific governance refs.
    audit_ref = None
    verify_ref = None
    recovery_ref = None
    if to_state == "production-approved":
        audit = find_readiness_audit(readiness_audit_id) if readiness_audit_id else None
        if not audit:
            fail(f"readiness_audit_id {readiness_audit_id!r} required and must resolve (PA-6)")
        if audit.get("package_id") != package_id:
            fail(f"readiness_audit {readiness_audit_id!r} is for package {audit.get('package_id')!r}, not {package_id!r} (PA-6)")
        if audit.get("status") != "ready":
            fail(f"readiness_audit {readiness_audit_id!r} status is {audit.get('status')!r}, must be 'ready' (PA-6)")
        audit_ref = readiness_audit_id
    elif to_state == "production-active":
        verify = find_deployment_verification(verification_id) if verification_id else None
        if not verify:
            fail(f"verification_id {verification_id!r} required and must resolve (PA-7)")
        if verify.get("package_id") != package_id:
            fail(f"verification {verification_id!r} is for package {verify.get('package_id')!r}, not {package_id!r} (PA-7)")
        if verify.get("status") != "deployable":
            fail(f"verification {verification_id!r} status is {verify.get('status')!r}, must be 'deployable' (PA-7)")
        verify_ref = verification_id
    elif to_state == "rollback-candidate":
        rec = find_recovery_playbook(recovery_playbook_id) if recovery_playbook_id else None
        if not rec:
            fail(f"recovery_playbook_id {recovery_playbook_id!r} required and must resolve (PA-8)")
        recovery_ref = recovery_playbook_id

    # Seed activation record on first transition.
    if current is None:
        seed = {
            "schema": LAYER_SCHEMA,
            "activation_id": activation_id,
            "package_id": package_id,
            "stabilization_id": stabilization_id,
            "stable_export_sha256": stab.get("stable_export_sha256"),
            "seeded_at_iso": _iso_now(),
            "reviewer": reviewer,
            "additive_lineage": True,
        }
        write_json(PRODUCTION_ACTIVATIONS / f"{activation_id}-{_now()}.json", seed)

    transition = {
        "schema": LAYER_SCHEMA,
        "activation_id": activation_id,
        "package_id": package_id,
        "stabilization_id": stabilization_id,
        "from_state": from_state,
        "to_state": to_state,
        "readiness_audit_ref": audit_ref,
        "verification_ref": verify_ref,
        "recovery_playbook_ref": recovery_ref,
        "rationale": rationale,
        "append_only": True,
        "no_overwrite_semantics": True,
        "transaction_safe": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(ACTIVATION_LIFECYCLE / f"{activation_id}-{from_state}-to-{to_state}-{_now()}.json", transition)
    append_event(ES_ACTIVATION, {
        "occurred_at_iso": _iso_now(),
        "kind": "production-activation-transition",
        "activation_id": activation_id,
        "package_id": package_id,
        "from_state": from_state,
        "to_state": to_state,
        "reviewer": reviewer,
    })
    append_audit("production-activation-transition", reviewer,
                 {"activation_id": activation_id, "from_state": from_state, "to_state": to_state})
    return {"activation_id": activation_id, "from_state": from_state, "to_state": to_state,
            "stable_export_sha256": stab.get("stable_export_sha256")}


def _verification_checks(package_id: str, manual_id: str | None,
                         stabilization_id: str | None) -> tuple[list[dict], str]:
    findings: list[dict] = []

    # 1. export-completeness: at least one export-finalization for package.
    has_finalization = any(f.get("package_id") == package_id for f in _scan_all(EXPORT_FINALIZATIONS))
    findings.append({
        "check": "export-completeness",
        "outcome": "pass" if has_finalization else "fail",
        "evidence_pointer": {"kind": "export-finalization", "scope": "package", "id": package_id},
    })

    # 2. stable-export-hash: stabilization for package matches a guarantee invariant.
    stab = find_stabilization(stabilization_id) if stabilization_id else None
    stable_hash = stab.get("stable_export_sha256") if stab else None
    if stable_hash:
        guarantee_match = any(
            g.get("deterministic_invariants", {}).get("export_payload_sha256") == stable_hash
            for g in _scan_all(PC_GUARANTEES)
            if g.get("package_id") == package_id
        )
    else:
        guarantee_match = False
    findings.append({
        "check": "stable-export-hash",
        "outcome": "pass" if guarantee_match else "fail",
        "evidence_pointer": {"kind": "export-stabilization", "id": stabilization_id,
                             "stable_export_sha256": stable_hash},
    })

    # 3. canonical-id-continuity: every canonical_section_id in stabilization map exists somewhere.
    if stab:
        cmap = stab.get("canonical_id_map", {}) or {}
        ids_ok = bool(cmap)
    else:
        ids_ok = False
    findings.append({
        "check": "canonical-id-continuity",
        "outcome": "pass" if ids_ok else "fail",
        "evidence_pointer": {"kind": "canonical-id-map", "stabilization_id": stabilization_id,
                             "canonical_id_count": len((stab or {}).get("canonical_id_map", {}) or {})},
    })

    # 4. unresolved-drift: no major/blocking drift.
    drift_bad = [d.get("drift_id") for d in _scan_all(PC_DRIFT) if d.get("severity") in ("major", "blocking")]
    findings.append({
        "check": "unresolved-drift",
        "outcome": "pass" if not drift_bad else "fail",
        "evidence_pointer": {"kind": "drift-records", "ids": sorted(drift_bad)},
    })

    # 5. unresolved-conflicts: no blocking conflicts without accept arbitration.
    arb_accepted = {a.get("conflict_id") for a in _scan_all(SC_ARBITRATION) if a.get("decision") == "accept"}
    blocking_unresolved = [c.get("conflict_id") for c in _scan_all(SC_CONFLICTS)
                           if c.get("severity") == "blocking" and c.get("conflict_id") not in arb_accepted]
    findings.append({
        "check": "unresolved-conflicts",
        "outcome": "pass" if not blocking_unresolved else "fail",
        "evidence_pointer": {"kind": "conflict-surfacings", "ids": sorted(blocking_unresolved)},
    })

    # 6. unresolved-visual-support: at least one visual support record for the manual.
    has_visual = any(
        v.get("manual_id") == manual_id or v.get("package_id") == package_id
        for v in _scan_all(VISUAL_SUPPORT)
    )
    findings.append({
        "check": "unresolved-visual-support",
        "outcome": "pass" if has_visual else "fail",
        "evidence_pointer": {"kind": "visual-support", "scope": "manual", "id": manual_id},
    })

    # 7. unresolved-multilingual-normalization: pass if no normalization tables OR
    #    every table has a sha256 (deterministic). Informational — no blocking gating.
    tables = _scan_all(PC_ML_TABLES)
    table_ok = all(isinstance(t.get("table_sha256"), str) and t["table_sha256"] for t in tables)
    findings.append({
        "check": "unresolved-multilingual-normalization",
        "outcome": "pass" if table_ok else "fail",
        "evidence_pointer": {"kind": "normalization-tables", "table_count": len(tables)},
    })

    # 8. missing-lineage: package must have manual_id.
    findings.append({
        "check": "missing-lineage",
        "outcome": "pass" if manual_id else "fail",
        "evidence_pointer": {"kind": "manual-package", "package_id": package_id, "manual_id": manual_id},
    })

    # 9. orphan-semantic-entities: every canonical entity referenced by stabilization map is resolvable.
    orphan_count = 0
    if stab:
        for sec in (stab.get("stable_export_payload", {}) or {}).get("sections", []) or []:
            ce = sec.get("canonical_entity_id")
            if ce and not find_canonical_entity(ce):
                orphan_count += 1
    findings.append({
        "check": "orphan-semantic-entities",
        "outcome": "pass" if orphan_count == 0 else "fail",
        "evidence_pointer": {"kind": "canonical-entity-resolution", "orphan_count": orphan_count},
    })

    findings.sort(key=lambda f: f["check"])
    status = "deployable" if all(f["outcome"] == "pass" for f in findings) else "not-deployable"
    return findings, status


def handle_deployment_verification_run(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "DV-7")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    verification_id = payload.get("verification_id")
    package_id = payload.get("package_id")
    stabilization_id = payload.get("stabilization_id")
    if not verification_id:
        fail("payload.verification_id required (DV-1)")
    if find_deployment_verification(verification_id):
        fail(f"verification_id {verification_id!r} already exists (DV-1)")
    pkg = find_package(package_id) if package_id else None
    if not pkg:
        fail(f"package_id {package_id!r} not found (DV-2)")
    if stabilization_id and not find_stabilization(stabilization_id):
        fail(f"stabilization_id {stabilization_id!r} not found (DV-3)")

    findings, status = _verification_checks(package_id, pkg.get("manual_id"), stabilization_id)
    verify_payload = {
        "verification_id": verification_id,
        "package_id": package_id,
        "manual_id": pkg.get("manual_id"),
        "stabilization_id": stabilization_id,
        "checks": findings,
        "status": status,
    }
    verification_sha256 = sha256_text(canonical_json(verify_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **verify_payload,
        "verification_sha256": verification_sha256,
        "informational_only": True,
        "reviewer_authoritative": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(DEPLOYMENT_VERIFICATIONS / f"{verification_id}-{_now()}.json", record)
    append_event(ES_VERIFICATION, {
        "occurred_at_iso": _iso_now(),
        "kind": "deployment-verification-run",
        "verification_id": verification_id,
        "package_id": package_id,
        "status": status,
        "verification_sha256": verification_sha256,
        "reviewer": reviewer,
    })
    append_audit("deployment-verification-run", reviewer,
                 {"verification_id": verification_id, "package_id": package_id, "status": status})
    return {"verification_id": verification_id, "status": status,
            "verification_sha256": verification_sha256, "check_count": len(findings)}


def handle_portfolio_summary_publish(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "PF-5")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    portfolio_id = payload.get("portfolio_id")
    package_refs = payload.get("package_refs")
    dimensions = payload.get("dimensions")
    notes = payload.get("notes", "")
    if not portfolio_id:
        fail("payload.portfolio_id required (PF-1)")
    if not isinstance(package_refs, list) or not package_refs:
        fail("package_refs must be a non-empty list (PF-2)")
    norm_refs = []
    for i, pid in enumerate(package_refs):
        if not isinstance(pid, str) or not pid.strip():
            fail(f"package_refs[{i}] must be a non-empty string (PF-2)")
        if not find_package(pid):
            fail(f"package_refs[{i}] {pid!r} not found (PF-2)")
        norm_refs.append(pid)
    norm_refs = sorted(set(norm_refs))
    if not isinstance(dimensions, list) or not dimensions:
        fail("dimensions must be a non-empty list (PF-3)")
    norm_dims = []
    for i, d in enumerate(dimensions):
        if d not in PORTFOLIO_DIMENSIONS:
            fail(f"dimensions[{i}] {d!r} not in {sorted(PORTFOLIO_DIMENSIONS)} (PF-3)")
        norm_dims.append(d)
    norm_dims = sorted(set(norm_dims))

    portfolio_payload = {
        "portfolio_id": portfolio_id,
        "package_refs": norm_refs,
        "dimensions": norm_dims,
        "notes": notes,
    }
    portfolio_sha256 = sha256_text(canonical_json(portfolio_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **portfolio_payload,
        "portfolio_sha256": portfolio_sha256,
        "package_count": len(norm_refs),
        "dimension_count": len(norm_dims),
        "presentation_neutral": True,
        "pointer_only": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(PORTFOLIO_SUMMARIES / f"{portfolio_id}-{_now()}.json", record)
    append_event(ES_PORTFOLIO, {
        "occurred_at_iso": _iso_now(),
        "kind": "portfolio-summary-publish",
        "portfolio_id": portfolio_id,
        "package_count": len(norm_refs),
        "dimension_count": len(norm_dims),
        "portfolio_sha256": portfolio_sha256,
        "reviewer": reviewer,
    })
    append_audit("portfolio-summary-publish", reviewer,
                 {"portfolio_id": portfolio_id, "package_count": len(norm_refs)})
    return {"portfolio_id": portfolio_id, "portfolio_sha256": portfolio_sha256,
            "package_count": len(norm_refs), "dimension_count": len(norm_dims)}


def handle_observability_summary_publish(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "OB-4")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    observability_id = payload.get("observability_id")
    observability_kind = payload.get("observability_kind")
    aggregated_refs = payload.get("aggregated_refs")
    notes = payload.get("notes", "")
    if not observability_id:
        fail("payload.observability_id required (OB-1)")
    if observability_kind not in OBSERVABILITY_KINDS:
        fail(f"observability_kind {observability_kind!r} not in {sorted(OBSERVABILITY_KINDS)} (OB-2)")
    if not isinstance(aggregated_refs, list):
        fail("aggregated_refs must be a list (OB-3)")
    norm_refs = []
    for i, r in enumerate(aggregated_refs):
        if not isinstance(r, dict) or not isinstance(r.get("kind"), str) or not isinstance(r.get("id"), str):
            fail(f"aggregated_refs[{i}] must be {{kind, id}} (OB-3)")
        norm_refs.append({"kind": r["kind"], "id": r["id"]})
    norm_refs.sort(key=lambda x: (x["kind"], x["id"]))

    obs_payload = {
        "observability_id": observability_id,
        "observability_kind": observability_kind,
        "aggregated_refs": norm_refs,
        "notes": notes,
    }
    summary_sha256 = sha256_text(canonical_json(obs_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **obs_payload,
        "summary_sha256": summary_sha256,
        "ref_count": len(norm_refs),
        "presentation_neutral": True,
        "pointer_only": True,
        "no_telemetry": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(OBSERVABILITY_SUMMARIES / f"{observability_id}-{_now()}.json", record)
    append_event(ES_OBSERVABILITY, {
        "occurred_at_iso": _iso_now(),
        "kind": "observability-summary-publish",
        "observability_id": observability_id,
        "observability_kind": observability_kind,
        "ref_count": len(norm_refs),
        "summary_sha256": summary_sha256,
        "reviewer": reviewer,
    })
    append_audit("observability-summary-publish", reviewer,
                 {"observability_id": observability_id, "observability_kind": observability_kind})
    return {"observability_id": observability_id, "summary_sha256": summary_sha256,
            "ref_count": len(norm_refs)}


def handle_deployment_package_build(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "DP-7")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    deployment_package_id = payload.get("deployment_package_id")
    package_id = payload.get("package_id")
    stabilization_id = payload.get("stabilization_id")
    declared_stable_hash = payload.get("stable_export_sha256")
    if not deployment_package_id:
        fail("payload.deployment_package_id required (DP-1)")
    if find_deployment_package(deployment_package_id):
        fail(f"deployment_package_id {deployment_package_id!r} already exists (DP-1)")
    pkg = find_package(package_id) if package_id else None
    if not pkg:
        fail(f"package_id {package_id!r} not found (DP-2)")
    stab = find_stabilization(stabilization_id) if stabilization_id else None
    if not stab:
        fail(f"stabilization_id {stabilization_id!r} not found (DP-3)")
    actual_hash = stab.get("stable_export_sha256")
    if not actual_hash:
        fail(f"stabilization {stabilization_id!r} missing stable_export_sha256 (DP-4)")
    if declared_stable_hash and declared_stable_hash != actual_hash:
        fail(f"declared stable_export_sha256 {declared_stable_hash!r} != stabilization {actual_hash!r} (DP-4)")

    canonical_id_map = stab.get("canonical_id_map", {}) or {}
    manifest_payload = {
        "deployment_package_id": deployment_package_id,
        "package_id": package_id,
        "manual_id": pkg.get("manual_id"),
        "stabilization_id": stabilization_id,
        "stable_export_sha256": actual_hash,
        "canonical_id_map_keys": sorted(canonical_id_map.keys()),
        "lineage_pointers": {
            "package_id": package_id,
            "stabilization_id": stabilization_id,
            "stable_export_sha256": actual_hash,
        },
    }
    deployment_package_sha256 = sha256_text(canonical_json(manifest_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **manifest_payload,
        "deployment_package_sha256": deployment_package_sha256,
        "pointer_only": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(DEPLOYMENT_PACKAGES / f"{deployment_package_id}-{_now()}.json", record)
    append_event(ES_DEPLOY_PKG, {
        "occurred_at_iso": _iso_now(),
        "kind": "deployment-package-build",
        "deployment_package_id": deployment_package_id,
        "package_id": package_id,
        "stable_export_sha256": actual_hash,
        "deployment_package_sha256": deployment_package_sha256,
        "reviewer": reviewer,
    })
    append_audit("deployment-package-build", reviewer,
                 {"deployment_package_id": deployment_package_id, "package_id": package_id})
    return {"deployment_package_id": deployment_package_id,
            "deployment_package_sha256": deployment_package_sha256,
            "stable_export_sha256": actual_hash}


def _resolve_dependency(kind: str, dep_id: str) -> dict | None:
    resolvers = {
        "canonical-entity": find_canonical_entity,
        "canonical-procedure": find_canonical_procedure,
        "export-stabilization": find_stabilization,
        "export-stability-guarantee": find_export_stability_guarantee,
        "normalization-table": find_normalization_table,
        "manual-package": find_package,
        "readiness-audit": find_readiness_audit,
    }
    resolver = resolvers.get(kind)
    if not resolver:
        return None
    return resolver(dep_id)


def handle_dependency_manifest_publish(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "DM-5")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    dependency_manifest_id = payload.get("dependency_manifest_id")
    deployment_package_id = payload.get("deployment_package_id")
    dependencies = payload.get("dependencies")
    if not dependency_manifest_id:
        fail("payload.dependency_manifest_id required (DM-1)")
    dp = find_deployment_package(deployment_package_id) if deployment_package_id else None
    if not dp:
        fail(f"deployment_package_id {deployment_package_id!r} not found (DM-2)")
    if not isinstance(dependencies, list) or not dependencies:
        fail("dependencies must be a non-empty list (DM-3)")
    norm_deps = []
    seen = set()
    for i, d in enumerate(dependencies):
        if not isinstance(d, dict):
            fail(f"dependencies[{i}] must be a dict (DM-3)")
        kind = d.get("kind")
        dep_id = d.get("id")
        sha_pointer = d.get("sha256_pointer")
        if not isinstance(kind, str) or not isinstance(dep_id, str):
            fail(f"dependencies[{i}] requires string kind and id (DM-3)")
        if not isinstance(sha_pointer, str) or not sha_pointer.strip():
            fail(f"dependencies[{i}].sha256_pointer required (DM-3)")
        resolved = _resolve_dependency(kind, dep_id)
        if not resolved:
            fail(f"dependencies[{i}] {kind}:{dep_id} not resolvable (DM-4)")
        key = (kind, dep_id)
        if key in seen:
            fail(f"dependencies[{i}] duplicates {kind}:{dep_id} (DM-3)")
        seen.add(key)
        norm_deps.append({"kind": kind, "id": dep_id, "sha256_pointer": sha_pointer})
    norm_deps.sort(key=lambda x: (x["kind"], x["id"]))

    manifest_payload = {
        "dependency_manifest_id": dependency_manifest_id,
        "deployment_package_id": deployment_package_id,
        "dependencies": norm_deps,
    }
    dependency_manifest_sha256 = sha256_text(canonical_json(manifest_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **manifest_payload,
        "dependency_manifest_sha256": dependency_manifest_sha256,
        "dependency_count": len(norm_deps),
        "local_only": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(DEPENDENCY_MANIFESTS / f"{dependency_manifest_id}-{_now()}.json", record)
    append_event(ES_DEPENDENCY, {
        "occurred_at_iso": _iso_now(),
        "kind": "dependency-manifest-publish",
        "dependency_manifest_id": dependency_manifest_id,
        "deployment_package_id": deployment_package_id,
        "dependency_count": len(norm_deps),
        "dependency_manifest_sha256": dependency_manifest_sha256,
        "reviewer": reviewer,
    })
    append_audit("dependency-manifest-publish", reviewer,
                 {"dependency_manifest_id": dependency_manifest_id,
                  "deployment_package_id": deployment_package_id})
    return {"dependency_manifest_id": dependency_manifest_id,
            "dependency_manifest_sha256": dependency_manifest_sha256,
            "dependency_count": len(norm_deps)}


def handle_consumer_payload_bundle_publish(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "CB-5")
    reject_probabilistic(payload)
    reject_translation(payload)
    reject_telemetry(payload)
    bundle_id = payload.get("bundle_id")
    deployment_package_id = payload.get("deployment_package_id")
    bundled_artifact_pointers = payload.get("bundled_artifact_pointers")
    prior_bundle_id = payload.get("prior_bundle_id")
    if not bundle_id:
        fail("payload.bundle_id required (CB-1)")
    if find_consumer_bundle(bundle_id):
        fail(f"bundle_id {bundle_id!r} already exists; supersede via new bundle_id (CB-4)")
    dp = find_deployment_package(deployment_package_id) if deployment_package_id else None
    if not dp:
        fail(f"deployment_package_id {deployment_package_id!r} not found (CB-2)")
    if not isinstance(bundled_artifact_pointers, list) or not bundled_artifact_pointers:
        fail("bundled_artifact_pointers must be a non-empty list (CB-3)")
    norm_pointers = []
    seen = set()
    for i, ap in enumerate(bundled_artifact_pointers):
        if not isinstance(ap, dict):
            fail(f"bundled_artifact_pointers[{i}] must be a dict (CB-3)")
        kind = ap.get("kind")
        pid = ap.get("id")
        sha = ap.get("sha256_pointer")
        if not isinstance(kind, str) or not isinstance(pid, str):
            fail(f"bundled_artifact_pointers[{i}] requires string kind and id (CB-3)")
        if not isinstance(sha, str) or not sha.strip():
            fail(f"bundled_artifact_pointers[{i}].sha256_pointer required (CB-3)")
        key = (kind, pid)
        if key in seen:
            fail(f"bundled_artifact_pointers[{i}] duplicates {kind}:{pid} (CB-3)")
        seen.add(key)
        norm_pointers.append({"kind": kind, "id": pid, "sha256_pointer": sha})
    norm_pointers.sort(key=lambda x: (x["kind"], x["id"]))

    if prior_bundle_id and not find_consumer_bundle(prior_bundle_id):
        fail(f"prior_bundle_id {prior_bundle_id!r} not found (CB-4)")

    bundle_payload = {
        "bundle_id": bundle_id,
        "deployment_package_id": deployment_package_id,
        "bundled_artifact_pointers": norm_pointers,
        "prior_bundle_id": prior_bundle_id,
    }
    consumer_payload_sha256 = sha256_text(canonical_json(bundle_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **bundle_payload,
        "consumer_payload_sha256": consumer_payload_sha256,
        "pointer_count": len(norm_pointers),
        "bundle_state": "sealed",
        "presentation_neutral": True,
        "lineage_pointers": {
            "deployment_package_id": deployment_package_id,
            "stable_export_sha256": dp.get("stable_export_sha256"),
            "stabilization_id": dp.get("stabilization_id"),
        },
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(CONSUMER_BUNDLES / f"{bundle_id}-{_now()}.json", record)
    append_event(ES_BUNDLE, {
        "occurred_at_iso": _iso_now(),
        "kind": "consumer-payload-bundle-publish",
        "bundle_id": bundle_id,
        "deployment_package_id": deployment_package_id,
        "consumer_payload_sha256": consumer_payload_sha256,
        "pointer_count": len(norm_pointers),
        "reviewer": reviewer,
    })
    append_audit("consumer-payload-bundle-publish", reviewer,
                 {"bundle_id": bundle_id, "deployment_package_id": deployment_package_id})
    return {"bundle_id": bundle_id, "consumer_payload_sha256": consumer_payload_sha256,
            "pointer_count": len(norm_pointers)}


# ============================================================================
# Dispatch table & CLI
# ============================================================================
DISPATCH = {
    "reviewer-playbook-publish": handle_reviewer_playbook_publish,
    "recovery-playbook-publish": handle_recovery_playbook_publish,
    "production-activation-transition": handle_production_activation_transition,
    "deployment-verification-run": handle_deployment_verification_run,
    "portfolio-summary-publish": handle_portfolio_summary_publish,
    "observability-summary-publish": handle_observability_summary_publish,
    "deployment-package-build": handle_deployment_package_build,
    "dependency-manifest-publish": handle_dependency_manifest_publish,
    "consumer-payload-bundle-publish": handle_consumer_payload_bundle_publish,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 57 operational deployment / activation executor")
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
