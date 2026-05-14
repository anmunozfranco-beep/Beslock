"""Phase 13 — Knowledge Access & Consumption Architecture.

Idempotent, non-destructive, modeling-only. Builds the seventh constitutional
layer `ACCESS_AND_CONSUMPTION_GOVERNANCE` and 10 numbered reports.

Hard rules honored:
  * NEVER modifies per-product knowledge-core/* files
  * NEVER modifies prior governance layers
  * NEVER builds chatbots, APIs, frontends, PDFs, images, rendering systems
  * Modeling-only — defines HOW knowledge is exposed, assembled, queried, consumed.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content" / "themes" / "beslock-custom" / "User manuals"
KB = USER_MANUALS / "KNOWLEDGE_BUILDING"
AC = KB / "ACCESS_AND_CONSUMPTION_GOVERNANCE"
REPORTS = USER_MANUALS / "_repository-governance" / "reports" / "access-and-consumption"

SCHEMA = "access-and-consumption-governance/1.0"
TODAY = date.today().isoformat()

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

# ---------------------------------------------------------------------------
# 1. Knowledge access model

ACCESS_PATTERNS = [
    {"id": "by-id",                "applies_to": ["all"],                          "shape": "(product, artifact_id) -> artifact",                          "guarantees": ["deterministic", "lineage-attached"]},
    {"id": "by-domain",            "applies_to": ["all"],                          "shape": "(product, domain) -> [artifact]",                            "guarantees": ["domain-bounded", "ordered-by-priority"]},
    {"id": "by-entity",            "applies_to": ["entities"],                     "shape": "(product, entity_id) -> {entity, references_in}",            "guarantees": ["entity-graph-attached"]},
    {"id": "by-procedure",         "applies_to": ["procedures", "install", "operation"], "shape": "(product, procedure_id) -> {procedure, prerequisites, warnings}", "guarantees": ["prerequisite-expanded", "warning-injected"]},
    {"id": "by-workflow",          "applies_to": ["workflows"],                    "shape": "(product, workflow_id) -> {workflow, actors, steps, dependencies}", "guarantees": ["actor-resolved", "dependency-expanded"]},
    {"id": "by-warning",           "applies_to": ["warnings"],                     "shape": "(product, warning_id) -> {warning, scoped_procedures}",      "guarantees": ["scope-resolved"]},
    {"id": "by-troubleshooting",   "applies_to": ["troubleshooting"],              "shape": "(product, symptom) -> {tier, recovery_path, escalation}",    "guarantees": ["tier-aware", "escalation-attached"]},
    {"id": "by-onboarding",        "applies_to": ["workflows", "procedural-semantics"], "shape": "(product, audience) -> ordered onboarding bundle",      "guarantees": ["audience-scoped", "cognitive-load-aware"]},
    {"id": "by-visual-intent",     "applies_to": ["visual-intent", "visual-risk", "component-visibility"], "shape": "(product, surface) -> visual descriptor", "guarantees": ["risk-classified", "visibility-aware"]},
    {"id": "by-governance",        "applies_to": ["governance-doctrine"],          "shape": "(layer, area) -> doctrine document",                         "guarantees": ["revision-tagged"]},
    {"id": "by-provenance",        "applies_to": ["all"],                          "shape": "artifact -> {source_refs, extraction_lineage, version}",     "guarantees": ["read-only", "complete-lineage"]},
]

ACCESS_RULES = [
    "All access is read-only at this layer; no mutation surface is exposed.",
    "Every access response carries provenance; provenance-stripped responses are forbidden.",
    "Access by id is the canonical primitive; all other patterns reduce to it.",
    "Access is scoped by (product, layer, audience) — global queries fan out, never collapse.",
    "Access never returns deprecated artifacts without an explicit `include_deprecated=true` flag.",
    "Access never returns unresolved-stage artifacts without an explicit `include_unresolved=true` flag.",
]

# ---------------------------------------------------------------------------
# 2. Semantic query architecture

QUERY_INTENTS = [
    {"id": "how-to",            "examples": ["how to reset e-orbit", "how to enroll fingerprint"], "primary_targets": ["procedures", "workflows", "procedural-semantics"]},
    {"id": "what-is",           "examples": ["what is 2.4G", "what is admin mode"],                "primary_targets": ["terminology", "entities", "capabilities"]},
    {"id": "where-is",          "examples": ["where is the reset button"],                          "primary_targets": ["entities", "component-visibility", "visual-intent"]},
    {"id": "why-failure",       "examples": ["pairing failures", "why won't it unlock"],            "primary_targets": ["troubleshooting", "warnings"]},
    {"id": "prerequisite",      "examples": ["installation prerequisites", "what do I need before"], "primary_targets": ["workflows.preconditions", "procedural-semantics"]},
    {"id": "comparison",        "examples": ["e-orbit vs e-shield"],                                "primary_targets": ["capabilities", "specifications", "shared-concepts"]},
    {"id": "safety",            "examples": ["is it safe to factory reset"],                        "primary_targets": ["warnings", "visual-risk", "publication-intent"]},
    {"id": "lookup-id",         "examples": ["wf-alta-desde-tuya-app"],                             "primary_targets": ["by-id"]},
    {"id": "ambiguous",         "examples": ["app", "lock"],                                        "primary_targets": ["disambiguation-set"]},
]

QUERY_RESOLUTION = [
    "Detect intent class.",
    "Resolve product scope (explicit token, current session product, or fan-out across all products).",
    "Map intent to primary targets via QUERY_INTENTS.",
    "Apply access-governance filters (maturity, deprecation, unresolved).",
    "Assemble context bundle (see context-assembly).",
    "If zero results, escalate to fallback strategy.",
    "If multiple equal-confidence results, return disambiguation-set, never silently choose.",
]

QUERY_FALLBACKS = [
    "synonym expansion via terminology.oem_variants",
    "bilingual expansion via terminology.canonical/oem_variants",
    "domain-broaden (procedures -> workflows -> procedural-semantics)",
    "product-broaden (single -> shared-concepts -> all)",
    "explicit unresolved-knowledge response (never fabricate)",
]

AMBIGUITY_RULES = [
    "An ambiguous query MUST return a disambiguation-set, not a guess.",
    "Disambiguation-set entries carry: id, product, summary, maturity, confidence.",
    "Resolution chosen by the consumer is recorded in the access trace.",
]

# ---------------------------------------------------------------------------
# 3. Context assembly model

ASSEMBLY_PROFILES = [
    {"id": "procedural-context",     "core": "by-procedure",       "expands": ["prerequisites", "warnings", "referenced-entities", "visual-intent"], "filters": ["maturity ≥ normalized", "exclude deprecated"]},
    {"id": "troubleshooting-context","core": "by-troubleshooting", "expands": ["recovery-path", "escalation-tier", "related-warnings"],               "filters": ["maturity ≥ normalized", "include verified preferred"]},
    {"id": "onboarding-context",     "core": "by-onboarding",      "expands": ["learning-path", "guidance-triggers", "cognitive-load-map"],            "filters": ["audience-scoped", "interruption-budget ≤ 2"]},
    {"id": "publication-context",    "core": "by-domain",          "expands": ["publication-intent", "deprecation-badges", "lineage"],                 "filters": ["maturity ≥ verified", "exclude unresolved"]},
    {"id": "provenance-context",     "core": "by-provenance",      "expands": ["source_refs", "extraction_lineage", "version"],                        "filters": ["read-only"]},
]

ASSEMBLY_RULES = [
    "Every assembled context records: profile id, source artifact ids, applied filters, generation timestamp.",
    "Warnings scoped to a procedure MUST be injected into procedural-context.",
    "Prerequisites MUST be expanded transitively but capped at depth 3 to prevent runaway expansion.",
    "Maturity-aware filtering is mandatory; consumers cannot opt out of safety filters.",
    "Confidence-aware assembly: a context whose core artifact is `confidence=low` MUST emit a confidence-warning.",
    "Provenance-aware assembly: every included artifact carries its source_refs into the bundle.",
]

# ---------------------------------------------------------------------------
# 4. Knowledge packaging

PACKAGE_TYPES = [
    {"id": "operational-bundle",   "purpose": "single procedure with all dependencies", "shape": "{procedure, prerequisites, warnings, entities, visuals?}"},
    {"id": "workflow-bundle",      "purpose": "single workflow ready for sequencing",   "shape": "{workflow, actors, steps, dependencies, channel_targets}"},
    {"id": "troubleshooting-bundle","purpose": "symptom -> resolution path",             "shape": "{symptom, tier, steps, escalation}"},
    {"id": "onboarding-bundle",    "purpose": "ordered audience-scoped flow",            "shape": "{audience, ordered_artifacts, guidance_triggers}"},
    {"id": "publication-bundle",   "purpose": "publication-neutral artifact set",        "shape": "{publication_intent, ordered_artifacts, deprecation_badges, lineage}"},
    {"id": "retrieval-bundle",     "purpose": "RAG-safe semantic chunk",                 "shape": "{chunk_text, ids, provenance, channel_targets}"},
    {"id": "visual-bundle",        "purpose": "visual descriptors for future assistance","shape": "{visual_intent, visual_risk, component_visibility}"},
]

PACKAGING_RULES = [
    "Packages are publication-neutral: they describe content, never rendering.",
    "Every package declares: package_type, schema, generated_at, source_artifact_ids, maturity_floor.",
    "Packages MUST be reproducible from the per-product knowledge-core; no orphan content.",
    "Packages MUST NOT inline rendering instructions, fonts, layouts, or media binaries.",
    "Retrieval bundles MUST carry stable retrieval-safe ids and provenance for every chunk.",
]

# ---------------------------------------------------------------------------
# 5. Access governance

ACCESS_FILTERS = [
    {"id": "maturity-floor",       "default": "normalized",       "stricter_for": ["publication-bundle (verified)", "RAG (canonical-knowledge)"]},
    {"id": "deprecation-filter",   "default": "exclude",          "override": "include_deprecated=true (records audit reason)"},
    {"id": "unresolved-isolation", "default": "exclude",          "override": "include_unresolved=true (review-only surfaces)"},
    {"id": "low-confidence-veil",  "default": "include-with-warning", "stricter_for": ["safety-critical surfaces -> exclude"]},
    {"id": "provenance-required",  "default": "always",           "override": None},
    {"id": "audience-scope",       "default": "explicit",         "override": None},
]

ACCESS_GOVERNANCE_RULES = [
    "Default access is safe-by-default; unsafe surfaces require explicit opt-in flags + audit trace.",
    "Deprecated knowledge is accessible only via override; surfaces MUST render a deprecation badge.",
    "Unresolved knowledge is isolated; never surfaces in retrieval-bundle by default.",
    "Low-confidence artifacts surfaced to safety-critical consumers MUST be excluded, not just warned.",
    "Every access call is loggable; access traces feed back into knowledge-health monitoring.",
]

# ---------------------------------------------------------------------------
# 6. Operational context hierarchies

CONTEXT_HIERARCHIES = [
    {"id": "beginner",                 "audience": "first-time end-user",     "knowledge_scope": ["terminology", "warnings", "by-onboarding (safe-first-use)"], "exclude": ["admin-procedures", "advanced-configuration"]},
    {"id": "installer",                "audience": "physical installer",      "knowledge_scope": ["install", "warnings", "visual-intent (physical-installation)", "specifications"], "exclude": ["app-onboarding", "advanced-configuration"]},
    {"id": "administrator",            "audience": "lock administrator",      "knowledge_scope": ["administrator-setup", "user-enrolment", "operation", "workflows"], "exclude": ["installer-only-procedures"]},
    {"id": "troubleshooting",          "audience": "support-tier responder",  "knowledge_scope": ["troubleshooting", "warnings", "procedural-semantics"], "exclude": ["onboarding-marketing-copy"]},
    {"id": "maintenance",              "audience": "owner / serviceperson",   "knowledge_scope": ["battery-replacement", "factory-reset-recovery", "warnings"], "exclude": ["initial-onboarding"]},
    {"id": "advanced-configuration",   "audience": "power-user / integrator", "knowledge_scope": ["all-promoted", "capabilities", "specifications"], "exclude": ["beginner-flows"]},
]

HIERARCHY_RULES = [
    "Audience scopes are declarative: an artifact may belong to multiple scopes, but inclusion is opt-in per artifact.",
    "Access calls without an audience scope default to the most restrictive (beginner).",
    "Hierarchy filters compose with access-governance filters; the stricter wins.",
    "Hierarchy assignment is a knowledge-center responsibility; access layer enforces, does not author.",
]

# ---------------------------------------------------------------------------
# 7. Machine consumption readiness

STABLE_SURFACES = [
    {"id": "artifact-id-surface",    "guarantee": "ids are stable across versions; supersession recorded via lineage"},
    {"id": "schema-surface",         "guarantee": "schemas are semver-versioned per LIFECYCLE_GOVERNANCE"},
    {"id": "provenance-surface",     "guarantee": "every artifact carries source_refs + extraction_lineage"},
    {"id": "context-bundle-surface", "guarantee": "deterministic given (profile, inputs, knowledge-core snapshot)"},
    {"id": "retrieval-chunk-surface","guarantee": "stable chunk ids; chunk content reproducible from canonical artifact"},
    {"id": "channel-target-surface", "guarantee": "channel_targets array declares opt-in surfaces (chatbot/rag/web/pdf/...)"},
]

DETERMINISTIC_CONSTRUCTION_RULES = [
    "Same inputs + same knowledge-core snapshot => byte-identical context bundle.",
    "Bundle generation records knowledge-core snapshot hash (future: integrate with lifecycle versioning).",
    "Non-deterministic enrichments (e.g. ML embeddings) live OUTSIDE the access layer.",
    "Lineage-safe: a bundle re-issued after artifact supersession explicitly references the new version + records the previous bundle hash.",
]

CONSUMPTION_GATES = [
    {"consumer": "RAG",                       "requires": ["maturity ≥ canonical", "lineage-break tolerance = 0", "channel_targets includes 'rag'"]},
    {"consumer": "semantic-API",              "requires": ["stable artifact-ids", "schema-surface pinned", "access-trace logging"]},
    {"consumer": "vector-retrieval",          "requires": ["retrieval-chunk-surface", "deterministic chunk boundaries", "provenance per chunk"]},
    {"consumer": "contextual-assistant",      "requires": ["context-bundle-surface", "audience-scope mandatory", "warning-injection enforced"]},
    {"consumer": "multimodal-system",         "requires": ["visual-bundle available", "visual-risk classified", "component-visibility declared"]},
    {"consumer": "adaptive-onboarding",       "requires": ["onboarding-bundle by audience", "cognitive-load-map present", "interruption budget honoured"]},
]

# ---------------------------------------------------------------------------
# 8. Delivery governance

CHARTER_PRINCIPLES = [
    "Access exposes; it does not transform meaning.",
    "Consumption is publication-neutral; rendering lives elsewhere.",
    "Every bundle carries provenance; provenance-stripped delivery is forbidden.",
    "Safety filters are non-negotiable defaults; opt-out requires audit trace.",
    "Determinism is a contract: same inputs, same snapshot, same bundle.",
    "Disambiguation is preferred over guessing; ambiguity surfaces, never hides.",
    "Access layer is subordinate to knowledge-core, lifecycle, and validation governance.",
    "Future systems inherit access contracts; access contracts never bend to satisfy a consumer.",
]

AUTHORITY_AREAS = [
    "knowledge-access", "semantic-query", "context-assembly", "knowledge-packaging",
    "access-governance", "context-hierarchies", "machine-consumption",
    "delivery-governance", "interoperability", "access-risks",
]

# ---------------------------------------------------------------------------
# 9. Interoperability

INTEROP_TARGETS = [
    {"system": "chatbot",              "consumes": ["retrieval-bundle", "context-assembly.troubleshooting", "context-assembly.procedural"], "guarantees_required": ["provenance per chunk", "disambiguation-set support"]},
    {"system": "onboarding",           "consumes": ["onboarding-bundle", "context-hierarchies.beginner|installer|administrator"],            "guarantees_required": ["cognitive-load-aware", "interruption budget"]},
    {"system": "troubleshooting",      "consumes": ["troubleshooting-bundle"],                                                                "guarantees_required": ["tier-aware escalation", "warning injection"]},
    {"system": "publication",          "consumes": ["publication-bundle"],                                                                   "guarantees_required": ["maturity ≥ verified", "deprecation badges"]},
    {"system": "visual-assistance",    "consumes": ["visual-bundle"],                                                                        "guarantees_required": ["visual-risk classified", "component-visibility declared"]},
    {"system": "multilingual",         "consumes": ["terminology by-domain", "context-assembly with language scope"],                        "guarantees_required": ["bilingual variants resolved", "shared-terminology declared"]},
]

INTEROP_INVARIANTS = [
    "provenance preserved across all interop boundaries",
    "governance preserved (no consumer overrides access-governance defaults silently)",
    "validation integrity preserved (consumers receive validation-passed artifacts only by default)",
    "ontology coherence preserved (cross-product collisions resolved before exposure)",
]

# ---------------------------------------------------------------------------
# 10. Unresolved access risks (qualitative — depends on prior validation)

ACCESS_RISKS = [
    {"id": "channel-targets-coverage-gap",  "severity": "high",   "description": "Many artifacts lack channel_targets; retrieval-bundle synthesis is constrained.", "ref": "validation/06-retrieval-validation.json"},
    {"id": "shared-concepts-undeclared",    "severity": "high",   "description": "Cross-product entity/terminology collisions detected without shared-concept registry; access fan-out cannot deduplicate.", "ref": "validation/03-entity-consistency.json"},
    {"id": "troubleshooting-corpus-thin",   "severity": "high",   "description": "5/6 products have no troubleshooting artifacts; troubleshooting-bundle synthesis blocked per product.", "ref": "validation/02-workflow-executability.json"},
    {"id": "warning-corpus-gap",            "severity": "high",   "description": "2 products have empty warning corpus; procedural-context warning-injection cannot fire.", "ref": "validation/05-experience-validation.json"},
    {"id": "maturity-floor-population",     "severity": "medium", "description": "Most artifacts are extraction-pending-review; canonical/verified pool is small (~7%); RAG gating excludes the majority."},
    {"id": "snapshot-hash-not-emitted",     "severity": "medium", "description": "Bundles do not yet carry knowledge-core snapshot hash; deterministic re-issue requires future lifecycle integration."},
    {"id": "audience-scope-not-declared",   "severity": "medium", "description": "Per-artifact audience-scope assignments are not yet authored; hierarchy filtering relies on heuristics."},
    {"id": "disambiguation-set-untested",   "severity": "low",    "description": "Disambiguation contract is declared but not exercised against a real query corpus."},
]

# ---------------------------------------------------------------------------
# Doc writers

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, payload: dict) -> None:
    payload = {"schema": SCHEMA, "generated": TODAY, **payload}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def doc_readme() -> str:
    return f"""# ACCESS_AND_CONSUMPTION_GOVERNANCE

