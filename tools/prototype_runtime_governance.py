"""
Phase 25 — FIRST REAL OPERATIONAL RUNTIME PROTOTYPING (modeling-only).

Nineteenth constitutional layer. Subordinate to knowledge-core and to all
eighteen prior governance layers. Models — does not implement — the first
supervised operational runtime prototype around the contextual-onboarding +
troubleshooting-retrieval slice.

Hard exclusions (verbatim):
- DO NOT build autonomous agents
- DO NOT deploy production systems
- DO NOT generate images
- DO NOT create PDFs
- DO NOT build large frontend ecosystems
- DO NOT optimize scale/performance

Idempotent. Non-destructive. Reads no per-product knowledge-core files.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "PROTOTYPE_RUNTIME_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "prototype-runtime"

SCHEMA = "prototype-runtime-governance/1.0"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def md_list(items):
    return "\n".join(f"- {x}" for x in items)


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


# ---------------------------------------------------------------------------
# Charter
# ---------------------------------------------------------------------------

CHARTER_PRINCIPLES = [
    "This prototype layer is itself modeling-only; it executes nothing.",
    "The prototype is a supervised proof-of-value runtime, not a production system.",
    "The prototype's first slice is contextual onboarding + troubleshooting retrieval.",
    "Every prototype layer is read-only by default; destructive surfaces are out of scope.",
    "Every prototype emission carries provenance, supervision receipt, and trace bindings.",
    "Every prototype run is demotable; demotion is the safe response to anomalies.",
    "Hard exclusions (no autonomous agents, no production deployment, no images, no PDFs, no large frontend, no perf optimization) bind every prototype layer.",
    "The prototype cannot promote P-tier, elevate confidence, or alter prior governance layers.",
    "Operator supervision is mandatory at every cognition boundary inside the prototype.",
    "All prototype work remains subordinate to the governed knowledge-core forever.",
]

CHARTER_AUTHORITY = [
    "Declares the first executable runtime architecture (six layers).",
    "Declares the first executable user flows for the onboarding + troubleshooting slice.",
    "Declares the executable retrieval pipeline and its validation predicates.",
    "Declares the executable contextual assembly flows.",
    "Declares the supervised operational guidance posture for the prototype.",
    "Declares operational safety validation predicates for the prototype.",
    "Declares the prototype observability requirements.",
    "Declares the prototype governance philosophy.",
    "Declares the controlled transition path to future production cognition runtimes.",
    "Declares the prototype readiness assessment criteria and outcome.",
]


# ---------------------------------------------------------------------------
# TASK 1 — Runtime architecture
# ---------------------------------------------------------------------------

ARCH_LAYERS = [
    {"id": "retrieval-layer",          "responsibility": "resolve query intent into a read-only retrieval-package over knowledge-core",
     "consumes": ["intent-record", "access-pattern"], "emits": ["retrieval-package", "provenance-manifest"], "supervision": "operator-observed"},
    {"id": "context-assembly-layer",   "responsibility": "merge retrieval-package + warnings + prerequisites + continuity-state into an assembly-package",
     "consumes": ["retrieval-package", "continuity-state"], "emits": ["assembly-package", "warning-record"], "supervision": "operator-observed"},
    {"id": "operational-guidance-layer","responsibility": "shape assembly-package into a supervised guidance-package per ADAPTIVE precedence",
     "consumes": ["assembly-package", "adaptation-record"], "emits": ["guidance-package", "chain-record"], "supervision": "supervised"},
    {"id": "escalation-layer",         "responsibility": "evaluate escalation predicates and produce 12-field escalation packages",
     "consumes": ["assembly-package", "guidance-package"], "emits": ["escalation-package", "handoff-record"], "supervision": "supervised"},
    {"id": "continuity-layer",         "responsibility": "load timeline + context vector and persist append-only checkpoint records",
     "consumes": ["timeline-id", "context-vector"], "emits": ["restoration-record", "checkpoint-record"], "supervision": "supervised"},
    {"id": "supervision-layer",        "responsibility": "host operator review checkpoints, override channel, and supervision receipts",
     "consumes": ["any-package"], "emits": ["supervision-receipt", "override-record"], "supervision": "operator-driven"},
]

ARCH_RULES = [
    "Layers are unidirectional: retrieval → assembly → guidance, with supervision/continuity/escalation as orthogonal observers.",
    "Every layer emits provenance; an unobserved emission invalidates the prototype run.",
    "No layer performs destructive operations during the prototype.",
    "No layer may bypass lifecycle P-tier gates or schema-pin enforcement.",
    "No layer may elevate confidence to compensate for missing inputs.",
]


# ---------------------------------------------------------------------------
# TASK 2 — User flows
# ---------------------------------------------------------------------------

USER_FLOWS = [
    {"id": "onboarding-flow",        "kind": "onboarding",     "in_scope": True,  "supervision": "supervised end-to-end",
     "steps": ["intent declared", "retrieval-package built", "assembly-package built", "supervised guidance emitted", "operator confirms completion"],
     "evidence": ["intent-id", "retrieval-package-id", "assembly-package-id", "guidance-package-id", "supervision-receipt-id"]},
    {"id": "first-pairing-flow",     "kind": "onboarding",     "in_scope": True,  "supervision": "supervised end-to-end",
     "steps": ["pairing prerequisites surfaced", "warnings stamped", "guidance emitted", "operator confirms outcome"],
     "evidence": ["prereq-record", "warning-record", "guidance-package-id", "supervision-receipt-id"]},
    {"id": "fingerprint-enrollment-flow", "kind": "onboarding","in_scope": True,  "supervision": "supervised end-to-end",
     "steps": ["enrollment prerequisites surfaced", "warnings stamped", "guidance emitted", "operator confirms outcome"],
     "evidence": ["prereq-record", "warning-record", "guidance-package-id", "supervision-receipt-id"]},
    {"id": "troubleshooting-lookup-flow", "kind": "troubleshooting","in_scope": True, "supervision": "supervised end-to-end",
     "steps": ["symptom declared", "diagnostic nodes retrieved", "causal edges traversed (when present)", "supervised guidance emitted"],
     "evidence": ["symptom-id", "retrieval-package-id", "chain-record-id", "guidance-package-id"]},
    {"id": "battery-recovery-flow",  "kind": "recovery",       "in_scope": True,  "supervision": "supervised end-to-end",
     "steps": ["recovery prerequisites surfaced", "warnings stamped", "checkpoint snapshot taken (when registry present)", "supervised guidance emitted"],
     "evidence": ["prereq-record", "warning-record", "checkpoint-record", "guidance-package-id"]},
    {"id": "escalation-handling-flow", "kind": "escalation",   "in_scope": True,  "supervision": "supervised end-to-end",
     "steps": ["escalation predicate evaluated", "continuity snapshot taken", "12-field escalation package built", "handoff record emitted"],
     "evidence": ["predicate-id", "continuity-snapshot-id", "escalation-package-id", "handoff-record-id"]},
]

FLOW_RULES = [
    "All prototype flows are read-only; destructive operations are out of scope.",
    "Flows declare steps and evidence keys; unobserved evidence invalidates the run.",
    "Flows emit guidance only after the operator has reviewed the assembly-package.",
    "Flows that cannot satisfy mandatory warnings cannot emit guidance.",
    "Flows respect confidence tiers; uncertain outputs are gated and labeled.",
]


# ---------------------------------------------------------------------------
# TASK 3 — Retrieval pipeline
# ---------------------------------------------------------------------------

RETRIEVAL_KINDS = [
    {"id": "operational-procedures", "validation": ["completeness-required-steps", "provenance-attachment"]},
    {"id": "troubleshooting",        "validation": ["coverage-symptom", "coverage-causal", "provenance-attachment"]},
    {"id": "warnings",               "validation": ["mandatory-warnings-attached", "severity-stamped", "provenance-attachment"]},
    {"id": "onboarding",             "validation": ["coverage", "provenance-attachment"]},
    {"id": "escalation",             "validation": ["retrievability", "12-field-shape", "provenance-attachment"]},
    {"id": "adaptive-guidance",      "validation": ["precedence-respected", "no-confidence-elevation", "provenance-attachment"]},
]

PIPELINE_STAGES = [
    "intent-bind",
    "access-pattern-resolve",
    "fetch-read-only",
    "validate-predicates",
    "attach-provenance-manifest",
    "emit-retrieval-package",
]

PIPELINE_RULES = [
    "Pipeline is read-only; mutations are out of scope for the prototype.",
    "Predicate failures gate emission; ambiguity is surfaced, not silently resolved.",
    "Pipeline outputs bind to a run-id + slice-id and are append-only.",
    "Pipeline cannot retroactively alter prior emissions.",
]


# ---------------------------------------------------------------------------
# TASK 4 — Context assembly
# ---------------------------------------------------------------------------

ASSEMBLY_FLOWS = [
    {"id": "procedures+warnings+prerequisites", "merges": ["procedure-nodes", "mandatory-warnings", "prerequisite-records"]},
    {"id": "troubleshooting+causal+continuity", "merges": ["diagnostic-nodes", "causal-edges", "continuity-state"]},
    {"id": "escalation+continuity+adaptive",     "merges": ["escalation-predicate-result", "continuity-snapshot", "adaptation-record"]},
    {"id": "onboarding+adaptive+supervision",    "merges": ["onboarding-nodes", "adaptation-record", "supervision-receipt"]},
]

ASSEMBLY_RULES = [
    "Mandatory warnings cannot be suppressed in any assembly.",
    "Prerequisite gaps block assembly emission; they do not silently degrade guidance.",
    "Continuity state is read-only at assembly time; mutations require declared continuity flow.",
    "Adaptive precedence (knowledge-core > adaptive) is invariant.",
    "Assembly emits a single bound assembly-package per run-step.",
]


# ---------------------------------------------------------------------------
# TASK 5 — Supervision
# ---------------------------------------------------------------------------

SUPERVISED_BEHAVIOR = [
    "every cognition boundary is supervised",
    "supervision posture is declared, not inferred",
    "supervision receipts are append-only and provenance-signed",
    "the prototype halts on missing supervision receipts",
]

UNCERTAINTY_SURFACING = [
    "confidence tier disclosed at the operator boundary",
    "ambiguity surfaced with all candidate options + sources",
    "contradictions surfaced verbatim with both source nodes",
    "uncertain-confidence outputs labeled and gated",
]

ESCALATION_TRIGGERS = [
    "validation predicate failure",
    "contract violation",
    "ambiguity unresolved within declared budget",
    "missing supervision receipt",
    "operator-raised tier",
]

UNSAFE_GUIDANCE_INTERRUPTION = [
    "unsafe-flow detected → halt slice + force escalating",
    "hallucination detected (node not in knowledge-core) → halt slice + demote",
    "irreversibility warning downgrade attempted → halt slice + demote",
    "governance bypass attempted → halt slice + demote",
]

REVIEW_CHECKPOINTS = [
    "pre-emission",
    "post-emission",
    "pre-handoff",
    "pre-completion",
    "post-anomaly",
]

OPERATOR_OVERRIDE = [
    "approve / reject / request-more-info / escalate / demote",
    "cannot relax safety-preserving adaptations",
    "cannot downgrade irreversibility warnings",
    "recorded with identity (when declared) + provenance + timestamp",
]


# ---------------------------------------------------------------------------
# TASK 6 — Safety validation
# ---------------------------------------------------------------------------

SAFETY_PREDICATES = [
    {"id": "hallucination-resistance",   "metric": "every emitted node is present in knowledge-core; no invented nodes/steps/edges"},
    {"id": "no-unsafe-retrieval",        "metric": "no retrieval crosses safety-boundary set declared by RUNTIME_GOVERNANCE"},
    {"id": "no-escalation-failure",      "metric": "every triggered escalation reaches a declared receiver state"},
    {"id": "no-continuity-loss",         "metric": "every interruption produces checkpoint or degradation record (no silent loss)"},
    {"id": "no-ambiguous-guidance",      "metric": "ambiguity is surfaced with candidate set; never silently picked"},
    {"id": "no-low-confidence-execution","metric": "uncertain-confidence outputs do not advance to guidance emission without supervised review"},
    {"id": "no-provenance-loss",         "metric": "every emitted package carries a provenance manifest"},
    {"id": "no-supervision-loss",        "metric": "every supervised boundary carries a supervision receipt"},
    {"id": "no-governance-bypass",       "metric": "no flow bypasses lifecycle P-tier, schema-pin, or any prior contract"},
]

SAFETY_RULES = [
    "All safety predicates are mandatory throughout the prototype run.",
    "Failure of any predicate immediately demotes the slice.",
    "Validation results are append-only and signed.",
    "Predicates are evaluated continuously, not only at completion.",
]


# ---------------------------------------------------------------------------
# TASK 7 — Observability
# ---------------------------------------------------------------------------

OBSERVABILITY_CHANNELS = [
    {"id": "reasoning-trace",       "binds_to": "chain-record",        "format": "append-only ndjson"},
    {"id": "retrieval-trace",       "binds_to": "retrieval-package",   "format": "append-only ndjson"},
    {"id": "escalation-trace",      "binds_to": "escalation-package",  "format": "append-only ndjson"},
    {"id": "continuity-trace",      "binds_to": "checkpoint-record",   "format": "append-only ndjson"},
    {"id": "orchestration-trace",   "binds_to": "run-id + slice-id",   "format": "append-only ndjson"},
    {"id": "operational-audit-log", "binds_to": "supervision-receipt", "format": "append-only ndjson"},
]

OBSERVABILITY_RULES = [
    "All channels are append-only; mutation is unsafe.",
    "Every emission carries a provenance reference.",
    "Every channel binds to run-id + slice-id; cross-run aggregation is out of prototype scope.",
    "Replay must be deterministic from the captured channels alone.",
    "No channel may carry destructive operation logs (none are produced).",
]


# ---------------------------------------------------------------------------
# TASK 8 — Prototype governance philosophy (constitutional root)
# ---------------------------------------------------------------------------

PROTOTYPE_PHILOSOPHY = [
    "A prototype is operational evidence at the smallest defensible scale.",
    "A prototype is supervised, controlled, and demotable.",
    "A prototype validates the architecture; it does not extend it.",
    "A prototype remains subordinate to the governed knowledge-core forever.",
    "A prototype is not a product, not a pilot, not a release.",
]

SUPERVISED_RUNTIME_DOCTRINE = [
    "Supervision is the default; autonomy is out of scope.",
    "Supervision boundaries are declared, gated, and audited.",
    "Supervision overrides cannot relax safety-preserving adaptations.",
    "Supervision receipts are append-only and provenance-signed.",
]

PROOF_METHODOLOGY = [
    "Define the smallest read-only slice that exercises retrieval + assembly + guidance.",
    "Declare evidence per step; evidence is binding.",
    "Run under operator observation with append-only traces.",
    "Promote only on documented evidence; demote on any anomaly.",
]

RUNTIME_SAFETY_PHILOSOPHY = [
    "Safety predicates are continuous, not terminal.",
    "Failure demotes; it does not silently pass.",
    "Irreversibility warnings cannot be downgraded.",
    "Hallucination is treated as a halt event, not a quality issue.",
]

ESCALATION_PHILOSOPHY = [
    "Escalation is monotonic; tier never decreases.",
    "Escalation produces append-only records with continuity bindings.",
    "Escalation locks the slice into a read-only handoff state.",
    "Escalation is a safety mechanism, not a fallback for low quality.",
]

OBSERVABILITY_PHILOSOPHY = [
    "What cannot be observed cannot be validated.",
    "What cannot be replayed cannot be approved.",
    "What cannot be demoted cannot be safely promoted.",
    "Audit trails are append-only by construction.",
]


# ---------------------------------------------------------------------------
# TASK 9 — Production transition
# ---------------------------------------------------------------------------

TRANSITIONS = [
    {
        "from": "prototype",
        "to": "supervised-pilot",
        "exit_criteria": [
            "all retrieval predicates pass for the slice",
            "all safety predicates pass continuously",
            "no contract violation observed",
            "operator-signed prototype report exists",
        ],
        "demotion_triggers": ["safety predicate failure", "contract violation", "operator demotion"],
    },
    {
        "from": "supervised-pilot",
        "to": "controlled-operational-deployment",
        "exit_criteria": [
            "bounded user population success criteria met",
            "incident review clean",
            "rollback path verified end-to-end",
        ],
        "demotion_triggers": ["unresolved escalation", "rollback failure", "operator demotion"],
    },
    {
        "from": "controlled-operational-deployment",
        "to": "future-production-cognition-runtime",
        "exit_criteria": [
            "regression suite green",
            "ecosystem observability green",
            "kill-switch verified",
            "post-deployment review clean",
        ],
        "demotion_triggers": ["regression", "observability red", "post-deployment finding", "operator demotion"],
    },
]

TRANSITION_RULES = [
    "Transitions are sequential; no skipping.",
    "Each transition carries explicit exit criteria and demotion triggers.",
    "Promotion requires a documented exit decision with provenance.",
    "Demotion requires no decision; it is the safe response to anomalies.",
    "All transitions remain subordinate to knowledge-core.",
]


# ---------------------------------------------------------------------------
# Readiness assessment
# ---------------------------------------------------------------------------

READINESS_CRITERIA = [
    "first slice declared and read-only",
    "all six runtime layers declared with provenance contracts",
    "all six prototype flows declared with evidence keys",
    "retrieval pipeline declared with predicate validation",
    "supervision posture declared and gated",
    "safety predicates declared and continuously evaluated",
    "observability channels declared and append-only",
    "transition path declared with demotion triggers",
]

PROTOTYPE_RISKS = [
    {"id": "no-evidence-channel-emitter",     "severity": "high",   "impact": "evidence keys cannot be physically produced"},
    {"id": "no-provenance-emitter",           "severity": "high",   "impact": "no package can be audit-signed"},
    {"id": "no-supervision-receipt-emitter",  "severity": "high",   "impact": "supervision boundaries cannot be audited"},
    {"id": "no-context-vector-emitter",       "severity": "high",   "impact": "assembly degrades; guidance gated"},
    {"id": "no-confidence-tier-on-nodes",     "severity": "high",   "impact": "low-confidence-execution predicate cannot bind"},
    {"id": "no-checkpoint-registry",          "severity": "high",   "impact": "battery-recovery + continuity-trace degrade"},
    {"id": "no-causal-edges-emitted",         "severity": "high",   "impact": "troubleshooting traversal cannot be exercised"},
    {"id": "no-hypothesis-store",             "severity": "high",   "impact": "troubleshooting/recovery hypotheses cannot persist"},
    {"id": "thin-troubleshooting-corpus",     "severity": "high",   "impact": "troubleshooting-lookup not eligible on most products"},
    {"id": "warning-corpus-gap",              "severity": "high",   "impact": "warning-stamping gated on affected products"},
    {"id": "no-incident-id-emitter",          "severity": "high",   "impact": "cross-step continuity binding unavailable"},
    {"id": "no-replay-harness",               "severity": "medium", "impact": "deterministic replay not yet possible"},
    {"id": "no-ground-truth-set",             "severity": "medium", "impact": "semantic-recall cannot be quantified"},
    {"id": "no-operator-identity-channel",    "severity": "medium", "impact": "override records cannot bind operator identity"},
    {"id": "no-prototype-report-template",    "severity": "medium", "impact": "operator-signed report not standardized"},
]


def assess_readiness():
    eligible_flows = [f["id"] for f in USER_FLOWS if f["in_scope"]]
    high_risks = [r["id"] for r in PROTOTYPE_RISKS if r["severity"] == "high"]
    return {
        "criteria": READINESS_CRITERIA,
        "first_slice": "contextual-onboarding + troubleshooting-retrieval",
        "eligible_flows_in_prototype_scope": eligible_flows,
        "modeling_complete": True,
        "execution_eligible_today": False,
        "blocking_emitters_required_for_execution": high_risks,
        "doctrine": "the prototype is fully modeled; execution requires the declared evidence emitters to exist and be wired",
        "recommended_first_run_slice": "contextual-retrieval-proof (per Phase 24 first-runtime proof)",
    }


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build():
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    (CONST_ROOT / "README.md").write_text(
        "# PROTOTYPE RUNTIME GOVERNANCE\n\n"
        "Nineteenth constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all eighteen prior governance layers.\n\n"
        "Models the first supervised operational runtime prototype around the "
        "contextual-onboarding + troubleshooting-retrieval slice. Does not implement "
        "production runtimes, autonomous agents, frontends, image generators, or PDF renderers.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Prototype Runtime Governance",
        "Declares the principles and authority of this layer. Subordinate to knowledge-core and to all eighteen prior governance layers.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Authority", md_list(CHARTER_AUTHORITY)),
            ("Hard Exclusions", md_list([
                "DO NOT build autonomous agents",
                "DO NOT deploy production systems",
                "DO NOT generate images",
                "DO NOT create PDFs",
                "DO NOT build large frontend ecosystems",
                "DO NOT optimize scale/performance",
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
                "ECOSYSTEM_INTEROPERABILITY", "REALIZATION_AND_DEPLOYMENT",
                "OPERATIONAL_PROOF",
            ],
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "runtime-architecture", "runtime-architecture",
        "Prototype Runtime Architecture",
        "Six declared runtime layers with contracts, emissions, and supervision posture.",
        [
            ("Layers", md_list([f"`{l['id']}` — {l['responsibility']} (supervision: {l['supervision']})" for l in ARCH_LAYERS])),
            ("Rules", md_list(ARCH_RULES)),
        ],
        {"schema": SCHEMA, "kind": "runtime-architecture", "layers": ARCH_LAYERS, "rules": ARCH_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "user-flows", "user-flows",
        "First Executable User Flows",
        "Six declared prototype flows around onboarding + troubleshooting + escalation.",
        [
            ("Flows", md_list([f"`{f['id']}` ({f['kind']}) — supervision: {f['supervision']} — in scope: {f['in_scope']}" for f in USER_FLOWS])),
            ("Rules", md_list(FLOW_RULES)),
        ],
        {"schema": SCHEMA, "kind": "user-flows", "flows": USER_FLOWS, "rules": FLOW_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "retrieval-pipeline", "retrieval-pipeline",
        "Executable Retrieval Pipeline",
        "Six declared retrieval kinds with predicate validation and a shared six-stage pipeline.",
        [
            ("Stages", md_list(PIPELINE_STAGES)),
            ("Kinds", md_list([f"`{k['id']}` — predicates: {', '.join(k['validation'])}" for k in RETRIEVAL_KINDS])),
            ("Rules", md_list(PIPELINE_RULES)),
        ],
        {"schema": SCHEMA, "kind": "retrieval-pipeline", "stages": PIPELINE_STAGES, "kinds": RETRIEVAL_KINDS, "rules": PIPELINE_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "context-assembly", "context-assembly",
        "Contextual Assembly Execution",
        "Four declared assembly flows merging procedures, warnings, prerequisites, troubleshooting, escalation, continuity, and adaptive guidance.",
        [
            ("Flows", md_list([f"`{f['id']}` — merges: {', '.join(f['merges'])}" for f in ASSEMBLY_FLOWS])),
            ("Rules", md_list(ASSEMBLY_RULES)),
        ],
        {"schema": SCHEMA, "kind": "context-assembly", "flows": ASSEMBLY_FLOWS, "rules": ASSEMBLY_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "supervision", "supervision",
        "Supervised Operational Guidance",
        "Supervision posture, uncertainty surfacing, escalation triggers, unsafe-guidance interruption, review checkpoints, operator override.",
        [
            ("Supervised behavior", md_list(SUPERVISED_BEHAVIOR)),
            ("Uncertainty surfacing", md_list(UNCERTAINTY_SURFACING)),
            ("Escalation triggers", md_list(ESCALATION_TRIGGERS)),
            ("Unsafe-guidance interruption", md_list(UNSAFE_GUIDANCE_INTERRUPTION)),
            ("Review checkpoints", md_list(REVIEW_CHECKPOINTS)),
            ("Operator override", md_list(OPERATOR_OVERRIDE)),
        ],
        {
            "schema": SCHEMA, "kind": "supervision",
            "supervised_behavior": SUPERVISED_BEHAVIOR,
            "uncertainty_surfacing": UNCERTAINTY_SURFACING,
            "escalation_triggers": ESCALATION_TRIGGERS,
            "unsafe_guidance_interruption": UNSAFE_GUIDANCE_INTERRUPTION,
            "review_checkpoints": REVIEW_CHECKPOINTS,
            "operator_override": OPERATOR_OVERRIDE,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "safety-validation", "safety-validation",
        "Operational Safety Validation",
        "Nine declared safety predicates evaluated continuously throughout any prototype run.",
        [
            ("Predicates", md_list([f"`{p['id']}` — {p['metric']}" for p in SAFETY_PREDICATES])),
            ("Rules", md_list(SAFETY_RULES)),
        ],
        {"schema": SCHEMA, "kind": "safety-validation", "predicates": SAFETY_PREDICATES, "rules": SAFETY_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "observability", "observability",
        "Prototype Observability",
        "Six declared append-only channels enabling deterministic replay and operational audit.",
        [
            ("Channels", md_list([f"`{c['id']}` → {c['binds_to']} ({c['format']})" for c in OBSERVABILITY_CHANNELS])),
            ("Rules", md_list(OBSERVABILITY_RULES)),
        ],
        {"schema": SCHEMA, "kind": "observability", "channels": OBSERVABILITY_CHANNELS, "rules": OBSERVABILITY_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "prototype-governance", "prototype-governance",
        "Prototype Governance Doctrine",
        "Philosophy + doctrine for the prototype, supervised runtime, proof methodology, runtime safety, escalation, observability.",
        [
            ("Prototype philosophy", md_list(PROTOTYPE_PHILOSOPHY)),
            ("Supervised-runtime doctrine", md_list(SUPERVISED_RUNTIME_DOCTRINE)),
            ("Operational proof methodology", md_list(PROOF_METHODOLOGY)),
            ("Runtime safety philosophy", md_list(RUNTIME_SAFETY_PHILOSOPHY)),
            ("Escalation philosophy", md_list(ESCALATION_PHILOSOPHY)),
            ("Observability philosophy", md_list(OBSERVABILITY_PHILOSOPHY)),
        ],
        {
            "schema": SCHEMA, "kind": "prototype-governance",
            "philosophy": PROTOTYPE_PHILOSOPHY,
            "supervised_runtime": SUPERVISED_RUNTIME_DOCTRINE,
            "proof_methodology": PROOF_METHODOLOGY,
            "runtime_safety": RUNTIME_SAFETY_PHILOSOPHY,
            "escalation_philosophy": ESCALATION_PHILOSOPHY,
            "observability_philosophy": OBSERVABILITY_PHILOSOPHY,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "production-transition", "production-transition",
        "Production Transition Path",
        "Three declared transitions: prototype → supervised pilot → controlled operational deployment → future production cognition runtimes.",
        [
            ("Transitions", md_list([f"`{t['from']}` → `{t['to']}` (exit criteria: {len(t['exit_criteria'])}, demotion triggers: {len(t['demotion_triggers'])})" for t in TRANSITIONS])),
            ("Rules", md_list(TRANSITION_RULES)),
        ],
        {"schema": SCHEMA, "kind": "production-transition", "transitions": TRANSITIONS, "rules": TRANSITION_RULES, "generated": now_iso()},
    )

    readiness = assess_readiness()

    reports = [
        ("01-runtime-architecture-summary.json", {
            "schema": SCHEMA,
            "layers": ARCH_LAYERS,
            "rules": ARCH_RULES,
        }),
        ("02-executable-user-flow-summary.json", {
            "schema": SCHEMA,
            "flows": USER_FLOWS,
            "in_scope": [f["id"] for f in USER_FLOWS if f["in_scope"]],
            "rules": FLOW_RULES,
        }),
        ("03-retrieval-pipeline-summary.json", {
            "schema": SCHEMA,
            "stages": PIPELINE_STAGES,
            "kinds": RETRIEVAL_KINDS,
            "rules": PIPELINE_RULES,
        }),
        ("04-contextual-assembly-summary.json", {
            "schema": SCHEMA,
            "flows": ASSEMBLY_FLOWS,
            "rules": ASSEMBLY_RULES,
        }),
        ("05-supervision-summary.json", {
            "schema": SCHEMA,
            "supervised_behavior": SUPERVISED_BEHAVIOR,
            "uncertainty_surfacing": UNCERTAINTY_SURFACING,
            "escalation_triggers": ESCALATION_TRIGGERS,
            "unsafe_guidance_interruption": UNSAFE_GUIDANCE_INTERRUPTION,
            "review_checkpoints": REVIEW_CHECKPOINTS,
            "operator_override": OPERATOR_OVERRIDE,
        }),
        ("06-safety-validation-summary.json", {
            "schema": SCHEMA,
            "predicates": SAFETY_PREDICATES,
            "rules": SAFETY_RULES,
        }),
        ("07-observability-summary.json", {
            "schema": SCHEMA,
            "channels": OBSERVABILITY_CHANNELS,
            "rules": OBSERVABILITY_RULES,
        }),
        ("08-prototype-governance-summary.json", {
            "schema": SCHEMA,
            "philosophy_blocks": {
                "prototype_philosophy": len(PROTOTYPE_PHILOSOPHY),
                "supervised_runtime": len(SUPERVISED_RUNTIME_DOCTRINE),
                "proof_methodology": len(PROOF_METHODOLOGY),
                "runtime_safety": len(RUNTIME_SAFETY_PHILOSOPHY),
                "escalation_philosophy": len(ESCALATION_PHILOSOPHY),
                "observability_philosophy": len(OBSERVABILITY_PHILOSOPHY),
            },
        }),
        ("09-production-transition-summary.json", {
            "schema": SCHEMA,
            "transitions": TRANSITIONS,
            "rules": TRANSITION_RULES,
        }),
        ("10-operational-prototype-readiness-assessment.json", {
            "schema": SCHEMA,
            **readiness,
            "risks": PROTOTYPE_RISKS,
            "risk_total": len(PROTOTYPE_RISKS),
            "risk_high": [r["id"] for r in PROTOTYPE_RISKS if r["severity"] == "high"],
            "risk_medium": [r["id"] for r in PROTOTYPE_RISKS if r["severity"] == "medium"],
        }),
    ]

    for name, payload in reports:
        (REPORTS_ROOT / name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    file_count = sum(1 for _ in CONST_ROOT.rglob("*") if _.is_file())
    high_risks = [r["id"] for r in PROTOTYPE_RISKS if r["severity"] == "high"]
    print(
        "Prototype runtime modeling complete.\n"
        f"  Constitutional root: {CONST_ROOT}\n"
        f"  Reports: {REPORTS_ROOT}/01..10\n"
        f"  Layers: {len(ARCH_LAYERS)} | Flows: {len(USER_FLOWS)} | Retrieval kinds: {len(RETRIEVAL_KINDS)} | "
        f"Assembly flows: {len(ASSEMBLY_FLOWS)} | Safety predicates: {len(SAFETY_PREDICATES)} | "
        f"Observability channels: {len(OBSERVABILITY_CHANNELS)} | Transitions: {len(TRANSITIONS)} | "
        f"Risks: {len(PROTOTYPE_RISKS)} (high: {len(high_risks)}).\n"
        f"  First slice: contextual-onboarding + troubleshooting-retrieval.\n"
        f"  Modeling complete: True | Execution eligible today: {readiness['execution_eligible_today']}.\n"
        f"  Files written under constitutional root: {file_count}"
    )


if __name__ == "__main__":
    build()
