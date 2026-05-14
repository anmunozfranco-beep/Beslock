"""
Phase 34 — OPERATIONAL PILOTS & FEEDBACK GOVERNANCE.

Constitutional layer 28. Modeling-only. Subordinate to knowledge-core and
to all twenty-seven prior governance layers.

Writes:
  - the six operational-pilots artifact folders under
    `wp-content/themes/beslock-custom/User manuals/operational-pilots/`
  - the doctrine root at
    `wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/OPERATIONAL_PILOT_GOVERNANCE/`
  - the ten final reports under
    `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/operational-pilots/01..10`

Idempotent. Non-destructive. Reads no per-product knowledge-core JSON.
Adds NO macro-governance mega-layer. Defines pilot/feedback/telemetry/friction/
retrieval-analytics/feedback-evolution models that the runtime + reviewer
ecosystem can later instrument against. Touches no runtime code.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
PILOT_ROOT = THEME_ROOT / "operational-pilots"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "OPERATIONAL_PILOT_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "operational-pilots"

SCHEMA = "operational-pilot-governance/1.0"


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
    "HUMAN_OPERATIONS", "ENVIRONMENT_AND_INTEGRATION", "REFERENCE_STACK",
    "ECOSYSTEM_NORMALIZATION",
]


# =============================================================================
# TASK 1 — OPERATIONAL PILOT MODEL
# =============================================================================

PILOT_DEFINITIONS = [
    {
        "id": "onboarding-pilot",
        "scope": "supervised onboarding flows for one product at a time",
        "supervision": "one accountable operator per session; receipts captured per layer-24 contract",
        "operator_constraints": ["no autonomous progression", "no skipped acknowledgements", "no replay-bypass"],
        "safety_boundaries": ["sandbox env (layer 25)", "candidate-only corpus surface", "no production telemetry sinks"],
        "trust_thresholds": {"minimum_confidence": 0.6, "escalate_below": 0.5, "block_below": 0.3},
    },
    {
        "id": "troubleshooting-pilot",
        "scope": "guided troubleshooting with replay-assisted reasoning",
        "supervision": "operator + reviewer-on-call; both receipts captured",
        "operator_constraints": ["must declare hypothesis before action", "must record observed outcome", "must invoke replay on uncertainty"],
        "safety_boundaries": ["read-only against installed-base data", "no remote actuation", "session-scoped continuity only"],
        "trust_thresholds": {"minimum_confidence": 0.65, "escalate_below": 0.55, "block_below": 0.35},
    },
    {
        "id": "reviewer-workflow-pilot",
        "scope": "reviewer elevation of pending candidates (132 outstanding)",
        "supervision": "scoped reviewer role per layer-23; revocation first-class",
        "operator_constraints": ["one candidate at a time", "decision rationale captured", "no batch promotion"],
        "safety_boundaries": ["dual-review env (layer 25) for trust-boundary changes", "audit trail mandatory"],
        "trust_thresholds": {"single_reviewer_max_tier": "internal", "dual_review_required_for": ["external", "production-shadow"]},
    },
    {
        "id": "oem-ingestion-pilot",
        "scope": "controlled OEM manual ingestion through the dual-review binding (layers 23 + 25)",
        "supervision": "ingestion operator + content reviewer (cannot be same person)",
        "operator_constraints": ["provenance complete or reject", "no merge into trusted corpus until promoted"],
        "safety_boundaries": ["ingestion env only", "candidate-tier on entry", "no runtime exposure pre-promotion"],
        "trust_thresholds": {"entry_tier": "candidate", "promotion_requires": "dual-review + reviewer-of-scope"},
    },
    {
        "id": "escalation-handling-pilot",
        "scope": "controlled escalation path exercise across runtime → operator → reviewer",
        "supervision": "escalation receiver named per channel; SLA observed not enforced",
        "operator_constraints": ["acknowledge within observation window", "record disposition"],
        "safety_boundaries": ["no auto-escalation loops", "termination after one operator hop"],
        "trust_thresholds": {"escalate_on_confidence_below": 0.5, "escalate_on_continuity_break": True},
    },
    {
        "id": "replay-assisted-review-pilot",
        "scope": "reviewers exercise replay (layer 22) to validate prior runtime decisions",
        "supervision": "reviewer-of-scope; replay receipts captured",
        "operator_constraints": ["replay must complete before decision", "discrepancies recorded as findings"],
        "safety_boundaries": ["replay reads supplemental corpus only", "skips synthetic empty packages", "no live corpus mutation"],
        "trust_thresholds": {"replay_divergence_alert_threshold": 0.1},
    },
]

PILOT_MODEL_RULES = [
    "every pilot is supervised; no autonomous pilot may run",
    "every pilot is sandboxed (layer-25 env tier appropriate to its scope)",
    "every pilot is candidate-corpus-only unless reviewer-promoted (layer 23)",
    "every pilot must produce supervision receipts (layer 24) before closing",
    "no pilot may bypass replay (layer 22) when confidence falls below its declared escalate threshold",
    "no pilot may auto-promote candidates; promotion is a separate reviewer act",
]


# =============================================================================
# TASK 2 — FEEDBACK INSTRUMENTATION
# =============================================================================

FEEDBACK_SIGNALS = [
    {"id": "retrieval-failure",          "captured_when": "retrieval returns 0 results or all results below escalate threshold", "fields": ["query", "product", "domain", "top_score", "result_count", "session_id"]},
    {"id": "escalation-frequency",       "captured_when": "session escalates to operator or reviewer", "fields": ["session_id", "trigger", "from_role", "to_role", "confidence_at_escalation"]},
    {"id": "continuity-breakdown",       "captured_when": "session checkpoint cannot be resumed or context is lost", "fields": ["session_id", "checkpoint_id", "break_reason"]},
    {"id": "operator-confusion",         "captured_when": "operator requests clarification, retracts an action, or loops on the same step", "fields": ["session_id", "step", "loop_count", "retraction"]},
    {"id": "reviewer-friction",          "captured_when": "reviewer defers, requests more provenance, or cannot decide", "fields": ["candidate_id", "reviewer_id", "deferral_reason", "missing_provenance_fields"]},
    {"id": "governance-bottleneck",      "captured_when": "candidates queue beyond a declared age threshold or one reviewer holds disproportionate load", "fields": ["queue_depth", "oldest_age_days", "reviewer_load_distribution"]},
    {"id": "ambiguity-hotspot",          "captured_when": "same query/topic produces divergent retrievals across nearby sessions", "fields": ["topic", "divergence_score", "sessions_observed"]},
]

FEEDBACK_INSTRUMENTATION_RULES = [
    "all signals are observation-only; instrumentation MUST NOT alter runtime behavior",
    "all signals carry provenance (session_id, operator role, timestamp, trust-zone)",
    "no signal stores PII or operator-identifying free text beyond declared fields",
    "signal storage is sandbox-tier in pilot phase (layer 25)",
    "signal aggregation is reviewer-visible; raw signals are not auto-actioned",
]


# =============================================================================
# TASK 3 — OPERATIONAL TELEMETRY
# =============================================================================

TELEMETRY_STREAMS = [
    {"id": "retrieval-confidence",       "metric": "distribution of top_score per (product, domain) per window", "purpose": "detect corpus weakness"},
    {"id": "runtime-uncertainty",        "metric": "fraction of decisions in escalate-band per session", "purpose": "detect ambiguity zones"},
    {"id": "escalation-propagation",     "metric": "depth and time-to-acknowledge of escalation chains", "purpose": "detect overloaded receivers"},
    {"id": "replay-frequency",           "metric": "replay invocations per session, per reviewer", "purpose": "detect over- or under-use of replay"},
    {"id": "reviewer-workload",          "metric": "candidates/day and time-to-decision per reviewer", "purpose": "detect reviewer fatigue"},
    {"id": "corpus-weakness-hotspots",   "metric": "joint (low retrieval-confidence × high escalation) per topic", "purpose": "prioritize corpus enrichment"},
    {"id": "operational-dead-ends",      "metric": "sessions terminated without resolution + topic clustering", "purpose": "detect missing flows"},
]

TELEMETRY_RULES = [
    "telemetry is aggregate; per-operator identification requires reviewer-of-scope authorization",
    "telemetry feeds are subordinate to layer-25 trust zones and layer-24 operator privacy",
    "no telemetry stream may auto-trigger runtime mutation",
    "telemetry retention is bounded; retention windows are governance-declared",
    "telemetry exposure outside the pilot env requires promotion + provenance",
]


# =============================================================================
# TASK 4 — REVIEWER & OPERATOR FRICTION ANALYTICS
# =============================================================================

FRICTION_PATTERNS = [
    {"id": "reviewer-fatigue",                "indicator": "time-to-decision rising over rolling window for a reviewer", "mitigation": "rotate reviewer-of-scope; reduce queue assignment"},
    {"id": "workflow-friction",               "indicator": "operator retraction rate or step-loop rate above baseline", "mitigation": "doctrine clarification (layer 24 ergonomics); console refinement"},
    {"id": "escalation-overload",             "indicator": "escalation receiver acknowledgement time exceeds declared envelope", "mitigation": "expand receiver pool; tighten escalation criteria"},
    {"id": "ambiguity-density",               "indicator": "topic cluster with high divergence-score across sessions", "mitigation": "corpus enrichment for that topic via layer-23 candidate flow"},
    {"id": "navigation-pain",                 "indicator": "operator requests clarification on the same step across operators", "mitigation": "layer-24 explainability artifact + console copy refinement"},
    {"id": "continuity-restoration-failures", "indicator": "checkpoint resume fails or operator restarts session", "mitigation": "review checkpoint contract; widen continuity scope (layer 14) without mutating runtime invariants"},
]

FRICTION_ANALYTICS_RULES = [
    "friction analytics inform reviewer + governance; never auto-mutate doctrine",
    "individual operator friction surfaces are scoped to that operator + their reviewer-of-scope",
    "friction findings flow into the candidate pipeline (layer 23); no shortcut into trusted corpus",
]


# =============================================================================
# TASK 5 — RETRIEVAL FAILURE ANALYTICS
# =============================================================================

RETRIEVAL_ANALYTIC_TRACKS = [
    {"id": "no-result-retrievals",        "tracked": "queries returning zero candidates", "review_action": "topic queued for corpus enrichment"},
    {"id": "thin-corpus-escalations",     "tracked": "queries where only candidate-tier results are present", "review_action": "candidate-elevation review prioritized"},
    {"id": "low-confidence-guidance",     "tracked": "guidance shown to operator while confidence is in escalate-band", "review_action": "either improve corpus or tighten threshold"},
    {"id": "causal-graph-gaps",           "tracked": "reasoning (layer 12) cannot construct chain for a topic", "review_action": "causal authoring task queued"},
    {"id": "warning-coverage-failures",   "tracked": "safety-relevant query without warning surfaced", "review_action": "warning corpus gap — high priority"},
    {"id": "troubleshooting-insufficiency","tracked": "troubleshooting flow exhausts options without resolution", "review_action": "flow extension via candidate authoring"},
]

RETRIEVAL_ANALYTICS_RULES = [
    "retrieval analytics drive corpus enrichment requests, not direct corpus writes",
    "warning-coverage failures are HIGH priority and surface to reviewer-of-scope immediately",
    "no analytic may alter retrieval ranking; ranking remains governed by CONFIDENCE_WEIGHTS source-of-truth",
]


# =============================================================================
# TASK 6 — FEEDBACK-DRIVEN CORPUS EVOLUTION
# =============================================================================

FEEDBACK_EVOLUTION_FLOW = [
    {"step": 1, "stage": "runtime observation",   "actor": "runtime",                "produces": "instrumented signal (TASK 2)"},
    {"step": 2, "stage": "aggregation",           "actor": "telemetry pipeline",     "produces": "hotspot / friction / retrieval finding (TASKs 3-5)"},
    {"step": 3, "stage": "reviewer triage",       "actor": "reviewer-of-scope",      "produces": "enrichment request OR closure with rationale"},
    {"step": 4, "stage": "candidate authoring",   "actor": "knowledge operator",     "produces": "candidate knowledge node (layer 23)"},
    {"step": 5, "stage": "trust evaluation",      "actor": "reviewer ecosystem",     "produces": "promotion decision (single or dual review per scope)"},
    {"step": 6, "stage": "promotion",             "actor": "promotion workflow",     "produces": "trusted corpus update"},
    {"step": 7, "stage": "runtime improvement",   "actor": "runtime",                "produces": "next-cycle observations (loop closes)"},
]

FEEDBACK_EVOLUTION_RULES = [
    "no step in this flow may be skipped",
    "no automation may compress steps 3 + 4 + 5 (the human-judgment band)",
    "every promotion carries provenance back to the originating signal cluster",
    "loop is observation-only on the first iteration of every new pilot product",
    "signal → corpus changes are governed; never inferred and applied silently",
]


# =============================================================================
# TASK 7 — PILOT GOVERNANCE (doctrine root contents)
# =============================================================================

CHARTER_PRINCIPLES = [
    "the ecosystem is architecturally complete; further maturation comes from real operational learning",
    "operational pilots are supervised observation, not autonomous execution",
    "feedback flows through governance, never around it",
    "telemetry is a measurement instrument, never a control surface",
    "operator and reviewer well-being is itself a first-class signal",
    "no pilot finding bypasses the candidate → review → promotion path",
    "operational maturity is earned through observed usage, not declared",
]

SUB_DOCTRINES = [
    ("pilot-philosophy",
     "Pilot Philosophy",
     "Pilots exist to expose the ecosystem to real operational pressure under supervision, not to validate the architecture. Failure observed in a pilot is information, not regression.",
     ["pilots are tests of the ecosystem-against-reality, not reality-against-the-ecosystem",
      "every pilot has a declared scope, exit criterion, and reviewer-of-scope",
      "pilots end; they are not a permanent operational state"]),
    ("operational-learning-doctrine",
     "Operational Learning Doctrine",
     "Operational learning is the disciplined conversion of observed runtime behavior into governed corpus evolution. It is bounded by provenance, supervision, and trust.",
     ["learning enters through signals (TASK 2)",
      "learning is interpreted by reviewers, not by automation",
      "learning produces candidates; promotions remain a separate, reviewed act"]),
    ("feedback-governed-evolution",
     "Feedback-Governed Evolution",
     "All ecosystem evolution induced by operational feedback is subordinate to layers 1-27. Feedback may not introduce new schemas, doctrines, or runtime invariants.",
     ["feedback can request enrichment; it cannot author doctrine",
      "feedback can prioritize candidates; it cannot promote them",
      "feedback can surface friction; it cannot redesign workflows"]),
    ("supervised-pilot-principles",
     "Supervised Pilot Principles",
     "Every pilot has a named accountable operator, a named reviewer-of-scope, and a sandboxed environment tier. Supervision is non-delegable.",
     ["one accountable operator per pilot session",
      "one reviewer-of-scope per pilot scope",
      "supervision receipts (layer 24) close every session"]),
    ("runtime-observation-philosophy",
     "Runtime Observation Philosophy",
     "Observation is non-mutating. The runtime under observation behaves identically whether telemetry is or is not collected (modulo sink I/O).",
     ["telemetry MUST NOT change runtime decisions",
      "instrumentation MUST be removable without runtime regression",
      "observation surface is bounded; new observation requires governance entry"]),
    ("operational-hardening-methodology",
     "Operational Hardening Methodology",
     "Hardening is the process of allowing observed pressure to inform candidate corpus, reviewer workload allocation, and console refinement — without any structural change to layers 1-28.",
     ["hardening targets corpus, ergonomics, and reviewer allocation",
      "hardening does not target runtime invariants",
      "hardening does not introduce new mega-layers"]),
]


# =============================================================================
# TASK 8 — LONG-TERM OPERATIONAL LEARNING
# =============================================================================

FUTURE_LEARNING_COMMITMENTS = [
    "long-term telemetry retention will be governance-declared with explicit retention windows",
    "reviewer ecosystem learning will be observable via aggregate workload + decision-quality metrics",
    "runtime hardening will proceed via candidate authoring + reviewer promotion only",
    "operational maturity will be reassessed at declared cadence, not continuously",
    "deployment-readiness observation will require explicit promotion of telemetry from pilot env to staging env (layer 25)",
    "supervised production pilots remain bounded to the dual-review binding (layers 23 + 25) and to receipts (layer 24)",
]

FUTURE_LEARNING_INVARIANTS = [
    "no telemetry stream becomes a control loop without governance entry",
    "no operational learning bypasses the candidate → review → promotion sequence",
    "no pilot promotes itself to production without explicit reviewer-of-scope authorization",
    "no observed friction silently rewrites doctrine",
    "no reviewer pain-point shortcut compresses the human-judgment band",
]


# =============================================================================
# REPORTS — open risks + maturity reassessment
# =============================================================================

UNRESOLVED_LEARNING_RISKS = [
    {"id": "no-pilot-yet-executed",                "severity": "high",   "note": "All declared pilots are modeled, not run; no real operational signal exists yet."},
    {"id": "no-instrumentation-emitter",           "severity": "high",   "note": "Signals (TASK 2) are declared; runtime emits none of them today."},
    {"id": "no-telemetry-sink",                    "severity": "high",   "note": "No sandbox-tier telemetry sink is provisioned (layer 25 incident-trace channel still pending)."},
    {"id": "no-reviewer-workload-meter",           "severity": "medium", "note": "Reviewer fatigue indicator cannot be computed without a workload meter."},
    {"id": "no-hotspot-aggregator",                "severity": "medium", "note": "Hotspot detection requires aggregation infrastructure not yet built."},
    {"id": "no-causal-gap-detector",               "severity": "medium", "note": "Causal-graph gap detection requires reasoning-trace export (layer 12)."},
    {"id": "candidate-elevation-throughput",       "severity": "high",   "note": "132 candidates pending elevation; pilot signal will increase, not decrease, this queue without reviewer capacity."},
    {"id": "console-absence",                      "severity": "high",   "note": "Operator + reviewer consoles remain design-only (layer 24); pilots cannot run without minimum surfaces."},
    {"id": "no-pilot-exit-criteria-test",          "severity": "low",    "note": "Pilot exit criteria are declared; no automated check verifies a pilot has met them before closure."},
    {"id": "supervision-receipt-runtime-emission", "severity": "high",   "note": "Carry-over from layer 24: supervision receipts not yet emitted by runtime."},
]

OPERATIONAL_MATURITY_REASSESSMENT = {
    "platform_status": "FOUNDATIONALLY COMPLETE (unchanged across phases 28-34)",
    "operational_maturity": "PRE-PILOT — instrumented in doctrine, not yet exercised in reality",
    "primary_bottleneck": "absence of executable surfaces (consoles, sinks, emitters) blocks every declared pilot",
    "secondary_bottleneck": "reviewer capacity vs. expected pilot signal volume (132 pending + new pilot inflow)",
    "next_natural_track": "executable enforcement of priors (consoles, emitters, sinks, registry) so pilots can RUN",
    "layer_count": 28,
    "subordinate_chain_length": 29,
    "test_suite_status": "19/19 passing (runtime untouched)",
    "no_new_mega_layers": True,
}


# =============================================================================
# BUILD
# =============================================================================

def build():
    PILOT_ROOT.mkdir(parents=True, exist_ok=True)
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    ts = now_iso()
    common = {"schema": SCHEMA, "generated_at": ts, "subordinate_to": SUBORDINATE_TO}

    # ---- TASK 1 — pilot-model
    write_pair(
        PILOT_ROOT / "pilot-model", "pilot-model",
        "Operational Pilot Model",
        "Six supervised pilots covering onboarding, troubleshooting, reviewer workflows, OEM ingestion, escalation handling, and replay-assisted review.",
        [
            ("Pilot definitions", md_list([
                f"`{p['id']}` — {p['scope']}; supervision: {p['supervision']}; thresholds: {p['trust_thresholds']}"
                for p in PILOT_DEFINITIONS])),
            ("Operator constraints", md_list([f"`{p['id']}`: " + "; ".join(p["operator_constraints"]) for p in PILOT_DEFINITIONS])),
            ("Safety boundaries", md_list([f"`{p['id']}`: " + "; ".join(p["safety_boundaries"]) for p in PILOT_DEFINITIONS])),
            ("Pilot model rules", md_list(PILOT_MODEL_RULES)),
        ],
        {**common, "pilots": PILOT_DEFINITIONS, "rules": PILOT_MODEL_RULES},
    )

    # ---- TASK 2 — feedback-instrumentation
    write_pair(
        PILOT_ROOT / "feedback-instrumentation", "feedback-instrumentation",
        "Feedback Instrumentation",
        "Seven observation-only signals capture retrieval failures, escalations, continuity breakdowns, operator confusion, reviewer friction, governance bottlenecks, and ambiguity hotspots.",
        [
            ("Signals", md_list([f"`{s['id']}` — when: {s['captured_when']}; fields: {', '.join(s['fields'])}" for s in FEEDBACK_SIGNALS])),
            ("Instrumentation rules", md_list(FEEDBACK_INSTRUMENTATION_RULES)),
        ],
        {**common, "signals": FEEDBACK_SIGNALS, "rules": FEEDBACK_INSTRUMENTATION_RULES},
    )

    # ---- TASK 3 — telemetry
    write_pair(
        PILOT_ROOT / "telemetry", "telemetry",
        "Operational Telemetry",
        "Seven aggregate telemetry streams over retrieval confidence, runtime uncertainty, escalation propagation, replay frequency, reviewer workload, corpus weakness hotspots, and operational dead-ends.",
        [
            ("Streams", md_list([f"`{t['id']}` — metric: {t['metric']}; purpose: {t['purpose']}" for t in TELEMETRY_STREAMS])),
            ("Telemetry rules", md_list(TELEMETRY_RULES)),
        ],
        {**common, "streams": TELEMETRY_STREAMS, "rules": TELEMETRY_RULES},
    )

    # ---- TASK 4 — friction-analytics
    write_pair(
        PILOT_ROOT / "friction-analytics", "friction-analytics",
        "Reviewer & Operator Friction Analytics",
        "Six friction patterns covering reviewer fatigue, workflow friction, escalation overload, ambiguity density, navigation pain, and continuity restoration failures.",
        [
            ("Patterns", md_list([f"`{f['id']}` — indicator: {f['indicator']}; mitigation: {f['mitigation']}" for f in FRICTION_PATTERNS])),
            ("Rules", md_list(FRICTION_ANALYTICS_RULES)),
        ],
        {**common, "patterns": FRICTION_PATTERNS, "rules": FRICTION_ANALYTICS_RULES},
    )

    # ---- TASK 5 — retrieval-analytics
    write_pair(
        PILOT_ROOT / "retrieval-analytics", "retrieval-analytics",
        "Retrieval Failure Analytics",
        "Six tracked failure modes from no-result retrievals to troubleshooting insufficiency, each routed to a reviewer action — never to direct corpus writes.",
        [
            ("Tracks", md_list([f"`{r['id']}` — tracked: {r['tracked']}; review action: {r['review_action']}" for r in RETRIEVAL_ANALYTIC_TRACKS])),
            ("Rules", md_list(RETRIEVAL_ANALYTICS_RULES)),
        ],
        {**common, "tracks": RETRIEVAL_ANALYTIC_TRACKS, "rules": RETRIEVAL_ANALYTICS_RULES},
    )

    # ---- TASK 6 — feedback-evolution
    write_pair(
        PILOT_ROOT / "feedback-evolution", "feedback-evolution",
        "Feedback-Driven Corpus Evolution",
        "Seven-step governed loop: runtime observation → aggregation → reviewer triage → candidate authoring → trust evaluation → promotion → runtime improvement.",
        [
            ("Loop", md_list([f"step {s['step']} — `{s['stage']}` (actor: {s['actor']}; produces: {s['produces']})" for s in FEEDBACK_EVOLUTION_FLOW])),
            ("Rules", md_list(FEEDBACK_EVOLUTION_RULES)),
        ],
        {**common, "loop": FEEDBACK_EVOLUTION_FLOW, "rules": FEEDBACK_EVOLUTION_RULES},
    )

    # ---- TASK 7 — doctrine root
    (CONST_ROOT / "README.md").write_text(
        "# Operational Pilot Governance\n\n"
        "Constitutional layer 28. Subordinate to knowledge-core and to all twenty-seven prior governance layers. "
        "Modeling-only. Adds no macro-governance mega-layer. Defines pilots, feedback instrumentation, telemetry, "
        "friction + retrieval analytics, and the governed feedback-evolution loop.\n",
        encoding="utf-8",
    )
    write_pair(
        CONST_ROOT, "00-charter",
        "Operational Pilot Governance Charter",
        "The ecosystem is architecturally complete; further maturation comes from real operational learning under supervision and governance.",
        [("Principles", md_list(CHARTER_PRINCIPLES)),
         ("Subordinate to", md_list(SUBORDINATE_TO))],
        {**common, "principles": CHARTER_PRINCIPLES},
    )
    for slug, title, intro, points in SUB_DOCTRINES:
        write_pair(
            CONST_ROOT, slug, title, intro,
            [("Tenets", md_list(points))],
            {**common, "tenets": points},
        )

    # ---- REPORTS 01..10
    reports = [
        ("01-pilot-model-summary", "Pilot Model Summary",
         {**common, "pilot_count": len(PILOT_DEFINITIONS), "pilots": [p["id"] for p in PILOT_DEFINITIONS], "rule_count": len(PILOT_MODEL_RULES)}),
        ("02-feedback-instrumentation-summary", "Feedback Instrumentation Summary",
         {**common, "signal_count": len(FEEDBACK_SIGNALS), "signals": [s["id"] for s in FEEDBACK_SIGNALS], "instrumentation_is_observation_only": True}),
        ("03-telemetry-summary", "Telemetry Summary",
         {**common, "stream_count": len(TELEMETRY_STREAMS), "streams": [t["id"] for t in TELEMETRY_STREAMS], "control_loops_introduced": 0}),
        ("04-friction-analytics-summary", "Friction Analytics Summary",
         {**common, "pattern_count": len(FRICTION_PATTERNS), "patterns": [f["id"] for f in FRICTION_PATTERNS]}),
        ("05-retrieval-analytics-summary", "Retrieval Analytics Summary",
         {**common, "track_count": len(RETRIEVAL_ANALYTIC_TRACKS), "tracks": [r["id"] for r in RETRIEVAL_ANALYTIC_TRACKS], "auto_corpus_writes": 0}),
        ("06-feedback-evolution-summary", "Feedback Evolution Summary",
         {**common, "step_count": len(FEEDBACK_EVOLUTION_FLOW), "human_judgment_band_steps": [3, 4, 5], "compressed": False}),
        ("07-pilot-governance-summary", "Pilot Governance Summary",
         {**common, "doctrine_root": str(CONST_ROOT.relative_to(REPO_ROOT)), "principle_count": len(CHARTER_PRINCIPLES), "sub_doctrine_count": len(SUB_DOCTRINES)}),
        ("08-long-term-learning-summary", "Long-Term Operational Learning Summary",
         {**common, "commitments": FUTURE_LEARNING_COMMITMENTS, "invariants": FUTURE_LEARNING_INVARIANTS}),
        ("09-unresolved-operational-learning-risks", "Unresolved Operational Learning Risks",
         {**common, "risks": UNRESOLVED_LEARNING_RISKS, "risk_count": len(UNRESOLVED_LEARNING_RISKS)}),
        ("10-ecosystem-operational-maturity-reassessment", "Ecosystem Operational Maturity Reassessment",
         {**common, **OPERATIONAL_MATURITY_REASSESSMENT}),
    ]
    for slug, title, payload in reports:
        write_pair(
            REPORTS_ROOT, slug, title,
            "Phase 34 final report — modeling-only; runtime untouched.",
            [("Payload", "See accompanying JSON.")],
            payload,
        )

    print("Operational Pilot Governance (layer 28) written to:")
    print(f"  {PILOT_ROOT}")
    print(f"  {CONST_ROOT}")
    print(f"  {REPORTS_ROOT}")
    print(f"  pilots: {len(PILOT_DEFINITIONS)}; signals: {len(FEEDBACK_SIGNALS)}; "
          f"telemetry streams: {len(TELEMETRY_STREAMS)}; friction patterns: {len(FRICTION_PATTERNS)}; "
          f"retrieval tracks: {len(RETRIEVAL_ANALYTIC_TRACKS)}; loop steps: {len(FEEDBACK_EVOLUTION_FLOW)}; "
          f"sub-doctrines: {len(SUB_DOCTRINES)}; risks: {len(UNRESOLVED_LEARNING_RISKS)}")


if __name__ == "__main__":
    build()
