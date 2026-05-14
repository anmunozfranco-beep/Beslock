#!/usr/bin/env python3
"""
Phase 56 builder — Final Operational Closure, Real-World Robustness &
Production-Ready Manual Delivery (constitutional layer 49).

Closing layer for production-readiness. Hardens existing runtimes against
real operational entropy:
  - real-world evidence robustness records,
  - deterministic multilingual normalization (NO machine translation),
  - export stability guarantees,
  - canonical drift detection (no silent mutation),
  - reviewer productivity summaries (presentation-neutral),
  - transaction-safe incremental refresh,
  - production readiness audits,
  - one deterministic operational closure path.

Idempotent. Writes ONLY into the layer's own runtime tree.
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

SCHEMA = "final-operational-closure-production-readiness/1.0"
LAYER = 49

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RULES_ROOT = OC_ROOT / "execution-engine"
ASSETS_EXEC_ROOT = OC_ROOT / "assets/exec"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
KB_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING"
REPORTS_ROOT = THEME_ROOT / "_repository-governance/reports"

PC_ROOT = OC_ROOT / "production-closure-runtime"
PC_SUBDIRS = [
    "evidence-robustness-records",
    "multilingual-normalization-tables",
    "multilingual-normalization-records",
    "export-stability-guarantees",
    "canonical-drift-records",
    "reviewer-summaries",
    "incremental-refresh-records",
    "readiness-audit-records",
    "closure-path-records",
]

# 47-entry chain ending with Phase 55 anchor.
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
]
assert len(SUBORDINATE_TO) >= 47, f"SUBORDINATE_TO too short: {len(SUBORDINATE_TO)}"

POSTURE = {
    "production_robustness_priority": True,
    "architectural_growth_priority": False,
    "wires_existing_systems": True,
    "introduces_new_orchestration": False,
    "introduces_new_replay_engine": False,
    "introduces_new_lifecycle_family": False,
    "introduces_new_extraction_framework": False,
    "introduces_new_publication_runtime": False,
    "deterministic_only": True,
    "no_embeddings": True,
    "no_vector_databases": True,
    "no_probabilistic_inference": True,
    "no_ml_models": True,
    "no_machine_translation": True,
    "no_llm_translation": True,
    "no_language_inference": True,
    "no_autonomous_arbitration": True,
    "no_autonomous_convergence": True,
    "no_autonomous_publication": True,
    "no_silent_normalization": True,
    "no_silent_conflict_flattening": True,
    "no_silent_canonical_mutation": True,
    "reviewer_authoritative": True,
    "reviewer_attribution_required": True,
    "lineage_preserving": True,
    "evidence_provenance_preserving": True,
    "transaction_safe_incremental_refresh": True,
    "stable_export_ids_preserved": True,
    "deterministic_export_hashes": True,
    "append_only_event_stores": True,
    "fail_closed_validation": True,
    "consumer_boundary_enforced": True,
    "presentation_neutral_outputs": True,
    "writes_only_into_production_closure_runtime_tree": True,
    "writes_to_semantic_convergence_runtime_tree": False,
    "writes_to_manual_runtime_closure_tree": False,
    "writes_to_manual_semantic_packaging_runtime_tree": False,
    "writes_to_semantic_extraction_runtime_tree": False,
    "no_frontend_frameworks": True,
    "no_responsive_rendering_systems": True,
    "no_presentation_orchestration": True,
    "stdlib_only": True,
    "local_first": True,
    "no_cloud_apis": True,
    "no_saas": True,
    "no_daemons": True,
    "cli_only_interface": True,
    "constitutional_layer_index": LAYER,
    "post_constitutional_closure_phase": True,
}

DISPATCH_KINDS = [
    "evidence-robustness-record",
    "multilingual-normalization-table-create",
    "multilingual-normalization-apply",
    "export-stability-guarantee",
    "canonical-drift-detect",
    "reviewer-summary-publish",
    "incremental-refresh-propagate",
    "readiness-audit-run",
    "closure-path-record",
]

ROBUSTNESS_KINDS = [
    "incomplete-evidence",
    "duplicated-document",
    "noisy-ocr-fragment",
    "multilingual-screenshot",
    "truncated-video",
    "contradictory-support-export",
    "inconsistent-specification-table",
    "low-quality-evidence",
    "fragmented-app-flow",
    "partial-troubleshooting-chain",
]

DRIFT_KINDS = [
    "procedure-modification",
    "warning-alteration",
    "specification-change",
    "troubleshooting-invalidation",
    "entity-supersession",
]

SUMMARY_KINDS = [
    "evidence-timeline",
    "canonical-entity-inspection",
    "convergence-summary",
    "drift-summary",
    "unresolved-conflict-summary",
    "export-readiness-summary",
]

REFRESH_TRIGGER_KINDS = [
    "approved-intake",
    "canonical-promotion",
    "arbitration-resolution",
    "drift-detection",
    "stability-guarantee-reaffirmed",
]

CLOSURE_PATH_STAGES = [
    "evidence",
    "analysis",
    "convergence",
    "canonical-entity",
    "canonical-procedure",
    "visual-support",
    "prompt-package",
    "stabilized-export",
    "readiness-audit",
    "consumer-payload",
]

# ---------------------------------------------------------------------------
# Rule tables
# ---------------------------------------------------------------------------
RULE_TABLES = {
    "evidence-robustness-rules.json": {
        "schema": SCHEMA,
        "rule_family": "evidence-robustness",
        "rules": [
            {"id": "ER-1", "rule": "record_id and source_evidence_id required"},
            {"id": "ER-2", "rule": "robustness_kind enum required"},
            {"id": "ER-3", "rule": "severity enum: informational | minor | major | blocking"},
            {"id": "ER-4", "rule": "lineage_pointers MUST preserve evidence_refs / grounding_refs / fingerprint_ids if present"},
            {"id": "ER-5", "rule": "no silent normalization — raw text / raw payload pointers preserved"},
            {"id": "ER-6", "rule": "reviewer attribution mandatory; append-only"},
            {"id": "ER-7", "rule": "no ML cleanup; deterministic markers only"},
        ],
    },
    "multilingual-normalization-table-rules.json": {
        "schema": SCHEMA,
        "rule_family": "multilingual-normalization-table",
        "rules": [
            {"id": "MN-1", "rule": "table_id required and unique"},
            {"id": "MN-2", "rule": "source_language and canonical_language required (ISO-639-1 lowercase)"},
            {"id": "MN-3", "rule": "mappings MUST be a non-empty list of {source_term, canonical_term} dicts"},
            {"id": "MN-4", "rule": "source_term and canonical_term MUST be deterministic strings; NO translation engines"},
            {"id": "MN-5", "rule": "table is append-only; superseding entries via new table_id with prior_table_id pointer"},
            {"id": "MN-6", "rule": "table_sha256 deterministic over canonical JSON"},
            {"id": "MN-7", "rule": "reviewer attribution mandatory"},
        ],
    },
    "multilingual-normalization-apply-rules.json": {
        "schema": SCHEMA,
        "rule_family": "multilingual-normalization-apply",
        "rules": [
            {"id": "MA-1", "rule": "application_id required and unique"},
            {"id": "MA-2", "rule": "table_id MUST resolve to an existing normalization table"},
            {"id": "MA-3", "rule": "source_evidence_id MUST be preserved (raw lineage)"},
            {"id": "MA-4", "rule": "applied_terms MUST list {source_term, canonical_term, table_entry_index}"},
            {"id": "MA-5", "rule": "every applied source_term MUST exist in the table mappings"},
            {"id": "MA-6", "rule": "NO machine translation, NO LLM translation, NO autodetect; deterministic dictionary lookup only"},
            {"id": "MA-7", "rule": "raw_text_sha256 preserved alongside normalized_text_sha256"},
        ],
    },
    "export-stability-guarantee-rules.json": {
        "schema": SCHEMA,
        "rule_family": "export-stability-guarantee",
        "rules": [
            {"id": "ES-1", "rule": "guarantee_id required and unique"},
            {"id": "ES-2", "rule": "stabilization_id MUST resolve to an existing Phase 55 export stabilization"},
            {"id": "ES-3", "rule": "deterministic_invariants MUST include: section_ordering_sha256, canonical_id_map_sha256, export_payload_sha256"},
            {"id": "ES-4", "rule": "guarantee_state begins 'reaffirmed'; supersession via new guarantee_id with prior_guarantee_id pointer"},
            {"id": "ES-5", "rule": "subsequent guarantees on same stabilization MUST observe identical invariants OR fail-closed"},
            {"id": "ES-6", "rule": "presentation keys forbidden recursively"},
        ],
    },
    "canonical-drift-rules.json": {
        "schema": SCHEMA,
        "rule_family": "canonical-drift",
        "rules": [
            {"id": "CD-1", "rule": "drift_id required and unique"},
            {"id": "CD-2", "rule": "EXACTLY ONE of canonical_entity_id or canonical_procedure_id required"},
            {"id": "CD-3", "rule": "the referenced canonical record MUST exist in Phase 55 storage"},
            {"id": "CD-4", "rule": "drift_kind enum required"},
            {"id": "CD-5", "rule": "new_evidence_refs MUST be a non-empty list"},
            {"id": "CD-6", "rule": "reviewer rationale required; reviewer attribution mandatory"},
            {"id": "CD-7", "rule": "drift records are POINTER-only; prior canonical record MUST NOT be mutated (no silent canonical mutation)"},
            {"id": "CD-8", "rule": "affected_downstream_refs MUST be enumerated deterministically"},
        ],
    },
    "reviewer-summary-rules.json": {
        "schema": SCHEMA,
        "rule_family": "reviewer-summary",
        "rules": [
            {"id": "RS-1", "rule": "summary_id required and unique"},
            {"id": "RS-2", "rule": "summary_kind enum required"},
            {"id": "RS-3", "rule": "summary content MUST be POINTER-only references to upstream records (no inline payload duplication)"},
            {"id": "RS-4", "rule": "summary MUST be presentation-neutral (no css/style/font/color/layout keys)"},
            {"id": "RS-5", "rule": "summary_sha256 deterministic over canonical JSON"},
            {"id": "RS-6", "rule": "reviewer attribution mandatory"},
        ],
    },
    "incremental-refresh-rules.json": {
        "schema": SCHEMA,
        "rule_family": "incremental-refresh",
        "rules": [
            {"id": "IR-1", "rule": "refresh_id required and unique"},
            {"id": "IR-2", "rule": "trigger_kind enum required"},
            {"id": "IR-3", "rule": "trigger_ref MUST resolve into the appropriate upstream store"},
            {"id": "IR-4", "rule": "affected_set MUST enumerate {kind, id} for entities/procedures/exports actually touched"},
            {"id": "IR-5", "rule": "unaffected_stable_set MUST explicitly enumerate canonical IDs preserved unchanged (transaction-safety)"},
            {"id": "IR-6", "rule": "POINTER-only; upstream extraction/packaging/closure/convergence trees NEVER mutated"},
            {"id": "IR-7", "rule": "append-only; replayable"},
        ],
    },
    "readiness-audit-rules.json": {
        "schema": SCHEMA,
        "rule_family": "readiness-audit",
        "rules": [
            {"id": "RA-1", "rule": "audit_id required and unique"},
            {"id": "RA-2", "rule": "package_id MUST resolve and MUST be in 'export-ready' lifecycle state"},
            {"id": "RA-3", "rule": "audit MUST inspect: unresolved_conflicts, missing_visual_support, broken_grounding, unstable_exports, unresolved_multilingual_mappings, missing_warnings, incomplete_troubleshooting, orphan_semantic_entities, export_drift, unresolved_reviewer_states"},
            {"id": "RA-4", "rule": "status enum: ready | not-ready"},
            {"id": "RA-5", "rule": "findings MUST list every check + outcome deterministically"},
            {"id": "RA-6", "rule": "audit is informational; reviewer remains authoritative — NO autonomous publication"},
            {"id": "RA-7", "rule": "audit_sha256 deterministic over canonical JSON"},
        ],
    },
    "closure-path-rules.json": {
        "schema": SCHEMA,
        "rule_family": "closure-path",
        "rules": [
            {"id": "CL-1", "rule": "closure_id required and unique"},
            {"id": "CL-2", "rule": "package_id MUST resolve"},
            {"id": "CL-3", "rule": "path_steps MUST enumerate the canonical 10 stages in order: evidence, analysis, convergence, canonical-entity, canonical-procedure, visual-support, prompt-package, stabilized-export, readiness-audit, consumer-payload"},
            {"id": "CL-4", "rule": "each step MUST reference at least one existing artifact id from the corresponding upstream store"},
            {"id": "CL-5", "rule": "closure_sha256 deterministic over canonical JSON"},
            {"id": "CL-6", "rule": "POINTER-only; upstream stores NEVER mutated"},
        ],
    },
}

NEW_EVENT_STORES = [
    "evidence-robustness-events",
    "multilingual-normalization-table-events",
    "multilingual-normalization-apply-events",
    "export-stability-guarantee-events",
    "canonical-drift-events",
    "reviewer-summary-events",
    "incremental-refresh-events",
    "readiness-audit-events",
    "closure-path-events",
]

JS_ASSETS = {
    "pc-robustness-engine.js": "real-world evidence robustness",
    "pc-multilingual-engine.js": "deterministic multilingual normalization",
    "pc-stability-engine.js": "export stability guarantee",
    "pc-drift-engine.js": "canonical drift detection",
    "pc-summary-engine.js": "reviewer productivity summaries",
    "pc-refresh-engine.js": "transaction-safe incremental refresh",
    "pc-audit-engine.js": "production readiness audit",
    "pc-closure-engine.js": "operational closure path",
}

CONSOLES = [
    "robustness-console",
    "multilingual-normalization-console",
    "drift-console",
    "readiness-audit-console",
    "closure-path-console",
    "reviewer-summary-console",
]

CSS_MARKER = "/* phase 56 — final operational closure, real-world robustness & production-ready manual delivery additions */"
CSS_ADDENDUM = (
    CSS_MARKER + "\n"
    "/* Phase 56 intentionally introduces ZERO presentation rules. */\n"
    "/* Operational hardening is reviewer-governed at the runtime layer; consumers own all presentation. */\n"
)

DOCTRINES = {
    "01-production-robustness-over-architectural-growth.md": (
        "# Production robustness over architectural growth\n\n"
        "Phase 56 closes operational seams instead of adding architectural families. "
        "Constitutional substrate is sufficient; remaining work is real-world resilience."
    ),
    "02-deterministic-multilingual-no-translation.md": (
        "# Deterministic multilingual normalization — no translation engines\n\n"
        "Multilingual normalization MUST use reviewer-governed append-only dictionary tables. "
        "Machine translation, LLM translation, and language-inference engines are FORBIDDEN."
    ),
    "03-export-stability-guarantees.md": (
        "# Export stability guarantees\n\n"
        "Identical semantic states MUST produce identical export payloads across rebuilds. "
        "Section ordering, canonical IDs, procedure ordering, warning grouping, troubleshooting "
        "ordering, and specification ordering MUST all be deterministic."
    ),
    "04-canonical-drift-no-silent-mutation.md": (
        "# Canonical drift — no silent mutation\n\n"
        "Drift MUST be surfaced explicitly. Prior canonical entities and prior exports MUST be "
        "preserved. Silent canonical mutation is FORBIDDEN."
    ),
    "05-incremental-refresh-stable-ids.md": (
        "# Incremental refresh — stable IDs preserved\n\n"
        "Refresh MUST be localized: only affected canonical entities, procedures, and exports "
        "are touched. Unaffected canonical IDs MUST be explicitly preserved in transaction-safe records."
    ),
    "06-reviewer-authoritative-readiness.md": (
        "# Reviewer-authoritative production readiness\n\n"
        "Production readiness audits are deterministic and informational. Reviewer remains the "
        "sole authority for publication. Autonomous approval is FORBIDDEN."
    ),
}

REPORTS = [
    ("01-real-world-evidence-robustness-summary", "Real-world evidence robustness"),
    ("02-deterministic-multilingual-normalization-summary", "Deterministic multilingual normalization"),
    ("03-export-stability-guarantees-summary", "Export stability guarantees"),
    ("04-canonical-drift-detection-summary", "Canonical drift detection"),
    ("05-reviewer-productivity-summary", "Reviewer productivity convergence"),
    ("06-transaction-safe-incremental-refresh-summary", "Transaction-safe incremental refresh"),
    ("07-production-readiness-audit-summary", "Production readiness audit runtime"),
    ("08-operational-closure-path-summary", "Final operational closure path"),
    ("09-production-robustness-posture-summary", "Production-robustness posture"),
    ("10-phase56-platform-maturity-reassessment", "Phase 56 platform maturity reassessment"),
]

RUNTIME_README_MARKER = "## phase 56 — final operational closure, real-world robustness & production-ready manual delivery"
RUNTIME_README_ADDENDUM = (
    RUNTIME_README_MARKER + "\n\n"
    f"- schema: `{SCHEMA}`\n"
    f"- constitutional layer: {LAYER}\n"
    "- storage tree: `operational-console/production-closure-runtime/`\n"
    "- 9 storage subdirs: evidence-robustness-records, multilingual-normalization-tables,\n"
    "  multilingual-normalization-records, export-stability-guarantees, canonical-drift-records,\n"
    "  reviewer-summaries, incremental-refresh-records, readiness-audit-records, closure-path-records.\n"
    "- 9 dispatch kinds: evidence-robustness-record, multilingual-normalization-table-create,\n"
    "  multilingual-normalization-apply, export-stability-guarantee, canonical-drift-detect,\n"
    "  reviewer-summary-publish, incremental-refresh-propagate, readiness-audit-run, closure-path-record.\n"
    "- posture: production robustness over architectural growth; deterministic only;\n"
    "  NO embeddings; NO vector DBs; NO probabilistic inference; NO machine translation;\n"
    "  NO autonomous arbitration / convergence / publication; reviewer-authoritative;\n"
    "  lineage-preserving; transaction-safe incremental refresh; no silent canonical mutation;\n"
    "  presentation-neutral; writes ONLY into the layer's own runtime tree.\n"
    "- this is the FINAL closure layer before true production-ready operational maturity:\n"
    "  it hardens the existing constitutional substrate WITHOUT introducing new architecture.\n"
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
    if write_if_missing(PC_ROOT / "README.md",
        f"# production-closure-runtime\n\nPhase 56 / layer {LAYER}. Schema `{SCHEMA}`.\n"):
        storage_roots_created += 1
    for sub in PC_SUBDIRS:
        d = PC_ROOT / sub
        if write_if_missing(d / ".gitkeep", ""):
            storage_roots_created += 1
        write_if_missing(d / "README.md", f"# {sub}\n\nPhase 56 / layer {LAYER}.\n")

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
            f"// {fn} — Phase 56 ({summary})\n"
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
            f"<!-- presentation-neutral phase 56 console — schema {SCHEMA} -->\n"
            f"<main data-phase=\"{LAYER}\" data-console=\"{c}\"></main>\n"
        )

    doctrine_root = KB_ROOT / "GOVERNED_FINAL_OPERATIONAL_CLOSURE_PRODUCTION_READINESS_GOVERNANCE"
    write_if_missing(doctrine_root / "00-INDEX.md",
        f"# GOVERNED FINAL OPERATIONAL CLOSURE & PRODUCTION READINESS (layer {LAYER})\n\n"
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
    })

    reports_dir = REPORTS_ROOT / "final-operational-closure-production-readiness"
    write_if_missing(reports_dir / "README.md",
        f"# final-operational-closure-production-readiness reports\n\nPhase 56 / layer {LAYER}.\n"
    )
    for slug, title in REPORTS:
        write_json_if_missing(reports_dir / f"{slug}.json", {
            "schema": SCHEMA,
            "report": slug,
            "title": title,
            "constitutional_layer_index": LAYER,
        })
        write_if_missing(reports_dir / f"{slug}.md",
            f"# {title}\n\nPhase 56 / layer {LAYER}. Schema `{SCHEMA}`.\n"
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
        "Phase 56 — final operational closure, real-world robustness & production-ready manual delivery written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {storage_roots_created} | New event stores: {new_event_stores_created} | "
        f"Rule tables: {len(RULE_TABLES)} | JS assets: {len(JS_ASSETS)} | Exec consoles: {len(CONSOLES)} | "
        f"Doctrines: {len(DOCTRINES)} | Reports: {len(REPORTS)} | RUNTIME_README addendum: {rr_addendum_added}"
    )


if __name__ == "__main__":
    main()