Constitutional layer governing **how knowledge is exposed, assembled, queried,
and consumed** by future systems.

- Schema: `{SCHEMA}`
- Generated: {TODAY}
- Subordinate to: `knowledge-core`, `LIFECYCLE_GOVERNANCE`, `VALIDATION_GOVERNANCE`
- Coexists with: `VISUAL_GOVERNANCE`, `KNOWLEDGE_CENTER`, `SEMANTIC_GOVERNANCE`,
  `EXPERIENCE_GOVERNANCE`, `LIFECYCLE_GOVERNANCE`, `VALIDATION_GOVERNANCE`

This layer **does not implement** chatbots, APIs, frontends, PDFs, images, or
rendering systems. It defines the contracts those future systems must honour
to consume operational knowledge safely.

## Authority areas
{chr(10).join(f"- {a}" for a in AUTHORITY_AREAS)}

## Doctrine layout
- `00-charter.md` — principles + authority areas
- `knowledge-access/` — canonical access patterns
- `semantic-query/` — intents, resolution, fallback, ambiguity
- `context-assembly/` — assembly profiles & rules
- `knowledge-packaging/` — publication-neutral package types
- `access-governance/` — filters & rules
- `context-hierarchies/` — audience scopes
- `machine-consumption/` — stable surfaces & determinism
- `delivery-governance/` — charter & doctrine
- `interoperability/` — future-system contracts
- `access-risks/` — unresolved access risks (qualitative)

