"""
Phase 39 — MULTIMODAL EVIDENCE CLASSIFICATION & INGESTION GOVERNANCE.

Constitutional layer 32. Modeling-only. Subordinate to knowledge-core and to
all thirty-one prior governance layers.

Writes (idempotent, non-destructive, stdlib-only):

  source-truth-governance/
    evidence-classification/
    ingestion-contracts/
    evidence-trust-model.json
    multimodal-lineage/
    cross-modal-grounding/
    ingestion-lifecycle/
    evidence-conflict-governance/
    future-multimodal-readiness.json
    README.md

  KNOWLEDGE_BUILDING/MULTIMODAL_EVIDENCE_GOVERNANCE/
    00-INDEX.md + 7 doctrine docs + manifest.json

  _repository-governance/reports/multimodal-evidence/01..10 (.json + .md)

Hard rules enforced by this layer:
  - Does NOT mutate knowledge-core, structured-knowledge, source-of-truth,
    runtime-implementation, generated_manuals, generated_manuals_supplemental.
  - Defines no ML pipelines, no embeddings, no autonomous interpretation,
    no visual generation, no prompt generation.
  - Reads no per-product knowledge-core JSON.
  - Adds NO macro-governance mega-layer.
  - Touches no runtime code (19/19 tests stay green).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"

STG_ROOT = THEME_ROOT / "source-truth-governance"
EC_ROOT = STG_ROOT / "evidence-classification"
IC_ROOT = STG_ROOT / "ingestion-contracts"
ML_ROOT = STG_ROOT / "multimodal-lineage"
CMG_ROOT = STG_ROOT / "cross-modal-grounding"
LC_ROOT = STG_ROOT / "ingestion-lifecycle"
CONF_ROOT = STG_ROOT / "evidence-conflict-governance"

CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "MULTIMODAL_EVIDENCE_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "multimodal-evidence"

SCHEMA = "multimodal-evidence-governance/1.0"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

SUBORDINATE_TO = [
    "knowledge-core",
    "structured-knowledge",
    "source-of-truth",
    "runtime-implementation",
    "knowledge-building",
    "publication-system",
    "publication-quality",
    "linguistic-governance",
    "operational-pilots",
    "review-governance",
    "channel-governance",
    "lineage-governance",
    "provenance-governance",
    "warning-governance",
    "terminology-governance",
    "visual-system",
    "visual-intent-governance",
    "component-visibility-governance",
    "procedural-semantics",
    "semantic-enrichment",
    "corpus-enrichment",
    "supplemental-source-governance",
    "phase1-cutover",
    "publication-and-delivery-governance",
    "operational-pilot-governance",
    "publication-renderer",
    "publication-quality-governance",
    "linguistic-rendering-governance",
    "publication-time-only-doctrine",
    "warning-fidelity-doctrine",
    "multimodal-subordination-doctrine",
]


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
        "constitutional_layer_index": 32,
        "subordinate_to": SUBORDINATE_TO,
        "modeling_only": True,
        "mutates_knowledge_core": False,
        "mutates_source_of_truth": False,
        "mutates_runtime": False,
        "generates_prompts": False,
        "generates_images": False,
        "introduces_ml_pipelines": False,
        "introduces_embeddings": False,
        "invokes_comfyui": False,
        "applied_at": "ingestion-time-and-publication-time-via-future-wiring",
        "summary": summary,
        "updated_at": NOW,
    }


# -----------------------------------------------------------------------------
# TASK 1 — Evidence classification
# -----------------------------------------------------------------------------

EVIDENCE_CLASSES = [
    {
        "id": "procedural-evidence",
        "label_es": "Evidencia procedimental",
        "description": "Stepwise operator procedures: pairing, enrollment, recovery, reset.",
        "primary_modalities": ["pdf", "md", "docx", "txt"],
        "secondary_modalities": ["mp4", "png"],
        "binds_to_knowledge_core_subdomains": ["operation", "workflows", "install"],
        "review_class": "operational-reviewer",
        "trust_floor": "verified-structured-export",
    },
    {
        "id": "visual-evidence",
        "label_es": "Evidencia visual",
        "description": "Photographs, renders, exploded diagrams, screenshots — every pixel that informs an operator.",
        "primary_modalities": ["png", "jpg", "webp", "svg"],
        "secondary_modalities": ["pdf", "mp4"],
        "binds_to_knowledge_core_subdomains": ["visual", "component-visibility", "visual-intent"],
        "review_class": "visual-reviewer",
        "trust_floor": "oem-direct-evidence",
    },
    {
        "id": "mechanical-evidence",
        "label_es": "Evidencia mecánica",
        "description": "Drilling templates, backsets, hole centres, dimensional drawings.",
        "primary_modalities": ["pdf", "svg", "cad", "png"],
        "secondary_modalities": ["xlsx", "csv"],
        "binds_to_knowledge_core_subdomains": ["install", "specifications"],
        "review_class": "installation-reviewer",
        "trust_floor": "oem-direct-evidence",
    },
    {
        "id": "troubleshooting-evidence",
        "label_es": "Evidencia de diagnóstico",
        "description": "Symptom-to-cause-to-action artefacts, escalation paths, field reports.",
        "primary_modalities": ["md", "pdf", "txt"],
        "secondary_modalities": ["mp4", "png"],
        "binds_to_knowledge_core_subdomains": ["troubleshooting", "warnings"],
        "review_class": "support-reviewer",
        "trust_floor": "support-evidence",
    },
    {
        "id": "firmware-evidence",
        "label_es": "Evidencia de firmware",
        "description": "Firmware versions, release notes, behavioural deltas.",
        "primary_modalities": ["txt", "md", "json"],
        "secondary_modalities": ["pdf"],
        "binds_to_knowledge_core_subdomains": ["capabilities", "specifications"],
        "review_class": "engineering-reviewer",
        "trust_floor": "oem-direct-evidence",
    },
    {
        "id": "specification-evidence",
        "label_es": "Evidencia de especificación",
        "description": "Datasheets, compatibility matrices, electrical/mechanical specs.",
        "primary_modalities": ["xlsx", "csv", "pdf"],
        "secondary_modalities": ["json"],
        "binds_to_knowledge_core_subdomains": ["specifications", "capabilities"],
        "review_class": "engineering-reviewer",
        "trust_floor": "verified-structured-export",
    },
    {
        "id": "operational-evidence",
        "label_es": "Evidencia operacional",
        "description": "Onboarding flows, app-screen sequences, day-to-day operator behaviour.",
        "primary_modalities": ["md", "pdf", "png", "mp4"],
        "secondary_modalities": ["txt"],
        "binds_to_knowledge_core_subdomains": ["operation", "workflows"],
        "review_class": "operational-reviewer",
        "trust_floor": "verified-structured-export",
    },
    {
        "id": "field-evidence",
        "label_es": "Evidencia de campo",
        "description": "Installer photos, support tickets, observed failures, retrofit notes.",
        "primary_modalities": ["png", "jpg", "mp4", "md"],
        "secondary_modalities": ["pdf"],
        "binds_to_knowledge_core_subdomains": ["troubleshooting", "install", "operation"],
        "review_class": "support-reviewer",
        "trust_floor": "installer-evidence",
    },
    {
        "id": "certification-evidence",
        "label_es": "Evidencia de certificación",
        "description": "Regulatory certifications, conformity declarations, test reports.",
        "primary_modalities": ["pdf"],
        "secondary_modalities": ["png"],
        "binds_to_knowledge_core_subdomains": ["specifications", "capabilities"],
        "review_class": "engineering-reviewer",
        "trust_floor": "oem-direct-evidence",
    },
]


def task_evidence_classification() -> None:
    write_json(
        EC_ROOT / "evidence-classes.json",
        {
            "id": "evidence-classes",
            "envelope": envelope(
                "evidence-classification",
                "Canonical multimodal evidence taxonomy.",
            ),
            "classes": EVIDENCE_CLASSES,
            "class_count": len(EVIDENCE_CLASSES),
        },
    )
    write_text(
        EC_ROOT / "README.md",
        (
            "# Evidence Classification\n\n"
            "Canonical multimodal evidence taxonomy. Every artifact ingested into\n"
            "`source-of-truth/` MUST be classified into exactly one primary class\n"
            "from `evidence-classes.json`. Secondary cross-classification is allowed\n"
            "via `multimodal-lineage/cross-modal-references.json`.\n\n"
            "Classes defined: " + str(len(EVIDENCE_CLASSES)) + ".\n"
        ),
    )


# -----------------------------------------------------------------------------
# TASK 2 — Ingestion contracts
# -----------------------------------------------------------------------------

INGESTION_CONTRACTS = [
    {
        "format": "pdf",
        "extensions": [".pdf"],
        "evidence_classes_supported": [
            "procedural-evidence", "mechanical-evidence", "specification-evidence",
            "certification-evidence", "troubleshooting-evidence", "operational-evidence",
        ],
        "extraction_expectations": {
            "primary": "deterministic-text-extraction-when-text-layer-present",
            "fallback": "OCR-derived",
            "structural": "section-and-page-anchors-required",
        },
        "trust_weighting": "oem-direct-evidence-when-from-OEM-channel-otherwise-OCR-derived",
        "lineage_requirements": [
            "source_path", "page_anchor", "extraction_method",
            "extraction_tool", "extraction_timestamp",
        ],
        "provenance_requirements": ["oem-channel", "oem-version", "received-from"],
        "reviewer_requirements": ["operational-reviewer-or-engineering-reviewer-by-class"],
        "forbidden": ["silent-paraphrase", "page-anchor-omission", "OEM-language-rewrite-at-ingest-time"],
    },
    {
        "format": "docx",
        "extensions": [".docx"],
        "evidence_classes_supported": [
            "procedural-evidence", "operational-evidence", "troubleshooting-evidence",
        ],
        "extraction_expectations": {
            "primary": "deterministic-text-and-style-extraction",
            "structural": "heading-tree-required",
        },
        "trust_weighting": "verified-structured-export-when-from-OEM-otherwise-installer-or-support-evidence",
        "lineage_requirements": ["source_path", "heading_anchor", "extraction_method", "extraction_timestamp"],
        "provenance_requirements": ["author", "received-from"],
        "reviewer_requirements": ["operational-reviewer"],
        "forbidden": ["embedded-image-loss", "style-loss"],
    },
    {
        "format": "txt",
        "extensions": [".txt"],
        "evidence_classes_supported": ["procedural-evidence", "firmware-evidence", "operational-evidence"],
        "extraction_expectations": {"primary": "byte-identical-ingest"},
        "trust_weighting": "verified-structured-export-or-OCR-derived",
        "lineage_requirements": ["source_path", "extraction_method", "extraction_timestamp"],
        "provenance_requirements": ["received-from"],
        "reviewer_requirements": ["operational-reviewer"],
        "forbidden": ["silent-encoding-conversion-without-record"],
    },
    {
        "format": "md",
        "extensions": [".md", ".markdown"],
        "evidence_classes_supported": [
            "procedural-evidence", "operational-evidence", "troubleshooting-evidence",
            "firmware-evidence",
        ],
        "extraction_expectations": {
            "primary": "byte-identical-ingest",
            "structural": "heading-tree-canonical",
        },
        "trust_weighting": "verified-structured-export",
        "lineage_requirements": ["source_path", "heading_anchor", "extraction_timestamp"],
        "provenance_requirements": ["received-from"],
        "reviewer_requirements": ["operational-reviewer"],
        "forbidden": ["silent-rewrite", "frontmatter-loss"],
    },
    {
        "format": "raster-image",
        "extensions": [".png", ".jpg", ".jpeg", ".webp"],
        "evidence_classes_supported": ["visual-evidence", "field-evidence", "operational-evidence"],
        "extraction_expectations": {
            "primary": "byte-identical-ingest",
            "structural": "EXIF-and-dimensions-recorded",
            "OCR": "optional-and-explicitly-flagged-when-applied",
        },
        "trust_weighting": "oem-direct-evidence-when-from-OEM-otherwise-installer-or-field-evidence",
        "lineage_requirements": ["source_path", "sha256", "dimensions", "EXIF_capture_time", "ingestion_timestamp"],
        "provenance_requirements": ["captured-by", "received-from"],
        "reviewer_requirements": ["visual-reviewer"],
        "forbidden": ["silent-resize", "silent-recompression", "EXIF-stripping-without-record"],
    },
    {
        "format": "video",
        "extensions": [".mp4", ".mov", ".webm"],
        "evidence_classes_supported": [
            "operational-evidence", "troubleshooting-evidence", "field-evidence",
            "visual-evidence",
        ],
        "extraction_expectations": {
            "primary": "byte-identical-ingest",
            "structural": "duration-codec-resolution-recorded",
            "frames": "no-automatic-frame-extraction-without-explicit-request",
        },
        "trust_weighting": "oem-direct-evidence-or-installer-evidence",
        "lineage_requirements": ["source_path", "sha256", "duration_seconds", "ingestion_timestamp"],
        "provenance_requirements": ["captured-by", "received-from"],
        "reviewer_requirements": ["visual-reviewer", "operational-reviewer"],
        "forbidden": ["silent-transcoding", "silent-trimming"],
    },
    {
        "format": "spreadsheet",
        "extensions": [".xls", ".xlsx", ".csv"],
        "evidence_classes_supported": ["specification-evidence", "firmware-evidence"],
        "extraction_expectations": {
            "primary": "deterministic-cell-extraction",
            "structural": "sheet-and-cell-anchors-required",
        },
        "trust_weighting": "verified-structured-export",
        "lineage_requirements": ["source_path", "sheet", "cell_range", "extraction_timestamp"],
        "provenance_requirements": ["received-from"],
        "reviewer_requirements": ["engineering-reviewer"],
        "forbidden": ["silent-cell-coercion", "silent-merge-of-rows"],
    },
    {
        "format": "vector-or-cad",
        "extensions": [".svg", ".dxf", ".dwg", ".step", ".stp"],
        "evidence_classes_supported": ["mechanical-evidence", "visual-evidence"],
        "extraction_expectations": {
            "primary": "byte-identical-ingest",
            "structural": "units-and-bounding-box-recorded",
        },
        "trust_weighting": "oem-direct-evidence",
        "lineage_requirements": ["source_path", "sha256", "units", "bounding_box", "ingestion_timestamp"],
        "provenance_requirements": ["received-from"],
        "reviewer_requirements": ["installation-reviewer"],
        "forbidden": ["unit-coercion", "silent-flattening"],
    },
    {
        "format": "json",
        "extensions": [".json"],
        "evidence_classes_supported": ["firmware-evidence", "specification-evidence", "operational-evidence"],
        "extraction_expectations": {
            "primary": "byte-identical-ingest",
            "structural": "schema-version-required-when-applicable",
        },
        "trust_weighting": "verified-structured-export",
        "lineage_requirements": ["source_path", "sha256", "ingestion_timestamp"],
        "provenance_requirements": ["received-from"],
        "reviewer_requirements": ["engineering-reviewer"],
        "forbidden": ["silent-key-rename", "schema-coercion"],
    },
]


def task_ingestion_contracts() -> None:
    for c in INGESTION_CONTRACTS:
        write_json(
            IC_ROOT / f"{c['format']}.json",
            {
                "id": f"ingestion-contract-{c['format']}",
                "envelope": envelope(
                    "ingestion-contracts",
                    f"Ingestion contract for {c['format']}.",
                ),
                "contract": c,
            },
        )
    write_json(
        IC_ROOT / "_index.json",
        {
            "id": "ingestion-contracts-index",
            "envelope": envelope("ingestion-contracts", "Index of all ingestion contracts."),
            "formats": [c["format"] for c in INGESTION_CONTRACTS],
            "format_count": len(INGESTION_CONTRACTS),
        },
    )
    write_text(
        IC_ROOT / "README.md",
        "# Ingestion Contracts\n\n"
        "One contract per format. Every ingest action MUST satisfy the matching\n"
        "contract: extraction expectations met, trust weighting assigned, lineage\n"
        "fields populated, provenance recorded, reviewer class identified.\n\n"
        f"Contracts defined: {len(INGESTION_CONTRACTS)}.\n",
    )


# -----------------------------------------------------------------------------
# TASK 3 — Evidence trust model
# -----------------------------------------------------------------------------

TRUST_HIERARCHY = [
    {"id": "oem-direct-evidence",         "rank": 100, "label_es": "Evidencia OEM directa",
     "description": "Sealed OEM artefacts received through the official channel."},
    {"id": "verified-structured-export",  "rank": 85,  "label_es": "Exportación estructurada verificada",
     "description": "Deterministic structured export from OEM systems, signed-off."},
    {"id": "installer-evidence",          "rank": 65,  "label_es": "Evidencia de instalador",
     "description": "Installer photos, retrofit notes, on-site captures."},
    {"id": "support-evidence",            "rank": 55,  "label_es": "Evidencia de soporte",
     "description": "Support-channel artefacts: tickets, ad-hoc captures, transcripts."},
    {"id": "ocr-derived-evidence",        "rank": 40,  "label_es": "Evidencia derivada por OCR",
     "description": "Text recovered from images/PDFs without text layer; ALWAYS flagged."},
    {"id": "inferred-evidence",           "rank": 25,  "label_es": "Evidencia inferida",
     "description": "Candidate-pending-review entries derived from corpus enrichment."},
    {"id": "deprecated-evidence",         "rank": 0,   "label_es": "Evidencia deprecada",
     "description": "Superseded artefacts retained for lineage only; never published."},
]


def task_trust_model() -> None:
    write_json(
        STG_ROOT / "evidence-trust-model.json",
        {
            "id": "evidence-trust-model",
            "envelope": envelope(
                "evidence-trust-model",
                "Canonical evidence trust hierarchy.",
            ),
            "hierarchy": TRUST_HIERARCHY,
            "tier_count": len(TRUST_HIERARCHY),
            "rules": {
                "publication_floor": "verified-structured-export",
                "warnings_publication_floor": "oem-direct-evidence",
                "mechanical_template_publication_floor": "oem-direct-evidence",
                "ocr_derived_requires_explicit_flag": True,
                "inferred_requires_candidate_pending_review_status": True,
                "deprecated_must_never_publish": True,
                "trust_downgrades_propagate_to_dependent_publications": True,
            },
        },
    )


# -----------------------------------------------------------------------------
# TASK 4 — Multimodal lineage
# -----------------------------------------------------------------------------

LINEAGE_KINDS = [
    "ingestion-lineage", "extraction-lineage", "reviewer-lineage",
    "promotion-lineage", "publication-lineage",
]


def task_multimodal_lineage() -> None:
    write_json(
        ML_ROOT / "lineage-schema.json",
        {
            "id": "multimodal-lineage-schema",
            "envelope": envelope(
                "multimodal-lineage",
                "Required lineage fields for every multimodal evidence artifact.",
            ),
            "lineage_kinds": LINEAGE_KINDS,
            "fields_required_per_artifact": [
                "artifact_id", "artifact_path", "evidence_class",
                "ingest_format", "trust_tier",
                "ingestion_lineage", "extraction_lineage",
                "reviewer_lineage", "promotion_lineage", "publication_lineage",
                "cross_modal_references",
            ],
            "lineage_event_shape": {
                "kind": "one-of:" + "|".join(LINEAGE_KINDS),
                "actor": "string (human reviewer id or tool id)",
                "tool": "string|null",
                "from_state": "ingestion-lifecycle state id",
                "to_state": "ingestion-lifecycle state id",
                "timestamp_utc": "ISO-8601 Z",
                "evidence_refs": "list[str]",
                "notes": "string",
            },
        },
    )
    write_json(
        ML_ROOT / "cross-modal-references.json",
        {
            "id": "cross-modal-references-schema",
            "envelope": envelope(
                "multimodal-lineage",
                "Schema for cross-modal references between evidence artifacts.",
            ),
            "reference_shape": {
                "from_artifact_id": "str",
                "from_modality": "pdf|md|png|...",
                "to_artifact_id": "str",
                "to_modality": "pdf|md|png|...",
                "relation": "one-of: depicts | annotates | supersedes | derived-from | "
                            "grounds | conflicts-with | clarifies | substitutes",
                "trust_inheritance": "min(from.trust_tier, to.trust_tier) unless explicitly-overridden-by-reviewer",
            },
            "forbidden_relations_without_reviewer_signoff": ["supersedes", "substitutes", "conflicts-with"],
        },
    )
    write_text(
        ML_ROOT / "README.md",
        "# Multimodal Lineage\n\n"
        "Every multimodal evidence artifact carries five lineage tracks plus an\n"
        "explicit cross-modal reference graph. Lineage is append-only: prior\n"
        "events MUST NOT be rewritten.\n",
    )


# -----------------------------------------------------------------------------
# TASK 5 — Cross-modal operational grounding (NO ML)
# -----------------------------------------------------------------------------

GROUNDING_TYPES = [
    {
        "id": "image-to-procedure",
        "label_es": "Imagen a procedimiento",
        "binds": "visual-evidence -> procedural-evidence",
        "binding_method": "explicit-reviewer-curation",
        "ml_required": False,
        "consumed_by_future": ["publication-renderer", "support-copilot"],
    },
    {
        "id": "video-to-workflow",
        "label_es": "Video a flujo",
        "binds": "operational-evidence(video) -> workflows",
        "binding_method": "explicit-reviewer-curation-with-timecodes",
        "ml_required": False,
        "consumed_by_future": ["publication-renderer", "onboarding-channel"],
    },
    {
        "id": "screenshot-to-operation",
        "label_es": "Captura de pantalla a operación",
        "binds": "visual-evidence(app-screenshot) -> operation/workflow step",
        "binding_method": "explicit-reviewer-curation",
        "ml_required": False,
        "consumed_by_future": ["publication-renderer", "support-copilot"],
    },
    {
        "id": "specification-to-warning",
        "label_es": "Especificación a advertencia",
        "binds": "specification-evidence -> warnings",
        "binding_method": "deterministic-rule-derivation-with-reviewer-signoff",
        "ml_required": False,
        "consumed_by_future": ["publication-renderer", "warning-governance"],
    },
    {
        "id": "firmware-to-publication",
        "label_es": "Firmware a publicación",
        "binds": "firmware-evidence -> publication-system entries",
        "binding_method": "version-anchored-reviewer-curation",
        "ml_required": False,
        "consumed_by_future": ["publication-renderer", "channel-governance"],
    },
]


def task_cross_modal_grounding() -> None:
    write_json(
        CMG_ROOT / "grounding-types.json",
        {
            "id": "cross-modal-grounding-types",
            "envelope": envelope(
                "cross-modal-grounding",
                "Deterministic, non-ML grounding contracts between modalities.",
            ),
            "types": GROUNDING_TYPES,
            "type_count": len(GROUNDING_TYPES),
            "global_constraints": {
                "no_ml_pipelines": True,
                "no_embeddings": True,
                "no_autonomous_inference": True,
                "all_groundings_require_reviewer_signoff_before_publication": True,
                "publication_use_strictly_subordinate_to_warning_governance": True,
            },
        },
    )
    write_text(
        CMG_ROOT / "README.md",
        "# Cross-Modal Operational Grounding\n\n"
        "Defines the contracts that allow an image, video, screenshot,\n"
        "specification, or firmware artefact to GROUND a publication step\n"
        "WITHOUT introducing ML. All groundings are explicit, reviewer-curated,\n"
        "and lineage-tracked. No autonomous interpretation is permitted.\n",
    )


# -----------------------------------------------------------------------------
# TASK 6 — Ingestion lifecycle
# -----------------------------------------------------------------------------

LIFECYCLE_STATES = [
    {"id": "raw-ingested",        "is_terminal": False, "publishable": False,
     "description": "Artefact landed in source-of-truth, classified, lineage initialised."},
    {"id": "extraction-pending",  "is_terminal": False, "publishable": False,
     "description": "Awaiting deterministic extraction per ingestion contract."},
    {"id": "ocr-derived",         "is_terminal": False, "publishable": False,
     "description": "Text recovered via OCR; explicitly flagged; awaiting review."},
    {"id": "candidate-generated", "is_terminal": False, "publishable": False,
     "description": "Knowledge-core candidate proposed; status=candidate-pending-review."},
    {"id": "reviewer-validated",  "is_terminal": False, "publishable": False,
     "description": "Reviewer signed off content + lineage + trust assignment."},
    {"id": "promoted",            "is_terminal": False, "publishable": True,
     "description": "Promoted into knowledge-core / structured-knowledge as canonical."},
    {"id": "deprecated",          "is_terminal": True,  "publishable": False,
     "description": "Withdrawn from publication; retained for lineage only."},
    {"id": "superseded",          "is_terminal": True,  "publishable": False,
     "description": "Replaced by a newer artefact; cross-modal-reference relation=supersedes."},
]

LIFECYCLE_TRANSITIONS = [
    ("raw-ingested",        "extraction-pending"),
    ("extraction-pending",  "ocr-derived"),
    ("extraction-pending",  "candidate-generated"),
    ("ocr-derived",         "candidate-generated"),
    ("candidate-generated", "reviewer-validated"),
    ("reviewer-validated",  "promoted"),
    ("promoted",            "superseded"),
    ("promoted",            "deprecated"),
    ("reviewer-validated",  "deprecated"),
    ("candidate-generated", "deprecated"),
]


def task_ingestion_lifecycle() -> None:
    write_json(
        LC_ROOT / "lifecycle-model.json",
        {
            "id": "ingestion-lifecycle-model",
            "envelope": envelope("ingestion-lifecycle", "Lifecycle state machine for every multimodal artifact."),
            "states": LIFECYCLE_STATES,
            "transitions": [{"from": a, "to": b} for a, b in LIFECYCLE_TRANSITIONS],
            "invariants": {
                "publishable_only_when_state_in": ["promoted"],
                "ocr_derived_must_pass_through_reviewer_validated_before_promotion": True,
                "candidate_generated_must_carry_validation_status_candidate_pending_review": True,
                "deprecated_or_superseded_are_terminal": True,
                "lineage_event_required_on_every_transition": True,
            },
        },
    )
    write_text(
        LC_ROOT / "README.md",
        "# Ingestion Lifecycle\n\n"
        f"States: {len(LIFECYCLE_STATES)}. Transitions: {len(LIFECYCLE_TRANSITIONS)}.\n"
        "Every state change MUST emit a lineage event under the relevant lineage track.\n",
    )


# -----------------------------------------------------------------------------
# TASK 7 — Evidence conflict governance
# -----------------------------------------------------------------------------

CONFLICT_KINDS = [
    {"id": "conflicting-manuals",        "detection": "two artefacts in same evidence-class with overlapping coverage and divergent procedural text"},
    {"id": "conflicting-procedures",     "detection": "knowledge-core entries from different sources prescribe incompatible operator actions"},
    {"id": "conflicting-specifications", "detection": "datasheet rows or capability flags disagree across artefacts of equal trust tier"},
    {"id": "visual-inconsistencies",     "detection": "visual evidence depicts components or layouts that contradict component-visibility-map"},
    {"id": "firmware-publication-drift", "detection": "promoted publication references firmware version absent from firmware-evidence"},
    {"id": "outdated-evidence",          "detection": "artefact older than supersedes-relation target in cross-modal-references"},
]

CONFLICT_RESOLUTION_POLICY = [
    "Higher trust tier wins.",
    "On equal trust tier: most recent reviewer-validated artefact wins.",
    "On equal trust tier and equal validation date: ESCALATE — block publication.",
    "Visual inconsistencies BLOCK publication of the bound procedure until resolved.",
    "Firmware/publication drift BLOCKS publication of affected entries.",
    "Outdated-evidence transitions to 'superseded' via lineage, never silent overwrite.",
]


def task_evidence_conflict_governance() -> None:
    write_json(
        CONF_ROOT / "conflict-kinds.json",
        {
            "id": "evidence-conflict-kinds",
            "envelope": envelope(
                "evidence-conflict-governance",
                "Detectable evidence-conflict classes and resolution policy.",
            ),
            "kinds": CONFLICT_KINDS,
            "resolution_policy": CONFLICT_RESOLUTION_POLICY,
            "blocking_kinds": ["visual-inconsistencies", "firmware-publication-drift"],
            "escalation_required_when_unresolvable": True,
        },
    )
    write_text(
        CONF_ROOT / "README.md",
        "# Evidence Conflict Governance\n\n"
        f"Conflict kinds: {len(CONFLICT_KINDS)}. Resolution policy is deterministic\n"
        "and trust-tier-anchored. Conflicts that cannot be resolved by policy are\n"
        "ESCALATED — never silently rewritten.\n",
    )


# -----------------------------------------------------------------------------
# TASK 8 — Future multimodal publication readiness
# -----------------------------------------------------------------------------

def task_future_multimodal_readiness() -> None:
    write_json(
        STG_ROOT / "future-multimodal-readiness.json",
        {
            "id": "future-multimodal-readiness",
            "envelope": envelope(
                "future-multimodal-readiness",
                "Readiness contract for downstream multimodal publication channels.",
            ),
            "future_capabilities_supported": [
                "supportive-visuals",
                "procedural-hybrid-diagrams",
                "video-assisted-onboarding",
                "multimodal-troubleshooting",
                "contextual-support-copilots",
            ],
            "non_negotiable_invariants": [
                "All outputs subordinate to evidence trust hierarchy.",
                "All outputs subordinate to warning-governance and warning-fidelity.",
                "All outputs subordinate to linguistic-governance (publication-time only).",
                "All outputs lineage-traceable to source-of-truth artefacts.",
                "No autonomous interpretation; reviewer signoff required before publication.",
                "No ML pipelines, no embeddings, no prompt generation, no image generation in this layer.",
            ],
            "interface_contract_for_downstream_consumers": {
                "must_read": [
                    "evidence-classification/evidence-classes.json",
                    "evidence-trust-model.json",
                    "ingestion-contracts/_index.json",
                    "ingestion-lifecycle/lifecycle-model.json",
                    "multimodal-lineage/lineage-schema.json",
                    "multimodal-lineage/cross-modal-references.json",
                    "cross-modal-grounding/grounding-types.json",
                    "evidence-conflict-governance/conflict-kinds.json",
                ],
                "must_honour": [
                    "publication_floor", "blocking conflict kinds",
                    "publishable lifecycle states", "reviewer signoff for groundings",
                ],
            },
        },
    )


# -----------------------------------------------------------------------------
# Constitutional doctrine
# -----------------------------------------------------------------------------

DOCTRINE_DOCS = {
    "00-INDEX.md": (
        "# Multimodal Evidence Governance — Constitutional Index (Layer 32)\n\n"
        "1. Evidence is the foundation; every publication step is anchored in a classified, trust-weighted, lineage-traceable artefact.\n"
        "2. Ingestion is contract-bound; every format has explicit extraction, lineage, provenance, and reviewer expectations.\n"
        "3. Trust is hierarchical and propagates downstream.\n"
        "4. Lineage is append-only; prior events are immutable.\n"
        "5. Cross-modal grounding is reviewer-curated and deterministic; no ML in this layer.\n"
        "6. Lifecycle is explicit; only `promoted` artefacts can publish.\n"
        "7. Conflicts are detected, never silently resolved; unresolvable cases escalate.\n"
    ),
    "01-evidence-foundation-doctrine.md": (
        "# Evidence Foundation Doctrine\n\n"
        "Knowledge-core entries without traceable evidence are NOT publishable.\n"
        "Every publishable claim resolves to one or more classified evidence artefacts.\n"
    ),
    "02-ingestion-contracts-doctrine.md": (
        "# Ingestion Contracts Doctrine\n\n"
        "Format-specific contracts define what 'ingested' means. Silent transformations\n"
        "(transcoding, resizing, encoding shifts, cell coercion) are forbidden without\n"
        "explicit lineage record.\n"
    ),
    "03-trust-hierarchy-doctrine.md": (
        "# Trust Hierarchy Doctrine\n\n"
        "OEM-direct > verified-structured-export > installer > support > OCR-derived > inferred > deprecated.\n"
        "Trust downgrades propagate to every publication that depends on the downgraded artefact.\n"
    ),
    "04-multimodal-lineage-doctrine.md": (
        "# Multimodal Lineage Doctrine\n\n"
        "Every artefact carries five lineage tracks: ingestion, extraction, reviewer,\n"
        "promotion, publication. Cross-modal references form a typed, append-only graph.\n"
    ),
    "05-cross-modal-grounding-doctrine.md": (
        "# Cross-Modal Grounding Doctrine\n\n"
        "Image, video, screenshot, specification, and firmware artefacts may GROUND a\n"
        "publication step ONLY through explicit reviewer-curated bindings. No autonomous\n"
        "interpretation. No ML in this layer.\n"
    ),
    "06-ingestion-lifecycle-doctrine.md": (
        "# Ingestion Lifecycle Doctrine\n\n"
        "raw-ingested → extraction-pending → (ocr-derived) → candidate-generated\n"
        "→ reviewer-validated → promoted. Terminal states: deprecated, superseded.\n"
        "Only `promoted` artefacts can be published.\n"
    ),
    "07-conflict-and-escalation-doctrine.md": (
        "# Conflict & Escalation Doctrine\n\n"
        "Visual inconsistencies and firmware/publication drift are PUBLICATION-BLOCKING.\n"
        "Unresolvable conflicts ESCALATE — they are never silently resolved by this layer\n"
        "and never bypassed by downstream consumers.\n"
    ),
}


def task_doctrine() -> None:
    for name, body in DOCTRINE_DOCS.items():
        write_text(CONST_ROOT / name, body)
    write_json(
        CONST_ROOT / "manifest.json",
        {
            "id": "multimodal-evidence-governance-doctrine-manifest",
            "envelope": envelope("constitutional-doctrine", "Doctrine manifest for layer 32."),
            "documents": list(DOCTRINE_DOCS.keys()),
            "document_count": len(DOCTRINE_DOCS),
        },
    )


# -----------------------------------------------------------------------------
# Top-level README + final reports
# -----------------------------------------------------------------------------

def task_top_readme() -> None:
    write_text(
        STG_ROOT / "README.md",
        (
            "# Source-Truth Governance (Layer 32)\n\n"
            "Multimodal evidence classification, ingestion contracts, trust model,\n"
            "lineage, cross-modal grounding, lifecycle, and conflict governance.\n\n"
            "Modeling-only. Knowledge-core, source-of-truth, and runtime are NEVER\n"
            "mutated by this layer. No ML, no embeddings, no prompts, no images.\n\n"
            "Subdirectories:\n\n"
            "- `evidence-classification/` — canonical evidence classes\n"
            "- `ingestion-contracts/` — per-format ingestion contracts\n"
            "- `evidence-trust-model.json` — trust hierarchy\n"
            "- `multimodal-lineage/` — five-track lineage + cross-modal references\n"
            "- `cross-modal-grounding/` — non-ML grounding contracts\n"
            "- `ingestion-lifecycle/` — lifecycle state machine\n"
            "- `evidence-conflict-governance/` — conflict detection + resolution\n"
            "- `future-multimodal-readiness.json` — downstream interface contract\n"
        ),
    )


def emit_reports() -> None:
    reports = [
        ("01-evidence-classification-summary",
         {
             "section": "1 — Evidence classification",
             "class_count": len(EVIDENCE_CLASSES),
             "classes": [c["id"] for c in EVIDENCE_CLASSES],
             "modalities_covered": sorted({m for c in EVIDENCE_CLASSES for m in c["primary_modalities"] + c["secondary_modalities"]}),
         }),
        ("02-ingestion-contract-summary",
         {
             "section": "2 — Ingestion contracts",
             "format_count": len(INGESTION_CONTRACTS),
             "formats": [c["format"] for c in INGESTION_CONTRACTS],
             "extensions_covered": sorted({e for c in INGESTION_CONTRACTS for e in c["extensions"]}),
         }),
        ("03-evidence-trust-model-summary",
         {
             "section": "3 — Evidence trust model",
             "tier_count": len(TRUST_HIERARCHY),
             "tiers": [t["id"] for t in TRUST_HIERARCHY],
             "publication_floor": "verified-structured-export",
             "warnings_publication_floor": "oem-direct-evidence",
         }),
        ("04-multimodal-lineage-summary",
         {
             "section": "4 — Multimodal lineage",
             "lineage_kinds": LINEAGE_KINDS,
             "append_only": True,
             "cross_modal_relations": [
                 "depicts", "annotates", "supersedes", "derived-from",
                 "grounds", "conflicts-with", "clarifies", "substitutes",
             ],
         }),
        ("05-cross-modal-grounding-summary",
         {
             "section": "5 — Cross-modal grounding",
             "type_count": len(GROUNDING_TYPES),
             "types": [g["id"] for g in GROUNDING_TYPES],
             "ml_pipelines_introduced": False,
             "embeddings_introduced": False,
             "reviewer_signoff_required": True,
         }),
        ("06-ingestion-lifecycle-summary",
         {
             "section": "6 — Ingestion lifecycle",
             "state_count": len(LIFECYCLE_STATES),
             "transition_count": len(LIFECYCLE_TRANSITIONS),
             "publishable_states": ["promoted"],
             "terminal_states": ["deprecated", "superseded"],
         }),
        ("07-evidence-conflict-governance-summary",
         {
             "section": "7 — Evidence conflict governance",
             "conflict_kind_count": len(CONFLICT_KINDS),
             "blocking_kinds": ["visual-inconsistencies", "firmware-publication-drift"],
             "policy": CONFLICT_RESOLUTION_POLICY,
             "escalation_required_when_unresolvable": True,
         }),
        ("08-future-multimodal-readiness-summary",
         {
             "section": "8 — Future multimodal publication readiness",
             "future_capabilities": [
                 "supportive-visuals", "procedural-hybrid-diagrams",
                 "video-assisted-onboarding", "multimodal-troubleshooting",
                 "contextual-support-copilots",
             ],
             "subordinate_to_warning_governance": True,
             "subordinate_to_linguistic_governance": True,
             "subordinate_to_evidence_trust_hierarchy": True,
         }),
        ("09-unresolved-ingestion-risks",
         {
             "section": "9 — Unresolved ingestion risks",
             "risks": [
                 "OCR-derived artefacts may pass reviewer-validation without an OCR-quality score (no quality scorer in this layer).",
                 "Cross-modal references currently rely on manual curation; absence of an automated drift detector means stale references can persist until next reviewer pass.",
                 "Field-evidence trust assignment depends on installer identity verification, which is not modelled here.",
                 "CAD/SVG ingestion records units but does not validate geometric plausibility against component-visibility-map.",
                 "Conflict detection is policy-modelled but not yet executed — no scanner runs against the live corpus in this layer.",
                 "Lifecycle event emission depends on downstream tools honouring the contract; no enforcement runtime added here.",
             ],
         }),
        ("10-multimodal-ingestion-maturity-reassessment",
         {
             "section": "10 — Multimodal ingestion maturity reassessment",
             "evidence_classes_defined": True,
             "ingestion_contracts_defined": True,
             "trust_model_defined": True,
             "lineage_schema_defined": True,
             "cross_modal_grounding_contracts_defined": True,
             "lifecycle_state_machine_defined": True,
             "conflict_governance_defined": True,
             "future_multimodal_interface_contract_defined": True,
             "executable_scanners_present": False,
             "knowledge_core_mutated": False,
             "source_of_truth_mutated": False,
             "runtime_mutated": False,
             "ml_pipelines_introduced": False,
             "next_executable_track": [
                 "scan source-of-truth/ trees and emit per-product evidence-inventories",
                 "wire lifecycle transitions into reviewer tooling",
                 "wire conflict-detection scanner over knowledge-core + source-of-truth",
                 "wire cross-modal-grounding consumption into publication renderer",
             ],
         }),
    ]
    for name, payload in reports:
        write_json(REPORTS_ROOT / f"{name}.json", {"envelope": envelope("report", payload["section"]), **payload})
        md_lines = [f"# {payload['section']}", ""]
        for k, v in payload.items():
            if k == "section":
                continue
            md_lines.append(f"- **{k}**: {json.dumps(v, ensure_ascii=False)}")
        write_text(REPORTS_ROOT / f"{name}.md", "\n".join(md_lines) + "\n")


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------

def build() -> None:
    for d in (STG_ROOT, EC_ROOT, IC_ROOT, ML_ROOT, CMG_ROOT, LC_ROOT, CONF_ROOT,
              CONST_ROOT, REPORTS_ROOT):
        d.mkdir(parents=True, exist_ok=True)
    task_evidence_classification()
    task_ingestion_contracts()
    task_trust_model()
    task_multimodal_lineage()
    task_cross_modal_grounding()
    task_ingestion_lifecycle()
    task_evidence_conflict_governance()
    task_future_multimodal_readiness()
    task_doctrine()
    task_top_readme()
    emit_reports()
    print("Multimodal Evidence Governance written to:")
    print(f"  {STG_ROOT.relative_to(REPO_ROOT)}")
    print(f"  {CONST_ROOT.relative_to(REPO_ROOT)}")
    print(f"  {REPORTS_ROOT.relative_to(REPO_ROOT)}")
    print(f"  Subordinate chain length: {len(SUBORDINATE_TO) + 1}")


if __name__ == "__main__":
    build()
