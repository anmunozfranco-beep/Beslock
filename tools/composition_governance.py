"""Phase 14 — Knowledge Composition & Operational Assembly.

Idempotent, non-destructive, modeling-only. Builds the eighth constitutional
layer `COMPOSITION_GOVERNANCE` and 10 numbered reports.

Hard rules honored:
  * NEVER modifies per-product knowledge-core/* files
  * NEVER modifies prior governance layers
  * NEVER builds PDFs, images, chatbots, frontends, renderers, Comfy orchestration
  * Modeling-only. Defines HOW knowledge is composed into operational assemblies.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
USER_MANUALS = REPO / "wp-content" / "themes" / "beslock-custom" / "User manuals"
KB = USER_MANUALS / "KNOWLEDGE_BUILDING"
CG = KB / "COMPOSITION_GOVERNANCE"
REPORTS = USER_MANUALS / "_repository-governance" / "reports" / "composition"

SCHEMA = "composition-governance/1.0"
TODAY = date.today().isoformat()

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

# ---------------------------------------------------------------------------
# 1. Composition primitives & operational packages

PRIMITIVES = [
    "entity", "procedure", "workflow", "warning", "terminology", "capability",
    "specification", "troubleshooting-symptom", "procedural-semantics",
    "visual-intent", "visual-risk", "publication-intent", "component-visibility",
    "provenance", "guidance-trigger", "cognitive-load-assessment", "priority-assignment",
]

OPERATIONAL_PACKAGES = [
    {"id": "installation-package",     "purpose": "physical install end-to-end",          "primitives": ["procedure(install/*)", "warning", "specification", "visual-intent(physical-installation)", "component-visibility", "provenance"]},
    {"id": "onboarding-package",       "purpose": "audience-scoped first-use flow",        "primitives": ["workflow", "procedural-semantics", "warning", "guidance-trigger", "cognitive-load-assessment", "terminology", "provenance"]},
    {"id": "troubleshooting-package",  "purpose": "symptom -> recovery path",              "primitives": ["troubleshooting-symptom", "warning", "procedure", "escalation-tier", "safety-constraint", "provenance"]},
    {"id": "administrator-setup-package","purpose": "admin enrolment + policy setup",      "primitives": ["workflow(administrator-setup)", "procedure(user-enrolment)", "capability", "warning", "provenance"]},
    {"id": "maintenance-package",      "purpose": "battery + routine maintenance",         "primitives": ["procedure(battery-replacement)", "warning", "specification", "visual-intent", "provenance"]},
    {"id": "recovery-package",         "purpose": "factory-reset / emergency-power",       "primitives": ["procedure(factory-reset)", "procedure(emergency-power)", "warning", "guidance-trigger(hard-interrupt)", "provenance"]},
]

COMPOSITION_RULES = [
    "Every package declares: id, purpose, primitives, source_artifact_ids, maturity_floor, audience_scope, channel_targets.",
    "Packages are reproducible from per-product knowledge-core; no orphan content allowed.",
    "Packages compose primitives by reference (id), never by inlined copy of mutable content.",
    "Provenance from every primitive flows into the package; provenance-stripped packages are forbidden.",
    "Packages MUST honour all access-governance filters (maturity, deprecation, unresolved-isolation).",
]

# ---------------------------------------------------------------------------
# 2. Operational assembly rules

ASSEMBLY_RULES = [
    {"id": "warnings-follow-procedures",        "rule": "Every procedure assembled into a package MUST carry the warnings scoped to it."},
    {"id": "prerequisites-are-transitive",      "rule": "Prerequisites expand transitively up to depth 3; circular dependencies are blocking findings."},
    {"id": "visual-attached-when-physical",     "rule": "Procedures with `surface=physical-installation` MUST attach visual-intent + component-visibility."},
    {"id": "troubleshooting-pulls-recovery",    "rule": "Troubleshooting symptoms MUST resolve to ≥1 recovery procedure or an explicit escalation tier."},
    {"id": "onboarding-pulls-guidance",         "rule": "Onboarding assemblies MUST attach guidance-triggers and a cognitive-load assessment per included procedure."},
    {"id": "guidance-respects-budget",          "rule": "Onboarding interruption budget ≤ 2 hard-interrupting triggers per session."},
    {"id": "safety-constraints-non-droppable",  "rule": "Safety-critical warnings (P0) cannot be dropped from any assembly that contains the related procedure."},
    {"id": "maturity-floor-enforced",           "rule": "Default maturity floor `normalized`; publication packages `verified`; RAG-bound packages `canonical-knowledge`."},
    {"id": "deterministic-order",               "rule": "Assembly ordering is deterministic: declared step-index first, then priority tier, then artifact-id."},
]

# ---------------------------------------------------------------------------
# 3. Contextual composition

COMPOSITION_DIMENSIONS = [
    {"id": "user-role",            "values": ["beginner", "installer", "administrator", "support-tier", "maintenance-operator", "advanced"]},
    {"id": "operational-stage",    "values": ["pre-install", "install", "first-use", "routine-operation", "maintenance", "recovery"]},
    {"id": "product-state",        "values": ["unconfigured", "paired-app", "admin-set", "users-enrolled", "low-battery", "lockout", "factory-default"]},
    {"id": "troubleshooting-state","values": ["nominal", "symptom-observed", "tier1-active", "tier3-escalated", "vendor-escalated"]},
    {"id": "onboarding-progress",  "values": ["not-started", "in-progress", "completed", "abandoned"]},
    {"id": "confidence-level",     "values": ["low", "medium", "high"]},
    {"id": "maturity-level",       "values": ["normalized", "canonicalized", "verified", "promoted"]},
]

CONTEXTUAL_PROFILES = [
    {"id": "beginner-installer",       "user_role": "installer",  "operational_stage": "install",    "package": "installation-package",      "filters": {"audience_scope": "installer", "maturity_floor": "normalized"}},
    {"id": "first-time-end-user",      "user_role": "beginner",   "operational_stage": "first-use",  "package": "onboarding-package",        "filters": {"audience_scope": "beginner",  "interruption_budget": 2}},
    {"id": "administrator-setup",      "user_role": "administrator","operational_stage": "first-use","package": "administrator-setup-package","filters": {"audience_scope": "administrator"}},
    {"id": "maintenance-operator",     "user_role": "maintenance-operator","operational_stage": "maintenance","package": "maintenance-package","filters": {"audience_scope": "maintenance"}},
    {"id": "support-tier-troubleshoot","user_role": "support-tier","operational_stage": "recovery",   "package": "troubleshooting-package",   "filters": {"audience_scope": "troubleshooting", "maturity_floor": "verified"}},
    {"id": "emergency-recovery",       "user_role": "beginner",   "operational_stage": "recovery",   "package": "recovery-package",          "filters": {"audience_scope": "maintenance",   "guidance_intensity": "hard-interrupt"}},
]

CONTEXTUAL_RULES = [
    "Composition profile = (user_role, operational_stage, product_state, confidence_level, maturity_level).",
    "Missing dimensions default to most restrictive: beginner / pre-install / unconfigured / low / verified.",
    "Confidence-level=low forces an explicit confidence-warning attached to the assembled package.",
    "Maturity-level upgrades narrow the candidate set; downgrades require an audit reason.",
    "Composition is recomputed when any dimension changes; no stale composition surfaces.",
]

# ---------------------------------------------------------------------------
# 4. Capability-based assembly

CAPABILITIES = [
    {"id": "fingerprint-management",   "primitives_query": "entities=fingerprint-sensor + procedures matching enrol/delete fingerprint + warnings scoped to fingerprint"},
    {"id": "app-pairing",              "primitives_query": "workflows surface=mobile-app + terminology(2.4G, TUYA APP) + warnings(network)"},
    {"id": "remote-unlock",            "primitives_query": "capability(remote-unlock) + procedures + warnings + connectivity-prereqs"},
    {"id": "emergency-recovery",       "primitives_query": "procedures(factory-reset, emergency-power) + warnings(safety-critical) + guidance-trigger(hard-interrupt)"},
    {"id": "battery-management",       "primitives_query": "procedures(battery-replacement) + warnings(low-battery) + specifications(battery)"},
    {"id": "administrator-control",    "primitives_query": "workflows(administrator-setup, user-enrolment) + capability(admin) + warnings(privilege)"},
]

CAPABILITY_RULES = [
    "Capability assemblies are document-agnostic; they query the knowledge-core by semantic predicate, not by source file.",
    "A capability assembly MUST resolve in every product where the capability is declared; absent capabilities are reported as gaps.",
    "Capability assemblies attach the union of warnings, prerequisites, and visual references across constituent primitives.",
    "Capability ids are stable across products; per-product specialisation lives in the knowledge-core, not in the capability id.",
]

# ---------------------------------------------------------------------------
# 5. Troubleshooting composition

TROUBLESHOOTING_INPUTS = ["symptom-category", "observed-state", "product-state", "user-role", "audience-scope"]

TROUBLESHOOTING_OUTPUTS = [
    "matched-symptom (or unresolved-symptom)",
    "tier-assignment (0..5)",
    "recovery-procedure-set",
    "warnings-injected",
    "safety-constraints-attached",
    "escalation-path",
    "provenance-bundle",
]

TROUBLESHOOTING_RULES = [
    "If symptom does not match the corpus, return unresolved-symptom + escalation to tier-4 (vendor) — never fabricate a recovery.",
    "Recovery procedures attached MUST be at maturity ≥ verified for safety-critical tiers.",
    "Tier escalation is monotonic: a single trace cannot oscillate down a tier.",
    "Safety constraints (P0 warnings) are always attached; consumers cannot suppress them.",
]

# ---------------------------------------------------------------------------
# 6. Onboarding composition

ONBOARDING_FLOWS = [
    {"id": "first-time-user",     "always_on": True,  "audience_scope": "beginner",       "package": "onboarding-package",         "interruption_budget": 2},
    {"id": "installer-onboarding","always_on": False, "audience_scope": "installer",      "package": "installation-package",       "interruption_budget": 2},
    {"id": "administrator-onboarding","always_on": False,"audience_scope": "administrator","package": "administrator-setup-package","interruption_budget": 1},
    {"id": "app-onboarding",      "always_on": False, "audience_scope": "beginner",       "package": "onboarding-package",         "interruption_budget": 2,
     "scope": "mobile-app workflows only"},
    {"id": "safe-operational-activation","always_on": True,"audience_scope": "beginner",  "package": "onboarding-package",         "interruption_budget": 2,
     "non_skippable": True},
]

ONBOARDING_RULES = [
    "Always-on flows are non-skippable; their inclusion is enforced by the composition layer, not the consumer.",
    "Interruption budget is hard-capped per session; exceeding it is a composition error.",
    "Onboarding flows compose with cognitive-load-map; very-high-load procedures MUST chunk + confirm.",
    "Audience scope is enforced; mismatched audience composition is rejected.",
]

# ---------------------------------------------------------------------------
# 7. Publication-neutral assemblies

NEUTRALITY_RULES = [
    "Assemblies declare content + ordering + dependencies; never fonts, layouts, colours, page sizes.",
    "Assemblies do not embed binary media; they reference media descriptors via visual-intent.",
    "Assemblies do not embed UI components, widgets, scripts, or chatbot prompts.",
    "Assemblies do not embed channel-specific transformations (PDF page breaks, web heading levels, etc.).",
    "Channel adaptation is the responsibility of downstream renderers; the assembly remains canonical.",
]

PROHIBITED_INLINE = [
    "PDF page-break directives", "HTML/CSS markup", "JavaScript", "chatbot prompt templates",
    "image binaries", "font files", "layout grids", "render-time hints",
]

# ---------------------------------------------------------------------------
# 8. Composition governance

CHARTER_PRINCIPLES = [
    "Composition assembles; it does not author.",
    "Every assembly is reproducible from the knowledge-core snapshot.",
    "Composition is publication-neutral; rendering lives elsewhere.",
    "Safety constraints are non-droppable; provenance is non-strippable.",
    "Determinism is a contract: same dimensions + same snapshot ⇒ same assembly.",
    "Capability assemblies are document-agnostic; they query by semantic predicate.",
    "Composition is subordinate to knowledge-core, lifecycle, validation, access governance.",
    "Future composition consumers inherit composition contracts; contracts never bend to satisfy a consumer.",
]

AUTHORITY_AREAS = [
    "knowledge-composition", "assembly-rules", "contextual-composition",
    "capability-composition", "troubleshooting-composition", "onboarding-composition",
    "publication-neutral-assemblies", "composition-governance",
    "composition-risks", "future-composition-readiness",
]

# ---------------------------------------------------------------------------
# 9. Unresolved composition risks (qualitative; reference prior reports)

COMPOSITION_RISKS = [
    {"id": "thin-troubleshooting-corpus",  "severity": "high",   "description": "5/6 products lack troubleshooting symptoms; troubleshooting-package only assembles for e-shield.", "ref": "validation/02-workflow-executability.json"},
    {"id": "warning-corpus-gap",           "severity": "high",   "description": "2 products have empty warning corpora; warnings-follow-procedures rule cannot fire.",             "ref": "validation/05-experience-validation.json"},
    {"id": "channel-targets-coverage",     "severity": "high",   "description": "417 artifacts missing channel_targets; package channel-binding under-determined.",                "ref": "validation/06-retrieval-validation.json"},
    {"id": "capability-not-declared-per-product","severity": "medium","description": "Capability assemblies (e.g. fingerprint-management) cannot resolve where capability is undeclared per product."},
    {"id": "audience-scope-not-authored",  "severity": "medium", "description": "Per-artifact audience_scope assignments not yet authored; contextual composition relies on heuristics."},
    {"id": "snapshot-hash-not-emitted",    "severity": "medium", "description": "Determinism contract requires knowledge-core snapshot hash on every assembly; not yet integrated."},
    {"id": "circular-prerequisite-detection","severity": "low",  "description": "Cycle detection at composition time depends on graph-validation passing; currently 0 cycles, but contract must remain enforced."},
    {"id": "shared-concepts-undeclared",   "severity": "high",   "description": "15 cross-product entity-collisions + 10 terminology-collisions block cross-product capability composition."},
]

# ---------------------------------------------------------------------------
# 10. Future composition readiness

FUTURE_CONSUMERS = [
    {"system": "adaptive-onboarding",     "consumes": ["onboarding-package", "contextual-composition"], "readiness_gate": "audience_scope authored per artifact"},
    {"system": "contextual-assistant",    "consumes": ["all packages", "contextual-composition"],       "readiness_gate": "snapshot-hash on bundles + access-trace logging"},
    {"system": "dynamic-manuals",         "consumes": ["installation-package", "publication-package"],  "readiness_gate": "maturity ≥ verified for included primitives"},
    {"system": "troubleshooting-systems", "consumes": ["troubleshooting-package"],                       "readiness_gate": "symptom corpus ≥ 10 per product"},
    {"system": "semantic-publication",    "consumes": ["publication-bundle (access layer)"],             "readiness_gate": "publication-neutral rules enforced + deprecation badges defined"},
    {"system": "multimodal-assistance",   "consumes": ["packages with visual-intent attached"],          "readiness_gate": "visual-risk classified + component-visibility declared"},
    {"system": "future-visual-assistance","consumes": ["visual-intent + visual-risk + component-visibility"], "readiness_gate": "visual-risk reclassification freeze window in place"},
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


def _table(rows: list[dict], cols: list[str]) -> str:
    out = "| " + " | ".join(cols) + " |\n"
    out += "|" + "|".join("---" for _ in cols) + "|\n"
    for r in rows:
        out += "| " + " | ".join(_cell(r.get(c, "")) for c in cols) + " |\n"
    return out


def _cell(v) -> str:
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    if isinstance(v, dict):
        return ", ".join(f"{k}={v2}" for k, v2 in v.items())
    return str(v) if v is not None else ""


def doc_readme() -> str:
    return f"""# COMPOSITION_GOVERNANCE

