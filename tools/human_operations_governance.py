"""
Phase 30 — HUMAN OPERATIONAL EXPERIENCE & EXECUTABLE WORKFLOW DESIGN.

Constitutional layer 24. Modeling-only. Subordinate to knowledge-core and
to all twenty-three prior governance layers.

Writes:
  - the seven human-operations artifact folders under
    `wp-content/themes/beslock-custom/User manuals/human-operations/`
  - the doctrine root at
    `wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/HUMAN_OPERATIONS_GOVERNANCE/`
  - the ten final reports under
    `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/human-operations/01..10`

Idempotent. Non-destructive. Reads no per-product knowledge-core JSON.
No frontends, no production UI, no autonomous operators, no deployment.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
HOPS_ROOT = THEME_ROOT / "human-operations"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "HUMAN_OPERATIONS_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "human-operations"

SCHEMA = "human-operations-governance/1.0"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def md_list(items): return "\n".join(f"- {x}" for x in items)


def write_pair(folder: Path, slug: str, title: str, intro: str, sections, payload: dict):
    folder.mkdir(parents=True, exist_ok=True)
    md = [f"# {title}", "", intro, ""]
    for h, body in sections:
        md += [f"## {h}", "", body, ""]
    (folder / f"{slug}.md").write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")
    (folder / f"{slug}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


SUBORDINATE_TO = [
    "knowledge-core",
    "VISUAL", "KNOWLEDGE_CENTER", "SEMANTIC", "EXPERIENCE",
    "LIFECYCLE", "VALIDATION", "ACCESS_AND_CONSUMPTION", "COMPOSITION",
    "EXECUTION", "ADAPTIVE_OPERATIONAL", "DECISION_INTELLIGENCE",
    "REASONING", "CONTINUITY", "RUNTIME", "RUNTIME_ORCHESTRATION",
    "ECOSYSTEM_INTEROPERABILITY", "REALIZATION_AND_DEPLOYMENT",
    "OPERATIONAL_PROOF", "PROTOTYPE_RUNTIME", "RUNTIME_IMPLEMENTATION",
    "RUNTIME_HARDENING", "KNOWLEDGE_LIFECYCLE", "KNOWLEDGE_OPERATIONS",
]


# =============================================================================
# TASK 1 — OPERATOR EXPERIENCE
# =============================================================================

OPERATOR_PROFILES = [
    {"id": "runtime-operator",        "primary_surface": "supervised flow CLI",       "decisions": ["approve", "reject", "demote"], "audit_required": True},
    {"id": "reviewer",                "primary_surface": "reviewer-workbench panels", "decisions": ["approve", "reject", "request-evidence", "open-dispute"], "audit_required": True},
    {"id": "governance-maintainer",   "primary_surface": "governance console",        "decisions": ["assign", "revoke", "scope-edit (within charter)"], "audit_required": True},
    {"id": "escalation-supervisor",   "primary_surface": "escalation console",        "decisions": ["accept-handoff", "route", "halt-slice", "request-dual-review"], "audit_required": True},
    {"id": "oem-reviewer",            "primary_surface": "OEM evidence panel",        "decisions": ["bind-source", "reject-source", "supersede-source"], "audit_required": True},
    {"id": "operational-auditor",     "primary_surface": "audit console (read-only)", "decisions": ["raise-finding", "request-replay"], "audit_required": True},
]

INTERACTION_PRINCIPLES = [
    "Every operator action emits a supervision-receipt; no silent action exists.",
    "Every operator surface declares its scope; out-of-scope actions are not exposed.",
    "Every operator decision is reversible by an equal-or-higher governance decision.",
    "Operators see provenance before they see conclusions.",
    "Operators see uncertainty before they see recommendations.",
]


# =============================================================================
# TASK 2 — EXECUTABLE WORKFLOWS
# =============================================================================

EXECUTABLE_WORKFLOWS = [
    {"id": "onboarding-execution",     "primary_actor": "runtime-operator",      "checkpoints": ["pre-emission", "post-emission"], "halts_on": ["safety-demote"]},
    {"id": "troubleshooting-execution","primary_actor": "runtime-operator",      "checkpoints": ["pre-emission", "candidate-only-disclosure"], "halts_on": ["candidate-only + irreversible-adjacent"]},
    {"id": "escalation-review",        "primary_actor": "escalation-supervisor", "checkpoints": ["accept-handoff", "route-decision", "post-route"], "halts_on": ["unresolved disagreement"]},
    {"id": "candidate-review",         "primary_actor": "reviewer",              "checkpoints": ["evidence-pull", "approve-or-reject", "post-audit"], "halts_on": ["missing-binding"]},
    {"id": "oem-verification",         "primary_actor": "oem-reviewer",          "checkpoints": ["binding-attached", "dual-review", "post-supersession"], "halts_on": ["dual-review-disagreement"]},
    {"id": "rollback-handling",        "primary_actor": "governance-maintainer", "checkpoints": ["target-confirm", "fanout-preview", "post-rollback"], "halts_on": ["fanout-exceeds-declared-scope"]},
    {"id": "runtime-incident-review",  "primary_actor": "operational-auditor",   "checkpoints": ["incident-claim", "replay-validate", "finding-emit"], "halts_on": ["replay-drift-exceeds-floor"]},
]

WORKFLOW_INVARIANTS = [
    "every workflow step is a declared checkpoint with a declared decision set",
    "every workflow halt is a declared, observable event — never a silent stall",
    "every workflow emits an append-only orchestration-trace record",
    "no workflow may auto-resume after a halt without an operator decision",
    "no workflow may bypass its declared checkpoints under any condition",
]


# =============================================================================
# TASK 3 — OPERATIONAL CONSOLES
# =============================================================================

CONSOLES = [
    {"id": "runtime-console",      "audience": "runtime-operator",      "surfaces": ["flow start", "retrieval-package preview", "approve/reject/demote"]},
    {"id": "reviewer-console",     "audience": "reviewer",              "surfaces": ["queue claim", "side-by-side OEM", "evidence attach", "approve/reject"]},
    {"id": "escalation-console",   "audience": "escalation-supervisor", "surfaces": ["incoming handoffs", "trigger explanation", "route choices"]},
    {"id": "governance-console",   "audience": "governance-maintainer", "surfaces": ["reviewer registry", "scope edits (within charter)", "emergency demotion"]},
    {"id": "audit-console",        "audience": "operational-auditor",   "surfaces": ["read-only event stream", "replay", "finding emission"]},
    {"id": "continuity-console",   "audience": "runtime-operator + escalation-supervisor", "surfaces": ["checkpoint timeline", "resume-from-checkpoint", "snapshot inspect"]},
]

CONSOLE_DESIGN_RULES = [
    "consoles are operator surfaces, not consumer applications",
    "consoles never render speculative content; only declared events and packages",
    "consoles always show provenance + confidence + uncertainty alongside any recommendation",
    "consoles never expose actions outside the operator's declared scope",
    "consoles emit append-only events for every operator action",
    "consoles are out of scope here as implementations; this layer is design-only",
]


# =============================================================================
# TASK 4 — EXPLAINABILITY
# =============================================================================

EXPLAINABILITY_PATTERNS = [
    {"id": "retrieval-reasoning",        "shows": ["query tokens", "matched node tokens", "Jaccard score", "confidence weight", "final score"]},
    {"id": "escalation-trigger",         "shows": ["trigger id", "underlying signal", "rule that fired", "next required actor"]},
    {"id": "confidence-disclosure",      "shows": ["per-node tier", "tier weight", "candidate_only flag", "human-review status"]},
    {"id": "provenance-inspection",      "shows": ["manifest_id", "source_files[].sha256", "extract_lineage", "binding chain"]},
    {"id": "continuity-visualization",   "shows": ["checkpoint timeline", "current snapshot id", "resume points", "last continuity-trace event"]},
    {"id": "operational-uncertainty",    "shows": ["ambiguous=True", "no-results", "candidate-only", "missing-prerequisite"]},
]

EXPLAINABILITY_INVARIANTS = [
    "explanation is sourced from append-only logs, never from speculation",
    "explanation always precedes the recommendation in the operator surface",
    "explanation is reproducible: same logs → same explanation",
    "explanation does not editorialize: it surfaces declared fields, not narratives",
    "explanation never conceals uncertainty to improve operator UX",
]


# =============================================================================
# TASK 5 — SAFE HITL PATTERNS
# =============================================================================

HITL_PATTERNS = [
    {"id": "interruption",             "trigger": "operator-initiated halt",                         "effect": "slice halts at next safe checkpoint"},
    {"id": "approval-checkpoint",      "trigger": "declared checkpoint",                             "effect": "wait for approve|reject|demote"},
    {"id": "escalation-intervention",  "trigger": "escalation-trace event",                          "effect": "route to escalation-supervisor"},
    {"id": "unsafe-runtime-interruption","trigger": "safety predicate failure",                       "effect": "demote slice; halt; emit operational-audit-log"},
    {"id": "operator-override",        "trigger": "operator decision contradicting recommendation",  "effect": "logged with rationale; never silent"},
    {"id": "reviewer-arbitration",     "trigger": "reviewer disagreement on a node",                 "effect": "open consensus review; cap node tier until resolved"},
    {"id": "governance-intervention",  "trigger": "governance-operator emergency action",            "effect": "append-only event + 24h auditor co-signature"},
]

HITL_INVARIANTS = [
    "no HITL pattern allows silent override",
    "no HITL pattern allows scope expansion",
    "every HITL action is reversible by an equal-or-higher decision",
    "every HITL action carries an operator identity + supervision-receipt",
    "HITL is the default; autonomous bypass does not exist at any operator surface",
]


# =============================================================================
# TASK 6 — NAVIGATION
# =============================================================================

NAVIGATION_SYSTEMS = [
    {"id": "operational-traversal",    "description": "moving across declared workflow steps within a slice"},
    {"id": "workflow-progression",     "description": "advancing checkpoint-by-checkpoint with explicit decisions"},
    {"id": "continuity-restoration",   "description": "resuming from a declared continuity-checkpoint snapshot"},
    {"id": "troubleshooting-navigation","description": "walking causal-graph edges + candidate troubleshooting hits"},
    {"id": "escalation-navigation",    "description": "moving across escalation tiers along declared monotonic transitions"},
    {"id": "reviewer-navigation",      "description": "queue → claim → evidence → decision → audit, in declared order"},
]

NAVIGATION_INVARIANTS = [
    "navigation is bounded by declared edges; ad-hoc jumps are forbidden",
    "navigation surfaces always show the current checkpoint and the next required decision",
    "navigation never silently skips a checkpoint",
    "navigation never silently rolls back; rollback is an explicit operator action",
    "navigation is product-scoped; cross-product navigation is forbidden",
]


# =============================================================================
# TASK 7 — ERGONOMICS
# =============================================================================

ERGONOMIC_PRINCIPLES = [
    {"id": "cognitive-load-reduction",  "rule": "show at most one decision per checkpoint; defer secondary information to expandable detail"},
    {"id": "operational-fatigue-prevention", "rule": "queues respect declared SLA tiers; no operator is auto-assigned beyond declared capacity ceiling"},
    {"id": "escalation-fatigue",        "rule": "repeated escalations from the same trigger collapse into one tracked incident, not N notifications"},
    {"id": "reviewer-overload",         "rule": "reviewer registry declares per-reviewer concurrent claim ceiling"},
    {"id": "ambiguity-minimization",    "rule": "every screen states what is known, what is uncertain, and the next required action"},
    {"id": "guided-operational-sequencing", "rule": "checkpoints are presented in a single declared order; no parallel competing decision surfaces"},
]

ERGONOMIC_DISCIPLINE = [
    "ergonomics never override safety predicates",
    "ergonomics never compress disclosure of irreversibility or uncertainty",
    "ergonomics never replace required dual-review with single-click flows",
    "ergonomics never auto-default approval; default is always 'pending operator decision'",
]


# =============================================================================
# TASK 8 — DOCTRINE
# =============================================================================

CHARTER_PRINCIPLES = [
    "This layer governs how humans interact with the operational cognition runtime.",
    "All human interaction is supervised, append-only, and reversible.",
    "All human interaction surfaces show provenance and uncertainty before recommendation.",
    "All human interaction respects the operator's declared scope and tier_ceiling.",
    "No autonomous operator path exists at any human-interaction surface.",
    "No production frontend, no consumer UI, no chatbot UX is in scope.",
    "All human interaction is subordinate to provenance and to all 23 prior governance layers.",
]

HUMAN_OPERATIONAL_PHILOSOPHY = [
    "Humans operate the runtime; the runtime never operates the humans.",
    "Humans see provenance before conclusions, uncertainty before recommendations.",
    "Humans hold the override; the runtime holds the audit trail.",
    "Humans set pace; the runtime never pressures a decision.",
]

SUPERVISED_INTERACTION_DOCTRINE = [
    "Every interaction is bound to a supervision-receipt.",
    "Every interaction is bound to an operator identity.",
    "Every interaction is bound to a declared checkpoint and a declared decision set.",
    "Every interaction is reversible by an equal-or-higher governance decision.",
]

EXPLAINABILITY_PHILOSOPHY = [
    "Explanation is a first-class surface, not a footer.",
    "Explanation is sourced from append-only logs, never from speculation.",
    "Explanation surfaces declared fields, not narratives.",
    "Explanation never conceals uncertainty to improve UX.",
]

OPERATIONAL_ERGONOMICS_DOCTRINE = [
    "Ergonomics reduce cognitive load; they never reduce safety.",
    "Ergonomics never compress required disclosure.",
    "Ergonomics never auto-default approval.",
    "Ergonomics defer to governance whenever they conflict with it.",
]

HUMAN_RUNTIME_COLLABORATION_PRINCIPLES = [
    "Collaboration is human-led; the runtime is supervised by default.",
    "Collaboration is bounded by declared scope on both sides.",
    "Collaboration is auditable end-to-end via the supervision-receipt + observability channels.",
    "Collaboration is reversible; rollback is a first-class operator action.",
]

SAFE_GOVERNANCE_INTERACTION_PHILOSOPHY = [
    "Governance interaction is dual-audited; no governance action is single-eyed.",
    "Governance interaction respects the no-self-approval rule.",
    "Governance interaction never silently expands scope.",
    "Governance interaction always carries an explicit rationale.",
]


# =============================================================================
# TASK 9 — FUTURE OPERATOR ECOSYSTEM
# =============================================================================

FUTURE_COMMITMENTS = [
    "reviewer ecosystems grow through the reviewer registry; revocation remains a first-class event",
    "governance teams partition by scope (domain × product); no global override is ever introduced",
    "operational support teams operate from append-only logs; no out-of-band edits",
    "supervised copilots, if introduced, must satisfy: (a) operator-led activation, (b) per-checkpoint approval, (c) full provenance disclosure, (d) reversibility",
    "runtime supervision centers, if introduced, are observation surfaces over the same NDJSON channels; they never bypass operator decisions",
    "future operational consoles inherit all invariants in this layer; new consoles are not new architecture",
]

FUTURE_INVARIANTS = [
    "no autonomous operator path is ever introduced",
    "no operator surface ever omits provenance or uncertainty",
    "no operator surface ever auto-defaults approval",
    "no operator surface ever bypasses the supervision-receipt",
    "no macro-governance mega-layer is spawned by human-operations work",
]


# =============================================================================
# BUILD
# =============================================================================

def build():
    HOPS_ROOT.mkdir(parents=True, exist_ok=True)
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    # --- Task 1 ----------------------------------------------------------
    write_pair(
        HOPS_ROOT / "operator-experience", "operator-experience",
        "Operator Experience Model",
        "Six declared operator profiles + interaction principles for safe, supervised use.",
        [
            ("Operator profiles", md_list([f"`{p['id']}` — surface: {p['primary_surface']}; decisions: " + ", ".join(p['decisions']) for p in OPERATOR_PROFILES])),
            ("Interaction principles", md_list(INTERACTION_PRINCIPLES)),
        ],
        {"schema": SCHEMA, "kind": "operator-experience",
         "operator_profiles": OPERATOR_PROFILES,
         "interaction_principles": INTERACTION_PRINCIPLES},
    )

    # --- Task 2 ----------------------------------------------------------
    write_pair(
        HOPS_ROOT / "workflows", "workflows",
        "Executable Workflow Design",
        "Seven declared executable workflows with checkpoints, halt conditions, and primary actors.",
        [
            ("Workflows", md_list([f"`{w['id']}` — actor: {w['primary_actor']}; checkpoints: " + ", ".join(w['checkpoints']) + f"; halts on: " + ", ".join(w['halts_on']) for w in EXECUTABLE_WORKFLOWS])),
            ("Workflow invariants", md_list(WORKFLOW_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "executable-workflows",
         "workflows": EXECUTABLE_WORKFLOWS,
         "workflow_invariants": WORKFLOW_INVARIANTS},
    )

    # --- Task 3 ----------------------------------------------------------
    write_pair(
        HOPS_ROOT / "consoles", "consoles",
        "Operational Console Modeling",
        "Six operator consoles, design-only — no implementation in this layer.",
        [
            ("Consoles", md_list([f"`{c['id']}` — audience: {c['audience']}; surfaces: " + ", ".join(c['surfaces']) for c in CONSOLES])),
            ("Console design rules", md_list(CONSOLE_DESIGN_RULES)),
        ],
        {"schema": SCHEMA, "kind": "consoles",
         "consoles": CONSOLES,
         "console_design_rules": CONSOLE_DESIGN_RULES},
    )

    # --- Task 4 ----------------------------------------------------------
    write_pair(
        HOPS_ROOT / "explainability", "explainability",
        "Runtime Explainability UX",
        "Six explanation patterns, each sourced from append-only logs and reproducible.",
        [
            ("Explainability patterns", md_list([f"`{p['id']}` — shows: " + ", ".join(p['shows']) for p in EXPLAINABILITY_PATTERNS])),
            ("Invariants", md_list(EXPLAINABILITY_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "explainability",
         "explainability_patterns": EXPLAINABILITY_PATTERNS,
         "explainability_invariants": EXPLAINABILITY_INVARIANTS},
    )

    # --- Task 5 ----------------------------------------------------------
    write_pair(
        HOPS_ROOT / "hitl-patterns", "hitl-patterns",
        "Safe Human-in-the-Loop Patterns",
        "Seven declared HITL patterns; HITL is the default and cannot be silently bypassed.",
        [
            ("Patterns", md_list([f"`{p['id']}` — trigger: {p['trigger']}; effect: {p['effect']}" for p in HITL_PATTERNS])),
            ("Invariants", md_list(HITL_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "hitl-patterns",
         "hitl_patterns": HITL_PATTERNS,
         "hitl_invariants": HITL_INVARIANTS},
    )

    # --- Task 6 ----------------------------------------------------------
    write_pair(
        HOPS_ROOT / "navigation", "navigation",
        "Operational Navigation Systems",
        "Six navigation systems bounded by declared edges; no ad-hoc jumps; product-scoped.",
        [
            ("Navigation systems", md_list([f"`{n['id']}` — {n['description']}" for n in NAVIGATION_SYSTEMS])),
            ("Invariants", md_list(NAVIGATION_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "navigation",
         "navigation_systems": NAVIGATION_SYSTEMS,
         "navigation_invariants": NAVIGATION_INVARIANTS},
    )

    # --- Task 7 ----------------------------------------------------------
    write_pair(
        HOPS_ROOT / "ergonomics", "ergonomics",
        "Workflow Ergonomics & Cognitive Load",
        "Six ergonomic principles bounded by safety discipline; ergonomics never override safety.",
        [
            ("Ergonomic principles", md_list([f"`{e['id']}` — {e['rule']}" for e in ERGONOMIC_PRINCIPLES])),
            ("Discipline", md_list(ERGONOMIC_DISCIPLINE)),
        ],
        {"schema": SCHEMA, "kind": "ergonomics",
         "ergonomic_principles": ERGONOMIC_PRINCIPLES,
         "ergonomic_discipline": ERGONOMIC_DISCIPLINE},
    )

    # --- Task 8 — doctrine root ------------------------------------------
    (CONST_ROOT / "README.md").write_text(
        "# HUMAN OPERATIONS GOVERNANCE\n\n"
        "Twenty-fourth constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all twenty-three prior governance layers.\n\n"
        "Governs how humans safely interact with the operational cognition runtime: "
        "operator profiles, executable workflows, consoles, explainability, HITL patterns, "
        "navigation, and ergonomics.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Human Operations Governance",
        "Declares principles + authority for safe, supervised, reversible human interaction.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Bound artifacts", md_list([
                "`wp-content/themes/beslock-custom/User manuals/human-operations/operator-experience/`",
                "`wp-content/themes/beslock-custom/User manuals/human-operations/workflows/`",
                "`wp-content/themes/beslock-custom/User manuals/human-operations/consoles/`",
                "`wp-content/themes/beslock-custom/User manuals/human-operations/explainability/`",
                "`wp-content/themes/beslock-custom/User manuals/human-operations/hitl-patterns/`",
                "`wp-content/themes/beslock-custom/User manuals/human-operations/navigation/`",
                "`wp-content/themes/beslock-custom/User manuals/human-operations/ergonomics/`",
            ])),
            ("Hard Exclusions", md_list([
                "DO NOT build production frontend systems",
                "DO NOT implement autonomous operators",
                "DO NOT create visual UI themes",
                "DO NOT expand cognition architecture recursively",
                "DO NOT deploy production applications",
            ])),
        ],
        {"schema": SCHEMA, "kind": "charter",
         "principles": CHARTER_PRINCIPLES,
         "subordinate_to": SUBORDINATE_TO,
         "generated": now_iso()},
    )

    for slug, title, intro, principles in [
        ("human-operational-philosophy", "Human Operational Philosophy",
         "Humans operate the runtime; the runtime never operates the humans.",
         HUMAN_OPERATIONAL_PHILOSOPHY),
        ("supervised-interaction-doctrine", "Supervised Interaction Doctrine",
         "Every interaction is bound to identity, checkpoint, decision set, and supervision-receipt.",
         SUPERVISED_INTERACTION_DOCTRINE),
        ("explainability-philosophy", "Explainability Philosophy",
         "Explanation is first-class, sourced from logs, never conceals uncertainty.",
         EXPLAINABILITY_PHILOSOPHY),
        ("operational-ergonomics-doctrine", "Operational Ergonomics Doctrine",
         "Ergonomics reduce cognitive load; they never reduce safety.",
         OPERATIONAL_ERGONOMICS_DOCTRINE),
        ("human-runtime-collaboration-principles", "Human-Runtime Collaboration Principles",
         "Human-led, scope-bounded, end-to-end auditable, reversible.",
         HUMAN_RUNTIME_COLLABORATION_PRINCIPLES),
        ("safe-governance-interaction-philosophy", "Safe Governance Interaction Philosophy",
         "Dual-audited, no self-approval, no silent scope expansion, explicit rationale.",
         SAFE_GOVERNANCE_INTERACTION_PHILOSOPHY),
    ]:
        write_pair(
            CONST_ROOT / slug, slug, title, intro,
            [("Principles", md_list(principles))],
            {"schema": SCHEMA, "kind": slug, "principles": principles},
        )

    # --- Final 10 reports ------------------------------------------------
    reports = [
        ("01-operator-experience-summary.json", {
            "schema": SCHEMA, "kind": "operator-experience-summary",
            "operator_profiles": [p["id"] for p in OPERATOR_PROFILES],
            "interaction_principles_count": len(INTERACTION_PRINCIPLES),
            "artifact": "wp-content/themes/beslock-custom/User manuals/human-operations/operator-experience/",
        }),
        ("02-executable-workflow-summary.json", {
            "schema": SCHEMA, "kind": "executable-workflow-summary",
            "workflows": [w["id"] for w in EXECUTABLE_WORKFLOWS],
            "workflow_invariants_count": len(WORKFLOW_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/human-operations/workflows/",
        }),
        ("03-console-model-summary.json", {
            "schema": SCHEMA, "kind": "console-model-summary",
            "consoles": [c["id"] for c in CONSOLES],
            "console_design_rules_count": len(CONSOLE_DESIGN_RULES),
            "implementation_status": "design-only (no implementation in this layer)",
            "artifact": "wp-content/themes/beslock-custom/User manuals/human-operations/consoles/",
        }),
        ("04-explainability-summary.json", {
            "schema": SCHEMA, "kind": "explainability-summary",
            "patterns": [p["id"] for p in EXPLAINABILITY_PATTERNS],
            "invariants_count": len(EXPLAINABILITY_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/human-operations/explainability/",
        }),
        ("05-hitl-pattern-summary.json", {
            "schema": SCHEMA, "kind": "hitl-pattern-summary",
            "patterns": [p["id"] for p in HITL_PATTERNS],
            "invariants_count": len(HITL_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/human-operations/hitl-patterns/",
        }),
        ("06-navigation-system-summary.json", {
            "schema": SCHEMA, "kind": "navigation-system-summary",
            "systems": [n["id"] for n in NAVIGATION_SYSTEMS],
            "invariants_count": len(NAVIGATION_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/human-operations/navigation/",
        }),
        ("07-ergonomics-summary.json", {
            "schema": SCHEMA, "kind": "ergonomics-summary",
            "principles": [e["id"] for e in ERGONOMIC_PRINCIPLES],
            "discipline_rules_count": len(ERGONOMIC_DISCIPLINE),
            "artifact": "wp-content/themes/beslock-custom/User manuals/human-operations/ergonomics/",
        }),
        ("08-human-operations-governance-summary.json", {
            "schema": SCHEMA, "kind": "human-operations-governance-summary",
            "layer_index": 24,
            "subordinate_to_count": len(SUBORDINATE_TO),
            "constitutional_root": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/HUMAN_OPERATIONS_GOVERNANCE/",
            "reports_root": "wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/human-operations/",
            "doctrine_sections": [
                "human-operational-philosophy",
                "supervised-interaction-doctrine",
                "explainability-philosophy",
                "operational-ergonomics-doctrine",
                "human-runtime-collaboration-principles",
                "safe-governance-interaction-philosophy",
            ],
        }),
        ("09-unresolved-human-operational-risks.json", {
            "schema": SCHEMA, "kind": "unresolved-human-operational-risks",
            "items": [
                {"id": "no-executable-consoles",            "severity": "high",   "impact": "all 6 consoles are design-only; no operator surface exists yet"},
                {"id": "no-explainability-renderer",        "severity": "high",   "impact": "explanation patterns declared; no renderer wired into the runtime CLI"},
                {"id": "no-claim-ownership-mediator",       "severity": "high",   "impact": "queue claim semantics declared; no mediator enforces concurrency ceiling"},
                {"id": "no-operator-identity-store",        "severity": "high",   "impact": "operator id is a free string in flows.py; no identity verification"},
                {"id": "no-checkpoint-pause-semantics-runtime","severity": "medium","impact": "executable workflows declare halts; runtime CLI has only auto-decide path"},
                {"id": "no-fatigue-throttle",               "severity": "medium", "impact": "ergonomic principles declare ceilings; no throttle exists yet"},
                {"id": "no-explanation-replayability-test", "severity": "medium", "impact": "explanation determinism is asserted, not yet tested"},
                {"id": "no-cognitive-load-measurement",     "severity": "low",    "impact": "no instrumentation to measure operator decision time / abandonment"},
                {"id": "carry-overs-from-phase-28-29",      "severity": "high",   "impact": "no executable reviewer registry, queue store, event log, binding store; 132 candidates still await elevation"},
            ],
        }),
        ("10-operator-readiness-reassessment.json", {
            "schema": SCHEMA, "kind": "operator-readiness-reassessment",
            "platform_status": "FOUNDATIONALLY COMPLETE (unchanged)",
            "human_operations_status": "MODELED (executable surfaces pending)",
            "primary_bottleneck": "SAFE HUMAN OPERATIONAL INTERACTION (now governed by declared model)",
            "next_bottleneck": "executable enforcement of operator surfaces (consoles, identity store, claim mediator, explanation renderer, checkpoint-pause runtime semantics)",
            "future_commitments": FUTURE_COMMITMENTS,
            "future_invariants": FUTURE_INVARIANTS,
            "generated": now_iso(),
        }),
    ]
    for name, payload in reports:
        (REPORTS_ROOT / name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(f"Human Operations Governance (layer 24) written to:\n  {HOPS_ROOT}\n  {CONST_ROOT}\n  {REPORTS_ROOT}")


if __name__ == "__main__":
    build()
