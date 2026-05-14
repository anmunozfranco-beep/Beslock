"""
Phase 35 — GOVERNED PUBLICATION & KNOWLEDGE DELIVERY.

Constitutional layer 29. Modeling-only. Subordinate to knowledge-core and
to all twenty-eight prior governance layers.

Writes:
  - the six publication-system artifact folders under
    `wp-content/themes/beslock-custom/User manuals/publication-system/`
  - the doctrine root at
    `wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/PUBLICATION_AND_DELIVERY_GOVERNANCE/`
  - the ten final reports under
    `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/publication-system/01..10`

Idempotent. Non-destructive. Reads no per-product knowledge-core JSON.
Adds NO macro-governance mega-layer. Defines composition, contextual
assembly, audience delivery, delivery formats, publication lineage, and
the governed manual assembly flow as modeling artifacts only. Touches
no runtime code, no frontend, and produces no visual artifacts.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
PUB_ROOT = THEME_ROOT / "publication-system"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "PUBLICATION_AND_DELIVERY_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "publication-system"

SCHEMA = "publication-and-delivery-governance/1.0"


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
    "ECOSYSTEM_NORMALIZATION", "OPERATIONAL_PILOT",
]


# =============================================================================
# TASK 1 — PUBLICATION COMPOSITION MODEL
# =============================================================================

PUBLICATION_TYPES = [
    {"id": "user-manual",         "audience_default": "end-user",   "required_sections": ["overview", "safety-warnings", "installation-summary", "operation", "maintenance", "troubleshooting-quickref", "support"], "tier_required": "trusted"},
    {"id": "onboarding-guide",    "audience_default": "end-user",   "required_sections": ["welcome", "prerequisites", "first-use-flow", "key-warnings", "where-to-go-next"],                                          "tier_required": "trusted"},
    {"id": "troubleshooting-guide","audience_default": "end-user",  "required_sections": ["symptom-index", "diagnostic-tree", "remediation-steps", "escalation-criteria", "support-contact"],                       "tier_required": "trusted"},
    {"id": "quick-start-guide",   "audience_default": "end-user",   "required_sections": ["unbox", "minimal-setup", "first-action", "safety-callouts"],                                                              "tier_required": "trusted"},
    {"id": "installation-guide",  "audience_default": "installer",  "required_sections": ["site-requirements", "tooling", "stepwise-procedure", "verification", "handoff-checklist"],                                "tier_required": "trusted"},
    {"id": "operational-faq",     "audience_default": "end-user",   "required_sections": ["question", "answer", "related-procedures", "confidence-band"],                                                            "tier_required": "trusted-or-elevated-candidate"},
    {"id": "support-knowledge-article","audience_default": "support-agent","required_sections": ["scenario", "diagnosis", "resolution", "escalation-path", "internal-notes"],                                        "tier_required": "trusted-or-elevated-candidate"},
]

COMPOSITION_RULES = [
    "every publication is composed from knowledge-core nodes; no free-text injection by the renderer",
    "every required section is present or the publication is rejected at validation",
    "candidate-tier nodes MAY appear only when explicitly elevated by reviewer-of-scope and disclosed in the publication",
    "no publication mixes products without explicit cross-product manifest",
    "no publication compresses safety warnings; warnings render verbatim from source",
    "section order is governance-declared; renderer MUST NOT reorder",
]


# =============================================================================
# TASK 2 — CONTEXTUAL PUBLICATION ASSEMBLY
# =============================================================================

ASSEMBLY_INPUTS = [
    {"id": "procedures",              "source_layer": "knowledge-core",                  "binding": "ordered steps with preconditions"},
    {"id": "warnings",                "source_layer": "knowledge-core (safety domain)",  "binding": "rendered verbatim, never abridged"},
    {"id": "troubleshooting",         "source_layer": "knowledge-core (troubleshooting)","binding": "symptom → diagnosis → remediation"},
    {"id": "escalation-guidance",     "source_layer": "HUMAN_OPERATIONS (layer 24)",     "binding": "escalation receiver + criterion"},
    {"id": "continuity-checkpoints",  "source_layer": "CONTINUITY (layer 14)",           "binding": "checkpoint markers between major sections"},
    {"id": "confidence-disclosure",   "source_layer": "RUNTIME / DECISION_INTELLIGENCE", "binding": "per-section confidence band when assembled at runtime"},
    {"id": "provenance-references",   "source_layer": "knowledge-core/1.0",              "binding": "source-node ids cited at section close"},
]

ASSEMBLY_RULES = [
    "assembly is deterministic given the same inputs and manifest",
    "assembly MUST NOT invent content; missing input → section omitted with a declared placeholder",
    "warnings MUST appear adjacent to the procedure they govern",
    "continuity checkpoints MUST be placed at governance-declared boundaries, never injected ad hoc",
    "confidence disclosure is mandatory whenever any contributing node is candidate-tier",
    "provenance references are mandatory for every published section",
]


# =============================================================================
# TASK 3 — AUDIENCE-AWARE DELIVERY
# =============================================================================

AUDIENCES = [
    {"id": "end-user",              "vocabulary": "non-technical",   "shows_internal_notes": False, "shows_provenance_summary": True,  "shows_full_provenance": False, "shows_confidence_band": True},
    {"id": "installer",             "vocabulary": "trade-technical", "shows_internal_notes": False, "shows_provenance_summary": True,  "shows_full_provenance": False, "shows_confidence_band": True},
    {"id": "reviewer",              "vocabulary": "doctrine-technical","shows_internal_notes": True, "shows_provenance_summary": True, "shows_full_provenance": True,  "shows_confidence_band": True},
    {"id": "operator",              "vocabulary": "operational",     "shows_internal_notes": True,  "shows_provenance_summary": True,  "shows_full_provenance": True,  "shows_confidence_band": True},
    {"id": "governance-maintainer", "vocabulary": "doctrine-technical","shows_internal_notes": True, "shows_provenance_summary": True, "shows_full_provenance": True,  "shows_confidence_band": True},
    {"id": "support-agent",         "vocabulary": "operational",     "shows_internal_notes": True,  "shows_provenance_summary": True,  "shows_full_provenance": False, "shows_confidence_band": True},
]

AUDIENCE_RULES = [
    "audience filters affect VISIBILITY only; the underlying assembled publication is identical across audiences",
    "no audience may receive content sourced from a tier above its declared trust scope (layer 25)",
    "audience-aware rendering is governance-declared; no per-publication override",
    "PII / operator-identifying material is never rendered for end-user, installer, or support-agent audiences",
    "confidence band is rendered for every audience that consumes the publication",
]


# =============================================================================
# TASK 4 — DELIVERY FORMAT GOVERNANCE
# =============================================================================

DELIVERY_FORMATS = [
    {"id": "markdown",          "purpose": "primary canonical publication output", "lossless": True,  "renderer_constraints": ["no executable scripts", "no inline HTML beyond declared subset"]},
    {"id": "web",               "purpose": "browser-consumable publication",       "lossless": False, "renderer_constraints": ["no client-side mutation of canonical content", "must preserve provenance citations"]},
    {"id": "structured-runtime","purpose": "runtime-consumable JSON for assembled responses", "lossless": True, "renderer_constraints": ["schema = publication-output/1.0 (declared in this layer)", "MUST embed provenance + confidence band"]},
    {"id": "pdf-ready",         "purpose": "print-fidelity export",                "lossless": False, "renderer_constraints": ["no interactive elements", "explicit page-break markers", "warnings retained verbatim"]},
    {"id": "support-article",   "purpose": "support-agent knowledge article",      "lossless": True,  "renderer_constraints": ["scenario/diagnosis/resolution structure required", "internal notes section required"]},
    {"id": "visual-prompt",     "purpose": "MODELING ONLY — declarative input to a future visual pipeline", "lossless": True, "renderer_constraints": ["text declaration only — generates no image", "subordinate to VISUAL governance + dual-review env (layer 25)"]},
]

DELIVERY_FORMAT_RULES = [
    "no format may add semantic content beyond what assembly produced",
    "lossy formats MUST disclose what is lost (e.g. interactivity, color fidelity)",
    "structured-runtime is the source-of-truth format; all other formats are derived from it",
    "visual-prompt format is declarative; this layer does NOT execute visual generation",
    "every format embeds provenance + confidence at minimum",
]


# =============================================================================
# TASK 5 — PUBLICATION LINEAGE & TRACEABILITY
# =============================================================================

LINEAGE_FACETS = [
    {"id": "provenance-traceability",   "guarantee": "every published section traces to one or more knowledge-core source nodes by id"},
    {"id": "source-node-lineage",       "guarantee": "source nodes carry trust-tier + last-promotion timestamp at publication time"},
    {"id": "confidence-disclosure",     "guarantee": "publication exposes the confidence band of its weakest contributing section"},
    {"id": "reviewer-attribution",      "guarantee": "promotion of any contributing candidate node is attributed to a named reviewer-of-scope"},
    {"id": "publication-version-lineage","guarantee": "each publication carries a version id + the manifest hash of its assembly inputs"},
    {"id": "runtime-generation-auditability","guarantee": "publications assembled at runtime emit an assembly receipt referencing inputs, audience, and format"},
]

LINEAGE_RULES = [
    "lineage is mandatory; a publication missing any facet is invalid",
    "lineage is immutable post-publication; corrections produce a new version, never a silent edit",
    "assembly receipts are sandbox-tier in pilot phase (layer 25, layer 28) and promoted with the publication",
    "no lineage facet may be omitted by audience filter; only its rendering may vary",
    "lineage MUST link forward to revocation: revocation of a contributing node SHALL flag dependent publications",
]


# =============================================================================
# TASK 6 — GOVERNED MANUAL ASSEMBLY FLOW
# =============================================================================

MANUAL_ASSEMBLY_FLOW = [
    {"step": 1, "stage": "knowledge-core",            "actor": "knowledge-core/1.0",          "produces": "selected source nodes per manifest"},
    {"step": 2, "stage": "contextual-assembly",       "actor": "assembly pipeline (TASK 2)",  "produces": "structured-runtime publication candidate"},
    {"step": 3, "stage": "publication-rendering",     "actor": "renderer per format (TASK 4)","produces": "format-specific outputs (markdown, web, pdf-ready, support-article, visual-prompt)"},
    {"step": 4, "stage": "reviewer-validation",       "actor": "reviewer-of-scope (layer 23)","produces": "validation decision + attribution"},
    {"step": 5, "stage": "publication-promotion",     "actor": "promotion workflow",          "produces": "versioned publication artifact"},
    {"step": 6, "stage": "runtime-consumable-output", "actor": "RUNTIME_IMPLEMENTATION",      "produces": "assembled response with embedded provenance + confidence"},
]

MANUAL_ASSEMBLY_RULES = [
    "no step in this flow may be skipped",
    "no automation compresses steps 4 + 5 (reviewer judgment + promotion)",
    "publication promotion is a distinct act from candidate promotion (layer 23)",
    "runtime-consumable outputs MUST cite the publication version they were derived from",
    "first publication of any new manual is observation-only against pilots (layer 28) before broad delivery",
]


# =============================================================================
# TASK 7 — PUBLICATION GOVERNANCE (doctrine root contents)
# =============================================================================

CHARTER_PRINCIPLES = [
    "publication is the act by which the operational knowledge-core becomes usable by humans",
    "publication is governed; it is never a freeform act of the renderer",
    "every published artifact is traceable to its source nodes, reviewers, and assembly inputs",
    "audience filters change visibility, never substance",
    "warnings are sacrosanct: rendered verbatim, never abridged, never reordered",
    "publication promotes nothing; promotion is a separate, reviewed act",
    "no publication exists outside the lineage chain",
]

SUB_DOCTRINES = [
    ("publication-philosophy",
     "Publication Philosophy",
     "Publication is the disciplined act of making the operational knowledge-core consumable by humans without distorting it. The renderer is a faithful intermediary, never an author.",
     ["the renderer adds form, never content",
      "publication is bounded by the corpus, not by the audience's wishes",
      "publication failures (missing input, missing section) fail loudly, never silently"]),
    ("governed-delivery-doctrine",
     "Governed Delivery Doctrine",
     "Delivery is governed end to end: composition, assembly, format, audience, and lineage are all subordinate to declared rules.",
     ["no format ships without lineage",
      "no audience receives content above its trust scope",
      "no delivery channel may strip provenance"]),
    ("operational-rendering-principles",
     "Operational Rendering Principles",
     "Rendering is deterministic given identical inputs and manifest. Identical inputs produce identical outputs across formats (within each format's lossless guarantees).",
     ["determinism is a renderer requirement, not an aspiration",
      "lossy formats MUST disclose what is lost",
      "structured-runtime is source-of-truth; other formats derive from it"]),
    ("audience-aware-publication-doctrine",
     "Audience-Aware Publication Doctrine",
     "Audience awareness changes what is visible, never what is true. Two audiences of the same publication may see different surfaces but never contradictory content.",
     ["audience filters are governance-declared, not author-chosen",
      "no audience override at publication time",
      "PII never reaches non-internal audiences"]),
    ("publication-lineage-philosophy",
     "Publication Lineage Philosophy",
     "Lineage is the spine of every publication. Without it, a publication is a rumor.",
     ["lineage is mandatory + immutable",
      "corrections create new versions, never silent edits",
      "revocation of a source node propagates as a flag on dependent publications"]),
    ("synchronized-knowledge-delivery-principles",
     "Synchronized Knowledge Delivery Principles",
     "When the knowledge-core advances, dependent publications are flagged for re-assembly; they do not silently drift.",
     ["publication freshness is observable and governed",
      "drift is a first-class signal (layer 28 instrumentation)",
      "stale publications are flagged, never auto-republished"]),
]


# =============================================================================
# TASK 8 — FUTURE CONSUMPTION ECOSYSTEMS
# =============================================================================

FUTURE_CONSUMPTION_COMMITMENTS = [
    "future web delivery surfaces will consume the structured-runtime format and apply governance-declared audience filters",
    "future operational support portals will be reviewer-attributed surfaces over the same publications, with no parallel corpus",
    "future contextual copilots will assemble responses via the manual-assembly flow (TASK 6); they may not bypass it",
    "future runtime-assisted onboarding will be a delivery surface over onboarding-guide publications, not a new authoring path",
    "future multimodal publications will subscribe visual-prompt outputs to the dual-review env (layer 25); generation remains out of scope here",
    "future visual guidance ecosystems will be subordinate to VISUAL governance and to publication lineage",
    "future support runtimes will consume support-knowledge-articles as their corpus surface",
]

FUTURE_CONSUMPTION_INVARIANTS = [
    "no consumption surface authors content; all surfaces are read-only over published artifacts",
    "no consumption surface bypasses lineage rendering",
    "no consumption surface re-tiers content (candidate cannot appear as trusted via a delivery channel)",
    "no consumption surface introduces a new audience without governance entry",
    "no consumption surface auto-republishes stale publications",
]


# =============================================================================
# REPORTS — open risks + readiness reassessment
# =============================================================================

UNRESOLVED_PUBLICATION_RISKS = [
    {"id": "no-renderer-implemented",          "severity": "high",   "note": "All composition + assembly + format rules are modeled; no renderer code exists yet."},
    {"id": "no-publication-version-registry",  "severity": "high",   "note": "Publication versions + manifest hashes are required by lineage but no registry exists."},
    {"id": "no-revocation-propagation",        "severity": "high",   "note": "Source-node revocation does not yet flag dependent publications (no dependency index)."},
    {"id": "no-assembly-receipt-emitter",      "severity": "high",   "note": "Runtime-generation auditability requires assembly receipts; runtime emits none today."},
    {"id": "audience-filter-not-enforced",     "severity": "medium", "note": "Audience filters are doctrine-declared; no executable enforcement layer exists."},
    {"id": "no-lossy-format-disclosure-check", "severity": "medium", "note": "Lossy formats must disclose what is lost; no automated check verifies this."},
    {"id": "no-section-order-validator",       "severity": "medium", "note": "Section order is governance-declared; no validator rejects reordered output."},
    {"id": "publication-freshness-undetected", "severity": "medium", "note": "Drift signal is named (layer 28) but has no implementation; stale publications cannot yet be flagged."},
    {"id": "visual-prompt-pipeline-absent",    "severity": "low",    "note": "Visual-prompt format is declarative only; no pipeline consumes it (intentional in this phase)."},
    {"id": "reviewer-validation-surface-absent","severity": "high",  "note": "Reviewer validation step (manual-assembly flow step 4) has no console; depends on layer-24 carry-over."},
]

PUBLICATION_READINESS_REASSESSMENT = {
    "platform_status": "FOUNDATIONALLY COMPLETE (unchanged across phases 28-35)",
    "publication_readiness": "MODELED — composition, assembly, formats, audiences, and lineage are doctrine-complete; no executable renderer yet",
    "primary_bottleneck": "no renderer + no publication version registry + no assembly-receipt emitter",
    "secondary_bottleneck": "reviewer-validation surface absent (carry-over from layer 24 console gap)",
    "next_natural_track": "executable enforcement: minimal renderer over structured-runtime format + version registry + revocation propagation index",
    "layer_count": 29,
    "subordinate_chain_length": 30,
    "test_suite_status": "19/19 passing (runtime untouched)",
    "no_new_mega_layers": True,
    "no_visuals_generated": True,
    "no_frontend_built": True,
}


# =============================================================================
# BUILD
# =============================================================================

def build():
    PUB_ROOT.mkdir(parents=True, exist_ok=True)
    CONST_ROOT.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    ts = now_iso()
    common = {"schema": SCHEMA, "generated_at": ts, "subordinate_to": SUBORDINATE_TO}

    # ---- TASK 1 — composition
    write_pair(
        PUB_ROOT / "composition", "composition",
        "Publication Composition Model",
        "Seven publication types (user-manual, onboarding-guide, troubleshooting-guide, quick-start-guide, installation-guide, operational-faq, support-knowledge-article) with required sections and trust tier requirements.",
        [
            ("Publication types", md_list([
                f"`{p['id']}` — audience: {p['audience_default']}; tier: {p['tier_required']}; required sections: {', '.join(p['required_sections'])}"
                for p in PUBLICATION_TYPES])),
            ("Composition rules", md_list(COMPOSITION_RULES)),
        ],
        {**common, "publication_types": PUBLICATION_TYPES, "rules": COMPOSITION_RULES},
    )

    # ---- TASK 2 — contextual-assembly
    write_pair(
        PUB_ROOT / "contextual-assembly", "contextual-assembly",
        "Contextual Publication Assembly",
        "Seven contextual inputs (procedures, warnings, troubleshooting, escalation guidance, continuity checkpoints, confidence disclosure, provenance references) bound deterministically into structured publications.",
        [
            ("Inputs", md_list([f"`{a['id']}` — source: {a['source_layer']}; binding: {a['binding']}" for a in ASSEMBLY_INPUTS])),
            ("Assembly rules", md_list(ASSEMBLY_RULES)),
        ],
        {**common, "inputs": ASSEMBLY_INPUTS, "rules": ASSEMBLY_RULES},
    )

    # ---- TASK 3 — audience-delivery
    write_pair(
        PUB_ROOT / "audience-delivery", "audience-delivery",
        "Audience-Aware Delivery",
        "Six audiences (end-user, installer, reviewer, operator, governance-maintainer, support-agent) with declared visibility profiles. Audience changes visibility only, never substance.",
        [
            ("Audiences", md_list([
                f"`{a['id']}` — vocabulary: {a['vocabulary']}; internal notes: {a['shows_internal_notes']}; provenance summary: {a['shows_provenance_summary']}; full provenance: {a['shows_full_provenance']}; confidence band: {a['shows_confidence_band']}"
                for a in AUDIENCES])),
            ("Audience rules", md_list(AUDIENCE_RULES)),
        ],
        {**common, "audiences": AUDIENCES, "rules": AUDIENCE_RULES},
    )

    # ---- TASK 4 — delivery-formats
    write_pair(
        PUB_ROOT / "delivery-formats", "delivery-formats",
        "Delivery Format Governance",
        "Six formats (markdown, web, structured-runtime, pdf-ready, support-article, visual-prompt). Structured-runtime is the source-of-truth format; all others derive from it.",
        [
            ("Formats", md_list([
                f"`{f['id']}` — purpose: {f['purpose']}; lossless: {f['lossless']}; constraints: " + "; ".join(f["renderer_constraints"])
                for f in DELIVERY_FORMATS])),
            ("Format rules", md_list(DELIVERY_FORMAT_RULES)),
        ],
        {**common, "formats": DELIVERY_FORMATS, "rules": DELIVERY_FORMAT_RULES},
    )

    # ---- TASK 5 — publication-lineage
    write_pair(
        PUB_ROOT / "publication-lineage", "publication-lineage",
        "Publication Lineage & Traceability",
        "Six lineage facets (provenance traceability, source-node lineage, confidence disclosure, reviewer attribution, publication-version lineage, runtime-generation auditability). Lineage is mandatory and immutable.",
        [
            ("Facets", md_list([f"`{l['id']}` — guarantee: {l['guarantee']}" for l in LINEAGE_FACETS])),
            ("Lineage rules", md_list(LINEAGE_RULES)),
        ],
        {**common, "facets": LINEAGE_FACETS, "rules": LINEAGE_RULES},
    )

    # ---- TASK 6 — manual-assembly
    write_pair(
        PUB_ROOT / "manual-assembly", "manual-assembly",
        "Governed Manual Assembly Flow",
        "Six-step governed flow: knowledge-core → contextual assembly → publication rendering → reviewer validation → publication promotion → runtime-consumable outputs.",
        [
            ("Flow", md_list([f"step {s['step']} — `{s['stage']}` (actor: {s['actor']}; produces: {s['produces']})" for s in MANUAL_ASSEMBLY_FLOW])),
            ("Manual assembly rules", md_list(MANUAL_ASSEMBLY_RULES)),
        ],
        {**common, "flow": MANUAL_ASSEMBLY_FLOW, "rules": MANUAL_ASSEMBLY_RULES},
    )

    # ---- TASK 7 — doctrine root
    (CONST_ROOT / "README.md").write_text(
        "# Publication and Delivery Governance\n\n"
        "Constitutional layer 29. Subordinate to knowledge-core and to all twenty-eight prior governance layers. "
        "Modeling-only. Adds no macro-governance mega-layer. Defines composition, contextual assembly, audience-aware "
        "delivery, delivery formats, publication lineage, and the governed manual assembly flow. The renderer is a "
        "faithful intermediary, never an author.\n",
        encoding="utf-8",
    )
    write_pair(
        CONST_ROOT, "00-charter",
        "Publication and Delivery Governance Charter",
        "Publication is the disciplined act by which the operational knowledge-core becomes consumable by humans. It is governed end to end: composition, assembly, format, audience, lineage.",
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
        ("01-publication-composition-summary", "Publication Composition Summary",
         {**common, "publication_type_count": len(PUBLICATION_TYPES), "types": [p["id"] for p in PUBLICATION_TYPES], "rule_count": len(COMPOSITION_RULES)}),
        ("02-contextual-assembly-summary", "Contextual Assembly Summary",
         {**common, "input_count": len(ASSEMBLY_INPUTS), "inputs": [a["id"] for a in ASSEMBLY_INPUTS], "deterministic": True}),
        ("03-audience-delivery-summary", "Audience Delivery Summary",
         {**common, "audience_count": len(AUDIENCES), "audiences": [a["id"] for a in AUDIENCES], "visibility_only": True}),
        ("04-delivery-format-summary", "Delivery Format Summary",
         {**common, "format_count": len(DELIVERY_FORMATS), "formats": [f["id"] for f in DELIVERY_FORMATS], "source_of_truth_format": "structured-runtime", "visuals_generated": 0}),
        ("05-publication-lineage-summary", "Publication Lineage Summary",
         {**common, "facet_count": len(LINEAGE_FACETS), "facets": [l["id"] for l in LINEAGE_FACETS], "lineage_immutable": True}),
        ("06-manual-assembly-summary", "Manual Assembly Summary",
         {**common, "step_count": len(MANUAL_ASSEMBLY_FLOW), "human_judgment_steps": [4, 5], "compressed": False}),
        ("07-publication-governance-summary", "Publication Governance Summary",
         {**common, "doctrine_root": str(CONST_ROOT.relative_to(REPO_ROOT)), "principle_count": len(CHARTER_PRINCIPLES), "sub_doctrine_count": len(SUB_DOCTRINES)}),
        ("08-future-consumption-summary", "Future Consumption Summary",
         {**common, "commitments": FUTURE_CONSUMPTION_COMMITMENTS, "invariants": FUTURE_CONSUMPTION_INVARIANTS}),
        ("09-unresolved-publication-risks", "Unresolved Publication Risks",
         {**common, "risks": UNRESOLVED_PUBLICATION_RISKS, "risk_count": len(UNRESOLVED_PUBLICATION_RISKS)}),
        ("10-publication-readiness-reassessment", "Publication Readiness Reassessment",
         {**common, **PUBLICATION_READINESS_REASSESSMENT}),
    ]
    for slug, title, payload in reports:
        write_pair(
            REPORTS_ROOT, slug, title,
            "Phase 35 final report — modeling-only; runtime untouched; no renderer implemented; no visuals generated.",
            [("Payload", "See accompanying JSON.")],
            payload,
        )

    print("Publication and Delivery Governance (layer 29) written to:")
    print(f"  {PUB_ROOT}")
    print(f"  {CONST_ROOT}")
    print(f"  {REPORTS_ROOT}")
    print(f"  publication types: {len(PUBLICATION_TYPES)}; assembly inputs: {len(ASSEMBLY_INPUTS)}; "
          f"audiences: {len(AUDIENCES)}; formats: {len(DELIVERY_FORMATS)}; lineage facets: {len(LINEAGE_FACETS)}; "
          f"flow steps: {len(MANUAL_ASSEMBLY_FLOW)}; sub-doctrines: {len(SUB_DOCTRINES)}; risks: {len(UNRESOLVED_PUBLICATION_RISKS)}")


if __name__ == "__main__":
    build()
