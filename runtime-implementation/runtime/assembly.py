"""Contextual assembly — merges procedures, warnings, prerequisites, troubleshooting,
escalation, continuity-state, adaptive-guidance into a bound assembly-package.

Mandatory warnings cannot be suppressed. Prerequisite gaps block emission.
Adaptive precedence (knowledge-core > adaptive) is invariant. No mutations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from . import provenance, retrieval


@dataclass
class AssemblyPackage:
    package_id: str
    run_id: str
    slice_id: str
    primary_kind: str
    procedure_nodes: list[retrieval.RetrievedNode]
    warning_nodes: list[retrieval.RetrievedNode]
    prerequisite_records: list[dict]
    troubleshooting_nodes: list[retrieval.RetrievedNode]
    escalation_predicate_result: dict
    continuity_state: dict
    adaptation_record: dict
    manifest: dict
    blockers: list[str] = field(default_factory=list)


def _extract_prereqs(nodes: Iterable[retrieval.RetrievedNode]) -> list[dict]:
    out: list[dict] = []
    for n in nodes:
        for pre in n.raw.get("preconditions", []) or []:
            if isinstance(pre, dict):
                out.append({"node_id": n.id, "text": pre.get("text", ""), "verified": pre.get("verified", False)})
            elif isinstance(pre, str):
                out.append({"node_id": n.id, "text": pre, "verified": False})
    return out


def _evaluate_escalation(procedure_pkg: retrieval.RetrievalPackage,
                         warning_pkg: retrieval.RetrievalPackage,
                         troubleshooting_pkg: retrieval.RetrievalPackage) -> dict:
    triggers: list[str] = []
    if procedure_pkg.no_results:
        triggers.append("no-procedure-retrievable")
    if procedure_pkg.ambiguous:
        triggers.append("procedure-ambiguity")
    if warning_pkg.no_results and procedure_pkg.kind in {"battery-recovery", "fingerprint-enrollment", "pairing"}:
        triggers.append("warning-corpus-gap")
    if troubleshooting_pkg.kind == "troubleshooting" and troubleshooting_pkg.no_results:
        triggers.append("thin-troubleshooting-corpus")
    # Candidate-only retrieval is treated as a soft escalation signal.
    if procedure_pkg.manifest.get("extra", {}).get("candidate_only"):
        triggers.append("procedure-candidate-only")
    if troubleshooting_pkg.manifest.get("extra", {}).get("candidate_only"):
        triggers.append("troubleshooting-candidate-only")
    return {
        "tier": "escalating" if triggers else "none",
        "triggers": triggers,
        "monotonic": True,
    }


def assemble(
    *,
    run_id: str,
    slice_id: str,
    procedure_pkg: retrieval.RetrievalPackage,
    warning_pkg: retrieval.RetrievalPackage,
    troubleshooting_pkg: retrieval.RetrievalPackage,
    continuity_state: dict | None = None,
    adaptation_record: dict | None = None,
) -> AssemblyPackage:
    continuity_state = continuity_state or {"timeline_id": None, "checkpoint_id": None,
                                            "context_vector_present": False}
    adaptation_record = adaptation_record or {"profile": "safest-default",
                                              "precedence": "knowledge-core>adaptive",
                                              "elevated_confidence": False}

    prereqs = _extract_prereqs(procedure_pkg.nodes)

    blockers: list[str] = []
    # Mandatory warnings cannot be suppressed: if procedure exists but warnings empty,
    # we mark a blocker for affected destructive-adjacent kinds.
    if procedure_pkg.kind in {"battery-recovery", "fingerprint-enrollment", "pairing"} \
            and warning_pkg.no_results:
        blockers.append("mandatory-warning-not-attached")
    if procedure_pkg.no_results:
        blockers.append("no-procedure-retrievable")
    if any(p["text"] and not p["verified"] for p in prereqs):
        blockers.append("prerequisite-unverified")
    if adaptation_record.get("elevated_confidence"):
        blockers.append("confidence-elevated-unsafe")

    esc = _evaluate_escalation(procedure_pkg, warning_pkg, troubleshooting_pkg)

    source_files = (
        [n.path for n in procedure_pkg.nodes]
        + [n.path for n in warning_pkg.nodes]
        + [n.path for n in troubleshooting_pkg.nodes]
    )
    source_ids = (
        [n.id for n in procedure_pkg.nodes]
        + [n.id for n in warning_pkg.nodes]
        + [n.id for n in troubleshooting_pkg.nodes]
    )
    manifest = provenance.build_manifest(
        run_id=run_id, slice_id=slice_id, package_kind="assembly-package",
        source_files=source_files, source_node_ids=source_ids,
        extra={"primary_kind": procedure_pkg.kind, "blockers": blockers,
               "escalation_tier": esc["tier"]},
    )

    return AssemblyPackage(
        package_id=provenance.new_id("asm"),
        run_id=run_id,
        slice_id=slice_id,
        primary_kind=procedure_pkg.kind,
        procedure_nodes=procedure_pkg.nodes,
        warning_nodes=warning_pkg.nodes,
        prerequisite_records=prereqs,
        troubleshooting_nodes=troubleshooting_pkg.nodes,
        escalation_predicate_result=esc,
        continuity_state=continuity_state,
        adaptation_record=adaptation_record,
        manifest=manifest,
        blockers=blockers,
    )


def assembly_to_dict(asm: AssemblyPackage) -> dict:
    return {
        "package_id": asm.package_id,
        "run_id": asm.run_id,
        "slice_id": asm.slice_id,
        "primary_kind": asm.primary_kind,
        "procedure_node_ids": [n.id for n in asm.procedure_nodes],
        "warning_node_ids": [n.id for n in asm.warning_nodes],
        "troubleshooting_node_ids": [n.id for n in asm.troubleshooting_nodes],
        "prerequisite_records": asm.prerequisite_records,
        "escalation_predicate_result": asm.escalation_predicate_result,
        "continuity_state": asm.continuity_state,
        "adaptation_record": asm.adaptation_record,
        "blockers": asm.blockers,
        "manifest": asm.manifest,
    }