Reports: `_repository-governance/reports/access-and-consumption/01..10`.
"""


def doc_charter() -> str:
    body = "# 00 — Access & Consumption Charter\n\n## Principles\n"
    for i, p in enumerate(CHARTER_PRINCIPLES, 1):
        body += f"{i}. {p}\n"
    body += "\n## Authority areas\n"
    for a in AUTHORITY_AREAS:
        body += f"- {a}\n"
    body += "\n## Hard guarantees\n"
    body += "- Modeling-only. Builds no chatbots, APIs, frontends, PDFs, images, renderers.\n"
    body += "- Read-only at runtime. Mutates no per-product knowledge.\n"
    body += "- Subordinate. Cannot override knowledge-core, lifecycle, or validation.\n"
    body += "- Deterministic. Same inputs + snapshot => same bundle.\n"
    return body


def doc_table(title: str, rows: list[dict], cols: list[str]) -> str:
    body = f"# {title}\n\n"
    body += "| " + " | ".join(cols) + " |\n"
    body += "|" + "|".join("---" for _ in cols) + "|\n"
    for r in rows:
        body += "| " + " | ".join(_render_cell(r.get(c, "")) for c in cols) + " |\n"
    return body


def _render_cell(v) -> str:
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return str(v) if v is not None else ""


def doc_rules(title: str, rules: list[str]) -> str:
    body = f"# {title}\n\n"
    for r in rules:
        body += f"- {r}\n"
    return body


# ---------------------------------------------------------------------------
# Main

def main() -> None:
    AC.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    _write(AC / "README.md", doc_readme())
    _write(AC / "00-charter.md", doc_charter())
    _write_json(AC / "00-charter.json", {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS})

    sections = [
        ("knowledge-access", "Knowledge Access Patterns",
         doc_table("Knowledge Access Patterns", ACCESS_PATTERNS, ["id", "applies_to", "shape", "guarantees"])
         + "\n\n## Rules\n\n" + "\n".join(f"- {r}" for r in ACCESS_RULES) + "\n",
         {"patterns": ACCESS_PATTERNS, "rules": ACCESS_RULES}),
        ("semantic-query", "Semantic Query Architecture",
         doc_table("Semantic Query Intents", QUERY_INTENTS, ["id", "examples", "primary_targets"])
         + "\n\n## Resolution procedure\n\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(QUERY_RESOLUTION))
         + "\n\n## Fallbacks\n\n" + "\n".join(f"- {f}" for f in QUERY_FALLBACKS)
         + "\n\n## Ambiguity rules\n\n" + "\n".join(f"- {r}" for r in AMBIGUITY_RULES) + "\n",
         {"intents": QUERY_INTENTS, "resolution": QUERY_RESOLUTION, "fallbacks": QUERY_FALLBACKS, "ambiguity_rules": AMBIGUITY_RULES}),
        ("context-assembly", "Context Assembly Model",
         doc_table("Assembly Profiles", ASSEMBLY_PROFILES, ["id", "core", "expands", "filters"])
         + "\n\n## Rules\n\n" + "\n".join(f"- {r}" for r in ASSEMBLY_RULES) + "\n",
         {"profiles": ASSEMBLY_PROFILES, "rules": ASSEMBLY_RULES}),
        ("knowledge-packaging", "Knowledge Packaging",
         doc_table("Package Types", PACKAGE_TYPES, ["id", "purpose", "shape"])
         + "\n\n## Rules\n\n" + "\n".join(f"- {r}" for r in PACKAGING_RULES) + "\n",
         {"package_types": PACKAGE_TYPES, "rules": PACKAGING_RULES}),
        ("access-governance", "Access Governance",
         doc_table("Access Filters", ACCESS_FILTERS, ["id", "default", "stricter_for", "override"])
         + "\n\n## Rules\n\n" + "\n".join(f"- {r}" for r in ACCESS_GOVERNANCE_RULES) + "\n",
         {"filters": ACCESS_FILTERS, "rules": ACCESS_GOVERNANCE_RULES}),
        ("context-hierarchies", "Operational Context Hierarchies",
         doc_table("Hierarchies", CONTEXT_HIERARCHIES, ["id", "audience", "knowledge_scope", "exclude"])
         + "\n\n## Rules\n\n" + "\n".join(f"- {r}" for r in HIERARCHY_RULES) + "\n",
         {"hierarchies": CONTEXT_HIERARCHIES, "rules": HIERARCHY_RULES}),
        ("machine-consumption", "Machine Consumption Readiness",
         doc_table("Stable Surfaces", STABLE_SURFACES, ["id", "guarantee"])
         + "\n\n## Determinism rules\n\n" + "\n".join(f"- {r}" for r in DETERMINISTIC_CONSTRUCTION_RULES)
         + "\n\n## Consumption gates\n\n"
         + doc_table("", CONSUMPTION_GATES, ["consumer", "requires"]).split("\n", 2)[2],
         {"stable_surfaces": STABLE_SURFACES, "determinism_rules": DETERMINISTIC_CONSTRUCTION_RULES, "consumption_gates": CONSUMPTION_GATES}),
        ("delivery-governance", "Delivery Governance",
         doc_charter(),
         {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS}),
        ("interoperability", "Future System Interoperability",
         doc_table("Interop Targets", INTEROP_TARGETS, ["system", "consumes", "guarantees_required"])
         + "\n\n## Invariants\n\n" + "\n".join(f"- {i}" for i in INTEROP_INVARIANTS) + "\n",
         {"targets": INTEROP_TARGETS, "invariants": INTEROP_INVARIANTS}),
        ("access-risks", "Unresolved Access Risks",
         doc_table("Risks", ACCESS_RISKS, ["id", "severity", "description", "ref"]),
         {"risks": ACCESS_RISKS}),
    ]

    for slug, _title, md_text, payload in sections:
        folder = AC / slug
        folder.mkdir(parents=True, exist_ok=True)
        _write(folder / f"{slug}.md", md_text)
        _write_json(folder / f"{slug}.json", payload)

    # Reports (numbered)
    reports = [
        ("01-knowledge-access-summary.json",   {"patterns": ACCESS_PATTERNS, "rules": ACCESS_RULES}),
        ("02-semantic-query-summary.json",     {"intents": QUERY_INTENTS, "resolution": QUERY_RESOLUTION, "fallbacks": QUERY_FALLBACKS, "ambiguity_rules": AMBIGUITY_RULES}),
        ("03-context-assembly-summary.json",   {"profiles": ASSEMBLY_PROFILES, "rules": ASSEMBLY_RULES}),
        ("04-knowledge-packaging-summary.json",{"package_types": PACKAGE_TYPES, "rules": PACKAGING_RULES}),
        ("05-access-governance-summary.json",  {"filters": ACCESS_FILTERS, "rules": ACCESS_GOVERNANCE_RULES}),
        ("06-context-hierarchy-summary.json",  {"hierarchies": CONTEXT_HIERARCHIES, "rules": HIERARCHY_RULES}),
        ("07-machine-consumption-summary.json",{"stable_surfaces": STABLE_SURFACES, "determinism_rules": DETERMINISTIC_CONSTRUCTION_RULES, "consumption_gates": CONSUMPTION_GATES}),
        ("08-delivery-governance-summary.json",{"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS}),
        ("09-interoperability-summary.json",   {"targets": INTEROP_TARGETS, "invariants": INTEROP_INVARIANTS, "products_in_scope": PRODUCTS}),
        ("10-unresolved-access-risks.json",    {"risks": ACCESS_RISKS}),
    ]
    for name, payload in reports:
        _write_json(REPORTS / name, payload)

    print("Access & consumption modeling complete.")
    print(f"  Constitutional root: {AC.relative_to(REPO)}")
    print(f"  Reports:             {REPORTS.relative_to(REPO)}/01..10")


if __name__ == "__main__":
    main()
