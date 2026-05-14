#!/usr/bin/env python3
"""
Phase 55 executor — semantic convergence, cross-evidence fusion &
operational runtime cohesion (constitutional layer 48).

Request envelope: governed-fs-operation-request/1.0
CLI: --kind <dispatch> --request <envelope.json> --confirm

Deterministic, reviewer-authoritative, append-only. Wires existing
runtimes (Phase 52 extraction, Phase 53 packaging, Phase 54 closure)
into one cohesive semantic manual-generation system WITHOUT expanding
governance, WITHOUT embeddings, WITHOUT autonomous arbitration.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = "governed-fs-operation-request/1.0"
LAYER_SCHEMA = "semantic-convergence-cross-evidence-fusion/1.0"
LAYER = 48

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"

# Phase 55 isolated storage tree
SC_ROOT = OC_ROOT / "semantic-convergence-runtime"
EVIDENCE_FINGERPRINTS = SC_ROOT / "evidence-fingerprints"
FUSION_CLUSTERS = SC_ROOT / "fusion-clusters"
CANONICAL_ENTITIES = SC_ROOT / "canonical-entities"
CANONICAL_PROCEDURES = SC_ROOT / "canonical-procedures"
CONFLICT_SURFACINGS = SC_ROOT / "conflict-surfacings"
ARBITRATION_DECISIONS = SC_ROOT / "arbitration-decisions"
REFRESH_COHESION_RECORDS = SC_ROOT / "refresh-cohesion-records"
WORKSPACE_FLOWS = SC_ROOT / "workspace-flows"
ROBUSTNESS_RECORDS = SC_ROOT / "robustness-records"
EXPORT_STABILIZATIONS = SC_ROOT / "export-stabilizations"

# Upstream (READ-ONLY) trees
PACKAGING_RUNTIME = OC_ROOT / "manual-semantic-packaging-runtime"
PACKAGES_DIR = PACKAGING_RUNTIME / "manual-packages"
SECTIONS_DIR = PACKAGING_RUNTIME / "semantic-sections"
EXTRACTION_RUNTIME = OC_ROOT / "semantic-extraction-runtime"
MR_ROOT = OC_ROOT / "manual-runtime-closure"
INTAKE_APPROVALS = MR_ROOT / "intake-approvals"

# Event stores
ES_FINGERPRINT = RUNTIME_MANIFESTS_ROOT / "evidence-fingerprint-events" / "_event-store.json"
ES_FUSION = RUNTIME_MANIFESTS_ROOT / "fusion-cluster-events" / "_event-store.json"
ES_CANONICAL_ENTITY = RUNTIME_MANIFESTS_ROOT / "canonical-entity-events" / "_event-store.json"
ES_CANONICAL_PROC = RUNTIME_MANIFESTS_ROOT / "canonical-procedure-events" / "_event-store.json"
ES_CONFLICT = RUNTIME_MANIFESTS_ROOT / "conflict-surfacing-events" / "_event-store.json"
ES_ARBITRATION = RUNTIME_MANIFESTS_ROOT / "arbitration-decision-events" / "_event-store.json"
ES_REFRESH = RUNTIME_MANIFESTS_ROOT / "refresh-cohesion-events" / "_event-store.json"
ES_WORKSPACE = RUNTIME_MANIFESTS_ROOT / "workspace-flow-events" / "_event-store.json"
ES_STABILIZE = RUNTIME_MANIFESTS_ROOT / "export-stabilization-events" / "_event-store.json"
ES_AUDIT = RUNTIME_MANIFESTS_ROOT / "audit-events" / "_event-store.json"

STRUCTURAL_KINDS = {
    "procedure-step", "warning", "specification",
    "troubleshooting", "app-flow", "navigation", "maintenance",
}
PROCEDURE_CLASS_KINDS = {"procedure-step", "app-flow", "troubleshooting", "navigation", "maintenance"}
ENTITY_KINDS = {"entity", "warning", "specification"}
CONFLICT_KINDS = {"specification-conflict", "procedure-conflict", "warning-conflict", "troubleshooting-conflict"}
CONFLICT_SEVERITY = {"informational", "minor", "major", "blocking"}
ARBITRATION_DECISIONS_ENUM = {"accept", "reject", "defer", "escalate"}
REFRESH_TRIGGER_KINDS = {"approved-intake", "canonical-promotion", "arbitration-resolution"}
WORKSPACE_FLOW_STAGES = {
    "evidence", "analysis", "fusion", "canonical-entity", "canonical-procedure",
    "conflict", "arbitration", "synthesis", "visual-support", "prompt-package", "export",
}
ROBUSTNESS_KINDS = {
    "incomplete-evidence", "noisy-ocr", "duplicate-document", "conflicting-oem-doc",
    "low-quality-screenshot", "partial-video", "multilingual-evidence", "fragmented-support-export",
}

FORBIDDEN_OVERWRITE_PREFIXES = (
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

# Forbidden probabilistic / embedding keys — Phase 55 must remain deterministic.
FORBIDDEN_PROBABILISTIC_KEYS = {
    "embedding", "embeddings", "vector", "vectors",
    "similarity_score", "semantic_score", "cosine_similarity",
    "ml_model", "model_inference", "probabilistic", "probability",
    "autonomous_decision", "autonomous_arbitration",
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


def reject_probabilistic(payload: dict, rule_id: str = "EFP-2") -> None:
    hit = find_forbidden_key(payload, FORBIDDEN_PROBABILISTIC_KEYS)
    if hit:
        fail(f"probabilistic/embedding key '{hit[1]}' at {hit[0]} forbidden — deterministic fingerprints only ({rule_id})")


def assert_target_path(payload: dict) -> None:
    tp = payload.get("target_path")
    if isinstance(tp, str) and tp:
        norm = tp.replace("\\", "/")
        for prefix in FORBIDDEN_OVERWRITE_PREFIXES:
            if prefix in norm:
                fail(f"target_path falls under a forbidden prefix '{prefix}' (RC-5)")


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
        "audit_event_id": f"a55-{kind}-{_now()}",
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


def find_fingerprint(fid: str) -> dict | None:
    return _scan_for_id(EVIDENCE_FINGERPRINTS, "fingerprint_id", fid)


def find_cluster(cid: str) -> dict | None:
    return _scan_for_id(FUSION_CLUSTERS, "cluster_id", cid)


def find_conflict(cid: str) -> dict | None:
    return _scan_for_id(CONFLICT_SURFACINGS, "conflict_id", cid)


def find_intake_approval(aid: str) -> dict | None:
    return _scan_for_id(INTAKE_APPROVALS, "approval_id", aid)


def find_canonical_entity(eid: str) -> dict | None:
    return _scan_for_id(CANONICAL_ENTITIES, "canonical_entity_id", eid)


def find_canonical_procedure(pid: str) -> dict | None:
    return _scan_for_id(CANONICAL_PROCEDURES, "canonical_procedure_id", pid)


def find_arbitration_decision(did: str) -> dict | None:
    return _scan_for_id(ARBITRATION_DECISIONS, "decision_id", did)


def find_package(pid: str) -> dict | None:
    return _scan_for_id(PACKAGES_DIR, "package_id", pid)


def find_existing_stabilization(package_id: str) -> dict | None:
    if not EXPORT_STABILIZATIONS.exists():
        return None
    matches = []
    for p in sorted(EXPORT_STABILIZATIONS.glob("*.json")):
        try:
            d = read_json(p)
        except Exception:
            continue
        if d.get("package_id") == package_id:
            matches.append(d)
    return matches[-1] if matches else None


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
# Deterministic normalization & fingerprinting
# ============================================================================
_PUNCT_RE = re.compile(r"[^\w\s]+", re.UNICODE)
_WS_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Deterministic text normalization: lowercase, strip punctuation, collapse whitespace."""
    if not isinstance(text, str):
        return ""
    s = text.lower()
    s = _PUNCT_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s).strip()
    return s


