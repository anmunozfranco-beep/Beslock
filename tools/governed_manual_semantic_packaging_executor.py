"""
Phase 53 — Governed Manual Semantic Packaging CLI executor (layer 46).

Reviewer-invoked. Foreground. Deterministic. Append-only. Fail-closed. Stdlib only.
NO daemon. NO watcher. NO scheduler. NO LLM. NO ML. NO probabilistic packaging.
NO embeddings. NO vector DB. NO autonomous semantic restructuring. NO cloud / SaaS.
NO CSS / NO breakpoints / NO layouts / NO typography / NO responsive logic /
NO UI frameworks / NO frontend rendering — packaging is presentation-neutral.

Records reviewer-authored manual packages, semantic sections, export contracts,
export renders, continuity scans, packaging lineage, packaging replays,
lifecycle transitions, integrity scans, and reviewer overrides. NEVER writes
the live publication tree, the layer-45 semantic-extraction-runtime tree, the
layer-44 publication-composition-runtime tree, the layer-43 visual-generation-
runtime tree, the layer-42 visual-publication-builds tree, frontend/theme
systems, OEM source assets, knowledge-core, governance, runtime-implementation,
runtime-manifests payloads, or uploads.
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
MP_ROOT = OC_ROOT / "manual-semantic-packaging-runtime"

PACKAGES_DIR = MP_ROOT / "manual-packages"
SECTIONS_DIR = MP_ROOT / "semantic-sections"
PROCEDURES_DIR = MP_ROOT / "semantic-procedures"
WARNINGS_DIR = MP_ROOT / "semantic-warnings"
SPECIFICATIONS_DIR = MP_ROOT / "semantic-specifications"
TROUBLESHOOTING_DIR = MP_ROOT / "semantic-troubleshooting"
SUPPORT_DIR = MP_ROOT / "semantic-support"
CONTRACTS_DIR = MP_ROOT / "export-contracts"
RAW_HTML_DIR = MP_ROOT / "raw-html-exports"
JSON_EXPORT_DIR = MP_ROOT / "structured-json-exports"
MARKDOWN_EXPORT_DIR = MP_ROOT / "semantic-markdown-exports"
LINEAGE_DIR = MP_ROOT / "packaging-lineage"
REPLAYS_DIR = MP_ROOT / "packaging-replays"
INTEGRITY_DIR = MP_ROOT / "packaging-integrity"
LIFECYCLE_DIR = MP_ROOT / "manual-packaging-lifecycle"
DECISIONS_DIR = MP_ROOT / "reviewer-packaging-decisions"
CONTINUITY_DIR = MP_ROOT / "packaging-integrity"  # continuity scans co-located under integrity tree

LAYER = 46
SCHEMA = "governed-fs-operation-request/1.0"

SECTION_KINDS = frozenset({
    "semantic-section", "semantic-procedure", "semantic-warning-group",
    "semantic-specification-group", "semantic-troubleshooting-group", "semantic-support-group",
})
EXPORT_KINDS = frozenset({"raw-html-export", "structured-json-export", "semantic-markdown-export"})
CONTINUITY_STATUSES = frozenset({"ok", "gaps-detected", "unresolved"})

LIFECYCLE_STATES = frozenset({
    "draft", "review-required", "reviewer-approved", "export-ready", "superseded", "deprecated",
})
LIFECYCLE_TERMINAL = frozenset({"deprecated"})
LIFECYCLE_EDGES = frozenset({
    ("draft", "review-required"), ("draft", "deprecated"),
    ("review-required", "reviewer-approved"), ("review-required", "draft"), ("review-required", "deprecated"),
    ("reviewer-approved", "export-ready"), ("reviewer-approved", "review-required"), ("reviewer-approved", "superseded"),
    ("export-ready", "reviewer-approved"), ("export-ready", "superseded"),
    ("superseded", "deprecated"),
})

OVERRIDE_KINDS = frozenset({"approve", "reject", "supersede", "annotate"})
OVERRIDE_TARGET_KINDS = frozenset({"package", "section", "contract", "export"})

# Forbidden destinations: every prior-layer storage tree, governance, frontend/theme, OEM uploads.
FORBIDDEN_OVERWRITE_PREFIXES = (
    "wp-content/themes/beslock-custom/User manuals/operational-console/semantic-extraction-runtime/",
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

# Presentation-bearing keys that are FORBIDDEN inside semantic payloads (MP-8/SS-6/XC-3).
FORBIDDEN_PRESENTATION_KEYS = frozenset({
    "css", "class", "classname", "style", "styles", "inline_style",
    "breakpoint", "breakpoints", "screen_size", "screen_width", "viewport",
    "layout", "grid", "flex", "column_count", "column_width",
    "typography", "font", "font_size", "font_family", "font_weight",
    "color", "background", "background_color", "padding", "margin",
    "responsive", "responsive_rules", "media_query", "media_queries",
    "rendering_hint", "render_hint", "ui_framework", "theme",
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def canonical_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


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


def find_presentation_key(obj, path: str = "") -> str | None:
    """Recursively search obj for any FORBIDDEN_PRESENTATION_KEYS. Returns dotted path or None."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.lower() in FORBIDDEN_PRESENTATION_KEYS:
                return f"{path}.{k}" if path else k
            found = find_presentation_key(v, f"{path}.{k}" if path else k)
            if found:
                return found
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found = find_presentation_key(v, f"{path}[{i}]")
            if found:
                return found
    return None


