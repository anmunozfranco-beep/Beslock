"""
Phase 28 — KNOWLEDGE LIFECYCLE & TRUST GOVERNANCE.

Constitutional layer 22. Modeling-only. Subordinate to knowledge-core and
to all twenty-one prior governance layers.

Writes:
  - the seven lifecycle artifact folders under
    `wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/`
  - the doctrine root at
    `wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/KNOWLEDGE_LIFECYCLE_GOVERNANCE/`
  - the ten final reports under
    `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/knowledge-lifecycle/01..10`

Idempotent. Non-destructive. Reads no per-product knowledge-core JSON.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
LIFECYCLE_ROOT = THEME_ROOT / "knowledge-lifecycle"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "KNOWLEDGE_LIFECYCLE_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "knowledge-lifecycle"

SCHEMA = "knowledge-lifecycle-governance/1.0"


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
    "RUNTIME_HARDENING",
]


# =============================================================================
# TASK 1 — LIFECYCLE MODEL
# =============================================================================

LIFECYCLE_STATES = [
    {"id": "candidate",              "description": "declared but unverified; lowest trust",        "default_for": ["supplemental builders"], "blocking_for_runtime": False},
    {"id": "ocr-derived",            "description": "extracted from OEM source via OCR; not yet reviewer-confirmed", "default_for": ["manual_ocr pipeline"], "blocking_for_runtime": False},
    {"id": "inferred",               "description": "derived from declared neighbours by governed inference",       "default_for": ["causal-graphs traversal"], "blocking_for_runtime": False},
    {"id": "reviewer-confirmed",     "description": "human reviewer signed off after evidence attachment",          "default_for": [], "blocking_for_runtime": False},
    {"id": "oem-verified",           "description": "bound to a verified OEM source artifact (PDF/screenshot/firmware doc)", "default_for": [], "blocking_for_runtime": False},
    {"id": "operationally-proven",   "description": "deployed in supervised runtime flows for N successful supervised runs without incident", "default_for": [], "blocking_for_runtime": False},
    {"id": "disputed",               "description": "two or more declared sources contradict; runtime must escalate", "default_for": [], "blocking_for_runtime": True},
    {"id": "deprecated",             "description": "superseded by a newer record but preserved for lineage",         "default_for": [], "blocking_for_runtime": True},
    {"id": "archived",               "description": "removed from active retrieval; lineage preserved read-only",     "default_for": [], "blocking_for_runtime": True},
]

LIFECYCLE_TRANSITIONS = [
    {"from": "candidate",          "to": "ocr-derived",          "gate": "ocr-evidence-attached",            "actor": "ocr-pipeline+reviewer", "reversible": True},
    {"from": "candidate",          "to": "inferred",             "gate": "inference-evidence-attached",      "actor": "reasoning-layer+reviewer", "reversible": True},
    {"from": "ocr-derived",        "to": "reviewer-confirmed",   "gate": "single-reviewer-approval",         "actor": "reviewer",          "reversible": True},
    {"from": "inferred",           "to": "reviewer-confirmed",   "gate": "single-reviewer-approval",         "actor": "reviewer",          "reversible": True},
    {"from": "reviewer-confirmed", "to": "oem-verified",         "gate": "oem-binding-attached + dual-review", "actor": "reviewer x2",     "reversible": True},
    {"from": "oem-verified",       "to": "operationally-proven", "gate": "N supervised runs without incident + signoff", "actor": "operator+reviewer", "reversible": True},
    {"from": "*",                  "to": "disputed",             "gate": "contradiction-detected",           "actor": "runtime+reviewer",  "reversible": True},
    {"from": "*",                  "to": "deprecated",           "gate": "supersession-record-attached",     "actor": "reviewer",          "reversible": True},
    {"from": "deprecated",         "to": "archived",             "gate": "retention-period-elapsed",         "actor": "governance",        "reversible": False, "note": "lineage preserved read-only"},
    {"from": "*",                  "to": "candidate",            "gate": "evidence-invalidated (demotion)",  "actor": "reviewer",          "reversible": True},
]

PROMOTION_GATES = [
    {"gate": "ocr-evidence-attached",       "requires": ["source_refs[*].kind in {pdf, ocr-fragment, screenshot}", "sha256 binding", "page/region"]},
    {"gate": "inference-evidence-attached", "requires": ["inference_lineage with source node ids", "inference rule id", "confidence floor"]},
    {"gate": "single-reviewer-approval",    "requires": ["reviewer identity", "supervision receipt", "evidence checksum match"]},
    {"gate": "dual-review",                 "requires": ["two distinct reviewers", "no shared review session", "no escalation override"]},
    {"gate": "oem-binding-attached",        "requires": ["oem_binding record present", "oem source artifact pinned by sha256"]},
    {"gate": "N supervised runs without incident", "requires": ["replay-deterministic", "no safety-demote", "no escalation"], "default_N": 5},
    {"gate": "contradiction-detected",      "requires": ["two oem-verified or reviewer-confirmed records disagree on a binding field"]},
    {"gate": "supersession-record-attached","requires": ["successor node id", "rationale", "reviewer"]},
    {"gate": "retention-period-elapsed",    "requires": ["age >= retention_days", "no active lineage references"]},
    {"gate": "evidence-invalidated",        "requires": ["invalidation rationale", "reviewer", "demotion target tier"]},
]

ARCHIVAL_RULES = [
    "archival never deletes the node — it moves it out of active retrieval domains",
    "archived nodes remain readable for lineage queries only",
    "archival is reversible only by governance review (re-promotion to candidate)",
    "archival of an OEM-verified record requires a supersession record",
]


# =============================================================================
# TASK 2 — REVIEW WORKFLOWS
# =============================================================================

REVIEWER_ASSIGNMENT = [
    "reviewers are declared in a reviewer registry (identity + signoff scope)",
    "assignment is by domain (operation, warnings, troubleshooting, install, ...) and product",
    "no reviewer may approve their own authored record",
    "OEM-binding reviews require an OEM-scope reviewer",
]

WORKFLOW_STEPS = [
    {"step": "intake",         "responsibility": "validate candidate schema + scope",         "actor": "automation"},
    {"step": "triage",         "responsibility": "assign reviewer(s) by domain+product",      "actor": "governance"},
    {"step": "evidence-pull",  "responsibility": "attach OEM source artifacts + checksums",   "actor": "reviewer"},
    {"step": "single-review",  "responsibility": "first-pass approve/reject + rationale",     "actor": "reviewer-1"},
    {"step": "dual-review",    "responsibility": "second-pass (required for OEM promotion)",  "actor": "reviewer-2"},
    {"step": "consensus",      "responsibility": "resolve disagreement via documented merge", "actor": "governance"},
    {"step": "signoff",        "responsibility": "emit supervision receipt + state transition","actor": "governance"},
    {"step": "post-audit",     "responsibility": "append append-only review record",          "actor": "automation"},
]

CONSENSUS_RULES = [
    "approve/approve → promote",
    "approve/reject  → escalate to consensus reviewer",
    "reject/reject   → demote to candidate + rationale",
    "any reviewer flags irreversible-operation → force escalation review",
    "no silent overrides; every override is a logged decision",
]

IRREVERSIBLE_OPERATION_REVIEW = [
    "records touching irreversible operations (factory reset, admin wipe, firmware) require:",
    "  - dual-review",
    "  - operator co-signature",
    "  - explicit reversibility statement (or declared irreversibility)",
    "  - mandatory escalation policy on the record",
]


# =============================================================================
# TASK 3 — OEM EVIDENCE BINDING
# =============================================================================

BINDING_KINDS = [
    {"kind": "pdf",                "fields": ["sha256", "path_or_url", "page", "region_bbox", "extract_lineage"]},
    {"kind": "ocr-fragment",       "fields": ["sha256", "source_pdf_sha256", "page", "region_bbox", "ocr_tool", "ocr_confidence"]},
    {"kind": "screenshot",         "fields": ["sha256", "captured_from", "captured_at", "annotator", "region_bbox"]},
    {"kind": "extracted-procedure","fields": ["sha256", "source_pdf_sha256", "page_range", "extract_lineage"]},
    {"kind": "troubleshooting-evidence", "fields": ["sha256", "source_kind", "source_ref", "observed_failure_mode"]},
    {"kind": "warning-evidence",   "fields": ["sha256", "source_kind", "source_ref", "irreversibility_flag"]},
]

BINDING_RULES = [
    "every binding record is content-addressed (sha256 of the source artifact)",
    "every binding record is append-only; updates create a new binding with prior_binding_id",
    "no binding may reference a non-existent or non-pinned source",
    "OEM-verified state requires at least one binding of kind pdf | ocr-fragment | extracted-procedure",
    "warning-evidence + troubleshooting-evidence bindings are required for those domains' OEM promotion",
    "runtime exposes binding ids via the provenance manifest; the runtime never edits bindings",
]

TRACEABLE_TRUST_PIPELINE = [
    "node -> oem_binding[] -> source artifact (sha256-pinned) -> declared origin",
    "any break in the chain demotes the node to candidate and emits escalation",
    "traceability is queryable; queries are read-only and bounded by knowledge-core scope",
]


# =============================================================================
# TASK 4 — TRUST MODEL
# =============================================================================

TRUST_TIERS = [
    {"tier": "candidate",            "weight": 0.40, "human_reviewed": False, "oem_bound": False, "runtime_use": "soft-escalation"},
    {"tier": "low-confidence",       "weight": 0.50, "human_reviewed": False, "oem_bound": False, "runtime_use": "supervised-only"},
    {"tier": "ocr-derived",          "weight": 0.85, "human_reviewed": False, "oem_bound": "partial", "runtime_use": "supervised"},
    {"tier": "inferred",             "weight": 0.65, "human_reviewed": False, "oem_bound": False, "runtime_use": "supervised + traversal evidence"},
    {"tier": "reviewer-confirmed",   "weight": 0.92, "human_reviewed": True,  "oem_bound": "partial", "runtime_use": "supervised"},
    {"tier": "oem-verified",         "weight": 1.00, "human_reviewed": True,  "oem_bound": True,  "runtime_use": "supervised primary"},
    {"tier": "operationally-proven", "weight": 1.00, "human_reviewed": True,  "oem_bound": True,  "runtime_use": "supervised primary + replay-validated"},
]

TRUST_TRANSITIONS = [
    "trust raises only through declared promotion gates",
    "trust may decay (see decay rules) but never silently",
    "trust inheritance: a derived node inherits the floor of its source tiers, not the ceiling",
    "dispute propagation: a disputed source caps all derived nodes at `low-confidence` until resolved",
]

TRUST_DECAY_RULES = [
    "OEM source supersession → all bound nodes demote to candidate pending re-review",
    "stale OCR pipeline version (older than declared floor) → demote to candidate",
    "reviewer revocation → records that reviewer signed alone revert to ocr-derived/inferred",
    "operational-incident on a node in supervised use → demote one tier + open dispute",
    "retention-period elapsed without re-validation → demote to candidate",
]

STALE_KNOWLEDGE_DETECTION = [
    "stale = `updated_at` older than the per-tier max_age",
    "stale = bound to a source artifact that has been superseded",
    "stale = bound to a reviewer whose signoff scope has changed",
    "detected stale records are queued for re-review, not silently kept",
]


# =============================================================================
# TASK 5 — REVERSIBILITY
# =============================================================================

REVERSIBLE_PROMOTION_RULES = [
    "every promotion is recorded as an append-only `promotion-event` with prior_state, new_state, rationale, reviewer(s), and binding ids",
    "every promotion is reversible by an equal-or-higher governance decision",
    "rollback emits a `demotion-event` referencing the original promotion-event id",
    "rollback never deletes the promotion-event; both events coexist in lineage",
]

INVALIDATION_PROPAGATION = [
    "invalidation of a source → fan out to all bound nodes (BFS over oem_binding edges)",
    "invalidation of an inference rule → fan out to all inferred nodes that cited it",
    "fan-out is bounded by the declared lineage edges only; no inferred fan-out",
    "each fanned-out demotion is its own append-only event",
]

RUNTIME_SAFE_DEMOTION = [
    "demotion never mutates retrieval-trace history; it only changes future retrievals",
    "demotion of a node currently inside a live supervised slice halts the slice",
    "demotion never silently lowers a slice's confidence after emission",
    "demotion of a record bound to an active continuity-checkpoint forces re-checkpoint",
]

DEPRECATED_NODE_HANDLING = [
    "deprecated nodes remain readable; retrieval ranks them at weight 0",
    "deprecated nodes carry `superseded_by` pointer(s)",
    "deprecated nodes are excluded from `oem-verified` and `operationally-proven` rollups",
    "deprecated nodes are not eligible for re-promotion without an explicit governance decision",
]

HISTORICAL_LINEAGE_PRESERVATION = [
    "every node carries an append-only `lineage` array of state transitions",
    "lineage entries are content-addressed and signed by the actor",
    "archival preserves lineage in a separate read-only domain",
    "lineage is never overwritten; it is only appended",
]


# =============================================================================
# TASK 6 — REVIEWER ACCOUNTABILITY
# =============================================================================

REVIEWER_IDENTITY_FIELDS = [
    "reviewer_id (stable, governance-issued)",
    "scope[] (domains + products the reviewer may approve)",
    "tier_ceiling (max tier this reviewer may approve unilaterally)",
    "active_since / revoked_at",
    "signoff_key_fingerprint (for receipt signing — declared, not implemented as crypto here)",
]

APPROVAL_PROVENANCE_FIELDS = [
    "approval_id", "node_id", "prior_state", "new_state",
    "reviewer_id", "co_reviewer_id (nullable)",
    "evidence_binding_ids[]", "rationale",
    "supervision_receipt_id", "timestamp_iso",
]

REVIEW_AUDIT_TRAIL_RULES = [
    "every approval emits an append-only `review-audit/1.0` record",
    "audit records are co-indexed by node_id and reviewer_id",
    "audit records are immutable; corrections are new records that supersede the prior id",
    "audit records carry the supervision-receipt id so runtime + governance share a single proof chain",
]

DISAGREEMENT_HANDLING = [
    "disagreement is recorded as a `disagreement-event` with both rationales",
    "disagreement does not silently resolve — it routes to consensus or escalation review",
    "an unresolved disagreement caps the node at its prior tier",
    "repeated disagreement on the same node opens a `disputed` state",
]

CRITICAL_OPERATION_SIGNOFF = [
    "irreversible-operation records require:",
    "  - dual-review (two distinct reviewer_ids, distinct sessions)",
    "  - operator co-signature (operator_id + supervision-receipt)",
    "  - explicit escalation_policy on the node",
    "  - explicit reversibility statement (or declared irreversibility)",
]


# =============================================================================
# TASK 7 — CORPUS MATURITY
# =============================================================================

MATURITY_DIMENSIONS = [
    {"id": "operational-readiness",  "rolls_up_from": ["operation", "workflows", "procedural-semantics", "install"]},
    {"id": "troubleshooting-maturity", "rolls_up_from": ["troubleshooting", "troubleshooting-expanded", "causal-graphs"]},
    {"id": "warning-maturity",       "rolls_up_from": ["warnings", "warnings-expanded"]},
    {"id": "continuity-maturity",    "rolls_up_from": ["continuity-checkpoints"]},
    {"id": "retrieval-readiness",    "rolls_up_from": ["all domains with at least one ocr-derived-or-higher record"]},
    {"id": "runtime-trustworthiness","rolls_up_from": ["operationally-proven node count + replay determinism rate"]},
]

MATURITY_SCORE_FORMULA = [
    "per-domain coverage_score = #(ocr-derived-or-higher) / #(declared)",
    "per-domain trust_score    = mean(tier_weight) over declared records",
    "per-product maturity      = weighted mean of dimension scores",
    "weights are declared, not learned; declared per phase",
    "scores are reproducible: same inputs → same outputs (no clock, no random)",
]

MATURITY_TIERS = [
    {"tier": "nascent",     "range": "< 0.30", "runtime_use": "supervised pilot only"},
    {"tier": "emerging",    "range": "0.30-0.60", "runtime_use": "supervised + mandatory escalation routes"},
    {"tier": "operational", "range": "0.60-0.85", "runtime_use": "supervised primary"},
    {"tier": "mature",      "range": ">= 0.85", "runtime_use": "supervised + replay-validated primary"},
]

RUNTIME_TRUSTWORTHINESS_INPUTS = [
    "share of retrieval packages whose top-K avg weight >= 0.85",
    "share of supervised runs that complete without demotion",
    "replay determinism rate over the last K runs",
    "share of escalation-trace events that were declared (not surprise)",
]


# =============================================================================
# TASK 8 — DOCTRINE
# =============================================================================

CHARTER_PRINCIPLES = [
    "This layer governs how candidate operational knowledge becomes trusted operational knowledge.",
    "Knowledge evolution is reversible, append-only, and human-supervised by default.",
    "No knowledge is auto-promoted; every promotion crosses a declared gate with a declared reviewer.",
    "Every promotion is reversible; rollback is recorded, never silent.",
    "OEM verification is the highest tier achievable without operational evidence.",
    "Operationally-proven status requires both OEM verification and replay-validated supervised runs.",
    "Disputes do not silently resolve; they cap derived trust until reviewed.",
    "All knowledge evolution is subordinate to provenance and to all 21 prior governance layers.",
]

TRUST_PHILOSOPHY = [
    "Trust is earned through declared gates, not inferred from usage.",
    "Trust is reversible; reversibility is a feature, not a defect.",
    "Trust is inherited at the floor of its sources, never the ceiling.",
    "Trust decays when its evidence decays.",
]

OPERATIONAL_KNOWLEDGE_EVOLUTION_DOCTRINE = [
    "Evolution is additive: new records, new bindings, new events — never silent mutation.",
    "Evolution is auditable: every change is a content-addressed append-only event.",
    "Evolution is bounded: only declared transitions exist; no ad-hoc promotion paths.",
    "Evolution is symmetric across products: the same gates apply to all 6 products.",
]

REVIEWER_GOVERNANCE_PHILOSOPHY = [
    "Reviewers are identified, scoped, and revocable.",
    "Reviewers may not approve their own authored records.",
    "Reviewers carry append-only audit trails bound to a supervision-receipt.",
    "Disagreement is governed, never silently averaged.",
]

REVERSIBLE_PROMOTION_PHILOSOPHY = [
    "Every promotion has a declared rollback path.",
    "Rollback fans out via declared lineage only.",
    "Rollback does not mutate captured runtime traces.",
    "Demoted nodes are preserved with lineage, never deleted.",
]

OEM_VERIFICATION_PHILOSOPHY = [
    "OEM verification is content-addressed binding to an OEM-origin artifact.",
    "OEM verification requires dual-review and binding artifact pinning.",
    "OEM verification is invalidated by supersession of its source.",
    "OEM verification does not imply operational proof; that is a separate tier.",
]

OPERATIONAL_TRUST_PRINCIPLES = [
    "Operational trust is the joint property of (corpus tier, runtime determinism, supervised outcome).",
    "Operational trust never bypasses any of its three inputs.",
    "Operational trust is product-scoped; cross-product inheritance is forbidden.",
    "Operational trust is reassessed on every supersession, dispute, or incident.",
]


# =============================================================================
# TASK 9 — OPERATIONAL SUSTAINABILITY
# =============================================================================

LONG_TERM_COMMITMENTS = [
    "corpus growth proceeds through declared categories per product, preserving symmetry",
    "reviewer ecosystem grows via the reviewer registry; revocation is a first-class event",
    "operational maintenance is performed against the lineage, never against canonical JSON in-place",
    "knowledge aging is detected by stale-knowledge rules; aged records are queued, not dropped",
    "OEM updates enter as new bindings; old bindings are superseded, not overwritten",
    "runtime-safe growth: new domains route through ALLOWED_DOMAINS + governed retrieval kinds",
    "production operational scaling is out of scope; sustainability is for the governed corpus only",
]

SUSTAINABILITY_INVARIANTS = [
    "no autonomous promotion path exists, ever",
    "no record is ever silently deleted; archival preserves lineage",
    "no reviewer signoff is ever silently overridden",
    "no runtime mutation of knowledge-core occurs from any layer",
    "no macro-governance mega-layer is spawned by sustainability work",
]


# =============================================================================
# BUILD
# =============================================================================

def build():
    LIFECYCLE_ROOT.mkdir(parents=True, exist_ok=True)
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    # --- Task 1 -----------------------------------------------------------
    write_pair(
        LIFECYCLE_ROOT / "lifecycle-model", "lifecycle-model",
        "Knowledge Lifecycle Model",
        "States, transitions, promotion gates, demotion paths, archival rules.",
        [
            ("States", md_list([f"`{s['id']}` — {s['description']}" for s in LIFECYCLE_STATES])),
            ("Transitions", md_list([f"`{t['from']}` → `{t['to']}` via *{t['gate']}* (actor: {t['actor']}, reversible: {t['reversible']})" for t in LIFECYCLE_TRANSITIONS])),
            ("Promotion gates", md_list([f"**{g['gate']}** — requires: " + ", ".join(g['requires']) for g in PROMOTION_GATES])),
            ("Archival rules", md_list(ARCHIVAL_RULES)),
        ],
        {
            "schema": SCHEMA, "kind": "lifecycle-model",
            "states": LIFECYCLE_STATES,
            "transitions": LIFECYCLE_TRANSITIONS,
            "promotion_gates": PROMOTION_GATES,
            "archival_rules": ARCHIVAL_RULES,
        },
    )

    # --- Task 2 -----------------------------------------------------------
    write_pair(
        LIFECYCLE_ROOT / "review-workflows", "review-workflows",
        "Human Review Workflows",
        "Reviewer assignment, evidence attachment, single/dual review, consensus, irreversible-operation review.",
        [
            ("Reviewer assignment", md_list(REVIEWER_ASSIGNMENT)),
            ("Workflow steps", md_list([f"**{s['step']}** — {s['responsibility']} (actor: {s['actor']})" for s in WORKFLOW_STEPS])),
            ("Consensus rules", md_list(CONSENSUS_RULES)),
            ("Irreversible-operation review", md_list(IRREVERSIBLE_OPERATION_REVIEW)),
        ],
        {
            "schema": SCHEMA, "kind": "review-workflows",
            "reviewer_assignment": REVIEWER_ASSIGNMENT,
            "workflow_steps": WORKFLOW_STEPS,
            "consensus_rules": CONSENSUS_RULES,
            "irreversible_operation_review": IRREVERSIBLE_OPERATION_REVIEW,
        },
    )

    # --- Task 3 -----------------------------------------------------------
    write_pair(
        LIFECYCLE_ROOT / "oem-binding", "oem-binding",
        "OEM Evidence Binding",
        "Content-addressed, append-only bindings to OEM source artifacts.",
        [
            ("Binding kinds", md_list([f"`{b['kind']}` — fields: " + ", ".join(b['fields']) for b in BINDING_KINDS])),
            ("Binding rules", md_list(BINDING_RULES)),
            ("Traceable trust pipeline", md_list(TRACEABLE_TRUST_PIPELINE)),
        ],
        {
            "schema": SCHEMA, "kind": "oem-binding",
            "binding_kinds": BINDING_KINDS,
            "binding_rules": BINDING_RULES,
            "traceable_trust_pipeline": TRACEABLE_TRUST_PIPELINE,
        },
    )

    # --- Task 4 -----------------------------------------------------------
    write_pair(
        LIFECYCLE_ROOT / "trust-model", "trust-model",
        "Trust Evolution Model",
        "Tiers, transitions, inheritance floor, decay, stale-knowledge detection, dispute propagation.",
        [
            ("Trust tiers", md_list([f"`{t['tier']}` (weight {t['weight']}, runtime: {t['runtime_use']})" for t in TRUST_TIERS])),
            ("Trust transitions", md_list(TRUST_TRANSITIONS)),
            ("Trust decay rules", md_list(TRUST_DECAY_RULES)),
            ("Stale-knowledge detection", md_list(STALE_KNOWLEDGE_DETECTION)),
        ],
        {
            "schema": SCHEMA, "kind": "trust-model",
            "trust_tiers": TRUST_TIERS,
            "trust_transitions": TRUST_TRANSITIONS,
            "trust_decay_rules": TRUST_DECAY_RULES,
            "stale_knowledge_detection": STALE_KNOWLEDGE_DETECTION,
        },
    )

    # --- Task 5 -----------------------------------------------------------
    write_pair(
        LIFECYCLE_ROOT / "reversibility", "reversibility",
        "Reversible Promotion Governance",
        "Append-only promotion/demotion events, invalidation propagation, runtime-safe demotion, lineage preservation.",
        [
            ("Reversible promotion rules", md_list(REVERSIBLE_PROMOTION_RULES)),
            ("Invalidation propagation", md_list(INVALIDATION_PROPAGATION)),
            ("Runtime-safe demotion", md_list(RUNTIME_SAFE_DEMOTION)),
            ("Deprecated node handling", md_list(DEPRECATED_NODE_HANDLING)),
            ("Historical lineage preservation", md_list(HISTORICAL_LINEAGE_PRESERVATION)),
        ],
        {
            "schema": SCHEMA, "kind": "reversibility",
            "reversible_promotion_rules": REVERSIBLE_PROMOTION_RULES,
            "invalidation_propagation": INVALIDATION_PROPAGATION,
            "runtime_safe_demotion": RUNTIME_SAFE_DEMOTION,
            "deprecated_node_handling": DEPRECATED_NODE_HANDLING,
            "historical_lineage_preservation": HISTORICAL_LINEAGE_PRESERVATION,
        },
    )

    # --- Task 6 -----------------------------------------------------------
    write_pair(
        LIFECYCLE_ROOT / "reviewer-accountability", "reviewer-accountability",
        "Reviewer Accountability",
        "Identity, approval provenance, audit trails, disagreement handling, critical-operation signoff.",
        [
            ("Reviewer identity fields", md_list(REVIEWER_IDENTITY_FIELDS)),
            ("Approval provenance fields", md_list(APPROVAL_PROVENANCE_FIELDS)),
            ("Review audit trail rules", md_list(REVIEW_AUDIT_TRAIL_RULES)),
            ("Disagreement handling", md_list(DISAGREEMENT_HANDLING)),
            ("Critical-operation signoff", md_list(CRITICAL_OPERATION_SIGNOFF)),
        ],
        {
            "schema": SCHEMA, "kind": "reviewer-accountability",
            "reviewer_identity_fields": REVIEWER_IDENTITY_FIELDS,
            "approval_provenance_fields": APPROVAL_PROVENANCE_FIELDS,
            "review_audit_trail_rules": REVIEW_AUDIT_TRAIL_RULES,
            "disagreement_handling": DISAGREEMENT_HANDLING,
            "critical_operation_signoff": CRITICAL_OPERATION_SIGNOFF,
        },
    )

    # --- Task 7 -----------------------------------------------------------
    write_pair(
        LIFECYCLE_ROOT / "corpus-maturity", "corpus-maturity",
        "Corpus Maturity Governance",
        "Dimensions, score formulas, maturity tiers, runtime-trustworthiness inputs.",
        [
            ("Maturity dimensions", md_list([f"`{d['id']}` — rolls up from: " + ", ".join(d['rolls_up_from']) for d in MATURITY_DIMENSIONS])),
            ("Score formula", md_list(MATURITY_SCORE_FORMULA)),
            ("Maturity tiers", md_list([f"`{t['tier']}` ({t['range']}) — runtime: {t['runtime_use']}" for t in MATURITY_TIERS])),
            ("Runtime-trustworthiness inputs", md_list(RUNTIME_TRUSTWORTHINESS_INPUTS)),
        ],
        {
            "schema": SCHEMA, "kind": "corpus-maturity",
            "maturity_dimensions": MATURITY_DIMENSIONS,
            "maturity_score_formula": MATURITY_SCORE_FORMULA,
            "maturity_tiers": MATURITY_TIERS,
            "runtime_trustworthiness_inputs": RUNTIME_TRUSTWORTHINESS_INPUTS,
        },
    )

    # --- Task 8 — doctrine root ------------------------------------------
    (CONST_ROOT / "README.md").write_text(
        "# KNOWLEDGE LIFECYCLE GOVERNANCE\n\n"
        "Twenty-second constitutional layer. Modeling-only. Subordinate to knowledge-core "
        "and to all twenty-one prior governance layers.\n\n"
        "Governs how candidate operational knowledge becomes trusted operational knowledge "
        "while preserving provenance, supervision, reversibility, accountability, and operational safety.\n\n"
        f"Schema: `{SCHEMA}`. Generated: {now_iso()}.\n",
        encoding="utf-8",
    )

    write_pair(
        CONST_ROOT, "00-charter",
        "Charter — Knowledge Lifecycle Governance",
        "Declares principles + authority for governed knowledge evolution.",
        [
            ("Principles", md_list(CHARTER_PRINCIPLES)),
            ("Bound artifacts", md_list([
                "`wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/lifecycle-model/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/review-workflows/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/oem-binding/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/trust-model/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/reversibility/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/reviewer-accountability/`",
                "`wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/corpus-maturity/`",
            ])),
            ("Hard Exclusions", md_list([
                "DO NOT expand cognition architecture recursively",
                "DO NOT spawn new macro-governance abstractions",
                "DO NOT implement autonomous promotion",
                "DO NOT bypass human review",
                "DO NOT deploy production systems",
                "DO NOT generate images / PDFs / large frontends",
            ])),
        ],
        {
            "schema": SCHEMA, "kind": "charter",
            "principles": CHARTER_PRINCIPLES,
            "subordinate_to": SUBORDINATE_TO,
            "generated": now_iso(),
        },
    )

    for slug, title, intro, principles in [
        ("trust-philosophy", "Trust Philosophy",
         "Trust is earned through declared gates, never inferred from usage.", TRUST_PHILOSOPHY),
        ("operational-knowledge-evolution-doctrine", "Operational Knowledge Evolution Doctrine",
         "Evolution is additive, auditable, bounded, symmetric.", OPERATIONAL_KNOWLEDGE_EVOLUTION_DOCTRINE),
        ("reviewer-governance-philosophy", "Reviewer Governance Philosophy",
         "Reviewers are identified, scoped, revocable, and audited.", REVIEWER_GOVERNANCE_PHILOSOPHY),
        ("reversible-promotion-philosophy", "Reversible Promotion Philosophy",
         "Every promotion has a declared rollback path.", REVERSIBLE_PROMOTION_PHILOSOPHY),
        ("oem-verification-philosophy", "OEM Verification Philosophy",
         "OEM verification is content-addressed and dual-reviewed.", OEM_VERIFICATION_PHILOSOPHY),
        ("operational-trust-principles", "Operational Trust Principles",
         "Operational trust = corpus tier × runtime determinism × supervised outcome.",
         OPERATIONAL_TRUST_PRINCIPLES),
    ]:
        write_pair(
            CONST_ROOT / slug, slug, title, intro,
            [("Principles", md_list(principles))],
            {"schema": SCHEMA, "kind": slug, "principles": principles},
        )

    # --- Final 10 reports -------------------------------------------------
    reports = [
        ("01-lifecycle-model-summary.json", {
            "schema": SCHEMA, "kind": "lifecycle-model-summary",
            "states_count": len(LIFECYCLE_STATES),
            "transitions_count": len(LIFECYCLE_TRANSITIONS),
            "promotion_gates_count": len(PROMOTION_GATES),
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/lifecycle-model/",
        }),
        ("02-review-workflow-summary.json", {
            "schema": SCHEMA, "kind": "review-workflow-summary",
            "workflow_steps": [s["step"] for s in WORKFLOW_STEPS],
            "consensus_rules_count": len(CONSENSUS_RULES),
            "irreversible_operation_review_required_for": [
                "factory-reset", "admin-wipe", "firmware-update",
                "all warnings tagged irreversible-operation",
            ],
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/review-workflows/",
        }),
        ("03-oem-binding-summary.json", {
            "schema": SCHEMA, "kind": "oem-binding-summary",
            "binding_kinds": [b["kind"] for b in BINDING_KINDS],
            "binding_rules_count": len(BINDING_RULES),
            "traceable_trust_pipeline_steps": len(TRACEABLE_TRUST_PIPELINE),
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/oem-binding/",
        }),
        ("04-trust-evolution-summary.json", {
            "schema": SCHEMA, "kind": "trust-evolution-summary",
            "tiers": [t["tier"] for t in TRUST_TIERS],
            "decay_rules_count": len(TRUST_DECAY_RULES),
            "stale_detection_rules_count": len(STALE_KNOWLEDGE_DETECTION),
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/trust-model/",
        }),
        ("05-reversible-promotion-summary.json", {
            "schema": SCHEMA, "kind": "reversible-promotion-summary",
            "rules_count": len(REVERSIBLE_PROMOTION_RULES),
            "invalidation_propagation_rules_count": len(INVALIDATION_PROPAGATION),
            "runtime_safe_demotion_rules_count": len(RUNTIME_SAFE_DEMOTION),
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/reversibility/",
        }),
        ("06-reviewer-accountability-summary.json", {
            "schema": SCHEMA, "kind": "reviewer-accountability-summary",
            "reviewer_identity_fields_count": len(REVIEWER_IDENTITY_FIELDS),
            "approval_provenance_fields_count": len(APPROVAL_PROVENANCE_FIELDS),
            "audit_trail_rules_count": len(REVIEW_AUDIT_TRAIL_RULES),
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/reviewer-accountability/",
        }),
        ("07-corpus-maturity-summary.json", {
            "schema": SCHEMA, "kind": "corpus-maturity-summary",
            "dimensions": [d["id"] for d in MATURITY_DIMENSIONS],
            "tiers": [t["tier"] for t in MATURITY_TIERS],
            "artifact": "wp-content/themes/beslock-custom/User manuals/knowledge-lifecycle/corpus-maturity/",
        }),
        ("08-lifecycle-governance-summary.json", {
            "schema": SCHEMA, "kind": "lifecycle-governance-summary",
            "layer_index": 22,
            "subordinate_to_count": len(SUBORDINATE_TO),
            "constitutional_root": "wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/KNOWLEDGE_LIFECYCLE_GOVERNANCE/",
            "reports_root": "wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/knowledge-lifecycle/",
            "doctrine_sections": [
                "trust-philosophy",
                "operational-knowledge-evolution-doctrine",
                "reviewer-governance-philosophy",
                "reversible-promotion-philosophy",
                "oem-verification-philosophy",
                "operational-trust-principles",
            ],
        }),
        ("09-unresolved-trust-risks.json", {
            "schema": SCHEMA, "kind": "unresolved-trust-risks",
            "items": [
                {"id": "no-reviewer-registry-implementation",   "severity": "high",   "impact": "review workflow is modeled but no executable registry exists yet"},
                {"id": "no-oem-binding-store",                  "severity": "high",   "impact": "binding records are modeled but no executable store/index exists yet"},
                {"id": "no-promotion-event-log",                "severity": "high",   "impact": "promotion/demotion events are modeled but no append-only log is wired"},
                {"id": "no-dispute-resolution-implementation",  "severity": "high",   "impact": "dispute state caps trust but no resolution UI/CLI exists"},
                {"id": "no-stale-detector-implementation",      "severity": "medium", "impact": "stale-knowledge detection is modeled, not yet scheduled"},
                {"id": "no-maturity-score-computer",            "severity": "medium", "impact": "maturity formulas are declared, not computed yet"},
                {"id": "no-cryptographic-signoff",              "severity": "medium", "impact": "signoff_key_fingerprint is declared but not bound to a real key"},
                {"id": "candidate-records-still-await-elevation","severity": "high",  "impact": "the 132 Phase-27 candidates remain unreviewed under the new lifecycle"},
                {"id": "no-supersession-graph-store",           "severity": "medium", "impact": "superseded_by pointers are modeled but not yet indexed for fan-out queries"},
            ],
        }),
        ("10-operational-sustainability-reassessment.json", {
            "schema": SCHEMA, "kind": "operational-sustainability-reassessment",
            "architecture_status": "FOUNDATIONALLY COMPLETE (unchanged)",
            "runtime_status": "ARCHITECTURALLY MATURE + HARDENED + FUNCTIONALLY VALIDATED (unchanged)",
            "trust_governance_status": "MODELED (executable enforcement pending)",
            "primary_bottleneck": "TRUSTED KNOWLEDGE EVOLUTION (now governed by declared model)",
            "next_bottleneck": "executable enforcement of the lifecycle model (registry, event log, binding store)",
            "long_term_commitments": LONG_TERM_COMMITMENTS,
            "sustainability_invariants": SUSTAINABILITY_INVARIANTS,
            "generated": now_iso(),
        }),
    ]
    for name, payload in reports:
        (REPORTS_ROOT / name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(f"Knowledge Lifecycle Governance (layer 22) written to:\n  {LIFECYCLE_ROOT}\n  {CONST_ROOT}\n  {REPORTS_ROOT}")


if __name__ == "__main__":
    build()
