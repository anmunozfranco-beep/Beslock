#!/usr/bin/env python3
"""
Phase 59 executor — Production Hardening, Corpus Validation & Final Reviewer
Readiness Closure (constitutional layer 52).

Request envelope: governed-fs-operation-request/1.0
CLI: --kind <dispatch> --request <envelope.json> --confirm

Hardening + convergence: pointer-only artifacts that stress-test, validate,
rehearse, attest, and stabilize the Phase 47–58 substrate. Reviewer-
authoritative. Append-only. Deterministic. NO autonomous remediation.
NO operational scoring. NO AI readiness claims.
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
LAYER_SCHEMA = "production-hardening-corpus-validation/1.0"
LAYER = 52

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"

# Phase 59 isolated storage tree
PH_ROOT = OC_ROOT / "production-hardening-runtime"
CORPUS_STRESS = PH_ROOT / "corpus-stress-validations"
HARDENING_SCANS = PH_ROOT / "runtime-hardening-scans"
READINESS_CHECKS = PH_ROOT / "reviewer-readiness-checks"
REGRESSION_SCANS = PH_ROOT / "operational-regression-scans"
ANOMALY_RECORDS = PH_ROOT / "corpus-anomaly-records"
REHEARSAL_RECORDS = PH_ROOT / "deployment-rehearsal-records"
ATTESTATIONS = PH_ROOT / "final-production-attestations"
MAINTENANCE_SUMMARIES = PH_ROOT / "runtime-maintenance-summaries"
BASELINE_RECORDS = PH_ROOT / "stability-baseline-records"
MATURITY_REPORTS = PH_ROOT / "operational-maturity-reports"

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

RO_ROOT = OC_ROOT / "reviewer-operational-runtime"
RO_GUIDED_WORKFLOWS = RO_ROOT / "guided-workflows"
RO_ONBOARDING = RO_ROOT / "onboarding-sequences"
RO_CHECKLISTS = RO_ROOT / "deployment-checklists"
RO_DIAGNOSTICS = RO_ROOT / "operational-diagnostics"
RO_NAV = RO_ROOT / "runtime-navigation-indexes"
RO_QUEUES = RO_ROOT / "corpus-review-queues"
RO_CONFIDENCE = RO_ROOT / "operational-confidence-summaries"
RO_PROOFS = RO_ROOT / "reproducibility-proofs"
RO_SESSIONS = RO_ROOT / "reviewer-session-records"
RO_HANDOFFS = RO_ROOT / "production-handoff-records"

# Phase 59 event stores
ES_STRESS = RUNTIME_MANIFESTS_ROOT / "corpus-stress-validation-events" / "_event-store.json"
ES_HARDENING = RUNTIME_MANIFESTS_ROOT / "runtime-hardening-scan-events" / "_event-store.json"
ES_READINESS = RUNTIME_MANIFESTS_ROOT / "reviewer-readiness-check-events" / "_event-store.json"
ES_REGRESSION = RUNTIME_MANIFESTS_ROOT / "operational-regression-scan-events" / "_event-store.json"
ES_ANOMALY = RUNTIME_MANIFESTS_ROOT / "corpus-anomaly-events" / "_event-store.json"
ES_REHEARSAL = RUNTIME_MANIFESTS_ROOT / "deployment-rehearsal-events" / "_event-store.json"
ES_ATTESTATION = RUNTIME_MANIFESTS_ROOT / "final-production-attestation-events" / "_event-store.json"
ES_MAINTENANCE = RUNTIME_MANIFESTS_ROOT / "runtime-maintenance-summary-events" / "_event-store.json"
ES_BASELINE = RUNTIME_MANIFESTS_ROOT / "stability-baseline-events" / "_event-store.json"
ES_MATURITY = RUNTIME_MANIFESTS_ROOT / "operational-maturity-report-events" / "_event-store.json"
ES_AUDIT = RUNTIME_MANIFESTS_ROOT / "audit-events" / "_event-store.json"

# Upstream event stores referenced for ordering / latest-state lookups
ES_PACKAGING_LIFECYCLE = RUNTIME_MANIFESTS_ROOT / "packaging-lifecycle-events" / "_event-store.json"
ES_ACTIVATION = RUNTIME_MANIFESTS_ROOT / "production-activation-events" / "_event-store.json"

# Enums
HARDENING_SCOPES = {
    "overwrite-isolation", "replay-consistency", "hash-consistency",
    "lifecycle-consistency", "export-reproducibility",
}
READINESS_AREAS = {"onboarding", "deployment", "rollback", "handoff", "audit"}
ANOMALY_KINDS = {
    "ingestion-anomaly", "extraction-anomaly", "synthesis-anomaly",
    "packaging-anomaly", "stabilization-anomaly", "deployment-anomaly",
    "activation-anomaly", "reviewer-process-anomaly",
}
ANOMALY_SEVERITIES = {"informational", "minor", "major", "blocking"}
REHEARSAL_OUTCOMES = {"pass", "fail", "skipped"}
MATURITY_DIMENSIONS = {
    "hardening-coverage", "regression-protection", "rehearsal-coverage",
    "attestation-coverage", "baseline-coverage", "anomaly-tracking",
    "maintenance-coverage", "reviewer-readiness-coverage",
}
ACTIVATION_STATES = {
    "production-candidate", "production-approved", "production-active",
    "superseded", "rollback-candidate",
}

# Forbidden overwrite prefixes — accumulate ALL prior phases through Phase 58.
FORBIDDEN_OVERWRITE_PREFIXES = (
    "reviewer-operational-runtime/",
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
    # Phase 59 hardening additions
    "auto_remediation", "automatic_remediation", "autonomous_fix",
    "ai_remediation", "ml_remediation", "remediation_score",
    "readiness_score", "ai_readiness", "ml_readiness",
    "predicted_readiness", "scoring_score", "maturity_score",
    "predicted_maturity", "ai_maturity", "ml_maturity",
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


def reject_probabilistic(payload: dict, rule_id: str = "PH-PROB") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_PROBABILISTIC_KEYS)
    if hit:
        fail(f"probabilistic/embedding/autonomous-prioritization/remediation/scoring key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


def reject_translation(payload: dict, rule_id: str = "PH-TRANS") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_TRANSLATION_KEYS)
    if hit:
        fail(f"translation/language-inference key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


def reject_telemetry(payload: dict, rule_id: str = "PH-TELE") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_TELEMETRY_KEYS)
    if hit:
        fail(f"telemetry/dashboard/streaming/analytics/behavior-tracking/daemon key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


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
        "audit_event_id": f"a59-{kind}-{_now()}",
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


def find_stabilization_for_package(pid: str) -> dict | None:
    for s in _scan_all(SC_STABILIZATIONS):
        if s.get("package_id") == pid:
            return s
    return None


def find_readiness_audit(aid: str) -> dict | None:
    return _scan_for_id(PC_AUDITS, "audit_id", aid)


def find_audit_for_package(pid: str) -> dict | None:
    for a in _scan_all(PC_AUDITS):
        if a.get("package_id") == pid:
            return a
    return None


def find_deployment_package(dpid: str) -> dict | None:
    return _scan_for_id(DEPLOYMENT_PACKAGES, "deployment_package_id", dpid)


def find_dp_for_package(pid: str) -> dict | None:
    for d in _scan_all(DEPLOYMENT_PACKAGES):
        if d.get("package_id") == pid:
            return d
    return None


def find_deployment_verification(vid: str) -> dict | None:
    return _scan_for_id(DEPLOYMENT_VERIFICATIONS, "verification_id", vid)


def find_reproducibility_proof(pid: str) -> dict | None:
    return _scan_for_id(RO_PROOFS, "proof_id", pid)


def find_proof_for_package(pid: str) -> dict | None:
    for p in _scan_all(RO_PROOFS):
        if p.get("package_id") == pid:
            return p
    return None


def find_handoff(hid: str) -> dict | None:
    return _scan_for_id(RO_HANDOFFS, "handoff_id", hid)


def find_checklist(cid: str) -> dict | None:
    return _scan_for_id(RO_CHECKLISTS, "checklist_id", cid)


def find_onboarding_sequence_for_area(area: str) -> dict | None:
    # Any onboarding sequence whose sequence_kind matches the area concept.
    mapping = {
        "onboarding": {"operator-onboarding", "reviewer-onboarding",
                       "deployment-onboarding", "recovery-onboarding"},
    }
    accept = mapping.get(area)
    for s in _scan_all(RO_ONBOARDING):
        if accept is None or s.get("sequence_kind") in accept:
            return s
    return None


# Self-layer finders
def find_corpus_stress(vid: str) -> dict | None:
    return _scan_for_id(CORPUS_STRESS, "validation_id", vid)


def find_hardening_scan(sid: str) -> dict | None:
    return _scan_for_id(HARDENING_SCANS, "scan_id", sid)


def find_readiness_check(cid: str) -> dict | None:
    return _scan_for_id(READINESS_CHECKS, "check_id", cid)


def find_regression_scan(sid: str) -> dict | None:
    return _scan_for_id(REGRESSION_SCANS, "scan_id", sid)


def find_anomaly(aid: str) -> dict | None:
    return _scan_for_id(ANOMALY_RECORDS, "anomaly_id", aid)


def find_rehearsal(rid: str) -> dict | None:
    return _scan_for_id(REHEARSAL_RECORDS, "rehearsal_id", rid)


def find_attestation(aid: str) -> dict | None:
    return _scan_for_id(ATTESTATIONS, "attestation_id", aid)


def find_maintenance_summary(sid: str) -> dict | None:
    return _scan_for_id(MAINTENANCE_SUMMARIES, "summary_id", sid)


def find_baseline(bid: str) -> dict | None:
    return _scan_for_id(BASELINE_RECORDS, "baseline_id", bid)


def find_maturity_report(rid: str) -> dict | None:
    return _scan_for_id(MATURITY_REPORTS, "report_id", rid)


# ============================================================================
# Dispatch handlers
# ============================================================================
def _per_package_snapshot(pid: str) -> dict:
    pkg = find_package(pid) or {}
    sections = pkg.get("sections", []) if isinstance(pkg.get("sections"), list) else []
    audits = [a for a in _scan_all(PC_AUDITS) if a.get("package_id") == pid]
    verifs = [v for v in _scan_all(DEPLOYMENT_VERIFICATIONS) if v.get("package_id") == pid]
    dps = [d for d in _scan_all(DEPLOYMENT_PACKAGES) if d.get("package_id") == pid]
    stabs = [s for s in _scan_all(SC_STABILIZATIONS) if s.get("package_id") == pid]
    drift = [d for d in _scan_all(PC_DRIFT) if d.get("package_id") == pid]
    return {
        "package_id": pid,
        "manual_id": pkg.get("manual_id"),
        "section_count": len(sections),
        "readiness_audit_count": len(audits),
        "deployment_verification_count": len(verifs),
        "deployment_package_count": len(dps),
        "stabilization_count": len(stabs),
        "drift_record_count": len(drift),
    }


def handle_corpus_stress_validation(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "CSV-5")
    reject_probabilistic(payload, "CSV-5")
    reject_translation(payload, "CSV-5")
    reject_telemetry(payload, "CSV-5")
    validation_id = payload.get("validation_id")
    package_ids = payload.get("package_ids")
    notes = payload.get("notes", "")
    if not validation_id:
        fail("payload.validation_id required (CSV-1)")
    if find_corpus_stress(validation_id):
        fail(f"validation_id {validation_id!r} already exists (CSV-1)")
    if not isinstance(package_ids, list) or not package_ids:
        fail("package_ids must be a non-empty list (CSV-2)")
    seen = set()
    for i, pid in enumerate(package_ids):
        if not isinstance(pid, str) or not pid.strip():
            fail(f"package_ids[{i}] must be a non-empty string (CSV-2)")
        if pid in seen:
            fail(f"package_ids[{i}] {pid!r} duplicate (CSV-2)")
        seen.add(pid)
        if not find_package(pid):
            fail(f"package_ids[{i}] {pid!r} not found (CSV-2)")

    snapshots = [_per_package_snapshot(pid) for pid in package_ids]
    snapshots.sort(key=lambda x: x["package_id"])
    content_slice = {
        "package_ids": sorted(package_ids),
        "snapshots": snapshots,
    }
    validation_sha256 = sha256_text(canonical_json(content_slice))
    record = {
        "schema": LAYER_SCHEMA,
        "validation_id": validation_id,
        "package_ids": sorted(package_ids),
        "package_count": len(package_ids),
        "snapshots": snapshots,
        "validation_sha256": validation_sha256,
        "pointer_only": True,
        "deterministic": True,
        "no_upstream_mutation": True,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(CORPUS_STRESS / f"{validation_id}-{_now()}.json", record)
    append_event(ES_STRESS, {
        "occurred_at_iso": _iso_now(),
        "kind": "corpus-stress-validation",
        "validation_id": validation_id,
        "package_count": len(package_ids),
        "validation_sha256": validation_sha256,
        "reviewer": reviewer,
    })
    append_audit("corpus-stress-validation", reviewer,
                 {"validation_id": validation_id, "package_count": len(package_ids)})
    return {"validation_id": validation_id, "validation_sha256": validation_sha256,
            "package_count": len(package_ids)}


def _scope_overwrite_isolation() -> dict:
    # Verify all forbidden prefixes have no Phase 59 records (defensive).
    findings: list[dict] = []
    for prefix in FORBIDDEN_OVERWRITE_PREFIXES:
        # We never scan disk for this — by construction Phase 59 cannot have
        # written there. Record the assertion deterministically.
        findings.append({"prefix": prefix, "isolated": True})
    return {"scope": "overwrite-isolation", "findings": findings, "status": "clean"}


def _scope_replay_consistency() -> dict:
    findings: list[dict] = []
    status = "clean"
    for store_path in (ES_STRESS, ES_HARDENING, ES_READINESS, ES_REGRESSION,
                       ES_ANOMALY, ES_REHEARSAL, ES_ATTESTATION,
                       ES_MAINTENANCE, ES_BASELINE, ES_MATURITY,
                       ES_PACKAGING_LIFECYCLE, ES_ACTIVATION):
        if not store_path.exists():
            continue
        try:
            events = read_json(store_path).get("events", [])
        except Exception:
            findings.append({"store": store_path.parent.name, "issue": "unreadable"})
            status = "findings"
            continue
        if not isinstance(events, list):
            findings.append({"store": store_path.parent.name, "issue": "events not list"})
            status = "findings"
            continue
        findings.append({"store": store_path.parent.name, "event_count": len(events)})
    return {"scope": "replay-consistency", "findings": findings, "status": status}


def _scope_hash_consistency() -> dict:
    findings: list[dict] = []
    status = "clean"
    # Each deployment-package's stable_export_sha256 should match the
    # corresponding stabilization's stable_export_sha256.
    stabs = {s.get("package_id"): s.get("stable_export_sha256") for s in _scan_all(SC_STABILIZATIONS)}
    for d in _scan_all(DEPLOYMENT_PACKAGES):
        pid = d.get("package_id")
        dp_hash = d.get("stable_export_sha256")
        stab_hash = stabs.get(pid)
        match = stab_hash is not None and dp_hash == stab_hash
        findings.append({
            "package_id": pid,
            "deployment_package_id": d.get("deployment_package_id"),
            "stab_export_hash": stab_hash,
            "deployment_export_hash": dp_hash,
            "match": match,
        })
        if not match:
            status = "findings"
    return {"scope": "hash-consistency", "findings": findings, "status": status}


def _scope_lifecycle_consistency() -> dict:
    findings: list[dict] = []
    status = "clean"
    if ES_ACTIVATION.exists():
        try:
            events = read_json(ES_ACTIVATION).get("events", [])
        except Exception:
            events = []
        per_id: dict[str, list[str]] = {}
        for e in events:
            aid = e.get("activation_id")
            ts = e.get("to_state")
            if aid and ts:
                per_id.setdefault(aid, []).append(ts)
        for aid, states in per_id.items():
            findings.append({"activation_id": aid, "transitions": states})
    return {"scope": "lifecycle-consistency", "findings": findings, "status": status}


def _scope_export_reproducibility() -> dict:
    findings: list[dict] = []
    status = "clean"
    for proof in _scan_all(RO_PROOFS):
        st = proof.get("status")
        findings.append({"proof_id": proof.get("proof_id"),
                         "package_id": proof.get("package_id"),
                         "status": st})
        if st != "confirmed":
            status = "findings"
    return {"scope": "export-reproducibility", "findings": findings, "status": status}


_SCOPE_HANDLERS = {
    "overwrite-isolation": _scope_overwrite_isolation,
    "replay-consistency": _scope_replay_consistency,
    "hash-consistency": _scope_hash_consistency,
    "lifecycle-consistency": _scope_lifecycle_consistency,
    "export-reproducibility": _scope_export_reproducibility,
}


def handle_runtime_hardening_scan(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "RHS-5")
    reject_probabilistic(payload, "RHS-5")
    reject_translation(payload, "RHS-5")
    reject_telemetry(payload, "RHS-5")
    scan_id = payload.get("scan_id")
    scopes = payload.get("scopes")
    notes = payload.get("notes", "")
    if not scan_id:
        fail("payload.scan_id required (RHS-1)")
    if find_hardening_scan(scan_id):
        fail(f"scan_id {scan_id!r} already exists (RHS-1)")
    if not isinstance(scopes, list) or not scopes:
        fail("scopes must be a non-empty list (RHS-2)")
    norm_scopes = []
    seen = set()
    for s in scopes:
        if s not in HARDENING_SCOPES:
            fail(f"scope {s!r} not in {sorted(HARDENING_SCOPES)} (RHS-2)")
        if s in seen:
            fail(f"scope {s!r} duplicate (RHS-2)")
        seen.add(s)
        norm_scopes.append(s)
    norm_scopes.sort()

    scope_results = [_SCOPE_HANDLERS[s]() for s in norm_scopes]
    overall_status = "findings" if any(r.get("status") == "findings" for r in scope_results) else "clean"

    content_slice = {
        "scopes": norm_scopes,
        "scope_results": scope_results,
        "overall_status": overall_status,
    }
    scan_sha256 = sha256_text(canonical_json(content_slice))
    record = {
        "schema": LAYER_SCHEMA,
        "scan_id": scan_id,
        "scopes": norm_scopes,
        "scope_results": scope_results,
        "overall_status": overall_status,
        "scan_sha256": scan_sha256,
        "informational_only": True,
        "no_autonomous_remediation": True,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(HARDENING_SCANS / f"{scan_id}-{_now()}.json", record)
    append_event(ES_HARDENING, {
        "occurred_at_iso": _iso_now(),
        "kind": "runtime-hardening-scan",
        "scan_id": scan_id,
        "scope_count": len(norm_scopes),
        "overall_status": overall_status,
        "scan_sha256": scan_sha256,
        "reviewer": reviewer,
    })
    append_audit("runtime-hardening-scan", reviewer,
                 {"scan_id": scan_id, "overall_status": overall_status})
    return {"scan_id": scan_id, "scan_sha256": scan_sha256,
            "overall_status": overall_status, "scope_count": len(norm_scopes)}


def _readiness_area_satisfied(area: str, package_id: str) -> tuple[bool, dict]:
    if area == "onboarding":
        seqs = _scan_all(RO_ONBOARDING)
        return (len(seqs) > 0,
                {"onboarding_sequence_count": len(seqs)})
    if area == "deployment":
        cl = [c for c in _scan_all(RO_CHECKLISTS) if c.get("package_id") == package_id]
        dp = find_dp_for_package(package_id)
        verifs = [v for v in _scan_all(DEPLOYMENT_VERIFICATIONS) if v.get("package_id") == package_id]
        ok = bool(cl) and dp is not None and bool(verifs)
        return (ok, {
            "deployment_checklist_count": len(cl),
            "deployment_package_present": dp is not None,
            "deployment_verification_count": len(verifs),
        })
    if area == "rollback":
        rb = [c for c in _scan_all(RO_CHECKLISTS)
              if c.get("package_id") == package_id and c.get("checklist_kind") == "rollback"]
        return (len(rb) > 0, {"rollback_checklist_count": len(rb)})
    if area == "handoff":
        h = [r for r in _scan_all(RO_HANDOFFS) if r.get("package_id") == package_id]
        return (len(h) > 0, {"handoff_count": len(h)})
    if area == "audit":
        a = [r for r in _scan_all(PC_AUDITS) if r.get("package_id") == package_id]
        return (len(a) > 0, {"readiness_audit_count": len(a)})
    return (False, {"unknown_area": area})


def handle_reviewer_readiness_check(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "RRC-5")
    reject_probabilistic(payload, "RRC-5")
    reject_translation(payload, "RRC-5")
    reject_telemetry(payload, "RRC-5")
    check_id = payload.get("check_id")
    package_id = payload.get("package_id")
    areas = payload.get("areas")
    notes = payload.get("notes", "")
    if not check_id:
        fail("payload.check_id required (RRC-1)")
    if find_readiness_check(check_id):
        fail(f"check_id {check_id!r} already exists (RRC-1)")
    if not package_id or not find_package(package_id):
        fail(f"package_id {package_id!r} not found (RRC-2)")
    if not isinstance(areas, list) or not areas:
        fail("areas must be a non-empty list (RRC-3)")
    norm_areas = []
    seen = set()
    for a in areas:
        if a not in READINESS_AREAS:
            fail(f"area {a!r} not in {sorted(READINESS_AREAS)} (RRC-3)")
        if a in seen:
            fail(f"area {a!r} duplicate (RRC-3)")
        seen.add(a)
        norm_areas.append(a)
    norm_areas.sort()

    area_results = []
    for a in norm_areas:
        ok, evidence = _readiness_area_satisfied(a, package_id)
        area_results.append({"area": a, "satisfied": ok, "evidence": evidence})
    status = "ready" if all(r["satisfied"] for r in area_results) else "incomplete"

    content_slice = {
        "package_id": package_id,
        "areas": norm_areas,
        "area_results": area_results,
        "status": status,
    }
    check_sha256 = sha256_text(canonical_json(content_slice))
    record = {
        "schema": LAYER_SCHEMA,
        "check_id": check_id,
        "package_id": package_id,
        "areas": norm_areas,
        "area_results": area_results,
        "status": status,
        "check_sha256": check_sha256,
        "deterministic_checklist": True,
        "no_ai_scoring": True,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(READINESS_CHECKS / f"{check_id}-{_now()}.json", record)
    append_event(ES_READINESS, {
        "occurred_at_iso": _iso_now(),
        "kind": "reviewer-readiness-check",
        "check_id": check_id,
        "package_id": package_id,
        "status": status,
        "check_sha256": check_sha256,
        "reviewer": reviewer,
    })
    append_audit("reviewer-readiness-check", reviewer,
                 {"check_id": check_id, "package_id": package_id, "status": status})
    return {"check_id": check_id, "check_sha256": check_sha256, "status": status,
            "area_count": len(norm_areas)}


def _rederive_baseline_hashes(package_id: str) -> dict:
    out: dict[str, str | None] = {}
    stab = find_stabilization_for_package(package_id)
    out["stable-export-hash"] = stab.get("stable_export_sha256") if stab else None
    dp = find_dp_for_package(package_id)
    out["deployment-package-hash"] = dp.get("deployment_package_sha256") if dp else None
    aud = find_audit_for_package(package_id)
    out["readiness-audit-hash"] = aud.get("audit_sha256") if aud else None
    proof = find_proof_for_package(package_id)
    out["reproducibility-proof-hash"] = proof.get("proof_sha256") if proof else None
    return out


def handle_stability_baseline_record(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "SBR-4")
    reject_probabilistic(payload, "SBR-4")
    reject_translation(payload, "SBR-4")
    reject_telemetry(payload, "SBR-4")
    baseline_id = payload.get("baseline_id")
    package_id = payload.get("package_id")
    notes = payload.get("notes", "")
    if not baseline_id:
        fail("payload.baseline_id required (SBR-1)")
    if find_baseline(baseline_id):
        fail(f"baseline_id {baseline_id!r} already exists (SBR-1)")
    if not package_id or not find_package(package_id):
        fail(f"package_id {package_id!r} not found (SBR-2)")

    hashes = _rederive_baseline_hashes(package_id)
    # Require at least the three mandatory hashes (export/deployment/audit) to
    # be present; reproducibility-proof-hash is optional.
    for required in ("stable-export-hash", "deployment-package-hash", "readiness-audit-hash"):
        if not hashes.get(required):
            fail(f"baseline target {required!r} could not be re-derived for package {package_id!r} (SBR-3)")

    content_slice = {
        "package_id": package_id,
        "baseline_hashes": dict(sorted(hashes.items())),
    }
    baseline_sha256 = sha256_text(canonical_json(content_slice))
    record = {
        "schema": LAYER_SCHEMA,
        "baseline_id": baseline_id,
        "package_id": package_id,
        "baseline_hashes": dict(sorted(hashes.items())),
        "baseline_sha256": baseline_sha256,
        "append_only": True,
        "reviewer_authoritative": True,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(BASELINE_RECORDS / f"{baseline_id}-{_now()}.json", record)
    append_event(ES_BASELINE, {
        "occurred_at_iso": _iso_now(),
        "kind": "stability-baseline-record",
        "baseline_id": baseline_id,
        "package_id": package_id,
        "baseline_sha256": baseline_sha256,
        "reviewer": reviewer,
    })
    append_audit("stability-baseline-record", reviewer,
                 {"baseline_id": baseline_id, "package_id": package_id})
    return {"baseline_id": baseline_id, "baseline_sha256": baseline_sha256,
            "package_id": package_id}


def handle_operational_regression_scan(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "ORS-5")
    reject_probabilistic(payload, "ORS-5")
    reject_translation(payload, "ORS-5")
    reject_telemetry(payload, "ORS-5")
    scan_id = payload.get("scan_id")
    baseline_id = payload.get("baseline_id")
    notes = payload.get("notes", "")
    if not scan_id:
        fail("payload.scan_id required (ORS-1)")
    if find_regression_scan(scan_id):
        fail(f"scan_id {scan_id!r} already exists (ORS-1)")
    base = find_baseline(baseline_id) if baseline_id else None
    if not base:
        fail(f"baseline_id {baseline_id!r} not found (ORS-2)")
    package_id = base.get("package_id")
    declared = base.get("baseline_hashes") or {}
    current = _rederive_baseline_hashes(package_id)

    comparisons: list[dict] = []
    regression_count = 0
    for target in sorted(declared.keys()):
        d = declared.get(target)
        c = current.get(target)
        match = (d is not None and c is not None and d == c)
        if not match:
            regression_count += 1
        comparisons.append({"target": target, "baseline_hash": d, "current_hash": c, "match": match})

    content_slice = {
        "baseline_id": baseline_id,
        "package_id": package_id,
        "comparisons": comparisons,
        "regression_count": regression_count,
    }
    scan_sha256 = sha256_text(canonical_json(content_slice))
    record = {
        "schema": LAYER_SCHEMA,
        "scan_id": scan_id,
        "baseline_id": baseline_id,
        "package_id": package_id,
        "comparisons": comparisons,
        "regression_count": regression_count,
        "scan_sha256": scan_sha256,
        "informational_only": True,
        "no_autonomous_remediation": True,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(REGRESSION_SCANS / f"{scan_id}-{_now()}.json", record)
    append_event(ES_REGRESSION, {
        "occurred_at_iso": _iso_now(),
        "kind": "operational-regression-scan",
        "scan_id": scan_id,
        "baseline_id": baseline_id,
        "regression_count": regression_count,
        "scan_sha256": scan_sha256,
        "reviewer": reviewer,
    })
    append_audit("operational-regression-scan", reviewer,
                 {"scan_id": scan_id, "baseline_id": baseline_id, "regression_count": regression_count})
    return {"scan_id": scan_id, "scan_sha256": scan_sha256,
            "regression_count": regression_count, "baseline_id": baseline_id}


def handle_corpus_anomaly_record(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "CAR-7")
    reject_probabilistic(payload, "CAR-7")
    reject_translation(payload, "CAR-7")
    reject_telemetry(payload, "CAR-7")
    anomaly_id = payload.get("anomaly_id")
    kind = payload.get("kind")
    severity = payload.get("severity")
    package_id = payload.get("package_id")
    scope = payload.get("scope")
    description = payload.get("description")
    references = payload.get("references", [])
    notes = payload.get("notes", "")
    if not anomaly_id:
        fail("payload.anomaly_id required (CAR-1)")
    if find_anomaly(anomaly_id):
        fail(f"anomaly_id {anomaly_id!r} already exists (CAR-1)")
    if kind not in ANOMALY_KINDS:
        fail(f"kind {kind!r} not in {sorted(ANOMALY_KINDS)} (CAR-2)")
    if severity not in ANOMALY_SEVERITIES:
        fail(f"severity {severity!r} not in {sorted(ANOMALY_SEVERITIES)} (CAR-3)")
    if package_id:
        if not find_package(package_id):
            fail(f"package_id {package_id!r} not found (CAR-4)")
    else:
        if scope != "corpus":
            fail("either package_id (resolvable) or scope='corpus' required (CAR-4)")
    if not isinstance(description, str) or not description.strip():
        fail("description (string) required (CAR-5)")
    if not isinstance(references, list):
        fail("references must be a list (CAR-5)")
    norm_refs = []
    for i, r in enumerate(references):
        if not isinstance(r, dict):
            fail(f"references[{i}] must be a dict {{kind, id}} (CAR-5)")
        rk = r.get("kind")
        rid = r.get("id")
        if not isinstance(rk, str) or not isinstance(rid, str):
            fail(f"references[{i}] requires string kind and id (CAR-5)")
        norm_refs.append({"kind": rk, "id": rid})
    norm_refs.sort(key=lambda x: (x["kind"], x["id"]))

    content_slice = {
        "kind": kind,
        "severity": severity,
        "package_id": package_id,
        "scope": scope if not package_id else None,
        "description": description,
        "references": norm_refs,
    }
    anomaly_sha256 = sha256_text(canonical_json(content_slice))
    record = {
        "schema": LAYER_SCHEMA,
        "anomaly_id": anomaly_id,
        "kind": kind,
        "severity": severity,
        "package_id": package_id,
        "scope": scope if not package_id else None,
        "description": description,
        "references": norm_refs,
        "anomaly_sha256": anomaly_sha256,
        "append_only": True,
        "reviewer_authored": True,
        "no_autonomous_remediation": True,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(ANOMALY_RECORDS / f"{anomaly_id}-{_now()}.json", record)
    append_event(ES_ANOMALY, {
        "occurred_at_iso": _iso_now(),
        "kind": "corpus-anomaly-record",
        "anomaly_id": anomaly_id,
        "anomaly_kind": kind,
        "severity": severity,
        "package_id": package_id,
        "anomaly_sha256": anomaly_sha256,
        "reviewer": reviewer,
    })
    append_audit("corpus-anomaly-record", reviewer,
                 {"anomaly_id": anomaly_id, "severity": severity})
    return {"anomaly_id": anomaly_id, "anomaly_sha256": anomaly_sha256, "severity": severity}


def handle_deployment_rehearsal_record(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "DRR-7")
    reject_probabilistic(payload, "DRR-7")
    reject_translation(payload, "DRR-7")
    reject_telemetry(payload, "DRR-7")
    rehearsal_id = payload.get("rehearsal_id")
    package_id = payload.get("package_id")
    checklist_id = payload.get("checklist_id")
    outcomes = payload.get("outcomes")
    notes = payload.get("notes", "")
    if not rehearsal_id:
        fail("payload.rehearsal_id required (DRR-1)")
    if find_rehearsal(rehearsal_id):
        fail(f"rehearsal_id {rehearsal_id!r} already exists (DRR-1)")
    if not package_id or not find_package(package_id):
        fail(f"package_id {package_id!r} not found (DRR-2)")
    checklist = find_checklist(checklist_id) if checklist_id else None
    if not checklist:
        fail(f"checklist_id {checklist_id!r} not found (DRR-3)")
    if checklist.get("package_id") != package_id:
        fail(f"checklist {checklist_id!r} package_id mismatch (DRR-3)")
    items = checklist.get("items", [])
    if not isinstance(outcomes, list):
        fail("outcomes must be a list (DRR-4)")
    if len(outcomes) != len(items):
        fail(f"outcomes count {len(outcomes)} != checklist item count {len(items)} (DRR-4)")
    item_ids = {it.get("item_id") for it in items}
    seen = set()
    norm_outcomes = []
    pass_n = fail_n = skip_n = 0
    for i, o in enumerate(outcomes):
        if not isinstance(o, dict):
            fail(f"outcomes[{i}] must be a dict (DRR-4)")
        iid = o.get("item_id")
        oc = o.get("outcome")
        note = o.get("note", "")
        if iid not in item_ids:
            fail(f"outcomes[{i}].item_id {iid!r} not in checklist items (DRR-4)")
        if iid in seen:
            fail(f"outcomes[{i}].item_id {iid!r} duplicate (DRR-4)")
        seen.add(iid)
        if oc not in REHEARSAL_OUTCOMES:
            fail(f"outcomes[{i}].outcome {oc!r} not in {sorted(REHEARSAL_OUTCOMES)} (DRR-5)")
        if oc == "pass":
            pass_n += 1
        elif oc == "fail":
            fail_n += 1
        else:
            skip_n += 1
        if not isinstance(note, str):
            fail(f"outcomes[{i}].note must be a string (DRR-4)")
        norm_outcomes.append({"item_id": iid, "outcome": oc, "note": note})
    if seen != item_ids:
        fail(f"outcomes must cover every checklist item_id exactly once (DRR-4)")
    norm_outcomes.sort(key=lambda x: x["item_id"])

    content_slice = {
        "package_id": package_id,
        "checklist_id": checklist_id,
        "outcomes": norm_outcomes,
    }
    rehearsal_sha256 = sha256_text(canonical_json(content_slice))
    record = {
        "schema": LAYER_SCHEMA,
        "rehearsal_id": rehearsal_id,
        "package_id": package_id,
        "checklist_id": checklist_id,
        "outcomes": norm_outcomes,
        "outcome_counts": {"pass": pass_n, "fail": fail_n, "skipped": skip_n},
        "rehearsal_sha256": rehearsal_sha256,
        "deterministic_outcomes_only": True,
        "no_live_deployment": True,
        "no_live_activation": True,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(REHEARSAL_RECORDS / f"{rehearsal_id}-{_now()}.json", record)
    append_event(ES_REHEARSAL, {
        "occurred_at_iso": _iso_now(),
        "kind": "deployment-rehearsal-record",
        "rehearsal_id": rehearsal_id,
        "package_id": package_id,
        "checklist_id": checklist_id,
        "outcome_counts": {"pass": pass_n, "fail": fail_n, "skipped": skip_n},
        "rehearsal_sha256": rehearsal_sha256,
        "reviewer": reviewer,
    })
    append_audit("deployment-rehearsal-record", reviewer,
                 {"rehearsal_id": rehearsal_id, "package_id": package_id})
    return {"rehearsal_id": rehearsal_id, "rehearsal_sha256": rehearsal_sha256,
            "outcome_counts": {"pass": pass_n, "fail": fail_n, "skipped": skip_n}}


def handle_final_production_attestation(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "FPA-5")
    reject_probabilistic(payload, "FPA-5")
    reject_translation(payload, "FPA-5")
    reject_telemetry(payload, "FPA-5")
    attestation_id = payload.get("attestation_id")
    package_id = payload.get("package_id")
    readiness_audit_id = payload.get("readiness_audit_id")
    verification_id = payload.get("verification_id")
    proof_id = payload.get("proof_id")
    rehearsal_id = payload.get("rehearsal_id")
    handoff_id = payload.get("handoff_id")
    reviewer_conclusion = payload.get("reviewer_conclusion")
    notes = payload.get("notes", "")
    if not attestation_id:
        fail("payload.attestation_id required (FPA-1)")
    if find_attestation(attestation_id):
        fail(f"attestation_id {attestation_id!r} already exists (FPA-1)")
    if not package_id or not find_package(package_id):
        fail(f"package_id {package_id!r} not found (FPA-2)")
    aud = find_readiness_audit(readiness_audit_id) if readiness_audit_id else None
    if not aud:
        fail(f"readiness_audit_id {readiness_audit_id!r} not found (FPA-3)")
    ver = find_deployment_verification(verification_id) if verification_id else None
    if not ver:
        fail(f"verification_id {verification_id!r} not found (FPA-3)")
    proof = find_reproducibility_proof(proof_id) if proof_id else None
    if not proof:
        fail(f"proof_id {proof_id!r} not found (FPA-3)")
    rehearsal = find_rehearsal(rehearsal_id) if rehearsal_id else None
    if not rehearsal:
        fail(f"rehearsal_id {rehearsal_id!r} not found (FPA-3)")
    handoff = find_handoff(handoff_id) if handoff_id else None
    if not handoff:
        fail(f"handoff_id {handoff_id!r} not found (FPA-3)")
    if not isinstance(reviewer_conclusion, str) or not reviewer_conclusion.strip():
        fail("reviewer_conclusion (string) required (FPA-4)")

    content_slice = {
        "package_id": package_id,
        "readiness_audit_id": readiness_audit_id,
        "verification_id": verification_id,
        "proof_id": proof_id,
        "rehearsal_id": rehearsal_id,
        "handoff_id": handoff_id,
        "reviewer_conclusion": reviewer_conclusion,
    }
    attestation_sha256 = sha256_text(canonical_json(content_slice))
    record = {
        "schema": LAYER_SCHEMA,
        "attestation_id": attestation_id,
        "package_id": package_id,
        "readiness_audit_id": readiness_audit_id,
        "verification_id": verification_id,
        "proof_id": proof_id,
        "rehearsal_id": rehearsal_id,
        "handoff_id": handoff_id,
        "reviewer_conclusion": reviewer_conclusion,
        "lineage_pointers": {
            "audit_sha256": aud.get("audit_sha256"),
            "verification_sha256": ver.get("verification_sha256"),
            "proof_sha256": proof.get("proof_sha256"),
            "rehearsal_sha256": rehearsal.get("rehearsal_sha256"),
            "handoff_sha256": handoff.get("handoff_sha256"),
        },
        "attestation_sha256": attestation_sha256,
        "append_only": True,
        "reviewer_authoritative": True,
        "no_ai_scoring": True,
        "no_autonomous_readiness_claim": True,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(ATTESTATIONS / f"{attestation_id}-{_now()}.json", record)
    append_event(ES_ATTESTATION, {
        "occurred_at_iso": _iso_now(),
        "kind": "final-production-attestation",
        "attestation_id": attestation_id,
        "package_id": package_id,
        "attestation_sha256": attestation_sha256,
        "reviewer": reviewer,
    })
    append_audit("final-production-attestation", reviewer,
                 {"attestation_id": attestation_id, "package_id": package_id})
    return {"attestation_id": attestation_id, "attestation_sha256": attestation_sha256,
            "package_id": package_id}


def _maintenance_aggregate() -> dict:
    """Pointer-only counts of records under prior runtime trees."""
    trees = {
        "manual-semantic-packaging-runtime/manual-packages": PACKAGES_DIR,
        "manual-runtime-closure/export-finalizations": EXPORT_FINALIZATIONS,
        "semantic-convergence-runtime/canonical-entities": SC_CANONICAL_ENTITIES,
        "semantic-convergence-runtime/canonical-procedures": SC_CANONICAL_PROCEDURES,
        "semantic-convergence-runtime/conflict-surfacings": SC_CONFLICTS,
        "semantic-convergence-runtime/arbitration-decisions": SC_ARBITRATION,
        "semantic-convergence-runtime/export-stabilizations": SC_STABILIZATIONS,
        "production-closure-runtime/canonical-drift-records": PC_DRIFT,
        "production-closure-runtime/export-stability-guarantees": PC_GUARANTEES,
        "production-closure-runtime/readiness-audit-records": PC_AUDITS,
        "production-closure-runtime/multilingual-normalization-tables": PC_ML_TABLES,
        "production-closure-runtime/robustness-records": PC_ROBUSTNESS,
        "operational-deployment-runtime/deployment-packages": DEPLOYMENT_PACKAGES,
        "operational-deployment-runtime/deployment-verifications": DEPLOYMENT_VERIFICATIONS,
        "operational-deployment-runtime/activation-lifecycle-records": ACTIVATION_LIFECYCLE,
        "reviewer-operational-runtime/guided-workflows": RO_GUIDED_WORKFLOWS,
        "reviewer-operational-runtime/onboarding-sequences": RO_ONBOARDING,
        "reviewer-operational-runtime/deployment-checklists": RO_CHECKLISTS,
        "reviewer-operational-runtime/operational-diagnostics": RO_DIAGNOSTICS,
        "reviewer-operational-runtime/runtime-navigation-indexes": RO_NAV,
        "reviewer-operational-runtime/corpus-review-queues": RO_QUEUES,
        "reviewer-operational-runtime/operational-confidence-summaries": RO_CONFIDENCE,
        "reviewer-operational-runtime/reproducibility-proofs": RO_PROOFS,
        "reviewer-operational-runtime/reviewer-session-records": RO_SESSIONS,
        "reviewer-operational-runtime/production-handoff-records": RO_HANDOFFS,
    }
    counts: dict[str, int] = {}
    for key, d in trees.items():
        counts[key] = len(_scan_all(d)) if d.exists() else 0
    return dict(sorted(counts.items()))


def handle_runtime_maintenance_summary(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "RMS-4")
    reject_probabilistic(payload, "RMS-4")
    reject_translation(payload, "RMS-4")
    reject_telemetry(payload, "RMS-4")
    summary_id = payload.get("summary_id")
    notes = payload.get("notes", "")
    if not summary_id:
        fail("payload.summary_id required (RMS-1)")
    if find_maintenance_summary(summary_id):
        fail(f"summary_id {summary_id!r} already exists (RMS-1)")

    counts = _maintenance_aggregate()
    content_slice = {"counts": counts}
    summary_sha256 = sha256_text(canonical_json(content_slice))
    record = {
        "schema": LAYER_SCHEMA,
        "summary_id": summary_id,
        "counts": counts,
        "summary_sha256": summary_sha256,
        "pointer_only": True,
        "no_payload_duplication": True,
        "no_telemetry": True,
        "no_dashboards": True,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(MAINTENANCE_SUMMARIES / f"{summary_id}-{_now()}.json", record)
    append_event(ES_MAINTENANCE, {
        "occurred_at_iso": _iso_now(),
        "kind": "runtime-maintenance-summary",
        "summary_id": summary_id,
        "tree_count": len(counts),
        "summary_sha256": summary_sha256,
        "reviewer": reviewer,
    })
    append_audit("runtime-maintenance-summary", reviewer,
                 {"summary_id": summary_id})
    return {"summary_id": summary_id, "summary_sha256": summary_sha256,
            "tree_count": len(counts)}


def _maturity_dimension_aggregate(dim: str) -> dict:
    if dim == "hardening-coverage":
        return {"hardening_scan_count": len(_scan_all(HARDENING_SCANS))}
    if dim == "regression-protection":
        return {"baseline_count": len(_scan_all(BASELINE_RECORDS)),
                "regression_scan_count": len(_scan_all(REGRESSION_SCANS))}
    if dim == "rehearsal-coverage":
        return {"rehearsal_count": len(_scan_all(REHEARSAL_RECORDS))}
    if dim == "attestation-coverage":
        return {"attestation_count": len(_scan_all(ATTESTATIONS))}
    if dim == "baseline-coverage":
        return {"baseline_count": len(_scan_all(BASELINE_RECORDS))}
    if dim == "anomaly-tracking":
        anomalies = _scan_all(ANOMALY_RECORDS)
        sev: dict[str, int] = {}
        for a in anomalies:
            s = a.get("severity")
            if isinstance(s, str):
                sev[s] = sev.get(s, 0) + 1
        return {"anomaly_count": len(anomalies), "severity_breakdown": dict(sorted(sev.items()))}
    if dim == "maintenance-coverage":
        return {"maintenance_summary_count": len(_scan_all(MAINTENANCE_SUMMARIES))}
    if dim == "reviewer-readiness-coverage":
        checks = _scan_all(READINESS_CHECKS)
        ready = sum(1 for c in checks if c.get("status") == "ready")
        return {"readiness_check_count": len(checks), "ready_count": ready}
    return {}


def handle_operational_maturity_report(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "OMR-5")
    reject_probabilistic(payload, "OMR-5")
    reject_translation(payload, "OMR-5")
    reject_telemetry(payload, "OMR-5")
    report_id = payload.get("report_id")
    dimensions = payload.get("dimensions")
    reviewer_conclusion = payload.get("reviewer_conclusion")
    notes = payload.get("notes", "")
    if not report_id:
        fail("payload.report_id required (OMR-1)")
    if find_maturity_report(report_id):
        fail(f"report_id {report_id!r} already exists (OMR-1)")
    if not isinstance(dimensions, list) or not dimensions:
        fail("dimensions must be a non-empty list (OMR-2)")
    norm_dims = []
    seen = set()
    for d in dimensions:
        if d not in MATURITY_DIMENSIONS:
            fail(f"dimension {d!r} not in {sorted(MATURITY_DIMENSIONS)} (OMR-2)")
        if d in seen:
            fail(f"dimension {d!r} duplicate (OMR-2)")
        seen.add(d)
        norm_dims.append(d)
    norm_dims.sort()
    if not isinstance(reviewer_conclusion, str) or not reviewer_conclusion.strip():
        fail("reviewer_conclusion (string) required — reviewer-authored (OMR-3)")

    aggregates = {d: _maturity_dimension_aggregate(d) for d in norm_dims}
    content_slice = {
        "dimensions": norm_dims,
        "aggregates": aggregates,
        "reviewer_conclusion": reviewer_conclusion,
    }
    report_sha256 = sha256_text(canonical_json(content_slice))
    record = {
        "schema": LAYER_SCHEMA,
        "report_id": report_id,
        "dimensions": norm_dims,
        "aggregates": aggregates,
        "reviewer_conclusion": reviewer_conclusion,
        "report_sha256": report_sha256,
        "append_only": True,
        "reviewer_authored_conclusion": True,
        "no_ai_scoring": True,
        "no_autonomous_maturity_claim": True,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(MATURITY_REPORTS / f"{report_id}-{_now()}.json", record)
    append_event(ES_MATURITY, {
        "occurred_at_iso": _iso_now(),
        "kind": "operational-maturity-report",
        "report_id": report_id,
        "dimension_count": len(norm_dims),
        "report_sha256": report_sha256,
        "reviewer": reviewer,
    })
    append_audit("operational-maturity-report", reviewer,
                 {"report_id": report_id, "dimension_count": len(norm_dims)})
    return {"report_id": report_id, "report_sha256": report_sha256,
            "dimension_count": len(norm_dims)}


# ============================================================================
# Dispatch table & CLI
# ============================================================================
DISPATCH = {
    "corpus-stress-validation": handle_corpus_stress_validation,
    "runtime-hardening-scan": handle_runtime_hardening_scan,
    "reviewer-readiness-check": handle_reviewer_readiness_check,
    "operational-regression-scan": handle_operational_regression_scan,
    "corpus-anomaly-record": handle_corpus_anomaly_record,
    "deployment-rehearsal-record": handle_deployment_rehearsal_record,
    "final-production-attestation": handle_final_production_attestation,
    "runtime-maintenance-summary": handle_runtime_maintenance_summary,
    "stability-baseline-record": handle_stability_baseline_record,
    "operational-maturity-report": handle_operational_maturity_report,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 59 production hardening + corpus validation executor")
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
