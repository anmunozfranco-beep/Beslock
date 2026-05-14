#!/usr/bin/env python3
"""
Phase 59 builder — Production Hardening, Corpus Validation & Final Reviewer
Readiness Closure (constitutional layer 52).

Convergence + hardening layer: NO new orchestration / semantic / synthesis /
publication / replay / extraction families. NO autonomous remediation. NO
operational scoring. NO AI readiness claims. NO behavior tracking. NO
telemetry. NO dashboards. Pointer-only artifacts that stress-test, harden,
verify, and stabilize the Phase 47–58 substrate.

Idempotent. Writes ONLY into the layer's own runtime tree.
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

SCHEMA = "production-hardening-corpus-validation/1.0"
LAYER = 52

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RULES_ROOT = OC_ROOT / "execution-engine"
ASSETS_EXEC_ROOT = OC_ROOT / "assets/exec"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
KB_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING"
REPORTS_ROOT = THEME_ROOT / "_repository-governance/reports"

PH_ROOT = OC_ROOT / "production-hardening-runtime"
PH_SUBDIRS = [
    "corpus-stress-validations",
    "runtime-hardening-scans",
    "reviewer-readiness-checks",
    "operational-regression-scans",
    "corpus-anomaly-records",
    "deployment-rehearsal-records",
    "final-production-attestations",
    "runtime-maintenance-summaries",
    "stability-baseline-records",
    "operational-maturity-reports",
]

# 50-entry chain ending with Phase 58 anchor.
SUBORDINATE_TO = [
    "governed-storefront-ownership",
    "governed-bem-presentation",
    "governed-active-bootstrap",
    "governed-runtime-isolation",
    "governed-product-card-presentation",
    "governed-product-card-runtime-ownership",
    "governed-frontend-architecture",
    "governed-component-migration",
    "governed-utilities-migration",
    "governed-header-runtime",
    "governed-header-css-consolidation",
    "governed-header-migration",
    "governed-homepage-surface-migration",
    "governed-main-css-decomposition",
    "governed-legacy-runtime-audit",
    "governed-worktree-normalization",
    "governed-bem-guidelines",
    "governed-cleanup-plan",
    "governed-architecture-doctrine",
    "governed-frontend-architecture-doctrine",
    "governed-runtime-ownership-doctrine",
    "governed-visual-system-doctrine",
    "governed-product-tabs-doctrine",
    "governed-product-interaction-doctrine",
    "governed-interactions-snapshot-doctrine",
    "governed-document-package-doctrine",
    "governed-generated-artifacts-doctrine",
    "governed-hero-overlay-layout-doctrine",
    "governed-hero-mobile-parity-doctrine",
    "governed-hero-startup-handoff-doctrine",
    "governed-phase1-cutover-doctrine",
    "governed-phase2-knowledge-runtime-doctrine",
    "governed-knowledge-extraction",
    "governed-manual-ocr",
    "governed-visual-generation-automation",
    "governed-canonical-product-id",
    "governed-bootstrap-consolidation",
    "governed-product-card-consolidation",
    "governed-evidence-ingestion",
    "governed-knowledge-synthesis",
    "governed-multimodal-knowledge-grounding",
    "governed-visual-generation-runtime",
    "governed-multimodal-publication-composition",
    "governed-semantic-evidence-extraction",
    "governed-manual-semantic-packaging",
    "unified-operational-manual-runtime-closure",
    "semantic-convergence-cross-evidence-fusion",
    "final-operational-closure-production-readiness",
    "operational-deployment-readiness-controlled-production-activation",
    "reviewer-operational-ergonomics-convergence",
]
assert len(SUBORDINATE_TO) >= 50, f"SUBORDINATE_TO too short: {len(SUBORDINATE_TO)}"

POSTURE = {
    # Hardening posture
    "production_hardening_priority": True,
    "corpus_validation_priority": True,
    "operational_stability_priority": True,
    "deterministic_regression_protection": True,
    "reviewer_confidence_priority": True,
    "operational_repeatability_priority": True,
    "runtime_maintainability_priority": True,
    "convergence_over_expansion": True,
    "architectural_growth_priority": False,
    "wires_existing_systems": True,
    # Hardening-specific negatives
    "no_autonomous_remediation": True,
    "no_runtime_expansion": True,
    "no_operational_scoring": True,
    "no_ai_readiness_claims": True,
    "no_hidden_runtime_behavior": True,
    # Standard negative posture
    "introduces_new_orchestration": False,
    "introduces_new_replay_engine": False,
    "introduces_new_lifecycle_family": False,
    "introduces_new_extraction_framework": False,
    "introduces_new_publication_runtime": False,
    "introduces_new_semantic_runtime": False,
    "introduces_new_presentation_runtime": False,
    "introduces_new_governance_family": False,
    "introduces_new_synthesis_system": False,
    "deterministic_only": True,
    "no_embeddings": True,
    "no_vector_databases": True,
    "no_probabilistic_inference": True,
    "no_ml_models": True,
    "no_machine_translation": True,
    "no_llm_translation": True,
    "no_autonomous_agents": True,
    "no_autonomous_arbitration": True,
    "no_autonomous_publication": True,
    "no_autonomous_activation": True,
    "no_autonomous_prioritization": True,
    "no_silent_production_replacement": True,
    "no_overwrite_semantics": True,
    "no_dashboards": True,
    "no_telemetry": True,
    "no_behavior_tracking": True,
    "no_analytics": True,
    "no_operational_automation": True,
    "no_deployment_automation": True,
    "no_background_workers": True,
    "no_hidden_propagation": True,
    "no_frontend_frameworks": True,
    "no_responsive_rendering_systems": True,
    "no_deployment_automation_daemons": True,
    "no_cloud_apis": True,
    "no_saas": True,
    "no_daemons": True,
    # Authority + lineage
    "reviewer_authoritative": True,
    "reviewer_attribution_required": True,
    "lineage_preserving": True,
    "additive_lineage": True,
    "append_only_event_stores": True,
    "fail_closed_validation": True,
    "presentation_neutral_outputs": True,
    "writes_only_into_production_hardening_runtime_tree": True,
    "writes_to_reviewer_operational_runtime_tree": False,
    "writes_to_operational_deployment_runtime_tree": False,
    "writes_to_production_closure_runtime_tree": False,
    "writes_to_semantic_convergence_runtime_tree": False,
    "writes_to_manual_runtime_closure_tree": False,
    "writes_to_manual_semantic_packaging_runtime_tree": False,
    "stdlib_only": True,
    "local_first": True,
    "cli_only_interface": True,
    "constitutional_layer_index": LAYER,
    "post_constitutional_hardening_phase": True,
}

DISPATCH_KINDS = [
    "corpus-stress-validation",
    "runtime-hardening-scan",
    "reviewer-readiness-check",
    "operational-regression-scan",
    "corpus-anomaly-record",
    "deployment-rehearsal-record",
    "final-production-attestation",
    "runtime-maintenance-summary",
    "stability-baseline-record",
    "operational-maturity-report",
]

HARDENING_SCOPES = [
    "overwrite-isolation",
    "replay-consistency",
    "hash-consistency",
    "lifecycle-consistency",
    "export-reproducibility",
]

READINESS_AREAS = [
    "onboarding",
    "deployment",
    "rollback",
    "handoff",
    "audit",
]

ANOMALY_KINDS = [
    "ingestion-anomaly",
    "extraction-anomaly",
    "synthesis-anomaly",
    "packaging-anomaly",
    "stabilization-anomaly",
    "deployment-anomaly",
    "activation-anomaly",
    "reviewer-process-anomaly",
]

ANOMALY_SEVERITIES = ["informational", "minor", "major", "blocking"]

REHEARSAL_OUTCOMES = ["pass", "fail", "skipped"]

MATURITY_DIMENSIONS = [
    "hardening-coverage",
    "regression-protection",
    "rehearsal-coverage",
    "attestation-coverage",
    "baseline-coverage",
    "anomaly-tracking",
    "maintenance-coverage",
    "reviewer-readiness-coverage",
]

# ---------------------------------------------------------------------------
# Rule tables
# ---------------------------------------------------------------------------
RULE_TABLES = {
    "corpus-stress-validation-rules.json": {
        "schema": SCHEMA, "rule_family": "corpus-stress-validation",
        "rules": [
            {"id": "CSV-1", "rule": "validation_id required and unique"},
            {"id": "CSV-2", "rule": "package_ids MUST be a non-empty list of resolvable package_ids"},
            {"id": "CSV-3", "rule": "validation is pointer-only deterministic — no upstream mutation"},
            {"id": "CSV-4", "rule": "validation_sha256 deterministic over canonical JSON of the per-package counts snapshot"},
            {"id": "CSV-5", "rule": "presentation/probabilistic/translation/telemetry keys forbidden"},
        ],
    },
    "runtime-hardening-scan-rules.json": {
        "schema": SCHEMA, "rule_family": "runtime-hardening-scan",
        "rules": [
            {"id": "RHS-1", "rule": "scan_id required and unique"},
            {"id": "RHS-2", "rule": "scopes MUST be a non-empty subset of {overwrite-isolation, replay-consistency, hash-consistency, lifecycle-consistency, export-reproducibility}"},
            {"id": "RHS-3", "rule": "for each scope, deterministic findings MUST be derived from existing append-only stores; no live polling"},
            {"id": "RHS-4", "rule": "reviewer-readable status enum: clean | findings (informational only; no autonomous remediation)"},
            {"id": "RHS-5", "rule": "scan_sha256 deterministic over canonical JSON"},
        ],
    },
    "reviewer-readiness-check-rules.json": {
        "schema": SCHEMA, "rule_family": "reviewer-readiness-check",
        "rules": [
            {"id": "RRC-1", "rule": "check_id required and unique"},
            {"id": "RRC-2", "rule": "package_id MUST resolve"},
            {"id": "RRC-3", "rule": "areas MUST be a non-empty subset of {onboarding, deployment, rollback, handoff, audit}"},
            {"id": "RRC-4", "rule": "deterministic checklist; for each area record satisfied=true/false with pointer-only evidence; reviewer-readable"},
            {"id": "RRC-5", "rule": "check_sha256 deterministic over canonical JSON; no AI scoring"},
        ],
    },
    "operational-regression-scan-rules.json": {
        "schema": SCHEMA, "rule_family": "operational-regression-scan",
        "rules": [
            {"id": "ORS-1", "rule": "scan_id required and unique"},
            {"id": "ORS-2", "rule": "baseline_id MUST resolve to a stability-baseline-record"},
            {"id": "ORS-3", "rule": "current upstream hashes MUST be re-derived; comparisons recorded per tracked id"},
            {"id": "ORS-4", "rule": "regression_count is the count of comparisons whose match=false; informational only"},
            {"id": "ORS-5", "rule": "scan_sha256 deterministic over canonical JSON"},
        ],
    },
    "corpus-anomaly-record-rules.json": {
        "schema": SCHEMA, "rule_family": "corpus-anomaly-record",
        "rules": [
            {"id": "CAR-1", "rule": "anomaly_id required and unique"},
            {"id": "CAR-2", "rule": "kind enum required"},
            {"id": "CAR-3", "rule": "severity enum required: informational | minor | major | blocking"},
            {"id": "CAR-4", "rule": "either package_id (resolvable) or scope='corpus' required"},
            {"id": "CAR-5", "rule": "description (string) required; references list pointer-only"},
            {"id": "CAR-6", "rule": "append-only; no autonomous remediation; reviewer-authored only"},
            {"id": "CAR-7", "rule": "anomaly_sha256 deterministic over canonical JSON"},
        ],
    },
    "deployment-rehearsal-record-rules.json": {
        "schema": SCHEMA, "rule_family": "deployment-rehearsal-record",
        "rules": [
            {"id": "DRR-1", "rule": "rehearsal_id required and unique"},
            {"id": "DRR-2", "rule": "package_id MUST resolve"},
            {"id": "DRR-3", "rule": "checklist_id MUST resolve to a Phase 58 deployment-checklist"},
            {"id": "DRR-4", "rule": "outcomes count MUST equal checklist item count; outcomes MUST cover every item_id exactly once"},
            {"id": "DRR-5", "rule": "outcome enum: pass | fail | skipped"},
            {"id": "DRR-6", "rule": "rehearsal records deterministic outcomes ONLY; no live deployment, no live activation"},
            {"id": "DRR-7", "rule": "rehearsal_sha256 deterministic over canonical JSON"},
        ],
    },
    "final-production-attestation-rules.json": {
        "schema": SCHEMA, "rule_family": "final-production-attestation",
        "rules": [
            {"id": "FPA-1", "rule": "attestation_id required and unique"},
            {"id": "FPA-2", "rule": "package_id MUST resolve"},
            {"id": "FPA-3", "rule": "readiness_audit_id, verification_id, proof_id, rehearsal_id, handoff_id MUST all resolve"},
            {"id": "FPA-4", "rule": "reviewer attribution mandatory; reviewer_conclusion (string) required"},
            {"id": "FPA-5", "rule": "attestation_sha256 deterministic over canonical JSON; append-only"},
        ],
    },
    "runtime-maintenance-summary-rules.json": {
        "schema": SCHEMA, "rule_family": "runtime-maintenance-summary",
        "rules": [
            {"id": "RMS-1", "rule": "summary_id required and unique"},
            {"id": "RMS-2", "rule": "summary aggregates pointer-only counts of records under prior runtime trees (Phase 47–58); no payload duplication"},
            {"id": "RMS-3", "rule": "no telemetry / no streaming / no dashboards"},
            {"id": "RMS-4", "rule": "summary_sha256 deterministic over canonical JSON"},
        ],
    },
    "stability-baseline-record-rules.json": {
        "schema": SCHEMA, "rule_family": "stability-baseline-record",
        "rules": [
            {"id": "SBR-1", "rule": "baseline_id required and unique"},
            {"id": "SBR-2", "rule": "package_id MUST resolve"},
            {"id": "SBR-3", "rule": "baseline_hashes are re-derived for: stable-export-hash (Phase 55), deployment-package-hash (Phase 57), readiness-audit-hash (Phase 56), reproducibility-proof-hash (Phase 58, optional)"},
            {"id": "SBR-4", "rule": "baseline_sha256 deterministic over canonical JSON of {package_id, baseline_hashes}; append-only"},
        ],
    },
    "operational-maturity-report-rules.json": {
        "schema": SCHEMA, "rule_family": "operational-maturity-report",
        "rules": [
            {"id": "OMR-1", "rule": "report_id required and unique"},
            {"id": "OMR-2", "rule": "dimensions MUST be a non-empty subset of allowed maturity dimensions"},
            {"id": "OMR-3", "rule": "reviewer_conclusion (string) required — reviewer-authored, NOT AI-generated"},
            {"id": "OMR-4", "rule": "no AI readiness claims; no autonomous scoring; aggregated counts only"},
            {"id": "OMR-5", "rule": "report_sha256 deterministic over canonical JSON; append-only"},
        ],
    },
}

NEW_EVENT_STORES = [
    "corpus-stress-validation-events",
    "runtime-hardening-scan-events",
    "reviewer-readiness-check-events",
    "operational-regression-scan-events",
    "corpus-anomaly-events",
    "deployment-rehearsal-events",
    "final-production-attestation-events",
    "runtime-maintenance-summary-events",
    "stability-baseline-events",
    "operational-maturity-report-events",
]

JS_ASSETS = {
    "ph-stress-engine.js": "corpus stress validation",
    "ph-hardening-engine.js": "runtime hardening scan",
    "ph-readiness-engine.js": "reviewer readiness check",
    "ph-regression-engine.js": "operational regression scan",
    "ph-anomaly-engine.js": "corpus anomaly record",
    "ph-rehearsal-engine.js": "deployment rehearsal record",
    "ph-attestation-engine.js": "final production attestation",
    "ph-maintenance-engine.js": "runtime maintenance summary",
    "ph-baseline-engine.js": "stability baseline record",
    "ph-maturity-engine.js": "operational maturity report",
}

CONSOLES = [
    "corpus-stress-console",
    "runtime-hardening-console",
    "reviewer-readiness-console",
    "regression-scan-console",
    "deployment-rehearsal-console",
    "production-attestation-console",
]

CSS_MARKER = "/* phase 59 — production hardening, corpus validation & final reviewer readiness closure additions */"
CSS_ADDENDUM = (
    CSS_MARKER + "\n"
    "/* Phase 59 intentionally introduces ZERO presentation rules. */\n"
    "/* Hardening + convergence; consumers own all presentation. */\n"
)

DOCTRINES = {
    "01-hardening-not-expansion.md": (
        "# Hardening, not expansion\n\n"
        "Phase 59 explicitly DOES NOT expand the constitutional substrate. The platform "
        "is operationally complete (~99%). This phase only stress-tests, validates, "
        "rehearses, and stabilizes the existing Phase 47–58 substrate. No new "
        "orchestration / semantic / synthesis / publication / replay / extraction "
        "families. No autonomous remediation. No operational scoring."
    ),
    "02-corpus-validation.md": (
        "# Corpus validation\n\n"
        "Corpus stress validations exercise large heterogeneous evidence sets across "
        "multiple manual packages, deterministically counting upstream artifacts and "
        "recording a pointer-only snapshot. Validations NEVER mutate upstream artifacts. "
        "They never normalize, repair, infer, or remediate."
    ),
    "03-deterministic-regression-protection.md": (
        "# Deterministic regression protection\n\n"
        "Stability baselines record reviewer-authoritative canonical hashes for export, "
        "deployment, audit, and reproducibility artifacts. Regression scans re-derive "
        "current hashes against the baseline and report byte-divergence. Baselines and "
        "regression scans are append-only. Reviewer remains authoritative for any "
        "remediation decision; nothing is automated."
    ),
    "04-reviewer-authoritative-attestation.md": (
        "# Reviewer-authoritative attestation\n\n"
        "Final production attestation requires reviewer attribution AND a reviewer-"
        "authored conclusion AND fully resolvable references to readiness audit, "
        "deployment verification, reproducibility proof, deployment rehearsal, and "
        "production handoff. There is NO AI scoring; there is NO autonomous readiness "
        "claim; the attestation is a reviewer signature over an existing governance graph."
    ),
    "05-no-autonomous-remediation.md": (
        "# No autonomous remediation\n\n"
        "Anomalies, regressions, hardening findings, and rehearsal failures are ALL "
        "informational and reviewer-readable. No background worker. No daemon. No auto-"
        "deploy. No auto-rollback. No auto-prioritization. Every remediation decision "
        "is a fresh reviewer-authored append-only record."
    ),
    "06-pointer-only-maintenance.md": (
        "# Pointer-only maintenance\n\n"
        "Runtime maintenance summaries aggregate pointer-only counts of records across "
        "all prior runtime trees (Phase 47–58). They NEVER duplicate payloads. They are "
        "NOT dashboards. They never poll, never stream, never broadcast."
    ),
}

REPORTS = [
    ("01-corpus-stress-validation-runtime", "Corpus stress validation runtime"),
    ("02-runtime-hardening-scan-runtime", "Runtime hardening scan runtime"),
    ("03-reviewer-readiness-check-runtime", "Reviewer readiness check runtime"),
    ("04-operational-regression-scan-runtime", "Operational regression scan runtime"),
    ("05-corpus-anomaly-tracking-runtime", "Corpus anomaly tracking runtime"),
    ("06-deployment-rehearsal-runtime", "Deployment rehearsal runtime"),
    ("07-final-production-attestation-runtime", "Final production attestation runtime"),
    ("08-runtime-maintenance-summary-runtime", "Runtime maintenance summary runtime"),
    ("09-stability-baseline-runtime", "Stability baseline runtime"),
    ("10-phase59-platform-maturity-final-reassessment", "Phase 59 platform maturity — final reassessment"),
]

RUNTIME_README_MARKER = "## phase 59 — production hardening, corpus validation & final reviewer readiness closure"
RUNTIME_README_ADDENDUM = (
    RUNTIME_README_MARKER + "\n\n"
    f"- schema: `{SCHEMA}`\n"
    f"- constitutional layer: {LAYER} (HARDENING + CONVERGENCE — not constitutional expansion)\n"
    "- storage tree: `operational-console/production-hardening-runtime/`\n"
    "- 10 storage subdirs: corpus-stress-validations, runtime-hardening-scans,\n"
    "  reviewer-readiness-checks, operational-regression-scans, corpus-anomaly-records,\n"
    "  deployment-rehearsal-records, final-production-attestations,\n"
    "  runtime-maintenance-summaries, stability-baseline-records,\n"
    "  operational-maturity-reports.\n"
    "- 10 dispatch kinds: corpus-stress-validation, runtime-hardening-scan,\n"
    "  reviewer-readiness-check, operational-regression-scan, corpus-anomaly-record,\n"
    "  deployment-rehearsal-record, final-production-attestation,\n"
    "  runtime-maintenance-summary, stability-baseline-record, operational-maturity-report.\n"
    "- posture: production hardening + corpus validation + operational stability +\n"
    "  deterministic regression protection + reviewer confidence over architectural growth;\n"
    "  pointer-only artifacts; deterministic only; NO embeddings; NO vector DBs;\n"
    "  NO probabilistic inference; NO ML / LLMs / MT; NO autonomous agents;\n"
    "  NO autonomous remediation; NO operational scoring; NO AI readiness claims;\n"
    "  NO behavior tracking; NO analytics; NO telemetry; NO dashboards;\n"
    "  NO operational automation; NO deployment automation; NO background workers;\n"
    "  NO hidden propagation; NO hidden runtime mutation; reviewer-authoritative;\n"
    "  lineage-preserving; presentation-neutral; writes ONLY into the layer's own\n"
    "  runtime tree.\n"
    "- this is the production hardening + corpus validation layer that stress-tests,\n"
    "  validates, rehearses, attests, and stabilizes the Phase 47–58 substrate without\n"
    "  any new architectural expansion.\n"
)


def _now() -> str:
    return _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_if_missing(p: Path, content: str) -> bool:
    if p.exists():
        return False
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return True


def write_json_if_missing(p: Path, data: dict) -> bool:
    return write_if_missing(p, json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def main() -> None:
    storage_roots_created = 0
    if write_if_missing(PH_ROOT / "README.md",
        f"# production-hardening-runtime\n\nPhase 59 / layer {LAYER}. Schema `{SCHEMA}`.\n"):
        storage_roots_created += 1
    for sub in PH_SUBDIRS:
        d = PH_ROOT / sub
        if write_if_missing(d / ".gitkeep", ""):
            storage_roots_created += 1
        write_if_missing(d / "README.md", f"# {sub}\n\nPhase 59 / layer {LAYER}.\n")

    for fn, body in RULE_TABLES.items():
        rules_path = RULES_ROOT / fn
        rules_path.parent.mkdir(parents=True, exist_ok=True)
        rules_path.write_text(json.dumps(body, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    new_event_stores_created = 0
    for s in NEW_EVENT_STORES:
        f = RUNTIME_MANIFESTS_ROOT / s / "_event-store.json"
        if write_json_if_missing(f, {
            "schema": "governed-fs-event-store/1.0",
            "kind": s,
            "constitutional_layer_index": LAYER,
            "created_at": _now(),
            "append_only": True,
            "deterministic": True,
            "reviewer_authoritative": True,
            "events": [],
        }):
            new_event_stores_created += 1

    for fn, summary in JS_ASSETS.items():
        body = (
            f"// {fn} — Phase 59 ({summary})\n"
            "// vanilla ES; attaches to window.OC.*; throws on missing reviewer;\n"
            "// builds envelopes via OC.FSBridge.buildRequestEnvelope; never writes FS directly.\n"
            "(function (global) {\n"
            "  'use strict';\n"
            "  const OC = global.OC = global.OC || {};\n"
            f"  OC.{fn.replace('.js','').replace('-','_')} = OC.{fn.replace('.js','').replace('-','_')} || Object.freeze({{\n"
            f"    schema: '{SCHEMA}',\n"
            f"    layer: {LAYER},\n"
            "    requireReviewer(reviewer) {\n"
            "      if (typeof reviewer !== 'string' || !reviewer.trim()) {\n"
            "        throw new Error('reviewer attribution required');\n"
            "      }\n"
            "      return reviewer;\n"
            "    },\n"
            "    buildEnvelope(kind, reviewer, payload) {\n"
            "      this.requireReviewer(reviewer);\n"
            "      if (!OC.FSBridge || !OC.FSBridge.buildRequestEnvelope) {\n"
            "        throw new Error('OC.FSBridge.buildRequestEnvelope unavailable');\n"
            "      }\n"
            "      return OC.FSBridge.buildRequestEnvelope({ kind, reviewer, payload });\n"
            "    }\n"
            "  });\n"
            "})(typeof window !== 'undefined' ? window : globalThis);\n"
        )
        write_if_missing(ASSETS_EXEC_ROOT / fn, body)

    for c in CONSOLES:
        write_if_missing(OC_ROOT / c / "exec.html",
            "<!doctype html>\n<meta charset=utf-8>\n"
            f"<title>{c} — phase {LAYER}</title>\n"
            f"<!-- presentation-neutral phase 59 console — schema {SCHEMA} -->\n"
            f"<main data-phase=\"{LAYER}\" data-console=\"{c}\"></main>\n"
        )

    doctrine_root = KB_ROOT / "GOVERNED_PRODUCTION_HARDENING_CORPUS_VALIDATION_GOVERNANCE"
    write_if_missing(doctrine_root / "00-INDEX.md",
        f"# GOVERNED PRODUCTION HARDENING CORPUS VALIDATION (layer {LAYER})\n\n"
        + "\n".join(f"- {n}" for n in sorted(DOCTRINES.keys())) + "\n"
    )
    for fn, body in DOCTRINES.items():
        write_if_missing(doctrine_root / fn, body + "\n")
    write_json_if_missing(doctrine_root / "manifest.json", {
        "schema": SCHEMA,
        "constitutional_layer_index": LAYER,
        "doctrine_count": len(DOCTRINES),
        "subordinate_to": SUBORDINATE_TO,
        "posture": POSTURE,
        "hardening_scopes": HARDENING_SCOPES,
        "readiness_areas": READINESS_AREAS,
        "anomaly_kinds": ANOMALY_KINDS,
        "anomaly_severities": ANOMALY_SEVERITIES,
        "rehearsal_outcomes": REHEARSAL_OUTCOMES,
        "maturity_dimensions": MATURITY_DIMENSIONS,
    })

    reports_dir = REPORTS_ROOT / "production-hardening-corpus-validation"
    write_if_missing(reports_dir / "README.md",
        f"# production-hardening-corpus-validation reports\n\nPhase 59 / layer {LAYER}.\n"
    )
    for slug, title in REPORTS:
        write_json_if_missing(reports_dir / f"{slug}.json", {
            "schema": SCHEMA,
            "report": slug,
            "title": title,
            "constitutional_layer_index": LAYER,
        })
        write_if_missing(reports_dir / f"{slug}.md",
            f"# {title}\n\nPhase 59 / layer {LAYER}. Schema `{SCHEMA}`.\n"
        )

    css_path = ASSETS_EXEC_ROOT / "exec.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    existing = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    if CSS_MARKER not in existing:
        css_path.write_text(existing + ("\n" if existing and not existing.endswith("\n") else "") + CSS_ADDENDUM, encoding="utf-8")

    rr_path = OC_ROOT / "RUNTIME_README.md"
    rr_existing = rr_path.read_text(encoding="utf-8") if rr_path.exists() else "# RUNTIME_README\n\n"
    rr_addendum_added = 0
    if RUNTIME_README_MARKER not in rr_existing:
        rr_path.write_text(rr_existing + ("\n" if rr_existing and not rr_existing.endswith("\n") else "") + "\n" + RUNTIME_README_ADDENDUM, encoding="utf-8")
        rr_addendum_added = 1

    print(
        "Phase 59 — production hardening, corpus validation & final reviewer readiness closure written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {storage_roots_created} | New event stores: {new_event_stores_created} | "
        f"Rule tables: {len(RULE_TABLES)} | JS assets: {len(JS_ASSETS)} | Exec consoles: {len(CONSOLES)} | "
        f"Doctrines: {len(DOCTRINES)} | Reports: {len(REPORTS)} | RUNTIME_README addendum: {rr_addendum_added}"
    )


if __name__ == "__main__":
    main()
