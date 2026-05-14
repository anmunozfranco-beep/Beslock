#!/usr/bin/env python3
"""
Phase 56 executor — final operational closure, real-world robustness &
production-ready manual delivery (constitutional layer 49).

Request envelope: governed-fs-operation-request/1.0
CLI: --kind <dispatch> --request <envelope.json> --confirm

Deterministic, reviewer-authoritative, append-only. Hardens the existing
constitutional substrate WITHOUT introducing new architectural families:
NO machine translation, NO LLM translation, NO autonomous arbitration,
NO silent canonical mutation, NO embeddings, NO probabilistic inference.
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
LAYER_SCHEMA = "final-operational-closure-production-readiness/1.0"
LAYER = 49

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"

# Phase 56 isolated storage tree
PC_ROOT = OC_ROOT / "production-closure-runtime"
EVIDENCE_ROBUSTNESS = PC_ROOT / "evidence-robustness-records"
ML_TABLES = PC_ROOT / "multilingual-normalization-tables"
ML_APPLICATIONS = PC_ROOT / "multilingual-normalization-records"
EXPORT_GUARANTEES = PC_ROOT / "export-stability-guarantees"
DRIFT_RECORDS = PC_ROOT / "canonical-drift-records"
REVIEWER_SUMMARIES = PC_ROOT / "reviewer-summaries"
INCREMENTAL_REFRESH = PC_ROOT / "incremental-refresh-records"
READINESS_AUDITS = PC_ROOT / "readiness-audit-records"
CLOSURE_PATHS = PC_ROOT / "closure-path-records"

# Upstream READ-ONLY trees
SC_ROOT = OC_ROOT / "semantic-convergence-runtime"
SC_CANONICAL_ENTITIES = SC_ROOT / "canonical-entities"
SC_CANONICAL_PROCEDURES = SC_ROOT / "canonical-procedures"
SC_FUSION_CLUSTERS = SC_ROOT / "fusion-clusters"
SC_CONFLICTS = SC_ROOT / "conflict-surfacings"
SC_ARBITRATION = SC_ROOT / "arbitration-decisions"
SC_STABILIZATIONS = SC_ROOT / "export-stabilizations"

PACKAGING_RUNTIME = OC_ROOT / "manual-semantic-packaging-runtime"
PACKAGES_DIR = PACKAGING_RUNTIME / "manual-packages"

MR_ROOT = OC_ROOT / "manual-runtime-closure"
INTAKE_APPROVALS = MR_ROOT / "intake-approvals"
INTAKE_ANALYSES = MR_ROOT / "intake-analyses"
VISUAL_SUPPORT = MR_ROOT / "visual-support-records"
PROMPT_PACKAGES = MR_ROOT / "prompt-packages"
EXPORT_FINALIZATIONS = MR_ROOT / "export-finalizations"

# Event stores
ES_ROBUSTNESS = RUNTIME_MANIFESTS_ROOT / "evidence-robustness-events" / "_event-store.json"
ES_ML_TABLE = RUNTIME_MANIFESTS_ROOT / "multilingual-normalization-table-events" / "_event-store.json"
ES_ML_APPLY = RUNTIME_MANIFESTS_ROOT / "multilingual-normalization-apply-events" / "_event-store.json"
ES_GUARANTEE = RUNTIME_MANIFESTS_ROOT / "export-stability-guarantee-events" / "_event-store.json"
ES_DRIFT = RUNTIME_MANIFESTS_ROOT / "canonical-drift-events" / "_event-store.json"
ES_SUMMARY = RUNTIME_MANIFESTS_ROOT / "reviewer-summary-events" / "_event-store.json"
ES_REFRESH = RUNTIME_MANIFESTS_ROOT / "incremental-refresh-events" / "_event-store.json"
ES_AUDIT_RA = RUNTIME_MANIFESTS_ROOT / "readiness-audit-events" / "_event-store.json"
ES_CLOSURE = RUNTIME_MANIFESTS_ROOT / "closure-path-events" / "_event-store.json"
ES_AUDIT = RUNTIME_MANIFESTS_ROOT / "audit-events" / "_event-store.json"

ROBUSTNESS_KINDS = {
    "incomplete-evidence", "duplicated-document", "noisy-ocr-fragment",
    "multilingual-screenshot", "truncated-video", "contradictory-support-export",
    "inconsistent-specification-table", "low-quality-evidence",
    "fragmented-app-flow", "partial-troubleshooting-chain",
}
SEVERITY = {"informational", "minor", "major", "blocking"}
DRIFT_KINDS = {
    "procedure-modification", "warning-alteration", "specification-change",
    "troubleshooting-invalidation", "entity-supersession",
}
SUMMARY_KINDS = {
    "evidence-timeline", "canonical-entity-inspection", "convergence-summary",
    "drift-summary", "unresolved-conflict-summary", "export-readiness-summary",
}
REFRESH_TRIGGER_KINDS = {
    "approved-intake", "canonical-promotion", "arbitration-resolution",
    "drift-detection", "stability-guarantee-reaffirmed",
}
CLOSURE_STAGES = [
    "evidence", "analysis", "convergence", "canonical-entity",
    "canonical-procedure", "visual-support", "prompt-package",
    "stabilized-export", "readiness-audit", "consumer-payload",
]

FORBIDDEN_OVERWRITE_PREFIXES = (
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
    "autonomous_decision", "autonomous_arbitration",
}

FORBIDDEN_TRANSLATION_KEYS = {
    "machine_translation", "llm_translation", "mt_model",
    "language_model_inference", "autodetect_language", "language_inference",
    "neural_translation", "translation_score", "translation_confidence",
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


def reject_probabilistic(payload: dict, rule_id: str = "PC-PROB") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_PROBABILISTIC_KEYS)
    if hit:
        fail(f"probabilistic/embedding key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


def reject_translation(payload: dict, rule_id: str = "MA-6") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_TRANSLATION_KEYS)
    if hit:
        fail(f"translation/language-inference key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


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
        "audit_event_id": f"a56-{kind}-{_now()}",
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


def find_canonical_entity(eid: str) -> dict | None:
    return _scan_for_id(SC_CANONICAL_ENTITIES, "canonical_entity_id", eid)


def find_canonical_procedure(pid: str) -> dict | None:
    return _scan_for_id(SC_CANONICAL_PROCEDURES, "canonical_procedure_id", pid)


def find_stabilization(sid: str) -> dict | None:
    return _scan_for_id(SC_STABILIZATIONS, "stabilization_id", sid)


def find_package(pid: str) -> dict | None:
    return _scan_for_id(PACKAGES_DIR, "package_id", pid)


def find_intake_approval(aid: str) -> dict | None:
    return _scan_for_id(INTAKE_APPROVALS, "approval_id", aid)


def find_intake_analysis(aid: str) -> dict | None:
    return _scan_for_id(INTAKE_ANALYSES, "analysis_id", aid)


def find_arbitration_decision(did: str) -> dict | None:
    return _scan_for_id(SC_ARBITRATION, "decision_id", did)


def find_conflict(cid: str) -> dict | None:
    return _scan_for_id(SC_CONFLICTS, "conflict_id", cid)


def find_visual_support(vid: str) -> dict | None:
    return _scan_for_id(VISUAL_SUPPORT, "visual_support_id", vid)


def find_prompt_package(pid: str) -> dict | None:
    return _scan_for_id(PROMPT_PACKAGES, "prompt_package_id", pid)


def find_export_finalization(fid: str) -> dict | None:
    return _scan_for_id(EXPORT_FINALIZATIONS, "finalization_id", fid)


def find_normalization_table(tid: str) -> dict | None:
    return _scan_for_id(ML_TABLES, "table_id", tid)


def find_fusion_cluster(cid: str) -> dict | None:
    return _scan_for_id(SC_FUSION_CLUSTERS, "cluster_id", cid)


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


# ============================================================================
# Dispatch handlers
# ============================================================================
def handle_evidence_robustness_record(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "ER-6")
    reject_probabilistic(payload)
    reject_translation(payload)
    record_id = payload.get("record_id")
    source_evidence_id = payload.get("source_evidence_id")
    robustness_kind = payload.get("robustness_kind")
    severity = payload.get("severity")
    lineage_pointers = payload.get("lineage_pointers", {})
    reviewer_notes = payload.get("reviewer_notes", "")
    if not record_id:
        fail("payload.record_id required (ER-1)")
    if not source_evidence_id:
        fail("payload.source_evidence_id required (ER-1)")
    if robustness_kind not in ROBUSTNESS_KINDS:
        fail(f"robustness_kind {robustness_kind!r} not in {sorted(ROBUSTNESS_KINDS)} (ER-2)")
    if severity not in SEVERITY:
        fail(f"severity {severity!r} not in {sorted(SEVERITY)} (ER-3)")
    if not isinstance(lineage_pointers, dict):
        fail("lineage_pointers must be a dict (ER-4)")

    record = {
        "schema": LAYER_SCHEMA,
        "record_id": record_id,
        "source_evidence_id": source_evidence_id,
        "robustness_kind": robustness_kind,
        "severity": severity,
        "lineage_pointers": dict(sorted(lineage_pointers.items())),
        "reviewer_notes": reviewer_notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(EVIDENCE_ROBUSTNESS / f"{record_id}-{_now()}.json", record)
    append_event(ES_ROBUSTNESS, {
        "occurred_at_iso": _iso_now(),
        "kind": "evidence-robustness-record",
        "record_id": record_id,
        "robustness_kind": robustness_kind,
        "severity": severity,
        "reviewer": reviewer,
    })
    append_audit("evidence-robustness-record", reviewer, {"record_id": record_id, "severity": severity})
    return {"record_id": record_id, "severity": severity}


def handle_multilingual_normalization_table_create(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "MN-7")
    reject_probabilistic(payload)
    reject_translation(payload)
    table_id = payload.get("table_id")
    source_lang = payload.get("source_language")
    canonical_lang = payload.get("canonical_language")
    mappings = payload.get("mappings")
    prior_table_id = payload.get("prior_table_id")
    if not table_id:
        fail("payload.table_id required (MN-1)")
    if find_normalization_table(table_id):
        fail(f"table_id {table_id!r} already exists; create a superseding table (MN-5)")
    if not isinstance(source_lang, str) or not source_lang.strip() or len(source_lang) > 8:
        fail("source_language required (ISO-639-1 string) (MN-2)")
    if not isinstance(canonical_lang, str) or not canonical_lang.strip() or len(canonical_lang) > 8:
        fail("canonical_language required (ISO-639-1 string) (MN-2)")
    if not isinstance(mappings, list) or not mappings:
        fail("mappings must be a non-empty list (MN-3)")
    seen = set()
    norm_mappings = []
    for i, m in enumerate(mappings):
        if not isinstance(m, dict):
            fail(f"mappings[{i}] must be a dict (MN-3)")
        st = m.get("source_term")
        ct = m.get("canonical_term")
        if not isinstance(st, str) or not st.strip():
            fail(f"mappings[{i}].source_term required (MN-4)")
        if not isinstance(ct, str) or not ct.strip():
            fail(f"mappings[{i}].canonical_term required (MN-4)")
        key = (source_lang.lower(), st.lower())
        if key in seen:
            fail(f"mappings[{i}] duplicates source_term {st!r} (MN-3)")
        seen.add(key)
        norm_mappings.append({"source_term": st, "canonical_term": ct})
    norm_mappings.sort(key=lambda m: m["source_term"])
    if prior_table_id and not find_normalization_table(prior_table_id):
        fail(f"prior_table_id {prior_table_id!r} not found (MN-5)")

    table_payload = {
        "table_id": table_id,
        "source_language": source_lang.lower(),
        "canonical_language": canonical_lang.lower(),
        "mappings": norm_mappings,
        "prior_table_id": prior_table_id,
    }
    table_sha256 = sha256_text(canonical_json(table_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **table_payload,
        "table_sha256": table_sha256,
        "mapping_count": len(norm_mappings),
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
        "deterministic": True,
        "no_machine_translation": True,
    }
    write_json(ML_TABLES / f"{table_id}-{_now()}.json", record)
    append_event(ES_ML_TABLE, {
        "occurred_at_iso": _iso_now(),
        "kind": "multilingual-normalization-table-create",
        "table_id": table_id,
        "source_language": source_lang.lower(),
        "canonical_language": canonical_lang.lower(),
        "mapping_count": len(norm_mappings),
        "table_sha256": table_sha256,
        "reviewer": reviewer,
    })
    append_audit("multilingual-normalization-table-create", reviewer,
                 {"table_id": table_id, "mapping_count": len(norm_mappings)})
    return {"table_id": table_id, "table_sha256": table_sha256, "mapping_count": len(norm_mappings)}


def handle_multilingual_normalization_apply(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "MA-7")
    reject_probabilistic(payload)
    reject_translation(payload)
    application_id = payload.get("application_id")
    table_id = payload.get("table_id")
    source_evidence_id = payload.get("source_evidence_id")
    raw_text = payload.get("raw_text", "")
    applied_terms = payload.get("applied_terms")
    if not application_id:
        fail("payload.application_id required (MA-1)")
    table = find_normalization_table(table_id) if table_id else None
    if not table:
        fail(f"table_id {table_id!r} not found (MA-2)")
    if not source_evidence_id:
        fail("payload.source_evidence_id required (MA-3)")
    if not isinstance(applied_terms, list) or not applied_terms:
        fail("applied_terms must be a non-empty list (MA-4)")

    table_mapping = {m["source_term"]: m["canonical_term"] for m in table.get("mappings", [])}
    table_index = {m["source_term"]: i for i, m in enumerate(table.get("mappings", []))}
    norm_applied = []
    for i, t in enumerate(applied_terms):
        if not isinstance(t, dict):
            fail(f"applied_terms[{i}] must be a dict (MA-4)")
        st = t.get("source_term")
        ct = t.get("canonical_term")
        if st not in table_mapping:
            fail(f"applied_terms[{i}].source_term {st!r} not in table {table_id!r} (MA-5)")
        if ct != table_mapping[st]:
            fail(f"applied_terms[{i}].canonical_term {ct!r} mismatches table mapping {table_mapping[st]!r} (MA-5)")
        norm_applied.append({
            "source_term": st,
            "canonical_term": ct,
            "table_entry_index": table_index[st],
        })
    norm_applied.sort(key=lambda x: x["table_entry_index"])

    raw_text_sha256 = sha256_text(raw_text or "")
    normalized_text = raw_text or ""
    for st, ct in sorted(table_mapping.items(), key=lambda kv: -len(kv[0])):
        normalized_text = normalized_text.replace(st, ct)
    normalized_text_sha256 = sha256_text(normalized_text)

    record = {
        "schema": LAYER_SCHEMA,
        "application_id": application_id,
        "table_id": table_id,
        "source_evidence_id": source_evidence_id,
        "applied_terms": norm_applied,
        "raw_text_sha256": raw_text_sha256,
        "normalized_text_sha256": normalized_text_sha256,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
        "lineage_preserved": True,
        "no_machine_translation": True,
    }
    write_json(ML_APPLICATIONS / f"{application_id}-{_now()}.json", record)
    append_event(ES_ML_APPLY, {
        "occurred_at_iso": _iso_now(),
        "kind": "multilingual-normalization-apply",
        "application_id": application_id,
        "table_id": table_id,
        "applied_term_count": len(norm_applied),
        "reviewer": reviewer,
    })
    append_audit("multilingual-normalization-apply", reviewer,
                 {"application_id": application_id, "table_id": table_id})
    return {"application_id": application_id, "applied_term_count": len(norm_applied),
            "raw_text_sha256": raw_text_sha256, "normalized_text_sha256": normalized_text_sha256}


def handle_export_stability_guarantee(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "ES-6")
    reject_probabilistic(payload)
    reject_translation(payload)
    guarantee_id = payload.get("guarantee_id")
    stabilization_id = payload.get("stabilization_id")
    prior_guarantee_id = payload.get("prior_guarantee_id")
    if not guarantee_id:
        fail("payload.guarantee_id required (ES-1)")
    stab = find_stabilization(stabilization_id) if stabilization_id else None
    if not stab:
        fail(f"stabilization_id {stabilization_id!r} not found (ES-2)")

    canonical_id_map = stab.get("canonical_id_map", {})
    sections = stab.get("stable_export_payload", {}).get("sections", [])
    section_ordering = [s.get("canonical_section_id") for s in sections]
    section_ordering_sha256 = sha256_text(canonical_json(section_ordering))
    canonical_id_map_sha256 = sha256_text(canonical_json(dict(sorted(canonical_id_map.items()))))
    export_payload_sha256 = stab.get("stable_export_sha256")
    if not export_payload_sha256:
        fail("stabilization missing stable_export_sha256 (ES-3)")
    recomputed = sha256_text(canonical_json(stab.get("stable_export_payload", {})))
    if recomputed != export_payload_sha256:
        fail(f"stabilization stable_export_sha256 not reproducible (recomputed {recomputed!r} vs stored {export_payload_sha256!r}) (ES-5)")

    invariants = {
        "section_ordering_sha256": section_ordering_sha256,
        "canonical_id_map_sha256": canonical_id_map_sha256,
        "export_payload_sha256": export_payload_sha256,
    }

    if prior_guarantee_id:
        prior = _scan_for_id(EXPORT_GUARANTEES, "guarantee_id", prior_guarantee_id)
        if not prior:
            fail(f"prior_guarantee_id {prior_guarantee_id!r} not found (ES-4)")
        prior_inv = prior.get("deterministic_invariants", {})
        for k, v in invariants.items():
            if prior_inv.get(k) != v:
                fail(f"invariant {k!r} regressed: prior {prior_inv.get(k)!r} != now {v!r} (ES-5)")

    record = {
        "schema": LAYER_SCHEMA,
        "guarantee_id": guarantee_id,
        "stabilization_id": stabilization_id,
        "package_id": stab.get("package_id"),
        "deterministic_invariants": invariants,
        "guarantee_state": "reaffirmed",
        "supersedes_prior_guarantee_id": prior_guarantee_id,
        "section_count": len(sections),
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(EXPORT_GUARANTEES / f"{guarantee_id}-{_now()}.json", record)
    append_event(ES_GUARANTEE, {
        "occurred_at_iso": _iso_now(),
        "kind": "export-stability-guarantee",
        "guarantee_id": guarantee_id,
        "stabilization_id": stabilization_id,
        "export_payload_sha256": export_payload_sha256,
        "reviewer": reviewer,
    })
    append_audit("export-stability-guarantee", reviewer,
                 {"guarantee_id": guarantee_id, "stabilization_id": stabilization_id})
    return {"guarantee_id": guarantee_id, "deterministic_invariants": invariants}


def handle_canonical_drift_detect(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "CD-7")
    reject_probabilistic(payload)
    reject_translation(payload)
    drift_id = payload.get("drift_id")
    canonical_entity_id = payload.get("canonical_entity_id")
    canonical_procedure_id = payload.get("canonical_procedure_id")
    drift_kind = payload.get("drift_kind")
    severity = payload.get("severity", "informational")
    new_evidence_refs = payload.get("new_evidence_refs")
    reviewer_rationale = payload.get("reviewer_rationale", "")
    affected_downstream_refs = payload.get("affected_downstream_refs", [])
    if not drift_id:
        fail("payload.drift_id required (CD-1)")
    if bool(canonical_entity_id) == bool(canonical_procedure_id):
        fail("EXACTLY ONE of canonical_entity_id or canonical_procedure_id required (CD-2)")
    target_kind = "canonical-entity" if canonical_entity_id else "canonical-procedure"
    if canonical_entity_id:
        target = find_canonical_entity(canonical_entity_id)
        target_id = canonical_entity_id
    else:
        target = find_canonical_procedure(canonical_procedure_id)
        target_id = canonical_procedure_id
    if not target:
        fail(f"target {target_id!r} ({target_kind}) not found (CD-3)")
    if drift_kind not in DRIFT_KINDS:
        fail(f"drift_kind {drift_kind!r} not in {sorted(DRIFT_KINDS)} (CD-4)")
    if not isinstance(new_evidence_refs, list) or not new_evidence_refs:
        fail("new_evidence_refs must be a non-empty list (CD-5)")
    if severity not in SEVERITY:
        fail(f"severity {severity!r} not in {sorted(SEVERITY)} (CD-4)")
    if not isinstance(reviewer_rationale, str) or not reviewer_rationale.strip():
        fail("reviewer_rationale required (CD-6)")
    if not isinstance(affected_downstream_refs, list):
        fail("affected_downstream_refs must be a list (CD-8)")

    prior_canonical_sha256 = target.get("canonical_sha256")
    record = {
        "schema": LAYER_SCHEMA,
        "drift_id": drift_id,
        "target_kind": target_kind,
        "target_id": target_id,
        "drift_kind": drift_kind,
        "severity": severity,
        "new_evidence_refs": sorted(set(new_evidence_refs)),
        "affected_downstream_refs": sorted(set(affected_downstream_refs)),
        "prior_canonical_sha256_pointer": prior_canonical_sha256,
        "reviewer_rationale": reviewer_rationale,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
        "no_silent_canonical_mutation": True,
        "pointer_only": True,
    }
    write_json(DRIFT_RECORDS / f"{drift_id}-{_now()}.json", record)
    append_event(ES_DRIFT, {
        "occurred_at_iso": _iso_now(),
        "kind": "canonical-drift-detect",
        "drift_id": drift_id,
        "target_kind": target_kind,
        "target_id": target_id,
        "drift_kind": drift_kind,
        "severity": severity,
        "reviewer": reviewer,
    })
    append_audit("canonical-drift-detect", reviewer,
                 {"drift_id": drift_id, "target_id": target_id, "drift_kind": drift_kind})
    return {"drift_id": drift_id, "target_kind": target_kind, "prior_canonical_sha256_pointer": prior_canonical_sha256}


def handle_reviewer_summary_publish(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "RS-4")
    reject_probabilistic(payload)
    reject_translation(payload)
    summary_id = payload.get("summary_id")
    summary_kind = payload.get("summary_kind")
    aggregated_refs = payload.get("aggregated_refs")
    notes = payload.get("notes", "")
    if not summary_id:
        fail("payload.summary_id required (RS-1)")
    if summary_kind not in SUMMARY_KINDS:
        fail(f"summary_kind {summary_kind!r} not in {sorted(SUMMARY_KINDS)} (RS-2)")
    if not isinstance(aggregated_refs, list) or not aggregated_refs:
        fail("aggregated_refs must be a non-empty list (RS-3)")
    norm_refs = []
    for i, r in enumerate(aggregated_refs):
        if not isinstance(r, dict):
            fail(f"aggregated_refs[{i}] must be a dict {{kind, id}} (RS-3)")
        if not isinstance(r.get("kind"), str) or not isinstance(r.get("id"), str):
            fail(f"aggregated_refs[{i}] requires string kind and id (RS-3)")
        norm_refs.append({"kind": r["kind"], "id": r["id"]})
    norm_refs.sort(key=lambda x: (x["kind"], x["id"]))

    summary_payload = {
        "summary_id": summary_id,
        "summary_kind": summary_kind,
        "aggregated_refs": norm_refs,
        "notes": notes,
    }
    summary_sha256 = sha256_text(canonical_json(summary_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **summary_payload,
        "summary_sha256": summary_sha256,
        "ref_count": len(norm_refs),
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
        "presentation_neutral": True,
        "pointer_only": True,
    }
    write_json(REVIEWER_SUMMARIES / f"{summary_id}-{_now()}.json", record)
    append_event(ES_SUMMARY, {
        "occurred_at_iso": _iso_now(),
        "kind": "reviewer-summary-publish",
        "summary_id": summary_id,
        "summary_kind": summary_kind,
        "ref_count": len(norm_refs),
        "summary_sha256": summary_sha256,
        "reviewer": reviewer,
    })
    append_audit("reviewer-summary-publish", reviewer,
                 {"summary_id": summary_id, "summary_kind": summary_kind})
    return {"summary_id": summary_id, "summary_sha256": summary_sha256, "ref_count": len(norm_refs)}


def handle_incremental_refresh_propagate(reviewer: str, payload: dict) -> dict:
    assert_target_path(payload)
    reject_probabilistic(payload)
    reject_translation(payload)
    refresh_id = payload.get("refresh_id")
    trigger_kind = payload.get("trigger_kind")
    trigger_ref = payload.get("trigger_ref")
    affected_set = payload.get("affected_set", [])
    unaffected_stable_set = payload.get("unaffected_stable_set", [])
    if not refresh_id:
        fail("payload.refresh_id required (IR-1)")
    if trigger_kind not in REFRESH_TRIGGER_KINDS:
        fail(f"trigger_kind {trigger_kind!r} not in {sorted(REFRESH_TRIGGER_KINDS)} (IR-2)")

    if trigger_kind == "approved-intake":
        ap = find_intake_approval(trigger_ref)
        if not ap or ap.get("decision") != "approve":
            fail(f"trigger_ref {trigger_ref!r} is not an approved intake (IR-3)")
    elif trigger_kind == "canonical-promotion":
        if not (find_canonical_entity(trigger_ref) or find_canonical_procedure(trigger_ref)):
            fail(f"trigger_ref {trigger_ref!r} is not a canonical entity or procedure (IR-3)")
    elif trigger_kind == "arbitration-resolution":
        if not find_arbitration_decision(trigger_ref):
            fail(f"trigger_ref {trigger_ref!r} is not an arbitration decision (IR-3)")
    elif trigger_kind == "drift-detection":
        if not _scan_for_id(DRIFT_RECORDS, "drift_id", trigger_ref):
            fail(f"trigger_ref {trigger_ref!r} is not a drift record (IR-3)")
    elif trigger_kind == "stability-guarantee-reaffirmed":
        if not _scan_for_id(EXPORT_GUARANTEES, "guarantee_id", trigger_ref):
            fail(f"trigger_ref {trigger_ref!r} is not a stability guarantee (IR-3)")

    if not isinstance(affected_set, list):
        fail("affected_set must be a list (IR-4)")
    if not isinstance(unaffected_stable_set, list):
        fail("unaffected_stable_set must be a list (IR-5)")
    norm_affected = []
    for i, a in enumerate(affected_set):
        if not isinstance(a, dict) or not isinstance(a.get("kind"), str) or not isinstance(a.get("id"), str):
            fail(f"affected_set[{i}] must be {{kind, id}} (IR-4)")
        norm_affected.append({"kind": a["kind"], "id": a["id"]})
    norm_unaffected = []
    for i, a in enumerate(unaffected_stable_set):
        if not isinstance(a, dict) or not isinstance(a.get("kind"), str) or not isinstance(a.get("id"), str):
            fail(f"unaffected_stable_set[{i}] must be {{kind, id}} (IR-5)")
        norm_unaffected.append({"kind": a["kind"], "id": a["id"]})
    norm_affected.sort(key=lambda x: (x["kind"], x["id"]))
    norm_unaffected.sort(key=lambda x: (x["kind"], x["id"]))

    record = {
        "schema": LAYER_SCHEMA,
        "refresh_id": refresh_id,
        "trigger_kind": trigger_kind,
        "trigger_ref": trigger_ref,
        "affected_set": norm_affected,
        "unaffected_stable_set": norm_unaffected,
        "affected_count": len(norm_affected),
        "unaffected_count": len(norm_unaffected),
        "transaction_safe": True,
        "pointer_only": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(INCREMENTAL_REFRESH / f"{refresh_id}-{_now()}.json", record)
    append_event(ES_REFRESH, {
        "occurred_at_iso": _iso_now(),
        "kind": "incremental-refresh-propagate",
        "refresh_id": refresh_id,
        "trigger_kind": trigger_kind,
        "affected_count": len(norm_affected),
        "unaffected_count": len(norm_unaffected),
        "reviewer": reviewer,
    })
    append_audit("incremental-refresh-propagate", reviewer,
                 {"refresh_id": refresh_id, "trigger_kind": trigger_kind})
    return {"refresh_id": refresh_id, "affected_count": len(norm_affected),
            "unaffected_count": len(norm_unaffected)}


def _audit_scan_findings(package_id: str, manual_id: str | None) -> list[dict]:
    findings: list[dict] = []

    # Unresolved blocking conflicts (no accept arbitration)
    if SC_CONFLICTS.exists():
        for p in sorted(SC_CONFLICTS.glob("*.json")):
            try:
                cf = read_json(p)
            except Exception:
                continue
            if cf.get("severity") != "blocking":
                continue
            cid = cf.get("conflict_id")
            resolved = False
            if SC_ARBITRATION.exists():
                for ap in sorted(SC_ARBITRATION.glob("*.json")):
                    try:
                        ad = read_json(ap)
                    except Exception:
                        continue
                    if ad.get("conflict_id") == cid and ad.get("decision") == "accept":
                        resolved = True
                        break
            if not resolved:
                findings.append({"check": "unresolved-blocking-conflict", "severity": "blocking",
                                 "ref_kind": "conflict", "ref_id": cid})

    # Unresolved drift records on canonical entities/procedures
    if DRIFT_RECORDS.exists():
        for p in sorted(DRIFT_RECORDS.glob("*.json")):
            try:
                d = read_json(p)
            except Exception:
                continue
            if d.get("severity") in ("major", "blocking"):
                findings.append({"check": "unresolved-drift", "severity": d.get("severity"),
                                 "ref_kind": "drift", "ref_id": d.get("drift_id")})

    # Stability guarantee presence — at least one for the package
    has_guarantee = False
    if EXPORT_GUARANTEES.exists():
        for p in sorted(EXPORT_GUARANTEES.glob("*.json")):
            try:
                g = read_json(p)
            except Exception:
                continue
            if g.get("package_id") == package_id:
                has_guarantee = True
                break
    if not has_guarantee:
        findings.append({"check": "missing-export-stability-guarantee", "severity": "major",
                         "ref_kind": "package", "ref_id": package_id})

    # Visual support presence for the manual
    has_visual = False
    if VISUAL_SUPPORT.exists():
        for p in sorted(VISUAL_SUPPORT.glob("*.json")):
            try:
                v = read_json(p)
            except Exception:
                continue
            if v.get("manual_id") == manual_id or v.get("package_id") == package_id:
                has_visual = True
                break
    if not has_visual:
        findings.append({"check": "missing-visual-support", "severity": "minor",
                         "ref_kind": "package", "ref_id": package_id})

    findings.sort(key=lambda f: (f["check"], f.get("ref_id", "")))
    return findings


def handle_readiness_audit_run(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "RA-7")
    reject_probabilistic(payload)
    reject_translation(payload)
    audit_id = payload.get("audit_id")
    package_id = payload.get("package_id")
    if not audit_id:
        fail("payload.audit_id required (RA-1)")
    pkg = find_package(package_id) if package_id else None
    if not pkg:
        fail(f"package_id {package_id!r} not found (RA-2)")
    state = package_lifecycle_state(package_id)
    if state != "export-ready":
        fail(f"package {package_id!r} lifecycle state is {state!r}, must be 'export-ready' (RA-2)")

    findings = _audit_scan_findings(package_id, pkg.get("manual_id"))
    severity_counts = {s: 0 for s in SEVERITY}
    for f in findings:
        sv = f.get("severity")
        if sv in severity_counts:
            severity_counts[sv] += 1
    blocking_or_major = severity_counts["blocking"] + severity_counts["major"]
    status = "ready" if blocking_or_major == 0 else "not-ready"

    audit_payload = {
        "audit_id": audit_id,
        "package_id": package_id,
        "manual_id": pkg.get("manual_id"),
        "status": status,
        "findings": findings,
        "finding_count_by_severity": severity_counts,
    }
    audit_sha256 = sha256_text(canonical_json(audit_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **audit_payload,
        "audit_sha256": audit_sha256,
        "informational_only": True,
        "reviewer_authoritative": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(READINESS_AUDITS / f"{audit_id}-{_now()}.json", record)
    append_event(ES_AUDIT_RA, {
        "occurred_at_iso": _iso_now(),
        "kind": "readiness-audit-run",
        "audit_id": audit_id,
        "package_id": package_id,
        "status": status,
        "finding_count": len(findings),
        "audit_sha256": audit_sha256,
        "reviewer": reviewer,
    })
    append_audit("readiness-audit-run", reviewer,
                 {"audit_id": audit_id, "package_id": package_id, "status": status})
    return {"audit_id": audit_id, "status": status, "audit_sha256": audit_sha256,
            "finding_count": len(findings), "finding_count_by_severity": severity_counts}


def handle_closure_path_record(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "CL-6")
    reject_probabilistic(payload)
    reject_translation(payload)
    closure_id = payload.get("closure_id")
    package_id = payload.get("package_id")
    path_steps = payload.get("path_steps")
    if not closure_id:
        fail("payload.closure_id required (CL-1)")
    pkg = find_package(package_id) if package_id else None
    if not pkg:
        fail(f"package_id {package_id!r} not found (CL-2)")
    if not isinstance(path_steps, list) or len(path_steps) != len(CLOSURE_STAGES):
        fail(f"path_steps must be a list of {len(CLOSURE_STAGES)} stages in canonical order (CL-3)")

    norm_steps = []
    for i, step in enumerate(path_steps):
        expected_stage = CLOSURE_STAGES[i]
        if not isinstance(step, dict):
            fail(f"path_steps[{i}] must be a dict (CL-3)")
        if step.get("stage") != expected_stage:
            fail(f"path_steps[{i}].stage {step.get('stage')!r} != expected {expected_stage!r} (CL-3)")
        ref_id = step.get("ref_id")
        if not isinstance(ref_id, str) or not ref_id.strip():
            fail(f"path_steps[{i}].ref_id required (CL-4)")
        # Stage-specific resolution.
        resolved = False
        if expected_stage == "evidence":
            resolved = bool(ref_id)
        elif expected_stage == "analysis":
            resolved = find_intake_analysis(ref_id) is not None
        elif expected_stage == "convergence":
            resolved = find_fusion_cluster(ref_id) is not None
        elif expected_stage == "canonical-entity":
            resolved = find_canonical_entity(ref_id) is not None
        elif expected_stage == "canonical-procedure":
            resolved = find_canonical_procedure(ref_id) is not None
        elif expected_stage == "visual-support":
            resolved = find_visual_support(ref_id) is not None
        elif expected_stage == "prompt-package":
            resolved = find_prompt_package(ref_id) is not None
        elif expected_stage == "stabilized-export":
            resolved = find_stabilization(ref_id) is not None
        elif expected_stage == "readiness-audit":
            resolved = _scan_for_id(READINESS_AUDITS, "audit_id", ref_id) is not None
        elif expected_stage == "consumer-payload":
            resolved = find_export_finalization(ref_id) is not None
        if not resolved:
            fail(f"path_steps[{i}] ref_id {ref_id!r} did not resolve in stage {expected_stage!r} (CL-4)")
        norm_steps.append({"step_index": i + 1, "stage": expected_stage, "ref_id": ref_id})

    closure_payload = {
        "closure_id": closure_id,
        "package_id": package_id,
        "manual_id": pkg.get("manual_id"),
        "path_steps": norm_steps,
    }
    closure_sha256 = sha256_text(canonical_json(closure_payload))
    record = {
        "schema": LAYER_SCHEMA,
        **closure_payload,
        "closure_sha256": closure_sha256,
        "step_count": len(norm_steps),
        "pointer_only": True,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(CLOSURE_PATHS / f"{closure_id}-{_now()}.json", record)
    append_event(ES_CLOSURE, {
        "occurred_at_iso": _iso_now(),
        "kind": "closure-path-record",
        "closure_id": closure_id,
        "package_id": package_id,
        "step_count": len(norm_steps),
        "closure_sha256": closure_sha256,
        "reviewer": reviewer,
    })
    append_audit("closure-path-record", reviewer,
                 {"closure_id": closure_id, "package_id": package_id})
    return {"closure_id": closure_id, "closure_sha256": closure_sha256,
            "step_count": len(norm_steps)}


# ============================================================================
# Dispatch table & CLI
# ============================================================================
DISPATCH = {
    "evidence-robustness-record": handle_evidence_robustness_record,
    "multilingual-normalization-table-create": handle_multilingual_normalization_table_create,
    "multilingual-normalization-apply": handle_multilingual_normalization_apply,
    "export-stability-guarantee": handle_export_stability_guarantee,
    "canonical-drift-detect": handle_canonical_drift_detect,
    "reviewer-summary-publish": handle_reviewer_summary_publish,
    "incremental-refresh-propagate": handle_incremental_refresh_propagate,
    "readiness-audit-run": handle_readiness_audit_run,
    "closure-path-record": handle_closure_path_record,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 56 production-closure executor")
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
