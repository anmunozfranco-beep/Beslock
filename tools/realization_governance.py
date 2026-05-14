"""
Phase 23 — REALIZATION & DEPLOYMENT PRIORITIZATION (modeling-only).

Seventeenth constitutional layer. Subordinate to knowledge-core and to all
sixteen prior governance layers. Defines how the cognition ecosystem transitions
into real operational systems through staged realization, deployment
prioritization, runtime sequencing, and operational value optimization.

Hard exclusions (verbatim):
- DO NOT implement production runtimes
- DO NOT build chatbots
- DO NOT generate images
- DO NOT create PDFs
- DO NOT implement autonomous cognition
- DO NOT build frontend systems

Idempotent. Non-destructive. Reads no per-product knowledge-core files.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "REALIZATION_AND_DEPLOYMENT_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "realization"

SCHEMA = "realization-and-deployment-governance/1.0"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def md_list(items):
    return "\n".join(f"- {x}" for x in items)


def write_pair(folder: Path, slug: str, title: str, intro: str, sections, payload: dict):
    folder.mkdir(parents=True, exist_ok=True)
    md_lines = [f"# {title}", "", intro, ""]
    for h, body in sections:
        md_lines.append(f"## {h}")
        md_lines.append("")
        md_lines.append(body)
        md_lines.append("")
    (folder / f"{slug}.md").write_text("\n".join(md_lines).rstrip() + "\n", encoding="utf-8")
    (folder / f"{slug}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Charter
# ---------------------------------------------------------------------------

CHARTER_PRINCIPLES = [
    "This realization layer is itself modeling-only; it deploys nothing.",
    "Realization is a staged, supervised, evidence-driven discipline — not a launch decision.",
    "No runtime is realized while any declared blocking risk for that runtime remains unresolved.",
    "Every realization stage produces evidence, provenance, and a documented exit decision.",
    "Realization preserves all prior constitutional layers verbatim; it can only narrow authority.",
    "Cognition-to-product transition cannot expand cognitive capabilities — only operationalize declared ones.",
    "Proof-of-value is required before promoting any runtime beyond supervised stages.",
    "Deployment prioritization is governed by safety > readiness > value — never the reverse.",
    "All runtime realization remains subordinate to the governed knowledge-core forever.",
    "Hard exclusions (no chatbots, frontends, PDFs, images, autonomous cognition, production runtimes) bind every roadmap entry.",
]

CHARTER_AUTHORITY = [
    "Declares the operational-value scoring rubric and ranking method.",
    "Declares the catalog of vertical slices and their proof-of-value contracts.",
    "Declares the deployment dependency model (runtime / cognition / orchestration / interop / governance).",
    "Declares the staged-rollout phases, gates, and evidence requirements.",
    "Declares the operational-risk taxonomy and prioritization rules.",
    "Declares the cognition-to-product transition contracts and surfaces.",
    "Declares the deployment governance philosophy and supervision posture.",
    "Declares the future-realization roadmap and per-consumer gates.",
    "Declares the first-production-candidate assessment criteria.",
    "Declares that realization remains subordinate to knowledge-core and to all sixteen prior layers.",
]


# ---------------------------------------------------------------------------
# TASK 1 — Operational value prioritization
# ---------------------------------------------------------------------------

VALUE_DIMENSIONS = [
    {"id": "operational-value",       "weight": 0.20, "scale": "1 (low) — 5 (high)"},
    {"id": "implementation-complexity","weight": 0.15, "scale": "1 (high complexity) — 5 (low complexity)"},
    {"id": "runtime-readiness",       "weight": 0.15, "scale": "1 (not ready) — 5 (fully gated)"},
    {"id": "cognition-maturity",      "weight": 0.15, "scale": "1 (immature) — 5 (mature)"},
    {"id": "user-impact",             "weight": 0.10, "scale": "1 (low) — 5 (high)"},
    {"id": "deployment-safety",       "weight": 0.15, "scale": "1 (unsafe) — 5 (safe by construction)"},
    {"id": "governance-stability",    "weight": 0.10, "scale": "1 (unstable) — 5 (stable)"},
]

CANDIDATES = [
    {
        "id": "contextual-retrieval",
        "scores": {"operational-value": 4, "implementation-complexity": 5, "runtime-readiness": 5,
                   "cognition-maturity": 5, "user-impact": 4, "deployment-safety": 5, "governance-stability": 5},
        "destructive_surface": False,
        "blocking_risks": [],
        "soft_risks": ["no-provenance-emitter"],
    },
    {
        "id": "procedural-assembly-runtime",
        "scores": {"operational-value": 4, "implementation-complexity": 4, "runtime-readiness": 4,
                   "cognition-maturity": 4, "user-impact": 4, "deployment-safety": 4, "governance-stability": 5},
        "destructive_surface": False,
        "blocking_risks": [],
        "soft_risks": ["no-context-vector-emitter", "no-confidence-tier-on-nodes"],
    },
    {
        "id": "operational-copilot",
        "scores": {"operational-value": 5, "implementation-complexity": 2, "runtime-readiness": 3,
                   "cognition-maturity": 4, "user-impact": 5, "deployment-safety": 3, "governance-stability": 4},
        "destructive_surface": False,
        "blocking_risks": ["no-context-vector-emitter", "no-confidence-tier-on-nodes", "no-provenance-emitter"],
        "soft_risks": [],
    },
    {
        "id": "onboarding-runtime",
        "scores": {"operational-value": 4, "implementation-complexity": 3, "runtime-readiness": 2,
                   "cognition-maturity": 4, "user-impact": 4, "deployment-safety": 3, "governance-stability": 4},
        "destructive_surface": False,
        "blocking_risks": ["no-checkpoint-registry", "no-intent-declaration-channel"],
        "soft_risks": [],
    },
    {
        "id": "troubleshooting-runtime",
        "scores": {"operational-value": 5, "implementation-complexity": 2, "runtime-readiness": 1,
                   "cognition-maturity": 2, "user-impact": 5, "deployment-safety": 2, "governance-stability": 3},
        "destructive_surface": False,
        "blocking_risks": ["thin-troubleshooting-corpus", "no-causal-edges-emitted", "no-hypothesis-store"],
        "soft_risks": [],
    },
    {
        "id": "administrator-assistant",
        "scores": {"operational-value": 3, "implementation-complexity": 1, "runtime-readiness": 1,
                   "cognition-maturity": 3, "user-impact": 3, "deployment-safety": 1, "governance-stability": 3},
        "destructive_surface": True,
        "blocking_risks": ["oem-channel-contract-missing", "role-declaration-missing", "no-checkpoint-registry"],
        "soft_risks": [],
    },
]


def weighted_score(c):
    total = 0.0
    for dim in VALUE_DIMENSIONS:
        total += c["scores"][dim["id"]] * dim["weight"]
    return round(total, 3)


for c in CANDIDATES:
    c["weighted_score"] = weighted_score(c)
    c["realizable_now"] = (not c["blocking_risks"]) and (not c["destructive_surface"])

RANKING = sorted(CANDIDATES, key=lambda c: (c["weighted_score"], -len(c["blocking_risks"])), reverse=True)

VALUE_RULES = [
    "Safety > readiness > value: deployment-safety and runtime-readiness dominate value when ranking ties or near-ties occur.",
    "Any candidate with a destructive surface is automatically gated to supervised-runtime phase or higher; never realized in prototype.",
    "A candidate with one or more blocking risks is non-realizable regardless of weighted score.",
    "Soft risks degrade the realization to the next-safer stage but do not block.",
    "Score updates require evidence; ad-hoc reweighting is unsafe.",
]


# ---------------------------------------------------------------------------
# TASK 2 — Vertical slices
# ---------------------------------------------------------------------------

VERTICAL_SLICES = [
    {
        "id": "slice-A-read-only-retrieval",
        "candidate": "contextual-retrieval",
        "kind": "first-runtime / proof-of-value",
        "supervision": "unsupervised (read-only)",
        "exit_criteria": [
            "declared query intents resolvable",
            "stable surfaces enumerated",
            "consumption gates enforceable read-side",
            "provenance manifest attached to each retrieval-package",
        ],
    },
    {
        "id": "slice-B-procedural-assembly",
        "candidate": "procedural-assembly-runtime",
        "kind": "second proof-of-value",
        "supervision": "unsupervised (read-only outputs); supervised when context vector absent",
        "exit_criteria": [
            "ADAPTIVE precedence engine declared (or safest-default fallback active)",
            "COMPOSITION assembly rules enforced",
            "adaptation provenance stamped",
        ],
    },
    {
        "id": "slice-C-supervised-onboarding-pilot",
        "candidate": "onboarding-runtime",
        "kind": "supervised pilot (gated)",
        "supervision": "supervised end-to-end",
        "exit_criteria": [
            "checkpoint registry available",
            "intent declaration channel available",
            "predicate coverage on onboarding flows ≥ declared threshold",
        ],
    },
    {
        "id": "slice-D-supervised-copilot-pilot",
        "candidate": "operational-copilot",
        "kind": "supervised pilot (gated)",
        "supervision": "supervised end-to-end",
        "exit_criteria": [
            "context-vector emitter available",
            "confidence-tier-on-nodes available",
            "provenance emitter available",
            "explicit-action gate available for any future destructive extension",
        ],
    },
    {
        "id": "slice-E-troubleshooting-controlled-pilot",
        "candidate": "troubleshooting-runtime",
        "kind": "deferred (corpus-bound)",
        "supervision": "supervised end-to-end",
        "exit_criteria": [
            "symptom corpus ≥ 10 per product",
            "causal edges emitted",
            "hypothesis store available",
        ],
    },
    {
        "id": "slice-F-administrator-controlled-trial",
        "candidate": "administrator-assistant",
        "kind": "deferred (destructive surface; requires OEM channel)",
        "supervision": "supervised + two-token irreversibility gate",
        "exit_criteria": [
            "OEM channel contract available",
            "role declaration channel available",
            "checkpoint registry available",
            "two-token irreversibility gate operationally available",
        ],
    },
]

SLICE_RULES = [
    "First slice MUST be read-only and have no blocking risks.",
    "Each slice declares supervision posture, exit criteria, and provenance requirements.",
    "Slices are sequenced by safety + readiness, not by value alone.",
    "A slice may not advance to the next staged-rollout phase until its exit criteria are satisfied with evidence.",
    "Deferred slices remain deferred until every declared blocking risk is resolved.",
]


# ---------------------------------------------------------------------------
# TASK 3 — Deployment dependencies
# ---------------------------------------------------------------------------

DEPENDENCIES = [
    {"id": "context-vector-emitter",        "required_by": ["operational-copilot", "procedural-assembly-runtime"], "kind": "cognition"},
    {"id": "confidence-tier-on-nodes",      "required_by": ["operational-copilot", "troubleshooting-runtime", "administrator-assistant"], "kind": "cognition"},
    {"id": "provenance-emitter",            "required_by": ["operational-copilot", "onboarding-runtime", "troubleshooting-runtime", "administrator-assistant"], "kind": "observability"},
    {"id": "incident-id-emitter",           "required_by": ["onboarding-runtime", "troubleshooting-runtime", "operational-copilot"], "kind": "continuity"},
    {"id": "checkpoint-registry",           "required_by": ["onboarding-runtime", "troubleshooting-runtime", "administrator-assistant"], "kind": "continuity"},
    {"id": "fallback-registry",             "required_by": ["operational-copilot", "troubleshooting-runtime"], "kind": "decision"},
    {"id": "intent-declaration-channel",    "required_by": ["onboarding-runtime", "operational-copilot"], "kind": "interop"},
    {"id": "supervision-receipt-emitter",   "required_by": ["operational-copilot", "onboarding-runtime", "administrator-assistant"], "kind": "supervision"},
    {"id": "schema-pin-enforcement",        "required_by": ["all"], "kind": "governance"},
    {"id": "oem-channel-contract",          "required_by": ["administrator-assistant"], "kind": "interop"},
    {"id": "role-declaration-channel",      "required_by": ["administrator-assistant"], "kind": "supervision"},
    {"id": "hypothesis-store",              "required_by": ["troubleshooting-runtime"], "kind": "reasoning"},
    {"id": "causal-edges-emitted",          "required_by": ["troubleshooting-runtime", "operational-copilot"], "kind": "reasoning"},
    {"id": "warning-corpus-complete",       "required_by": ["onboarding-runtime", "troubleshooting-runtime", "operational-copilot", "administrator-assistant"], "kind": "experience"},
    {"id": "symptom-corpus-≥10-per-product","required_by": ["troubleshooting-runtime"], "kind": "knowledge-core"},
]

DEPENDENCY_RULES = [
    "Dependencies are declared; ad-hoc dependencies are unsafe.",
    "A runtime cannot be promoted past supervised-runtime phase while any declared dependency is unmet.",
    "Cross-runtime dependencies follow the federation contracts; never invented at deployment time.",
    "Governance dependencies (schema-pin-enforcement) bind every candidate.",
    "Dependency satisfaction requires evidence (a passing report or a declared emitter).",
]


# ---------------------------------------------------------------------------
# TASK 4 — Staged rollout
# ---------------------------------------------------------------------------

STAGES = [
    {
        "id": "prototype",
        "supervision": "unsupervised allowed only for read-only slices",
        "destructive_allowed": False,
        "evidence": ["builder run", "report files written", "no blocking risks for the slice"],
        "exit_to": "assisted-runtime",
    },
    {
        "id": "assisted-runtime",
        "supervision": "supervised by an operator at every boundary",
        "destructive_allowed": False,
        "evidence": ["loop traces", "supervision receipts", "provenance manifests on every step"],
        "exit_to": "supervised-runtime",
    },
    {
        "id": "supervised-runtime",
        "supervision": "supervised end-to-end; explicit-action gate required for any destructive extension",
        "destructive_allowed": "supervised-only with two-token gate",
        "evidence": ["loop + delegation + handoff traces", "audit append-only log", "no open warnings at completion"],
        "exit_to": "operational-pilot",
    },
    {
        "id": "operational-pilot",
        "supervision": "supervised; bounded user population; explicit success criteria",
        "destructive_allowed": "supervised-only with two-token gate",
        "evidence": ["proof-of-value report", "incident review", "no unresolved escalations", "no contract violations"],
        "exit_to": "controlled-production",
    },
    {
        "id": "controlled-production",
        "supervision": "supervised by SRE/operator on-call; defined kill-switch",
        "destructive_allowed": "supervised-only with two-token gate + audit",
        "evidence": ["controlled-rollout report", "post-deployment review", "regression suite green", "ecosystem observability green"],
        "exit_to": "(no further stage; remains under continuous governance)",
    },
]

STAGE_RULES = [
    "Stages are sequential; no skipping a stage that produced state.",
    "Each stage has explicit supervision posture and evidence requirements.",
    "Promotion to the next stage requires a documented exit decision with provenance.",
    "Demotion (to a prior stage) is always allowed and is the safe response to incidents.",
    "Controlled production remains under continuous governance; it is never a terminal stage of governance.",
]


# ---------------------------------------------------------------------------
# TASK 5 — Operational risks
# ---------------------------------------------------------------------------

OPERATIONAL_RISKS = [
    {"id": "unsafe-runtime-realization",       "severity": "high",   "mitigation": "block any candidate with blocking risks; never realize past prototype with destructive surface uncontracted"},
    {"id": "over-automation",                  "severity": "high",   "mitigation": "supervised-by-default; no autonomous runtime modelled; explicit-action gate mandatory for destructive"},
    {"id": "cognition-drift",                  "severity": "high",   "mitigation": "schema-pin enforcement; append-only history; no runtime-time promotion"},
    {"id": "governance-bypass",                "severity": "high",   "mitigation": "lifecycle P-tier gates enforced at every boundary; federation cannot widen authority"},
    {"id": "escalation-failure",               "severity": "high",   "mitigation": "tier-4/5 require declared receiver; queue + lock when absent; broadcast lock at tier-5"},
    {"id": "operational-hallucination",        "severity": "high",   "mitigation": "retrieval cannot emit nodes absent from knowledge-core; reasoning only on declared causal edges"},
    {"id": "deployment-sequencing-error",      "severity": "high",   "mitigation": "stages sequential; promotion requires evidence; demotion always allowed"},
    {"id": "premature-pilot-promotion",        "severity": "high",   "mitigation": "exit criteria with evidence required; soft risks degrade to safer stage"},
    {"id": "uncontrolled-destructive-surface", "severity": "high",   "mitigation": "two-token irreversibility gate; never inheritable across continuity restoration; audit dedicated"},
    {"id": "supervision-receipt-loss",         "severity": "high",   "mitigation": "supervision receipts mandatory at every supervised boundary; missing receipt = unsafe"},
    {"id": "provenance-loss-at-boundary",      "severity": "high",   "mitigation": "cross-runtime provenance bus required; unattributable messages dropped"},
    {"id": "rollback-unavailability",          "severity": "high",   "mitigation": "checkpoint registry required for any stage past assisted-runtime"},
    {"id": "value-without-readiness",          "severity": "medium", "mitigation": "value cannot dominate ranking; safety > readiness > value rule"},
    {"id": "cognition-to-product-leakage",     "severity": "medium", "mitigation": "transition contracts narrow authority; never widen"},
    {"id": "operator-fatigue",                 "severity": "medium", "mitigation": "supervision boundaries declared; degraded modes prefer safest defaults to minimize unnecessary prompts"},
]


# ---------------------------------------------------------------------------
# TASK 6 — Cognition-to-product transition
# ---------------------------------------------------------------------------

TRANSITION_TARGETS = [
    {"id": "operational-products",            "from": "contextual-retrieval + procedural-assembly", "narrowing": "read-only retrieval surfaces"},
    {"id": "runtime-services",                "from": "any read-only slice",                          "narrowing": "stable APIs bound by access patterns"},
    {"id": "onboarding-systems",              "from": "onboarding-runtime",                            "narrowing": "supervised flows + checkpoints"},
    {"id": "troubleshooting-systems",         "from": "troubleshooting-runtime",                       "narrowing": "supervised flows + hypothesis lifecycle"},
    {"id": "contextual-assistants",           "from": "operational-copilot",                           "narrowing": "supervised contextual guidance, no destructive surface"},
    {"id": "multimodal-operational-ecosystems","from": "any + visual-assistance contract (gated)",     "narrowing": "no image generation; visual-risk freeze contract honored"},
]

TRANSITION_CONTRACTS = [
    "Transition contracts narrow authority; they may never widen it.",
    "Transition contracts preserve all hard exclusions verbatim.",
    "Transition contracts are versioned via schema-pin federation.",
    "Transition contracts cannot promote P-tier or elevate confidence at the boundary.",
    "Transition contracts cannot bypass lifecycle P-tier gates.",
    "Transition contracts are subject to demotion and rollback at any stage.",
]


# ---------------------------------------------------------------------------
# TASK 7 — Deployment governance philosophy
# ---------------------------------------------------------------------------

REALIZATION_PHILOSOPHY = [
    "Realization is earned through evidence, not declared by ambition.",
    "Safety, readiness, and governance stability dominate value in every ranking.",
    "Realization is staged; staged realization is honest realization.",
    "Realization can always be demoted; demotion is the safe response to incidents.",
    "Realization remains subordinate to the governed knowledge-core forever.",
]

STAGED_DEPLOYMENT_DOCTRINE = [
    "Stages are sequential and evidence-gated.",
    "No stage may skip the supervision posture of its predecessor.",
    "Every stage produces audit-grade evidence (traces, receipts, provenance).",
    "Promotion is a documented decision; demotion does not require one.",
]

SAFE_OPERATIONAL_ROLLOUT = [
    "Rollouts are bounded by user population and explicit success criteria.",
    "Rollouts are reversible; kill-switches are declared at supervised-runtime and beyond.",
    "Rollouts honor every prior constitutional layer verbatim.",
    "Rollouts cannot expand authority; they can only operationalize declared authority.",
]

PROOF_OF_VALUE_DOCTRINE = [
    "Proof-of-value is required before promotion past supervised-runtime.",
    "Proof-of-value is measured against declared user impact + safety + readiness.",
    "Proof-of-value reports are append-only and signed with provenance.",
    "Proof-of-value cannot be retroactively assigned.",
]

COGNITION_DEPLOYMENT_GOVERNANCE = [
    "Cognition deployment is the operationalization of declared cognition; it is never the creation of new cognition.",
    "Cognition deployment narrows authority across the transition contract.",
    "Cognition deployment preserves directionality, monotonicity, and provenance.",
    "Cognition deployment is supervised by default.",
]

OPERATIONAL_PRIORITIZATION = [
    "Safety > readiness > value, always.",
    "Destructive surface gates the candidate to supervised-runtime or higher.",
    "Blocking risks gate the candidate to no realization at all.",
    "Soft risks degrade to the next-safer stage.",
    "Ties are broken by deployment-safety and governance-stability, in that order.",
]


# ---------------------------------------------------------------------------
# TASK 8 — Future realization roadmap
# ---------------------------------------------------------------------------

FUTURE_ROADMAP = [
    {"id": "onboarding-runtimes",              "stage_target": "supervised-runtime", "gates": ["checkpoint-registry", "intent-declaration-channel", "warning-corpus-complete"]},
    {"id": "troubleshooting-ecosystems",       "stage_target": "operational-pilot",  "gates": ["symptom-corpus-≥10-per-product", "causal-edges-emitted", "hypothesis-store"]},
    {"id": "contextual-copilots",              "stage_target": "supervised-runtime", "gates": ["context-vector-emitter", "confidence-tier-on-nodes", "provenance-emitter", "supervision-receipt-emitter"]},
    {"id": "multimodal-operational-systems",   "stage_target": "deferred",            "gates": ["visual-risk-freeze-contract", "visual-unavailable-fallback", "no-image-generation hard exclusion preserved"]},
    {"id": "adaptive-operational-assistants",  "stage_target": "supervised-runtime", "gates": ["ADAPTIVE-precedence-engine", "skill-model-emitter", "warning-corpus-complete"]},
    {"id": "future-visual-assistance",         "stage_target": "deferred",            "gates": ["visual-provenance-contract", "no-rendering-runtime hard exclusion preserved"]},
    {"id": "federated-cognition-runtimes",     "stage_target": "controlled-production","gates": ["all interop contracts active", "ecosystem observability green", "schema-pin-federation enforced"]},
]

FUTURE_DOCTRINE = [
    "All future runtime realization remains subordinate to knowledge-core.",
    "All future runtime realization preserves the hard exclusions of every prior layer.",
    "All future runtime realization is staged, supervised, and evidence-gated.",
    "All future runtime realization may be demoted at any time.",
]


# ---------------------------------------------------------------------------
# Realization risks
# ---------------------------------------------------------------------------

REALIZATION_RISKS = [
    {"id": "no-evidence-channel",            "severity": "high",   "impact": "stage promotions cannot be evidence-gated"},
    {"id": "no-supervision-receipt-emitter", "severity": "high",   "impact": "supervised stages cannot satisfy evidence requirements"},
    {"id": "no-provenance-emitter",          "severity": "high",   "impact": "no stage can produce audit-grade evidence"},
    {"id": "no-checkpoint-registry",         "severity": "high",   "impact": "rollback unavailable; controlled-production blocked"},
    {"id": "no-kill-switch-mechanism",       "severity": "high",   "impact": "controlled-production cannot be safely entered"},
    {"id": "no-context-vector-emitter",      "severity": "high",   "impact": "operational-copilot + procedural-assembly cannot promote"},
    {"id": "no-confidence-tier-on-nodes",    "severity": "high",   "impact": "decisioning + reasoning + uncertainty handling all degrade"},
    {"id": "no-incident-id-emitter",         "severity": "high",   "impact": "cross-stage continuity binding unavailable"},
    {"id": "thin-troubleshooting-corpus",    "severity": "high",   "impact": "troubleshooting realization deferred indefinitely on most products"},
    {"id": "warning-corpus-gap",             "severity": "high",   "impact": "guidance realization with mandatory-warning surface gated"},
    {"id": "oem-channel-contract-missing",   "severity": "high",   "impact": "administrator-assistant cannot leave deferred"},
    {"id": "no-rollback-policy",             "severity": "medium", "impact": "demotion path not formalized"},
    {"id": "no-rollout-success-criteria-template", "severity": "medium", "impact": "operational-pilot success cannot be measured"},
    {"id": "no-regression-suite",            "severity": "medium", "impact": "controlled-production exit evidence incomplete"},
    {"id": "no-post-deployment-review-template", "severity": "medium", "impact": "controlled-production audit incomplete"},
]


# ---------------------------------------------------------------------------
# First-production-candidate assessment
# ---------------------------------------------------------------------------

FIRST_PROD_CRITERIA = [
    "no blocking realization risks for the candidate",
    "no destructive surface (or destructive surface fully gated by two-token + role + OEM contract)",
    "evidence channel + provenance emitter + supervision receipt emitter present (for stages ≥ assisted-runtime)",
    "all upstream constitutional layer contracts honored",
    "rollback path defined (checkpoint registry) for stages ≥ supervised-runtime",
]


def assess_first_prod():
    candidates_pass = []
    for c in CANDIDATES:
        if c["destructive_surface"]:
            continue
        if c["blocking_risks"]:
            continue
        candidates_pass.append({
            "id": c["id"],
            "weighted_score": c["weighted_score"],
            "soft_risks": c["soft_risks"],
            "stage_target": "prototype" if c["soft_risks"] else "assisted-runtime",
        })
    candidates_pass.sort(key=lambda x: x["weighted_score"], reverse=True)
    primary = candidates_pass[0] if candidates_pass else None
    secondary = candidates_pass[1] if len(candidates_pass) > 1 else None
    return {
        "criteria": FIRST_PROD_CRITERIA,
        "primary_first_production_candidate": primary,
        "secondary_first_production_candidate": secondary,
        "deferred_candidates": [
            {"id": c["id"], "blocking_risks": c["blocking_risks"], "destructive_surface": c["destructive_surface"]}
            for c in CANDIDATES if c["blocking_risks"] or c["destructive_surface"]
        ],
        "doctrine": "no slice is realised while any declared blocking-risk for that slice remains unresolved",
    }


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build():
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    (CONST_ROOT / "README.md").write_text(
        "# REALIZATION & DEPLOYMENT GOVERNANCE\n\n"
        "Seventeenth constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all sixteen prior governance layers.\n\n"
        "Defines how the cognition ecosystem transitions into real operational systems through "
        "staged realization, deployment prioritization, runtime sequencing, and operational value "
        "optimization. It does not implement production runtimes, agents, chatbots, frontends, "
        "image generators, PDF renderers, or autonomous cognition.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Realization & Deployment Governance",
        "Declares the principles and authority of this layer. Subordinate to knowledge-core and to all sixteen prior governance layers.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Authority", md_list(CHARTER_AUTHORITY)),
            ("Hard Exclusions", md_list([
                "DO NOT implement production runtimes",
                "DO NOT build chatbots",
                "DO NOT generate images",
                "DO NOT create PDFs",
                "DO NOT implement autonomous cognition",
                "DO NOT build frontend systems",
            ])),
        ],
        {
            "schema": SCHEMA, "kind": "charter",
            "principles": CHARTER_PRINCIPLES, "authority": CHARTER_AUTHORITY,
            "subordinate_to": [
                "knowledge-core",
                "VISUAL", "KNOWLEDGE_CENTER", "SEMANTIC", "EXPERIENCE",
                "LIFECYCLE", "VALIDATION", "ACCESS_AND_CONSUMPTION", "COMPOSITION",
                "EXECUTION", "ADAPTIVE_OPERATIONAL", "DECISION_INTELLIGENCE",
                "REASONING", "CONTINUITY", "RUNTIME", "RUNTIME_ORCHESTRATION",
                "ECOSYSTEM_INTEROPERABILITY",
            ],
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "value-prioritization", "value-prioritization",
        "Operational Value Prioritization",
        "Weighted scoring rubric and ranking of all candidate runtime realizations. Safety > readiness > value.",
        [
            ("Dimensions", md_list([f"`{d['id']}` (weight: {d['weight']}, {d['scale']})" for d in VALUE_DIMENSIONS])),
            ("Candidates (ranked)", md_list([
                f"`{c['id']}` — score: {c['weighted_score']} — destructive: {c['destructive_surface']} — "
                f"blocking: {len(c['blocking_risks'])} — realizable now: {c['realizable_now']}"
                for c in RANKING
            ])),
            ("Rules", md_list(VALUE_RULES)),
        ],
        {
            "schema": SCHEMA, "kind": "value-prioritization",
            "dimensions": VALUE_DIMENSIONS,
            "candidates": CANDIDATES,
            "ranking": [c["id"] for c in RANKING],
            "rules": VALUE_RULES,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "vertical-slices", "vertical-slices",
        "Vertical Slice Realization",
        "Declared catalog of vertical realization slices, each with supervision posture and exit criteria.",
        [
            ("Slices", md_list([f"`{s['id']}` — candidate: {s['candidate']} — kind: {s['kind']}" for s in VERTICAL_SLICES])),
            ("Rules", md_list(SLICE_RULES)),
        ],
        {"schema": SCHEMA, "kind": "vertical-slices", "slices": VERTICAL_SLICES, "rules": SLICE_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "dependencies", "dependencies",
        "Deployment Dependencies",
        "Declared deployment dependencies across runtime / cognition / orchestration / interop / governance layers.",
        [
            ("Dependencies", md_list([f"`{d['id']}` (kind: {d['kind']}) → required by: {', '.join(d['required_by'])}" for d in DEPENDENCIES])),
            ("Rules", md_list(DEPENDENCY_RULES)),
        ],
        {"schema": SCHEMA, "kind": "dependencies", "dependencies": DEPENDENCIES, "rules": DEPENDENCY_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "staged-rollout", "staged-rollout",
        "Staged Realization Strategy",
        "Five sequential stages from prototype to controlled production. Each stage has explicit supervision posture, evidence requirements, and exit decision.",
        [
            ("Stages", md_list([f"`{s['id']}` → exit_to: {s['exit_to']}" for s in STAGES])),
            ("Rules", md_list(STAGE_RULES)),
        ],
        {"schema": SCHEMA, "kind": "staged-rollout", "stages": STAGES, "rules": STAGE_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "risk-prioritization", "risk-prioritization",
        "Operational Risk Prioritization",
        "Operational risk taxonomy with mitigation rules.",
        [
            ("Risks", md_list([f"`{r['id']}` ({r['severity']}) — {r['mitigation']}" for r in OPERATIONAL_RISKS])),
        ],
        {"schema": SCHEMA, "kind": "risk-prioritization", "risks": OPERATIONAL_RISKS, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "product-transition", "product-transition",
        "Cognition-to-Product Transition",
        "Declared transition targets and contracts. Transition contracts narrow authority; they may never widen it.",
        [
            ("Transition targets", md_list([f"`{t['id']}` — from: {t['from']} — narrowing: {t['narrowing']}" for t in TRANSITION_TARGETS])),
            ("Transition contracts", md_list(TRANSITION_CONTRACTS)),
        ],
        {"schema": SCHEMA, "kind": "product-transition", "targets": TRANSITION_TARGETS, "contracts": TRANSITION_CONTRACTS, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "deployment-governance", "deployment-governance",
        "Deployment Governance Doctrine",
        "Philosophy + doctrine for realization, staged deployment, safe rollout, proof-of-value, cognition deployment, and operational prioritization.",
        [
            ("Realization philosophy", md_list(REALIZATION_PHILOSOPHY)),
            ("Staged deployment doctrine", md_list(STAGED_DEPLOYMENT_DOCTRINE)),
            ("Safe operational rollout philosophy", md_list(SAFE_OPERATIONAL_ROLLOUT)),
            ("Proof-of-value doctrine", md_list(PROOF_OF_VALUE_DOCTRINE)),
            ("Cognition deployment governance", md_list(COGNITION_DEPLOYMENT_GOVERNANCE)),
            ("Operational prioritization principles", md_list(OPERATIONAL_PRIORITIZATION)),
        ],
        {
            "schema": SCHEMA, "kind": "deployment-governance",
            "philosophy": REALIZATION_PHILOSOPHY,
            "staged_doctrine": STAGED_DEPLOYMENT_DOCTRINE,
            "safe_rollout": SAFE_OPERATIONAL_ROLLOUT,
            "proof_of_value": PROOF_OF_VALUE_DOCTRINE,
            "cognition_deployment": COGNITION_DEPLOYMENT_GOVERNANCE,
            "prioritization": OPERATIONAL_PRIORITIZATION,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "future-realization-roadmap", "future-realization-roadmap",
        "Future Realization Roadmap",
        "Declared future runtime targets, their stage targets, and per-target gates. All realization remains subordinate to the governed knowledge-core.",
        [
            ("Roadmap", md_list([f"`{r['id']}` → stage_target: {r['stage_target']} — gates: {len(r['gates'])}" for r in FUTURE_ROADMAP])),
            ("Doctrine", md_list(FUTURE_DOCTRINE)),
        ],
        {"schema": SCHEMA, "kind": "future-realization-roadmap", "roadmap": FUTURE_ROADMAP, "doctrine": FUTURE_DOCTRINE, "generated": now_iso()},
    )

    first_prod = assess_first_prod()

    reports = [
        ("01-operational-value-summary.json", {
            "schema": SCHEMA,
            "dimensions": VALUE_DIMENSIONS,
            "ranking": [{"id": c["id"], "weighted_score": c["weighted_score"], "destructive_surface": c["destructive_surface"], "blocking_risks": c["blocking_risks"], "soft_risks": c["soft_risks"]} for c in RANKING],
            "rules": VALUE_RULES,
        }),
        ("02-vertical-slice-summary.json", {
            "schema": SCHEMA,
            "slices": VERTICAL_SLICES,
            "rules": SLICE_RULES,
        }),
        ("03-deployment-dependency-summary.json", {
            "schema": SCHEMA,
            "dependencies": DEPENDENCIES,
            "by_kind": sorted({d["kind"] for d in DEPENDENCIES}),
            "rules": DEPENDENCY_RULES,
        }),
        ("04-staged-rollout-summary.json", {
            "schema": SCHEMA,
            "stages": STAGES,
            "rules": STAGE_RULES,
        }),
        ("05-operational-risk-summary.json", {
            "schema": SCHEMA,
            "risks": OPERATIONAL_RISKS,
            "high": [r["id"] for r in OPERATIONAL_RISKS if r["severity"] == "high"],
            "medium": [r["id"] for r in OPERATIONAL_RISKS if r["severity"] == "medium"],
        }),
        ("06-cognition-to-product-summary.json", {
            "schema": SCHEMA,
            "targets": TRANSITION_TARGETS,
            "contracts": TRANSITION_CONTRACTS,
        }),
        ("07-deployment-governance-summary.json", {
            "schema": SCHEMA,
            "philosophy_principles": len(REALIZATION_PHILOSOPHY),
            "staged_doctrine": len(STAGED_DEPLOYMENT_DOCTRINE),
            "safe_rollout": len(SAFE_OPERATIONAL_ROLLOUT),
            "proof_of_value": len(PROOF_OF_VALUE_DOCTRINE),
            "cognition_deployment": len(COGNITION_DEPLOYMENT_GOVERNANCE),
            "prioritization": len(OPERATIONAL_PRIORITIZATION),
        }),
        ("08-future-realization-roadmap-summary.json", {
            "schema": SCHEMA,
            "roadmap": FUTURE_ROADMAP,
            "doctrine": FUTURE_DOCTRINE,
        }),
        ("09-unresolved-realization-risks.json", {
            "schema": SCHEMA,
            "risks": REALIZATION_RISKS,
            "total": len(REALIZATION_RISKS),
            "high": [r["id"] for r in REALIZATION_RISKS if r["severity"] == "high"],
            "medium": [r["id"] for r in REALIZATION_RISKS if r["severity"] == "medium"],
        }),
        ("10-first-production-candidate-assessment.json", {
            "schema": SCHEMA,
            **first_prod,
        }),
    ]

    for name, payload in reports:
        (REPORTS_ROOT / name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    file_count = sum(1 for _ in CONST_ROOT.rglob("*") if _.is_file())
    high_realization_risks = [r["id"] for r in REALIZATION_RISKS if r["severity"] == "high"]

    print(
        "Realization & deployment prioritization modeling complete.\n"
        f"  Constitutional root: {CONST_ROOT}\n"
        f"  Reports: {REPORTS_ROOT}/01..10\n"
        f"  Candidates: {len(CANDIDATES)} | Slices: {len(VERTICAL_SLICES)} | Dependencies: {len(DEPENDENCIES)} | "
        f"Stages: {len(STAGES)} | Operational risks: {len(OPERATIONAL_RISKS)} | "
        f"Realization risks: {len(REALIZATION_RISKS)} (high: {len(high_realization_risks)}).\n"
        f"  Top-ranked: {RANKING[0]['id']} (score: {RANKING[0]['weighted_score']}, realizable now: {RANKING[0]['realizable_now']}).\n"
        f"  First production candidate: {first_prod['primary_first_production_candidate']['id'] if first_prod['primary_first_production_candidate'] else 'none'}.\n"
        f"  Files written under constitutional root: {file_count}"
    )


if __name__ == "__main__":
    build()
