#!/usr/bin/env python3
"""
Phase 17 — DECISION INTELLIGENCE GOVERNANCE (modeling-only).

Builds the eleventh constitutional layer:
  KNOWLEDGE_BUILDING/DECISION_INTELLIGENCE_GOVERNANCE/

Subordinate to: knowledge-core + all 10 prior governance layers.
Does NOT implement: chatbots, PDFs, images, rendering runtimes, frontends,
automation runtimes, or recommendation engines.
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
ROOT = KB / "DECISION_INTELLIGENCE_GOVERNANCE"
REPORTS = MANUALS / "_repository-governance" / "reports" / "decision"

SCHEMA = "decision-intelligence-governance/1.0"
PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

# ---------------------------------------------------------------------------
# 1. DECISION POINTS
# ---------------------------------------------------------------------------
DECISION_POINTS = [
    {"id": "retry-vs-recovery", "context": "after validation-failure or step-failure", "options": ["retry-same-step", "enter-recovery"], "default": "retry-same-step (capped by retry-threshold)"},
    {"id": "reset-vs-troubleshooting", "context": "persistent failure with available troubleshooting paths", "options": ["troubleshoot-first", "factory-reset"], "default": "troubleshoot-first (factory-reset only as last resort, administrator-only)"},
    {"id": "administrator-vs-beginner-flow", "context": "step requires elevated authority", "options": ["beginner-flow", "administrator-flow"], "default": "role-gated (no silent elevation)"},
    {"id": "degraded-vs-escalation", "context": "environment or evidence prevents canonical path", "options": ["registered-fallback", "escalate"], "default": "registered-fallback if present; otherwise escalate"},
    {"id": "safe-continue-vs-interrupt", "context": "warning surfaced mid-procedure", "options": ["continue-with-acknowledgement", "interrupt-and-recover"], "default": "interrupt-and-recover when severity >= warning"},
    {"id": "local-recovery-vs-oem", "context": "irrecoverable or vendor-bound failure", "options": ["local-recovery", "oem-intervention"], "default": "oem-intervention for irrecoverable / firmware-bricked"},
    {"id": "manual-vs-electronic-path", "context": "electronic path unavailable AND manual fallback registered", "options": ["manual-fallback", "wait-and-retry"], "default": "manual-fallback when registered"},
    {"id": "verified-vs-inferred-claim", "context": "guidance must produce a claim", "options": ["assert-verified", "downgrade-to-likely", "withhold"], "default": "downgrade-to-likely or withhold based on confidence tier"},
    {"id": "cancel-vs-rollback", "context": "user-cancel mid-procedure", "options": ["cancel-no-state-change", "rollback-to-checkpoint"], "default": "rollback-to-checkpoint when checkpoints exist"},
    {"id": "single-attempt-vs-batch", "context": "non-destructive sequence with installer/admin role", "options": ["per-step", "batched"], "default": "batched only for non-destructive declared sequences"},
    {"id": "ask-disambiguation-vs-proceed", "context": "intent-clarity in {ambiguous,missing}", "options": ["ask-disambiguation", "proceed-with-default"], "default": "ask-disambiguation (no silent default for destructive ops)"},
]

DECISION_POINT_RULES = [
    "every decision point declares its options, default, and selection predicate",
    "no decision point has an undeclared 'else' path",
    "destructive decisions require explicit-action; never selected silently",
    "decision outputs are observable and provenance-tagged",
    "decision points cannot bypass validation predicates of the underlying procedure",
]

# ---------------------------------------------------------------------------
# 2. BRANCHING SEMANTICS
# ---------------------------------------------------------------------------
BRANCH_TYPES = [
    {"id": "procedural", "description": "branch declared inside a canonical procedure"},
    {"id": "conditional", "description": "branch driven by a declared boolean predicate over context vector"},
    {"id": "context-driven", "description": "branch selected from observed context dimensions"},
    {"id": "failure-driven", "description": "branch entered after a declared failure class"},
    {"id": "recovery", "description": "branch entered to restore a safe state"},
    {"id": "escalation", "description": "branch that hands off to a higher tier or OEM"},
    {"id": "ambiguity-driven", "description": "branch entered to resolve an ambiguous input"},
]

BRANCHING_RULES = [
    "branches are declared, not invented at runtime",
    "branch selection is deterministic given the context vector",
    "each branch carries provenance (which input(s) selected it)",
    "branches preserve safeguards from the parent procedure",
    "branch transitions never silently change user intent",
    "branches must terminate (no infinite loops; cap by retry thresholds)",
]

BRANCH_OUTCOMES = [
    "completed", "alternative-completed", "fallback-completed",
    "interrupted", "blocked", "escalated", "abandoned",
]

# ---------------------------------------------------------------------------
# 3. DECISION CONFIDENCE
# ---------------------------------------------------------------------------
CONFIDENCE_LEVELS = [
    {"id": "high", "evidence_basis": "verified-truth", "may_drive_destructive": True, "presentation": "assert"},
    {"id": "medium", "evidence_basis": "inferred from verified inputs", "may_drive_destructive": False, "presentation": "suggest"},
    {"id": "low", "evidence_basis": "ocr-derived or partial", "may_drive_destructive": False, "presentation": "downgrade-to-likely"},
    {"id": "ambiguous", "evidence_basis": "conflicting / unresolved", "may_drive_destructive": False, "presentation": "ask-disambiguation-or-withhold"},
    {"id": "missing", "evidence_basis": "absent", "may_drive_destructive": False, "presentation": "block"},
    {"id": "oem-required", "evidence_basis": "verified-truth not yet OEM-confirmed for P0 promotion", "may_drive_destructive": False, "presentation": "withhold-and-escalate"},
]

CONFIDENCE_RULES = [
    "decision confidence = lowest tier across required evidence nodes",
    "high-confidence is the only level that may drive destructive decisions without administrator override",
    "low/ambiguous/missing decisions cannot be silently elevated",
    "OEM-required decisions cannot be assumed; they escalate",
    "confidence must be recorded with the decision (audit trail)",
    "aggregation never elevates inferred to verified-truth",
]

# ---------------------------------------------------------------------------
# 4. PATH PRIORITIZATION
# ---------------------------------------------------------------------------
PATH_CLASSES = [
    {"id": "preferred", "description": "canonical path with verified-truth evidence and full safeguards"},
    {"id": "alternative", "description": "alternate canonical path also verified-truth (e.g. role-specific)"},
    {"id": "fallback", "description": "registered fallback when canonical unavailable"},
    {"id": "emergency", "description": "safety-only path under emergency operational mode"},
    {"id": "safe-minimal", "description": "smallest safe path that still asserts validation predicate"},
    {"id": "advanced", "description": "expanded path for advanced/installer/administrator/maintenance roles"},
    {"id": "degraded", "description": "operational path under reduced capability"},
]

PRIORITIZATION_RULES = [
    "preferred > alternative > fallback > degraded > emergency > escalation",
    "safety-preserving overrides simplifying or shorter",
    "verified-truth path beats inferred path of same shape",
    "role-eligible paths beat role-gated paths the user cannot execute",
    "registered fallback beats improvisation (improvisation is forbidden)",
    "irreversible operations always require an explicit administrator-flow path",
]

PATH_TIE_BREAKERS = [
    "shortest declared path among same-class candidates",
    "fewest cross-product collisions",
    "highest declared maturity level of underlying nodes",
    "fewest unresolved validation findings on the path",
]

# ---------------------------------------------------------------------------
# 5. AMBIGUITY RESOLUTION
# ---------------------------------------------------------------------------
AMBIGUITY_TYPES = [
    {"id": "missing-evidence", "trigger": "required evidence node absent"},
    {"id": "conflicting-evidence", "trigger": "two verified-truth claims disagree"},
    {"id": "incomplete-procedure", "trigger": "step missing precondition or validation predicate"},
    {"id": "unclear-troubleshooting-state", "trigger": "no eligible branch resolves from current context"},
    {"id": "uncertain-recovery", "trigger": "no checkpoint AND destructive-step started"},
    {"id": "ambiguous-intent", "trigger": "intent-clarity in {ambiguous,missing} for non-trivial action"},
    {"id": "shared-concept-collision", "trigger": "concept reused across products without canonical owner"},
]

AMBIGUITY_RULES = [
    "ambiguity is named, not silently resolved",
    "destructive decisions never proceed under ambiguity",
    "ambiguity must select between: ask-disambiguation, withhold, or escalate",
    "default behavior under ambiguity = the safest of the three",
    "every ambiguity event is recorded for knowledge-health intake",
    "OEM-confirmation is the only resolver for verified-truth conflicts on P0 procedures",
]

AMBIGUITY_RESOLUTION_PATHS = [
    {"id": "ask-disambiguation", "when": "intent-clarity ambiguous AND non-destructive", "effect": "surface declarative question"},
    {"id": "withhold", "when": "evidence missing AND non-destructive", "effect": "decline to assert; expose disclosure"},
    {"id": "escalate", "when": "destructive OR irrecoverable OR conflicting verified-truth", "effect": "hand off to higher tier or OEM"},
]

# ---------------------------------------------------------------------------
# 6. ESCALATION
# ---------------------------------------------------------------------------
ESCALATION_TIERS = [
    {"tier": 1, "id": "self-service", "audience": "end user"},
    {"tier": 2, "id": "advanced-self-service", "audience": "advanced/installer/administrator"},
    {"tier": 3, "id": "support-required", "audience": "vendor/dealer support"},
    {"tier": 4, "id": "vendor-intervention", "audience": "OEM technical support"},
    {"tier": 5, "id": "rma-irrecoverable", "audience": "OEM RMA / replacement"},
]

ESCALATION_TRIGGERS = [
    {"id": "validation-failure-x3", "from": 1, "to": 2},
    {"id": "pairing-failed-x3", "from": 2, "to": 3},
    {"id": "lockout-cycles-ge-2", "from": 1, "to": 3},
    {"id": "battery-replacement-failure", "from": 2, "to": 4},
    {"id": "firmware-rollback-failure", "from": 4, "to": 5},
    {"id": "irrecoverable-failure", "from": "*", "to": 5},
    {"id": "conflicting-verified-truth", "from": "*", "to": 4},
    {"id": "destructive-under-ambiguity", "from": "*", "to": 3},
]

ESCALATION_RULES = [
    "escalation is monotonic during a single incident (no silent demotion)",
    "escalation cannot return to tier 1 without verified recovery (predicate)",
    "irrecoverable failures emit RMA escalation; no 'retry' affordance",
    "OEM intervention required for: firmware-bricked, conflicting verified-truth on P0, irrecoverable mid-destructive",
    "escalation events carry provenance and operational state snapshot",
]

# ---------------------------------------------------------------------------
# 7. ADAPTIVE RECOMMENDATION INTELLIGENCE
# ---------------------------------------------------------------------------
RECOMMENDATION_KINDS = [
    {"id": "next-step-recommendation", "scope": "within an active procedure"},
    {"id": "recovery-recommendation", "scope": "after failure / interruption"},
    {"id": "alternative-path-recommendation", "scope": "when preferred path is blocked"},
    {"id": "safety-first-recommendation", "scope": "when severity >= warning"},
    {"id": "simplification-recommendation", "scope": "for beginner / operator roles"},
    {"id": "evidence-disclosure-recommendation", "scope": "when confidence < high"},
    {"id": "escalation-recommendation", "scope": "when ambiguity / irrecoverable / OEM-required"},
]

RECOMMENDATION_RULES = [
    "recommendations are derived from declared decision points and path classes (no opaque ranking)",
    "recommendations are not commands; they describe options with justifications",
    "safety-first ranking dominates simplification ranking",
    "recommendations carry confidence + provenance",
    "recommendations never invent steps absent from the canonical procedure",
    "destructive recommendations require explicit-action confirmation contract",
    "recommendations remain subordinate to knowledge-core and prior governance layers",
]

RECOMMENDATION_PRIORITIZATION = [
    "safety > recovery > escalation > alternative > simplification > next-step",
    "high-confidence > low-confidence within the same kind",
    "role-eligible > role-gated within the same kind",
    "verified-truth > inferred within the same kind",
]

# ---------------------------------------------------------------------------
# 8. CHARTER
# ---------------------------------------------------------------------------
CHARTER_PRINCIPLES = [
    "the decision layer selects among declared options; it never invents options",
    "decisions are deterministic given the declared context vector + evidence",
    "destructive decisions require high confidence + explicit-action + role eligibility",
    "ambiguity is named, never silently resolved",
    "escalation is monotonic and observable",
    "preferred > alternative > fallback > degraded > emergency > escalation",
    "improvisation is forbidden; absence of a registered path => block + escalate",
    "decision provenance is auditable (inputs, predicate, selected option, confidence)",
    "subordinate to knowledge-core and to all ten prior governance layers",
    "future decision consumers inherit these contracts; the decision layer never bends them for a consumer",
]

AUTHORITY_AREAS = [
    "decision-point declarations",
    "branch type definitions and branching rules",
    "decision-confidence semantics",
    "path-class declarations and prioritization rules",
    "ambiguity classification and resolution paths",
    "escalation tiers, triggers, and monotonicity",
    "recommendation kinds and ranking rules",
    "audit/provenance requirements",
    "interaction contracts with adaptive layer",
    "future decision-consumer gates",
]

# ---------------------------------------------------------------------------
# 9. UNRESOLVED DECISION RISKS
# ---------------------------------------------------------------------------
DECISION_RISKS = [
    {"id": "thin-troubleshooting-corpus", "severity": "high", "summary": "branching/recommendations have limited eligible paths on 5/6 products", "cross_ref": "validation/maturity + execution + adaptive"},
    {"id": "no-confidence-tier-on-nodes", "severity": "high", "summary": "decision confidence is heuristic; per-node confidence not yet emitted by knowledge-core", "cross_ref": "knowledge-core/provenance + adaptive"},
    {"id": "no-fallback-registry", "severity": "high", "summary": "alternative-path-recommendation cannot resolve targets without registered fallbacks", "cross_ref": "adaptive/fallback"},
    {"id": "no-checkpoint-registry", "severity": "high", "summary": "cancel-vs-rollback decision degrades to cancel-no-state-change", "cross_ref": "execution/checkpoints"},
    {"id": "intent-clarity-detector-missing", "severity": "medium", "summary": "ask-disambiguation-vs-proceed is contractual; no live detector", "cross_ref": "adaptive/intent-clarity"},
    {"id": "context-vector-not-emitted", "severity": "medium", "summary": "decision determinism depends on a context-vector emitter not yet wired", "cross_ref": "adaptive/context-vector"},
    {"id": "shared-concepts-undeclared", "severity": "medium", "summary": "cross-product collisions cause ambiguous tie-breakers", "cross_ref": "validation/entity"},
    {"id": "oem-confirmation-channel-missing", "severity": "medium", "summary": "OEM-required resolutions cannot complete without an OEM channel contract", "cross_ref": "lifecycle/promotion-gates"},
    {"id": "decision-provenance-not-emitted", "severity": "medium", "summary": "auditable trail requires upstream emitter (modelled here, not implemented)", "cross_ref": "execution/snapshot-hash"},
]

# ---------------------------------------------------------------------------
# 10. FUTURE CONSUMERS
# ---------------------------------------------------------------------------
FUTURE_CONSUMERS = [
    {"id": "adaptive-operational-assistant", "gates": ["context-vector emitter", "per-node confidence", "checkpoint registry"]},
    {"id": "troubleshooting-decision-system", "gates": ["symptom corpus >= 10 per product", "branch provenance logging", "retry-threshold telemetry"]},
    {"id": "onboarding-decision-guidance", "gates": ["onboarding-stage emitter", "skill-declaration channel", "evidence disclosure contract"]},
    {"id": "context-aware-chatbot-system", "gates": ["execution snapshot-hash", "intent declaration channel", "decision provenance log"]},
    {"id": "multimodal-operational-assistance", "gates": ["visual-intent attached to physical-installation procedures", "evidence-disclosure renderer contract"]},
    {"id": "future-visual-assistance", "gates": ["visual-risk reclassification freeze", "fallback registry for visual-unavailable"]},
    {"id": "intelligent-escalation-system", "gates": ["OEM channel contract", "monotonic escalation log", "provenance with operational-state snapshot"]},
]

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
        "# DECISION_INTELLIGENCE_GOVERNANCE\n\n"
        "Eleventh constitutional layer — **modeling-only**.\n\n"
        "Models how the system evaluates, selects, prioritizes, escalates, and adapts "
        "between operational paths. The decision layer chooses among declared options, "
        "with declared predicates and provenance; it never invents options, never bypasses "
        "validation predicates, and never silently resolves ambiguity.\n\n"
        "Subordinate to: knowledge-core, VISUAL, KNOWLEDGE_CENTER, SEMANTIC, EXPERIENCE, "
        "LIFECYCLE, VALIDATION, ACCESS_AND_CONSUMPTION, COMPOSITION, EXECUTION, "
        "ADAPTIVE_OPERATIONAL.\n\n"
        "Excludes: chatbots, PDFs, image generation, rendering runtimes, frontends, "
        "automation runtimes, recommendation engines.\n",
        encoding="utf-8",
    )

    write_pair(
        ROOT, "00-charter", "Decision Intelligence Governance — Charter",
        "## Principles\n\n" + md_list(CHARTER_PRINCIPLES) +
        "\n\n## Authority Areas\n\n" + md_list(AUTHORITY_AREAS),
        {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS},
    )

    write_pair(
        ROOT / "decision-points", "decision-points", "Operational Decision Points",
        "## Decision Points\n\n" + md_list(DECISION_POINTS, key="id") +
        "\n\n## Rules\n\n" + md_list(DECISION_POINT_RULES),
        {"decision_points": DECISION_POINTS, "rules": DECISION_POINT_RULES},
    )

    write_pair(
        ROOT / "branching-semantics", "branching-semantics", "Branching Semantics",
        "## Branch Types\n\n" + md_list(BRANCH_TYPES, key="id") +
        "\n\n## Rules\n\n" + md_list(BRANCHING_RULES) +
        "\n\n## Outcomes\n\n" + md_list(BRANCH_OUTCOMES),
        {"branch_types": BRANCH_TYPES, "rules": BRANCHING_RULES, "outcomes": BRANCH_OUTCOMES},
    )

    write_pair(
        ROOT / "confidence-models", "confidence-models", "Decision Confidence",
        "## Levels\n\n" + md_list(CONFIDENCE_LEVELS, key="id") +
        "\n\n## Rules\n\n" + md_list(CONFIDENCE_RULES),
        {"levels": CONFIDENCE_LEVELS, "rules": CONFIDENCE_RULES},
    )

    write_pair(
        ROOT / "path-prioritization", "path-prioritization", "Alternative Path Prioritization",
        "## Path Classes\n\n" + md_list(PATH_CLASSES, key="id") +
        "\n\n## Rules\n\n" + md_list(PRIORITIZATION_RULES) +
        "\n\n## Tie-breakers\n\n" + md_list(PATH_TIE_BREAKERS),
        {"path_classes": PATH_CLASSES, "rules": PRIORITIZATION_RULES, "tie_breakers": PATH_TIE_BREAKERS},
    )

    write_pair(
        ROOT / "ambiguity-resolution", "ambiguity-resolution", "Ambiguity Resolution Semantics",
        "## Types\n\n" + md_list(AMBIGUITY_TYPES, key="id") +
        "\n\n## Rules\n\n" + md_list(AMBIGUITY_RULES) +
        "\n\n## Resolution Paths\n\n" + md_list(AMBIGUITY_RESOLUTION_PATHS, key="id"),
        {"types": AMBIGUITY_TYPES, "rules": AMBIGUITY_RULES, "resolution_paths": AMBIGUITY_RESOLUTION_PATHS},
    )

    write_pair(
        ROOT / "escalation", "escalation", "Escalation Decisioning",
        "## Tiers\n\n" + md_list(ESCALATION_TIERS, key="id") +
        "\n\n## Triggers\n\n" + md_list(ESCALATION_TRIGGERS, key="id") +
        "\n\n## Rules\n\n" + md_list(ESCALATION_RULES),
        {"tiers": ESCALATION_TIERS, "triggers": ESCALATION_TRIGGERS, "rules": ESCALATION_RULES},
    )

    write_pair(
        ROOT / "recommendations", "recommendations", "Adaptive Recommendation Intelligence",
        "## Kinds\n\n" + md_list(RECOMMENDATION_KINDS, key="id") +
        "\n\n## Rules\n\n" + md_list(RECOMMENDATION_RULES) +
        "\n\n## Prioritization\n\n" + md_list(RECOMMENDATION_PRIORITIZATION),
        {"kinds": RECOMMENDATION_KINDS, "rules": RECOMMENDATION_RULES, "prioritization": RECOMMENDATION_PRIORITIZATION},
    )

    write_pair(
        ROOT / "decision-risks", "decision-risks", "Unresolved Decision Risks",
        md_list(DECISION_RISKS, key="id"),
        {"risks": DECISION_RISKS},
    )

    write_pair(
        ROOT / "future-consumers", "future-consumers", "Future Decision-System Readiness",
        md_list(FUTURE_CONSUMERS, key="id"),
        {"future_consumers": FUTURE_CONSUMERS, "products": PRODUCTS},
    )

    reports = [
        ("01-decision-point-summary.json", {"count": len(DECISION_POINTS), "decision_points": DECISION_POINTS, "rules": DECISION_POINT_RULES}),
        ("02-branching-semantics-summary.json", {"branch_types": BRANCH_TYPES, "rules": BRANCHING_RULES, "outcomes": BRANCH_OUTCOMES}),
        ("03-decision-confidence-summary.json", {"levels": CONFIDENCE_LEVELS, "rules": CONFIDENCE_RULES}),
        ("04-path-prioritization-summary.json", {"path_classes": PATH_CLASSES, "rules": PRIORITIZATION_RULES, "tie_breakers": PATH_TIE_BREAKERS}),
        ("05-ambiguity-resolution-summary.json", {"types": AMBIGUITY_TYPES, "rules": AMBIGUITY_RULES, "resolution_paths": AMBIGUITY_RESOLUTION_PATHS}),
        ("06-escalation-summary.json", {"tiers": ESCALATION_TIERS, "triggers": ESCALATION_TRIGGERS, "rules": ESCALATION_RULES}),
        ("07-adaptive-recommendation-summary.json", {"kinds": RECOMMENDATION_KINDS, "rules": RECOMMENDATION_RULES, "prioritization": RECOMMENDATION_PRIORITIZATION}),
        ("08-decision-governance-summary.json", {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS}),
        ("09-unresolved-decision-risks.json", {"risks": DECISION_RISKS, "count": len(DECISION_RISKS), "high_count": sum(1 for r in DECISION_RISKS if r["severity"] == "high")}),
        ("10-future-decision-readiness.json", {"future_consumers": FUTURE_CONSUMERS, "products": PRODUCTS}),
    ]
    for name, payload in reports:
        out = {"schema": SCHEMA, "generated_at": now_iso(), **payload}
        (REPORTS / name).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Decision intelligence modeling complete.")
    print(f"  Constitutional root: {ROOT.relative_to(REPO)}")
    print(f"  Reports:             {REPORTS.relative_to(REPO)}/01..10")
    print(f"  Decision points: {len(DECISION_POINTS)} | Branch types: {len(BRANCH_TYPES)} | Confidence levels: {len(CONFIDENCE_LEVELS)} | Path classes: {len(PATH_CLASSES)} | Ambiguity types: {len(AMBIGUITY_TYPES)} | Escalation tiers: {len(ESCALATION_TIERS)} | Recommendation kinds: {len(RECOMMENDATION_KINDS)} | Risks: {len(DECISION_RISKS)}")


if __name__ == "__main__":
    main()
