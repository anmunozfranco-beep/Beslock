"""
Phase 51 — Governed multimodal publication composition & page orchestration CLI executor (layer 44).

Reviewer-invoked. Foreground. Deterministic. Append-only. Fail-closed.
NO daemon. NO watcher. NO scheduler. NO LLM. NO ML. NO probabilistic composition.
NO autonomous layout generation. NO cloud / SaaS. Stdlib only.

The executor records reviewer-authored composition drafts, page layouts,
multimodal sequences, responsive parity manifests, page-continuity scans,
publication assemblies, page-level layout reviews, composition-lifecycle
transitions, and composition-integrity scans. It NEVER writes the live
publication tree, the layer-42 visual-publication-builds tree, or the
layer-43 visual-generation-runtime tree.
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
PC_ROOT = OC_ROOT / "publication-composition-runtime"
VG_ASSETS_DIR = OC_ROOT / "visual-generation-runtime" / "generated-assets"

COMPOSITION_DRAFTS_DIR = PC_ROOT / "composition-drafts"
PAGE_LAYOUTS_DIR = PC_ROOT / "page-layouts"
SECTION_COMPOSITIONS_DIR = PC_ROOT / "section-compositions"
SEQUENCES_DIR = PC_ROOT / "multimodal-sequences"
RESPONSIVE_DIR = PC_ROOT / "responsive-layouts"
ASSEMBLIES_DIR = PC_ROOT / "publication-assemblies"
LAYOUT_LINEAGE_DIR = PC_ROOT / "layout-lineage"
CONTINUITY_DIR = PC_ROOT / "page-continuity"
LAYOUT_REVIEW_DIR = PC_ROOT / "layout-review"
LIFECYCLE_DIR = PC_ROOT / "publication-composition-lifecycle"
PREVIEWS_DIR = PC_ROOT / "render-previews"
DECISIONS_DIR = PC_ROOT / "reviewer-layout-decisions"

LAYER = 44
SCHEMA = "governed-fs-operation-request/1.0"

MANUAL_KINDS = {
    "procedural", "troubleshooting", "specification-heavy", "comparison",
    "warning-centric", "multimodal-responsive", "oem-derived", "generated-visual",
}

SECTION_ROLES = {
    "overview", "warning", "specification", "procedural",
    "troubleshooting", "comparison", "evidence-trace", "appendix",
}

RESPONSIVE_BREAKPOINTS = {"mobile", "tablet", "desktop", "print"}

LIFECYCLE_STATES = {
    "draft", "composed", "review-required", "reviewer-approved",
    "publication-ready", "superseded", "deprecated",
}
LIFECYCLE_TERMINAL = {"deprecated"}
LIFECYCLE_EDGES = {
    ("draft", "composed"),
    ("composed", "review-required"),
    ("composed", "draft"),
    ("review-required", "reviewer-approved"),
    ("review-required", "composed"),
    ("reviewer-approved", "publication-ready"),
    ("reviewer-approved", "review-required"),
    ("publication-ready", "superseded"),
    ("publication-ready", "deprecated"),
    ("superseded", "deprecated"),
}

REVIEW_DECISIONS = {"approve", "request-changes", "reject"}
SEQUENCE_KINDS = {"procedural", "troubleshooting", "comparison"}

# Forbidden destinations: layer-43 visual-generation-runtime data, layer-42
# visual-publication-builds, live publication tree, knowledge-core, governance,
# runtime-implementation, runtime-manifests payloads, OEM source assets.
FORBIDDEN_OVERWRITE_PREFIXES = (
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
# Replay helpers
# ---------------------------------------------------------------------------

def find_composition_record(composition_id: str) -> dict | None:
    if not COMPOSITION_DRAFTS_DIR.exists():
        return None
    latest = None
    for p in sorted(COMPOSITION_DRAFTS_DIR.glob("*.json")):
        try:
            d = load_json(p)
        except Exception:
            continue
        if d.get("composition_id") == composition_id:
            latest = d
    return latest


def current_composition_state(composition_id: str) -> str | None:
    store_path = RUNTIME_MANIFESTS_ROOT / "composition-lifecycle-events" / "_event-store.json"
    last = None
    if store_path.exists():
        for e in load_json(store_path).get("events", []):
            if e.get("composition_id") != composition_id:
                continue
            if e.get("kind") == "lifecycle-transition":
                last = e.get("to_state")
            elif e.get("kind") == "register" and last is None:
                last = "draft"
    return last


def find_asset_record(asset_id: str) -> dict | None:
    if not VG_ASSETS_DIR.exists():
        return None
    latest = None
    for p in sorted(VG_ASSETS_DIR.glob("*.json")):
        try:
            d = load_json(p)
        except Exception:
            continue
        if d.get("asset_id") == asset_id:
            latest = d
    return latest


def list_page_layouts_for_composition(composition_id: str) -> list[dict]:
    if not PAGE_LAYOUTS_DIR.exists():
        return []
    out: list[dict] = []
    for p in sorted(PAGE_LAYOUTS_DIR.glob("*.json")):
        try:
            d = load_json(p)
        except Exception:
            continue
        if d.get("composition_id") == composition_id:
            out.append(d)
    return out


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


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

def handle_composition_draft(env: dict, confirm: bool) -> int:
    p = env["payload"]
    reviewer = env["reviewer"]
    require(p, "synthesis_id")
    require(p, "manual_kind")
    if p["manual_kind"] not in MANUAL_KINDS:
        raise SystemExit(f"FAIL-CLOSED: manual_kind '{p['manual_kind']}' not in {sorted(MANUAL_KINDS)}")
    section_order = require(p, "section_order", list)
    if not all(isinstance(s, str) and s for s in section_order):
        raise SystemExit("FAIL-CLOSED: section_order must be non-empty strings")
    if len(section_order) != len(set(section_order)):
        raise SystemExit("FAIL-CLOSED: section_order MUST be unique (deterministic ordering)")
    if attempts_overwrite_forbidden(p.get("target_path")):
        raise SystemExit("FAIL-CLOSED: target_path falls under a forbidden prefix")

    composition_id = p.get("composition_id") or "comp-" + sha256_hex(
        p["synthesis_id"] + "|" + "|".join(section_order)
    )[:16]
    op_id = "op-cdraft-" + now_compact()
    payload = {
        "schema": "publication-composition-draft/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "composition_id": composition_id,
        "synthesis_id": p["synthesis_id"],
        "manual_id": p.get("manual_id"),
        "manual_kind": p["manual_kind"],
        "canonical_product_id": p.get("canonical_product_id"),
        "section_order": section_order,
        "rationale": p.get("rationale", ""),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0

    written = write_collision_safe_json(COMPOSITION_DRAFTS_DIR, composition_id, payload)
    append_event("composition-events", {
        "composition_event_id": op_id,
        "kind": "register",
        "composition_id": composition_id,
        "synthesis_id": p["synthesis_id"],
        "manual_kind": p["manual_kind"],
        "section_count": len(section_order),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    # initial lifecycle anchor (draft)
    append_event("composition-lifecycle-events", {
        "lifecycle_event_id": op_id + "-lc",
        "kind": "register",
        "composition_id": composition_id,
        "from_state": None,
        "to_state": "draft",
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "composition-draft", "info",
               f"composition draft recorded: {composition_id}", reviewer,
               {"composition_id": composition_id, "manifest_path": str(written.relative_to(REPO_ROOT))})
    print(json.dumps({"ok": True, "composition_id": composition_id,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_page_layout(env: dict, confirm: bool) -> int:
    p = env["payload"]
    reviewer = env["reviewer"]
    composition_id = require(p, "composition_id")
    page_index = p.get("page_index")
    if not isinstance(page_index, int) or page_index < 1:
        raise SystemExit("FAIL-CLOSED: page_index must be int >= 1")
    blocks = require(p, "blocks", list)
    block_ids = []
    has_warning = False
    has_procedural_after_warning = True
    saw_warning = False
    visual_count = 0
    for i, b in enumerate(blocks):
        if not isinstance(b, dict):
            raise SystemExit(f"FAIL-CLOSED: blocks[{i}] must be object")
        bid = b.get("block_id")
        role = b.get("role")
        if not bid:
            raise SystemExit(f"FAIL-CLOSED: blocks[{i}].block_id required")
        if role not in SECTION_ROLES:
            raise SystemExit(f"FAIL-CLOSED: blocks[{i}].role '{role}' not in {sorted(SECTION_ROLES)}")
        if bid in block_ids:
            raise SystemExit(f"FAIL-CLOSED: duplicate block_id '{bid}'")
        block_ids.append(bid)
        if role == "warning":
            saw_warning = True
            has_warning = True
        if role == "procedural" and not saw_warning and any(
            bb.get("role") == "warning" for bb in blocks
        ):
            # warnings exist but were placed after this procedural block
            has_procedural_after_warning = False
        if b.get("asset_id"):
            visual_count += 1
            if not b.get("grounding_id"):
                raise SystemExit(f"FAIL-CLOSED: blocks[{i}] cites asset_id without grounding_id (LO-3)")
            if find_asset_record(b["asset_id"]) is None:
                raise SystemExit(f"FAIL-CLOSED: orphan visual: asset_id '{b['asset_id']}' not found in layer-43 records (LO-3)")
    if not has_procedural_after_warning:
        raise SystemExit("FAIL-CLOSED: warning blocks MUST precede the procedural blocks they govern (LO-4)")
    max_visuals = p.get("max_visuals_per_page", 6)
    if visual_count > max_visuals:
        raise SystemExit(f"FAIL-CLOSED: visual density {visual_count} exceeds ceiling {max_visuals} (LO-6)")
    if attempts_overwrite_forbidden(p.get("target_path")):
        raise SystemExit("FAIL-CLOSED: target_path falls under a forbidden prefix")

    if find_composition_record(composition_id) is None:
        raise SystemExit(f"FAIL-CLOSED: composition '{composition_id}' not found")

    page_layout_id = p.get("page_layout_id") or f"pl-{composition_id}-p{page_index:03d}"
    op_id = "op-playout-" + now_compact()
    payload = {
        "schema": "page-layout/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "page_layout_id": page_layout_id,
        "composition_id": composition_id,
        "page_index": page_index,
        "section_id": p.get("section_id"),
        "continuation_of": p.get("continuation_of"),
        "blocks": blocks,
        "max_visuals_per_page": max_visuals,
        "has_warning": has_warning,
        "visual_count": visual_count,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(PAGE_LAYOUTS_DIR, page_layout_id, payload)
    append_event("layout-events", {
        "layout_event_id": op_id,
        "kind": "register",
        "page_layout_id": page_layout_id,
        "composition_id": composition_id,
        "page_index": page_index,
        "block_count": len(blocks),
        "visual_count": visual_count,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    # lineage record
    write_collision_safe_json(LAYOUT_LINEAGE_DIR, page_layout_id + "-lineage", {
        "schema": "layout-lineage/1.0",
        "constitutional_layer_index": LAYER,
        "page_layout_id": page_layout_id,
        "composition_id": composition_id,
        "section_id": p.get("section_id"),
        "continuation_of": p.get("continuation_of"),
        "block_ids": block_ids,
        "asset_ids": [b.get("asset_id") for b in blocks if b.get("asset_id")],
        "grounding_ids": [b.get("grounding_id") for b in blocks if b.get("grounding_id")],
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "page-layout", "info",
               f"page layout recorded: {page_layout_id}", reviewer,
               {"page_layout_id": page_layout_id, "manifest_path": str(written.relative_to(REPO_ROOT))})
    print(json.dumps({"ok": True, "page_layout_id": page_layout_id,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_multimodal_sequence(env: dict, confirm: bool) -> int:
    p = env["payload"]
    reviewer = env["reviewer"]
    composition_id = require(p, "composition_id")
    if find_composition_record(composition_id) is None:
        raise SystemExit(f"FAIL-CLOSED: composition '{composition_id}' not found")
    sequence_kind = p.get("sequence_kind", "procedural")
    if sequence_kind not in SEQUENCE_KINDS:
        raise SystemExit(f"FAIL-CLOSED: sequence_kind '{sequence_kind}' not in {sorted(SEQUENCE_KINDS)}")
    steps = require(p, "steps", list)
    if sequence_kind == "comparison" and len(steps) < 2:
        raise SystemExit("FAIL-CLOSED: comparison sequences require >= 2 entries (SQ-5)")
    severity_order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    last_severity = 0
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            raise SystemExit(f"FAIL-CLOSED: steps[{i}] must be object")
        if sequence_kind == "procedural":
            idx = step.get("step_index")
            if idx != i + 1:
                raise SystemExit(f"FAIL-CLOSED: procedural step_index gap at {i}: expected {i+1} got {idx} (SQ-2)")
        if step.get("asset_id") and not step.get("grounding_id"):
            raise SystemExit(f"FAIL-CLOSED: steps[{i}] cites asset_id without grounding_id (SQ-3)")
        if sequence_kind == "troubleshooting":
            sev = severity_order.get(step.get("severity"), 0)
            if sev == 0:
                raise SystemExit(f"FAIL-CLOSED: troubleshooting steps[{i}] missing/invalid severity (SQ-4)")
            if sev < last_severity:
                raise SystemExit(f"FAIL-CLOSED: troubleshooting reverse-escalation at step {i} (SQ-4)")
            last_severity = sev
    if attempts_overwrite_forbidden(p.get("target_path")):
        raise SystemExit("FAIL-CLOSED: target_path falls under a forbidden prefix")
    sequence_id = p.get("sequence_id") or f"seq-{composition_id}-{sequence_kind}-{sha256_hex(json.dumps(steps, sort_keys=True))[:10]}"
    op_id = "op-seq-" + now_compact()
    payload = {
        "schema": "multimodal-sequence/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "sequence_id": sequence_id,
        "composition_id": composition_id,
        "sequence_kind": sequence_kind,
        "steps": steps,
        "image_text_ratio_ceiling": p.get("image_text_ratio_ceiling"),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(SEQUENCES_DIR, sequence_id, payload)
    append_event("sequence-events", {
        "sequence_event_id": op_id,
        "kind": "register",
        "sequence_id": sequence_id,
        "composition_id": composition_id,
        "sequence_kind": sequence_kind,
        "step_count": len(steps),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "multimodal-sequence", "info",
               f"sequence recorded: {sequence_id}", reviewer,
               {"sequence_id": sequence_id})
    print(json.dumps({"ok": True, "sequence_id": sequence_id,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_responsive_layout(env: dict, confirm: bool) -> int:
    p = env["payload"]
    reviewer = env["reviewer"]
    composition_id = require(p, "composition_id")
    if find_composition_record(composition_id) is None:
        raise SystemExit(f"FAIL-CLOSED: composition '{composition_id}' not found")
    parity = require(p, "parity", dict)  # { block_id: { breakpoint: bool } }
    omissions = p.get("omissions", [])  # [ { block_id, breakpoint, reviewer_rationale } ]
    omitted = {(o["block_id"], o["breakpoint"]) for o in omissions if "block_id" in o and "breakpoint" in o}
    page_layout_id = p.get("page_layout_id")
    block_role_map: dict[str, str] = {}
    if page_layout_id:
        for ll in list_page_layouts_for_composition(composition_id):
            if ll.get("page_layout_id") == page_layout_id:
                for b in ll.get("blocks", []):
                    block_role_map[b.get("block_id")] = b.get("role")
                break

    parity_ok = True
    broken: list[dict] = []
    for block_id, bps in parity.items():
        if not isinstance(bps, dict):
            raise SystemExit(f"FAIL-CLOSED: parity['{block_id}'] must be object")
        for bp in RESPONSIVE_BREAKPOINTS:
            present = bool(bps.get(bp, False))
            if not present and (block_id, bp) not in omitted:
                parity_ok = False
                broken.append({"block_id": block_id, "breakpoint": bp})
            if not present and block_role_map.get(block_id) == "warning":
                # Warnings cannot be omitted at any breakpoint (RR-3)
                raise SystemExit(f"FAIL-CLOSED: warning block '{block_id}' omitted at breakpoint '{bp}' (RR-3)")
    if attempts_overwrite_forbidden(p.get("target_path")):
        raise SystemExit("FAIL-CLOSED: target_path falls under a forbidden prefix")

    rl_id = p.get("responsive_layout_id") or f"rl-{composition_id}-{sha256_hex(json.dumps(parity, sort_keys=True))[:10]}"
    op_id = "op-resp-" + now_compact()
    payload = {
        "schema": "responsive-layout/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "responsive_layout_id": rl_id,
        "composition_id": composition_id,
        "page_layout_id": page_layout_id,
        "parity": parity,
        "omissions": omissions,
        "parity_ok": parity_ok,
        "broken_parity": broken,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(RESPONSIVE_DIR, rl_id, payload)
    # Deterministic preview snapshot
    write_collision_safe_json(PREVIEWS_DIR, rl_id + "-preview", {
        "schema": "render-preview/1.0",
        "constitutional_layer_index": LAYER,
        "responsive_layout_id": rl_id,
        "composition_id": composition_id,
        "snapshot_sha256": sha256_hex(json.dumps(payload, sort_keys=True)),
        "recorded_at_iso": now_iso(),
        "append_only": True,
    })
    append_event("responsive-render-events", {
        "responsive_event_id": op_id,
        "kind": "register",
        "responsive_layout_id": rl_id,
        "composition_id": composition_id,
        "parity_ok": parity_ok,
        "broken_count": len(broken),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    severity = "info" if parity_ok else "warning"
    emit_audit(op_id, "responsive-layout", severity,
               f"responsive layout recorded: {rl_id} parity_ok={parity_ok}", reviewer,
               {"responsive_layout_id": rl_id, "broken_parity": broken})
    print(json.dumps({"ok": True, "responsive_layout_id": rl_id, "parity_ok": parity_ok,
                      "broken_parity": broken,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_page_continuity(env: dict, confirm: bool) -> int:
    p = env["payload"]
    reviewer = env["reviewer"]
    composition_id = require(p, "composition_id")
    composition = find_composition_record(composition_id)
    if composition is None:
        raise SystemExit(f"FAIL-CLOSED: composition '{composition_id}' not found")
    declared_sections = composition.get("section_order", [])

    layouts = list_page_layouts_for_composition(composition_id)
    page_indices = sorted({ll.get("page_index") for ll in layouts if isinstance(ll.get("page_index"), int)})
    declared_page_indices = p.get("page_indices") or page_indices
    # contiguity check
    contiguous = (declared_page_indices == list(range(1, len(declared_page_indices) + 1)))
    # acyclic continuation_of
    cont_map = {ll.get("page_layout_id"): ll.get("continuation_of") for ll in layouts}
    acyclic = True
    cycle_node = None
    for start in cont_map:
        seen = set()
        cur = start
        while cur:
            if cur in seen:
                acyclic = False
                cycle_node = cur
                break
            seen.add(cur)
            cur = cont_map.get(cur)
        if not acyclic:
            break

    sections_present = set()
    asset_ids_referenced: list[str] = []
    for ll in layouts:
        if ll.get("section_id"):
            sections_present.add(ll["section_id"])
        for b in ll.get("blocks", []):
            if b.get("section_id"):
                sections_present.add(b["section_id"])
            if b.get("asset_id"):
                asset_ids_referenced.append(b["asset_id"])
    orphan_sections = [s for s in declared_sections if s not in sections_present]
    orphan_assets = [a for a in asset_ids_referenced if find_asset_record(a) is None]
    hidden_sections = sorted(sections_present - set(declared_sections))

    integrity_ok = (contiguous and acyclic and not orphan_sections
                    and not orphan_assets and not hidden_sections)

    if attempts_overwrite_forbidden(p.get("target_path")):
        raise SystemExit("FAIL-CLOSED: target_path falls under a forbidden prefix")

    check_id = p.get("continuity_check_id") or f"cont-{composition_id}-{now_compact()}"
    op_id = "op-cont-" + now_compact()
    payload = {
        "schema": "page-continuity/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "continuity_check_id": check_id,
        "composition_id": composition_id,
        "page_indices": declared_page_indices,
        "contiguous": contiguous,
        "acyclic": acyclic,
        "cycle_node": cycle_node,
        "declared_sections": declared_sections,
        "sections_present": sorted(sections_present),
        "orphan_sections": orphan_sections,
        "orphan_assets": orphan_assets,
        "hidden_sections": hidden_sections,
        "integrity_ok": integrity_ok,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(CONTINUITY_DIR, check_id, payload)
    append_event("page-continuity-events", {
        "continuity_event_id": op_id,
        "kind": "register",
        "continuity_check_id": check_id,
        "composition_id": composition_id,
        "integrity_ok": integrity_ok,
        "orphan_section_count": len(orphan_sections),
        "orphan_asset_count": len(orphan_assets),
        "hidden_section_count": len(hidden_sections),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    severity = "info" if integrity_ok else "warning"
    emit_audit(op_id, "page-continuity", severity,
               f"continuity scan recorded: {check_id} integrity_ok={integrity_ok}", reviewer,
               {"continuity_check_id": check_id,
                "orphan_sections": orphan_sections,
                "orphan_assets": orphan_assets,
                "hidden_sections": hidden_sections})
    print(json.dumps({"ok": True, "continuity_check_id": check_id, "integrity_ok": integrity_ok,
                      "orphan_sections": orphan_sections, "orphan_assets": orphan_assets,
                      "hidden_sections": hidden_sections,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_publication_assembly(env: dict, confirm: bool) -> int:
    p = env["payload"]
    reviewer = env["reviewer"]
    composition_id = require(p, "composition_id")
    page_layout_ids = require(p, "page_layout_ids", list)
    if find_composition_record(composition_id) is None:
        raise SystemExit(f"FAIL-CLOSED: composition '{composition_id}' not found")
    state = current_composition_state(composition_id)
    if state not in ("reviewer-approved", "publication-ready"):
        raise SystemExit(f"FAIL-CLOSED: composition state '{state}' is not reviewer-approved/publication-ready (PA-2)")
    layouts = {ll.get("page_layout_id"): ll for ll in list_page_layouts_for_composition(composition_id)}
    missing = [pl for pl in page_layout_ids if pl not in layouts]
    if missing:
        raise SystemExit(f"FAIL-CLOSED: assembly references missing page_layout_ids: {missing}")
    if attempts_overwrite_forbidden(p.get("target_path")):
        raise SystemExit("FAIL-CLOSED: target_path falls under a forbidden prefix")

    layout_hashes = {pl: sha256_hex(json.dumps(layouts[pl], sort_keys=True)) for pl in page_layout_ids}
    section_ids = sorted({ll.get("section_id") for ll in layouts.values() if ll.get("section_id")})
    assembly_id = p.get("assembly_id") or f"asm-{composition_id}-{now_compact()}"
    op_id = "op-asm-" + now_compact()
    manifest_core = {
        "composition_id": composition_id,
        "page_layout_ids": page_layout_ids,
        "layout_hashes": layout_hashes,
        "section_ids": section_ids,
    }
    payload = {
        "schema": "publication-assembly/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "assembly_id": assembly_id,
        "composition_id": composition_id,
        "page_layout_ids": page_layout_ids,
        "layout_hashes": layout_hashes,
        "section_ids": section_ids,
        "prior_assembly_id": p.get("prior_assembly_id"),
        "manifest_sha256": sha256_hex(json.dumps(manifest_core, sort_keys=True)),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(ASSEMBLIES_DIR, assembly_id, payload)
    append_event("publication-assembly-events", {
        "assembly_event_id": op_id,
        "kind": "register",
        "assembly_id": assembly_id,
        "composition_id": composition_id,
        "page_layout_count": len(page_layout_ids),
        "manifest_sha256": payload["manifest_sha256"],
        "prior_assembly_id": p.get("prior_assembly_id"),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "publication-assembly", "info",
               f"assembly recorded: {assembly_id}", reviewer,
               {"assembly_id": assembly_id, "manifest_sha256": payload["manifest_sha256"]})
    print(json.dumps({"ok": True, "assembly_id": assembly_id,
                      "manifest_sha256": payload["manifest_sha256"],
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_layout_review(env: dict, confirm: bool) -> int:
    p = env["payload"]
    reviewer = env["reviewer"]
    composition_id = require(p, "composition_id")
    if find_composition_record(composition_id) is None:
        raise SystemExit(f"FAIL-CLOSED: composition '{composition_id}' not found")
    decision = require(p, "decision")
    if decision not in REVIEW_DECISIONS:
        raise SystemExit(f"FAIL-CLOSED: decision '{decision}' not in {sorted(REVIEW_DECISIONS)}")
    cited = p.get("cited_rule_ids", [])
    if decision == "reject" and not (isinstance(cited, list) and cited):
        raise SystemExit("FAIL-CLOSED: reject decisions require cited_rule_ids (LR-4)")
    if attempts_overwrite_forbidden(p.get("target_path")):
        raise SystemExit("FAIL-CLOSED: target_path falls under a forbidden prefix")

    review_id = p.get("review_id") or f"lr-{composition_id}-{now_compact()}"
    op_id = "op-lreview-" + now_compact()
    payload = {
        "schema": "layout-review/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "review_id": review_id,
        "composition_id": composition_id,
        "page_index": p.get("page_index", "all"),
        "decision": decision,
        "cited_rule_ids": cited,
        "prior_decision_id": p.get("prior_decision_id"),
        "rationale": p.get("rationale", ""),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(LAYOUT_REVIEW_DIR, review_id, payload)
    write_collision_safe_json(DECISIONS_DIR, review_id + "-decision", {
        "schema": "reviewer-layout-decision/1.0",
        "review_id": review_id,
        "composition_id": composition_id,
        "decision": decision,
        "page_index": p.get("page_index", "all"),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    })
    append_event("layout-review-events", {
        "review_event_id": op_id,
        "kind": "register",
        "review_id": review_id,
        "composition_id": composition_id,
        "decision": decision,
        "page_index": p.get("page_index", "all"),
        "cited_rule_count": len(cited),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "layout-review", "info",
               f"layout review recorded: {review_id} decision={decision}", reviewer,
               {"review_id": review_id, "decision": decision})
    print(json.dumps({"ok": True, "review_id": review_id, "decision": decision,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_composition_lifecycle_transition(env: dict, confirm: bool) -> int:
    p = env["payload"]
    reviewer = env["reviewer"]
    composition_id = require(p, "composition_id")
    from_state = require(p, "from_state")
    to_state = require(p, "to_state")
    if from_state not in LIFECYCLE_STATES or to_state not in LIFECYCLE_STATES:
        raise SystemExit("FAIL-CLOSED: invalid lifecycle state(s)")
    if (from_state, to_state) not in LIFECYCLE_EDGES:
        raise SystemExit(f"FAIL-CLOSED: illegal lifecycle transition {from_state} -> {to_state} (LC-4)")
    actual = current_composition_state(composition_id)
    if actual is None:
        raise SystemExit(f"FAIL-CLOSED: composition '{composition_id}' has no recorded lifecycle (LC-4)")
    if actual != from_state:
        raise SystemExit(f"FAIL-CLOSED: declared from_state '{from_state}' != actual '{actual}' (LC-4)")
    if actual in LIFECYCLE_TERMINAL:
        raise SystemExit(f"FAIL-CLOSED: composition is in terminal state '{actual}' (LC-3)")
    if to_state == "publication-ready":
        # Require at least one passed continuity check and reviewer-approved layout review.
        approved = False
        for path in sorted(LAYOUT_REVIEW_DIR.glob("*.json")) if LAYOUT_REVIEW_DIR.exists() else []:
            try:
                d = load_json(path)
            except Exception:
                continue
            if d.get("composition_id") == composition_id and d.get("decision") == "approve":
                approved = True
                break
        if not approved:
            raise SystemExit("FAIL-CLOSED: publication-ready requires at least one approve layout-review (LC-2)")
        continuity_ok = False
        for path in sorted(CONTINUITY_DIR.glob("*.json")) if CONTINUITY_DIR.exists() else []:
            try:
                d = load_json(path)
            except Exception:
                continue
            if d.get("composition_id") == composition_id and d.get("integrity_ok"):
                continuity_ok = True
                break
        if not continuity_ok:
            raise SystemExit("FAIL-CLOSED: publication-ready requires a passing continuity scan (LC-2)")
        responsive_ok = False
        if RESPONSIVE_DIR.exists():
            for path in sorted(RESPONSIVE_DIR.glob("*.json")):
                try:
                    d = load_json(path)
                except Exception:
                    continue
                if d.get("composition_id") == composition_id and d.get("parity_ok"):
                    responsive_ok = True
                    break
        if not responsive_ok:
            raise SystemExit("FAIL-CLOSED: publication-ready requires a passing responsive parity manifest (LC-2)")
    if to_state == "superseded" and not p.get("successor_composition_id"):
        raise SystemExit("FAIL-CLOSED: publication-ready -> superseded requires successor_composition_id (LC-5)")
    if attempts_overwrite_forbidden(p.get("target_path")):
        raise SystemExit("FAIL-CLOSED: target_path falls under a forbidden prefix")

    op_id = "op-clc-" + now_compact()
    payload = {
        "schema": "composition-lifecycle-transition/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "composition_id": composition_id,
        "from_state": from_state,
        "to_state": to_state,
        "successor_composition_id": p.get("successor_composition_id"),
        "reasoning_chain": p.get("reasoning_chain", []),
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(LIFECYCLE_DIR, f"{composition_id}-{from_state}-to-{to_state}", payload)
    append_event("composition-lifecycle-events", {
        "lifecycle_event_id": op_id,
        "kind": "lifecycle-transition",
        "composition_id": composition_id,
        "from_state": from_state,
        "to_state": to_state,
        "successor_composition_id": p.get("successor_composition_id"),
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "composition-lifecycle-transition", "info",
               f"lifecycle: {composition_id} {from_state} -> {to_state}", reviewer,
               {"composition_id": composition_id})
    print(json.dumps({"ok": True, "composition_id": composition_id,
                      "from_state": from_state, "to_state": to_state,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


def handle_composition_integrity(env: dict, confirm: bool) -> int:
    p = env["payload"]
    reviewer = env["reviewer"]
    composition_id = require(p, "composition_id")
    composition = find_composition_record(composition_id)
    if composition is None:
        raise SystemExit(f"FAIL-CLOSED: composition '{composition_id}' not found")
    declared_sections = set(composition.get("section_order", []))
    layouts = list_page_layouts_for_composition(composition_id)
    findings: list[dict] = []
    section_present: set[str] = set()
    for ll in layouts:
        if ll.get("section_id"):
            section_present.add(ll["section_id"])
        # warning placement re-check
        roles = [b.get("role") for b in ll.get("blocks", [])]
        if "warning" in roles and "procedural" in roles:
            if roles.index("warning") > roles.index("procedural"):
                findings.append({"rule_id": "IN-4", "page_layout_id": ll.get("page_layout_id"),
                                 "detail": "warning placed after procedural"})
        for b in ll.get("blocks", []):
            if b.get("asset_id") and find_asset_record(b["asset_id"]) is None:
                findings.append({"rule_id": "IN-3", "page_layout_id": ll.get("page_layout_id"),
                                 "detail": f"orphan visual asset_id={b['asset_id']}"})
            if b.get("section_id"):
                section_present.add(b["section_id"])
    hidden = sorted(section_present - declared_sections)
    if hidden:
        findings.append({"rule_id": "IN-7", "detail": f"hidden sections present: {hidden}"})
    missing = sorted(declared_sections - section_present)
    if missing:
        findings.append({"rule_id": "IN-1", "detail": f"sections without lineage: {missing}"})
    # responsive parity quick scan
    if RESPONSIVE_DIR.exists():
        any_responsive = False
        any_broken = False
        for path in sorted(RESPONSIVE_DIR.glob("*.json")):
            try:
                d = load_json(path)
            except Exception:
                continue
            if d.get("composition_id") != composition_id:
                continue
            any_responsive = True
            if not d.get("parity_ok"):
                any_broken = True
        if any_responsive and any_broken:
            findings.append({"rule_id": "IN-5", "detail": "broken responsive parity present"})
    blocking = bool(findings)
    if attempts_overwrite_forbidden(p.get("target_path")):
        raise SystemExit("FAIL-CLOSED: target_path falls under a forbidden prefix")

    check_id = p.get("integrity_check_id") or f"int-{composition_id}-{now_compact()}"
    op_id = "op-int-" + now_compact()
    payload = {
        "schema": "composition-integrity/1.0",
        "constitutional_layer_index": LAYER,
        "operation_id": op_id,
        "integrity_check_id": check_id,
        "composition_id": composition_id,
        "scope": p.get("scope", "all"),
        "findings": findings,
        "blocking": blocking,
        "reviewer": reviewer,
        "recorded_at_iso": now_iso(),
        "append_only": True,
    }
    if not confirm:
        print(json.dumps({"dry_run": True, "would_record": payload}, indent=2))
        return 0
    written = write_collision_safe_json(PC_ROOT / "page-continuity", check_id + "-integrity", payload)
    append_event("composition-integrity-events", {
        "integrity_event_id": op_id,
        "kind": "register",
        "integrity_check_id": check_id,
        "composition_id": composition_id,
        "finding_count": len(findings),
        "blocking": blocking,
        "manifest_path": str(written.relative_to(REPO_ROOT)),
        "reviewer": reviewer,
        "occurred_at_iso": now_iso(),
        "append_only": True,
    })
    emit_audit(op_id, "composition-integrity", "warning" if blocking else "info",
               f"integrity scan recorded: {check_id} blocking={blocking}", reviewer,
               {"integrity_check_id": check_id, "findings": findings})
    print(json.dumps({"ok": True, "integrity_check_id": check_id,
                      "blocking": blocking, "findings": findings,
                      "manifest_path": str(written.relative_to(REPO_ROOT))}, indent=2))
    return 0


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

DISPATCH = {
    "composition-draft": handle_composition_draft,
    "page-layout": handle_page_layout,
    "multimodal-sequence": handle_multimodal_sequence,
    "responsive-layout": handle_responsive_layout,
    "page-continuity": handle_page_continuity,
    "publication-assembly": handle_publication_assembly,
    "layout-review": handle_layout_review,
    "composition-lifecycle-transition": handle_composition_lifecycle_transition,
    "composition-integrity": handle_composition_integrity,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 51 — governed publication composition CLI executor (layer 44).",
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
