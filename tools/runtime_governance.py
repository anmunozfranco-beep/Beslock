#!/usr/bin/env python3
"""
Phase 20 — RUNTIME GOVERNANCE (modeling-only).

Builds the fourteenth constitutional layer:
  KNOWLEDGE_BUILDING/RUNTIME_GOVERNANCE/

Subordinate to: knowledge-core + all 13 prior governance layers.
Does NOT implement: agents, chatbots, PDFs, images, rendering runtimes,
frontends, automation runtimes, recommendation engines, reasoning engines,
persistent storage, or any executable runtime. This file ONLY describes the
strategy by which the governance stack becomes future runtime systems.
Idempotent. Non-destructive.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
THEME = REPO / "wp-content" / "themes" / "beslock-custom"
MANUALS = THEME / "User manuals"
KB = MANUALS / "KNOWLEDGE_BUILDING"
ROOT = KB / "RUNTIME_GOVERNANCE"
REPORTS = MANUALS / "_repository-governance" / "reports" / "runtime"

SCHEMA = "runtime-governance/1.0"
PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

# ---------------------------------------------------------------------------
# 1. VERTICAL SLICES
# ---------------------------------------------------------------------------
SLICE_CANDIDATES = [
    {
        "id": "onboarding-guidance",
        "value": "high",
        "risk": "medium",
        "destructive_surface": "low (no factory-reset / firmware ops)",
        "evidence_readiness": "medium (onboarding procedures present across 6/6 products)",
        "predicate_coverage": "partial (pairing/enrollment predicates declared)",
        "preferred_score": 8,
        "rationale": "high user value, mostly non-destructive, predicates partially declared, fallback registry not strictly required",
    },
    {
        "id": "procedural-retrieval",
        "value": "high",
        "risk": "low",
        "destructive_surface": "none (read-only)",
        "evidence_readiness": "high (knowledge-core nodes addressable)",
        "predicate_coverage": "n/a (no execution)",
        "preferred_score": 9,
        "rationale": "safest first runtime; pure read; activates ACCESS_AND_CONSUMPTION + COMPOSITION contracts without execution risk",
    },
    {
        "id": "contextual-operational-assembly",
        "value": "high",
        "risk": "low",
        "destructive_surface": "none (assembly only)",
        "evidence_readiness": "high",
        "predicate_coverage": "n/a (no execution)",
        "preferred_score": 8,
        "rationale": "exercises COMPOSITION + ADAPTIVE precedence without crossing execution boundaries",
    },
    {
        "id": "troubleshooting-guidance",
        "value": "high",
        "risk": "high",
        "destructive_surface": "medium (may surface escalation paths)",
        "evidence_readiness": "low (thin troubleshooting corpus on 5/6 products)",
        "predicate_coverage": "low",
        "preferred_score": 4,
        "rationale": "blocked by thin-troubleshooting-corpus + missing causal edges + missing checkpoint registry",
    },
    {
        "id": "administrator-assistance",
        "value": "medium",
        "risk": "high",
        "destructive_surface": "high (admin actions, factory-reset, delete-users)",
        "evidence_readiness": "medium",
        "predicate_coverage": "partial (factory-reset predicate declared)",
        "preferred_score": 3,
        "rationale": "destructive surface; require OEM channel + role-declaration + checkpoint registry before runtime",
    },
    {
        "id": "recovery-assistance",
        "value": "medium",
        "risk": "high",
        "destructive_surface": "medium",
        "evidence_readiness": "low",
        "predicate_coverage": "low",
        "preferred_score": 3,
        "rationale": "blocked by no-checkpoint-registry + no-causal-edges; cannot anchor recovery deterministically",
    },
]

SLICE_SELECTION = [
    "primary first slice: procedural-retrieval (read-only, lowest risk, exercises ACCESS_AND_CONSUMPTION + COMPOSITION contracts)",
    "secondary second slice: contextual-operational-assembly (still non-executive; exercises ADAPTIVE precedence and COMPOSITION rules)",
    "third slice (gated): onboarding-guidance, only after checkpoint registry + intent-declaration channel are wired",
    "deferred: troubleshooting-guidance, administrator-assistance, recovery-assistance (blocked by declared high-severity risks)",
]

SLICE_RULES = [
    "no slice is realized while any of its declared blocking-risks remains unresolved",
    "each slice declares: scope, evidence readiness, predicate coverage, destructive surface, blocking risks, exit criteria",
    "no slice may extend its surface at runtime; surface is declared at packaging time",
    "slices are read-only by default; any executive behaviour requires an explicit, governed extension",
]

# ---------------------------------------------------------------------------
# 2. RUNTIME CONTRACTS
# ---------------------------------------------------------------------------
RUNTIME_CONTRACTS = [
    {"id": "knowledge-core-access-contract", "between": ["runtime", "knowledge-core"], "operations": ["read"], "guarantees": ["addressable nodes", "verified-truth flag honoured", "OEM-required flag honoured", "no mutation"]},
    {"id": "retrieval-contract", "between": ["runtime", "ACCESS_AND_CONSUMPTION"], "operations": ["query-by-intent", "assemble-package"], "guarantees": ["declared query intents only", "stable surfaces", "consumption gates enforced"]},
    {"id": "composition-contract", "between": ["runtime", "COMPOSITION"], "operations": ["assemble", "validate-rules"], "guarantees": ["declared assembly rules", "declared primitives only", "no improvised composition"]},
    {"id": "adaptive-contract", "between": ["runtime", "ADAPTIVE_OPERATIONAL"], "operations": ["apply-context-vector", "select-adaptation"], "guarantees": ["declared triggers + effects", "precedence honoured", "non-removable safeguards"]},
    {"id": "decision-contract", "between": ["runtime", "DECISION_INTELLIGENCE"], "operations": ["select-option-at-decision-point"], "guarantees": ["declared options/predicates", "destructive requires explicit-action + role + high-confidence", "provenance emitted"]},
    {"id": "reasoning-contract", "between": ["runtime", "REASONING"], "operations": ["build-chain", "track-hypothesis"], "guarantees": ["abductive presented as 'likely'", "uncertainty propagation", "chain termination", "provenance emitted"]},
    {"id": "execution-contract", "between": ["runtime", "EXECUTION"], "operations": ["observe-state", "evaluate-predicate"], "guarantees": ["declared transitions only", "validation predicates required for completion", "destructive requires explicit-action"]},
    {"id": "continuity-contract", "between": ["runtime", "CONTINUITY"], "operations": ["snapshot-context", "restore-context", "append-history", "build-escalation-package"], "guarantees": ["append-only history", "non-inheritable destructive-confirmation", "OEM-required flag preservation"]},
    {"id": "validation-contract", "between": ["runtime", "VALIDATION"], "operations": ["read-findings", "report-runtime-events"], "guarantees": ["read-only on findings", "events feed knowledge-health intake"]},
    {"id": "lifecycle-contract", "between": ["runtime", "LIFECYCLE"], "operations": ["respect-promotion-tier"], "guarantees": ["P0 promotion requires OEM-confirmation", "no runtime promotion bypass"]},
    {"id": "experience-contract", "between": ["runtime", "EXPERIENCE"], "operations": ["read-experience-shape"], "guarantees": ["UX semantics observed; presentation never weakens safeguards"]},
    {"id": "semantic-contract", "between": ["runtime", "SEMANTIC + KNOWLEDGE_CENTER"], "operations": ["resolve-concept"], "guarantees": ["shared-concept ownership respected; cross-product collisions surface as ambiguity"]},
    {"id": "visual-contract", "between": ["runtime", "VISUAL_GOVERNANCE"], "operations": ["read-visual-spec"], "guarantees": ["visual-risk classification observed; no generation"]},
]

CONTRACT_RULES = [
    "every contract declares operations + guarantees + provenance requirements",
    "runtime may not invent operations beyond declared contracts",
    "contracts are read-only with respect to upstream layers (no upstream mutation)",
    "contract violations are runtime errors, not warnings",
    "contracts are versioned by schema; runtime pins a schema version",
]

# ---------------------------------------------------------------------------
# 3. RUNTIME BOUNDARIES
# ---------------------------------------------------------------------------
PROHIBITED_RUNTIME_BEHAVIOURS = [
    "inventing procedures, steps, warnings, or causal links",
    "elevating confidence beyond the source evidence tier",
    "suppressing irreversibility warnings or explicit-action requirements",
    "executing destructive operations without high-confidence + role + explicit-action",
    "auto-resuming destructive steps after interruption",
    "improvising a fallback when none is registered",
    "silently resolving contradictions or ambiguity",
    "modifying knowledge-core or any prior governance layer at runtime",
    "promoting any node to a higher tier (P-levels) at runtime",
    "generating images, PDFs, or rendering visual outputs",
    "acting autonomously without a declared decision point",
]

HUMAN_REVIEW_BOUNDARIES = [
    "all destructive recommendations",
    "all OEM-required resolutions",
    "all conflicting-verified-truth events",
    "all escalations to tier >= 3",
    "all promotions to verified-truth/P0 (offline pipeline only)",
    "any runtime that would surface a step not declared in canonical procedure",
]

ESCALATION_REQUIRED_STATES = [
    "ambiguous-intent on a destructive decision",
    "conflicting verified-truth on P0 procedures",
    "irrecoverable failure mid-destructive op",
    "absent fallback when canonical path is blocked",
    "missing checkpoint anchor when rollback is required",
]

UNSAFE_RUNTIME_CONSTRAINTS = [
    "no parallel destructive operations on the same device",
    "no batching across destructive boundaries",
    "no silent intent change",
    "no silent context elevation across sessions",
    "no runtime in emergency-mode beyond safety-critical surfaces",
]

AUTHORITY_LIMITATIONS = [
    "runtime cannot override knowledge-core authority",
    "runtime cannot weaken adaptive precedence",
    "runtime cannot bypass validation predicates",
    "runtime cannot expand authority-area declarations",
    "runtime cannot introduce new escalation tiers or fallback patterns",
]

# ---------------------------------------------------------------------------
# 4. EXECUTION FLOWS
# ---------------------------------------------------------------------------
EXECUTION_FLOWS = [
    {
        "id": "retrieval-execution-flow",
        "steps": ["receive query intent", "validate against declared intents", "resolve via ACCESS_AND_CONSUMPTION", "apply consumption gates", "emit retrieval provenance", "return read-only result"],
    },
    {
        "id": "contextual-assembly-execution-flow",
        "steps": ["receive request + context vector", "apply ADAPTIVE precedence", "compose via COMPOSITION rules", "validate composition", "emit assembly provenance", "return assembled package"],
    },
    {
        "id": "reasoning-invocation-flow",
        "steps": ["bind context", "open reasoning chain", "evaluate causal links + predicates", "track hypotheses", "terminate (concluded / inconclusive / escalated)", "emit chain provenance"],
    },
    {
        "id": "escalation-flow",
        "steps": ["detect trigger", "monotonic tier increment", "build escalation package via CONTINUITY", "hand off (read-only)", "append escalation-history", "emit provenance"],
    },
    {
        "id": "interruption-flow",
        "steps": ["detect interruption case", "halt destructive boundaries", "preserve checkpoints + provenance", "emit interruption event", "await resume / cancel / escalate"],
    },
    {
        "id": "continuity-restoration-flow",
        "steps": ["load context schema", "verify session+product", "re-evaluate last predicate", "re-acknowledge open warnings/escalations", "verify checkpoint anchor", "rebind hypotheses", "emit restoration provenance"],
    },
]

FLOW_RULES = [
    "every flow declares its steps; runtime may not insert undeclared steps",
    "every flow emits provenance at completion or failure",
    "flows are reproducible from declared inputs",
    "flows respect contract guarantees of the layers they invoke",
    "destructive flows always include an explicit-action step",
]

# ---------------------------------------------------------------------------
# 5. HUMAN ↔ RUNTIME INTERACTION
# ---------------------------------------------------------------------------
HUMAN_INTERACTION_MODEL = [
    {"id": "supervision-boundary", "rule": "destructive operations are supervised: explicit-action by an authorised human is mandatory"},
    {"id": "override-semantics", "rule": "human override may relax simplifying adaptations but never safety-preserving ones"},
    {"id": "escalation-handoff", "rule": "escalation handoff is human-receiving; the runtime cannot resolve OEM-required events"},
    {"id": "operator-intervention-points", "rule": "declared at: confirmation steps, ambiguity resolutions, recovery decisions, escalation tiers"},
    {"id": "approval-checkpoints", "rule": "destructive steps and irreversible operations require approval checkpoints with provenance"},
    {"id": "uncertainty-signaling", "rule": "runtime must signal confidence + disclosure to the human surface; never silently assert"},
]

INTERACTION_RULES = [
    "the runtime is supervised by default; autonomous behaviour is not modelled here",
    "humans may approve, reject, request more information, or escalate",
    "human approval is recorded with identity (when declared) and provenance",
    "human override events feed knowledge-health intake",
    "no human override may downgrade an irreversibility warning",
]

# ---------------------------------------------------------------------------
# 6. RUNTIME PACKAGING
# ---------------------------------------------------------------------------
RUNTIME_PACKAGE_TYPES = [
    {"id": "retrieval-package", "consumers": ["onboarding-systems", "troubleshooting-systems", "contextual-assistants", "operational-copilots"], "surface": "read-only"},
    {"id": "assembly-package", "consumers": ["contextual-assistants", "operational-copilots", "future-visual-assistance"], "surface": "read-only"},
    {"id": "guidance-package", "consumers": ["onboarding-copilots", "troubleshooting-assistants", "operational-copilots"], "surface": "read-only + supervised-confirmation"},
    {"id": "escalation-package", "consumers": ["support-handoff", "OEM-handoff"], "surface": "read-only snapshot"},
    {"id": "continuity-package", "consumers": ["session-aware-operational-copilots", "operational-memory-systems"], "surface": "read-only + supervised-resume"},
    {"id": "multimodal-package (gated)", "consumers": ["multimodal-runtime-systems", "future-visual-assistance"], "surface": "read-only", "gated_by": ["visual-risk reclassification freeze", "fallback registry for visual-unavailable"]},
]

PACKAGING_RULES = [
    "packages declare: surface (read-only / supervised), consumers, contracts honoured, schema version, gates",
    "packages are immutable once emitted; updates produce a new package version",
    "packages carry provenance manifests (which knowledge-core nodes contributed)",
    "packages cannot include un-promoted content beyond declared tier",
    "no package mixes read-only and executive surfaces in a single artefact",
]

# ---------------------------------------------------------------------------
# 7. EXECUTION LIFECYCLE
# ---------------------------------------------------------------------------
COGNITION_EXECUTION_LIFECYCLE = [
    {"id": "runtime-initialization", "activities": ["pin schema versions", "verify contracts available", "load declared dimensions/profiles"]},
    {"id": "context-acquisition", "activities": ["receive declared context vector", "fill missing dimensions with safest defaults", "record provenance of acquisition"]},
    {"id": "semantic-retrieval", "activities": ["resolve query intent", "fetch via knowledge-core-access-contract", "apply consumption gates"]},
    {"id": "reasoning-execution", "activities": ["build chain", "evaluate predicates + causal links", "track hypotheses", "propagate uncertainty"]},
    {"id": "decisioning", "activities": ["select among declared options at decision points", "respect prioritisation + tie-breakers", "emit decision provenance"]},
    {"id": "escalation", "activities": ["detect triggers", "build escalation package", "hand off (read-only)", "append history"]},
    {"id": "continuity-persistence", "activities": ["snapshot context", "append history", "preserve OEM-required flags", "respect non-inheritable destructive-confirmation"]},
    {"id": "runtime-completion", "activities": ["emit final provenance bundle", "close timelines", "release scoped context per declared expiry"]},
]

LIFECYCLE_RULES = [
    "lifecycle stages are declared; runtime cannot skip a stage that produced state",
    "every stage emits provenance",
    "destructive activity may only occur after decisioning has selected a destructive option with explicit-action",
    "completion requires terminal state AND validation predicate (per EXECUTION_GOVERNANCE)",
    "runtime cannot exit while any open warning or unresolved escalation remains, except by escalation-handoff",
]

# ---------------------------------------------------------------------------
# 8. CHARTER
# ---------------------------------------------------------------------------
CHARTER_PRINCIPLES = [
    "the runtime layer specifies how cognition becomes execution; it is itself modeling-only",
    "runtime is supervised by default; autonomous execution is not modelled here",
    "runtime is bounded by declared contracts with each prior layer; it may not invent operations",
    "runtime is read-only with respect to all 13 prior governance layers",
    "destructive execution requires high-confidence + role + explicit-action + provenance",
    "uncertainty, ambiguity, and contradictions are surfaced — never silently resolved",
    "irreversibility warnings and explicit-action requirements are immutable at runtime",
    "promotion (P-tiers) and authority changes are out-of-band; never at runtime",
    "all runtime activity emits provenance and may be replayed deterministically from declared inputs",
    "future runtime consumers inherit these contracts; the runtime layer never bends them for a consumer",
]

AUTHORITY_AREAS = [
    "vertical-slice selection and gating",
    "runtime contract declarations and versioning",
    "runtime boundary declarations (prohibitions / human review / escalation-required)",
    "execution flow declarations and provenance requirements",
    "human ↔ runtime interaction model",
    "runtime packaging types and immutability rules",
    "cognition execution lifecycle and stage rules",
    "supervision and override semantics",
    "schema-version pinning and contract compatibility",
    "future runtime-consumer gates",
]

# ---------------------------------------------------------------------------
# 9. UNRESOLVED RUNTIME RISKS
# ---------------------------------------------------------------------------
RUNTIME_RISKS = [
    {"id": "no-context-vector-emitter", "severity": "high", "summary": "context-acquisition stage cannot bind without an upstream emitter", "cross_ref": "adaptive + continuity"},
    {"id": "no-confidence-tier-on-nodes", "severity": "high", "summary": "uncertainty propagation, decision confidence, reasoning chains all depend on per-node confidence not yet emitted", "cross_ref": "knowledge-core/provenance"},
    {"id": "no-checkpoint-registry", "severity": "high", "summary": "interruption + recovery flows degrade to restart-from-safe-state", "cross_ref": "execution + continuity + decision"},
    {"id": "no-fallback-registry", "severity": "high", "summary": "alternative-path execution flows cannot resolve targets", "cross_ref": "adaptive + decision"},
    {"id": "no-incident-id-emitter", "severity": "high", "summary": "history queries and escalation packages cannot bind across sessions", "cross_ref": "continuity"},
    {"id": "no-provenance-emitter", "severity": "high", "summary": "runtime requires upstream provenance emission for replay determinism", "cross_ref": "execution/snapshot-hash + decision + reasoning + continuity"},
    {"id": "thin-troubleshooting-corpus", "severity": "high", "summary": "guidance-package for troubleshooting cannot be released on 5/6 products", "cross_ref": "validation/maturity"},
    {"id": "warning-corpus-gap", "severity": "high", "summary": "mandatory-warning surface cannot fire on 2 products at runtime", "cross_ref": "validation/warnings"},
    {"id": "oem-channel-contract-missing", "severity": "high", "summary": "tier-4/5 handoff cannot complete without OEM channel contract", "cross_ref": "decision/escalation + continuity/handoff"},
    {"id": "no-causal-edges-emitted", "severity": "medium", "summary": "reasoning-invocation flow degrades when causal edges are not addressable", "cross_ref": "reasoning/causality"},
    {"id": "no-hypothesis-store", "severity": "medium", "summary": "reasoning flow cannot persist hypotheses across resume", "cross_ref": "reasoning/hypothesis-tracking"},
    {"id": "schema-version-pinning-not-enforced", "severity": "medium", "summary": "runtime must pin schema versions; no upstream pin contract yet", "cross_ref": "this layer / contracts"},
]

# ---------------------------------------------------------------------------
# 10. FUTURE READINESS / FIRST-RUNTIME ASSESSMENT
# ---------------------------------------------------------------------------
FUTURE_RUNTIME_CONSUMERS = [
    {"id": "onboarding-copilot", "gates": ["context-vector emitter", "intent declaration channel", "checkpoint registry on onboarding", "predicate coverage on pairing+enrollment", "provenance emitter"]},
    {"id": "troubleshooting-assistant", "gates": ["symptom corpus >= 10/product", "causal edges emitted", "hypothesis store contract", "branch provenance log"]},
    {"id": "contextual-operational-assistant", "gates": ["context-vector emitter", "decision provenance log", "reasoning provenance log", "fallback registry"]},
    {"id": "multimodal-runtime-system", "gates": ["visual-risk reclassification freeze", "visual-intent attached to physical-installation", "evidence-disclosure renderer contract"]},
    {"id": "future-visual-assistance", "gates": ["visual-risk reclassification freeze", "fallback registry for visual-unavailable contexts"]},
    {"id": "adaptive-operational-runtime", "gates": ["context store contract", "session-signal emitter", "OEM channel contract", "all four 'high' runtime risks resolved for the chosen slice"]},
]

FIRST_RUNTIME_READINESS = {
    "primary_first_slice": "procedural-retrieval",
    "rationale": "read-only; no destructive surface; activates ACCESS_AND_CONSUMPTION + COMPOSITION + CONTINUITY (snapshot only) without execution risk",
    "blocking_risks_for_primary": [],
    "soft_risks_for_primary": ["no-provenance-emitter (degrades replay determinism but does not block read-only retrieval)"],
    "exit_criteria": [
        "declared query intents resolvable",
        "stable surfaces enumerated",
        "consumption gates enforceable read-side",
        "provenance manifest attached to each retrieval-package",
    ],
    "secondary_slice": "contextual-operational-assembly",
    "blocking_risks_for_secondary": ["no-context-vector-emitter (degraded mode possible: use safest defaults)"],
    "deferred_slices": ["onboarding-guidance", "troubleshooting-guidance", "administrator-assistance", "recovery-assistance"],
    "deferred_blocking_summary": [
        "onboarding-guidance: requires checkpoint registry + intent declaration + predicate coverage",
        "troubleshooting-guidance: requires symptom corpus >= 10/product + causal edges + hypothesis store",
        "administrator-assistance: requires OEM channel contract + role declaration + checkpoint registry",
        "recovery-assistance: requires checkpoint registry + causal edges + hypothesis store",
    ],
    "doctrine": "no slice is realised while any declared blocking-risk for that slice remains unresolved",
}

# ---------------------------------------------------------------------------
# WRITERS
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_pair(folder: Path, slug: str, title: str, body_md: str, payload: dict) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{slug}.md").write_text(f"# {title}\n\n{body_md}\n", encoding="utf-8")
    payload = {"schema": SCHEMA, "generated_at": now_iso(), **payload}
    (folder / f"{slug}.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def md_list(items, key=None):
    out = []
    for it in items:
        if isinstance(it, dict):
            label = it.get(key) if key else (it.get("id") or it.get("rule") or json.dumps(it))
            extras = {k: v for k, v in it.items() if k != key}
            if extras:
                out.append(f"- **{label}** — {json.dumps(extras, ensure_ascii=False)}")
            else:
                out.append(f"- **{label}**")
        else:
            out.append(f"- {it}")
    return "\n".join(out)


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    (ROOT / "README.md").write_text(
        "# RUNTIME_GOVERNANCE\n\n"
        "Fourteenth constitutional layer — **modeling-only**.\n\n"
        "Specifies the strategy by which the governance stack becomes future runtime "
        "systems. The runtime layer is itself modeling-only; it does not execute. It "
        "declares vertical slices, contracts with each prior layer, runtime boundaries, "
        "execution flows, the human ↔ runtime interaction model, packaging strategy, "
        "the cognition execution lifecycle, supervision/override semantics, and the gates "
        "that future runtime consumers must pass.\n\n"
        "Subordinate to: knowledge-core, VISUAL, KNOWLEDGE_CENTER, SEMANTIC, EXPERIENCE, "
        "LIFECYCLE, VALIDATION, ACCESS_AND_CONSUMPTION, COMPOSITION, EXECUTION, "
        "ADAPTIVE_OPERATIONAL, DECISION_INTELLIGENCE, REASONING, CONTINUITY.\n\n"
        "Excludes: chatbots, frontends, PDFs, image generation, rendering runtimes, "
        "agents, autonomous execution, recommendation engines, autonomous reasoning "
        "engines, persistent storage implementations.\n",
        encoding="utf-8",
    )

    write_pair(
        ROOT, "00-charter", "Runtime Governance — Charter",
        "## Principles\n\n" + md_list(CHARTER_PRINCIPLES) +
        "\n\n## Authority Areas\n\n" + md_list(AUTHORITY_AREAS),
        {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS},
    )

    write_pair(
        ROOT / "vertical-slices", "vertical-slices", "Vertical Slice Identification",
        "## Candidates\n\n" + md_list(SLICE_CANDIDATES, key="id") +
        "\n\n## Selection\n\n" + md_list(SLICE_SELECTION) +
        "\n\n## Rules\n\n" + md_list(SLICE_RULES),
        {"candidates": SLICE_CANDIDATES, "selection": SLICE_SELECTION, "rules": SLICE_RULES},
    )

    write_pair(
        ROOT / "runtime-contracts", "runtime-contracts", "Runtime Contracts",
        "## Contracts\n\n" + md_list(RUNTIME_CONTRACTS, key="id") +
        "\n\n## Rules\n\n" + md_list(CONTRACT_RULES),
        {"contracts": RUNTIME_CONTRACTS, "rules": CONTRACT_RULES},
    )

    write_pair(
        ROOT / "runtime-boundaries", "runtime-boundaries", "Runtime Boundaries",
        "## Prohibited Behaviours\n\n" + md_list(PROHIBITED_RUNTIME_BEHAVIOURS) +
        "\n\n## Human-Review Boundaries\n\n" + md_list(HUMAN_REVIEW_BOUNDARIES) +
        "\n\n## Escalation-Required States\n\n" + md_list(ESCALATION_REQUIRED_STATES) +
        "\n\n## Unsafe-Runtime Constraints\n\n" + md_list(UNSAFE_RUNTIME_CONSTRAINTS) +
        "\n\n## Authority Limitations\n\n" + md_list(AUTHORITY_LIMITATIONS),
        {
            "prohibited_behaviours": PROHIBITED_RUNTIME_BEHAVIOURS,
            "human_review_boundaries": HUMAN_REVIEW_BOUNDARIES,
            "escalation_required_states": ESCALATION_REQUIRED_STATES,
            "unsafe_runtime_constraints": UNSAFE_RUNTIME_CONSTRAINTS,
            "authority_limitations": AUTHORITY_LIMITATIONS,
        },
    )

    write_pair(
        ROOT / "execution-flows", "execution-flows", "Contextual Execution Flows",
        "## Flows\n\n" + md_list(EXECUTION_FLOWS, key="id") +
        "\n\n## Rules\n\n" + md_list(FLOW_RULES),
        {"flows": EXECUTION_FLOWS, "rules": FLOW_RULES},
    )

    write_pair(
        ROOT / "human-runtime-interaction", "human-runtime-interaction", "Human ↔ Runtime Interaction Model",
        "## Model\n\n" + md_list(HUMAN_INTERACTION_MODEL, key="id") +
        "\n\n## Rules\n\n" + md_list(INTERACTION_RULES),
        {"model": HUMAN_INTERACTION_MODEL, "rules": INTERACTION_RULES},
    )

    write_pair(
        ROOT / "runtime-packaging", "runtime-packaging", "Runtime Packaging Strategy",
        "## Package Types\n\n" + md_list(RUNTIME_PACKAGE_TYPES, key="id") +
        "\n\n## Rules\n\n" + md_list(PACKAGING_RULES),
        {"package_types": RUNTIME_PACKAGE_TYPES, "rules": PACKAGING_RULES},
    )

    write_pair(
        ROOT / "execution-lifecycle", "execution-lifecycle", "Cognition Execution Lifecycle",
        "## Stages\n\n" + md_list(COGNITION_EXECUTION_LIFECYCLE, key="id") +
        "\n\n## Rules\n\n" + md_list(LIFECYCLE_RULES),
        {"stages": COGNITION_EXECUTION_LIFECYCLE, "rules": LIFECYCLE_RULES},
    )

    write_pair(
        ROOT / "runtime-risks", "runtime-risks", "Unresolved Runtime Risks",
        md_list(RUNTIME_RISKS, key="id"),
        {"risks": RUNTIME_RISKS},
    )

    write_pair(
        ROOT / "future-readiness", "future-readiness", "Future Runtime Readiness",
        "## Future Consumers\n\n" + md_list(FUTURE_RUNTIME_CONSUMERS, key="id") +
        "\n\n## First-Runtime Assessment\n\n```json\n" + json.dumps(FIRST_RUNTIME_READINESS, indent=2, ensure_ascii=False) + "\n```",
        {"future_consumers": FUTURE_RUNTIME_CONSUMERS, "first_runtime_readiness": FIRST_RUNTIME_READINESS, "products": PRODUCTS},
    )

    reports = [
        ("01-vertical-slice-summary.json", {"candidates": SLICE_CANDIDATES, "selection": SLICE_SELECTION, "rules": SLICE_RULES}),
        ("02-runtime-contract-summary.json", {"contracts": RUNTIME_CONTRACTS, "rules": CONTRACT_RULES, "count": len(RUNTIME_CONTRACTS)}),
        ("03-runtime-boundary-summary.json", {"prohibited_behaviours": PROHIBITED_RUNTIME_BEHAVIOURS, "human_review_boundaries": HUMAN_REVIEW_BOUNDARIES, "escalation_required_states": ESCALATION_REQUIRED_STATES, "unsafe_runtime_constraints": UNSAFE_RUNTIME_CONSTRAINTS, "authority_limitations": AUTHORITY_LIMITATIONS}),
        ("04-execution-flow-summary.json", {"flows": EXECUTION_FLOWS, "rules": FLOW_RULES}),
        ("05-human-runtime-summary.json", {"model": HUMAN_INTERACTION_MODEL, "rules": INTERACTION_RULES}),
        ("06-runtime-packaging-summary.json", {"package_types": RUNTIME_PACKAGE_TYPES, "rules": PACKAGING_RULES}),
        ("07-execution-lifecycle-summary.json", {"stages": COGNITION_EXECUTION_LIFECYCLE, "rules": LIFECYCLE_RULES}),
        ("08-runtime-governance-summary.json", {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS}),
        ("09-unresolved-runtime-risks.json", {"risks": RUNTIME_RISKS, "count": len(RUNTIME_RISKS), "high_count": sum(1 for r in RUNTIME_RISKS if r["severity"] == "high")}),
        ("10-first-runtime-readiness.json", {"first_runtime_readiness": FIRST_RUNTIME_READINESS, "future_consumers": FUTURE_RUNTIME_CONSUMERS}),
    ]
    for name, payload in reports:
        out = {"schema": SCHEMA, "generated_at": now_iso(), **payload}
        (REPORTS / name).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Runtime realization strategy modeling complete.")
    print(f"  Constitutional root: {ROOT.relative_to(REPO)}")
    print(f"  Reports:             {REPORTS.relative_to(REPO)}/01..10")
    print(f"  Slices: {len(SLICE_CANDIDATES)} | Contracts: {len(RUNTIME_CONTRACTS)} | Flows: {len(EXECUTION_FLOWS)} | Lifecycle stages: {len(COGNITION_EXECUTION_LIFECYCLE)} | Package types: {len(RUNTIME_PACKAGE_TYPES)} | Risks: {len(RUNTIME_RISKS)} (high: {sum(1 for r in RUNTIME_RISKS if r['severity']=='high')})")
    print(f"  First runtime: {FIRST_RUNTIME_READINESS['primary_first_slice']}")


if __name__ == "__main__":
    main()
