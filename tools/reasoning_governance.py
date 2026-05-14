#!/usr/bin/env python3
"""
Phase 18 — REASONING GOVERNANCE (modeling-only).

Builds the twelfth constitutional layer:
  KNOWLEDGE_BUILDING/REASONING_GOVERNANCE/

Subordinate to: knowledge-core + all 11 prior governance layers.
Does NOT implement: chatbots, PDFs, images, rendering runtimes, frontends,
automation runtimes, recommendation engines, or reasoning engines.
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
ROOT = KB / "REASONING_GOVERNANCE"
REPORTS = MANUALS / "_repository-governance" / "reports" / "reasoning"

SCHEMA = "reasoning-governance/1.0"
PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

# ---------------------------------------------------------------------------
# 1. CAUSALITY
# ---------------------------------------------------------------------------
CAUSAL_RELATION_TYPES = [
    {"id": "causes", "description": "A directly produces B (deterministic)"},
    {"id": "enables", "description": "A makes B reachable but does not produce it"},
    {"id": "blocks", "description": "A prevents B"},
    {"id": "requires", "description": "B cannot occur without A"},
    {"id": "triggers", "description": "A initiates B as a side process"},
    {"id": "recovers-from", "description": "A restores a safe state after B"},
    {"id": "escalates-from", "description": "A is the escalation produced by B"},
    {"id": "confirms", "description": "A asserts B has occurred (validation predicate)"},
    {"id": "contradicts", "description": "A and B cannot both hold"},
]

CAUSAL_DOMAINS = [
    "actions", "states", "failures", "recoveries", "escalations", "confirmations", "interruptions",
]

CAUSAL_RULES = [
    "causal claims are declared, never inferred from co-occurrence",
    "every causal claim names its relation type and provenance",
    "deterministic 'causes' requires verified-truth evidence",
    "non-deterministic links use 'enables' or 'triggers' (never 'causes')",
    "absence of cause => the outcome cannot be asserted",
    "causality respects state transitions declared by EXECUTION_GOVERNANCE",
    "no causal link may bypass validation predicates",
]

# ---------------------------------------------------------------------------
# 2. REASONING CHAINS
# ---------------------------------------------------------------------------
CHAIN_TYPES = [
    {"id": "sequential", "description": "linear deduction across declared steps"},
    {"id": "dependent", "description": "later inferences depend on earlier verified outcomes"},
    {"id": "branching", "description": "chain forks at a declared decision point"},
    {"id": "recovery", "description": "chain re-enters at a checkpoint after failure"},
    {"id": "troubleshooting", "description": "chain advances by symptom-resolution branches"},
    {"id": "deductive", "description": "from declared facts and predicates to a conclusion"},
    {"id": "abductive", "description": "best-fit hypothesis among declared alternatives (always downgraded)"},
]

CHAIN_RULES = [
    "every chain is reproducible from declared inputs (context vector + evidence)",
    "every chain step records: predicate, inputs, evidence tier, confidence",
    "chain steps cannot invent new procedure steps",
    "abductive steps must be presented as 'likely', never 'verified'",
    "chains terminate (no infinite reasoning; bounded by retry thresholds)",
    "a chain that crosses an unsafe transition must be halted and escalated",
    "chains preserve user intent; intent change requires a new chain with provenance link",
]

CHAIN_TERMINATION_OUTCOMES = [
    "concluded-verified", "concluded-likely", "inconclusive", "blocked", "escalated", "abandoned",
]

# ---------------------------------------------------------------------------
# 3. CONSEQUENCE PROPAGATION
# ---------------------------------------------------------------------------
CONSEQUENCE_TYPES = [
    {"id": "direct-effect", "scope": "the step's declared outcome"},
    {"id": "side-effect", "scope": "declared collateral effects of the step"},
    {"id": "downstream-consequence", "scope": "effects on subsequent procedures or surfaces"},
    {"id": "unsafe-continuation-effect", "scope": "consequences when an unsafe path is forced"},
    {"id": "interrupted-state-consequence", "scope": "effects of leaving a procedure mid-step"},
    {"id": "recovery-impact", "scope": "effects propagated by recovery (rollback, retry, reset)"},
    {"id": "escalation-impact", "scope": "operational implications of moving up an escalation tier"},
]

PROPAGATION_RULES = [
    "consequences are declared, not inferred from history",
    "destructive steps must declare both direct and downstream consequences",
    "unsafe-continuation effects must list the safeguards being violated",
    "recovery impact must list which checkpoints/state restorations are required",
    "escalation impact must list which authority tier and which provenance is attached",
    "consequence claims carry confidence (verified-truth / inferred / OEM-confirmed)",
    "no consequence may silently downgrade a warning declared by knowledge-core",
]

# ---------------------------------------------------------------------------
# 4. STATE-DEPENDENT REASONING
# ---------------------------------------------------------------------------
REASONING_DIMENSIONS = [
    "operational-state", "recovery-status", "onboarding-stage", "degradation-level",
    "troubleshooting-stage", "confidence-level", "user-role", "evidence-completeness",
]

STATE_REASONING_RULES = [
    "the same input may resolve to different conclusions under different declared states",
    "state-dependent shifts must be explicitly declared (no implicit context drift)",
    "reasoning under degraded operation may use only fallback-eligible paths",
    "reasoning under recovery requires checkpoint anchors",
    "reasoning under low confidence downgrades all dependent conclusions",
    "reasoning under emergency-mode is restricted to safety-critical claims",
    "user-role gates conclusions that imply elevated authority",
]

REASONING_PROFILES = [
    {"id": "normal-operation", "applies_when": "operational-mode=normal", "default_chain_types": ["sequential", "deductive"]},
    {"id": "onboarding-reasoning", "applies_when": "operational-mode=onboarding", "default_chain_types": ["sequential", "dependent"]},
    {"id": "troubleshooting-reasoning", "applies_when": "operational-mode=troubleshooting", "default_chain_types": ["troubleshooting", "abductive"]},
    {"id": "recovery-reasoning", "applies_when": "operational-mode=recovery", "default_chain_types": ["recovery", "dependent"]},
    {"id": "degraded-reasoning", "applies_when": "operational-mode=degraded", "default_chain_types": ["sequential", "deductive"], "restrictions": ["fallback-eligible only"]},
    {"id": "emergency-reasoning", "applies_when": "operational-mode=emergency", "default_chain_types": ["deductive"], "restrictions": ["safety-critical only"]},
]

# ---------------------------------------------------------------------------
# 5. CONTRADICTION & CONFLICT
# ---------------------------------------------------------------------------
CONFLICT_TYPES = [
    {"id": "evidence-conflict", "description": "two evidence nodes disagree on the same claim"},
    {"id": "procedure-conflict", "description": "two procedures prescribe contradictory steps for the same situation"},
    {"id": "predicate-conflict", "description": "two validation predicates yield opposite results on the same state"},
    {"id": "state-conflict", "description": "current state cannot match the precondition of any eligible branch"},
    {"id": "intent-conflict", "description": "declared intent contradicts current operational state"},
    {"id": "recovery-signal-conflict", "description": "recovery indicators disagree (e.g., partial success + failure flag)"},
    {"id": "authority-conflict", "description": "two layers claim authority over the same decision"},
]

CONFLICT_RESOLUTION_RULES = [
    "no conflict may be resolved silently",
    "evidence-conflict at verified-truth tier escalates to OEM (P0 procedures)",
    "procedure-conflict requires composition-layer disambiguation (declared owner)",
    "predicate-conflict halts the chain and emits validation-finding",
    "state-conflict requires recovery-reasoning or escalation",
    "intent-conflict requires ask-disambiguation (non-destructive) or escalate",
    "authority-conflict resolves by the declared layer ordering (knowledge-core wins; adaptive/decision/reasoning never override)",
    "every conflict event is recorded for knowledge-health intake",
]

UNSAFE_REASONING_INDICATORS = [
    "abductive conclusion presented as verified",
    "chain crossing an unsafe state without escalation",
    "consequence claimed without declared causal link",
    "recovery asserted without checkpoint anchor",
    "destructive recommendation under low/ambiguous confidence",
]

# ---------------------------------------------------------------------------
# 6. UNCERTAINTY-AWARE REASONING
# ---------------------------------------------------------------------------
UNCERTAINTY_KINDS = [
    {"id": "evidence-incomplete", "treatment": "downgrade conclusions; require explicit acknowledgement"},
    {"id": "evidence-missing", "treatment": "block dependent conclusion; surface disclosure"},
    {"id": "inferred-state", "treatment": "label state as inferred; do not drive destructive ops"},
    {"id": "ambiguous-input", "treatment": "ask-disambiguation or withhold"},
    {"id": "oem-required", "treatment": "withhold and escalate to OEM channel"},
    {"id": "low-confidence-path", "treatment": "present as alternative-path, not preferred"},
    {"id": "irreducible-uncertainty", "treatment": "surface explicitly; never hide as a guess"},
]

UNCERTAINTY_RULES = [
    "uncertainty is named, not hidden",
    "uncertainty propagates: a chain step's confidence cannot exceed its inputs",
    "destructive operations require high-confidence inputs along the entire chain",
    "uncertainty disclosure is non-suppressible by adaptive presentation",
    "OEM-required uncertainty cannot be resolved by inference",
    "uncertainty events are recorded for knowledge-health intake",
]

# ---------------------------------------------------------------------------
# 7. HYPOTHESIS TRACKING
# ---------------------------------------------------------------------------
HYPOTHESIS_LIFECYCLE = [
    "proposed",
    "under-test",
    "confirmed",
    "refuted",
    "abandoned",
    "escalated",
    "refined",
]

HYPOTHESIS_FIELDS = [
    "id",
    "claim",
    "evidence-required",
    "evidence-collected",
    "predicate",
    "confidence-tier",
    "lifecycle-state",
    "parent-hypothesis (if refined)",
    "provenance",
]

HYPOTHESIS_RULES = [
    "every troubleshooting/recovery chain attaches at least one hypothesis",
    "hypotheses are explicit; no chain may proceed on an undeclared assumption",
    "confirmation requires the declared validation predicate to evaluate true",
    "refutation closes the hypothesis with provenance (no silent retry)",
    "refined hypotheses must link to their parent (audit trail)",
    "abandoned hypotheses cannot be silently re-opened in the same incident",
    "hypothesis confidence cannot exceed evidence confidence",
]

HYPOTHESIS_AUDIT_REQUIREMENTS = [
    "hypothesis state transitions are recorded",
    "evidence references are recorded",
    "predicate evaluation result is recorded",
    "linked decisions and branches are recorded",
    "linked escalations are recorded",
]

# ---------------------------------------------------------------------------
# 8. CHARTER
# ---------------------------------------------------------------------------
CHARTER_PRINCIPLES = [
    "the reasoning layer derives conclusions from declared causal links and predicates; it never invents knowledge",
    "every conclusion is reproducible from declared inputs and provenance",
    "abductive reasoning is permitted but always presented as 'likely' (never 'verified')",
    "uncertainty is named, never hidden; OEM-required uncertainty escalates",
    "contradictions and conflicts are surfaced, never silently resolved",
    "consequences are declared, not inferred from history",
    "reasoning chains terminate; bounded by retry thresholds and escalation triggers",
    "reasoning preserves user intent; intent changes start new chains with provenance",
    "reasoning is subordinate to knowledge-core and to all 11 prior governance layers",
    "future reasoning consumers inherit these contracts; the reasoning layer never bends them for a consumer",
]

AUTHORITY_AREAS = [
    "causal relation type declarations",
    "reasoning chain rules and termination outcomes",
    "consequence propagation rules",
    "state-dependent reasoning profiles",
    "contradiction classification and resolution rules",
    "uncertainty kinds and treatments",
    "hypothesis lifecycle and audit requirements",
    "audit/provenance requirements for reasoning",
    "interaction contracts with adaptive and decision layers",
    "future reasoning-consumer gates",
]

# ---------------------------------------------------------------------------
# 9. UNRESOLVED REASONING RISKS
# ---------------------------------------------------------------------------
REASONING_RISKS = [
    {"id": "thin-troubleshooting-corpus", "severity": "high", "summary": "abductive/troubleshooting chains have insufficient declared alternatives on 5/6 products", "cross_ref": "validation/maturity + decision + adaptive"},
    {"id": "no-confidence-tier-on-nodes", "severity": "high", "summary": "uncertainty propagation is heuristic without per-node confidence", "cross_ref": "knowledge-core/provenance"},
    {"id": "no-checkpoint-registry", "severity": "high", "summary": "recovery-reasoning lacks anchors; refined hypotheses cannot bind to a known good state", "cross_ref": "execution/checkpoints"},
    {"id": "no-causal-edges-emitted", "severity": "high", "summary": "causal relations are modelled here but not emitted as edges in knowledge-core", "cross_ref": "knowledge-core/graph"},
    {"id": "predicate-coverage-incomplete", "severity": "medium", "summary": "validation predicates exist for 5 procedure classes; chain confirmation is otherwise inferred", "cross_ref": "execution/validation-predicates"},
    {"id": "intent-clarity-detector-missing", "severity": "medium", "summary": "intent-conflict detection is contractual; no live detector", "cross_ref": "adaptive/intent-clarity + decision"},
    {"id": "context-vector-not-emitted", "severity": "medium", "summary": "state-dependent reasoning depends on a context-vector emitter not yet wired", "cross_ref": "adaptive/context-vector"},
    {"id": "shared-concepts-undeclared", "severity": "medium", "summary": "cross-product collisions create authority-conflict ambiguity", "cross_ref": "validation/entity"},
    {"id": "hypothesis-store-not-emitted", "severity": "medium", "summary": "hypothesis lifecycle is modelled here; no upstream store yet", "cross_ref": "this layer / future store contract"},
    {"id": "reasoning-provenance-not-emitted", "severity": "medium", "summary": "auditable trail requires upstream emitter", "cross_ref": "execution/snapshot-hash + decision/provenance"},
]

# ---------------------------------------------------------------------------
# 10. FUTURE CONSUMERS
# ---------------------------------------------------------------------------
FUTURE_CONSUMERS = [
    {"id": "reasoning-aware-troubleshooting-assistant", "gates": ["symptom corpus >= 10/product", "causal edges emitted", "hypothesis store contract"]},
    {"id": "adaptive-onboarding-system", "gates": ["onboarding-stage emitter", "predicate coverage on onboarding procedures", "context-vector emitter"]},
    {"id": "operational-decision-support-system", "gates": ["decision provenance log", "reasoning provenance log", "per-node confidence"]},
    {"id": "contextual-operational-copilot", "gates": ["context-vector emitter", "execution snapshot-hash", "hypothesis store contract", "intent declaration channel"]},
    {"id": "multimodal-reasoning-system", "gates": ["visual-intent attached to physical-installation procedures", "evidence-disclosure renderer contract"]},
    {"id": "future-visual-assistance", "gates": ["visual-risk reclassification freeze", "fallback registry for visual-unavailable contexts"]},
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
        "# REASONING_GOVERNANCE\n\n"
        "Twelfth constitutional layer — **modeling-only**.\n\n"
        "Models how operational reasoning unfolds coherently across multi-step workflows, "
        "troubleshooting, adaptive recovery, branching states, uncertainty, escalation, and "
        "interruption. Reasoning derives conclusions from declared causal links and predicates; "
        "it never invents knowledge, never hides uncertainty, and never silently resolves "
        "contradictions.\n\n"
        "Subordinate to: knowledge-core, VISUAL, KNOWLEDGE_CENTER, SEMANTIC, EXPERIENCE, "
        "LIFECYCLE, VALIDATION, ACCESS_AND_CONSUMPTION, COMPOSITION, EXECUTION, "
        "ADAPTIVE_OPERATIONAL, DECISION_INTELLIGENCE.\n\n"
        "Excludes: chatbots, PDFs, image generation, rendering runtimes, frontends, "
        "automation runtimes, recommendation engines, autonomous reasoning engines.\n",
        encoding="utf-8",
    )

    write_pair(
        ROOT, "00-charter", "Reasoning Governance — Charter",
        "## Principles\n\n" + md_list(CHARTER_PRINCIPLES) +
        "\n\n## Authority Areas\n\n" + md_list(AUTHORITY_AREAS),
        {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS},
    )

    write_pair(
        ROOT / "causality", "causality", "Operational Causality",
        "## Relation Types\n\n" + md_list(CAUSAL_RELATION_TYPES, key="id") +
        "\n\n## Domains\n\n" + md_list(CAUSAL_DOMAINS) +
        "\n\n## Rules\n\n" + md_list(CAUSAL_RULES),
        {"relation_types": CAUSAL_RELATION_TYPES, "domains": CAUSAL_DOMAINS, "rules": CAUSAL_RULES},
    )

    write_pair(
        ROOT / "reasoning-chains", "reasoning-chains", "Multi-Step Reasoning Chains",
        "## Chain Types\n\n" + md_list(CHAIN_TYPES, key="id") +
        "\n\n## Rules\n\n" + md_list(CHAIN_RULES) +
        "\n\n## Termination Outcomes\n\n" + md_list(CHAIN_TERMINATION_OUTCOMES),
        {"chain_types": CHAIN_TYPES, "rules": CHAIN_RULES, "termination_outcomes": CHAIN_TERMINATION_OUTCOMES},
    )

    write_pair(
        ROOT / "consequence-propagation", "consequence-propagation", "Consequence Propagation",
        "## Types\n\n" + md_list(CONSEQUENCE_TYPES, key="id") +
        "\n\n## Rules\n\n" + md_list(PROPAGATION_RULES),
        {"types": CONSEQUENCE_TYPES, "rules": PROPAGATION_RULES},
    )

    write_pair(
        ROOT / "state-reasoning", "state-reasoning", "State-Dependent Reasoning",
        "## Dimensions\n\n" + md_list(REASONING_DIMENSIONS) +
        "\n\n## Rules\n\n" + md_list(STATE_REASONING_RULES) +
        "\n\n## Profiles\n\n" + md_list(REASONING_PROFILES, key="id"),
        {"dimensions": REASONING_DIMENSIONS, "rules": STATE_REASONING_RULES, "profiles": REASONING_PROFILES},
    )

    write_pair(
        ROOT / "conflict-reasoning", "conflict-reasoning", "Contradiction & Conflict Reasoning",
        "## Conflict Types\n\n" + md_list(CONFLICT_TYPES, key="id") +
        "\n\n## Resolution Rules\n\n" + md_list(CONFLICT_RESOLUTION_RULES) +
        "\n\n## Unsafe Reasoning Indicators\n\n" + md_list(UNSAFE_REASONING_INDICATORS),
        {"conflict_types": CONFLICT_TYPES, "resolution_rules": CONFLICT_RESOLUTION_RULES, "unsafe_indicators": UNSAFE_REASONING_INDICATORS},
    )

    write_pair(
        ROOT / "uncertainty", "uncertainty", "Uncertainty-Aware Reasoning",
        "## Kinds\n\n" + md_list(UNCERTAINTY_KINDS, key="id") +
        "\n\n## Rules\n\n" + md_list(UNCERTAINTY_RULES),
        {"kinds": UNCERTAINTY_KINDS, "rules": UNCERTAINTY_RULES},
    )

    write_pair(
        ROOT / "hypothesis-tracking", "hypothesis-tracking", "Operational Hypothesis Tracking",
        "## Lifecycle\n\n" + md_list(HYPOTHESIS_LIFECYCLE) +
        "\n\n## Fields\n\n" + md_list(HYPOTHESIS_FIELDS) +
        "\n\n## Rules\n\n" + md_list(HYPOTHESIS_RULES) +
        "\n\n## Audit Requirements\n\n" + md_list(HYPOTHESIS_AUDIT_REQUIREMENTS),
        {"lifecycle": HYPOTHESIS_LIFECYCLE, "fields": HYPOTHESIS_FIELDS, "rules": HYPOTHESIS_RULES, "audit_requirements": HYPOTHESIS_AUDIT_REQUIREMENTS},
    )

    write_pair(
        ROOT / "reasoning-risks", "reasoning-risks", "Unresolved Reasoning Risks",
        md_list(REASONING_RISKS, key="id"),
        {"risks": REASONING_RISKS},
    )

    write_pair(
        ROOT / "future-consumers", "future-consumers", "Future Reasoning-System Readiness",
        md_list(FUTURE_CONSUMERS, key="id"),
        {"future_consumers": FUTURE_CONSUMERS, "products": PRODUCTS},
    )

    reports = [
        ("01-causality-summary.json", {"relation_types": CAUSAL_RELATION_TYPES, "domains": CAUSAL_DOMAINS, "rules": CAUSAL_RULES}),
        ("02-reasoning-chain-summary.json", {"chain_types": CHAIN_TYPES, "rules": CHAIN_RULES, "termination_outcomes": CHAIN_TERMINATION_OUTCOMES}),
        ("03-consequence-propagation-summary.json", {"types": CONSEQUENCE_TYPES, "rules": PROPAGATION_RULES}),
        ("04-state-reasoning-summary.json", {"dimensions": REASONING_DIMENSIONS, "rules": STATE_REASONING_RULES, "profiles": REASONING_PROFILES}),
        ("05-conflict-summary.json", {"conflict_types": CONFLICT_TYPES, "resolution_rules": CONFLICT_RESOLUTION_RULES, "unsafe_indicators": UNSAFE_REASONING_INDICATORS}),
        ("06-uncertainty-summary.json", {"kinds": UNCERTAINTY_KINDS, "rules": UNCERTAINTY_RULES}),
        ("07-hypothesis-tracking-summary.json", {"lifecycle": HYPOTHESIS_LIFECYCLE, "fields": HYPOTHESIS_FIELDS, "rules": HYPOTHESIS_RULES, "audit_requirements": HYPOTHESIS_AUDIT_REQUIREMENTS}),
        ("08-reasoning-governance-summary.json", {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS}),
        ("09-unresolved-reasoning-risks.json", {"risks": REASONING_RISKS, "count": len(REASONING_RISKS), "high_count": sum(1 for r in REASONING_RISKS if r["severity"] == "high")}),
        ("10-future-reasoning-readiness.json", {"future_consumers": FUTURE_CONSUMERS, "products": PRODUCTS}),
    ]
    for name, payload in reports:
        out = {"schema": SCHEMA, "generated_at": now_iso(), **payload}
        (REPORTS / name).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Reasoning intelligence modeling complete.")
    print(f"  Constitutional root: {ROOT.relative_to(REPO)}")
    print(f"  Reports:             {REPORTS.relative_to(REPO)}/01..10")
    print(f"  Causal relations: {len(CAUSAL_RELATION_TYPES)} | Chain types: {len(CHAIN_TYPES)} | Consequences: {len(CONSEQUENCE_TYPES)} | Reasoning profiles: {len(REASONING_PROFILES)} | Conflicts: {len(CONFLICT_TYPES)} | Uncertainty kinds: {len(UNCERTAINTY_KINDS)} | Hypothesis lifecycle: {len(HYPOTHESIS_LIFECYCLE)} | Risks: {len(REASONING_RISKS)}")


if __name__ == "__main__":
    main()
