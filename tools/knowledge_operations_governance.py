"""
Phase 29 — KNOWLEDGE OPERATIONS & REVIEW TOOLING.

Constitutional layer 23. Modeling-only. Subordinate to knowledge-core and
to all twenty-two prior governance layers.

Writes:
  - the seven operations artifact folders under
    `wp-content/themes/beslock-custom/User manuals/knowledge-operations/`
  - the doctrine root at
    `wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/KNOWLEDGE_OPERATIONS_GOVERNANCE/`
  - the ten final reports under
    `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/knowledge-operations/01..10`

Idempotent. Non-destructive. Reads no per-product knowledge-core JSON.
No frontends, no autonomous review, no production deployment.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
OPS_ROOT = THEME_ROOT / "knowledge-operations"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "KNOWLEDGE_OPERATIONS_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "knowledge-operations"

SCHEMA = "knowledge-operations-governance/1.0"


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
    "RUNTIME_HARDENING", "KNOWLEDGE_LIFECYCLE",
]


# =============================================================================
# TASK 1 — OPS MODEL
# =============================================================================

OPS_DOMAINS = [
    {"id": "corpus-maintenance",   "responsibility": "keep per-product knowledge-core healthy: stale review, supersession, retention"},
    {"id": "review-operations",    "responsibility": "operate the review queues; assign, track, audit"},
    {"id": "promotion-operations", "responsibility": "execute promotion/demotion events through declared lifecycle gates"},
    {"id": "oem-ingestion",        "responsibility": "intake OEM artifacts, stage OCR, attach bindings"},
    {"id": "runtime-maintenance",  "responsibility": "monitor runtime channels, replay drift, escalation rate"},
    {"id": "governance-maintenance","responsibility": "maintain reviewer registry, scope, revocation, audit-trail integrity"},
]

OPS_ROLES = [
    {"role": "reviewer",            "scope": "per-domain, per-product approval"},
    {"role": "oem-reviewer",        "scope": "binding artifact verification"},
    {"role": "operator",            "scope": "supervised runtime execution"},
    {"role": "governance-operator", "scope": "registry, scope, revocation, emergency demotion"},
    {"role": "auditor",             "scope": "read-only audit trail inspection"},
]

OPS_INVARIANTS = [
    "every operation produces an append-only event",
    "no operation mutates canonical knowledge-core JSON in-place",
    "no operation may bypass declared lifecycle gates",
    "no operation may run autonomously without an actor identity",
    "every operation references a supervision-receipt",
]


# =============================================================================
# TASK 2 — REVIEW QUEUES
# =============================================================================

REVIEW_QUEUES = [
    {"id": "candidate-review",            "source": "any node at state=candidate",                "sla_tier": "standard", "blocking_runtime": False},
    {"id": "ocr-review",                  "source": "ocr-derived nodes pending reviewer-confirm", "sla_tier": "standard", "blocking_runtime": False},
    {"id": "warning-review",              "source": "warnings/* pending promotion or stale",      "sla_tier": "elevated", "blocking_runtime": False},
    {"id": "troubleshooting-review",      "source": "troubleshooting/* pending promotion",        "sla_tier": "standard", "blocking_runtime": False},
    {"id": "irreversible-operation-review","source": "nodes tagged irreversible-operation",       "sla_tier": "critical", "blocking_runtime": True},
    {"id": "stale-knowledge-review",      "source": "nodes flagged by stale detector",            "sla_tier": "standard", "blocking_runtime": False},
    {"id": "disputed-knowledge-review",   "source": "nodes at state=disputed",                    "sla_tier": "critical", "blocking_runtime": True},
]

QUEUE_DISCIPLINE = [
    "queues are append-only logs; consumed items are marked, not deleted",
    "items carry priority = (sla_tier, age, blocking_runtime)",
    "ownership is explicit: every claim is logged with reviewer_id + timestamp",
    "no auto-claim; reviewers must explicitly take ownership",
    "expired claims are released back to the queue with a release event",
    "queue back-pressure (length, age) feeds the health-monitoring dashboard",
]


# =============================================================================
# TASK 3 — REVIEWER WORKBENCH
# =============================================================================

WORKBENCH_PANELS = [
    {"panel": "side-by-side-oem",      "purpose": "show candidate node next to its bound OEM source artifact"},
    {"panel": "ocr-fragment-inspector","purpose": "render OCR fragment + bbox + ocr_confidence + source page"},
    {"panel": "provenance-inspector",  "purpose": "show full provenance manifest chain + sha256 verification status"},
    {"panel": "promotion-approval",    "purpose": "execute declared transition with rationale + supervision-receipt"},
    {"panel": "confidence-adjustment", "purpose": "demote/hold confidence within declared tier ceiling; never raise unilaterally"},
    {"panel": "evidence-attachment",   "purpose": "attach a new binding record (sha256-pinned) to a node"},
    {"panel": "rollback-operations",   "purpose": "issue a demotion-event referencing a prior promotion-event"},
]

WORKBENCH_INVARIANTS = [
    "the workbench is a thin operator surface, not an application: it emits events into the governed log",
    "the workbench cannot edit canonical knowledge-core JSON; it only emits append-only events",
    "the workbench cannot perform any action without a supervision-receipt",
    "the workbench cannot promote past a reviewer's declared tier_ceiling",
    "the workbench surfaces, but does not resolve, disagreement",
]

WORKBENCH_OUT_OF_SCOPE = [
    "no consumer-facing UI",
    "no chatbot interaction",
    "no autonomous suggestion engine",
    "no embedding/ML-driven match suggestions",
]


# =============================================================================
# TASK 4 — DIFF & LINEAGE
# =============================================================================

DIFF_KINDS = [
    {"kind": "node-diff",          "compares": "two versions of a node by id; structural + semantic field-level diff"},
    {"kind": "binding-diff",       "compares": "current vs prior_binding_id chain"},
    {"kind": "trust-tier-diff",    "compares": "tier transitions over time"},
    {"kind": "lineage-walk",       "compares": "promotion/demotion event chain for a node"},
    {"kind": "evidence-walk",      "compares": "binding chain from node to OEM source artifact"},
    {"kind": "rollback-walk",      "compares": "rollback chain referencing original promotion ids"},
]

LINEAGE_VIEWS = [
    "operational-history: chronological event stream per node",
    "promotion-lineage: state transitions only",
    "evidence-lineage: binding records only",
    "rollback-lineage: demotions referencing promotions",
    "trust-evolution-visualization: tier-over-time per node (data; no rendering layer)",
]

DIFF_LINEAGE_INVARIANTS = [
    "diffs are deterministic and reproducible from append-only logs",
    "lineage is never reconstructed; it is read directly from the event store",
    "diffs do not mutate; they only report",
    "diffs respect scope (per product, per domain); cross-product diffs are forbidden",
]


# =============================================================================
# TASK 5 — GOVERNANCE OPERATOR WORKFLOWS
# =============================================================================

GOVERNANCE_WORKFLOWS = [
    {"id": "governance-escalation",        "trigger": "blocking queue item or runtime escalation-trace event", "actor": "governance-operator"},
    {"id": "unsafe-knowledge-intervention","trigger": "node demoted by safety-predicate failure",              "actor": "governance-operator"},
    {"id": "runtime-incident-review",      "trigger": "supervised run with safety demotion or replay drift",   "actor": "governance-operator + reviewer"},
    {"id": "operational-audit-review",     "trigger": "scheduled or on-demand audit of review-audit log",      "actor": "auditor"},
    {"id": "disputed-knowledge-handling",  "trigger": "node at state=disputed",                                "actor": "governance-operator + dual-review"},
    {"id": "emergency-demotion",           "trigger": "operational incident or contradiction detected",        "actor": "governance-operator"},
]

EMERGENCY_DEMOTION_RULES = [
    "emergency demotion is an append-only event with severity, scope, and rationale",
    "emergency demotion fans out via declared lineage edges only",
    "emergency demotion never deletes; it only changes future retrievals",
    "emergency demotion requires governance-operator + auditor co-signature within 24 hours",
    "emergency demotion is reviewable; reversal is a separate governed event",
]

GOVERNANCE_OPERATOR_GUARDRAILS = [
    "may not author or approve their own records",
    "may not extend their own scope or tier_ceiling",
    "all actions are co-indexed in review-audit + governance-audit logs",
    "all actions are reversible by governance review",
]


# =============================================================================
# TASK 6 — OEM INGESTION OPERATIONS
# =============================================================================

OEM_INGESTION_STAGES = [
    {"stage": "intake",            "responsibility": "receive OEM artifact (PDF/screenshot); compute sha256; reject duplicates"},
    {"stage": "ocr-staging",       "responsibility": "run declared OCR pipeline version; emit ocr-fragment records (candidate state)"},
    {"stage": "ingestion-validation","responsibility": "schema + scope check; reject malformed payloads"},
    {"stage": "duplicate-detection","responsibility": "match sha256 + content fingerprint against existing source store"},
    {"stage": "source-reconciliation","responsibility": "if a near-duplicate exists, open a reconciliation review (do not auto-merge)"},
    {"stage": "source-aging",      "responsibility": "track source age vs supersession-window; flag stale sources for re-review"},
    {"stage": "oem-replacement",   "responsibility": "supersession of an OEM source: emit supersession event; fan out demotion to bound nodes"},
]

OEM_INGESTION_INVARIANTS = [
    "no auto-binding from a new OEM source to existing nodes; binding requires reviewer action",
    "no merge of two OEM sources without a documented reconciliation review",
    "no OEM source is ever overwritten; new uploads create new source records",
    "every stage produces an append-only event",
    "ingestion respects the read-only posture over canonical knowledge-core",
]

OEM_REPLACEMENT_FLOW = [
    "1. new OEM source ingested + sha256 pinned",
    "2. supersession event proposed (old_sha256, new_sha256, rationale, reviewer)",
    "3. dual-review of supersession",
    "4. on approval: bound nodes demote to candidate-pending-rebinding",
    "5. each demoted node enters candidate-review queue",
]


# =============================================================================
# TASK 7 — HEALTH MONITORING
# =============================================================================

HEALTH_INDICATORS = [
    {"id": "corpus-health-score",          "inputs": ["mean tier_weight", "stale ratio", "candidate ratio"]},
    {"id": "stale-knowledge-detection",    "inputs": ["updated_at vs per-tier max_age", "superseded source bindings"]},
    {"id": "retrieval-degradation",        "inputs": ["share of retrieval packages with no_results", "share with candidate_only=True"]},
    {"id": "warning-coverage-gap",         "inputs": ["domains where warnings retrieval returns empty for declared canonical queries"]},
    {"id": "troubleshooting-coverage-gap", "inputs": ["domains where troubleshooting retrieval is candidate-only or empty"]},
    {"id": "runtime-reliability",          "inputs": ["replay determinism rate", "supervised-run demotion rate", "escalation-trace declared-vs-surprise ratio"]},
    {"id": "queue-back-pressure",          "inputs": ["per-queue length", "oldest-item age", "claim-expiry rate"]},
]

HEALTH_DISCIPLINE = [
    "indicators are computed from append-only logs; they are reproducible",
    "indicators are not thresholds for autonomous action; they feed governance review",
    "indicators are exposed read-only; the dashboard layer is out of scope here",
    "indicators are scoped per product and per domain; no global single-number health",
]

DEGRADATION_RESPONSE_RULES = [
    "retrieval-degradation > declared floor → open governance-escalation",
    "warning-coverage-gap detected → open warning-review queue items + escalation",
    "queue back-pressure > declared ceiling → governance-operator notified, no auto-bypass",
    "runtime-reliability drop → halt supervised promotions until reviewed",
]


# =============================================================================
# TASK 8 — DOCTRINE
# =============================================================================

CHARTER_PRINCIPLES = [
    "This layer governs how the corpus is operated and maintained by humans.",
    "All operations are append-only, supervised, and reversible.",
    "All operator actions emit a supervision-receipt and a review-audit record.",
    "No operator action may bypass declared lifecycle gates or reviewer scope.",
    "No autonomous review or auto-promotion exists at any operations surface.",
    "All tooling described here is operator-surface modeling; no consumer UI is in scope.",
    "All operations are subordinate to provenance and to all 22 prior governance layers.",
]

OPERATIONAL_MAINTENANCE_PHILOSOPHY = [
    "Maintenance is additive: events, not edits.",
    "Maintenance is observable: every change appears in the audit trail.",
    "Maintenance is bounded: only declared workflows exist.",
    "Maintenance is reversible: every action has a governed rollback path.",
]

REVIEWER_TOOLING_PHILOSOPHY = [
    "Reviewer tooling is a thin operator surface, not an application.",
    "Reviewer tooling cannot edit canonical knowledge-core JSON.",
    "Reviewer tooling cannot promote past the reviewer's tier_ceiling.",
    "Reviewer tooling surfaces evidence; it does not invent it.",
]

GOVERNANCE_OPERATOR_DOCTRINE = [
    "Governance operators steward the registry, scope, and emergency response.",
    "Governance operators may not author or approve their own records.",
    "Governance operators may not extend their own scope or tier_ceiling.",
    "Governance operator actions are append-only and dual-audited.",
]

OPERATIONAL_SUSTAINABILITY_DOCTRINE = [
    "Sustainability is the joint property of (active reviewer pool, healthy queues, fresh OEM bindings, replay-deterministic runtime).",
    "Sustainability is measured per product, per domain; no global single number.",
    "Sustainability degradation is escalated, not silently absorbed.",
    "Sustainability is bounded by the declared invariants; no autonomous workaround exists.",
]

CORPUS_MAINTENANCE_PRINCIPLES = [
    "Canonical per-product knowledge-core JSON is read-only forever to the runtime and to operators outside the lifecycle.",
    "Mutations occur only through declared events: promotion, demotion, binding, supersession, archival.",
    "Stale records are queued for re-review, not silently kept and not deleted.",
    "Coverage gaps are visible by symmetry across the 6 products.",
]

TRUST_PRESERVING_OPERATIONS_PHILOSOPHY = [
    "Operations preserve trust by preserving provenance.",
    "Operations preserve trust by preserving lineage.",
    "Operations preserve trust by preserving reviewer accountability.",
    "Operations preserve trust by preserving reversibility.",
]


# =============================================================================
# TASK 9 — FUTURE HUMAN-IN-THE-LOOP OPERATIONS
# =============================================================================

FUTURE_COMMITMENTS = [
    "reviewer ecosystems grow through the reviewer registry; revocation remains a first-class event",
    "distributed governance teams partition work by scope (domain × product); no global override",
    "operational maintenance teams operate from append-only logs; no out-of-band edits",
    "OEM update operations enter as new sources + supersession events; old sources never overwritten",
    "runtime incident operations are bounded by replay + safety-predicate logs; no silent recovery",
    "supervised operational scaling proceeds product by product, domain by domain; no fan-out shortcuts",
]

FUTURE_INVARIANTS = [
    "no autonomous review path is ever introduced",
    "no operator action ever bypasses a supervision-receipt",
    "no canonical JSON mutation ever occurs in-place",
    "no governance scope is ever silently expanded",
    "no macro-governance mega-layer is spawned by operations work",
]


# =============================================================================
# BUILD
# =============================================================================

def build():
    OPS_ROOT.mkdir(parents=True, exist_ok=True)
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    # --- Task 1 ----------------------------------------------------------
    write_pair(
        OPS_ROOT / "ops-model", "ops-model",
        "Knowledge Operations Model",
        "Operational domains, roles, and invariants that bound human knowledge operations.",
        [
            ("Operational domains", md_list([f"`{d['id']}` — {d['responsibility']}" for d in OPS_DOMAINS])),
            ("Roles", md_list([f"`{r['role']}` — {r['scope']}" for r in OPS_ROLES])),
            ("Invariants", md_list(OPS_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "ops-model",
         "domains": OPS_DOMAINS, "roles": OPS_ROLES, "invariants": OPS_INVARIANTS},
    )

    # --- Task 2 ----------------------------------------------------------
    write_pair(
        OPS_ROOT / "review-queues", "review-queues",
        "Review Queue Systems",
        "Seven append-only queues, each with declared source, SLA tier, and blocking semantics.",
        [
            ("Queues", md_list([f"`{q['id']}` — source: {q['source']}; SLA: {q['sla_tier']}; blocks runtime: {q['blocking_runtime']}" for q in REVIEW_QUEUES])),
            ("Queue discipline", md_list(QUEUE_DISCIPLINE)),
        ],
        {"schema": SCHEMA, "kind": "review-queues",
         "queues": REVIEW_QUEUES, "queue_discipline": QUEUE_DISCIPLINE},
    )

    # --- Task 3 ----------------------------------------------------------
    write_pair(
        OPS_ROOT / "reviewer-workbench", "reviewer-workbench",
        "Reviewer Workbench",
        "Thin operator surface — emits append-only events; never edits canonical JSON.",
        [
            ("Panels", md_list([f"`{p['panel']}` — {p['purpose']}" for p in WORKBENCH_PANELS])),
            ("Invariants", md_list(WORKBENCH_INVARIANTS)),
            ("Out of scope", md_list(WORKBENCH_OUT_OF_SCOPE)),
        ],
        {"schema": SCHEMA, "kind": "reviewer-workbench",
         "panels": WORKBENCH_PANELS, "invariants": WORKBENCH_INVARIANTS,
         "out_of_scope": WORKBENCH_OUT_OF_SCOPE},
    )

    # --- Task 4 ----------------------------------------------------------
    write_pair(
        OPS_ROOT / "diff-lineage", "diff-lineage",
        "Knowledge Diff & Lineage Tooling",
        "Deterministic, read-only diffs and lineage walks computed from append-only logs.",
        [
            ("Diff kinds", md_list([f"`{d['kind']}` — {d['compares']}" for d in DIFF_KINDS])),
            ("Lineage views", md_list(LINEAGE_VIEWS)),
            ("Invariants", md_list(DIFF_LINEAGE_INVARIANTS)),
        ],
        {"schema": SCHEMA, "kind": "diff-lineage",
         "diff_kinds": DIFF_KINDS, "lineage_views": LINEAGE_VIEWS,
         "invariants": DIFF_LINEAGE_INVARIANTS},
    )

    # --- Task 5 ----------------------------------------------------------
    write_pair(
        OPS_ROOT / "governance-workflows", "governance-workflows",
        "Governance Operator Workflows",
        "Six declared workflows for escalation, intervention, audit, dispute, and emergency demotion.",
        [
            ("Workflows", md_list([f"`{w['id']}` — trigger: {w['trigger']}; actor: {w['actor']}" for w in GOVERNANCE_WORKFLOWS])),
            ("Emergency demotion rules", md_list(EMERGENCY_DEMOTION_RULES)),
            ("Governance operator guardrails", md_list(GOVERNANCE_OPERATOR_GUARDRAILS)),
        ],
        {"schema": SCHEMA, "kind": "governance-workflows",
         "workflows": GOVERNANCE_WORKFLOWS,
         "emergency_demotion_rules": EMERGENCY_DEMOTION_RULES,
         "governance_operator_guardrails": GOVERNANCE_OPERATOR_GUARDRAILS},
    )

    # --- Task 6 ----------------------------------------------------------
    write_pair(
        OPS_ROOT / "oem-operations", "oem-operations",
        "OEM Ingestion Operations",
        "Seven-stage governed flow for OEM artifact intake, OCR staging, reconciliation, and supersession.",
        [
            ("Stages", md_list([f"`{s['stage']}` — {s['responsibility']}" for s in OEM_INGESTION_STAGES])),
            ("Invariants", md_list(OEM_INGESTION_INVARIANTS)),
            ("OEM replacement flow", md_list(OEM_REPLACEMENT_FLOW)),
        ],
        {"schema": SCHEMA, "kind": "oem-operations",
         "stages": OEM_INGESTION_STAGES,
         "invariants": OEM_INGESTION_INVARIANTS,
         "oem_replacement_flow": OEM_REPLACEMENT_FLOW},
    )

    # --- Task 7 ----------------------------------------------------------
    write_pair(
        OPS_ROOT / "health-monitoring", "health-monitoring",
        "Knowledge Health & Maintenance",
        "Deterministic, append-only-log-derived indicators; never used for autonomous action.",
        [
            ("Health indicators", md_list([f"`{h['id']}` — inputs: " + ", ".join(h['inputs']) for h in HEALTH_INDICATORS])),
            ("Health discipline", md_list(HEALTH_DISCIPLINE)),
            ("Degradation response rules", md_list(DEGRADATION_RESPONSE_RULES)),
        ],
        {"schema": SCHEMA, "kind": "health-monitoring",
         "health_indicators": HEALTH_INDICATORS,
         "health_discipline": HEALTH_DISCIPLINE,
         "degradation_response_rules": DEGRADATION_RESPONSE_RULES},
    )

    # --- Task 8 — doctrine root ------------------------------------------
    (CONST_ROOT / "README.md").write_text(
        "# KNOWLEDGE OPERATIONS GOVERNANCE\n\n"
        "Twenty-third constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all twenty-two prior governance layers.\n\n"
        "Governs how the corpus is operated, reviewed, and maintained by humans, while "
        "preserving provenance, supervision, reversibility, and accountability.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Knowledge Operations Governance",
        "Declares principles + authority for human operations over the governed corpus.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Bound artifacts", md_list([
                "`wp-content/themes/beslock-custom/User manuals/knowledge-operations/ops-model/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-operations/review-queues/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-operations/reviewer-workbench/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-operations/diff-lineage/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-operations/governance-workflows/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-operations/oem-operations/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-operations/health-monitoring/`",
            ])),
            ("Hard Exclusions", md_list([
                "DO NOT build production UI",
                "DO NOT build frontend applications",
                "DO NOT implement autonomous review",
                "DO NOT bypass human governance",
                "DO NOT expand macro-cognition recursively",
                "DO NOT deploy production systems",
            ])),
        ],
        {"schema": SCHEMA, "kind": "charter",
         "principles": CHARTER_PRINCIPLES,
         "subordinate_to": SUBORDINATE_TO,
         "generated": now_iso()},
    )

    for slug, title, intro, principles in [
        ("operational-maintenance-philosophy", "Operational Maintenance Philosophy",
         "Maintenance is additive, observable, bounded, reversible.", OPERATIONAL_MAINTENANCE_PHILOSOPHY),
        ("reviewer-tooling-philosophy", "Reviewer Tooling Philosophy",
         "Reviewer tooling is a thin operator surface, not an application.", REVIEWER_TOOLING_PHILOSOPHY),
        ("governance-operator-doctrine", "Governance Operator Doctrine",
         "Governance operators steward registry, scope, and emergency response under dual-audit.",
         GOVERNANCE_OPERATOR_DOCTRINE),
        ("operational-sustainability-doctrine", "Operational Sustainability Doctrine",
         "Sustainability = active reviewer pool × healthy queues × fresh OEM bindings × replay-deterministic runtime.",
         OPERATIONAL_SUSTAINABILITY_DOCTRINE),
        ("corpus-maintenance-principles", "Corpus Maintenance Principles",
         "Canonical knowledge-core is read-only; mutations occur only through declared events.",
         CORPUS_MAINTENANCE_PRINCIPLES),
        ("trust-preserving-operations-philosophy", "Trust-Preserving Operations Philosophy",
         "Operations preserve trust by preserving provenance, lineage, accountability, and reversibility.",
         TRUST_PRESERVING_OPERATIONS_PHILOSOPHY),
    ]:
        write_pair(
            CONST_ROOT / slug, slug, title, intro,
            [("Principles", md_list(principles))],
            {"schema": SCHEMA, "kind": slug, "principles": principles},
        )

    # --- Final 10 reports ------------------------------------------------
    reports = [
        ("01-ops-model-summary.json", {
            "schema": SCHEMA, "kind": "ops-model-summary",
            "domains": [d["id"] for d in OPS_DOMAINS],
            "roles": [r["role"] for r in OPS_ROLES],
            "invariants_count": len(OPS_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-operations/ops-model/",
        }),
        ("02-review-queue-summary.json", {
            "schema": SCHEMA, "kind": "review-queue-summary",
            "queues": [q["id"] for q in REVIEW_QUEUES],
            "blocking_runtime_queues": [q["id"] for q in REVIEW_QUEUES if q["blocking_runtime"]],
            "discipline_rules_count": len(QUEUE_DISCIPLINE),
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-operations/review-queues/",
        }),
        ("03-reviewer-workbench-summary.json", {
            "schema": SCHEMA, "kind": "reviewer-workbench-summary",
            "panels": [p["panel"] for p in WORKBENCH_PANELS],
            "invariants_count": len(WORKBENCH_INVARIANTS),
            "out_of_scope": WORKBENCH_OUT_OF_SCOPE,
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-operations/reviewer-workbench/",
        }),
        ("04-diff-lineage-summary.json", {
            "schema": SCHEMA, "kind": "diff-lineage-summary",
            "diff_kinds": [d["kind"] for d in DIFF_KINDS],
            "lineage_views_count": len(LINEAGE_VIEWS),
            "invariants_count": len(DIFF_LINEAGE_INVARIANTS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-operations/diff-lineage/",
        }),
        ("05-governance-workflow-summary.json", {
            "schema": SCHEMA, "kind": "governance-workflow-summary",
            "workflows": [w["id"] for w in GOVERNANCE_WORKFLOWS],
            "emergency_demotion_rules_count": len(EMERGENCY_DEMOTION_RULES),
            "guardrails_count": len(GOVERNANCE_OPERATOR_GUARDRAILS),
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-operations/governance-workflows/",
        }),
        ("06-oem-operations-summary.json", {
            "schema": SCHEMA, "kind": "oem-operations-summary",
            "stages": [s["stage"] for s in OEM_INGESTION_STAGES],
            "invariants_count": len(OEM_INGESTION_INVARIANTS),
            "replacement_flow_steps": len(OEM_REPLACEMENT_FLOW),
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-operations/oem-operations/",
        }),
        ("07-health-monitoring-summary.json", {
            "schema": SCHEMA, "kind": "health-monitoring-summary",
            "indicators": [h["id"] for h in HEALTH_INDICATORS],
            "discipline_rules_count": len(HEALTH_DISCIPLINE),
            "degradation_response_rules_count": len(DEGRADATION_RESPONSE_RULES),
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-operations/health-monitoring/",
        }),
        ("08-operations-governance-summary.json", {
            "schema": SCHEMA, "kind": "operations-governance-summary",
            "layer_index": 23,
            "subordinate_to_count": len(SUBORDINATE_TO),
            "constitutional_root": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/KNOWLEDGE_OPERATIONS_GOVERNANCE/",
            "reports_root": "wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/knowledge-operations/",
            "doctrine_sections": [
                "operational-maintenance-philosophy",
                "reviewer-tooling-philosophy",
                "governance-operator-doctrine",
                "operational-sustainability-doctrine",
                "corpus-maintenance-principles",
                "trust-preserving-operations-philosophy",
            ],
        }),
        ("09-unresolved-operational-maintenance-risks.json", {
            "schema": SCHEMA, "kind": "unresolved-operational-maintenance-risks",
            "items": [
                {"id": "no-executable-queue-store",        "severity": "high",   "impact": "review queues are modeled but not yet implemented as a real append-only store"},
                {"id": "no-executable-workbench",          "severity": "high",   "impact": "reviewer workbench panels are modeled; no operator surface exists yet"},
                {"id": "no-executable-event-log",          "severity": "high",   "impact": "promotion/demotion/binding events have a schema but no real store"},
                {"id": "no-reviewer-registry-impl",        "severity": "high",   "impact": "carry-over from Phase 28 — still unresolved"},
                {"id": "no-oem-binding-store-impl",        "severity": "high",   "impact": "carry-over from Phase 28 — still unresolved"},
                {"id": "no-health-indicator-computer",     "severity": "medium", "impact": "indicator definitions exist; no scheduled computer wired"},
                {"id": "no-emergency-demotion-cli",        "severity": "medium", "impact": "emergency demotion rules declared; no operator entry point"},
                {"id": "no-claim-expiry-scheduler",        "severity": "medium", "impact": "claim release semantics declared; no scheduler"},
                {"id": "no-source-aging-scheduler",        "severity": "medium", "impact": "source-aging stage declared; no schedule"},
                {"id": "candidate-records-still-await-elevation", "severity": "high", "impact": "carry-over: 132 Phase-27 candidates remain unreviewed"},
            ],
        }),
        ("10-long-term-sustainability-reassessment.json", {
            "schema": SCHEMA, "kind": "long-term-sustainability-reassessment",
            "platform_status": "FOUNDATIONALLY COMPLETE (unchanged)",
            "operations_governance_status": "MODELED (executable enforcement pending)",
            "primary_bottleneck": "HUMAN OPERATIONAL MAINTAINABILITY (now governed by declared model)",
            "next_bottleneck": "executable enforcement of the operations model (queue store, event log, reviewer registry, workbench, schedulers)",
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

    print(f"Knowledge Operations Governance (layer 23) written to:\n  {OPS_ROOT}\n  {CONST_ROOT}\n  {REPORTS_ROOT}")


if __name__ == "__main__":
    build()
