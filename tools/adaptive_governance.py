#!/usr/bin/env python3
"""
Phase 16 — ADAPTIVE OPERATIONAL CONTEXT INTELLIGENCE (modeling-only).

Builds the tenth constitutional layer:
  KNOWLEDGE_BUILDING/ADAPTIVE_OPERATIONAL_GOVERNANCE/

Subordinate to: knowledge-core + all 9 prior governance layers.
Does NOT implement: chatbots, PDFs, images, rendering runtimes, adaptive UIs,
frontends, automation runtimes.
Idempotent. Non-destructive. Read-only with respect to per-product knowledge-core
and prior governance.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
THEME = REPO / "wp-content" / "themes" / "beslock-custom"
MANUALS = THEME / "User manuals"
KB = MANUALS / "KNOWLEDGE_BUILDING"
ROOT = KB / "ADAPTIVE_OPERATIONAL_GOVERNANCE"
REPORTS = MANUALS / "_repository-governance" / "reports" / "adaptive"

SCHEMA = "adaptive-operational-governance/1.0"
PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

# ---------------------------------------------------------------------------
# 1. CONTEXT DIMENSIONS
# ---------------------------------------------------------------------------
CONTEXT_DIMENSIONS = [
    {"id": "user-role", "values": ["beginner", "intermediate", "advanced", "installer", "administrator", "operator", "maintenance"]},
    {"id": "operational-mode", "values": ["normal", "onboarding", "troubleshooting", "recovery", "maintenance", "degraded", "emergency"]},
    {"id": "lifecycle-stage", "values": ["pre-install", "installing", "configuring", "operating", "decommissioning"]},
    {"id": "confidence-level", "values": ["verified-truth", "inferred", "ocr-derived", "ambiguous", "unverified"]},
    {"id": "severity-level", "values": ["nominal", "warning", "blocked", "unsafe", "irrecoverable"]},
    {"id": "recovery-status", "values": ["none", "in-progress", "succeeded", "failed", "escalated"]},
    {"id": "onboarding-stage", "values": ["unboxed", "physically-installed", "powered", "paired", "enrolled", "verified"]},
    {"id": "environmental", "values": ["normal-power", "low-battery", "offline", "noisy", "physical-restricted-access"]},
    {"id": "evidence-completeness", "values": ["complete", "partial", "missing", "conflicting"]},
    {"id": "intent-clarity", "values": ["explicit", "inferred", "ambiguous", "missing"]},
]

CONTEXT_RULES = [
    "context dimensions are observed, never assumed",
    "missing dimensions resolve to the safest value",
    "dimension values must be declared (no free-form context)",
    "multiple dimensions compose; no dimension overrides another silently",
    "context vector must be reproducible from declared inputs",
]

# ---------------------------------------------------------------------------
# 2. ADAPTIVE GUIDANCE SEMANTICS
# ---------------------------------------------------------------------------
GUIDANCE_ADAPTATIONS = [
    {"id": "simplified-onboarding-for-beginners", "trigger": "user-role=beginner AND operational-mode=onboarding", "effect": "expand prerequisites; collapse advanced shortcuts; add irreversibility warnings explicitly"},
    {"id": "shortcut-paths-for-installers", "trigger": "user-role=installer AND lifecycle-stage in {installing,configuring}", "effect": "permit batched steps when no destructive boundary is crossed"},
    {"id": "warnings-amplified-during-recovery", "trigger": "operational-mode=recovery", "effect": "force mandatory-warning surfaces before every transition"},
    {"id": "troubleshooting-first-under-failure", "trigger": "severity-level in {blocked,unsafe}", "effect": "suppress non-essential operational steps; surface symptom-resolution branch first"},
    {"id": "confidence-aware-expansion", "trigger": "confidence-level in {inferred,ocr-derived,ambiguous}", "effect": "attach evidence disclosure; widen step granularity; require explicit user acknowledgement"},
    {"id": "admin-only-controls-gated", "trigger": "user-role!=administrator AND step.requires=admin", "effect": "block step entry; surface escalation path"},
    {"id": "degraded-mode-substitution", "trigger": "operational-mode=degraded", "effect": "swap full procedure for fallback procedure when registered; otherwise block"},
    {"id": "emergency-mode-pruning", "trigger": "operational-mode=emergency", "effect": "retain only safety-critical steps; defer all configuration"},
    {"id": "evidence-incomplete-disclosure", "trigger": "evidence-completeness in {partial,missing,conflicting}", "effect": "annotate guidance with disclosure; prohibit verified-truth claims"},
]

GUIDANCE_RULES = [
    "adaptation may simplify presentation but never silently weaken safeguards",
    "destructive steps cannot be removed by any adaptation",
    "irreversibility warnings cannot be suppressed by any adaptation",
    "adaptations must compose deterministically (declared precedence)",
    "every adaptation must declare its trigger predicate and observable effect",
    "no adaptation may invent steps not present in the canonical procedure",
]

ADAPTATION_PRECEDENCE = [
    "safety-preserving > simplifying",
    "explicit-context > inferred-context",
    "block > warn > suppress > expand > collapse",
    "knowledge-core authority > adaptive layer",
]

# ---------------------------------------------------------------------------
# 3. USER-SKILL MODELS
# ---------------------------------------------------------------------------
USER_SKILL_MODELS = [
    {"id": "beginner", "audience": "first-time end user", "complexity_ceiling": "low", "permissions": ["operate", "request-help"], "defaults": ["expanded-prereqs", "irreversibility-warnings-explicit", "no-batching"]},
    {"id": "intermediate", "audience": "returning end user", "complexity_ceiling": "medium", "permissions": ["operate", "self-troubleshoot-tier1"], "defaults": ["compact-prereqs", "batched-non-destructive"]},
    {"id": "advanced", "audience": "power user / facility owner", "complexity_ceiling": "high", "permissions": ["operate", "configure", "self-troubleshoot-tier2"], "defaults": ["batched-non-destructive", "advanced-options-visible"]},
    {"id": "installer", "audience": "professional installer", "complexity_ceiling": "high", "permissions": ["install", "configure", "verify-install"], "defaults": ["batched-non-destructive", "skip-orientation"]},
    {"id": "administrator", "audience": "site/system admin", "complexity_ceiling": "high", "permissions": ["configure", "admin-actions", "delete-users", "factory-reset"], "defaults": ["full-controls", "irreversibility-warnings-explicit"]},
    {"id": "operator", "audience": "day-to-day operator with limited authority", "complexity_ceiling": "medium", "permissions": ["operate", "log-incidents"], "defaults": ["compact-prereqs", "no-admin-controls"]},
    {"id": "maintenance", "audience": "field maintenance technician", "complexity_ceiling": "high", "permissions": ["operate", "battery-replacement", "diagnostics", "verify-install"], "defaults": ["diagnostics-visible", "physical-presence-required"]},
]

SKILL_RULES = [
    "skill never widens permissions beyond authority-area declarations",
    "skill never lowers safeguards (only presentation density)",
    "advanced/installer/administrator/maintenance may batch only non-destructive steps",
    "factory-reset and delete-all-users remain administrator-only across all skills",
]

# ---------------------------------------------------------------------------
# 4. WARNING ESCALATION
# ---------------------------------------------------------------------------
WARNING_LEVELS = [
    {"id": "informational", "rank": 0, "must_acknowledge": False},
    {"id": "advisory", "rank": 1, "must_acknowledge": False},
    {"id": "caution", "rank": 2, "must_acknowledge": True},
    {"id": "warning", "rank": 3, "must_acknowledge": True},
    {"id": "critical", "rank": 4, "must_acknowledge": True},
    {"id": "irreversible", "rank": 5, "must_acknowledge": True, "requires_explicit_action": True},
    {"id": "emergency", "rank": 6, "must_acknowledge": True, "requires_explicit_action": True},
]

WARNING_ESCALATION_RULES = [
    {"id": "severity-driven", "rule": "severity-level=warning -> minimum caution; severity-level in {blocked,unsafe} -> minimum warning"},
    {"id": "interruption-driven", "rule": "interruption during destructive step -> escalate to critical"},
    {"id": "unsafe-state-driven", "rule": "entering an unsafe state -> warning + mandatory-warning surface"},
    {"id": "recovery-driven", "rule": "recovery in progress -> all subsequent steps escalate one level"},
    {"id": "irreversible-driven", "rule": "irreversible operations -> always 'irreversible' level + explicit-action confirmation"},
    {"id": "emergency-driven", "rule": "operational-mode=emergency -> emergency level on any non-safety step blocking continuation"},
    {"id": "evidence-driven", "rule": "confidence-level in {inferred,ocr-derived,ambiguous} -> attach 'advisory' disclosure to operational claims"},
]

ESCALATION_INVARIANTS = [
    "warnings can be escalated by adaptation but never demoted",
    "an explicit-action confirmation cannot be replaced by acknowledgement",
    "warnings declared by knowledge-core or composition are non-removable",
    "every escalation must record its trigger predicate (auditable)",
]

# ---------------------------------------------------------------------------
# 5. DYNAMIC TROUBLESHOOTING BRANCHING
# ---------------------------------------------------------------------------
TROUBLESHOOTING_INPUTS = [
    "observed-symptom",
    "failed-recovery-attempt-count",
    "current-operational-state",
    "user-role",
    "confidence-level",
    "unresolved-ambiguity",
    "environmental-conditions",
    "evidence-completeness",
]

BRANCHING_STRATEGIES = [
    {"id": "symptom-first", "trigger": "observed-symptom present", "effect": "branch to symptom-resolution path before procedural retry"},
    {"id": "retry-cap", "trigger": "failed-recovery-attempt-count >= threshold", "effect": "block further retries; escalate one tier per threshold rule"},
    {"id": "state-coherent-paths", "trigger": "current-operational-state declared", "effect": "only paths whose preconditions match the state are eligible"},
    {"id": "role-gated-paths", "trigger": "path requires elevated role", "effect": "filter out paths the current role cannot execute"},
    {"id": "confidence-gated-claims", "trigger": "confidence-level in {inferred,ocr-derived,ambiguous}", "effect": "downgrade resolution claims to 'likely-resolution' until verified by predicate"},
    {"id": "ambiguity-resolution-first", "trigger": "unresolved-ambiguity present", "effect": "ask disambiguating question (declarative) before progressing"},
    {"id": "environmental-fallback", "trigger": "environmental constraint blocks canonical path", "effect": "swap to registered fallback or escalate"},
    {"id": "evidence-disclosure-branch", "trigger": "evidence-completeness in {partial,missing,conflicting}", "effect": "annotate branch with disclosure; require explicit acknowledgement to proceed"},
]

BRANCHING_RULES = [
    "all branches resolve from declared inputs (no opaque heuristics)",
    "no branch may bypass validation predicates of the underlying procedure",
    "branch eligibility must be deterministic given the context vector",
    "every branch carries provenance (which input(s) selected it)",
    "branch transitions never silently change user intent",
]

RETRY_THRESHOLDS = [
    {"id": "validation-failure", "after": 3, "action": "escalate-to-tier-2"},
    {"id": "pairing-failure", "after": 3, "action": "escalate-to-tier-3"},
    {"id": "lockout-cycles", "after": 2, "action": "escalate-to-tier-3"},
    {"id": "battery-replacement-failure", "after": 1, "action": "escalate-to-tier-4-vendor"},
    {"id": "firmware-rollback-failure", "after": 1, "action": "escalate-to-tier-5-rma"},
]

# ---------------------------------------------------------------------------
# 6. FALLBACK & DEGRADED OPERATION MODELS
# ---------------------------------------------------------------------------
DEGRADATION_LEVELS = [
    {"id": "full", "description": "all capabilities available"},
    {"id": "reduced", "description": "non-essential capabilities suppressed"},
    {"id": "safety-only", "description": "only safety-critical actions and observation permitted"},
    {"id": "read-only", "description": "no state-changing actions; observation allowed"},
    {"id": "halted", "description": "no operation; escalate"},
]

FALLBACK_PATTERNS = [
    {"id": "manual-fallback", "trigger": "automation/electronic path unavailable", "effect": "expose declared manual procedure if registered"},
    {"id": "physical-key-fallback", "trigger": "electronic-unlock path unavailable AND device supports physical-key", "effect": "guide to physical-key procedure"},
    {"id": "offline-fallback", "trigger": "environmental=offline", "effect": "restrict to offline-safe procedures only"},
    {"id": "low-battery-fallback", "trigger": "environmental=low-battery", "effect": "block firmware/destructive ops; permit replacement and unlock"},
    {"id": "low-confidence-fallback", "trigger": "confidence-level in {inferred,ocr-derived,ambiguous}", "effect": "downgrade to 'likely-procedure' framing; require explicit acknowledgement"},
    {"id": "emergency-recovery", "trigger": "irrecoverable failure mid-destructive op", "effect": "halt and surface vendor/RMA escalation; never auto-resume"},
]

DEGRADATION_RULES = [
    "degradation may reduce capabilities but never weaken safeguards",
    "fallback procedures must themselves be governed (charters, predicates, provenance)",
    "absence of a registered fallback => block + escalate (never improvise)",
    "degraded-mode transitions are observable and recorded",
    "return to 'full' requires verified restoration (predicate, not assumption)",
]

# ---------------------------------------------------------------------------
# 7. CONFIDENCE-AWARE GUIDANCE
# ---------------------------------------------------------------------------
CONFIDENCE_TIERS = [
    {"id": "verified-truth", "claim_strength": "asserts", "may_drive_destructive_step": True, "disclosure_required": False},
    {"id": "inferred", "claim_strength": "suggests", "may_drive_destructive_step": False, "disclosure_required": True},
    {"id": "ocr-derived", "claim_strength": "transcribes", "may_drive_destructive_step": False, "disclosure_required": True},
    {"id": "ambiguous", "claim_strength": "questions", "may_drive_destructive_step": False, "disclosure_required": True},
    {"id": "unverified", "claim_strength": "withholds", "may_drive_destructive_step": False, "disclosure_required": True},
    {"id": "missing", "claim_strength": "blocks", "may_drive_destructive_step": False, "disclosure_required": True},
]

CONFIDENCE_RULES = [
    "destructive operations require verified-truth or explicit administrator override",
    "non-verified content must be linguistically downgraded ('likely', 'reported', 'per OCR')",
    "missing evidence blocks the dependent step; never silently inferred",
    "OEM-confirmed content cannot be downgraded by adaptation",
    "confidence tier of a step = lowest tier among its required evidence nodes",
    "guidance must not aggregate inferred claims into a verified-truth presentation",
]

CONFIDENCE_FAILSAFES = [
    "ambiguity present => surface disambiguation, not a guess",
    "conflicting evidence => block + escalate to knowledge-health",
    "OCR disagreement with verified-truth => verified-truth wins; OCR flagged",
    "thresholded numeric specs missing => substitute 'manufacturer-specified' placeholder, do not invent",
]

# ---------------------------------------------------------------------------
# 8. ADAPTIVE GOVERNANCE — CHARTER
# ---------------------------------------------------------------------------
CHARTER_PRINCIPLES = [
    "the adaptive layer observes context and shapes presentation; it never invents knowledge",
    "all adaptation is subordinate to knowledge-core and to every prior governance layer",
    "safety-preserving adaptations override simplifying adaptations",
    "destructive steps, irreversibility warnings, and validation predicates are non-adaptable",
    "context dimensions are declared and observable; no opaque heuristics",
    "confidence drives presentation strength; verified-truth is never weakened, inferred is never amplified",
    "fallback and degraded operation are first-class, governed, and registered (no improvisation)",
    "warnings may escalate but never demote; explicit-action requirements are immutable",
    "every adaptation is auditable: trigger predicate + observable effect + provenance",
    "future adaptive consumers inherit these contracts; the adaptive layer never bends them for a consumer",
]

AUTHORITY_AREAS = [
    "context-dimension declaration",
    "adaptive-guidance trigger predicates",
    "user-skill model definitions",
    "warning escalation rules",
    "troubleshooting branching strategies",
    "fallback and degradation registries",
    "confidence-tier semantics",
    "adaptation precedence ordering",
    "audit/provenance requirements",
    "future adaptive consumer gates",
]

# ---------------------------------------------------------------------------
# 9. UNRESOLVED ADAPTIVE RISKS
# ---------------------------------------------------------------------------
ADAPTIVE_RISKS = [
    {"id": "thin-troubleshooting-corpus", "severity": "high", "summary": "symptom-first branching has limited eligible paths on 5/6 products", "cross_ref": "validation/maturity + execution/troubleshooting-readiness"},
    {"id": "warning-corpus-gap", "severity": "high", "summary": "escalation cannot fire 'mandatory-warning surface' on 2 products", "cross_ref": "validation/warnings + execution/safeguards"},
    {"id": "no-confidence-tier-on-nodes", "severity": "high", "summary": "confidence-aware guidance currently relies on heuristic mapping; per-node confidence not yet emitted by knowledge-core", "cross_ref": "knowledge-core/provenance"},
    {"id": "no-fallback-registry", "severity": "high", "summary": "degraded-mode substitution cannot resolve targets without a registered fallback list per procedure", "cross_ref": "execution/fallback + composition"},
    {"id": "context-vector-not-emitted", "severity": "medium", "summary": "context dimensions are modelled here but no upstream emitter populates them yet", "cross_ref": "future runtime contract"},
    {"id": "intent-clarity-detector-missing", "severity": "medium", "summary": "ambiguous-intent branch is contractual; no live detector", "cross_ref": "execution/intent-rules"},
    {"id": "skill-inference-undefined", "severity": "medium", "summary": "user-role assumed declared; inference path not modelled here by design", "cross_ref": "future product-surface contract"},
    {"id": "shared-concepts-undeclared", "severity": "medium", "summary": "cross-product collisions block uniform adaptation across the family", "cross_ref": "validation/entity"},
    {"id": "adaptation-precedence-conflicts", "severity": "low", "summary": "rare overlapping triggers may produce ambiguous order; precedence rules cover declared cases", "cross_ref": "this layer / precedence"},
]

# ---------------------------------------------------------------------------
# 10. FUTURE ADAPTIVE-SYSTEM READINESS
# ---------------------------------------------------------------------------
FUTURE_CONSUMERS = [
    {"id": "adaptive-onboarding-assistant", "gates": ["context-vector emitter", "skill declaration channel", "checkpoint registry per procedure"]},
    {"id": "contextual-troubleshooting-assistant", "gates": ["symptom corpus >= 10 per product", "retry-threshold telemetry channel", "branch provenance logging"]},
    {"id": "state-aware-chatbot-system", "gates": ["execution snapshot-hash on traces", "intent declaration channel", "confidence tier on nodes"]},
    {"id": "adaptive-multimodal-guidance", "gates": ["visual-intent attached to physical-installation procedures", "evidence-disclosure renderer contract"]},
    {"id": "future-visual-assistance", "gates": ["visual-risk reclassification freeze in place", "fallback registry for visual-unavailable contexts"]},
    {"id": "contextual-operational-rendering", "gates": ["adaptation-effect contract honoured by renderer", "non-removable safeguards enforced at render boundary"]},
    {"id": "personalized-operational-assistance", "gates": ["per-user context vector with consent contract", "skill model declared by host application"]},
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

    # README
    (ROOT / "README.md").write_text(
        "# ADAPTIVE_OPERATIONAL_GOVERNANCE\n\n"
        "Tenth constitutional layer — **modeling-only**.\n\n"
        "Models how operational guidance adapts to context, skill, confidence, severity, "
        "recovery, environment, and evidence completeness. The adaptive layer observes and "
        "shapes presentation; it never invents knowledge, never weakens safeguards, and "
        "never overrides knowledge-core authority.\n\n"
        "Subordinate to: knowledge-core, VISUAL, KNOWLEDGE_CENTER, SEMANTIC, EXPERIENCE, "
        "LIFECYCLE, VALIDATION, ACCESS_AND_CONSUMPTION, COMPOSITION, EXECUTION.\n\n"
        "Excludes: chatbots, PDFs, image generation, rendering runtimes, adaptive UIs, "
        "frontends, automation runtimes.\n",
        encoding="utf-8",
    )

    # 00 — charter
    write_pair(
        ROOT, "00-charter", "Adaptive Operational Governance — Charter",
        "## Principles\n\n" + md_list(CHARTER_PRINCIPLES) +
        "\n\n## Authority Areas\n\n" + md_list(AUTHORITY_AREAS),
        {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS},
    )

    # 1 context dimensions
    write_pair(
        ROOT / "context-dimensions", "context-dimensions", "Context Dimensions",
        "## Dimensions\n\n" + md_list(CONTEXT_DIMENSIONS, key="id") +
        "\n\n## Rules\n\n" + md_list(CONTEXT_RULES),
        {"dimensions": CONTEXT_DIMENSIONS, "rules": CONTEXT_RULES},
    )

    # 2 guidance semantics
    write_pair(
        ROOT / "guidance-semantics", "guidance-semantics", "Adaptive Guidance Semantics",
        "## Adaptations\n\n" + md_list(GUIDANCE_ADAPTATIONS, key="id") +
        "\n\n## Rules\n\n" + md_list(GUIDANCE_RULES) +
        "\n\n## Precedence\n\n" + md_list(ADAPTATION_PRECEDENCE),
        {"adaptations": GUIDANCE_ADAPTATIONS, "rules": GUIDANCE_RULES, "precedence": ADAPTATION_PRECEDENCE},
    )

    # 3 user skill
    write_pair(
        ROOT / "user-skill-models", "user-skill-models", "User-Skill Models",
        "## Models\n\n" + md_list(USER_SKILL_MODELS, key="id") +
        "\n\n## Rules\n\n" + md_list(SKILL_RULES),
        {"models": USER_SKILL_MODELS, "rules": SKILL_RULES},
    )

    # 4 warning escalation
    write_pair(
        ROOT / "warning-escalation", "warning-escalation", "Contextual Warning Escalation",
        "## Levels\n\n" + md_list(WARNING_LEVELS, key="id") +
        "\n\n## Rules\n\n" + md_list(WARNING_ESCALATION_RULES, key="id") +
        "\n\n## Invariants\n\n" + md_list(ESCALATION_INVARIANTS),
        {"levels": WARNING_LEVELS, "rules": WARNING_ESCALATION_RULES, "invariants": ESCALATION_INVARIANTS},
    )

    # 5 troubleshooting adaptation
    write_pair(
        ROOT / "troubleshooting-adaptation", "troubleshooting-adaptation", "Dynamic Troubleshooting Branching",
        "## Inputs\n\n" + md_list(TROUBLESHOOTING_INPUTS) +
        "\n\n## Strategies\n\n" + md_list(BRANCHING_STRATEGIES, key="id") +
        "\n\n## Rules\n\n" + md_list(BRANCHING_RULES) +
        "\n\n## Retry Thresholds\n\n" + md_list(RETRY_THRESHOLDS, key="id"),
        {"inputs": TROUBLESHOOTING_INPUTS, "strategies": BRANCHING_STRATEGIES, "rules": BRANCHING_RULES, "retry_thresholds": RETRY_THRESHOLDS},
    )

    # 6 fallback / degraded
    write_pair(
        ROOT / "fallback-models", "fallback-models", "Fallback & Degraded Operation",
        "## Degradation Levels\n\n" + md_list(DEGRADATION_LEVELS, key="id") +
        "\n\n## Fallback Patterns\n\n" + md_list(FALLBACK_PATTERNS, key="id") +
        "\n\n## Rules\n\n" + md_list(DEGRADATION_RULES),
        {"levels": DEGRADATION_LEVELS, "fallbacks": FALLBACK_PATTERNS, "rules": DEGRADATION_RULES},
    )

    # 7 confidence
    write_pair(
        ROOT / "confidence-models", "confidence-models", "Confidence-Aware Guidance",
        "## Tiers\n\n" + md_list(CONFIDENCE_TIERS, key="id") +
        "\n\n## Rules\n\n" + md_list(CONFIDENCE_RULES) +
        "\n\n## Failsafes\n\n" + md_list(CONFIDENCE_FAILSAFES),
        {"tiers": CONFIDENCE_TIERS, "rules": CONFIDENCE_RULES, "failsafes": CONFIDENCE_FAILSAFES},
    )

    # 8 risks
    write_pair(
        ROOT / "adaptive-risks", "adaptive-risks", "Unresolved Adaptive Risks",
        md_list(ADAPTIVE_RISKS, key="id"),
        {"risks": ADAPTIVE_RISKS},
    )

    # 9 future consumers
    write_pair(
        ROOT / "future-consumers", "future-consumers", "Future Adaptive-System Readiness",
        md_list(FUTURE_CONSUMERS, key="id"),
        {"future_consumers": FUTURE_CONSUMERS, "products": PRODUCTS},
    )

    # ----- numbered reports -----
    reports = [
        ("01-context-dimension-summary.json", {"dimension_count": len(CONTEXT_DIMENSIONS), "dimensions": CONTEXT_DIMENSIONS, "rules": CONTEXT_RULES}),
        ("02-adaptive-guidance-summary.json", {"adaptation_count": len(GUIDANCE_ADAPTATIONS), "rule_count": len(GUIDANCE_RULES), "precedence": ADAPTATION_PRECEDENCE, "adaptations": GUIDANCE_ADAPTATIONS}),
        ("03-user-skill-summary.json", {"model_count": len(USER_SKILL_MODELS), "models": USER_SKILL_MODELS, "rules": SKILL_RULES}),
        ("04-warning-escalation-summary.json", {"levels": WARNING_LEVELS, "rules": WARNING_ESCALATION_RULES, "invariants": ESCALATION_INVARIANTS}),
        ("05-troubleshooting-adaptation-summary.json", {"inputs": TROUBLESHOOTING_INPUTS, "strategies": BRANCHING_STRATEGIES, "rules": BRANCHING_RULES, "retry_thresholds": RETRY_THRESHOLDS}),
        ("06-fallback-degraded-summary.json", {"levels": DEGRADATION_LEVELS, "fallbacks": FALLBACK_PATTERNS, "rules": DEGRADATION_RULES}),
        ("07-confidence-aware-summary.json", {"tiers": CONFIDENCE_TIERS, "rules": CONFIDENCE_RULES, "failsafes": CONFIDENCE_FAILSAFES}),
        ("08-adaptive-governance-summary.json", {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS}),
        ("09-unresolved-adaptive-risks.json", {"risks": ADAPTIVE_RISKS, "count": len(ADAPTIVE_RISKS), "high_count": sum(1 for r in ADAPTIVE_RISKS if r["severity"] == "high")}),
        ("10-future-adaptive-readiness.json", {"future_consumers": FUTURE_CONSUMERS, "products": PRODUCTS}),
    ]
    for name, payload in reports:
        out = {"schema": SCHEMA, "generated_at": now_iso(), **payload}
        (REPORTS / name).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Adaptive operational context modeling complete.")
    print(f"  Constitutional root: {ROOT.relative_to(REPO)}")
    print(f"  Reports:             {REPORTS.relative_to(REPO)}/01..10")
    print(f"  Dimensions: {len(CONTEXT_DIMENSIONS)} | Adaptations: {len(GUIDANCE_ADAPTATIONS)} | Skill models: {len(USER_SKILL_MODELS)} | Warning levels: {len(WARNING_LEVELS)} | Branch strategies: {len(BRANCHING_STRATEGIES)} | Fallbacks: {len(FALLBACK_PATTERNS)} | Confidence tiers: {len(CONFIDENCE_TIERS)} | Risks: {len(ADAPTIVE_RISKS)}")


if __name__ == "__main__":
    main()
