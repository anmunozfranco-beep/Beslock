"""Phase 11 — Knowledge Evolution & Lifecycle Governance builder.

Idempotent, non-destructive, modeling-only. Establishes the fourth+ constitutional
layer `LIFECYCLE_GOVERNANCE` under KNOWLEDGE_BUILDING/, plus 10 numbered reports.

Hard rules honored:
  * NEVER modifies per-product knowledge-core/* files
  * NEVER modifies prior governance layers (visual / knowledge / semantic / experience)
  * NEVER touches Comfy / orchestration / runtime / frontend
  * NEVER generates PDFs, images, chatbots, publication systems
  * Modeling-only. Does not originate product knowledge.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths & schema

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content" / "themes" / "beslock-custom" / "User manuals"
KB = USER_MANUALS / "KNOWLEDGE_BUILDING"
LG = KB / "LIFECYCLE_GOVERNANCE"
REPORTS = USER_MANUALS / "_repository-governance" / "reports" / "lifecycle-governance"

SCHEMA = "lifecycle-governance/1.0"
TODAY = date.today().isoformat()

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

# ---------------------------------------------------------------------------
# 1. Lifecycle stages

LIFECYCLE_STAGES = [
    {"id": "discovered",    "order":  1, "terminal": False, "description": "Source material identified (OEM PDF, image, web), no semantic interpretation yet."},
    {"id": "extracted",     "order":  2, "terminal": False, "description": "Raw content extracted from source (text, structure, references)."},
    {"id": "ocr-derived",   "order":  3, "terminal": False, "description": "Content obtained via OCR; explicitly flagged for confidence review."},
    {"id": "inferred",      "order":  4, "terminal": False, "description": "Semantic shape inferred from extracted/OCR content; not yet normalized."},
    {"id": "normalized",    "order":  5, "terminal": False, "description": "Conformed to ontology vocabulary, id format, and shared terminology."},
    {"id": "canonicalized", "order":  6, "terminal": False, "description": "Single authoritative representation chosen across duplicates/synonyms/bilingual variants."},
    {"id": "verified",      "order":  7, "terminal": False, "description": "Reviewed by human/OEM checkpoint; lineage and evidence cross-validated."},
    {"id": "promoted",      "order":  8, "terminal": False, "description": "Granted operational authority; usable by retrieval, onboarding, troubleshooting models."},
    {"id": "deprecated",    "order":  9, "terminal": False, "description": "Marked for retirement; still readable; flagged not-for-new-use."},
    {"id": "superseded",    "order": 10, "terminal": False, "description": "Replaced by a newer canonical artifact; lineage link to successor required."},
    {"id": "archived",      "order": 11, "terminal": True,  "description": "Removed from active surfaces; retained for audit/lineage; never re-promoted."},
    {"id": "unresolved",    "order": 12, "terminal": False, "description": "Cannot progress without human/OEM input; tracked as knowledge debt."},
]

LIFECYCLE_TRANSITIONS = [
    ("discovered", "extracted"),
    ("extracted", "ocr-derived"),
    ("extracted", "inferred"),
    ("ocr-derived", "inferred"),
    ("inferred", "normalized"),
    ("inferred", "unresolved"),
    ("normalized", "canonicalized"),
    ("normalized", "unresolved"),
    ("canonicalized", "verified"),
    ("canonicalized", "unresolved"),
    ("verified", "promoted"),
    ("verified", "deprecated"),
    ("promoted", "deprecated"),
    ("promoted", "superseded"),
    ("deprecated", "superseded"),
    ("deprecated", "archived"),
    ("superseded", "archived"),
    ("unresolved", "normalized"),
    ("unresolved", "archived"),
]

# ---------------------------------------------------------------------------
# 2. Promotion governance

PROMOTION_LEVELS = [
    {"id": "evidence",            "rank": 0, "description": "Raw OEM source or extracted artifact; not citable as truth."},
    {"id": "semantic-candidate",  "rank": 1, "description": "Inferred semantic shape; speculative; never user-facing."},
    {"id": "normalized-artifact", "rank": 2, "description": "Conforms to ontology and id rules; safe for internal cross-reference."},
    {"id": "canonical-knowledge", "rank": 3, "description": "One authoritative representation; safe for retrieval indexing."},
    {"id": "verified-truth",      "rank": 4, "description": "Human/OEM-verified; safe for safety-critical surfaces and onboarding."},
]

PROMOTION_CRITERIA = [
    {"from": "evidence",            "to": "semantic-candidate",  "requires": ["source-traceability", "extraction-method-recorded"]},
    {"from": "semantic-candidate",  "to": "normalized-artifact", "requires": ["ontology-conformance", "id-format-valid", "terminology-aligned"]},
    {"from": "normalized-artifact", "to": "canonical-knowledge", "requires": ["duplicate-resolution", "synonym-merge", "bilingual-merge", "cross-product-collision-resolved"]},
    {"from": "canonical-knowledge", "to": "verified-truth",      "requires": ["human-review-pass OR oem-confirmation", "evidence-link", "no-open-debt-of-blocking-class"]},
]

PROMOTION_AUTHORITIES = [
    {"level": "semantic-candidate",  "authority": "automated-pipeline"},
    {"level": "normalized-artifact", "authority": "automated-pipeline + ontology-validator"},
    {"level": "canonical-knowledge", "authority": "automated-pipeline + canonicalization-resolver"},
    {"level": "verified-truth",      "authority": "human-reviewer OR OEM-confirmation"},
]

# ---------------------------------------------------------------------------
# 3. Deprecation governance

DEPRECATION_REASONS = [
    {"id": "superseded-by-newer-version",  "destructive": False, "requires_successor": True},
    {"id": "ontology-rule-change",         "destructive": False, "requires_successor": False},
    {"id": "oem-correction",               "destructive": False, "requires_successor": True},
    {"id": "evidence-retracted",           "destructive": False, "requires_successor": False},
    {"id": "duplicate-canonicalized-away", "destructive": False, "requires_successor": True},
    {"id": "product-discontinued",         "destructive": False, "requires_successor": False},
    {"id": "policy-restricted",            "destructive": False, "requires_successor": False},
]

DEPRECATION_RULES = [
    "Deprecation is reversible until archival; archival is terminal.",
    "Lineage links (predecessor/successor) MUST be recorded on every transition.",
    "Deprecated artifacts remain readable; surfaces must render a deprecation badge.",
    "Superseded artifacts MUST link to their successor; orphaned supersession is a blocking debt.",
    "Stale terminology is deprecated, never deleted; aliases preserve historical references.",
    "Obsolete workflows retain ordering and warnings for forensic audit.",
    "Silent destruction of any semantic artifact is a governance violation.",
]

# ---------------------------------------------------------------------------
# 4. Versioning governance

VERSIONED_AXES = [
    {"axis": "ontology",        "scheme": "semver",   "scope": "global",      "breaking_triggers": ["domain-removed", "field-removed", "id-format-changed"]},
    {"axis": "schema",          "scheme": "semver",   "scope": "per-schema",  "breaking_triggers": ["required-field-added", "field-type-changed"]},
    {"axis": "terminology",     "scheme": "calver",   "scope": "global",      "breaking_triggers": ["canonical-term-renamed-without-alias"]},
    {"axis": "workflow",        "scheme": "semver",   "scope": "per-product", "breaking_triggers": ["step-reordered", "step-removed", "warning-removed"]},
    {"axis": "procedure",       "scheme": "semver",   "scope": "per-product", "breaking_triggers": ["safety-step-removed", "input-precondition-changed"]},
    {"axis": "governance-doc",  "scheme": "revision", "scope": "per-doctrine","breaking_triggers": ["principle-removed", "authority-area-removed"]},
    {"axis": "product-release", "scheme": "oem-tag",  "scope": "per-product", "breaking_triggers": ["hardware-revision", "firmware-major-change"]},
]

VERSION_RULES = [
    "Every versioned artifact records: previous-version, change-type (additive/breaking/corrective), change-rationale.",
    "Breaking changes MUST emit a change-impact report (see TASK 7) before promotion.",
    "Calver applies to terminology releases (terminology drifts slowly; date-anchored audit trail preferred).",
    "Governance doctrine is revision-numbered, not semver — principles do not 'minor-bump'.",
    "Product-release versions are OEM-authoritative; the knowledge center mirrors, never invents, them.",
]

# ---------------------------------------------------------------------------
# 5. Knowledge health monitoring

HEALTH_INDICATORS = [
    {"id": "stale-procedure",            "severity": "medium", "detection": "promoted artifact unchanged > review-cycle and no recent OEM source"},
    {"id": "orphan-entity",              "severity": "medium", "detection": "entity referenced by no procedure / workflow / capability"},
    {"id": "unresolved-reference",       "severity": "high",   "detection": "reference target id not present in canonical set"},
    {"id": "maturity-inconsistency",     "severity": "medium", "detection": "promoted artifact whose dependencies are still semantic-candidate"},
    {"id": "duplicated-semantic",        "severity": "high",   "detection": "two canonical artifacts with overlapping intent (synonym/bilingual collision)"},
    {"id": "governance-conflict",        "severity": "high",   "detection": "two doctrine docs assert contradictory rules in the same authority area"},
    {"id": "ontology-fragmentation",     "severity": "high",   "detection": "domain referenced with diverging field shapes across products"},
    {"id": "low-confidence-overload",    "severity": "medium", "detection": "ratio of ocr-derived/inferred content above per-product threshold"},
    {"id": "lineage-break",              "severity": "critical","detection": "deprecated/superseded artifact missing successor link"},
    {"id": "promotion-without-evidence", "severity": "critical","detection": "verified-truth artifact missing source provenance"},
]

HEALTH_THRESHOLDS = {
    "low_confidence_ratio_max": 0.35,
    "stale_procedure_review_cycle_days": 365,
    "orphan_entity_grace_days": 90,
    "lineage_break_tolerance": 0,
    "promotion_without_evidence_tolerance": 0,
}

# ---------------------------------------------------------------------------
# 6. Review governance

REVIEW_CHECKPOINTS = [
    {"id": "ontology-conformance-review",   "trigger": "promotion to normalized-artifact",  "actor": "automated + ontology-steward"},
    {"id": "canonicalization-review",       "trigger": "promotion to canonical-knowledge",  "actor": "canonicalization-resolver + human-reviewer"},
    {"id": "human-verification-review",     "trigger": "promotion to verified-truth",       "actor": "human-reviewer"},
    {"id": "oem-verification-checkpoint",   "trigger": "safety-critical or P0 priority",    "actor": "OEM-confirmation"},
    {"id": "deprecation-review",            "trigger": "any deprecation request",           "actor": "human-reviewer"},
    {"id": "ambiguity-escalation-review",   "trigger": "unresolved-stage entry",            "actor": "human-reviewer + OEM-when-applicable"},
    {"id": "governance-revision-review",    "trigger": "doctrine principle change",         "actor": "governance-steward (multi-party)"},
]

REVIEW_RULES = [
    "Every promotion to verified-truth requires a human reviewer signature recorded in lineage.",
    "Safety-critical (P0) artifacts require OEM confirmation in addition to human review.",
    "Unresolved-stage artifacts are surfaced to a review queue, never silently dropped.",
    "Ambiguity escalation must record: the ambiguity, the candidates considered, the decision rationale.",
    "Governance principle changes require multi-party review and a revision-number bump.",
]

# ---------------------------------------------------------------------------
# 7. Change impact modeling

IMPACT_TARGETS = [
    "ontology", "schemas", "terminology", "entities", "procedures", "workflows",
    "warnings", "capabilities", "specifications", "troubleshooting",
    "procedural-semantics", "visual-intent", "visual-risk", "publication-intent",
    "component-visibility", "provenance",
    "retrieval-index", "onboarding-flows", "guidance-triggers", "cognitive-load-map",
    "priority-assignments", "experience-charter",
]

IMPACT_RULES = [
    {"change": "terminology rename without alias",        "propagates_to": ["entities", "procedures", "workflows", "warnings", "retrieval-index", "guidance-triggers"]},
    {"change": "ontology field removed",                  "propagates_to": ["schemas", "all knowledge-core domains", "retrieval-index"]},
    {"change": "procedure step reordered",                "propagates_to": ["workflows", "cognitive-load-map", "onboarding-flows", "guidance-triggers"]},
    {"change": "warning removed",                         "propagates_to": ["procedures", "workflows", "publication-intent", "experience-charter"]},
    {"change": "entity superseded",                       "propagates_to": ["procedures", "workflows", "visual-intent", "component-visibility", "retrieval-index"]},
    {"change": "priority tier change (P-level)",          "propagates_to": ["onboarding-flows", "guidance-triggers", "review-checkpoints"]},
    {"change": "visual-risk reclassification",            "propagates_to": ["visual-intent", "publication-intent", "guidance-triggers"]},
    {"change": "schema breaking change",                  "propagates_to": ["all knowledge-core domains", "retrieval-index", "review-checkpoints"]},
]

IMPACT_PROCEDURE = [
    "Detect change class (additive / corrective / breaking).",
    "Resolve propagation set via IMPACT_RULES.",
    "Generate change-impact-report listing every dependent artifact id.",
    "Block promotion if any dependent artifact would enter unresolved/lineage-break state.",
    "Attach the impact-report id to the version-bump record.",
]

# ---------------------------------------------------------------------------
# 8. Knowledge debt governance

DEBT_CLASSES = [
    {"id": "unresolved-gap",              "blocking": False, "description": "Known missing knowledge area; tracked but not blocking promotion of unrelated artifacts."},
    {"id": "ocr-confidence-debt",         "blocking": False, "description": "Content derived from OCR below confidence threshold; requires human pass."},
    {"id": "low-confidence-region",       "blocking": False, "description": "Cluster of inferred artifacts in one domain; needs targeted review."},
    {"id": "missing-specification",       "blocking": True,  "description": "Procedure references a spec that does not exist; blocks promotion of dependents."},
    {"id": "unresolved-semantic",         "blocking": True,  "description": "Ambiguity escalation that did not resolve; blocks canonicalization."},
    {"id": "governance-todo",             "blocking": False, "description": "Open governance principle / authority gap; tracked at doctrine level."},
    {"id": "blocked-domain",              "blocking": True,  "description": "Whole semantic domain blocked pending OEM input; blocks promotion within domain."},
    {"id": "lineage-debt",                "blocking": True,  "description": "Deprecated/superseded artifact missing successor link."},
    {"id": "maturity-debt",               "blocking": False, "description": "Promoted artifact whose dependencies are not yet promoted."},
]

DEBT_RULES = [
    "All debt items have: id, class, owner, opened-date, blocking-flag, related-artifact-ids.",
    "Blocking debt prevents promotion of dependent artifacts but never destroys lineage.",
    "Debt items are closed only by an explicit resolution event (resolved / wont-fix / superseded-by).",
    "Wont-fix debt MUST record rationale and reviewer.",
]

# ---------------------------------------------------------------------------
# 9. Long-term architecture governance

ARCHITECTURE_PRINCIPLES = [
    "The knowledge-core is the single source of truth; all other layers are subordinate.",
    "Constitutional layers are additive; new layers must declare their subordination to knowledge-core.",
    "New products integrate by inheriting ontology + governance + lifecycle, never by forking them.",
    "Multimodal systems (visual, retrieval, onboarding, troubleshooting) consume knowledge; they never originate it.",
    "Governance expansion is revision-numbered; revisions never silently rewrite past doctrine.",
    "Ontology coherence is maintained by: shared vocabulary, shared id format, shared promotion gates.",
    "Every new system declares its read/write surface against the knowledge-core lifecycle states it depends on.",
    "Lineage preservation is non-negotiable across product additions, ontology revisions, and layer expansions.",
]

NEW_PRODUCT_INTEGRATION_STEPS = [
    "Allocate product-id and per-product knowledge-core/ folder.",
    "Run discovery → extraction → ocr-derived (where applicable) → inferred pipeline.",
    "Apply ontology + terminology vocabulary; produce normalized artifacts.",
    "Run canonicalization with cross-product collision detection.",
    "Open review checkpoints; promote in priority order (P0 → P5).",
    "Register product in priority-assignments, onboarding-flows, troubleshooting tiers.",
    "Emit change-impact-report scoped to additive change.",
]

LAYER_SUBORDINATION = [
    {"layer": "VISUAL_GOVERNANCE",     "subordinate_to": "knowledge-core", "may_originate": False},
    {"layer": "KNOWLEDGE_CENTER",      "subordinate_to": "knowledge-core", "may_originate": False, "note": "indexes, never authors"},
    {"layer": "SEMANTIC_GOVERNANCE",   "subordinate_to": "knowledge-core", "may_originate": False},
    {"layer": "EXPERIENCE_GOVERNANCE", "subordinate_to": "knowledge-core", "may_originate": False},
    {"layer": "LIFECYCLE_GOVERNANCE",  "subordinate_to": "knowledge-core", "may_originate": False, "note": "governs evolution, not content"},
]

# ---------------------------------------------------------------------------
# 10. Future system readiness

FUTURE_CONSUMERS = [
    {"id": "continuous-oem-ingestion", "consumes": ["lifecycle-stages", "promotion-criteria", "review-checkpoints"], "readiness_gate": "OEM source-tracker present per product"},
    {"id": "automated-semantic-enrichment", "consumes": ["promotion-criteria", "ontology-conformance"], "readiness_gate": "ontology version pinned + breaking-change detector active"},
    {"id": "multilingual-expansion", "consumes": ["terminology axis", "canonicalization rules"], "readiness_gate": "bilingual-merge backlog cleared; alias registry active"},
    {"id": "RAG-system", "consumes": ["canonical-knowledge", "verified-truth", "lineage links"], "readiness_gate": "lineage-break tolerance = 0; promotion-without-evidence tolerance = 0"},
    {"id": "troubleshooting-assistant", "consumes": ["troubleshooting tiers", "symptom corpus", "priority-assignments"], "readiness_gate": "symptom corpus ≥ 10 per product"},
    {"id": "onboarding-system", "consumes": ["onboarding-flows", "guidance-triggers", "cognitive-load-map"], "readiness_gate": "per-product onboarding specialisation present"},
    {"id": "future-visual-assistance", "consumes": ["visual-intent", "visual-risk", "component-visibility"], "readiness_gate": "visual-risk reclassification freeze window in place"},
    {"id": "future-publication-systems", "consumes": ["publication-intent", "verified-truth", "deprecation badges"], "readiness_gate": "deprecation badge renderer specified at doctrine level"},
]

NON_NEGOTIABLES = [
    "provenance preserved on every artifact, every version, every transition",
    "governance preserved across layer additions and revisions",
    "semantic integrity preserved across promotion and deprecation",
    "ontology coherence preserved across new products and new layers",
]

# ---------------------------------------------------------------------------
# Charter

CHARTER_PRINCIPLES = [
    "Knowledge evolves; lineage does not break.",
    "Every artifact has a lifecycle stage; no artifact is stage-less.",
    "Promotion is gated, evidenced, and reviewed; never implicit.",
    "Deprecation is recorded, never silent; archival is the only terminal state.",
    "Versioning is explicit on every axis; breaking changes emit impact reports.",
    "Health monitoring is continuous; critical indicators have zero tolerance.",
    "Human review is mandatory at verified-truth and at safety-critical promotions.",
    "Knowledge debt is named, owned, and closed only by an explicit event.",
    "Governance is additive and subordinate to the knowledge-core.",
]

AUTHORITY_AREAS = [
    "lifecycle-stages", "promotion-governance", "deprecation-governance",
    "versioning-governance", "knowledge-health", "review-governance",
    "change-impact", "knowledge-debt", "long-term-architecture", "future-readiness",
]

# ---------------------------------------------------------------------------
# Writers

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, payload: dict) -> None:
    payload = {"schema": SCHEMA, "generated": TODAY, **payload}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Doctrine generators

def doc_readme() -> str:
    return f"""# LIFECYCLE_GOVERNANCE