# ---------------------------------------------------------------------------
# Scanners
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


def find_package(package_id: str) -> dict | None:
    return _scan_by_id(PACKAGES_DIR, "package_id", package_id)


def find_section(section_id: str) -> dict | None:
    return _scan_by_id(SECTIONS_DIR, "section_id", section_id)


def find_sections_for_manual(manual_id: str) -> list[dict]:
    out = []
    if not SECTIONS_DIR.exists():
        return out
    seen_ids = set()
    for p in sorted(SECTIONS_DIR.glob("*.json")):
        try:
            d = load_json(p)
        except Exception:
            continue
        if d.get("manual_id") != manual_id:
            continue
        sid = d.get("section_id")
        if sid in seen_ids:
            continue  # latest wins; deduplicate by id (not duplicate registration)
        seen_ids.add(sid)
        out.append(d)
    return out


def find_contract(contract_id: str) -> dict | None:
    return _scan_by_id(CONTRACTS_DIR, "contract_id", contract_id)


def current_package_state(package_id: str) -> str | None:
    store_path = RUNTIME_MANIFESTS_ROOT / "packaging-lifecycle-events" / "_event-store.json"
    last = None
    if store_path.exists():
        for e in load_json(store_path).get("events", []):
            if e.get("package_id") != package_id:
                continue
            if e.get("kind") == "lifecycle-transition":
                last = e.get("to_state")
            elif e.get("kind") == "register" and last is None:
                last = e.get("to_state") or "draft"
    return last


def has_successful_replay(package_id: str) -> bool:
    store_path = RUNTIME_MANIFESTS_ROOT / "packaging-replay-events" / "_event-store.json"
    if not store_path.exists():
        return False
    for e in load_json(store_path).get("events", []):
        if e.get("package_id") == package_id and e.get("replay_ok") is True:
            return True
    return False


def has_blocking_integrity_finding(package_id: str) -> bool:
    store_path = RUNTIME_MANIFESTS_ROOT / "packaging-integrity-events" / "_event-store.json"
    if not store_path.exists():
        return False
    blocking = False
    cleared = False
    for e in load_json(store_path).get("events", []):
        if e.get("package_id") != package_id:
            continue
        if e.get("blocking"):
            blocking = True
            cleared = False
        else:
            cleared = True
            blocking = False
    return blocking and not cleared


# ---------------------------------------------------------------------------
# Request loading
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
        raise SystemExit("FAIL-CLOSED: target_path falls under a forbidden prefix (PI-8)")


def reject_presentation(p: dict, rule_id: str) -> None:
    found = find_presentation_key(p)
    if found:
        raise SystemExit(f"FAIL-CLOSED: presentation-bearing field '{found}' is FORBIDDEN ({rule_id})")


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

PER_KIND_SECTION_DIR = {
    "semantic-section": SECTIONS_DIR,
    "semantic-procedure": PROCEDURES_DIR,
    "semantic-warning-group": WARNINGS_DIR,
    "semantic-specification-group": SPECIFICATIONS_DIR,
    "semantic-troubleshooting-group": TROUBLESHOOTING_DIR,
    "semantic-support-group": SUPPORT_DIR,
}

PER_EXPORT_DIR = {
    "raw-html-export": RAW_HTML_DIR,
    "structured-json-export": JSON_EXPORT_DIR,
    "semantic-markdown-export": MARKDOWN_EXPORT_DIR,
}


