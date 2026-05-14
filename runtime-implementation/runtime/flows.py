"""Six declared supervised flows.

Each flow:
  1. Builds retrieval-package(s) for the slice's primary + warning + troubleshooting kinds.
  2. Assembles a contextual assembly-package.
  3. Emits trace events to observability.
  4. Halts at the pre-emission checkpoint and waits for operator approval.
  5. Evaluates safety predicates; demotes the slice on any failure.
  6. Emits a guidance-package only after approval + safety-pass.

This is a real, modeling-aligned, supervised executable runtime — not a chatbot,
not an autonomous agent, not a production system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from . import assembly, observability, provenance, retrieval, safety, supervision


FLOW_KINDS: dict[str, dict] = {
    "onboarding":              {"primary": "onboarding",            "warnings": "warnings", "troubleshooting": None},
    "first-pairing":           {"primary": "pairing",               "warnings": "warnings", "troubleshooting": None},
    "fingerprint-enrollment":  {"primary": "fingerprint-enrollment","warnings": "warnings", "troubleshooting": None},
    "troubleshooting-lookup":  {"primary": "troubleshooting",       "warnings": "warnings", "troubleshooting": "troubleshooting"},
    "battery-recovery":        {"primary": "battery-recovery",      "warnings": "warnings", "troubleshooting": "troubleshooting"},
    "escalation-handling":     {"primary": "escalation",            "warnings": "warnings", "troubleshooting": "troubleshooting"},
}


@dataclass
class FlowResult:
    run_id: str
    slice_id: str
    flow: str
    product: str
    query: str
    retrieval_package: dict
    warning_package: dict
    troubleshooting_package: dict
    assembly_package: dict
    safety_report: dict
    pre_emission_receipt: dict
    guidance_package: dict | None
    demoted: bool
    demote_reasons: list[str]


def run_flow(
    *,
    flow: str,
    product: str,
    query: str,
    operator: str = "operator-cli",
    auto_decision: str | None = None,
    supervise_prompt: Callable[[str, dict], tuple[str, str]] | None = None,
) -> FlowResult:
    if flow not in FLOW_KINDS:
        raise ValueError(f"unknown flow: {flow}")

    kinds = FLOW_KINDS[flow]
    run_id = provenance.new_id("run")
    slice_id = provenance.new_id("slice")

    observability.emit("orchestration-trace", {
        "kind": "flow-start", "run_id": run_id, "slice_id": slice_id,
        "flow": flow, "product": product, "query": query, "operator": operator,
    })

    primary_pkg = retrieval.retrieve(run_id=run_id, slice_id=slice_id, product=product,
                                     query=query, kind=kinds["primary"])
    observability.emit("retrieval-trace", {
        "kind": "retrieval-package", "run_id": run_id,
        "package": retrieval.package_to_dict(primary_pkg),
    })

    warning_pkg = retrieval.retrieve(run_id=run_id, slice_id=slice_id, product=product,
                                     query=query, kind=kinds["warnings"])
    observability.emit("retrieval-trace", {
        "kind": "warning-package", "run_id": run_id,
        "package": retrieval.package_to_dict(warning_pkg),
    })

    if kinds["troubleshooting"]:
        ts_pkg = retrieval.retrieve(run_id=run_id, slice_id=slice_id, product=product,
                                    query=query, kind=kinds["troubleshooting"])
    else:
        ts_pkg = retrieval.RetrievalPackage(
            package_id=provenance.new_id("retr"), run_id=run_id, slice_id=slice_id,
            query=query, kind="troubleshooting", product=product, nodes=[],
            manifest=provenance.build_manifest(run_id=run_id, slice_id=slice_id,
                                               package_kind="retrieval-package",
                                               source_files=[], source_node_ids=[],
                                               extra={"empty": True, "kind": "troubleshooting"}),
            ambiguous=False, no_results=True,
        )
    observability.emit("retrieval-trace", {
        "kind": "troubleshooting-package", "run_id": run_id,
        "package": retrieval.package_to_dict(ts_pkg),
    })

    asm = assembly.assemble(run_id=run_id, slice_id=slice_id,
                            procedure_pkg=primary_pkg,
                            warning_pkg=warning_pkg,
                            troubleshooting_pkg=ts_pkg)
    observability.emit("reasoning-trace", {
        "kind": "assembly-package", "run_id": run_id,
        "package": assembly.assembly_to_dict(asm),
    })
    observability.emit("escalation-trace", {
        "kind": "escalation-evaluation", "run_id": run_id,
        "result": asm.escalation_predicate_result,
    })
    observability.emit("continuity-trace", {
        "kind": "continuity-snapshot", "run_id": run_id,
        "state": asm.continuity_state,
    })

    safety_report = safety.evaluate(asm)
    observability.emit("reasoning-trace", {
        "kind": "safety-report", "run_id": run_id, "report": safety_report,
    })

    pre_emission_summary = {
        "flow": flow, "product": product, "primary_kind": asm.primary_kind,
        "procedure_nodes": [n.id for n in asm.procedure_nodes],
        "warning_nodes": [n.id for n in asm.warning_nodes],
        "troubleshooting_nodes": [n.id for n in asm.troubleshooting_nodes],
        "blockers": asm.blockers,
        "escalation_tier": asm.escalation_predicate_result.get("tier"),
        "safety_failed": safety_report["failed"],
    }
    receipt = supervision.supervise(
        run_id=run_id, slice_id=slice_id,
        checkpoint="pre-emission",
        payload_summary=pre_emission_summary,
        operator=operator,
        auto_decision=auto_decision,
        prompt=supervise_prompt,
    )
    observability.emit("operational-audit-log", {
        "kind": "supervision-receipt", "run_id": run_id, "receipt": receipt.to_dict(),
    })

    demote_reasons: list[str] = []
    if safety_report["demote"]:
        demote_reasons.append("safety-predicate-failure")
    if asm.blockers:
        demote_reasons.append("assembly-blockers-present")
    if supervision.is_blocking(receipt.decision):
        demote_reasons.append(f"operator-{receipt.decision}")
    if not supervision.is_advancing(receipt.decision):
        demote_reasons.append(f"operator-{receipt.decision}")

    guidance_package: dict | None = None
    demoted = bool(demote_reasons)
    if not demoted:
        guidance_package = {
            "package_id": provenance.new_id("gui"),
            "run_id": run_id,
            "slice_id": slice_id,
            "flow": flow,
            "product": product,
            "primary_kind": asm.primary_kind,
            "guidance_summary": asm.procedure_nodes[0].summary if asm.procedure_nodes else "",
            "ordered_node_ids": [n.id for n in asm.procedure_nodes],
            "warning_node_ids": [n.id for n in asm.warning_nodes],
            "troubleshooting_node_ids": [n.id for n in asm.troubleshooting_nodes],
            "confidence_disclosed": asm.procedure_nodes[0].confidence if asm.procedure_nodes else "unknown",
            "manifest": provenance.build_manifest(
                run_id=run_id, slice_id=slice_id, package_kind="guidance-package",
                source_files=[n.path for n in asm.procedure_nodes],
                source_node_ids=[n.id for n in asm.procedure_nodes],
                extra={"flow": flow, "supervision_receipt_id": receipt.receipt_id},
            ),
        }
        observability.emit("operational-audit-log", {
            "kind": "guidance-package", "run_id": run_id, "package": guidance_package,
        })

    observability.emit("orchestration-trace", {
        "kind": "flow-end", "run_id": run_id, "slice_id": slice_id, "flow": flow,
        "demoted": demoted, "demote_reasons": demote_reasons,
    })

    return FlowResult(
        run_id=run_id, slice_id=slice_id, flow=flow, product=product, query=query,
        retrieval_package=retrieval.package_to_dict(primary_pkg),
        warning_package=retrieval.package_to_dict(warning_pkg),
        troubleshooting_package=retrieval.package_to_dict(ts_pkg),
        assembly_package=assembly.assembly_to_dict(asm),
        safety_report=safety_report,
        pre_emission_receipt=receipt.to_dict(),
        guidance_package=guidance_package,
        demoted=demoted,
        demote_reasons=demote_reasons,
    )
