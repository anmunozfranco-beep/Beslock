"""
Phase 40 — KNOWLEDGE INTAKE, EVIDENCE ROUTING & OPERATIONAL NAVIGATION GOVERNANCE.

Constitutional layer 33. Modeling-only. Subordinate to knowledge-core and to all
thirty-two prior governance layers (in particular, layer 32 multimodal evidence
governance).

Writes (idempotent, non-destructive, stdlib-only):

  source-of-truth/governance/
    intake-routing/
    evidence-taxonomy/
    trust-models/
    routing-examples/
    intake-consultation/

  source-of-truth/portfolio-vs-product-governance/
  source-of-truth/operational-navigation/
  source-of-truth/intake-safety-governance/

  KNOWLEDGE_BUILDING/INTAKE_AND_NAVIGATION_GOVERNANCE/
    00-INDEX.md + 8 doctrine docs + manifest.json

  _repository-governance/reports/intake-and-navigation/01..10 (.json + .md)

Hard rules:
  - Reads no per-product knowledge-core JSON.
  - Mutates no source-of-truth artefact, no knowledge-core, no runtime.
  - Defines no autonomous agents, no ML, no embeddings, no prompts, no images.
  - Builds NO frontend.
  - Adds NO mega-layer; reuses layer-32 evidence classes, trust tiers,
    ingestion contracts, lifecycle, and conflict policy by reference.
  - 19/19 runtime tests must remain green.

The "source-of-truth/governance/" path written here is the ECOSYSTEM-WIDE
governance root described in the phase-40 brief. It is distinct from the
per-product `ext-images/<product>/source-of-truth/` corpora and does not touch
any per-product directory.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"

# Ecosystem-level (NOT per-product) source-of-truth governance root.
SOT_GOV_ROOT = THEME_ROOT / "source-of-truth-governance"

INTAKE_ROOT = SOT_GOV_ROOT / "governance" / "intake-routing"
TAXO_ROOT = SOT_GOV_ROOT / "governance" / "evidence-taxonomy"
TRUST_ROOT = SOT_GOV_ROOT / "governance" / "trust-models"
ROUTE_EX_ROOT = SOT_GOV_ROOT / "governance" / "routing-examples"
CONSULT_ROOT = SOT_GOV_ROOT / "governance" / "intake-consultation"

PVP_ROOT = SOT_GOV_ROOT / "portfolio-vs-product-governance"
NAV_ROOT = SOT_GOV_ROOT / "operational-navigation"
SAFETY_ROOT = SOT_GOV_ROOT / "intake-safety-governance"

CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "INTAKE_AND_NAVIGATION_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "intake-and-navigation"

SCHEMA = "intake-and-navigation-governance/1.0"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

SUBORDINATE_TO = [
    "knowledge-core", "structured-knowledge", "source-of-truth",
    "runtime-implementation", "knowledge-building",
    "publication-system", "publication-quality", "linguistic-governance",
    "operational-pilots", "review-governance", "channel-governance",
    "lineage-governance", "provenance-governance", "warning-governance",
    "terminology-governance", "visual-system", "visual-intent-governance",
    "component-visibility-governance", "procedural-semantics",
    "semantic-enrichment", "corpus-enrichment",
    "supplemental-source-governance", "phase1-cutover",
    "publication-and-delivery-governance", "operational-pilot-governance",
    "publication-renderer", "publication-quality-governance",
    "linguistic-rendering-governance", "publication-time-only-doctrine",
    "warning-fidelity-doctrine", "multimodal-subordination-doctrine",
    "multimodal-evidence-governance",
]

PRODUCTS = ["e-orbit", "e-prime", "e-flex", "e-touch", "e-shield", "e-nova"]


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def envelope(layer: str, summary: str) -> dict:
    return {
        "schema_version": SCHEMA,
        "layer": layer,
        "constitutional_layer_index": 33,
        "subordinate_to": SUBORDINATE_TO,
        "modeling_only": True,
        "mutates_knowledge_core": False,
        "mutates_source_of_truth": False,
        "mutates_runtime": False,
        "introduces_autonomous_agents": False,
        "introduces_ml_or_embeddings": False,
        "generates_prompts": False,
        "generates_images": False,
        "builds_frontend": False,
        "summary": summary,
        "updated_at": NOW,
    }


# -----------------------------------------------------------------------------
# TASK 1 — Intake-routing doctrine (canonical intake decision pipeline)
# -----------------------------------------------------------------------------

INTAKE_PIPELINE_STEPS = [
    {"id": "1-identify-format",
     "question": "What is the file's format and extension?",
     "decides": "which ingestion contract applies (layer-32 ingestion-contracts)"},
    {"id": "2-classify-evidence-class",
     "question": "Which evidence class does the artefact fall into?",
     "decides": "primary class from layer-32 evidence-classes.json"},
    {"id": "3-determine-scope",
     "question": "Is this product-level, portfolio-level, or shared-ecosystem?",
     "decides": "destination subtree under product-level/ vs portfolio-level/"},
    {"id": "4-identify-product-binding",
     "question": "If product-level, which product does it bind to?",
     "decides": "concrete <product>/ subdirectory"},
    {"id": "5-assign-trust-tier",
     "question": "What is the trust tier per layer-32 evidence-trust-model?",
     "decides": "publishability and downstream propagation"},
    {"id": "6-detect-duplicates",
     "question": "Is this artefact already represented by another (sha256 or supersedes target)?",
     "decides": "ingest-vs-supersede-vs-reject (handled by intake-safety)"},
    {"id": "7-assign-lifecycle-state",
     "question": "What is the initial lifecycle state?",
     "decides": "raw-ingested (default); ocr-derived if extraction is OCR"},
    {"id": "8-record-lineage",
     "question": "Which lineage events must be emitted?",
     "decides": "ingestion-lineage entry minimum; reviewer-lineage planned"},
    {"id": "9-anticipate-downstream-impact",
     "question": "Which publications, warnings, or workflows may this artefact affect?",
     "decides": "downstream-impact note attached to lineage"},
    {"id": "10-assign-reviewer",
     "question": "Which reviewer class must validate before promotion?",
     "decides": "operational-/visual-/installation-/support-/engineering-reviewer"},
]


def task_intake_routing() -> None:
    write_json(
        INTAKE_ROOT / "intake-pipeline.json",
        {
            "id": "intake-pipeline",
            "envelope": envelope("intake-routing", "Canonical 10-step intake decision pipeline."),
            "steps": INTAKE_PIPELINE_STEPS,
            "step_count": len(INTAKE_PIPELINE_STEPS),
            "subordinate_references": {
                "ingestion_contracts": "source-truth-governance/ingestion-contracts/_index.json",
                "evidence_classes": "source-truth-governance/evidence-classification/evidence-classes.json",
                "trust_model": "source-truth-governance/evidence-trust-model.json",
                "lifecycle": "source-truth-governance/ingestion-lifecycle/lifecycle-model.json",
                "lineage_schema": "source-truth-governance/multimodal-lineage/lineage-schema.json",
                "conflict_policy": "source-truth-governance/evidence-conflict-governance/conflict-kinds.json",
            },
        },
    )
    write_json(
        INTAKE_ROOT / "routing-policy.json",
        {
            "id": "routing-policy",
            "envelope": envelope("intake-routing", "Deterministic routing policy."),
            "rules": [
                "Every artefact MUST resolve to exactly one destination path.",
                "Product-level artefacts route under product-level/<product>/<class-folder>/.",
                "Portfolio-level artefacts route under portfolio-level/<portfolio-folder>/.",
                "An artefact cannot be ingested without a classified evidence class.",
                "An artefact cannot be ingested without an assigned trust tier.",
                "An artefact cannot be ingested without an initial lifecycle state.",
                "An artefact cannot be ingested without an assigned reviewer class.",
                "Routing decisions are append-only; revisions emit new lineage events.",
                "When scope is ambiguous, intake-consultation MUST be invoked before placement.",
                "When trust is ambiguous, default to lowest plausible tier and require reviewer escalation.",
            ],
        },
    )
    write_text(
        INTAKE_ROOT / "README.md",
        (
            "# Intake Routing\n\n"
            f"Canonical 10-step intake decision pipeline + routing policy.\n"
            f"Subordinate to layer-32 multimodal evidence governance.\n"
            f"Steps: {len(INTAKE_PIPELINE_STEPS)}.\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 2 — Routing examples + intake consultation
# -----------------------------------------------------------------------------

ROUTING_EXAMPLES = [
    {
        "id": "ex-01-oem-pdf-manual-single-product",
        "input": {
            "filename": "e-Orbit_3.pdf",
            "format": "pdf",
            "received_from": "OEM channel",
            "operator_intent": "official OEM manual for e-orbit revision 3",
        },
        "decisions": {
            "evidence_class": "procedural-evidence",
            "scope": "product-level",
            "product": "e-orbit",
            "destination": "source-of-truth/product-level/e-orbit/manuals/pdf/e-Orbit_3.pdf",
            "ingestion_contract": "pdf",
            "trust_tier": "oem-direct-evidence",
            "lifecycle_state": "raw-ingested",
            "reviewer": "operational-reviewer",
            "downstream_impact": ["publication-system/e-orbit/*", "warnings/*", "operation/*"],
        },
    },
    {
        "id": "ex-02-installer-photo-of-mounted-lock",
        "input": {
            "filename": "IMG_5821.jpg",
            "format": "jpg",
            "received_from": "installer",
            "operator_intent": "photo of installed e-prime in retrofit door",
        },
        "decisions": {
            "evidence_class": "field-evidence",
            "scope": "product-level",
            "product": "e-prime",
            "destination": "source-of-truth/product-level/e-prime/field-evidence/IMG_5821.jpg",
            "ingestion_contract": "raster-image",
            "trust_tier": "installer-evidence",
            "lifecycle_state": "raw-ingested",
            "reviewer": "visual-reviewer",
            "downstream_impact": ["troubleshooting/*", "install/*"],
        },
    },
    {
        "id": "ex-03-portfolio-comparison-matrix-xlsx",
        "input": {
            "filename": "lock-portfolio-comparison.xlsx",
            "format": "xlsx",
            "received_from": "internal product team",
            "operator_intent": "side-by-side capability comparison across all 6 locks",
        },
        "decisions": {
            "evidence_class": "specification-evidence",
            "scope": "portfolio-level",
            "product": None,
            "destination": "source-of-truth/portfolio-level/comparison-matrices/lock-portfolio-comparison.xlsx",
            "ingestion_contract": "spreadsheet",
            "trust_tier": "verified-structured-export",
            "lifecycle_state": "raw-ingested",
            "reviewer": "engineering-reviewer",
            "downstream_impact": ["portfolio-level/capability-taxonomies/*", "publication-system/Product_Manuals.html"],
        },
    },
    {
        "id": "ex-04-app-screenshot-shared-app",
        "input": {
            "filename": "app-pairing-step-3.png",
            "format": "png",
            "received_from": "app team",
            "operator_intent": "screenshot of shared app pairing step 3",
        },
        "decisions": {
            "evidence_class": "visual-evidence",
            "scope": "shared-ecosystem",
            "product": None,
            "destination": "source-of-truth/portfolio-level/shared-app-ecosystems/screenshots/app-pairing-step-3.png",
            "ingestion_contract": "raster-image",
            "trust_tier": "verified-structured-export",
            "lifecycle_state": "raw-ingested",
            "reviewer": "visual-reviewer",
            "downstream_impact": ["operation/pairing across all products"],
        },
    },
    {
        "id": "ex-05-firmware-release-notes-md",
        "input": {
            "filename": "e-shield-fw-1.4.2-release-notes.md",
            "format": "md",
            "received_from": "OEM engineering",
            "operator_intent": "firmware 1.4.2 release notes for e-shield",
        },
        "decisions": {
            "evidence_class": "firmware-evidence",
            "scope": "product-level",
            "product": "e-shield",
            "destination": "source-of-truth/product-level/e-shield/firmware/e-shield-fw-1.4.2-release-notes.md",
            "ingestion_contract": "md",
            "trust_tier": "oem-direct-evidence",
            "lifecycle_state": "raw-ingested",
            "reviewer": "engineering-reviewer",
            "downstream_impact": ["capabilities/*", "publication-system/e-shield/*"],
        },
    },
    {
        "id": "ex-06-ocr-scan-of-paper-installer-card",
        "input": {
            "filename": "installer-card-scan.pdf",
            "format": "pdf",
            "received_from": "support",
            "operator_intent": "scanned paper installer card without text layer",
        },
        "decisions": {
            "evidence_class": "procedural-evidence",
            "scope": "product-level",
            "product": "e-touch",
            "destination": "source-of-truth/product-level/e-touch/manuals/pdf/installer-card-scan.pdf",
            "ingestion_contract": "pdf",
            "trust_tier": "ocr-derived-evidence",
            "lifecycle_state": "ocr-derived",
            "reviewer": "operational-reviewer",
            "downstream_impact": ["install/*"],
            "notes": "OCR fallback: must be flagged 'ocr-derived' until reviewer-validated.",
        },
    },
    {
        "id": "ex-07-ambiguous-spreadsheet-pricing-and-specs-mixed",
        "input": {
            "filename": "internal-mixed-sheet.xlsx",
            "format": "xlsx",
            "received_from": "sales ops",
            "operator_intent": "mix of pricing tabs and capability tabs",
        },
        "decisions": {
            "evidence_class": "specification-evidence + portfolio-pricing (split required)",
            "scope": "ambiguous → intake-consultation required",
            "product": None,
            "destination": "DO NOT INGEST AS-IS — split into per-tab artefacts; route capability tabs to portfolio-level/capability-taxonomies/, pricing tabs to portfolio-level/pricing/",
            "ingestion_contract": "spreadsheet",
            "trust_tier": "verified-structured-export",
            "lifecycle_state": "extraction-pending",
            "reviewer": "engineering-reviewer + portfolio-reviewer",
            "downstream_impact": ["portfolio-level/pricing/*", "portfolio-level/capability-taxonomies/*"],
            "notes": "Mixed-purpose artefacts MUST be split before placement to preserve scope governance.",
        },
    },
    {
        "id": "ex-08-cad-drilling-template-svg",
        "input": {
            "filename": "e-flex-drilling-template.svg",
            "format": "svg",
            "received_from": "OEM engineering",
            "operator_intent": "1:1 drilling template for e-flex",
        },
        "decisions": {
            "evidence_class": "mechanical-evidence",
            "scope": "product-level",
            "product": "e-flex",
            "destination": "source-of-truth/product-level/e-flex/specifications/datasheets/e-flex-drilling-template.svg",
            "ingestion_contract": "vector-or-cad",
            "trust_tier": "oem-direct-evidence",
            "lifecycle_state": "raw-ingested",
            "reviewer": "installation-reviewer",
            "downstream_impact": ["install/* for e-flex", "publication-system/e-flex/installation.html"],
            "notes": "Units + bounding box MUST be recorded per ingestion contract before promotion.",
        },
    },
]


def task_routing_examples() -> None:
    for ex in ROUTING_EXAMPLES:
        write_json(ROUTE_EX_ROOT / f"{ex['id']}.json",
                   {"envelope": envelope("routing-examples", ex["id"]), **ex})
    write_json(
        ROUTE_EX_ROOT / "_index.json",
        {
            "envelope": envelope("routing-examples", "Index of routing examples."),
            "examples": [e["id"] for e in ROUTING_EXAMPLES],
            "example_count": len(ROUTING_EXAMPLES),
        },
    )
    write_text(
        ROUTE_EX_ROOT / "README.md",
        "# Routing Examples\n\n"
        f"{len(ROUTING_EXAMPLES)} worked examples answering 'I have this file. Where should it go?'.\n"
        "Each example records inputs and the deterministic routing decisions per intake-pipeline.\n",
    )


def task_intake_consultation() -> None:
    write_json(
        CONSULT_ROOT / "consultation-protocol.json",
        {
            "id": "intake-consultation-protocol",
            "envelope": envelope("intake-consultation", "Reviewer-facing consultation protocol."),
            "trigger_conditions": [
                "scope is ambiguous (product vs portfolio vs shared)",
                "evidence class is ambiguous (mixed-purpose artefact)",
                "trust tier cannot be assigned from provenance alone",
                "potential duplicate detected by intake-safety",
                "potential cross-product contamination detected",
                "potential lineage break detected (no upstream artefact)",
            ],
            "consultation_questions": [
                "What is the operator's INTENT for this file?",
                "Did this file originate from an OEM channel, installer, support, or unknown source?",
                "Does this file describe one product, multiple products, or the shared app?",
                "Does this file contain mixed-purpose content that should be split?",
                "Does this file supersede an existing artefact? If so, which?",
                "Is OCR required? If yes, the artefact must enter as 'ocr-derived'.",
                "Which reviewer classes need to sign off before promotion?",
                "Which downstream publications, warnings, or workflows are likely affected?",
            ],
            "output_contract": {
                "must_produce": [
                    "evidence_class", "scope", "product_or_null",
                    "destination_path", "ingestion_contract",
                    "trust_tier", "initial_lifecycle_state",
                    "reviewer_classes", "downstream_impact_notes",
                    "lineage_event:ingestion-lineage",
                ],
                "must_block_when": [
                    "scope_unresolved",
                    "evidence_class_unresolved",
                    "trust_tier_unresolved",
                    "duplicate_unresolved",
                    "mixed_purpose_not_split",
                ],
            },
        },
    )
    write_text(
        CONSULT_ROOT / "README.md",
        "# Intake Consultation\n\n"
        "Reviewer-facing protocol invoked whenever intake routing has any unresolved\n"
        "ambiguity. Consultation BLOCKS placement until all required outputs are produced.\n",
    )


# -----------------------------------------------------------------------------
# TASK 3 — Product-level vs portfolio-level governance
# -----------------------------------------------------------------------------

PRODUCT_LEVEL_FOLDERS = [
    "manuals", "images", "videos", "specifications", "firmware",
    "app-guides", "certifications", "field-evidence", "lineage",
]

PORTFOLIO_LEVEL_FOLDERS = [
    "catalogs", "comparison-matrices", "pricing", "capability-taxonomies",
    "reconciled-master-documents", "structured-evidence", "shared-app-ecosystems",
]

EVIDENCE_SCOPES = [
    {"id": "product-level-evidence",
     "binds_to": "exactly one <product>",
     "publication_target": "product-specific publications",
     "examples": ["OEM manual for e-orbit", "drilling template for e-flex", "e-shield firmware notes"]},
    {"id": "portfolio-level-evidence",
     "binds_to": "two or more products OR the portfolio as a whole",
     "publication_target": "portfolio publications + cross-product surfaces",
     "examples": ["lock-portfolio comparison matrix", "pricing sheet", "capability taxonomy"]},
    {"id": "shared-ecosystem-evidence",
     "binds_to": "the shared app or shared infrastructure",
     "publication_target": "shared-app surfaces + every product page that references the app",
     "examples": ["app pairing screenshots", "shared onboarding video"]},
    {"id": "reconciled-evidence",
     "binds_to": "merged view derived from multiple OEM artefacts after reviewer reconciliation",
     "publication_target": "reconciled-master-documents/",
     "examples": ["unified e-flex installer card after merging two OEM revisions"]},
    {"id": "synthesized-evidence",
     "binds_to": "human-authored synthesis built ON TOP of source-of-truth artefacts",
     "publication_target": "publication-system entries marked synthesised; lineage MUST cite all inputs",
     "examples": ["consolidated troubleshooting matrix authored from field-evidence"]},
    {"id": "structured-evidence",
     "binds_to": "structured exports (JSON/CSV/XLSX) derived from unstructured artefacts after reviewer validation",
     "publication_target": "structured-evidence/ + downstream consumers",
     "examples": ["JSON export of capability matrix", "CSV of certified compatibility pairs"]},
]


def task_portfolio_vs_product() -> None:
    write_json(
        PVP_ROOT / "evidence-scopes.json",
        {
            "id": "evidence-scopes",
            "envelope": envelope("portfolio-vs-product", "Scope taxonomy for evidence routing."),
            "scopes": EVIDENCE_SCOPES,
            "product_level_folders": PRODUCT_LEVEL_FOLDERS,
            "portfolio_level_folders": PORTFOLIO_LEVEL_FOLDERS,
            "products": PRODUCTS,
            "rules": [
                "An artefact has exactly one scope.",
                "Mixed-purpose artefacts MUST be split before placement.",
                "Product-level evidence MUST NOT be silently aggregated into portfolio surfaces.",
                "Portfolio-level evidence MUST NOT silently override product-level evidence.",
                "Reconciled and synthesized evidence MUST cite all input lineage.",
            ],
        },
    )
    write_text(
        PVP_ROOT / "README.md",
        "# Portfolio-vs-Product Governance\n\n"
        f"Scopes defined: {len(EVIDENCE_SCOPES)}.\n"
        f"Product-level folders: {len(PRODUCT_LEVEL_FOLDERS)}. "
        f"Portfolio-level folders: {len(PORTFOLIO_LEVEL_FOLDERS)}.\n",
    )


# -----------------------------------------------------------------------------
# TASK 4 — Multimodal evidence taxonomy (operator-facing)
# -----------------------------------------------------------------------------

TAXONOMY_ENTRIES = [
    {"format": "pdf",                 "extensions": [".pdf"],          "default_class": "procedural-evidence",   "scope_default": "product-level",     "ingestion_contract": "pdf"},
    {"format": "docx",                "extensions": [".docx"],         "default_class": "procedural-evidence",   "scope_default": "product-level",     "ingestion_contract": "docx"},
    {"format": "xlsx",                "extensions": [".xls", ".xlsx"], "default_class": "specification-evidence","scope_default": "portfolio-level",   "ingestion_contract": "spreadsheet"},
    {"format": "csv",                 "extensions": [".csv"],          "default_class": "specification-evidence","scope_default": "portfolio-level",   "ingestion_contract": "spreadsheet"},
    {"format": "raster-image",        "extensions": [".png", ".jpg", ".jpeg", ".webp"], "default_class": "visual-evidence", "scope_default": "product-level", "ingestion_contract": "raster-image"},
    {"format": "video",               "extensions": [".mp4", ".mov", ".webm"], "default_class": "operational-evidence", "scope_default": "product-level", "ingestion_contract": "video"},
    {"format": "json",                "extensions": [".json"],         "default_class": "specification-evidence","scope_default": "varies",            "ingestion_contract": "json"},
    {"format": "vector-or-cad",       "extensions": [".svg", ".dxf", ".dwg", ".step", ".stp"], "default_class": "mechanical-evidence", "scope_default": "product-level", "ingestion_contract": "vector-or-cad"},
    {"format": "screenshot",          "extensions": [".png", ".jpg"],  "default_class": "visual-evidence",       "scope_default": "shared-ecosystem (when from shared app)", "ingestion_contract": "raster-image"},
    {"format": "support-archive",     "extensions": [".zip", ".tar", ".tgz"], "default_class": "field-evidence",  "scope_default": "product-level OR portfolio (split required)", "ingestion_contract": "n/a — MUST be unpacked then re-classified per file"},
    {"format": "catalog",             "extensions": [".pdf", ".xlsx"], "default_class": "specification-evidence","scope_default": "portfolio-level",   "ingestion_contract": "pdf-or-spreadsheet"},
    {"format": "comparison-matrix",   "extensions": [".xlsx", ".csv"], "default_class": "specification-evidence","scope_default": "portfolio-level",   "ingestion_contract": "spreadsheet"},
    {"format": "firmware-doc",        "extensions": [".md", ".txt", ".pdf"], "default_class": "firmware-evidence","scope_default": "product-level",     "ingestion_contract": "md-or-txt-or-pdf"},
    {"format": "txt",                 "extensions": [".txt"],          "default_class": "procedural-evidence",   "scope_default": "product-level",     "ingestion_contract": "txt"},
    {"format": "md",                  "extensions": [".md"],           "default_class": "procedural-evidence",   "scope_default": "product-level",     "ingestion_contract": "md"},
]


def task_evidence_taxonomy() -> None:
    write_json(
        TAXO_ROOT / "evidence-taxonomy.json",
        {
            "id": "evidence-taxonomy",
            "envelope": envelope("evidence-taxonomy", "Operator-facing taxonomy mapping format → default class + scope + contract."),
            "entries": TAXONOMY_ENTRIES,
            "entry_count": len(TAXONOMY_ENTRIES),
            "rules": [
                "Defaults are starting points; intake-consultation may override.",
                "Support-archives must be unpacked and re-classified per inner file.",
                "JSON scope is intentionally 'varies' — depends on payload semantics.",
                "Screenshots default to shared-ecosystem when sourced from the shared app.",
            ],
        },
    )
    write_text(
        TAXO_ROOT / "README.md",
        "# Evidence Taxonomy\n\n"
        f"{len(TAXONOMY_ENTRIES)} format entries. Defaults are NON-binding starting points\n"
        "for intake-routing; final placement requires the full intake-pipeline.\n",
    )


# -----------------------------------------------------------------------------
# TASK 5 — Trust models (operator-facing references to layer-32 hierarchy)
# -----------------------------------------------------------------------------

TRUST_RULES = [
    {"tier": "oem-direct-evidence",          "publishable_default": True,  "review_required": True,  "notes": "Sealed OEM artefact via official channel."},
    {"tier": "verified-structured-export",   "publishable_default": True,  "review_required": True,  "notes": "Deterministic structured export, signed-off."},
    {"tier": "structured-evidence",          "publishable_default": True,  "review_required": True,  "notes": "Reviewer-validated structured derivative; carries provenance to inputs."},
    {"tier": "synthesized-evidence",         "publishable_default": False, "review_required": True,  "notes": "Human-authored synthesis; publishable only after reviewer signoff and lineage citation."},
    {"tier": "reconciled-evidence",          "publishable_default": False, "review_required": True,  "notes": "Merged view; publishable only after reviewer reconciliation and lineage citation."},
    {"tier": "installer-evidence",           "publishable_default": False, "review_required": True,  "notes": "Installer photos/notes; usable for troubleshooting/install with reviewer signoff."},
    {"tier": "support-evidence",             "publishable_default": False, "review_required": True,  "notes": "Support-channel artefacts; usable for troubleshooting with reviewer signoff."},
    {"tier": "ocr-derived-evidence",         "publishable_default": False, "review_required": True,  "notes": "Always flagged; never published without explicit reviewer validation."},
    {"tier": "field-evidence",               "publishable_default": False, "review_required": True,  "notes": "Captured on-site; trust depends on captor identity verification (out of scope for this layer)."},
    {"tier": "deprecated-evidence",          "publishable_default": False, "review_required": False, "notes": "Retained for lineage only; never published."},
]


def task_trust_models() -> None:
    write_json(
        TRUST_ROOT / "trust-rules.json",
        {
            "id": "intake-trust-rules",
            "envelope": envelope("trust-models", "Operator-facing trust rules referencing layer-32 hierarchy."),
            "rules": TRUST_RULES,
            "tier_count": len(TRUST_RULES),
            "anchor": "source-truth-governance/evidence-trust-model.json",
            "publication_floor_for_general_publication": "verified-structured-export",
            "publication_floor_for_warnings_and_mechanical_templates": "oem-direct-evidence",
            "ambiguity_default": "lowest-plausible-tier-then-escalate",
        },
    )
    write_text(
        TRUST_ROOT / "README.md",
        "# Trust Models (Intake View)\n\n"
        f"{len(TRUST_RULES)} tier-rule entries. Anchored to layer-32 evidence-trust-model.json.\n",
    )


# -----------------------------------------------------------------------------
# TASK 6 — Operational navigation
# -----------------------------------------------------------------------------

NAVIGATION_DOMAINS = [
    {"domain": "knowledge-core",         "purpose": "canonical, publishable, per-product semantic entries", "operator_question": "Where does the meaning live?"},
    {"domain": "structured-knowledge",   "purpose": "reviewer-validated structured derivatives",            "operator_question": "Where do structured exports live?"},
    {"domain": "source-of-truth",        "purpose": "raw OEM and field artefacts (never mutated)",          "operator_question": "Where does the original file live?"},
    {"domain": "publication-system",     "purpose": "rendered publications + manifests + previews",         "operator_question": "Where does the produced manual live?"},
    {"domain": "publication-quality",    "purpose": "readability, sequencing, cognitive-load doctrine",     "operator_question": "Where do we govern HOW it reads?"},
    {"domain": "linguistic-governance",  "purpose": "Colombian operational Spanish renderers + doctrine",   "operator_question": "Where do we govern WORDS at render time?"},
    {"domain": "source-truth-governance","purpose": "evidence classes, contracts, trust, lineage, lifecycle (layer 32)", "operator_question": "Where do we govern incoming evidence?"},
    {"domain": "source-of-truth-governance", "purpose": "intake routing, navigation, intake-safety (layer 33)", "operator_question": "Where do we route a new file?"},
    {"domain": "_repository-governance/reports", "purpose": "every layer's 10-section reports",             "operator_question": "Where do we read what a layer did?"},
    {"domain": "KNOWLEDGE_BUILDING",     "purpose": "constitutional doctrine roots per layer",              "operator_question": "Where do we read WHY a layer exists?"},
    {"domain": "runtime-implementation", "purpose": "Python runtime; never modified by governance phases",  "operator_question": "Where does the runtime live?"},
]


def task_operational_navigation() -> None:
    write_json(
        NAV_ROOT / "navigation-map.json",
        {
            "id": "operational-navigation-map",
            "envelope": envelope("operational-navigation", "Top-level ecosystem navigation map."),
            "domains": NAVIGATION_DOMAINS,
            "domain_count": len(NAVIGATION_DOMAINS),
        },
    )
    write_text(
        NAV_ROOT / "ecosystem-self-orientation.md",
        (
            "# Ecosystem Self-Orientation\n\n"
            "This document orients a new operator to the ecosystem in 60 seconds.\n\n"
            "## Three immovable surfaces\n\n"
            "1. `runtime-implementation/` — the Python runtime. Governance phases NEVER touch it.\n"
            "2. `wp-content/themes/beslock-custom/User manuals/ext-images/<product>/source-of-truth/` — raw OEM/field artefacts. Read-only by every governance phase.\n"
            "3. `wp-content/themes/beslock-custom/User manuals/ext-images/<product>/knowledge-core/` — canonical per-product semantic entries. Read-only by every governance phase except its own builder.\n\n"
            "## Two write surfaces governance phases USE\n\n"
            "1. `wp-content/themes/beslock-custom/User manuals/<governance-folder>/` — modeling output of each phase.\n"
            "2. `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/<phase>/` — 10-section final reports per phase.\n\n"
            "## When a new file lands\n\n"
            "Open `source-of-truth-governance/governance/intake-routing/intake-pipeline.json` and walk the 10 steps.\n"
            "Use `routing-examples/` for concrete precedents. If anything is ambiguous, invoke `intake-consultation/`.\n\n"
            "## When a publication needs to change\n\n"
            "Do NOT edit `publication-system/generated-publications/` by hand. Edit knowledge-core (with reviewer\n"
            "lineage) and re-run `tools/publication_renderer.py`.\n\n"
            "## When a warning needs to change\n\n"
            "Warnings live in knowledge-core. Severity, irreversibility, escalation flags are immutable at\n"
            "publication-render time per linguistic-governance (layer 31) + warning-fidelity doctrine.\n"
        ),
    )
    write_text(
        NAV_ROOT / "README.md",
        "# Operational Navigation\n\n"
        f"{len(NAVIGATION_DOMAINS)} ecosystem domains mapped, plus a 60-second self-orientation guide.\n",
    )


# -----------------------------------------------------------------------------
# TASK 7 — Future copilot intake readiness (NO autonomous agents)
# -----------------------------------------------------------------------------

def task_future_copilot_readiness() -> None:
    write_json(
        SOT_GOV_ROOT / "future-copilot-intake-readiness.json",
        {
            "id": "future-copilot-intake-readiness",
            "envelope": envelope("future-copilot-readiness", "Readiness contract for future Copilot-assisted intake."),
            "future_capabilities": [
                "Copilot-assisted intake (suggestion-only)",
                "semi-automated routing recommendation",
                "evidence recommendation against routing-examples",
                "ingestion validation against ingestion-contracts",
                "trust-aware classification suggestion (suggestion-only)",
            ],
            "non_negotiable_invariants": [
                "Copilot is suggestion-only. Reviewer signoff is required for placement.",
                "No autonomous ingestion; every placement is a human decision.",
                "Copilot must consume intake-pipeline.json and routing-policy.json verbatim.",
                "Copilot must surface ambiguity and trigger intake-consultation when triggers fire.",
                "Copilot must never bypass intake-safety governance.",
                "Copilot must never mutate knowledge-core or source-of-truth.",
                "No ML or embeddings introduced in this layer.",
            ],
            "interface_contract_for_future_copilot": {
                "must_read": [
                    "source-of-truth-governance/governance/intake-routing/intake-pipeline.json",
                    "source-of-truth-governance/governance/intake-routing/routing-policy.json",
                    "source-of-truth-governance/governance/evidence-taxonomy/evidence-taxonomy.json",
                    "source-of-truth-governance/governance/trust-models/trust-rules.json",
                    "source-of-truth-governance/governance/routing-examples/_index.json",
                    "source-of-truth-governance/governance/intake-consultation/consultation-protocol.json",
                    "source-of-truth-governance/portfolio-vs-product-governance/evidence-scopes.json",
                    "source-of-truth-governance/intake-safety-governance/safety-rules.json",
                    "source-truth-governance/* (layer 32 anchors)",
                ],
                "must_emit_per_placement_proposal": [
                    "evidence_class", "scope", "product_or_null",
                    "destination_path", "ingestion_contract",
                    "trust_tier", "initial_lifecycle_state",
                    "reviewer_classes", "downstream_impact_notes",
                    "ambiguity_flags", "suggested_lineage_event",
                ],
            },
        },
    )


# -----------------------------------------------------------------------------
# TASK 8 — Intake safety governance
# -----------------------------------------------------------------------------

SAFETY_RISKS = [
    {"id": "evidence-duplication",         "detection": "sha256 collision OR same logical artefact across paths", "block_action": "BLOCK placement; require supersedes-relation or rejection."},
    {"id": "routing-chaos",                "detection": "artefact placed outside any defined product-level/portfolio-level/shared-ecosystem folder", "block_action": "BLOCK placement; route via intake-pipeline."},
    {"id": "cross-product-contamination",  "detection": "artefact placed under wrong product OR mixing multiple products' content under one product folder", "block_action": "BLOCK placement; split or re-route via intake-consultation."},
    {"id": "trust-ambiguity",              "detection": "trust tier not assignable from provenance", "block_action": "BLOCK placement; default to lowest plausible and escalate."},
    {"id": "misplaced-portfolio-evidence", "detection": "portfolio-level artefact placed under a single product folder", "block_action": "BLOCK placement; relocate under portfolio-level/."},
    {"id": "broken-lineage",               "detection": "ingestion-lineage event missing OR upstream artefact unreachable", "block_action": "BLOCK promotion; require lineage repair before reviewer-validation."},
    {"id": "mixed-purpose-not-split",      "detection": "single artefact carries content belonging to two or more scopes/classes", "block_action": "BLOCK placement; split into per-purpose artefacts."},
    {"id": "ocr-derived-not-flagged",      "detection": "OCR-extracted content ingested without 'ocr-derived' lifecycle state", "block_action": "BLOCK promotion; mark lifecycle state correctly."},
]


def task_intake_safety() -> None:
    write_json(
        SAFETY_ROOT / "safety-rules.json",
        {
            "id": "intake-safety-rules",
            "envelope": envelope("intake-safety-governance", "Block-on-detection intake safety rules."),
            "risks": SAFETY_RISKS,
            "risk_count": len(SAFETY_RISKS),
            "global_invariants": [
                "Detection emits an audit event; block_action MUST be respected.",
                "Safety rules are subordinate to layer-32 conflict policy.",
                "Block actions never silently rewrite an artefact; they require human action.",
            ],
        },
    )
    write_text(
        SAFETY_ROOT / "README.md",
        "# Intake Safety Governance\n\n"
        f"{len(SAFETY_RISKS)} risk classes. Every detection BLOCKS placement or promotion until\n"
        "a reviewer resolves it through intake-consultation.\n",
    )


# -----------------------------------------------------------------------------
# Constitutional doctrine
# -----------------------------------------------------------------------------

DOCTRINE_DOCS = {
    "00-INDEX.md": (
        "# Intake & Navigation Governance — Constitutional Index (Layer 33)\n\n"
        "1. Intake is human-governed; no autonomous ingestion.\n"
        "2. Routing is deterministic; intake-consultation is the only legal escape hatch.\n"
        "3. Scope is binary at the artefact level: product, portfolio, or shared-ecosystem (mixed → split).\n"
        "4. Trust is layer-32 anchored; ambiguity defaults to the lowest plausible tier.\n"
        "5. Operational navigation is a first-class deliverable — operators must be able to self-orient.\n"
        "6. Future Copilot is suggestion-only. Reviewer signoff is required for placement.\n"
        "7. Intake safety BLOCKS, never silently rewrites.\n"
        "8. This layer touches no per-product knowledge-core or source-of-truth artefact.\n"
    ),
    "01-intake-philosophy.md": (
        "# Intake Philosophy\n\n"
        "Every new artefact enters the ecosystem through a deterministic 10-step pipeline.\n"
        "Operators are not asked to remember rules; the rules are written down once, read by\n"
        "humans, and (in the future) consumed by Copilot.\n"
    ),
    "02-routing-determinism-doctrine.md": (
        "# Routing Determinism Doctrine\n\n"
        "Given the same inputs, intake-routing must yield the same destination, evidence\n"
        "class, trust tier, lifecycle state, and reviewer assignment. Determinism is the\n"
        "precondition for future Copilot suggestion.\n"
    ),
    "03-scope-binarity-doctrine.md": (
        "# Scope Binarity Doctrine\n\n"
        "An artefact has exactly one scope: product-level, portfolio-level, or shared-ecosystem.\n"
        "Mixed-purpose artefacts MUST be split before placement. Silent aggregation across scopes\n"
        "is forbidden.\n"
    ),
    "04-trust-anchoring-doctrine.md": (
        "# Trust Anchoring Doctrine\n\n"
        "All intake trust assignments are anchored to layer-32 evidence-trust-model.json.\n"
        "When provenance does not establish a tier, default to the lowest plausible tier and\n"
        "escalate to reviewer.\n"
    ),
    "05-self-orientation-doctrine.md": (
        "# Self-Orientation Doctrine\n\n"
        "Operators must be able to answer 'where does this live?' and 'why does this layer exist?'\n"
        "in under 60 seconds. operational-navigation/ exists for exactly this purpose.\n"
    ),
    "06-copilot-subordination-doctrine.md": (
        "# Copilot Subordination Doctrine\n\n"
        "Future Copilot intake is suggestion-only. It MUST consume the intake-pipeline,\n"
        "routing-policy, taxonomy, trust-rules, examples, consultation-protocol, scope rules,\n"
        "and safety-rules verbatim. It MUST NOT mutate knowledge-core or source-of-truth.\n"
    ),
    "07-safety-doctrine.md": (
        "# Safety Doctrine\n\n"
        "Detection BLOCKS placement or promotion until a reviewer resolves the underlying\n"
        "issue. Safety never silently rewrites. Safety rules subordinate to layer-32 conflict\n"
        "policy and the warning-fidelity doctrine.\n"
    ),
    "08-non-mutation-doctrine.md": (
        "# Non-Mutation Doctrine\n\n"
        "This layer writes only governance documents. It reads no per-product knowledge-core\n"
        "JSON. It writes no source-of-truth artefact. It modifies no runtime code. The 19/19\n"
        "runtime test invariant must remain green after every build of this layer.\n"
    ),
}


def task_doctrine() -> None:
    for name, body in DOCTRINE_DOCS.items():
        write_text(CONST_ROOT / name, body)
    write_json(
        CONST_ROOT / "manifest.json",
        {
            "id": "intake-and-navigation-doctrine-manifest",
            "envelope": envelope("constitutional-doctrine", "Doctrine manifest for layer 33."),
            "documents": list(DOCTRINE_DOCS.keys()),
            "document_count": len(DOCTRINE_DOCS),
        },
    )


# -----------------------------------------------------------------------------
# Top-level README + final reports
# -----------------------------------------------------------------------------

def task_top_readme() -> None:
    write_text(
        SOT_GOV_ROOT / "README.md",
        (
            "# Source-of-Truth Governance (Layer 33)\n\n"
            "Knowledge intake, evidence routing, operational navigation, and intake safety.\n\n"
            "Modeling-only. Subordinate to layer 32 (multimodal evidence governance) and to\n"
            "every prior governance layer. Writes no per-product artefact; mutates no runtime.\n\n"
            "Subdirectories:\n\n"
            "- `governance/intake-routing/` — 10-step intake pipeline + routing policy\n"
            "- `governance/evidence-taxonomy/` — operator-facing format → class/scope/contract map\n"
            "- `governance/trust-models/` — operator-facing trust rules anchored to layer 32\n"
            "- `governance/routing-examples/` — worked 'where does this go?' examples\n"
            "- `governance/intake-consultation/` — reviewer-facing consultation protocol\n"
            "- `portfolio-vs-product-governance/` — scope taxonomy + folder layouts\n"
            "- `operational-navigation/` — ecosystem self-orientation\n"
            "- `intake-safety-governance/` — block-on-detection safety rules\n"
            "- `future-copilot-intake-readiness.json` — interface contract for future Copilot\n"
        ),
    )


def emit_reports() -> None:
    reports = [
        ("01-intake-governance-summary",
         {"section": "1 — Intake governance",
          "pipeline_steps": len(INTAKE_PIPELINE_STEPS),
          "policy_rules": 10,
          "consultation_triggers": 6,
          "anchored_to": "layer-32 multimodal evidence governance"}),
        ("02-evidence-routing-summary",
         {"section": "2 — Evidence routing",
          "examples": [e["id"] for e in ROUTING_EXAMPLES],
          "example_count": len(ROUTING_EXAMPLES),
          "ambiguity_handling": "intake-consultation BLOCKS placement until resolved"}),
        ("03-portfolio-vs-product-summary",
         {"section": "3 — Portfolio vs product",
          "scope_count": len(EVIDENCE_SCOPES),
          "scopes": [s["id"] for s in EVIDENCE_SCOPES],
          "product_level_folders": PRODUCT_LEVEL_FOLDERS,
          "portfolio_level_folders": PORTFOLIO_LEVEL_FOLDERS,
          "products": PRODUCTS}),
        ("04-evidence-taxonomy-summary",
         {"section": "4 — Evidence taxonomy",
          "entry_count": len(TAXONOMY_ENTRIES),
          "formats": [t["format"] for t in TAXONOMY_ENTRIES]}),
        ("05-trust-model-summary",
         {"section": "5 — Trust model",
          "tier_count": len(TRUST_RULES),
          "publication_floor": "verified-structured-export",
          "warnings_floor": "oem-direct-evidence",
          "anchor": "layer-32 evidence-trust-model.json"}),
        ("06-operational-navigation-summary",
         {"section": "6 — Operational navigation",
          "domain_count": len(NAVIGATION_DOMAINS),
          "self_orientation_doc": "operational-navigation/ecosystem-self-orientation.md"}),
        ("07-future-copilot-readiness-summary",
         {"section": "7 — Future Copilot intake readiness",
          "copilot_mode": "suggestion-only",
          "autonomous_ingestion": False,
          "ml_introduced": False,
          "interface_contract_emitted": True}),
        ("08-intake-safety-governance-summary",
         {"section": "8 — Intake safety governance",
          "risk_count": len(SAFETY_RISKS),
          "risks": [r["id"] for r in SAFETY_RISKS],
          "all_detections_block": True,
          "silent_rewrite_allowed": False}),
        ("09-unresolved-intake-risks",
         {"section": "9 — Unresolved intake risks",
          "risks": [
              "No executable scanner over existing source-of-truth/ trees runs in this layer; risks are policy-defined but not yet detected against the live corpus.",
              "Mixed-purpose artefact splitting depends on reviewer judgement; no automated splitter exists.",
              "Field-evidence captor identity verification is out of scope; trust tier defaults to 'installer-evidence' or below pending external attestation.",
              "Cross-product contamination detection relies on placement audit; an automated path validator is not implemented in this layer.",
              "Future Copilot interface contract is documented but no Copilot is implemented; absence does not invalidate the contract.",
              "Routing-policy assumes one canonical destination per artefact; multi-destination cases (e.g., legitimate dual-product artefacts) require future doctrine extension via reconciled-master-documents/.",
          ]}),
        ("10-operational-intake-maturity-reassessment",
         {"section": "10 — Operational intake maturity reassessment",
          "intake_pipeline_defined": True,
          "routing_policy_defined": True,
          "examples_defined": True,
          "consultation_protocol_defined": True,
          "scope_taxonomy_defined": True,
          "evidence_taxonomy_defined": True,
          "trust_rules_defined": True,
          "navigation_documented": True,
          "future_copilot_interface_defined": True,
          "safety_rules_defined": True,
          "executable_scanners_present": False,
          "knowledge_core_mutated": False,
          "source_of_truth_mutated": False,
          "runtime_mutated": False,
          "autonomous_ingestion_introduced": False,
          "ml_or_embeddings_introduced": False,
          "next_executable_track": [
              "scan ext-images/<product>/source-of-truth/ trees and emit per-product placement audits",
              "build a path-validator that enforces routing-policy on the live corpus",
              "wire intake-pipeline JSON into reviewer tooling",
              "design Copilot prompt-set against the future-copilot interface contract",
          ]}),
    ]
    for name, payload in reports:
        write_json(REPORTS_ROOT / f"{name}.json", {"envelope": envelope("report", payload["section"]), **payload})
        md = [f"# {payload['section']}", ""]
        for k, v in payload.items():
            if k == "section":
                continue
            md.append(f"- **{k}**: {json.dumps(v, ensure_ascii=False)}")
        write_text(REPORTS_ROOT / f"{name}.md", "\n".join(md) + "\n")


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------

def build() -> None:
    for d in (SOT_GOV_ROOT, INTAKE_ROOT, TAXO_ROOT, TRUST_ROOT, ROUTE_EX_ROOT,
              CONSULT_ROOT, PVP_ROOT, NAV_ROOT, SAFETY_ROOT, CONST_ROOT, REPORTS_ROOT):
        d.mkdir(parents=True, exist_ok=True)
    task_intake_routing()
    task_routing_examples()
    task_intake_consultation()
    task_portfolio_vs_product()
    task_evidence_taxonomy()
    task_trust_models()
    task_operational_navigation()
    task_future_copilot_readiness()
    task_intake_safety()
    task_doctrine()
    task_top_readme()
    emit_reports()
    print("Intake & Navigation Governance written to:")
    print(f"  {SOT_GOV_ROOT.relative_to(REPO_ROOT)}")
    print(f"  {CONST_ROOT.relative_to(REPO_ROOT)}")
    print(f"  {REPORTS_ROOT.relative_to(REPO_ROOT)}")
    print(f"  Subordinate chain length: {len(SUBORDINATE_TO) + 1}")


if __name__ == "__main__":
    build()