def handle_manual_package(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    require(p, "manual_id")
    require(p, "canonical_product_id")
    require(p, "package_version")
    require(p, "semantic_structure", list)
    reject_forbidden(p)
    reject_presentation(p, "MP-8")

    semantic_structure = p["semantic_structure"]
    for i, sid in enumerate(semantic_structure):
        if not isinstance(sid, str) or not sid:
            raise SystemExit(f"FAIL-CLOSED: semantic_structure[{i}] must be non-empty string (MP-1)")
    if len(semantic_structure) != len(set(semantic_structure)):
        raise SystemExit("FAIL-CLOSED: duplicate section_id in semantic_structure (PI-4)")

    for ref_key in ("synthesis_ids", "extraction_ids", "grounding_ids", "evidence_refs"):
        v = p.get(ref_key, [])
        if not isinstance(v, list):
            raise SystemExit(f"FAIL-CLOSED: {ref_key} must be list (MP-2)")
    if not (p.get("extraction_ids") or p.get("synthesis_ids") or p.get("grounding_ids")):
        raise SystemExit("FAIL-CLOSED: missing lineage (extraction_ids / synthesis_ids / grounding_ids all empty) (PI-1)")

    continuity_status = p.get("continuity_status", "unresolved")
    if continuity_status not in CONTINUITY_STATUSES:
        raise SystemExit(f"FAIL-CLOSED: continuity_status '{continuity_status}' not in {sorted(CONTINUITY_STATUSES)} (MP-5)")

    pv = p["package_version"]
    parts = pv.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise SystemExit(f"FAIL-CLOSED: package_version '{pv}' must be MAJOR.MINOR.PATCH (MP-4)")

    if p.get("prior_package_id") and find_package(p["prior_package_id"]) is None:
        raise SystemExit(f"FAIL-CLOSED: prior_package_id '{p['prior_package_id']}' not found (MP-6)")

    canonical = {
        "manual_id": p["manual_id"],
        "canonical_product_id": p["canonical_product_id"],
        "package_version": pv,
        "semantic_structure": semantic_structure,
        "synthesis_ids": p.get("synthesis_ids", []),
        "extraction_ids": p.get("extraction_ids", []),
        "grounding_ids": p.get("grounding_ids", []),
        "evidence_refs": p.get("evidence_refs", []),
        "prior_package_id": p.get("prior_package_id"),
    }
    package_sha256 = sha256_hex(canonical_json(canonical))

    package_id = p.get("package_id") or "pkg-" + sha256_hex(p["manual_id"] + "|" + pv + "|" + package_sha256)[:16]
    op_id = "op-pkg-" + now_compact()
    payload = {
        "schema": "manual-package/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "package_id": package_id,
        "manual_id": p["manual_id"],
        "canonical_product_id": p["canonical_product_id"],
        "package_version": pv,
        "semantic_structure": semantic_structure,
        "synthesis_ids": p.get("synthesis_ids", []),
        "extraction_ids": p.get("extraction_ids", []),
        "grounding_ids": p.get("grounding_ids", []),
        "evidence_refs": p.get("evidence_refs", []),
        "continuity_status": continuity_status,
        "reasoning_chain": p.get("reasoning_chain", []),
        "prior_package_id": p.get("prior_package_id"),
        "package_sha256": package_sha256,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(PACKAGES_DIR, package_id, payload)
    append_event("manual-package-events", {
        "package_event_id": op_id, "kind": "register",
        "package_id": package_id, "manual_id": p["manual_id"],
        "package_version": pv, "package_sha256": package_sha256,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    append_event("packaging-lifecycle-events", {
        "lifecycle_event_id": op_id + "-lc", "kind": "register",
        "package_id": package_id, "from_state": None, "to_state": "draft",
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "manual-package", "info",
               f"package recorded: {package_id}", reviewer,
               {"package_id": package_id, "manual_id": p["manual_id"]})
    print(json.dumps({"ok": True, "package_id": package_id, "package_sha256": package_sha256,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_semantic_section(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    section_id = require(p, "section_id")
    manual_id = require(p, "manual_id")
    section_kind = require(p, "section_kind")
    if section_kind not in SECTION_KINDS:
        raise SystemExit(f"FAIL-CLOSED: section_kind '{section_kind}' not in {sorted(SECTION_KINDS)} (SS-2)")
    reject_forbidden(p)
    reject_presentation(p, "SS-6")

    for ref_key in ("extraction_ids", "grounding_ids", "evidence_refs", "body_blocks", "unresolved_states"):
        v = p.get(ref_key, [])
        if not isinstance(v, list):
            raise SystemExit(f"FAIL-CLOSED: {ref_key} must be list (SS-1)")

    trust = p.get("trust_composition", {"reviewer-approved": 0, "review-required": 0, "unresolved": 0})
    if not isinstance(trust, dict):
        raise SystemExit("FAIL-CLOSED: trust_composition must be dict (SS-3)")
    for k in ("reviewer-approved", "review-required", "unresolved"):
        if not isinstance(trust.get(k, 0), int):
            raise SystemExit(f"FAIL-CLOSED: trust_composition.{k} must be int (SS-3)")

    # SS-5 duplicate section_id within manual is FORBIDDEN
    existing = find_section(section_id)
    if existing is not None and existing.get("manual_id") == manual_id and not p.get("prior_section_id"):
        raise SystemExit(f"FAIL-CLOSED: duplicate section_id '{section_id}' in manual '{manual_id}' (SS-5/PI-4)")

    if section_kind == "semantic-procedure":
        steps = p.get("body_blocks", [])
        indices = []
        for i, b in enumerate(steps):
            if not isinstance(b, dict):
                raise SystemExit(f"FAIL-CLOSED: body_blocks[{i}] must be object (SS-8)")
            si = b.get("step_index")
            if not isinstance(si, int) or si < 1:
                raise SystemExit(f"FAIL-CLOSED: body_blocks[{i}].step_index must be int >= 1 (SS-8)")
            indices.append(si)
        if indices and indices != list(range(1, len(indices) + 1)):
            raise SystemExit(f"FAIL-CLOSED: semantic-procedure step indices must be contiguous starting at 1, got {indices} (SS-8/PC-2)")

    if not (p.get("extraction_ids") or p.get("grounding_ids")):
        raise SystemExit("FAIL-CLOSED: section missing lineage (extraction_ids and grounding_ids both empty) (SS-4/PI-3)")

    op_id = "op-sec-" + now_compact()
    payload = {
        "schema": "semantic-section/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "section_id": section_id,
        "manual_id": manual_id,
        "section_kind": section_kind,
        "title": p.get("title", ""),
        "extraction_ids": p.get("extraction_ids", []),
        "grounding_ids": p.get("grounding_ids", []),
        "evidence_refs": p.get("evidence_refs", []),
        "body_blocks": p.get("body_blocks", []),
        "unresolved_states": p.get("unresolved_states", []),
        "trust_composition": trust,
        "prior_section_id": p.get("prior_section_id"),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(SECTIONS_DIR, section_id, payload)
    mirror_dir = PER_KIND_SECTION_DIR[section_kind]
    if mirror_dir != SECTIONS_DIR:
        write_collision_safe_json(mirror_dir, section_id + "-mirror", {
            "schema": "semantic-section-mirror/1.0",
            "section_id": section_id, "section_kind": section_kind,
            "manifest_path": str(written.relative_to(REPO_ROOT)),
            "reviewer": reviewer, "recorded_at_iso": now_iso(),
        })
    append_event("semantic-section-events", {
        "section_event_id": op_id, "kind": "register",
        "section_id": section_id, "section_kind": section_kind,
        "manual_id": manual_id,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "semantic-section", "info",
               f"section recorded: {section_id}", reviewer,
               {"section_id": section_id, "section_kind": section_kind})
    print(json.dumps({"ok": True, "section_id": section_id,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_export_contract(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    manual_id = require(p, "manual_id")
    package_id = require(p, "package_id")
    export_kind = require(p, "export_kind")
    if export_kind not in EXPORT_KINDS:
        raise SystemExit(f"FAIL-CLOSED: export_kind '{export_kind}' not in {sorted(EXPORT_KINDS)} (XC-2)")
    reject_forbidden(p)
    reject_presentation(p, "XC-3")
    pkg = find_package(package_id)
    if pkg is None:
        raise SystemExit(f"FAIL-CLOSED: package '{package_id}' not found (XC-4/PI-7)")
    if pkg.get("manual_id") != manual_id:
        raise SystemExit("FAIL-CLOSED: manual_id does not match package (XC-4)")

    contract_id = p.get("contract_id") or "xc-" + sha256_hex(package_id + "|" + export_kind + "|" + now_compact())[:16]
    op_id = "op-xc-" + now_compact()
    payload = {
        "schema": "export-contract/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "contract_id": contract_id,
        "manual_id": manual_id,
        "package_id": package_id,
        "export_kind": export_kind,
        "reasoning_chain": p.get("reasoning_chain", []),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(CONTRACTS_DIR, contract_id, payload)
    append_event("export-contract-events", {
        "contract_event_id": op_id, "kind": "register",
        "contract_id": contract_id, "package_id": package_id,
        "export_kind": export_kind,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "export-contract", "info",
               f"export contract recorded: {contract_id}", reviewer,
               {"contract_id": contract_id, "export_kind": export_kind})
    print(json.dumps({"ok": True, "contract_id": contract_id,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def _render_payload(pkg: dict, sections_by_id: dict, export_kind: str) -> tuple[str, str]:
    """Deterministic renderer. Returns (rendered_text, sha256). Presentation-neutral."""
    ordered_sections = []
    for sid in pkg.get("semantic_structure", []):
        sec = sections_by_id.get(sid)
        if sec is None:
            raise SystemExit(f"FAIL-CLOSED: semantic_structure references missing section '{sid}' (PC-7/PI-3)")
        # Strip non-deterministic fields for rendering canonical view.
        ordered_sections.append({
            "section_id": sec.get("section_id"),
            "section_kind": sec.get("section_kind"),
            "title": sec.get("title", ""),
            "body_blocks": sec.get("body_blocks", []),
            "extraction_ids": sec.get("extraction_ids", []),
            "grounding_ids": sec.get("grounding_ids", []),
            "evidence_refs": sec.get("evidence_refs", []),
            "trust_composition": sec.get("trust_composition", {}),
            "unresolved_states": sec.get("unresolved_states", []),
        })
    if export_kind == "structured-json-export":
        text = json.dumps({
            "schema": "structured-json-export/1.0",
            "constitutional_layer_index": LAYER,
            "package_id": pkg.get("package_id"),
            "manual_id": pkg.get("manual_id"),
            "package_version": pkg.get("package_version"),
            "package_sha256": pkg.get("package_sha256"),
            "sections": ordered_sections,
        }, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    elif export_kind == "semantic-markdown-export":
        lines = [f"# {pkg.get('manual_id')} ({pkg.get('package_version')})", ""]
        for sec in ordered_sections:
            lines.append(f"## [{sec['section_kind']}] {sec.get('title') or sec['section_id']}")
            lines.append("")
            lines.append(f"<!-- section_id: {sec['section_id']} -->")
            for blk in sec.get("body_blocks", []):
                if isinstance(blk, dict):
                    if "step_index" in blk:
                        lines.append(f"{blk['step_index']}. {blk.get('text', '')}")
                    elif "text" in blk:
                        lines.append(blk["text"])
                    else:
                        lines.append(json.dumps(blk, ensure_ascii=False, sort_keys=True))
            lines.append("")
        text = "\n".join(lines)
    else:  # raw-html-export
        # Semantic HTML5 only; no class, no style, no breakpoints.
        parts = ["<article>",
                 f"  <h1>{pkg.get('manual_id')} ({pkg.get('package_version')})</h1>"]
        for sec in ordered_sections:
            parts.append("  <section>")
            parts.append(f"    <h2>{sec.get('title') or sec['section_id']}</h2>")
            for blk in sec.get("body_blocks", []):
                if isinstance(blk, dict):
                    if "step_index" in blk:
                        # group as ordered list — collected per section below would be cleaner, but stay simple
                        parts.append(f"    <p>{blk.get('step_index')}. {blk.get('text', '')}</p>")
                    elif "text" in blk:
                        parts.append(f"    <p>{blk['text']}</p>")
                    else:
                        parts.append(f"    <p>{json.dumps(blk, ensure_ascii=False, sort_keys=True)}</p>")
            parts.append("  </section>")
        parts.append("</article>")
        text = "\n".join(parts) + "\n"
    return text, sha256_hex(text)


def handle_export_render(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    contract_id = require(p, "contract_id")
    reject_forbidden(p)
    contract = find_contract(contract_id)
    if contract is None:
        raise SystemExit(f"FAIL-CLOSED: contract '{contract_id}' not found (XC-1)")
    pkg = find_package(contract["package_id"])
    if pkg is None:
        raise SystemExit(f"FAIL-CLOSED: package '{contract['package_id']}' not found (XC-4)")
    sections = find_sections_for_manual(pkg["manual_id"])
    sections_by_id = {s["section_id"]: s for s in sections}
    text, payload_sha256 = _render_payload(pkg, sections_by_id, contract["export_kind"])

    op_id = "op-xr-" + now_compact()
    render_id = p.get("render_id") or f"xr-{contract_id}-{now_compact()}"
    out_dir = PER_EXPORT_DIR[contract["export_kind"]]
    payload = {
        "schema": "export-render/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "render_id": render_id,
        "contract_id": contract_id,
        "package_id": pkg["package_id"],
        "manual_id": pkg["manual_id"],
        "export_kind": contract["export_kind"],
        "payload_sha256": payload_sha256,
        "reasoning_chain": p.get("reasoning_chain", []),
        "rendered_payload": text,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": {**payload, "rendered_payload_preview": text[:200]}}, indent=2))
        return 0
    written = write_collision_safe_json(out_dir, render_id, payload)
    append_event("export-contract-events", {
        "contract_event_id": op_id, "kind": "render",
        "contract_id": contract_id, "render_id": render_id,
        "package_id": pkg["package_id"], "export_kind": contract["export_kind"],
        "payload_sha256": payload_sha256,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "export-render", "info",
               f"export rendered: {render_id} ({contract['export_kind']}) sha256={payload_sha256}",
               reviewer, {"render_id": render_id, "payload_sha256": payload_sha256})
    print(json.dumps({"ok": True, "render_id": render_id, "payload_sha256": payload_sha256,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_packaging_continuity(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    manual_id = require(p, "manual_id")
    package_id = require(p, "package_id")
    reject_forbidden(p)
    pkg = find_package(package_id)
    if pkg is None:
        raise SystemExit(f"FAIL-CLOSED: package '{package_id}' not found (PC-1)")
    sections = find_sections_for_manual(manual_id)
    sections_by_id = {s["section_id"]: s for s in sections}

    findings: list[dict] = []
    seen = set()
    for sid in pkg.get("semantic_structure", []):
        if sid in seen:
            findings.append({"rule_id": "PC-9", "section_id": sid, "detail": "duplicate section_id in semantic_structure"})
        seen.add(sid)
        if sid not in sections_by_id:
            findings.append({"rule_id": "PC-7", "section_id": sid, "detail": "orphan section: cited in semantic_structure but not registered"})
            continue
        sec = sections_by_id[sid]
        if not (sec.get("extraction_ids") or sec.get("grounding_ids")):
            findings.append({"rule_id": "PC-8", "section_id": sid, "detail": "broken evidence lineage on section"})
        if sec.get("section_kind") == "semantic-procedure":
            indices = [b.get("step_index") for b in (sec.get("body_blocks") or []) if isinstance(b, dict)]
            if indices and indices != list(range(1, len(indices) + 1)):
                findings.append({"rule_id": "PC-2", "section_id": sid, "detail": f"procedural gap; indices={indices}"})
        if sec.get("section_kind") == "semantic-warning-group":
            severities = {b.get("severity") for b in (sec.get("body_blocks") or []) if isinstance(b, dict)}
            if not severities:
                findings.append({"rule_id": "PC-3", "section_id": sid, "detail": "warning group missing severity coverage"})
        if sec.get("section_kind") == "semantic-troubleshooting-group":
            has_escalation = any(isinstance(b, dict) and b.get("escalation") for b in (sec.get("body_blocks") or []))
            if not has_escalation:
                findings.append({"rule_id": "PC-5", "section_id": sid, "detail": "troubleshooting group missing escalation path"})

    blocking = bool(findings)
    check_id = p.get("continuity_check_id") or f"pc-{package_id}-{now_compact()}"
    op_id = "op-pc-" + now_compact()
    payload = {
        "schema": "packaging-continuity/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "continuity_check_id": check_id,
        "manual_id": manual_id,
        "package_id": package_id,
        "findings": findings,
        "blocking": blocking,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(CONTINUITY_DIR, check_id, payload)
    append_event("packaging-continuity-events", {
        "continuity_event_id": op_id, "kind": "register",
        "continuity_check_id": check_id, "package_id": package_id,
        "blocking": blocking, "finding_count": len(findings),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "packaging-continuity", "warning" if blocking else "info",
               f"continuity scan: {check_id} blocking={blocking}", reviewer,
               {"continuity_check_id": check_id, "findings": findings})
    print(json.dumps({"ok": True, "continuity_check_id": check_id,
                      "blocking": blocking, "findings": findings,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def _package_lineage_chain(package_id: str) -> dict:
    pkg = find_package(package_id)
    if pkg is None:
        raise SystemExit(f"FAIL-CLOSED: package '{package_id}' not found (PL-3)")
    sections = find_sections_for_manual(pkg["manual_id"])
    sections_by_id = {s["section_id"]: s for s in sections}
    missing: list[str] = []
    artifact_hashes = {"package": sha256_hex(canonical_json(pkg))}
    for sid in pkg.get("semantic_structure", []):
        sec = sections_by_id.get(sid)
        if sec is None:
            missing.append(f"section:{sid}")
            continue
        artifact_hashes[f"section:{sid}"] = sha256_hex(canonical_json(sec))
    prior = pkg.get("prior_package_id")
    if prior and find_package(prior) is None:
        missing.append(f"prior_package:{prior}")
    return {
        "package_id": package_id,
        "missing_pointers": missing,
        "artifact_hashes": artifact_hashes,
        "lineage_ok": not missing,
    }


def handle_packaging_lineage(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    package_id = require(p, "package_id")
    reject_forbidden(p)
    chain = _package_lineage_chain(package_id)
    lineage_id = p.get("lineage_id") or f"pl-{package_id}-{now_compact()}"
    op_id = "op-pl-" + now_compact()
    payload = {
        "schema": "packaging-lineage/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "lineage_id": lineage_id,
        "package_id": package_id,
        "scope": p.get("scope", "package"),
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
    written = write_collision_safe_json(LINEAGE_DIR, lineage_id, payload)
    append_event("packaging-lineage-events", {
        "lineage_event_id": op_id, "kind": "register",
        "lineage_id": lineage_id, "package_id": package_id,
        "lineage_ok": chain["lineage_ok"],
        "missing_pointers": chain["missing_pointers"],
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    if not chain["lineage_ok"]:
        emit_audit(op_id, "packaging-lineage", "warning",
                   f"lineage broken: {lineage_id}", reviewer,
                   {"lineage_id": lineage_id, "missing_pointers": chain["missing_pointers"]})
        raise SystemExit(f"FAIL-CLOSED: lineage broken: {chain['missing_pointers']} (PL-3)")
    emit_audit(op_id, "packaging-lineage", "info",
               f"lineage replayed: {lineage_id}", reviewer, {"lineage_id": lineage_id})
    print(json.dumps({"ok": True, "lineage_id": lineage_id, "lineage_ok": True,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def _recompute_package_sha256(pkg: dict) -> str:
    canonical = {
        "manual_id": pkg["manual_id"],
        "canonical_product_id": pkg["canonical_product_id"],
        "package_version": pkg["package_version"],
        "semantic_structure": pkg["semantic_structure"],
        "synthesis_ids": pkg.get("synthesis_ids", []),
        "extraction_ids": pkg.get("extraction_ids", []),
        "grounding_ids": pkg.get("grounding_ids", []),
        "evidence_refs": pkg.get("evidence_refs", []),
        "prior_package_id": pkg.get("prior_package_id"),
    }
    return sha256_hex(canonical_json(canonical))


def handle_packaging_replay(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    package_id = require(p, "package_id")
    reject_forbidden(p)
    pkg = find_package(package_id)
    if pkg is None:
        raise SystemExit(f"FAIL-CLOSED: package '{package_id}' not found (PR-1)")
    chain = _package_lineage_chain(package_id)
    recomputed = _recompute_package_sha256(pkg)
    sha_mismatch = recomputed != pkg.get("package_sha256")
    expected = p.get("expected_package_sha256")
    expected_mismatch = bool(expected) and expected != pkg.get("package_sha256")
    replay_ok = chain["lineage_ok"] and not sha_mismatch and not expected_mismatch

    replay_id = p.get("replay_id") or f"pr-{package_id}-{now_compact()}"
    op_id = "op-pr-" + now_compact()
    payload = {
        "schema": "packaging-replay/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "replay_id": replay_id,
        "package_id": package_id,
        "stored_package_sha256": pkg.get("package_sha256"),
        "recomputed_package_sha256": recomputed,
        "expected_package_sha256": expected,
        "sha_mismatch": sha_mismatch,
        "expected_mismatch": expected_mismatch,
        "missing_pointers": chain["missing_pointers"],
        "artifact_hashes": chain["artifact_hashes"],
        "replay_ok": replay_ok,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(REPLAYS_DIR, replay_id, payload)
    append_event("packaging-replay-events", {
        "replay_event_id": op_id, "kind": "register",
        "replay_id": replay_id, "package_id": package_id,
        "replay_ok": replay_ok,
        "missing_pointer_count": len(chain["missing_pointers"]),
        "sha_mismatch": sha_mismatch,
        "expected_mismatch": expected_mismatch,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    if not replay_ok:
        emit_audit(op_id, "packaging-replay", "warning",
                   f"replay failed: {replay_id}", reviewer,
                   {"missing_pointers": chain["missing_pointers"],
                    "sha_mismatch": sha_mismatch, "expected_mismatch": expected_mismatch})
        raise SystemExit(f"FAIL-CLOSED: replay failed missing={chain['missing_pointers']} sha_mismatch={sha_mismatch} expected_mismatch={expected_mismatch} (PR-2)")
    emit_audit(op_id, "packaging-replay", "info",
               f"replay ok: {replay_id}", reviewer, {"replay_id": replay_id})
    print(json.dumps({"ok": True, "replay_id": replay_id, "replay_ok": True,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_packaging_lifecycle_transition(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    package_id = require(p, "package_id")
    from_state = require(p, "from_state")
    to_state = require(p, "to_state")
    if from_state not in LIFECYCLE_STATES or to_state not in LIFECYCLE_STATES:
        raise SystemExit("FAIL-CLOSED: invalid lifecycle state(s) (PXL-1)")
    if (from_state, to_state) not in LIFECYCLE_EDGES:
        raise SystemExit(f"FAIL-CLOSED: illegal lifecycle transition {from_state} -> {to_state} (PXL-2)")
    if find_package(package_id) is None:
        raise SystemExit(f"FAIL-CLOSED: package '{package_id}' not found (PXL-1)")
    actual = current_package_state(package_id)
    if actual is None:
        raise SystemExit(f"FAIL-CLOSED: package '{package_id}' has no recorded lifecycle (PXL-2)")
    if actual != from_state:
        raise SystemExit(f"FAIL-CLOSED: declared from_state '{from_state}' != actual '{actual}' (PXL-2)")
    if actual in LIFECYCLE_TERMINAL:
        raise SystemExit(f"FAIL-CLOSED: package is in terminal state '{actual}' (PXL-3)")
    if to_state == "superseded" and not p.get("successor_package_id"):
        raise SystemExit("FAIL-CLOSED: superseded transition requires successor_package_id (PXL-4)")
    if to_state == "export-ready":
        if not has_successful_replay(package_id):
            raise SystemExit("FAIL-CLOSED: export-ready requires a prior successful packaging-replay (PXL-6)")
        if has_blocking_integrity_finding(package_id):
            raise SystemExit("FAIL-CLOSED: export-ready blocked by unresolved integrity findings (PXL-6)")
    reject_forbidden(p)

    op_id = "op-pxl-" + now_compact()
    payload = {
        "schema": "packaging-lifecycle-transition/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "package_id": package_id,
        "from_state": from_state,
        "to_state": to_state,
        "successor_package_id": p.get("successor_package_id"),
        "reasoning_chain": p.get("reasoning_chain", []),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(LIFECYCLE_DIR, f"{package_id}-{from_state}-to-{to_state}", payload)
    append_event("packaging-lifecycle-events", {
        "lifecycle_event_id": op_id, "kind": "lifecycle-transition",
        "package_id": package_id, "from_state": from_state, "to_state": to_state,
        "successor_package_id": p.get("successor_package_id"),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "packaging-lifecycle-transition", "info",
               f"lifecycle: {package_id} {from_state} -> {to_state}", reviewer,
               {"package_id": package_id})
    print(json.dumps({"ok": True, "package_id": package_id,
                      "from_state": from_state, "to_state": to_state,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_packaging_integrity(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    reject_forbidden(p)
    target_package_id = p.get("package_id")
    target_manual_id = p.get("manual_id")
    findings: list[dict] = []
    packages: list[dict] = []
    seen_pkg = set()
    if PACKAGES_DIR.exists():
        for path in sorted(PACKAGES_DIR.glob("*.json")):
            try:
                d = load_json(path)
            except Exception:
                continue
            if target_package_id and d.get("package_id") != target_package_id:
                continue
            if target_manual_id and d.get("manual_id") != target_manual_id:
                continue
            pid = d.get("package_id")
            if pid in seen_pkg:
                continue
            seen_pkg.add(pid)
            packages.append(d)

    for pkg in packages:
        pid = pkg.get("package_id")
        if not (pkg.get("extraction_ids") or pkg.get("synthesis_ids") or pkg.get("grounding_ids")):
            findings.append({"rule_id": "PI-1", "package_id": pid, "detail": "missing lineage"})
        sections = find_sections_for_manual(pkg.get("manual_id"))
        sections_by_id = {s["section_id"]: s for s in sections}
        seen_sids = set()
        for sid in pkg.get("semantic_structure", []):
            if sid in seen_sids:
                findings.append({"rule_id": "PI-4", "package_id": pid, "section_id": sid, "detail": "duplicate section_id"})
            seen_sids.add(sid)
            if sid not in sections_by_id:
                findings.append({"rule_id": "PI-3", "package_id": pid, "section_id": sid, "detail": "orphan section"})
                continue
            sec = sections_by_id[sid]
            if not sec.get("grounding_ids") and not sec.get("extraction_ids"):
                findings.append({"rule_id": "PI-2", "package_id": pid, "section_id": sid, "detail": "unresolved grounding/extraction"})
            if not sec.get("evidence_refs"):
                findings.append({"rule_id": "PI-6", "package_id": pid, "section_id": sid, "detail": "unresolved evidence_refs"})
        chain = _package_lineage_chain(pid)
        if not chain["lineage_ok"]:
            findings.append({"rule_id": "PI-5", "package_id": pid, "detail": f"broken continuity/lineage: {chain['missing_pointers']}"})
        recomputed = _recompute_package_sha256(pkg)
        if recomputed != pkg.get("package_sha256"):
            findings.append({"rule_id": "PI-9", "package_id": pid, "detail": "hidden semantic mutation: sha256 mismatch"})
        # invalid contracts
        if CONTRACTS_DIR.exists():
            for cpath in sorted(CONTRACTS_DIR.glob("*.json")):
                try:
                    c = load_json(cpath)
                except Exception:
                    continue
                if c.get("package_id") != pid:
                    continue
                if c.get("export_kind") not in EXPORT_KINDS:
                    findings.append({"rule_id": "PI-7", "package_id": pid, "contract_id": c.get("contract_id"),
                                     "detail": f"invalid export_kind: {c.get('export_kind')}"})
                pres = find_presentation_key(c)
                if pres:
                    findings.append({"rule_id": "PI-7", "package_id": pid, "contract_id": c.get("contract_id"),
                                     "detail": f"contract carries presentation key: {pres}"})

    blocking = bool(findings)
    check_id = p.get("integrity_check_id") or f"pi-{now_compact()}"
    op_id = "op-pi-" + now_compact()
    payload = {
        "schema": "packaging-integrity/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "integrity_check_id": check_id,
        "scope": p.get("scope", "all"),
        "manual_id": target_manual_id,
        "package_id": target_package_id,
        "package_count": len(packages),
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
    append_event("packaging-integrity-events", {
        "integrity_event_id": op_id, "kind": "register",
        "integrity_check_id": check_id, "blocking": blocking,
        "package_id": target_package_id,
        "finding_count": len(findings),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "packaging-integrity", "warning" if blocking else "info",
               f"integrity scan: {check_id} blocking={blocking}", reviewer,
               {"integrity_check_id": check_id, "findings": findings})
    print(json.dumps({"ok": True, "integrity_check_id": check_id,
                      "blocking": blocking, "findings": findings,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_reviewer_packaging_override(env: dict, confirm: bool) -> int:
    p = env["payload"]; reviewer = env["reviewer"]
    target_id = require(p, "target_artifact_id")
    target_kind = p.get("target_kind", "package")
    if target_kind not in OVERRIDE_TARGET_KINDS:
        raise SystemExit(f"FAIL-CLOSED: target_kind '{target_kind}' not in {sorted(OVERRIDE_TARGET_KINDS)} (PRO-1)")
    kind = p.get("kind", "reject")
    if kind not in OVERRIDE_KINDS:
        raise SystemExit(f"FAIL-CLOSED: override kind '{kind}' not in {sorted(OVERRIDE_KINDS)} (PRO-1)")
    cited = p.get("cited_rule_ids", [])
    if kind == "reject" and not (isinstance(cited, list) and cited):
        raise SystemExit("FAIL-CLOSED: reject overrides require cited_rule_ids (PRO-3)")
    reject_forbidden(p)
    if target_kind == "package" and find_package(target_id) is None:
        raise SystemExit(f"FAIL-CLOSED: target package '{target_id}' not found (PRO-1)")
    if target_kind == "section" and find_section(target_id) is None:
        raise SystemExit(f"FAIL-CLOSED: target section '{target_id}' not found (PRO-1)")
    if target_kind == "contract" and find_contract(target_id) is None:
        raise SystemExit(f"FAIL-CLOSED: target contract '{target_id}' not found (PRO-1)")

    override_id = p.get("override_id") or f"pro-{target_id}-{now_compact()}"
    op_id = "op-pro-" + now_compact()
    payload = {
        "schema": "reviewer-packaging-decision/1.0",
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
    append_event("reviewer-packaging-decision-events", {
        "decision_event_id": op_id, "kind": "reviewer-override",
        "override_id": override_id, "target_artifact_id": target_id,
        "target_kind": target_kind, "override_kind": kind,
        "cited_rule_ids": cited,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer, "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "reviewer-packaging-override", "info",
               f"reviewer override recorded: {override_id} kind={kind}", reviewer,
               {"override_id": override_id, "target_artifact_id": target_id})
    print(json.dumps({"ok": True, "override_id": override_id, "kind": kind,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

DISPATCH = {
    "manual-package": handle_manual_package,
    "semantic-section": handle_semantic_section,
    "export-contract": handle_export_contract,
    "export-render": handle_export_render,
    "packaging-continuity": handle_packaging_continuity,
    "packaging-lineage": handle_packaging_lineage,
    "packaging-replay": handle_packaging_replay,
    "packaging-lifecycle-transition": handle_packaging_lifecycle_transition,
    "packaging-integrity": handle_packaging_integrity,
    "reviewer-packaging-override": handle_reviewer_packaging_override,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 53 — governed manual semantic packaging CLI executor (layer 46).",
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