Constitutional layer governing the **long-term evolution** of the Beslock knowledge center.

- Schema: `{SCHEMA}`
- Generated: {TODAY}
- Subordinate to: `knowledge-core`
- Coexists with: `VISUAL_GOVERNANCE`, `KNOWLEDGE_CENTER`, `SEMANTIC_GOVERNANCE`, `EXPERIENCE_GOVERNANCE`

This layer governs **how knowledge changes over time**. It does not originate
knowledge, does not author content, and does not modify per-product
`knowledge-core/` files. It defines the lifecycle, promotion gates, deprecation
rules, versioning axes, health monitoring, review checkpoints, change-impact
propagation, knowledge debt classes, long-term architecture rules, and future
system readiness gates.

## Authority areas
{chr(10).join(f"- {a}" for a in AUTHORITY_AREAS)}

## Doctrine layout
- `00-charter.md` — principles + authority areas
- `knowledge-lifecycle/` — stages and transitions
- `promotion-governance/` — evidence → verified-truth gates
- `deprecation-governance/` — retirement, supersession, archival rules
- `version-governance/` — semver / calver / revision axes
- `knowledge-health/` — indicators and thresholds
- `review-governance/` — human and OEM checkpoints
- `change-impact/` — propagation rules and procedure
- `knowledge-debt/` — debt classes and resolution rules
- `long-term-architecture/` — principles, integration, subordination
- `future-readiness/` — downstream-consumer readiness gates
"""


def doc_charter() -> str:
    body = "# 00 — Lifecycle Governance Charter\n\n"
    body += "## Principles\n"
    for i, p in enumerate(CHARTER_PRINCIPLES, 1):
        body += f"{i}. {p}\n"
    body += "\n## Authority areas\n"
    for a in AUTHORITY_AREAS:
        body += f"- {a}\n"
    body += "\n## Hard guarantees\n"
    body += "- Modeling-only. Does not author product knowledge.\n"
    body += "- Subordinate to `knowledge-core`. Cannot override it.\n"
    body += "- Lineage preservation is non-negotiable.\n"
    body += "- Silent destruction of any semantic artifact is a governance violation.\n"
    return body


def doc_lifecycle() -> str:
    body = "# Knowledge Lifecycle\n\n## Stages\n\n"
    body += "| order | id | terminal | description |\n|---|---|---|---|\n"
    for s in LIFECYCLE_STAGES:
        body += f"| {s['order']} | `{s['id']}` | {s['terminal']} | {s['description']} |\n"
    body += "\n## Allowed transitions\n\n"
    for a, b in LIFECYCLE_TRANSITIONS:
        body += f"- `{a}` → `{b}`\n"
    body += "\nAny transition not listed above is a governance violation.\n"
    return body


def doc_promotion() -> str:
    body = "# Semantic Promotion Governance\n\n## Promotion levels\n\n"
    body += "| rank | id | description |\n|---|---|---|\n"
    for p in PROMOTION_LEVELS:
        body += f"| {p['rank']} | `{p['id']}` | {p['description']} |\n"
    body += "\n## Promotion criteria\n\n"
    for c in PROMOTION_CRITERIA:
        body += f"- `{c['from']}` → `{c['to']}` requires: {', '.join(c['requires'])}\n"
    body += "\n## Authority\n\n"
    for a in PROMOTION_AUTHORITIES:
        body += f"- `{a['level']}` — {a['authority']}\n"
    body += "\n## Lineage\n\nEvery promotion records: previous-level, evidence-link, reviewer (where applicable), timestamp.\n"
    return body


def doc_deprecation() -> str:
    body = "# Deprecation Governance\n\n## Deprecation reasons\n\n"
    body += "| id | requires successor |\n|---|---|\n"
    for r in DEPRECATION_REASONS:
        body += f"| `{r['id']}` | {r['requires_successor']} |\n"
    body += "\n## Rules\n\n"
    for r in DEPRECATION_RULES:
        body += f"- {r}\n"
    return body


def doc_version() -> str:
    body = "# Version Governance\n\n## Versioned axes\n\n"
    body += "| axis | scheme | scope | breaking triggers |\n|---|---|---|---|\n"
    for v in VERSIONED_AXES:
        body += f"| {v['axis']} | {v['scheme']} | {v['scope']} | {', '.join(v['breaking_triggers'])} |\n"
    body += "\n## Rules\n\n"
    for r in VERSION_RULES:
        body += f"- {r}\n"
    return body


def doc_health() -> str:
    body = "# Knowledge Health Monitoring\n\n## Indicators\n\n"
    body += "| id | severity | detection |\n|---|---|---|\n"
    for h in HEALTH_INDICATORS:
        body += f"| `{h['id']}` | {h['severity']} | {h['detection']} |\n"
    body += "\n## Thresholds\n\n"
    for k, v in HEALTH_THRESHOLDS.items():
        body += f"- `{k}`: {v}\n"
    return body


def doc_review() -> str:
    body = "# Review Governance\n\n## Checkpoints\n\n"
    body += "| id | trigger | actor |\n|---|---|---|\n"
    for r in REVIEW_CHECKPOINTS:
        body += f"| `{r['id']}` | {r['trigger']} | {r['actor']} |\n"
    body += "\n## Rules\n\n"
    for r in REVIEW_RULES:
        body += f"- {r}\n"
    return body


def doc_impact() -> str:
    body = "# Change Impact Modeling\n\n## Impact targets\n\n"
    for t in IMPACT_TARGETS:
        body += f"- {t}\n"
    body += "\n## Propagation rules\n\n"
    for r in IMPACT_RULES:
        body += f"- **{r['change']}** → {', '.join(r['propagates_to'])}\n"
    body += "\n## Procedure\n\n"
    for i, step in enumerate(IMPACT_PROCEDURE, 1):
        body += f"{i}. {step}\n"
    return body


def doc_debt() -> str:
    body = "# Knowledge Debt Governance\n\n## Debt classes\n\n"
    body += "| id | blocking | description |\n|---|---|---|\n"
    for d in DEBT_CLASSES:
        body += f"| `{d['id']}` | {d['blocking']} | {d['description']} |\n"
    body += "\n## Rules\n\n"
    for r in DEBT_RULES:
        body += f"- {r}\n"
    return body


def doc_architecture() -> str:
    body = "# Long-Term Architecture Governance\n\n## Principles\n\n"
    for i, p in enumerate(ARCHITECTURE_PRINCIPLES, 1):
        body += f"{i}. {p}\n"
    body += "\n## New product integration\n\n"
    for i, s in enumerate(NEW_PRODUCT_INTEGRATION_STEPS, 1):
        body += f"{i}. {s}\n"
    body += "\n## Layer subordination\n\n"
    body += "| layer | subordinate to | may originate | note |\n|---|---|---|---|\n"
    for l in LAYER_SUBORDINATION:
        body += f"| {l['layer']} | {l['subordinate_to']} | {l['may_originate']} | {l.get('note','')} |\n"
    return body


def doc_future() -> str:
    body = "# Future System Readiness\n\n## Future consumers\n\n"
    body += "| id | consumes | readiness gate |\n|---|---|---|\n"
    for f in FUTURE_CONSUMERS:
        body += f"| `{f['id']}` | {', '.join(f['consumes'])} | {f['readiness_gate']} |\n"
    body += "\n## Non-negotiables\n\n"
    for n in NON_NEGOTIABLES:
        body += f"- {n}\n"
    body += "\n## Hard exclusions\n\n"
    body += "- No PDFs generated.\n- No images generated.\n- No chatbot runtimes built.\n- No publication systems built.\n- No frontend experiences built.\n- No rendering runtimes optimized.\n"
    return body


# ---------------------------------------------------------------------------
# Reports

def reports() -> list[tuple[str, dict]]:
    return [
        ("01-lifecycle-model-summary.json", {
            "stages": LIFECYCLE_STAGES,
            "transition_count": len(LIFECYCLE_TRANSITIONS),
            "terminal_stages": [s["id"] for s in LIFECYCLE_STAGES if s["terminal"]],
        }),
        ("02-semantic-promotion-summary.json", {
            "levels": PROMOTION_LEVELS,
            "criteria": PROMOTION_CRITERIA,
            "authorities": PROMOTION_AUTHORITIES,
        }),
        ("03-deprecation-governance-summary.json", {
            "reasons": DEPRECATION_REASONS,
            "rules": DEPRECATION_RULES,
        }),
        ("04-versioning-governance-summary.json", {
            "axes": VERSIONED_AXES,
            "rules": VERSION_RULES,
        }),
        ("05-knowledge-health-summary.json", {
            "indicators": HEALTH_INDICATORS,
            "thresholds": HEALTH_THRESHOLDS,
            "critical_indicator_ids": [h["id"] for h in HEALTH_INDICATORS if h["severity"] == "critical"],
        }),
        ("06-review-governance-summary.json", {
            "checkpoints": REVIEW_CHECKPOINTS,
            "rules": REVIEW_RULES,
        }),
        ("07-change-impact-summary.json", {
            "targets": IMPACT_TARGETS,
            "rules": IMPACT_RULES,
            "procedure": IMPACT_PROCEDURE,
        }),
        ("08-knowledge-debt-summary.json", {
            "classes": DEBT_CLASSES,
            "blocking_classes": [d["id"] for d in DEBT_CLASSES if d["blocking"]],
            "rules": DEBT_RULES,
        }),
        ("09-long-term-architecture-summary.json", {
            "principles": ARCHITECTURE_PRINCIPLES,
            "new_product_integration": NEW_PRODUCT_INTEGRATION_STEPS,
            "layer_subordination": LAYER_SUBORDINATION,
            "products_in_scope": PRODUCTS,
        }),
        ("10-future-evolution-readiness.json", {
            "consumers": FUTURE_CONSUMERS,
            "non_negotiables": NON_NEGOTIABLES,
            "hard_exclusions": [
                "no-pdf-generation", "no-image-generation", "no-chatbot-runtime",
                "no-publication-system", "no-frontend-experience", "no-render-optimization",
            ],
        }),
    ]


# ---------------------------------------------------------------------------
# Main

def main() -> None:
    LG.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    _write(LG / "README.md", doc_readme())
    _write(LG / "00-charter.md", doc_charter())
    _write_json(LG / "00-charter.json", {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS})

    sections = [
        ("knowledge-lifecycle", doc_lifecycle, {"stages": LIFECYCLE_STAGES, "transitions": LIFECYCLE_TRANSITIONS}),
        ("promotion-governance", doc_promotion, {"levels": PROMOTION_LEVELS, "criteria": PROMOTION_CRITERIA, "authorities": PROMOTION_AUTHORITIES}),
        ("deprecation-governance", doc_deprecation, {"reasons": DEPRECATION_REASONS, "rules": DEPRECATION_RULES}),
        ("version-governance", doc_version, {"axes": VERSIONED_AXES, "rules": VERSION_RULES}),
        ("knowledge-health", doc_health, {"indicators": HEALTH_INDICATORS, "thresholds": HEALTH_THRESHOLDS}),
        ("review-governance", doc_review, {"checkpoints": REVIEW_CHECKPOINTS, "rules": REVIEW_RULES}),
        ("change-impact", doc_impact, {"targets": IMPACT_TARGETS, "rules": IMPACT_RULES, "procedure": IMPACT_PROCEDURE}),
        ("knowledge-debt", doc_debt, {"classes": DEBT_CLASSES, "rules": DEBT_RULES}),
        ("long-term-architecture", doc_architecture, {
            "principles": ARCHITECTURE_PRINCIPLES,
            "new_product_integration": NEW_PRODUCT_INTEGRATION_STEPS,
            "layer_subordination": LAYER_SUBORDINATION,
        }),
        ("future-readiness", doc_future, {"consumers": FUTURE_CONSUMERS, "non_negotiables": NON_NEGOTIABLES}),
    ]

    for slug, doc_fn, payload in sections:
        folder = LG / slug
        _write(folder / f"{slug}.md", doc_fn())
        _write_json(folder / f"{slug}.json", payload)

    for filename, payload in reports():
        _write_json(REPORTS / filename, payload)

    print("Lifecycle governance modeling complete.")
    print(f"  Constitutional root: {LG.relative_to(REPO)}")
    print(f"  Reports:             {REPORTS.relative_to(REPO)}/01..10")


if __name__ == "__main__":
    main()
