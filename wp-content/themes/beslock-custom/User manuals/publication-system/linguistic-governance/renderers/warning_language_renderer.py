"""
warning_language_renderer — renders warning entities in Colombian operational
Spanish while preserving severity, irreversibility and escalation semantics.

Pure function. Does NOT mutate knowledge-core. Loads taxonomy at call time.
Returns structured payload the renderer can convert to HTML.

NOT yet wired into the publication renderer. Wiring is the next executable track.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional

_HERE = Path(__file__).resolve().parent
_TERM_ROOT = _HERE.parent / "terminology"


def _taxonomy() -> dict:
    with (_TERM_ROOT / "warnings-taxonomy.json").open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _classify(entity: dict) -> dict:
    cats = {c["id"]: c for c in _taxonomy().get("warning_classes", [])}
    if entity.get("escalation_required"):
        return cats["escalation-required"]
    if entity.get("is_irreversible"):
        return cats["irreversible-operation"]
    cat = (entity.get("category") or "").lower()
    if "battery" in cat or "bater" in cat:
        return cats["low-battery"]
    if "install" in cat:
        return cats["installation-hazard"]
    if entity.get("severity") in {"high", "medium"} and entity.get("operator_action_required"):
        return cats["operational-warning"]
    return cats["informational-note"]


def render(entity: dict) -> Dict[str, object]:
    """Return a structured Colombian-Spanish warning payload, severity preserved."""
    cls = _classify(entity)
    return {
        "warning_class_id": cls["id"],
        "label_es": cls["label_es"],
        "severity": entity.get("severity", cls.get("severity")),
        "is_irreversible": bool(entity.get("is_irreversible")),
        "operator_action_required": bool(
            entity.get("operator_action_required", cls.get("operator_action_required"))
        ),
        "consequence_es": entity.get("consequence") or entity.get("summary") or "",
        "trigger_condition_es": entity.get("trigger_condition") or "",
        "operator_action_es": entity.get("operator_action") or "",
        "escalation_required": bool(entity.get("escalation_required")),
        "render_position": cls.get("render_position", "inline-before-triggering-step"),
        "source_refs": list(entity.get("source_refs", [])),
        "preserved_from_knowledge_core": True,
    }


__all__ = ["render"]
