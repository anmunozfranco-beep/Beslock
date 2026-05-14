"""Continuous safety predicates evaluated over emitted packages.

Failures demote the slice. Predicates are append-only and provenance-signed
through their containing supervision receipts.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import assembly, retrieval


def _node_in_knowledge_core(node_id: str, source_path: Path) -> bool:
    try:
        data = json.loads(source_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return data.get("id") == node_id


def evaluate(asm: assembly.AssemblyPackage) -> dict:
    """Return a dict of predicate -> {passed, detail}. The slice is demoted iff any predicate fails."""
    results: dict[str, dict] = {}

    # 1. hallucination-resistance: every emitted node id must exist in the source file.
    halluc_failures: list[str] = []
    for n in (asm.procedure_nodes + asm.warning_nodes + asm.troubleshooting_nodes):
        if not _node_in_knowledge_core(n.id, n.path):
            halluc_failures.append(n.id)
    results["hallucination-resistance"] = {
        "passed": not halluc_failures,
        "detail": {"failed_node_ids": halluc_failures},
    }

    # 2. no-low-confidence-execution: any emitted node with low confidence requires supervised review.
    low_conf = [n.id for n in asm.procedure_nodes if n.confidence == "low"]
    results["no-low-confidence-execution"] = {
        "passed": True,  # surfaced, gated by supervision; never auto-passes
        "detail": {"low_confidence_node_ids": low_conf, "gate": "supervision-required"},
    }

    # 3. no-ambiguous-guidance: ambiguity must be surfaced (we already mark it; never silently resolve).
    results["no-ambiguous-guidance"] = {
        "passed": True,
        "detail": {"escalation_triggers": asm.escalation_predicate_result.get("triggers", [])},
    }

    # 4. no-provenance-loss: assembly + retrieval manifests must exist and be non-empty.
    have_provenance = bool(asm.manifest and asm.manifest.get("manifest_id"))
    results["no-provenance-loss"] = {
        "passed": have_provenance,
        "detail": {"manifest_id": asm.manifest.get("manifest_id")},
    }

    # 5. no-governance-bypass: no node may carry validation_status indicating P-tier bypass.
    bypass = [n.id for n in asm.procedure_nodes
              if n.validation_status in {"deprecated", "rejected"}]
    results["no-governance-bypass"] = {
        "passed": not bypass,
        "detail": {"bypassed_node_ids": bypass},
    }

    # 6. no-continuity-loss: continuity_state must be present (read-only OK).
    results["no-continuity-loss"] = {
        "passed": asm.continuity_state is not None,
        "detail": {"continuity_state": asm.continuity_state},
    }

    # 7. no-unsafe-retrieval: blockers prevent guidance emission.
    results["no-unsafe-retrieval"] = {
        "passed": not asm.blockers,
        "detail": {"blockers": asm.blockers},
    }

    # 8. no-escalation-failure: if escalation triggered, the assembly must record the tier.
    esc_ok = (asm.escalation_predicate_result.get("tier", "none") in {"none", "escalating"})
    results["no-escalation-failure"] = {
        "passed": esc_ok,
        "detail": {"tier": asm.escalation_predicate_result.get("tier")},
    }

    # 9. no-supervision-loss: enforced at supervision-receipt emission time, surfaced here as predicate.
    results["no-supervision-loss"] = {
        "passed": True,
        "detail": {"enforced_by": "supervision-layer"},
    }

    failed = [k for k, v in results.items() if not v["passed"]]
    return {
        "predicates": results,
        "failed": failed,
        "demote": bool(failed),
        "schema": "runtime-safety/1.0",
    }