Constitutional layer governing **dynamic knowledge composition** and
**operational assembly** across the Beslock knowledge center.

- Schema: `{SCHEMA}`
- Generated: {TODAY}
- Subordinate to: `knowledge-core`, `LIFECYCLE_GOVERNANCE`, `VALIDATION_GOVERNANCE`, `ACCESS_AND_CONSUMPTION_GOVERNANCE`

This layer **does not implement** PDFs, frontends, chatbots, renderers, or
Comfy orchestration. It defines how semantic primitives are composed into
reusable, contextual, publication-neutral operational assemblies.

## Authority areas
{chr(10).join(f"- {a}" for a in AUTHORITY_AREAS)}

## Doctrine layout
- `00-charter.md`
- `knowledge-composition/`
- `assembly-rules/`
- `contextual-composition/`
- `capability-composition/`
- `troubleshooting-composition/`
- `onboarding-composition/`
- `publication-neutral-assemblies/`
- `composition-governance/`
- `composition-risks/`
- `future-composition-readiness/`

Reports: `_repository-governance/reports/composition/01..10`.
"""


def doc_charter() -> str:
    body = "# 00 — Composition Governance Charter\n\n## Principles\n"
    for i, p in enumerate(CHARTER_PRINCIPLES, 1):
        body += f"{i}. {p}\n"
    body += "\n## Authority areas\n" + "\n".join(f"- {a}" for a in AUTHORITY_AREAS)
    body += "\n\n## Hard guarantees\n"
    body += "- Modeling-only. Builds no PDFs, images, chatbots, frontends, renderers, Comfy orchestration.\n"
    body += "- Read-only. Mutates no per-product knowledge.\n"
    body += "- Subordinate. Cannot override knowledge-core, lifecycle, validation, or access governance.\n"
    body += "- Deterministic. Same dimensions + same snapshot => same assembly.\n"
    return body


# ---------------------------------------------------------------------------
# Main

def main() -> None:
    CG.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    _write(CG / "README.md", doc_readme())
    _write(CG / "00-charter.md", doc_charter())
    _write_json(CG / "00-charter.json", {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS})

    sections = [
        ("knowledge-composition",
         "# Knowledge Composition\n\n## Primitives\n\n" + "\n".join(f"- {p}" for p in PRIMITIVES)
         + "\n\n## Operational packages\n\n" + _table(OPERATIONAL_PACKAGES, ["id", "purpose", "primitives"])
         + "\n## Rules\n\n" + "\n".join(f"- {r}" for r in COMPOSITION_RULES) + "\n",
         {"primitives": PRIMITIVES, "operational_packages": OPERATIONAL_PACKAGES, "rules": COMPOSITION_RULES}),
        ("assembly-rules",
         "# Operational Assembly Rules\n\n" + _table(ASSEMBLY_RULES, ["id", "rule"]),
         {"rules": ASSEMBLY_RULES}),
        ("contextual-composition",
         "# Contextual Composition\n\n## Dimensions\n\n" + _table(COMPOSITION_DIMENSIONS, ["id", "values"])
         + "\n## Profiles\n\n" + _table(CONTEXTUAL_PROFILES, ["id", "user_role", "operational_stage", "package", "filters"])
         + "\n## Rules\n\n" + "\n".join(f"- {r}" for r in CONTEXTUAL_RULES) + "\n",
         {"dimensions": COMPOSITION_DIMENSIONS, "profiles": CONTEXTUAL_PROFILES, "rules": CONTEXTUAL_RULES}),
        ("capability-composition",
         "# Capability-Based Assembly\n\n" + _table(CAPABILITIES, ["id", "primitives_query"])
         + "\n## Rules\n\n" + "\n".join(f"- {r}" for r in CAPABILITY_RULES) + "\n",
         {"capabilities": CAPABILITIES, "rules": CAPABILITY_RULES}),
        ("troubleshooting-composition",
         "# Troubleshooting Composition\n\n## Inputs\n\n" + "\n".join(f"- {i}" for i in TROUBLESHOOTING_INPUTS)
         + "\n\n## Outputs\n\n" + "\n".join(f"- {o}" for o in TROUBLESHOOTING_OUTPUTS)
         + "\n\n## Rules\n\n" + "\n".join(f"- {r}" for r in TROUBLESHOOTING_RULES) + "\n",
         {"inputs": TROUBLESHOOTING_INPUTS, "outputs": TROUBLESHOOTING_OUTPUTS, "rules": TROUBLESHOOTING_RULES}),
        ("onboarding-composition",
         "# Onboarding Composition\n\n" + _table(ONBOARDING_FLOWS, ["id", "always_on", "audience_scope", "package", "interruption_budget"])
         + "\n## Rules\n\n" + "\n".join(f"- {r}" for r in ONBOARDING_RULES) + "\n",
         {"flows": ONBOARDING_FLOWS, "rules": ONBOARDING_RULES}),
        ("publication-neutral-assemblies",
         "# Publication-Neutral Assemblies\n\n## Rules\n\n" + "\n".join(f"- {r}" for r in NEUTRALITY_RULES)
         + "\n\n## Prohibited inline content\n\n" + "\n".join(f"- {p}" for p in PROHIBITED_INLINE) + "\n",
         {"rules": NEUTRALITY_RULES, "prohibited_inline": PROHIBITED_INLINE}),
        ("composition-governance",
         doc_charter(),
         {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS}),
        ("composition-risks",
         "# Unresolved Composition Risks\n\n" + _table(COMPOSITION_RISKS, ["id", "severity", "description", "ref"]),
         {"risks": COMPOSITION_RISKS}),
        ("future-composition-readiness",
         "# Future Composition Readiness\n\n" + _table(FUTURE_CONSUMERS, ["system", "consumes", "readiness_gate"]),
         {"consumers": FUTURE_CONSUMERS}),
    ]

    for slug, md_text, payload in sections:
        folder = CG / slug
        folder.mkdir(parents=True, exist_ok=True)
        _write(folder / f"{slug}.md", md_text)
        _write_json(folder / f"{slug}.json", payload)

    reports = [
        ("01-knowledge-composition-summary.json",  {"primitives": PRIMITIVES, "operational_packages": OPERATIONAL_PACKAGES, "rules": COMPOSITION_RULES}),
        ("02-operational-assembly-summary.json",   {"rules": ASSEMBLY_RULES}),
        ("03-contextual-composition-summary.json", {"dimensions": COMPOSITION_DIMENSIONS, "profiles": CONTEXTUAL_PROFILES, "rules": CONTEXTUAL_RULES}),
        ("04-capability-composition-summary.json", {"capabilities": CAPABILITIES, "rules": CAPABILITY_RULES}),
        ("05-troubleshooting-composition-summary.json", {"inputs": TROUBLESHOOTING_INPUTS, "outputs": TROUBLESHOOTING_OUTPUTS, "rules": TROUBLESHOOTING_RULES}),
        ("06-onboarding-composition-summary.json", {"flows": ONBOARDING_FLOWS, "rules": ONBOARDING_RULES}),
        ("07-publication-neutral-summary.json",    {"rules": NEUTRALITY_RULES, "prohibited_inline": PROHIBITED_INLINE}),
        ("08-composition-governance-summary.json", {"principles": CHARTER_PRINCIPLES, "authority_areas": AUTHORITY_AREAS}),
        ("09-unresolved-composition-risks.json",   {"risks": COMPOSITION_RISKS}),
        ("10-future-composition-readiness.json",   {"consumers": FUTURE_CONSUMERS, "products_in_scope": PRODUCTS}),
    ]
    for name, payload in reports:
        _write_json(REPORTS / name, payload)

    print("Composition modeling complete.")
    print(f"  Constitutional root: {CG.relative_to(REPO)}")
    print(f"  Reports:             {REPORTS.relative_to(REPO)}/01..10")


if __name__ == "__main__":
    main()
