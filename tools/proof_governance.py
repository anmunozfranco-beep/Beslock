"""
Phase 24 — EXECUTABLE OPERATIONAL PROOF-OF-VALUE (modeling-only).

Eighteenth constitutional layer. Subordinate to knowledge-core and to all
seventeen prior governance layers. Models how the cognition ecosystem produces
controlled, executable proof-of-value operational slices — without implementing
production runtimes, chatbots, frontends, image generators, PDF renderers, or
autonomous agents.

Hard exclusions (verbatim):
- DO NOT build production chatbots
- DO NOT build frontend systems
- DO NOT generate images
- DO NOT create PDFs
- DO NOT implement autonomous agents
- DO NOT deploy production runtimes

Idempotent. Non-destructive. Reads no per-product knowledge-core files.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "OPERATIONAL_PROOF_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "operational-proof"

SCHEMA = "operational-proof-governance/1.0"


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
    "This proof-of-value layer is itself modeling-only; it executes nothing.",
    "Proof-of-value is controlled, supervised, and bounded — never a production launch.",
    "Proof-of-value validates the ecosystem; it does not extend it.",
    "Every executable slice is read-only by default; destructive surfaces are out of scope for proof.",
    "Every executable slice produces evidence (traces, receipts, provenance manifests) or it is not a proof.",
    "Every executable slice is demotable; demotion is the safe response to any anomaly.",
    "Hard exclusions (no chatbots, no frontends, no PDFs, no images, no autonomous agents, no production runtimes) bind every proof slice.",
    "Proof-of-value cannot promote P-tier, elevate confidence, or alter prior governance layers.",
    "Operator supervision is mandatory at every cognition boundary inside a proof slice.",
    "All proof-of-value remains subordinate to the governed knowledge-core forever.",
]

CHARTER_AUTHORITY = [
    "Declares the catalog of first executable slices and their selection criteria.",
    "Declares executable context-assembly flows and their evidence requirements.",
    "Declares retrieval-validation predicates per retrieval kind.",
    "Declares operational-guidance execution surfaces and their supervision postures.",
    "Declares the human-supervision model for proof slices.",
    "Declares the safety-validation predicate set and unsafe-flow taxonomy.",
    "Declares the proof-of-value governance philosophy.",
    "Declares the proof → supervised pilot → controlled runtime → future production roadmap transitions.",
    "Declares the first-runtime proof assessment criteria and outcome.",
    "Declares that proof-of-value remains subordinate to knowledge-core and to all seventeen prior layers.",
]


# ---------------------------------------------------------------------------
# TASK 1 — First executable slice selection
# ---------------------------------------------------------------------------

SELECTION_CRITERIA = [
    {"id": "operational-value",      "weight": 0.20},
    {"id": "runtime-risk-inverse",   "weight": 0.20},
    {"id": "validates-architecture", "weight": 0.15},
    {"id": "validates-retrieval",    "weight": 0.15},
    {"id": "validates-assembly",     "weight": 0.15},
    {"id": "validates-coherence",    "weight": 0.15},
]

SLICE_CANDIDATES = [
    {
        "id": "contextual-retrieval-proof",
        "kind": "first executable slice",
        "scores": {"operational-value": 4, "runtime-risk-inverse": 5, "validates-architecture": 5,
                   "validates-retrieval": 5, "validates-assembly": 4, "validates-coherence": 4},
        "destructive_surface": False,
        "blocking_risks": [],
        "soft_risks": ["no-provenance-emitter"],
        "supervision": "operator-observed (read-only outputs)",
    },
    {
        "id": "procedural-assistance-proof",
        "kind": "second executable slice",
        "scores": {"operational-value": 4, "runtime-risk-inverse": 4, "validates-architecture": 5,
                   "validates-retrieval": 4, "validates-assembly": 5, "validates-coherence": 5},
        "destructive_surface": False,
        "blocking_risks": [],
        "soft_risks": ["no-context-vector-emitter", "no-confidence-tier-on-nodes"],
        "supervision": "operator-observed; supervised when context vector absent",
    },
    {
        "id": "onboarding-guidance-proof",
        "kind": "deferred (supervised-pilot)",
        "scores": {"operational-value": 4, "runtime-risk-inverse": 3, "validates-architecture": 4,
                   "validates-retrieval": 4, "validates-assembly": 4, "validates-coherence": 4},
        "destructive_surface": False,
        "blocking_risks": ["no-checkpoint-registry", "no-intent-declaration-channel"],
        "soft_risks": [],
        "supervision": "supervised end-to-end",
    },
    {
        "id": "troubleshooting-guidance-proof",
        "kind": "deferred (corpus-bound)",
        "scores": {"operational-value": 5, "runtime-risk-inverse": 2, "validates-architecture": 4,
                   "validates-retrieval": 3, "validates-assembly": 4, "validates-coherence": 3},
        "destructive_surface": False,
        "blocking_risks": ["thin-troubleshooting-corpus", "no-causal-edges-emitted", "no-hypothesis-store"],
        "soft_risks": [],
        "supervision": "supervised end-to-end",
    },
    {
        "id": "operational-recovery-assistance-proof",
        "kind": "deferred (continuity-bound)",
        "scores": {"operational-value": 4, "runtime-risk-inverse": 2, "validates-architecture": 4,
                   "validates-retrieval": 3, "validates-assembly": 4, "validates-coherence": 4},
        "destructive_surface": False,
        "blocking_risks": ["no-checkpoint-registry", "no-causal-edges-emitted", "no-hypothesis-store"],
        "soft_risks": [],
        "supervision": "supervised end-to-end",
    },
    {
        "id": "administrator-guidance-proof",
        "kind": "deferred (destructive surface — out of scope for proof)",
        "scores": {"operational-value": 3, "runtime-risk-inverse": 1, "validates-architecture": 3,
                   "validates-retrieval": 3, "validates-assembly": 3, "validates-coherence": 3},
        "destructive_surface": True,
        "blocking_risks": ["destructive-surface-out-of-proof-scope", "oem-channel-contract-missing", "role-declaration-missing"],
        "soft_risks": [],
        "supervision": "not eligible for proof",
    },
]


def weighted(c):
    return round(sum(c["scores"][d["id"]] * d["weight"] for d in SELECTION_CRITERIA), 3)


for c in SLICE_CANDIDATES:
    c["weighted_score"] = weighted(c)
    c["proof_eligible"] = (not c["destructive_surface"]) and (not c["blocking_risks"])

SLICE_RANKING = sorted(SLICE_CANDIDATES, key=lambda c: c["weighted_score"], reverse=True)

SELECTION_RULES = [
    "First executable slice MUST be read-only and have no blocking risks.",
    "Destructive surfaces are out of scope for proof-of-value.",
    "Soft risks degrade the slice to operator-observed mode but do not block.",
    "Score updates require evidence; ad-hoc reweighting is unsafe.",
    "Selected slice must validate retrieval + assembly + coherence simultaneously.",
]


# ---------------------------------------------------------------------------
# TASK 2 — Executable context assembly
# ---------------------------------------------------------------------------

ASSEMBLY_FLOWS = [
    {
        "id": "retrieval-flow",
        "steps": [
            "bind query intent to declared access pattern",
            "resolve hierarchy + filters",
            "fetch read-only nodes from declared stable surfaces",
            "attach provenance manifest",
            "emit retrieval-package",
        ],
        "evidence": ["retrieval-package-id", "provenance-manifest-ref", "query-intent-id"],
    },
    {
        "id": "procedural-guidance-flow",
        "steps": [
            "consume retrieval-package (read-only)",
            "apply COMPOSITION assembly rules",
            "select profile per ADAPTIVE precedence (or safest default)",
            "emit guidance-package (read-only)",
        ],
        "evidence": ["guidance-package-id", "adaptation-record-ref", "profile-id"],
    },
    {
        "id": "warning-surface-flow",
        "steps": [
            "enumerate mandatory warnings attached to selected nodes",
            "stamp warning-record with severity + source",
            "block guidance emission if mandatory warning is unverified",
        ],
        "evidence": ["warning-record-ref", "severity", "source-node-id"],
    },
    {
        "id": "escalation-flow",
        "steps": [
            "evaluate declared escalation predicates",
            "snapshot continuity (read-only, append-only history)",
            "build 12-field escalation package",
            "lock proof slice to read-only handoff state",
        ],
        "evidence": ["escalation-package-ref", "continuity-snapshot-ref", "tier"],
    },
    {
        "id": "continuity-flow",
        "steps": [
            "load declared timeline + context vector",
            "verify checkpoint integrity (when registry exists)",
            "filter non-inheritable signals at boundary",
            "emit restoration-record",
        ],
        "evidence": ["timeline-id", "checkpoint-id", "non-inheritable-filter-record"],
    },
    {
        "id": "adaptive-guidance-flow",
        "steps": [
            "compute guidance adaptation per ADAPTIVE rules",
            "respect 4-tier precedence (knowledge-core>adaptive)",
            "never override safety-preserving adaptations",
            "emit adaptation-record",
        ],
        "evidence": ["adaptation-record-ref", "precedence-rule-id"],
    },
    {
        "id": "reasoning-trace-flow",
        "steps": [
            "consume assembly-package (read-only)",
            "traverse declared causal relations only",
            "track hypothesis lifecycle stages",
            "emit chain-record",
        ],
        "evidence": ["chain-record-ref", "termination-outcome", "edges-traversed[]"],
    },
]

ASSEMBLY_RULES = [
    "Flows are declared; no flow may be invented during a proof slice.",
    "Every flow emits provenance; an unobserved step invalidates the proof.",
    "Flows are read-only; destructive transitions are out of scope for proof-of-value.",
    "Mandatory warnings cannot be suppressed at any flow.",
    "Adaptive guidance never elevates confidence to compensate for missing inputs.",
]


# ---------------------------------------------------------------------------
# TASK 3 — Retrieval validation
# ---------------------------------------------------------------------------

RETRIEVAL_PREDICATES = [
    {"id": "semantic-precision-≥-threshold",      "kind": "semantic",       "metric": "fraction of retrieved nodes that match query intent"},
    {"id": "semantic-recall-≥-threshold",         "kind": "semantic",       "metric": "fraction of relevant nodes returned vs declared ground-truth set"},
    {"id": "contextual-coherence-no-contradiction","kind": "contextual",    "metric": "no chain of retrieved nodes contradicts knowledge-core verified-truth"},
    {"id": "guidance-completeness-mandatory-warnings","kind": "guidance",   "metric": "every mandatory warning attached to selected nodes is present in package"},
    {"id": "guidance-completeness-required-steps","kind": "guidance",       "metric": "every required step in declared workflow is present in package"},
    {"id": "onboarding-coverage",                 "kind": "onboarding",     "metric": "every declared onboarding flow has retrievable bound nodes"},
    {"id": "troubleshooting-coverage-symptom",    "kind": "troubleshooting","metric": "for each symptom, ≥1 retrievable diagnostic node exists"},
    {"id": "troubleshooting-coverage-causal",     "kind": "troubleshooting","metric": "for each symptom, declared causal edges are traversable"},
    {"id": "escalation-retrievability",           "kind": "escalation",     "metric": "for every declared escalation predicate, retrievable handoff procedure exists"},
    {"id": "provenance-attachment",               "kind": "all",            "metric": "every retrieval-package carries a provenance manifest"},
]

RETRIEVAL_VALIDATION_RULES = [
    "Predicates are declared; ad-hoc validation is unsafe.",
    "Failure of any high-severity predicate blocks promotion of the slice past proof.",
    "Validation results are append-only and signed with provenance.",
    "Validation cannot mutate knowledge-core under any circumstance.",
    "Predicates are evaluated per product when scope is per-product.",
]


# ---------------------------------------------------------------------------
# TASK 4 — Guidance execution surfaces
# ---------------------------------------------------------------------------

GUIDANCE_SURFACES = [
    {"id": "executable-onboarding",     "kind": "onboarding",     "supervision": "supervised end-to-end", "destructive": False, "in_scope_for_proof": False, "blocked_by": ["no-checkpoint-registry", "no-intent-declaration-channel"]},
    {"id": "executable-troubleshooting","kind": "troubleshooting","supervision": "supervised end-to-end", "destructive": False, "in_scope_for_proof": False, "blocked_by": ["thin-troubleshooting-corpus", "no-causal-edges-emitted", "no-hypothesis-store"]},
    {"id": "executable-recovery",       "kind": "recovery",       "supervision": "supervised end-to-end", "destructive": False, "in_scope_for_proof": False, "blocked_by": ["no-checkpoint-registry", "no-causal-edges-emitted"]},
    {"id": "executable-contextual-assistance","kind": "contextual","supervision": "operator-observed", "destructive": False, "in_scope_for_proof": True, "blocked_by": []},
]

GUIDANCE_RULES = [
    "Guidance surfaces declare supervision posture, scope, and blockers.",
    "Only surfaces with no blocking risks and no destructive surface are in scope for proof.",
    "Guidance surfaces emit guidance-packages bound to a retrieval-package + adaptation-record.",
    "Guidance surfaces never execute destructive operations during proof.",
    "Guidance surfaces respect lifecycle P-tier gates and may not release un-promoted content.",
]


# ---------------------------------------------------------------------------
# TASK 5 — Human supervision
# ---------------------------------------------------------------------------

REVIEW_CHECKPOINTS = [
    "pre-emission (operator inspects retrieval-package + assembly-package before any guidance-package release)",
    "post-emission (operator reviews emitted guidance-package and chain-record)",
    "pre-handoff (operator approves any escalation handoff)",
    "pre-completion (operator confirms no open warnings, no unresolved escalations)",
    "post-anomaly (operator reviews anomaly + decides demotion)",
]

ESCALATION_INTERVENTION = [
    "operator may raise escalation tier at any review checkpoint",
    "operator may NOT lower escalation tier (monotonic)",
    "operator may demote the proof slice at any time",
    "operator may halt the slice on any open contract violation",
]

UNCERTAINTY_SURFACING = [
    "confidence tier is disclosed at the operator boundary; never silently elevated",
    "ambiguity surfaces with all candidate options + their declared sources",
    "contradictions surface verbatim with both source nodes",
    "uncertain-confidence outputs are labeled and gated",
]

OPERATOR_OVERRIDE = [
    "operator may approve / reject / request more info / escalate / demote",
    "operator cannot override safety-preserving adaptations",
    "operator cannot downgrade irreversibility warnings",
    "operator overrides are recorded with identity (when declared) + provenance + timestamp",
]

COGNITION_SUPERVISION = [
    "every cognition boundary inside the proof slice carries a supervision receipt",
    "every supervision receipt is append-only and provenance-signed",
    "missing supervision receipt = unsafe; the step is invalid",
]

UNSAFE_RUNTIME_INTERRUPTION = [
    "operator-cancel → graceful return to last checkpointed state (read-only by default in proof)",
    "contract-violation → force escalating + halt slice",
    "validation-predicate-failed → force demotion or escalating",
    "ambiguity-unresolved → force escalating",
    "explicit-action-timeout → force blocked (proof has no destructive paths, so this is informational)",
]


# ---------------------------------------------------------------------------
# TASK 6 — Safety validation
# ---------------------------------------------------------------------------

SAFETY_PREDICATES = [
    {"id": "no-unsafe-operational-flow",   "metric": "no flow violates the declared safety-boundary set from RUNTIME_GOVERNANCE"},
    {"id": "no-hallucination",             "metric": "every retrieved node is present in knowledge-core; no invented nodes; no invented steps"},
    {"id": "no-escalation-failure",        "metric": "every triggered escalation reaches a declared receiver state (handed-off or queued+locked)"},
    {"id": "no-continuity-loss",           "metric": "every interruption produces a checkpoint-or-degradation record; no silent loss"},
    {"id": "no-retrieval-ambiguity-silent","metric": "ambiguity in retrieval is surfaced (never silently picked)"},
    {"id": "no-low-confidence-execution",  "metric": "uncertain-confidence outputs do not advance to guidance emission without supervised review"},
    {"id": "no-governance-bypass",         "metric": "no flow bypasses lifecycle P-tier gates, schema-pin, or any prior layer's contract"},
    {"id": "no-irreversibility-bypass",    "metric": "irreversibility warnings are never downgraded; two-token gate is honored when destructive surfaces are touched (out of proof scope)"},
    {"id": "no-provenance-loss",           "metric": "every emitted package carries a provenance manifest"},
    {"id": "no-supervision-loss",          "metric": "every supervised boundary carries a supervision receipt"},
]

SAFETY_VALIDATION_RULES = [
    "All safety predicates are mandatory for any proof slice.",
    "Failure of any safety predicate immediately demotes the slice.",
    "Safety validation results are append-only and signed.",
    "Safety predicates are evaluated continuously, not only at completion.",
    "Safety validation cannot be retroactively assigned.",
]


# ---------------------------------------------------------------------------
# TASK 7 — Proof governance philosophy
# ---------------------------------------------------------------------------

PROOF_PHILOSOPHY = [
    "Proof-of-value is operational evidence, not marketing.",
    "Proof-of-value is supervised, controlled, and bounded.",
    "Proof-of-value validates the architecture; it does not extend it.",
    "Proof-of-value is demotable; demotion is the safe response to anomalies.",
    "Proof-of-value remains subordinate to the governed knowledge-core forever.",
]

EXECUTABLE_COGNITION_DOCTRINE = [
    "Executable cognition is the operationalization of declared cognition; it is never the creation of new cognition.",
    "Executable cognition is read-only by default in proof slices.",
    "Executable cognition emits provenance at every step.",
    "Executable cognition cannot promote P-tier or elevate confidence.",
]

SUPERVISED_REALIZATION_PHILOSOPHY = [
    "Supervision is the default; autonomy is not modelled here.",
    "Supervision boundaries are declared, gated, and audited.",
    "Supervision overrides cannot relax safety-preserving adaptations.",
    "Supervision approvals carry identity (when declared) + provenance + timestamp.",
]

RUNTIME_VALIDATION_DOCTRINE = [
    "Validation is predicate-based and append-only.",
    "Validation predicates are declared; ad-hoc validation is unsafe.",
    "Validation failures demote; they do not silently pass.",
    "Validation results bind to the slice id + run id + provenance manifest.",
]

PROOF_METHODOLOGY = [
    "Select the safest, highest-value read-only slice.",
    "Define executable context-assembly flows with evidence per step.",
    "Define retrieval and safety predicates with thresholds.",
    "Run under operator observation with append-only traces.",
    "Decide promotion or demotion strictly from evidence.",
]

VALIDATION_PRINCIPLES = [
    "What cannot be observed cannot be validated.",
    "What cannot be replayed cannot be approved.",
    "What cannot be demoted cannot be safely promoted.",
    "Evidence dominates intuition.",
]


# ---------------------------------------------------------------------------
# TASK 8 — Realization roadmap
# ---------------------------------------------------------------------------

ROADMAP_TRANSITIONS = [
    {
        "from": "proof-of-value-slice",
        "to": "supervised-operational-pilot",
        "exit_criteria": [
            "all retrieval predicates pass on declared scope",
            "all safety predicates pass continuously across the run window",
            "no contract violation observed",
            "operator-signed proof report exists",
        ],
        "demotion_triggers": ["any safety predicate failure", "any contract violation", "operator demotion decision"],
    },
    {
        "from": "supervised-operational-pilot",
        "to": "controlled-runtime-system",
        "exit_criteria": [
            "bounded user population success criteria met",
            "incident review clean (no unresolved escalations)",
            "proof-of-value report appended with pilot evidence",
            "rollback path verified end-to-end",
        ],
        "demotion_triggers": ["unresolved escalation", "rollback failure", "operator demotion decision"],
    },
    {
        "from": "controlled-runtime-system",
        "to": "future-production-operational-ecosystem",
        "exit_criteria": [
            "regression suite green",
            "ecosystem observability green",
            "post-deployment review clean",
            "kill-switch verified",
            "all interop contracts active and pinned",
        ],
        "demotion_triggers": ["regression", "ecosystem observability red", "post-deployment review finding", "operator demotion decision"],
    },
]

ROADMAP_RULES = [
    "Transitions are sequential; no skipping a transition that produced state.",
    "Each transition has explicit exit criteria and demotion triggers.",
    "Promotion requires a documented exit decision with provenance.",
    "Demotion does not require a decision; it is the safe response to anomalies.",
    "All transitions remain subordinate to the governed knowledge-core forever.",
]


# ---------------------------------------------------------------------------
# Operational-proof risks
# ---------------------------------------------------------------------------

PROOF_RISKS = [
    {"id": "no-evidence-channel",            "severity": "high",   "impact": "proof slices cannot be evidence-gated"},
    {"id": "no-provenance-emitter",          "severity": "high",   "impact": "no slice can produce audit-grade evidence"},
    {"id": "no-supervision-receipt-emitter", "severity": "high",   "impact": "supervised boundaries cannot be audited"},
    {"id": "no-context-vector-emitter",      "severity": "high",   "impact": "procedural-assistance proof degrades"},
    {"id": "no-confidence-tier-on-nodes",    "severity": "high",   "impact": "low-confidence-execution predicate cannot bind"},
    {"id": "no-checkpoint-registry",         "severity": "high",   "impact": "continuity proof flows degrade; recovery proofs deferred"},
    {"id": "no-causal-edges-emitted",        "severity": "high",   "impact": "reasoning-trace proof flow cannot enumerate edges"},
    {"id": "no-hypothesis-store",            "severity": "high",   "impact": "troubleshooting and recovery proofs cannot persist hypotheses"},
    {"id": "thin-troubleshooting-corpus",    "severity": "high",   "impact": "troubleshooting proof not eligible on most products"},
    {"id": "warning-corpus-gap",             "severity": "high",   "impact": "warning-surface proof gated on affected products"},
    {"id": "no-incident-id-emitter",         "severity": "high",   "impact": "cross-step continuity binding unavailable"},
    {"id": "no-ground-truth-set",            "severity": "medium", "impact": "semantic-recall predicate cannot be evaluated quantitatively"},
    {"id": "no-anomaly-channel",             "severity": "medium", "impact": "post-anomaly review checkpoint not formalized"},
    {"id": "no-proof-report-template",       "severity": "medium", "impact": "operator-signed proof report not standardized"},
    {"id": "no-replay-harness",              "severity": "medium", "impact": "proof runs cannot be deterministically replayed"},
]


# ---------------------------------------------------------------------------
# First-runtime proof assessment
# ---------------------------------------------------------------------------

FIRST_PROOF_CRITERIA = [
    "no destructive surface",
    "no blocking proof risks for the slice",
    "all four validators activated: architecture + retrieval + assembly + coherence",
    "operator review checkpoints declared and supervisable",
    "demotion path declared",
]


def assess_first_proof():
    eligible = [c for c in SLICE_CANDIDATES if c["proof_eligible"]]
    eligible.sort(key=lambda c: c["weighted_score"], reverse=True)
    primary = eligible[0] if eligible else None
    secondary = eligible[1] if len(eligible) > 1 else None
    return {
        "criteria": FIRST_PROOF_CRITERIA,
        "primary_first_runtime_proof": primary,
        "secondary_first_runtime_proof": secondary,
        "deferred_slices": [
            {"id": c["id"], "blocking_risks": c["blocking_risks"], "destructive_surface": c["destructive_surface"]}
            for c in SLICE_CANDIDATES if not c["proof_eligible"]
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
        "# OPERATIONAL PROOF GOVERNANCE\n\n"
        "Eighteenth constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all seventeen prior governance layers.\n\n"
        "Models how the cognition ecosystem produces controlled, executable proof-of-value "
        "operational slices. It does not implement production runtimes, agents, chatbots, "
        "frontends, image generators, PDF renderers, or autonomous cognition.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Operational Proof Governance",
        "Declares the principles and authority of this layer. Subordinate to knowledge-core and to all seventeen prior governance layers.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Authority", md_list(CHARTER_AUTHORITY)),
            ("Hard Exclusions", md_list([
                "DO NOT build production chatbots",
                "DO NOT build frontend systems",
                "DO NOT generate images",
                "DO NOT create PDFs",
                "DO NOT implement autonomous agents",
                "DO NOT deploy production runtimes",
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
            ],
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "first-slices", "first-slices",
        "First Executable Slice Selection",
        "Weighted ranking of executable proof-of-value candidates. Safety > runtime risk > value. Destructive surfaces are out of scope for proof.",
        [
            ("Selection criteria", md_list([f"`{c['id']}` (weight: {c['weight']})" for c in SELECTION_CRITERIA])),
            ("Candidates (ranked)", md_list([
                f"`{c['id']}` — score: {c['weighted_score']} — destructive: {c['destructive_surface']} — "
                f"blocking: {len(c['blocking_risks'])} — proof eligible: {c['proof_eligible']}"
                for c in SLICE_RANKING
            ])),
            ("Rules", md_list(SELECTION_RULES)),
        ],
        {
            "schema": SCHEMA, "kind": "first-slices",
            "criteria": SELECTION_CRITERIA,
            "candidates": SLICE_CANDIDATES,
            "ranking": [c["id"] for c in SLICE_RANKING],
            "rules": SELECTION_RULES,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "context-assembly", "context-assembly",
        "Executable Context Assembly",
        "Declared executable context-assembly flows with steps + evidence requirements per flow.",
        [
            ("Flows", md_list([f"`{f['id']}` — steps: {len(f['steps'])} — evidence keys: {', '.join(f['evidence'])}" for f in ASSEMBLY_FLOWS])),
            ("Rules", md_list(ASSEMBLY_RULES)),
        ],
        {"schema": SCHEMA, "kind": "context-assembly", "flows": ASSEMBLY_FLOWS, "rules": ASSEMBLY_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "retrieval-validation", "retrieval-validation",
        "Retrieval Execution Validation",
        "Declared retrieval validation predicates per retrieval kind.",
        [
            ("Predicates", md_list([f"`{p['id']}` ({p['kind']}) — {p['metric']}" for p in RETRIEVAL_PREDICATES])),
            ("Rules", md_list(RETRIEVAL_VALIDATION_RULES)),
        ],
        {"schema": SCHEMA, "kind": "retrieval-validation", "predicates": RETRIEVAL_PREDICATES, "rules": RETRIEVAL_VALIDATION_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "guidance-execution", "guidance-execution",
        "Operational Guidance Execution",
        "Declared executable guidance surfaces, supervision postures, scope, and blockers.",
        [
            ("Surfaces", md_list([f"`{s['id']}` ({s['kind']}) — supervision: {s['supervision']} — in scope: {s['in_scope_for_proof']}" for s in GUIDANCE_SURFACES])),
            ("Rules", md_list(GUIDANCE_RULES)),
        ],
        {"schema": SCHEMA, "kind": "guidance-execution", "surfaces": GUIDANCE_SURFACES, "rules": GUIDANCE_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "human-supervision", "human-supervision",
        "Human Supervision Model",
        "Review checkpoints, escalation intervention, uncertainty surfacing, operator override, cognition supervision, unsafe-runtime interruption.",
        [
            ("Review checkpoints", md_list(REVIEW_CHECKPOINTS)),
            ("Escalation intervention", md_list(ESCALATION_INTERVENTION)),
            ("Uncertainty surfacing", md_list(UNCERTAINTY_SURFACING)),
            ("Operator override", md_list(OPERATOR_OVERRIDE)),
            ("Cognition supervision", md_list(COGNITION_SUPERVISION)),
            ("Unsafe-runtime interruption", md_list(UNSAFE_RUNTIME_INTERRUPTION)),
        ],
        {
            "schema": SCHEMA, "kind": "human-supervision",
            "review_checkpoints": REVIEW_CHECKPOINTS,
            "escalation_intervention": ESCALATION_INTERVENTION,
            "uncertainty_surfacing": UNCERTAINTY_SURFACING,
            "operator_override": OPERATOR_OVERRIDE,
            "cognition_supervision": COGNITION_SUPERVISION,
            "unsafe_runtime_interruption": UNSAFE_RUNTIME_INTERRUPTION,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "safety-validation", "safety-validation",
        "Executable Safety Validation",
        "Declared safety predicates that must hold continuously throughout any proof slice.",
        [
            ("Predicates", md_list([f"`{p['id']}` — {p['metric']}" for p in SAFETY_PREDICATES])),
            ("Rules", md_list(SAFETY_VALIDATION_RULES)),
        ],
        {"schema": SCHEMA, "kind": "safety-validation", "predicates": SAFETY_PREDICATES, "rules": SAFETY_VALIDATION_RULES, "generated": now_iso()},
    )

    write_pair(
        CONST_ROOT / "proof-governance", "proof-governance",
        "Proof-of-Value Governance Doctrine",
        "Philosophy + doctrine for proof-of-value, executable cognition, supervised realization, runtime validation, methodology, and validation principles.",
        [
            ("Proof-of-value philosophy", md_list(PROOF_PHILOSOPHY)),
            ("Executable cognition doctrine", md_list(EXECUTABLE_COGNITION_DOCTRINE)),
            ("Supervised operational realization philosophy", md_list(SUPERVISED_REALIZATION_PHILOSOPHY)),
            ("Runtime validation doctrine", md_list(RUNTIME_VALIDATION_DOCTRINE)),
            ("Operational proof methodology", md_list(PROOF_METHODOLOGY)),
            ("Cognition validation principles", md_list(VALIDATION_PRINCIPLES)),
        ],
        {
            "schema": SCHEMA, "kind": "proof-governance",
            "philosophy": PROOF_PHILOSOPHY,
            "executable_cognition": EXECUTABLE_COGNITION_DOCTRINE,
            "supervised_realization": SUPERVISED_REALIZATION_PHILOSOPHY,
            "runtime_validation": RUNTIME_VALIDATION_DOCTRINE,
            "methodology": PROOF_METHODOLOGY,
            "validation_principles": VALIDATION_PRINCIPLES,
            "generated": now_iso(),
        },
    )

    write_pair(
        CONST_ROOT / "realization-roadmap", "realization-roadmap",
        "Realization Roadmap (Proof → Supervised Pilot → Controlled Runtime → Future Production)",
        "Declared transitions with exit criteria and demotion triggers. All transitions remain subordinate to the governed knowledge-core.",
        [
            ("Transitions", md_list([f"`{t['from']}` → `{t['to']}` (exit criteria: {len(t['exit_criteria'])}, demotion triggers: {len(t['demotion_triggers'])})" for t in ROADMAP_TRANSITIONS])),
            ("Rules", md_list(ROADMAP_RULES)),
        ],
        {"schema": SCHEMA, "kind": "realization-roadmap", "transitions": ROADMAP_TRANSITIONS, "rules": ROADMAP_RULES, "generated": now_iso()},
    )

    first_proof = assess_first_proof()

    reports = [
        ("01-first-slice-summary.json", {
            "schema": SCHEMA,
            "criteria": SELECTION_CRITERIA,
            "ranking": [{"id": c["id"], "weighted_score": c["weighted_score"], "proof_eligible": c["proof_eligible"], "blocking_risks": c["blocking_risks"], "soft_risks": c["soft_risks"]} for c in SLICE_RANKING],
            "rules": SELECTION_RULES,
        }),
        ("02-executable-context-summary.json", {
            "schema": SCHEMA,
            "flows": [{"id": f["id"], "steps": len(f["steps"]), "evidence": f["evidence"]} for f in ASSEMBLY_FLOWS],
            "rules": ASSEMBLY_RULES,
        }),
        ("03-retrieval-validation-summary.json", {
            "schema": SCHEMA,
            "predicates": RETRIEVAL_PREDICATES,
            "by_kind": sorted({p["kind"] for p in RETRIEVAL_PREDICATES}),
            "rules": RETRIEVAL_VALIDATION_RULES,
        }),
        ("04-guidance-execution-summary.json", {
            "schema": SCHEMA,
            "surfaces": GUIDANCE_SURFACES,
            "in_scope_for_proof": [s["id"] for s in GUIDANCE_SURFACES if s["in_scope_for_proof"]],
            "rules": GUIDANCE_RULES,
        }),
        ("05-human-supervision-summary.json", {
            "schema": SCHEMA,
            "review_checkpoints": REVIEW_CHECKPOINTS,
            "escalation_intervention": ESCALATION_INTERVENTION,
            "uncertainty_surfacing": UNCERTAINTY_SURFACING,
            "operator_override": OPERATOR_OVERRIDE,
            "cognition_supervision": COGNITION_SUPERVISION,
            "unsafe_runtime_interruption": UNSAFE_RUNTIME_INTERRUPTION,
        }),
        ("06-safety-validation-summary.json", {
            "schema": SCHEMA,
            "predicates": SAFETY_PREDICATES,
            "rules": SAFETY_VALIDATION_RULES,
        }),
        ("07-proof-governance-summary.json", {
            "schema": SCHEMA,
            "philosophy": len(PROOF_PHILOSOPHY),
            "executable_cognition": len(EXECUTABLE_COGNITION_DOCTRINE),
            "supervised_realization": len(SUPERVISED_REALIZATION_PHILOSOPHY),
            "runtime_validation": len(RUNTIME_VALIDATION_DOCTRINE),
            "methodology": len(PROOF_METHODOLOGY),
            "validation_principles": len(VALIDATION_PRINCIPLES),
        }),
        ("08-realization-roadmap-summary.json", {
            "schema": SCHEMA,
            "transitions": ROADMAP_TRANSITIONS,
            "rules": ROADMAP_RULES,
        }),
        ("09-unresolved-operational-proof-risks.json", {
            "schema": SCHEMA,
            "risks": PROOF_RISKS,
            "total": len(PROOF_RISKS),
            "high": [r["id"] for r in PROOF_RISKS if r["severity"] == "high"],
            "medium": [r["id"] for r in PROOF_RISKS if r["severity"] == "medium"],
        }),
        ("10-first-runtime-proof-assessment.json", {
            "schema": SCHEMA,
            **first_proof,
        }),
    ]

    for name, payload in reports:
        (REPORTS_ROOT / name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    file_count = sum(1 for _ in CONST_ROOT.rglob("*") if _.is_file())
    high_proof_risks = [r["id"] for r in PROOF_RISKS if r["severity"] == "high"]

    print(
        "Operational proof-of-value modeling complete.\n"
        f"  Constitutional root: {CONST_ROOT}\n"
        f"  Reports: {REPORTS_ROOT}/01..10\n"
        f"  Slice candidates: {len(SLICE_CANDIDATES)} | Assembly flows: {len(ASSEMBLY_FLOWS)} | "
        f"Retrieval predicates: {len(RETRIEVAL_PREDICATES)} | Guidance surfaces: {len(GUIDANCE_SURFACES)} | "
        f"Safety predicates: {len(SAFETY_PREDICATES)} | Roadmap transitions: {len(ROADMAP_TRANSITIONS)} | "
        f"Proof risks: {len(PROOF_RISKS)} (high: {len(high_proof_risks)}).\n"
        f"  Top-ranked proof slice: {SLICE_RANKING[0]['id']} (score: {SLICE_RANKING[0]['weighted_score']}, eligible: {SLICE_RANKING[0]['proof_eligible']}).\n"
        f"  First runtime proof: {first_proof['primary_first_runtime_proof']['id'] if first_proof['primary_first_runtime_proof'] else 'none'}.\n"
        f"  Files written under constitutional root: {file_count}"
    )


if __name__ == "__main__":
    build()
