#!/usr/bin/env python3
"""
Phase 54 executor — unified operational manual runtime closure.

Request envelope: governed-fs-operation-request/1.0
CLI: --kind <dispatch> --request <envelope.json> --confirm

Wires existing layers (Phase 46 FS, Phase 47 transactional runtime,
Phase 49 grounding, Phase 52 extraction, Phase 53 packaging) into the
first end-to-end reviewer-driven manual-generation loop.

This executor:
  - validates envelopes fail-closed,
  - rejects presentation/layout/CSS/typography keys recursively,
  - never mutates upstream extraction/semantic/packaging trees,
  - appends events only into Phase 54's own event stores + audit-events,
  - records deterministic SHA-256 hashes for replayability.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "governed-fs-operation-request/1.0"
LAYER_SCHEMA = "unified-operational-manual-runtime-closure/1.0"
LAYER = 47

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"

# Phase 54 isolated storage tree
MR_ROOT = OC_ROOT / "manual-runtime-closure"
INTAKE_ANALYSES = MR_ROOT / "intake-analyses"
INTAKE_REVISIONS = MR_ROOT / "intake-revisions"
INTAKE_APPROVALS = MR_ROOT / "intake-approvals"
REFRESH_RECORDS = MR_ROOT / "refresh-records"
SEMANTIC_BANK_SNAPSHOTS = MR_ROOT / "semantic-bank-snapshots"
MANUAL_SYNTHESIS_DRAFTS = MR_ROOT / "manual-synthesis-drafts"
VISUAL_SUPPORT_NEEDS = MR_ROOT / "visual-support-needs"
PROMPT_PACKAGES = MR_ROOT / "prompt-packages"
EXPORT_FINALIZATIONS = MR_ROOT / "export-finalizations"
CLOSURE_LINEAGE = MR_ROOT / "closure-lineage"

# Upstream (read-only) trees
PACKAGING_RUNTIME = OC_ROOT / "manual-semantic-packaging-runtime"
PACKAGES_DIR = PACKAGING_RUNTIME / "manual-packages"
SECTIONS_DIR = PACKAGING_RUNTIME / "semantic-sections"
PACKAGING_LIFECYCLE = PACKAGING_RUNTIME / "manual-packaging-lifecycle"
EXTRACTION_RUNTIME = OC_ROOT / "semantic-extraction-runtime"
EXTRACTION_CANDIDATES = EXTRACTION_RUNTIME / "extraction-candidates"

# Event stores
EVENT_STORE_INTAKE_ANALYSIS = RUNTIME_MANIFESTS_ROOT / "intake-analysis-events" / "_event-store.json"
EVENT_STORE_INTAKE_APPROVAL = RUNTIME_MANIFESTS_ROOT / "intake-approval-events" / "_event-store.json"
EVENT_STORE_REFRESH = RUNTIME_MANIFESTS_ROOT / "refresh-propagation-events" / "_event-store.json"
EVENT_STORE_BANK = RUNTIME_MANIFESTS_ROOT / "semantic-bank-events" / "_event-store.json"
EVENT_STORE_SYNTHESIS = RUNTIME_MANIFESTS_ROOT / "manual-synthesis-events" / "_event-store.json"
EVENT_STORE_VS = RUNTIME_MANIFESTS_ROOT / "visual-support-events" / "_event-store.json"
EVENT_STORE_PROMPT = RUNTIME_MANIFESTS_ROOT / "prompt-package-events" / "_event-store.json"
EVENT_STORE_EXPORT = RUNTIME_MANIFESTS_ROOT / "export-finalization-events" / "_event-store.json"
EVENT_STORE_AUDIT = RUNTIME_MANIFESTS_ROOT / "audit-events" / "_event-store.json"

EVIDENCE_KINDS = {"video", "image", "pdf", "xls", "xlsx", "csv", "json", "yaml", "doc", "docx"}
INTAKE_DECISIONS = {"approve", "reject"}
VISUAL_SUPPORT_CONFIDENCE = {"low", "medium", "high"}
VISUAL_SUPPORT_SEVERITY = {"informational", "recommended", "required", "blocking"}

# Forbidden write prefixes — Phase 54 must NEVER mutate upstream trees.
FORBIDDEN_OVERWRITE_PREFIXES = (
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

# Presentation-bearing keys forbidden in any payload (consumer-boundary).
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

# Visual-support keyword heuristics (deterministic, not probabilistic).
VS_KEYWORDS_REQUIRED = {
    "install", "wire", "wiring", "pair", "pairing", "enroll", "enrollment",
    "replace", "replacement", "battery", "fingerprint",
}
VS_KEYWORDS_RECOMMENDED = {
    "navigate", "open app", "menu", "settings", "screen", "tap", "press",
    "swipe", "scroll", "select", "icon", "indicator",
}
VS_KEYWORDS_INFORMATIONAL = {
    "see", "appears", "displays", "shows", "visible",
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


def find_presentation_key(obj: Any, path: str = "$") -> tuple[str, str] | None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.lower() in FORBIDDEN_PRESENTATION_KEYS:
                return (path + "." + k, k.lower())
            sub = find_presentation_key(v, path + "." + (k if isinstance(k, str) else "?"))
            if sub:
                return sub
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            sub = find_presentation_key(v, path + "[" + str(i) + "]")
            if sub:
                return sub
    return None


def reject_presentation(payload: dict, rule_id: str) -> None:
    hit = find_presentation_key(payload)
    if hit:
        fail(f"presentation key '{hit[1]}' at {hit[0]} forbidden ({rule_id})")


def assert_target_path(payload: dict) -> None:
    tp = payload.get("target_path")
    if isinstance(tp, str) and tp:
        norm = tp.replace("\\", "/")
        for prefix in FORBIDDEN_OVERWRITE_PREFIXES:
            if prefix in norm:
                fail(f"target_path falls under a forbidden prefix '{prefix}' (RR-3)")


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
    aid = f"a54-{kind}-{_now()}"
    event = {
        "audit_event_id": aid,
        "occurred_at_iso": _iso_now(),
        "kind": kind,
        "reviewer": reviewer,
        "layer": LAYER,
        "schema": LAYER_SCHEMA,
        "append_only": True,
        "payload": payload,
    }
    append_event(EVENT_STORE_AUDIT, event)


# ----------------------------------------------------------------------------
# Lookups across Phase 54 trees
# ----------------------------------------------------------------------------
def _scan_dir_for_id(d: Path, id_field: str, target_id: str) -> dict | None:
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


def find_analysis(analysis_id: str) -> dict | None:
    found = _scan_dir_for_id(INTAKE_ANALYSES, "analysis_id", analysis_id)
    if found:
        return found
    return _scan_dir_for_id(INTAKE_REVISIONS, "revision_id", analysis_id)


def find_approval(approval_id: str) -> dict | None:
    return _scan_dir_for_id(INTAKE_APPROVALS, "approval_id", approval_id)


def find_snapshot(snapshot_id: str) -> dict | None:
    return _scan_dir_for_id(SEMANTIC_BANK_SNAPSHOTS, "snapshot_id", snapshot_id)


def find_synthesis(synthesis_id: str) -> dict | None:
    return _scan_dir_for_id(MANUAL_SYNTHESIS_DRAFTS, "synthesis_id", synthesis_id)


def find_support_need(support_need_id: str) -> dict | None:
    if not VISUAL_SUPPORT_NEEDS.exists():
        return None
    for p in sorted(VISUAL_SUPPORT_NEEDS.glob("*.json")):
        try:
            data = read_json(p)
        except Exception:
            continue
        for need in data.get("needs", []):
            if need.get("support_need_id") == support_need_id:
                return {"detection": data, "need": need}
    return None


def find_package(package_id: str) -> dict | None:
    return _scan_dir_for_id(PACKAGES_DIR, "package_id", package_id)


def find_sections_for_manual(manual_id: str) -> list[dict]:
    out: list[dict] = []
    if not SECTIONS_DIR.exists():
        return out
    for p in sorted(SECTIONS_DIR.glob("*.json")):
        try:
            data = read_json(p)
        except Exception:
            continue
        if data.get("manual_id") == manual_id:
            out.append(data)
    return sorted(out, key=lambda d: d.get("section_id", ""))


def package_lifecycle_state(package_id: str) -> str | None:
    """Read latest lifecycle state for a Phase 53 package from packaging-lifecycle-events."""
    store = RUNTIME_MANIFESTS_ROOT / "packaging-lifecycle-events" / "_event-store.json"
    if not store.exists():
        return None
    try:
        events = read_json(store).get("events", [])
    except Exception:
        return None
    last = None
    for e in events:
        # Phase 53 lifecycle events store package_id/to_state at top-level.
        pid = e.get("package_id") or e.get("payload", {}).get("package_id")
        to_state = e.get("to_state") or e.get("payload", {}).get("to_state")
        if pid == package_id and to_state:
            last = to_state
    return last


# ============================================================================
# Dispatch handlers
# ============================================================================
def handle_intake_analyze(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "IA-8")
    analysis_id = payload.get("analysis_id")
    evidence_id = payload.get("evidence_id")
    evidence_kind = payload.get("evidence_kind")
    inferred_product_id = payload.get("inferred_product_id")
    inferred_semantic_domains = payload.get("inferred_semantic_domains")
    inferred_downstream_impacts = payload.get("inferred_downstream_impacts")
    evidence_refs = payload.get("evidence_refs")
    if not analysis_id:
        fail("payload.analysis_id required (IA-1)")
    if not evidence_id:
        fail("payload.evidence_id required (IA-1)")
    if evidence_kind not in EVIDENCE_KINDS:
        fail(f"evidence_kind {evidence_kind!r} not in {sorted(EVIDENCE_KINDS)} (IA-2)")
    if not inferred_product_id:
        fail("payload.inferred_product_id required (IA-3)")
    if not isinstance(inferred_semantic_domains, list):
        fail("payload.inferred_semantic_domains must be a list (IA-4)")
    if not isinstance(inferred_downstream_impacts, list):
        fail("payload.inferred_downstream_impacts must be a list (IA-5)")
    if not isinstance(evidence_refs, list) or not evidence_refs:
        fail("payload.evidence_refs must be a non-empty list (IA-1)")
    if payload.get("state") not in (None, "pending-review"):
        fail("intake-analyze cannot directly assert non-pending state (IA-7)")

    canonical_payload = {
        "analysis_id": analysis_id,
        "evidence_id": evidence_id,
        "evidence_kind": evidence_kind,
        "inferred_product_id": inferred_product_id,
        "inferred_semantic_domains": sorted(inferred_semantic_domains),
        "inferred_downstream_impacts": sorted(inferred_downstream_impacts),
        "evidence_refs": sorted(evidence_refs),
        "reviewer_notes": payload.get("reviewer_notes", ""),
    }
    analysis_sha256 = sha256_text(canonical_json(canonical_payload))
    record = {
        "schema": LAYER_SCHEMA,
        "analysis_id": analysis_id,
        "state": "pending-review",
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
        "analysis_sha256": analysis_sha256,
        **canonical_payload,
    }
    out_path = INTAKE_ANALYSES / f"{analysis_id}-{_now()}.json"
    write_json(out_path, record)
    event = {
        "occurred_at_iso": _iso_now(),
        "kind": "intake-analyze",
        "analysis_id": analysis_id,
        "evidence_id": evidence_id,
        "evidence_kind": evidence_kind,
        "reviewer": reviewer,
        "analysis_sha256": analysis_sha256,
    }
    append_event(EVENT_STORE_INTAKE_ANALYSIS, event)
    append_audit("intake-analyze", reviewer, {"analysis_id": analysis_id, "evidence_id": evidence_id})
    return {"analysis_id": analysis_id, "state": "pending-review", "analysis_sha256": analysis_sha256}


def handle_intake_reanalyze(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "IA-8")
    revision_id = payload.get("revision_id")
    prior_analysis_id = payload.get("prior_analysis_id")
    rationale = payload.get("reviewer_rationale")
    if not revision_id:
        fail("payload.revision_id required (IR-1)")
    if not prior_analysis_id:
        fail("payload.prior_analysis_id required (IR-2)")
    prior = find_analysis(prior_analysis_id)
    if not prior:
        fail(f"prior_analysis_id {prior_analysis_id!r} not found (IR-2)")
    if not rationale:
        fail("payload.reviewer_rationale required (IR-5)")

    # Determine revision_number deterministically.
    existing = 0
    if INTAKE_REVISIONS.exists():
        for p in INTAKE_REVISIONS.glob("*.json"):
            try:
                d = read_json(p)
            except Exception:
                continue
            if d.get("prior_analysis_id") == prior_analysis_id:
                existing += 1
    revision_number = existing + 1

    adjusted = payload.get("adjusted_assumptions", {})
    if not isinstance(adjusted, dict):
        fail("payload.adjusted_assumptions must be a dict if provided")
    canonical_payload = {
        "revision_id": revision_id,
        "prior_analysis_id": prior_analysis_id,
        "revision_number": revision_number,
        "reviewer_rationale": rationale,
        "adjusted_assumptions": dict(sorted(adjusted.items())),
        "evidence_id": prior.get("evidence_id"),
        "evidence_kind": prior.get("evidence_kind"),
    }
    analysis_sha256 = sha256_text(canonical_json(canonical_payload))
    record = {
        "schema": LAYER_SCHEMA,
        "state": "pending-review",
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
        "analysis_sha256": analysis_sha256,
        **canonical_payload,
    }
    out_path = INTAKE_REVISIONS / f"{revision_id}-{_now()}.json"
    write_json(out_path, record)
    append_event(
        EVENT_STORE_INTAKE_ANALYSIS,
        {
            "occurred_at_iso": _iso_now(),
            "kind": "intake-revision",
            "revision_id": revision_id,
            "prior_analysis_id": prior_analysis_id,
            "revision_number": revision_number,
            "reviewer": reviewer,
            "analysis_sha256": analysis_sha256,
        },
    )
    append_audit("intake-reanalyze", reviewer, {"revision_id": revision_id, "prior_analysis_id": prior_analysis_id})
    return {"revision_id": revision_id, "revision_number": revision_number, "state": "pending-review"}


def handle_intake_approve(reviewer: str, payload: dict) -> dict:
    approval_id = payload.get("approval_id")
    analysis_id = payload.get("analysis_id")
    decision = payload.get("decision")
    cited = payload.get("cited_rule_ids")
    if not approval_id:
        fail("payload.approval_id required (IAP-1)")
    if not analysis_id:
        fail("payload.analysis_id required (IAP-2)")
    if not find_analysis(analysis_id):
        fail(f"analysis_id {analysis_id!r} not found (IAP-2)")
    if decision not in INTAKE_DECISIONS:
        fail(f"decision {decision!r} not in {sorted(INTAKE_DECISIONS)} (IAP-3)")
    if decision == "reject":
        if not isinstance(cited, list) or not cited:
            fail("reject requires non-empty cited_rule_ids (IAP-4)")
    record = {
        "schema": LAYER_SCHEMA,
        "approval_id": approval_id,
        "analysis_id": analysis_id,
        "decision": decision,
        "cited_rule_ids": sorted(cited) if isinstance(cited, list) else [],
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
        "refresh_eligible": decision == "approve",
    }
    out_path = INTAKE_APPROVALS / f"{approval_id}-{_now()}.json"
    write_json(out_path, record)
    append_event(
        EVENT_STORE_INTAKE_APPROVAL,
        {
            "occurred_at_iso": _iso_now(),
            "kind": "intake-approve",
            "approval_id": approval_id,
            "analysis_id": analysis_id,
            "decision": decision,
            "reviewer": reviewer,
        },
    )
    append_audit("intake-approve", reviewer, {"approval_id": approval_id, "decision": decision})
    return {"approval_id": approval_id, "decision": decision, "refresh_eligible": decision == "approve"}


def handle_refresh_propagate(reviewer: str, payload: dict) -> dict:
    assert_target_path(payload)
    refresh_id = payload.get("refresh_id")
    approval_id = payload.get("approval_id")
    if not refresh_id:
        fail("payload.refresh_id required (RR-1)")
    if not approval_id:
        fail("payload.approval_id required (RR-2)")
    approval = find_approval(approval_id)
    if not approval:
        fail(f"approval_id {approval_id!r} not found (RR-2)")
    if approval.get("decision") != "approve":
        fail(f"approval {approval_id!r} is not in 'approve' state (RR-2)")
    analysis = find_analysis(approval["analysis_id"])
    if not analysis:
        fail("approval references missing analysis (RR-2)")

    # Refresh is a POINTER record — never mutates upstream trees.
    refresh_targets = [
        {"system": "semantic-extraction-runtime", "kind": "extraction-refresh", "scope": analysis.get("evidence_id")},
        {"system": "manual-semantic-packaging-runtime", "kind": "packaging-refresh-eligibility", "scope": analysis.get("inferred_product_id")},
    ]
    record = {
        "schema": LAYER_SCHEMA,
        "refresh_id": refresh_id,
        "approval_id": approval_id,
        "analysis_id": approval["analysis_id"],
        "evidence_id": analysis.get("evidence_id"),
        "inferred_product_id": analysis.get("inferred_product_id"),
        "refresh_targets": refresh_targets,
        "reviewer": reviewer,
        "occurred_at_iso": _iso_now(),
        "note": "pointer record only; upstream trees are NEVER mutated by Phase 54 (RR-3)",
    }
    out_path = REFRESH_RECORDS / f"{refresh_id}-{_now()}.json"
    write_json(out_path, record)
    append_event(
        EVENT_STORE_REFRESH,
        {
            "occurred_at_iso": _iso_now(),
            "kind": "refresh-propagate",
            "refresh_id": refresh_id,
            "approval_id": approval_id,
            "reviewer": reviewer,
        },
    )
    append_audit("refresh-propagate", reviewer, {"refresh_id": refresh_id, "approval_id": approval_id})
    return {"refresh_id": refresh_id, "refresh_targets": refresh_targets}


def handle_semantic_bank_snapshot(reviewer: str, payload: dict) -> dict:
    snapshot_id = payload.get("snapshot_id")
    if not snapshot_id:
        fail("payload.snapshot_id required (SB-1)")
    scope_manual_id = payload.get("scope_manual_id")
    scope_product_id = payload.get("scope_product_id")

    # Aggregate semantic sections (Phase 53)
    sections: list[dict] = []
    if SECTIONS_DIR.exists():
        for p in sorted(SECTIONS_DIR.glob("*.json")):
            try:
                d = read_json(p)
            except Exception:
                continue
            if scope_manual_id and d.get("manual_id") != scope_manual_id:
                continue
            sections.append(
                {
                    "section_id": d.get("section_id"),
                    "manual_id": d.get("manual_id"),
                    "section_kind": d.get("section_kind"),
                    "title": d.get("title"),
                    "extraction_ids": sorted(d.get("extraction_ids") or []),
                    "grounding_ids": sorted(d.get("grounding_ids") or []),
                    "evidence_refs": sorted(d.get("evidence_refs") or []),
                    "body_blocks": d.get("body_blocks", []),
                }
            )
    sections.sort(key=lambda s: s.get("section_id") or "")

    # Aggregate extraction candidates (Phase 52) if present
    candidates: list[dict] = []
    if EXTRACTION_CANDIDATES.exists():
        for p in sorted(EXTRACTION_CANDIDATES.glob("*.json")):
            try:
                d = read_json(p)
            except Exception:
                continue
            if scope_product_id and d.get("product_id") and d["product_id"] != scope_product_id:
                continue
            candidates.append(
                {
                    "candidate_id": d.get("candidate_id"),
                    "candidate_kind": d.get("candidate_kind"),
                    "evidence_id": d.get("evidence_id"),
                    "reviewer_state": d.get("reviewer_state") or d.get("state"),
                }
            )
    candidates.sort(key=lambda c: c.get("candidate_id") or "")

    aggregation = {
        "snapshot_id": snapshot_id,
        "scope_manual_id": scope_manual_id,
        "scope_product_id": scope_product_id,
        "sections": sections,
        "candidates": candidates,
    }
    snapshot_sha256 = sha256_text(canonical_json(aggregation))
    record = {
        "schema": LAYER_SCHEMA,
        "occurred_at_iso": _iso_now(),
        "reviewer": reviewer,
        "snapshot_sha256": snapshot_sha256,
        "section_count": len(sections),
        "candidate_count": len(candidates),
        **aggregation,
    }
    out_path = SEMANTIC_BANK_SNAPSHOTS / f"{snapshot_id}-{_now()}.json"
    write_json(out_path, record)
    append_event(
        EVENT_STORE_BANK,
        {
            "occurred_at_iso": _iso_now(),
            "kind": "semantic-bank-snapshot",
            "snapshot_id": snapshot_id,
            "snapshot_sha256": snapshot_sha256,
            "section_count": len(sections),
            "candidate_count": len(candidates),
            "reviewer": reviewer,
        },
    )
    append_audit("semantic-bank-snapshot", reviewer, {"snapshot_id": snapshot_id})
    return {
        "snapshot_id": snapshot_id,
        "snapshot_sha256": snapshot_sha256,
        "section_count": len(sections),
        "candidate_count": len(candidates),
    }


def handle_manual_synthesize(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "MS-7")
    synthesis_id = payload.get("synthesis_id")
    snapshot_id = payload.get("snapshot_id")
    target_manual_id = payload.get("target_manual_id")
    target_product_id = payload.get("target_product_id")
    if not synthesis_id:
        fail("payload.synthesis_id required (MS-1)")
    snap = find_snapshot(snapshot_id) if snapshot_id else None
    if not snap:
        fail(f"snapshot_id {snapshot_id!r} not found (MS-2)")
    if not target_manual_id or not target_product_id:
        fail("payload.target_manual_id and target_product_id required (MS-3)")

    # Aggregate sections by canonical kind. Each procedural step must reference
    # at least one evidence_id or grounding_id (MS-5).
    by_kind: dict[str, list[dict]] = {}
    for sec in snap.get("sections", []):
        kind = sec.get("section_kind") or "semantic-section"
        by_kind.setdefault(kind, []).append(sec)
    procedural_steps: list[dict] = []
    procs = by_kind.get("semantic-procedure", [])
    for sec in procs:
        for blk in sec.get("body_blocks", []) or []:
            si = blk.get("step_index")
            text = blk.get("text", "")
            ev = sec.get("evidence_refs") or []
            grnd = sec.get("grounding_ids") or []
            if not ev and not grnd:
                fail(f"procedural step in section {sec.get('section_id')!r} lacks evidence/grounding (MS-5)")
            procedural_steps.append({
                "section_id": sec.get("section_id"),
                "step_index": si,
                "text": text,
                "evidence_refs": sorted(ev),
                "grounding_ids": sorted(grnd),
            })

    # Sort kinds and steps deterministically.
    kinds_sorted = {k: sorted(v, key=lambda s: s.get("section_id") or "") for k, v in sorted(by_kind.items())}
    procedural_steps.sort(key=lambda s: (s.get("section_id") or "", s.get("step_index") or 0))

    canonical = {
        "synthesis_id": synthesis_id,
        "snapshot_id": snapshot_id,
        "target_manual_id": target_manual_id,
        "target_product_id": target_product_id,
        "sections_by_kind": kinds_sorted,
        "procedural_steps": procedural_steps,
    }
    synthesis_sha256 = sha256_text(canonical_json(canonical))
    record = {
        "schema": LAYER_SCHEMA,
        "occurred_at_iso": _iso_now(),
        "reviewer": reviewer,
        "state": "synthesized",
        "synthesis_sha256": synthesis_sha256,
        "step_count": len(procedural_steps),
        **canonical,
    }
    out_path = MANUAL_SYNTHESIS_DRAFTS / f"{synthesis_id}-{_now()}.json"
    write_json(out_path, record)
    append_event(
        EVENT_STORE_SYNTHESIS,
        {
            "occurred_at_iso": _iso_now(),
            "kind": "manual-synthesize",
            "synthesis_id": synthesis_id,
            "snapshot_id": snapshot_id,
            "step_count": len(procedural_steps),
            "synthesis_sha256": synthesis_sha256,
            "reviewer": reviewer,
        },
    )
    append_audit("manual-synthesize", reviewer, {"synthesis_id": synthesis_id, "snapshot_id": snapshot_id})
    return {"synthesis_id": synthesis_id, "synthesis_sha256": synthesis_sha256, "step_count": len(procedural_steps)}


def _classify_visual_support(text: str) -> tuple[str, str, str] | None:
    low = text.lower()
    matched_required = [k for k in VS_KEYWORDS_REQUIRED if k in low]
    matched_recommended = [k for k in VS_KEYWORDS_RECOMMENDED if k in low]
    matched_info = [k for k in VS_KEYWORDS_INFORMATIONAL if k in low]
    if matched_required:
        return ("high", "required", f"matched required-action keywords: {sorted(matched_required)}")
    if matched_recommended:
        return ("medium", "recommended", f"matched UI-navigation keywords: {sorted(matched_recommended)}")
    if matched_info:
        return ("low", "informational", f"matched informational keywords: {sorted(matched_info)}")
    return None


def handle_visual_support_detect(reviewer: str, payload: dict) -> dict:
    detection_id = payload.get("detection_id")
    synthesis_id = payload.get("synthesis_id")
    if not detection_id:
        fail("payload.detection_id required (VS-1)")
    syn = find_synthesis(synthesis_id) if synthesis_id else None
    if not syn:
        fail(f"synthesis_id {synthesis_id!r} not found (VS-2)")

    needs: list[dict] = []
    for step in syn.get("procedural_steps", []):
        cls = _classify_visual_support(step.get("text", ""))
        if not cls:
            continue
        confidence, severity, rationale = cls
        if confidence not in VISUAL_SUPPORT_CONFIDENCE:
            fail(f"confidence {confidence!r} invalid (VS-3)")
        if severity not in VISUAL_SUPPORT_SEVERITY:
            fail(f"severity {severity!r} invalid (VS-4)")
        support_need_id = f"{detection_id}-{step.get('section_id')}-step-{step.get('step_index')}"
        needs.append({
            "support_need_id": support_need_id,
            "section_id": step.get("section_id"),
            "step_index": step.get("step_index"),
            "confidence": confidence,
            "severity": severity,
            "rationale": rationale,
            "affected_step_refs": [{"section_id": step.get("section_id"), "step_index": step.get("step_index")}],
            "evidence_refs": step.get("evidence_refs", []),
            "grounding_ids": step.get("grounding_ids", []),
        })
    needs.sort(key=lambda n: n["support_need_id"])
    record = {
        "schema": LAYER_SCHEMA,
        "occurred_at_iso": _iso_now(),
        "reviewer": reviewer,
        "detection_id": detection_id,
        "synthesis_id": synthesis_id,
        "needs": needs,
        "needs_count": len(needs),
        "note": "Phase 54 DETECTS visual-support needs only; it MUST NOT generate images (VS-6)",
    }
    out_path = VISUAL_SUPPORT_NEEDS / f"{detection_id}-{_now()}.json"
    write_json(out_path, record)
    append_event(
        EVENT_STORE_VS,
        {
            "occurred_at_iso": _iso_now(),
            "kind": "visual-support-detect",
            "detection_id": detection_id,
            "synthesis_id": synthesis_id,
            "needs_count": len(needs),
            "reviewer": reviewer,
        },
    )
    append_audit("visual-support-detect", reviewer, {"detection_id": detection_id, "needs_count": len(needs)})
    return {"detection_id": detection_id, "needs_count": len(needs)}


def handle_prompt_package_generate(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "PP-7")
    package_id = payload.get("package_id")
    support_need_id = payload.get("support_need_id")
    visual_role = payload.get("visual_role")
    if not package_id:
        fail("payload.package_id required (PP-1)")
    found = find_support_need(support_need_id) if support_need_id else None
    if not found:
        fail(f"support_need_id {support_need_id!r} not found (PP-2)")
    if not visual_role:
        fail("payload.visual_role required (PP-5)")
    need = found["need"]
    detection = found["detection"]

    # Deterministic prompt assembly.
    framing = payload.get("required_framing", "neutral product-focused framing")
    context = payload.get("required_context", "")
    continuity_refs = sorted(payload.get("continuity_refs", []) or [])
    prohibited = sorted(payload.get("prohibited_inaccuracies", []) or [])
    if not isinstance(prohibited, list):
        fail("payload.prohibited_inaccuracies must be a list (PP-6)")
    reviewer_notes = payload.get("reviewer_notes", "")

    base_prompt = (
        f"visual_role={visual_role}; severity={need.get('severity')}; "
        f"section_id={need.get('section_id')}; step_index={need.get('step_index')}; "
        f"rationale={need.get('rationale')}"
    )
    canonical = {
        "package_id": package_id,
        "support_need_id": support_need_id,
        "detection_id": detection.get("detection_id"),
        "synthesis_id": detection.get("synthesis_id"),
        "visual_role": visual_role,
        "prompt_text": base_prompt,
        "required_framing": framing,
        "required_context": context,
        "continuity_refs": continuity_refs,
        "grounding_refs": sorted(need.get("grounding_ids", [])),
        "evidence_refs": sorted(need.get("evidence_refs", [])),
        "prohibited_inaccuracies": prohibited,
        "reviewer_notes": reviewer_notes,
    }
    package_sha256 = sha256_text(canonical_json(canonical))
    record = {
        "schema": LAYER_SCHEMA,
        "occurred_at_iso": _iso_now(),
        "reviewer": reviewer,
        "package_sha256": package_sha256,
        **canonical,
    }
    out_path = PROMPT_PACKAGES / f"{package_id}-{_now()}.json"
    write_json(out_path, record)
    append_event(
        EVENT_STORE_PROMPT,
        {
            "occurred_at_iso": _iso_now(),
            "kind": "prompt-package-generate",
            "package_id": package_id,
            "support_need_id": support_need_id,
            "package_sha256": package_sha256,
            "reviewer": reviewer,
        },
    )
    append_audit("prompt-package-generate", reviewer, {"package_id": package_id, "support_need_id": support_need_id})
    return {"package_id": package_id, "package_sha256": package_sha256}


def handle_export_finalize(reviewer: str, payload: dict) -> dict:
    reject_presentation(payload, "EF-4")
    finalization_id = payload.get("finalization_id")
    pkg_id = payload.get("package_id")
    if not finalization_id:
        fail("payload.finalization_id required (EF-1)")
    pkg = find_package(pkg_id) if pkg_id else None
    if not pkg:
        fail(f"package_id {pkg_id!r} not found (EF-2)")
    state = package_lifecycle_state(pkg_id)
    if state != "export-ready":
        fail(f"package {pkg_id!r} lifecycle state is {state!r}, must be 'export-ready' (EF-2)")

    sections = find_sections_for_manual(pkg.get("manual_id"))
    consumer_payload = {
        "package_id": pkg_id,
        "manual_id": pkg.get("manual_id"),
        "canonical_product_id": pkg.get("canonical_product_id"),
        "package_version": pkg.get("package_version"),
        "semantic_structure": pkg.get("semantic_structure", []),
        "sections": [
            {
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
    # Defensive: re-scan consumer_payload for forbidden presentation keys.
    hit = find_presentation_key(consumer_payload)
    if hit:
        fail(f"consumer_payload contains forbidden presentation key '{hit[1]}' at {hit[0]} (EF-4)")
    consumer_payload_sha256 = sha256_text(canonical_json(consumer_payload))
    record = {
        "schema": LAYER_SCHEMA,
        "occurred_at_iso": _iso_now(),
        "reviewer": reviewer,
        "finalization_id": finalization_id,
        "package_id": pkg_id,
        "consumer_payload": consumer_payload,
        "consumer_payload_sha256": consumer_payload_sha256,
        "section_count": len(sections),
    }
    out_path = EXPORT_FINALIZATIONS / f"{finalization_id}-{_now()}.json"
    write_json(out_path, record)
    append_event(
        EVENT_STORE_EXPORT,
        {
            "occurred_at_iso": _iso_now(),
            "kind": "export-finalize",
            "finalization_id": finalization_id,
            "package_id": pkg_id,
            "consumer_payload_sha256": consumer_payload_sha256,
            "section_count": len(sections),
            "reviewer": reviewer,
        },
    )
    append_audit("export-finalize", reviewer, {"finalization_id": finalization_id, "package_id": pkg_id})
    # Closure-lineage record (the operational loop is now complete for this package).
    write_json(
        CLOSURE_LINEAGE / f"{finalization_id}-{_now()}.json",
        {
            "schema": LAYER_SCHEMA,
            "finalization_id": finalization_id,
            "package_id": pkg_id,
            "consumer_payload_sha256": consumer_payload_sha256,
            "occurred_at_iso": _iso_now(),
            "reviewer": reviewer,
            "loop_closed": True,
        },
    )
    return {"finalization_id": finalization_id, "consumer_payload_sha256": consumer_payload_sha256}


# ============================================================================
# Dispatch table & CLI
# ============================================================================
DISPATCH = {
    "intake-analyze": handle_intake_analyze,
    "intake-reanalyze": handle_intake_reanalyze,
    "intake-approve": handle_intake_approve,
    "refresh-propagate": handle_refresh_propagate,
    "semantic-bank-snapshot": handle_semantic_bank_snapshot,
    "manual-synthesize": handle_manual_synthesize,
    "visual-support-detect": handle_visual_support_detect,
    "prompt-package-generate": handle_prompt_package_generate,
    "export-finalize": handle_export_finalize,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 54 unified operational manual runtime closure executor")
    parser.add_argument("--kind", required=True, choices=sorted(DISPATCH.keys()))
    parser.add_argument("--request", required=True, help="Path to JSON request envelope")
    parser.add_argument("--confirm", action="store_true", help="Required to actually execute")
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

    schema = envelope.get("schema")
    if schema != SCHEMA:
        fail(f"request schema must be '{SCHEMA}' (got {schema!r})")
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