def compute_fingerprint(structural_kind: str, normalized_text: str, structural_features: dict) -> str:
    canonical = {
        "structural_kind": structural_kind,
        "normalized_text": normalized_text,
        "structural_features": dict(sorted(structural_features.items())) if isinstance(structural_features, dict) else {},
    }
    return sha256_text(canonical_json(canonical))


# ============================================================================
# Dispatch handlers
# ============================================================================
def handle_evidence_fingerprint(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "EFP-6")
    reject_probabilistic(payload, "EFP-2")
    fingerprint_id = payload.get("fingerprint_id")
    source_evidence_id = payload.get("source_evidence_id")
    structural_kind = payload.get("structural_kind")
    raw_text = payload.get("raw_text", "")
    structural_features = payload.get("structural_features", {})
    evidence_refs = payload.get("evidence_refs")
    grounding_refs = payload.get("grounding_refs", [])

    if not fingerprint_id:
        fail("payload.fingerprint_id required (EFP-1)")
    if not source_evidence_id:
        fail("payload.source_evidence_id required (EFP-1)")
    if structural_kind not in STRUCTURAL_KINDS:
        fail(f"structural_kind {structural_kind!r} not in {sorted(STRUCTURAL_KINDS)} (EFP-4)")
    if not isinstance(structural_features, dict):
        fail("payload.structural_features must be a dict (EFP-2)")
    if not isinstance(evidence_refs, list) or not evidence_refs:
        fail("payload.evidence_refs must be a non-empty list (EFP-5)")
    if not isinstance(grounding_refs, list):
        fail("payload.grounding_refs must be a list if provided (EFP-5)")

    normalized = normalize_text(raw_text)
    fingerprint_sha256 = compute_fingerprint(structural_kind, normalized, structural_features)

    record = {
        "schema": LAYER_SCHEMA,
        "fingerprint_id": fingerprint_id,
        "source_evidence_id": source_evidence_id,
        "structural_kind": structural_kind,
        "normalized_text": normalized,
        "structural_features": dict(sorted(structural_features.items())),
        "evidence_refs": sorted(evidence_refs),
        "grounding_refs": sorted(grounding_refs),
        "fingerprint_sha256": fingerprint_sha256,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(EVIDENCE_FINGERPRINTS / f"{fingerprint_id}-{_now()}.json", record)
    append_event(ES_FINGERPRINT, {
        "occurred_at_iso": _iso_now(),
        "kind": "evidence-fingerprint",
        "fingerprint_id": fingerprint_id,
        "structural_kind": structural_kind,
        "fingerprint_sha256": fingerprint_sha256,
        "reviewer": reviewer,
    })
    append_audit("evidence-fingerprint", reviewer, {"fingerprint_id": fingerprint_id})
    return {"fingerprint_id": fingerprint_id, "fingerprint_sha256": fingerprint_sha256}


def handle_fusion_cluster_form(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "EFP-6")
    reject_probabilistic(payload)
    cluster_id = payload.get("cluster_id")
    members = payload.get("member_fingerprint_ids")
    if not cluster_id:
        fail("payload.cluster_id required (FC-1)")
    if not isinstance(members, list) or not members:
        fail("payload.member_fingerprint_ids must be a non-empty list (FC-2)")

    resolved: list[dict] = []
    structural_kind = None
    evidence_union: set[str] = set()
    grounding_union: set[str] = set()
    fingerprint_shas: list[str] = []
    for fid in sorted(set(members)):
        fp = find_fingerprint(fid)
        if not fp:
            fail(f"member fingerprint {fid!r} not found (FC-2)")
        if structural_kind is None:
            structural_kind = fp.get("structural_kind")
        elif fp.get("structural_kind") != structural_kind:
            fail(f"members span multiple structural_kinds (FC-4): {structural_kind!r} vs {fp.get('structural_kind')!r}")
        evidence_union.update(fp.get("evidence_refs", []))
        grounding_union.update(fp.get("grounding_refs", []))
        fingerprint_shas.append(fp.get("fingerprint_sha256", ""))
        resolved.append(fp)

    cluster_fingerprint = sha256_text(canonical_json(sorted(fingerprint_shas)))
    record = {
        "schema": LAYER_SCHEMA,
        "cluster_id": cluster_id,
        "member_fingerprint_ids": sorted(set(members)),
        "structural_kind": structural_kind,
        "evidence_refs_union": sorted(evidence_union),
        "grounding_refs_union": sorted(grounding_union),
        "cluster_fingerprint": cluster_fingerprint,
        "cluster_state": "pending-review",
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
        "member_count": len(resolved),
    }
    write_json(FUSION_CLUSTERS / f"{cluster_id}-{_now()}.json", record)
    append_event(ES_FUSION, {
        "occurred_at_iso": _iso_now(),
        "kind": "fusion-cluster-form",
        "cluster_id": cluster_id,
        "member_count": len(resolved),
        "structural_kind": structural_kind,
        "cluster_fingerprint": cluster_fingerprint,
        "reviewer": reviewer,
    })
    append_audit("fusion-cluster-form", reviewer, {"cluster_id": cluster_id, "member_count": len(resolved)})
    return {"cluster_id": cluster_id, "cluster_fingerprint": cluster_fingerprint, "member_count": len(resolved)}


def handle_canonical_entity_promote(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "CE-6")
    reject_probabilistic(payload)
    entity_id = payload.get("canonical_entity_id")
    cluster_id = payload.get("source_cluster_id")
    entity_kind = payload.get("entity_kind")
    canonical_payload = payload.get("canonical_payload", {})
    if not entity_id:
        fail("payload.canonical_entity_id required (CE-1)")
    cluster = find_cluster(cluster_id) if cluster_id else None
    if not cluster:
        fail(f"source_cluster_id {cluster_id!r} not found (CE-2)")
    if entity_kind not in ENTITY_KINDS:
        fail(f"entity_kind {entity_kind!r} not in {sorted(ENTITY_KINDS)} (CE-3)")
    if not isinstance(canonical_payload, dict):
        fail("payload.canonical_payload must be a dict (CE-6)")
    reject_presentation(canonical_payload, "CE-6")

    lineage_pointers = {
        "source_cluster_id": cluster_id,
        "member_fingerprint_ids": cluster.get("member_fingerprint_ids", []),
        "evidence_refs": cluster.get("evidence_refs_union", []),
        "grounding_refs": cluster.get("grounding_refs_union", []),
    }
    canonical = {
        "canonical_entity_id": entity_id,
        "entity_kind": entity_kind,
        "canonical_payload": canonical_payload,
        "lineage_pointers": lineage_pointers,
    }
    canonical_sha256 = sha256_text(canonical_json(canonical))
    record = {
        "schema": LAYER_SCHEMA,
        "occurred_at_iso": _iso_now(),
        "reviewer": reviewer,
        "canonical_sha256": canonical_sha256,
        **canonical,
    }
    write_json(CANONICAL_ENTITIES / f"{entity_id}-{_now()}.json", record)
    append_event(ES_CANONICAL_ENTITY, {
        "occurred_at_iso": _iso_now(),
        "kind": "canonical-entity-promote",
        "canonical_entity_id": entity_id,
        "source_cluster_id": cluster_id,
        "entity_kind": entity_kind,
        "canonical_sha256": canonical_sha256,
        "reviewer": reviewer,
    })
    append_audit("canonical-entity-promote", reviewer, {"canonical_entity_id": entity_id})
    return {"canonical_entity_id": entity_id, "canonical_sha256": canonical_sha256}


def handle_canonical_procedure_converge(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "CP-7")
    reject_probabilistic(payload)
    proc_id = payload.get("canonical_procedure_id")
    cluster_ids = payload.get("source_cluster_ids")
    step_sequence = payload.get("step_sequence")
    if not proc_id:
        fail("payload.canonical_procedure_id required (CP-1)")
    if not isinstance(cluster_ids, list) or not cluster_ids:
        fail("payload.source_cluster_ids must be a non-empty list (CP-2)")
    if not isinstance(step_sequence, list) or not step_sequence:
        fail("payload.step_sequence must be a non-empty list (CP-3)")

    resolved_clusters = []
    for cid in cluster_ids:
        c = find_cluster(cid)
        if not c:
            fail(f"source_cluster_id {cid!r} not found (CP-2)")
        if c.get("structural_kind") not in PROCEDURE_CLASS_KINDS:
            fail(f"cluster {cid!r} has structural_kind {c.get('structural_kind')!r} which is not procedure-class (CP-2)")
        resolved_clusters.append(c)
    cluster_member_index = {fid for c in resolved_clusters for fid in c.get("member_fingerprint_ids", [])}

    # Validate step ordering 1..N and source references.
    for i, step in enumerate(step_sequence, 1):
        if not isinstance(step, dict):
            fail(f"step_sequence[{i-1}] must be a dict (CP-3)")
        if step.get("step_index") != i:
            fail(f"step_sequence not contiguous 1..N (CP-3): expected {i}, got {step.get('step_index')!r}")
        srcs = step.get("source_fingerprint_ids")
        if not isinstance(srcs, list) or not srcs:
            fail(f"step {i} missing source_fingerprint_ids (CP-4)")
        for fid in srcs:
            if fid not in cluster_member_index:
                fail(f"step {i} references fingerprint {fid!r} not in any source cluster (CP-4)")
        # Preserve evidence/grounding refs (CP-5)
        if not isinstance(step.get("evidence_refs", []), list) or not step.get("evidence_refs", []):
            fail(f"step {i} missing evidence_refs (CP-5)")

    # Block on any unresolved blocking conflict for these clusters (CP-6).
    if CONFLICT_SURFACINGS.exists():
        for cp in sorted(CONFLICT_SURFACINGS.glob("*.json")):
            try:
                cf = read_json(cp)
            except Exception:
                continue
            if cf.get("severity") != "blocking":
                continue
            refs = set(cf.get("conflicting_refs", []))
            if refs & cluster_member_index:
                # Check if arbitration accepted resolution
                resolved = False
                if ARBITRATION_DECISIONS.exists():
                    for ap in sorted(ARBITRATION_DECISIONS.glob("*.json")):
                        try:
                            ad = read_json(ap)
                        except Exception:
                            continue
                        if ad.get("conflict_id") == cf.get("conflict_id") and ad.get("decision") == "accept":
                            resolved = True
                            break
                if not resolved:
                    fail(f"unresolved blocking conflict {cf.get('conflict_id')!r} gates this procedure (CP-6)")

    canonical = {
        "canonical_procedure_id": proc_id,
        "source_cluster_ids": sorted(set(cluster_ids)),
        "step_sequence": [
            {
                "step_index": s["step_index"],
                "text": s.get("text", ""),
                "source_fingerprint_ids": sorted(s["source_fingerprint_ids"]),
                "evidence_refs": sorted(s.get("evidence_refs", [])),
                "grounding_refs": sorted(s.get("grounding_refs", [])),
            }
            for s in step_sequence
        ],
    }
    canonical_sha256 = sha256_text(canonical_json(canonical))
    record = {
        "schema": LAYER_SCHEMA,
        "occurred_at_iso": _iso_now(),
        "reviewer": reviewer,
        "canonical_sha256": canonical_sha256,
        "step_count": len(step_sequence),
        **canonical,
    }
    write_json(CANONICAL_PROCEDURES / f"{proc_id}-{_now()}.json", record)
    append_event(ES_CANONICAL_PROC, {
        "occurred_at_iso": _iso_now(),
        "kind": "canonical-procedure-converge",
        "canonical_procedure_id": proc_id,
        "step_count": len(step_sequence),
        "canonical_sha256": canonical_sha256,
        "reviewer": reviewer,
    })
    append_audit("canonical-procedure-converge", reviewer, {"canonical_procedure_id": proc_id})
    return {"canonical_procedure_id": proc_id, "canonical_sha256": canonical_sha256, "step_count": len(step_sequence)}


def handle_conflict_surface(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "CS-1")
    reject_probabilistic(payload)
    conflict_id = payload.get("conflict_id")
    conflict_kind = payload.get("conflict_kind")
    refs = payload.get("conflicting_refs")
    severity = payload.get("severity")
    trust_composition = payload.get("trust_composition", {})
    rationale = payload.get("rationale", "")
    if not conflict_id:
        fail("payload.conflict_id required (CS-1)")
    if conflict_kind not in CONFLICT_KINDS:
        fail(f"conflict_kind {conflict_kind!r} not in {sorted(CONFLICT_KINDS)} (CS-2)")
    if not isinstance(refs, list) or len(set(refs)) < 2:
        fail("conflicting_refs must contain >= 2 distinct refs (CS-3)")
    if severity not in CONFLICT_SEVERITY:
        fail(f"severity {severity!r} not in {sorted(CONFLICT_SEVERITY)} (CS-4)")
    if not isinstance(trust_composition, dict) or not trust_composition:
        fail("trust_composition must be a non-empty dict (CS-5)")

    record = {
        "schema": LAYER_SCHEMA,
        "conflict_id": conflict_id,
        "conflict_kind": conflict_kind,
        "conflicting_refs": sorted(set(refs)),
        "severity": severity,
        "trust_composition": dict(sorted(trust_composition.items())),
        "rationale": rationale,
        "state": "pending-arbitration",
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(CONFLICT_SURFACINGS / f"{conflict_id}-{_now()}.json", record)
    append_event(ES_CONFLICT, {
        "occurred_at_iso": _iso_now(),
        "kind": "conflict-surface",
        "conflict_id": conflict_id,
        "conflict_kind": conflict_kind,
        "severity": severity,
        "ref_count": len(set(refs)),
        "reviewer": reviewer,
    })
    append_audit("conflict-surface", reviewer, {"conflict_id": conflict_id, "severity": severity})
    return {"conflict_id": conflict_id, "severity": severity}


def handle_arbitration_decide(reviewer: str, payload: dict) -> dict:
    reject_probabilistic(payload)
    decision_id = payload.get("decision_id")
    conflict_id = payload.get("conflict_id")
    decision = payload.get("decision")
    accepted_ref = payload.get("accepted_ref")
    cited = payload.get("cited_rule_ids", [])
    prior_decision_id = payload.get("prior_decision_id")
    rationale = payload.get("rationale", "")
    if not decision_id:
        fail("payload.decision_id required (AD-1)")
    conflict = find_conflict(conflict_id) if conflict_id else None
    if not conflict:
        fail(f"conflict_id {conflict_id!r} not found (AD-2)")
    if decision not in ARBITRATION_DECISIONS_ENUM:
        fail(f"decision {decision!r} not in {sorted(ARBITRATION_DECISIONS_ENUM)} (AD-3)")
    if decision == "accept":
        if accepted_ref not in set(conflict.get("conflicting_refs", [])):
            fail("accept requires accepted_ref to be one of conflicting_refs (AD-4)")
    if decision in ("reject", "escalate"):
        if not isinstance(cited, list) or not cited:
            fail(f"{decision} requires non-empty cited_rule_ids (AD-5)")
    if prior_decision_id and not find_arbitration_decision(prior_decision_id):
        fail(f"prior_decision_id {prior_decision_id!r} not found (AD-7)")

    record = {
        "schema": LAYER_SCHEMA,
        "decision_id": decision_id,
        "conflict_id": conflict_id,
        "decision": decision,
        "accepted_ref": accepted_ref if decision == "accept" else None,
        "cited_rule_ids": sorted(cited) if isinstance(cited, list) else [],
        "prior_decision_id": prior_decision_id,
        "rationale": rationale,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(ARBITRATION_DECISIONS / f"{decision_id}-{_now()}.json", record)
    append_event(ES_ARBITRATION, {
        "occurred_at_iso": _iso_now(),
        "kind": "arbitration-decide",
        "decision_id": decision_id,
        "conflict_id": conflict_id,
        "decision": decision,
        "reviewer": reviewer,
    })
    append_audit("arbitration-decide", reviewer, {"decision_id": decision_id, "decision": decision})
    return {"decision_id": decision_id, "decision": decision}


def handle_refresh_cohesion_propagate(reviewer: str, payload: dict) -> dict:
    assert_target_path(payload)
    reject_probabilistic(payload)
    cohesion_id = payload.get("cohesion_id")
    trigger_kind = payload.get("trigger_kind")
    trigger_ref = payload.get("trigger_ref")
    if not cohesion_id:
        fail("payload.cohesion_id required (RC-1)")
    if trigger_kind not in REFRESH_TRIGGER_KINDS:
        fail(f"trigger_kind {trigger_kind!r} not in {sorted(REFRESH_TRIGGER_KINDS)} (RC-2)")

    # Resolve trigger_ref against the appropriate upstream tree (RC-3).
    if trigger_kind == "approved-intake":
        ap = find_intake_approval(trigger_ref)
        if not ap or ap.get("decision") != "approve":
            fail(f"trigger_ref {trigger_ref!r} is not an approved intake (RC-3)")
    elif trigger_kind == "canonical-promotion":
        if not (find_canonical_entity(trigger_ref) or find_canonical_procedure(trigger_ref)):
            fail(f"trigger_ref {trigger_ref!r} is not a canonical entity or procedure (RC-3)")
    elif trigger_kind == "arbitration-resolution":
        if not find_arbitration_decision(trigger_ref):
            fail(f"trigger_ref {trigger_ref!r} is not an arbitration decision (RC-3)")

    refresh_chain = [
        {"step": 1, "system": "evidence-fingerprints", "kind": "fingerprint-refresh-eligibility"},
        {"step": 2, "system": "fusion-clusters", "kind": "cluster-refresh-eligibility"},
        {"step": 3, "system": "canonical-entities", "kind": "canonical-entity-refresh-eligibility"},
        {"step": 4, "system": "canonical-procedures", "kind": "canonical-procedure-refresh-eligibility"},
        {"step": 5, "system": "manual-runtime-closure/manual-synthesis-drafts", "kind": "synthesis-refresh-eligibility"},
        {"step": 6, "system": "manual-runtime-closure/export-finalizations", "kind": "export-invalidation-eligibility"},
    ]
    record = {
        "schema": LAYER_SCHEMA,
        "cohesion_id": cohesion_id,
        "trigger_kind": trigger_kind,
        "trigger_ref": trigger_ref,
        "refresh_chain": refresh_chain,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
        "note": "POINTER-only chain; upstream trees NEVER mutated by Phase 55 (RC-5)",
    }
    write_json(REFRESH_COHESION_RECORDS / f"{cohesion_id}-{_now()}.json", record)
    append_event(ES_REFRESH, {
        "occurred_at_iso": _iso_now(),
        "kind": "refresh-cohesion-propagate",
        "cohesion_id": cohesion_id,
        "trigger_kind": trigger_kind,
        "trigger_ref": trigger_ref,
        "chain_length": len(refresh_chain),
        "reviewer": reviewer,
    })
    append_audit("refresh-cohesion-propagate", reviewer, {"cohesion_id": cohesion_id, "trigger_kind": trigger_kind})
    return {"cohesion_id": cohesion_id, "chain_length": len(refresh_chain)}


def handle_workspace_flow_record(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "WF-1")
    reject_probabilistic(payload)
    flow_event_id = payload.get("flow_event_id")
    stage = payload.get("stage")
    ref_id = payload.get("ref_id")
    notes = payload.get("notes", "")
    if not flow_event_id:
        fail("payload.flow_event_id required (WF-1)")
    if stage not in WORKSPACE_FLOW_STAGES:
        fail(f"stage {stage!r} not in {sorted(WORKSPACE_FLOW_STAGES)} (WF-2)")
    if not ref_id:
        fail("payload.ref_id required (WF-3)")
    record = {
        "schema": LAYER_SCHEMA,
        "flow_event_id": flow_event_id,
        "stage": stage,
        "ref_id": ref_id,
        "notes": notes,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
        "observational_only": True,
    }
    write_json(WORKSPACE_FLOWS / f"{flow_event_id}-{_now()}.json", record)
    append_event(ES_WORKSPACE, {
        "occurred_at_iso": _iso_now(),
        "kind": "workspace-flow-record",
        "flow_event_id": flow_event_id,
        "stage": stage,
        "ref_id": ref_id,
        "reviewer": reviewer,
    })
    append_audit("workspace-flow-record", reviewer, {"flow_event_id": flow_event_id, "stage": stage})
    return {"flow_event_id": flow_event_id, "stage": stage}


def handle_export_stabilize(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "ES-4")
    reject_probabilistic(payload)
    stabilization_id = payload.get("stabilization_id")
    package_id = payload.get("package_id")
    if not stabilization_id:
        fail("payload.stabilization_id required (ES-1)")
    pkg = find_package(package_id) if package_id else None
    if not pkg:
        fail(f"package_id {package_id!r} not found (ES-2)")
    state = package_lifecycle_state(package_id)
    if state != "export-ready":
        fail(f"package {package_id!r} lifecycle state is {state!r}, must be 'export-ready' (ES-2)")

    # Aggregate sections for the manual.
    sections = []
    if SECTIONS_DIR.exists():
        for p in sorted(SECTIONS_DIR.glob("*.json")):
            try:
                d = read_json(p)
            except Exception:
                continue
            if d.get("manual_id") == pkg.get("manual_id"):
                sections.append(d)
    sections.sort(key=lambda s: s.get("section_id") or "")

    # Canonical ID assignment — additive across stabilization cycles.
    prior = find_existing_stabilization(package_id)
    canonical_id_map = dict(prior.get("canonical_id_map", {})) if prior else {}
    next_index = (
        max([int(v.split("-")[-1]) for v in canonical_id_map.values() if v.split("-")[-1].isdigit()] + [0])
        + 1
    )
    for sec in sections:
        sid = sec.get("section_id")
        if sid not in canonical_id_map:
            canonical_id_map[sid] = f"canon-{package_id}-sec-{next_index:04d}"
            next_index += 1

    # Build presentation-neutral stable export payload.
    stable_payload = {
        "package_id": package_id,
        "manual_id": pkg.get("manual_id"),
        "canonical_product_id": pkg.get("canonical_product_id"),
        "package_version": pkg.get("package_version"),
        "canonical_id_map": dict(sorted(canonical_id_map.items())),
        "sections": [
            {
                "canonical_section_id": canonical_id_map[s.get("section_id")],
                "section_id": s.get("section_id"),
                "section_kind": s.get("section_kind"),
                "title": s.get("title"),
                "body_blocks": s.get("body_blocks", []),
                "evidence_refs": sorted(s.get("evidence_refs") or []),
                "grounding_ids": sorted(s.get("grounding_ids") or []),
            }
            for s in sections
        ],
    }
    hit = find_forbidden_key(stable_payload, FORBIDDEN_PRESENTATION_KEYS)
    if hit:
        fail(f"stable_export_payload contains forbidden presentation key '{hit[1]}' at {hit[0]} (ES-4)")

    # Verify additive-only invariant (ES-6) — every prior canonical ID preserved.
    if prior:
        for k, v in prior.get("canonical_id_map", {}).items():
            if canonical_id_map.get(k) != v:
                fail(f"canonical_id_map regression for section {k!r}: prior {v!r} != now {canonical_id_map.get(k)!r} (ES-6)")

    stable_export_sha256 = sha256_text(canonical_json(stable_payload))
    record = {
        "schema": LAYER_SCHEMA,
        "stabilization_id": stabilization_id,
        "package_id": package_id,
        "canonical_id_map": dict(sorted(canonical_id_map.items())),
        "stable_export_payload": stable_payload,
        "stable_export_sha256": stable_export_sha256,
        "section_count": len(sections),
        "supersedes_prior_stabilization_id": prior.get("stabilization_id") if prior else None,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
    }
    write_json(EXPORT_STABILIZATIONS / f"{stabilization_id}-{_now()}.json", record)
    append_event(ES_STABILIZE, {
        "occurred_at_iso": _iso_now(),
        "kind": "export-stabilize",
        "stabilization_id": stabilization_id,
        "package_id": package_id,
        "stable_export_sha256": stable_export_sha256,
        "section_count": len(sections),
        "reviewer": reviewer,
    })
    append_audit("export-stabilize", reviewer, {"stabilization_id": stabilization_id, "package_id": package_id})
    return {"stabilization_id": stabilization_id, "stable_export_sha256": stable_export_sha256, "section_count": len(sections)}


# ============================================================================
# Dispatch table & CLI
# ============================================================================
DISPATCH = {
    "evidence-fingerprint": handle_evidence_fingerprint,
    "fusion-cluster-form": handle_fusion_cluster_form,
    "canonical-entity-promote": handle_canonical_entity_promote,
    "canonical-procedure-converge": handle_canonical_procedure_converge,
    "conflict-surface": handle_conflict_surface,
    "arbitration-decide": handle_arbitration_decide,
    "refresh-cohesion-propagate": handle_refresh_cohesion_propagate,
    "workspace-flow-record": handle_workspace_flow_record,
    "export-stabilize": handle_export_stabilize,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 55 semantic convergence executor")
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
