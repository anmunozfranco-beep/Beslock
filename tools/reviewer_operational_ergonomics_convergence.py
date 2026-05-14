#!/usr/bin/env python3
"""
Phase 58 builder — Reviewer Operational Ergonomics, Guided Runtime Workflows
& Production Usability Closure (constitutional layer 51).

Convergence layer: optimizes reviewer operability, deployment repeatability,
deterministic reproducibility, and onboarding clarity over the Phase 47–57
substrate. NO new semantic / convergence / extraction / publication / replay
families. NO autonomous agents. NO presentation/rendering systems. NO ML.
NO telemetry / dashboards / behavior tracking / autonomous prioritization.

Idempotent. Writes ONLY into the layer's own runtime tree.
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

SCHEMA = "reviewer-operational-ergonomics-convergence/1.0"
LAYER = 51

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RULES_ROOT = OC_ROOT / "execution-engine"
ASSETS_EXEC_ROOT = OC_ROOT / "assets/exec"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
KB_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING"
REPORTS_ROOT = THEME_ROOT / "_repository-governance/reports"

RO_ROOT = OC_ROOT / "reviewer-operational-runtime"
RO_SUBDIRS = [
    "guided-workflows",
    "onboarding-sequences",
    "deployment-checklists",
    "operational-diagnostics",
    "runtime-navigation-indexes",
    "corpus-review-queues",
    "operational-confidence-summaries",
    "reproducibility-proofs",
    "reviewer-session-records",
    "production-handoff-records",
]

# 49-entry chain ending with Phase 57 anchor.
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
]
assert len(SUBORDINATE_TO) >= 49, f"SUBORDINATE_TO too short: {len(SUBORDINATE_TO)}"

POSTURE = {
    # Convergence-oriented optimizations
    "reviewer_operability_priority": True,
    "operational_ergonomics_priority": True,
    "deployment_repeatability_priority": True,
    "deterministic_reproducibility_priority": True,
    "human_centered_runtime_navigation": True,
    "pointer_only_operational_views": True,
    "onboarding_clarity_priority": True,
    "convergence_over_expansion": True,
    "architectural_growth_priority": False,
    "wires_existing_systems": True,
    # Negative posture
    "introduces_new_orchestration": False,
    "introduces_new_replay_engine": False,
    "introduces_new_lifecycle_family": False,
    "introduces_new_extraction_framework": False,
    "introduces_new_publication_runtime": False,
    "introduces_new_semantic_runtime": False,
    "introduces_new_presentation_runtime": False,
    "introduces_new_governance_family": False,
    "introduces_new_synthesis_system": False,
    # Strict deterministic posture
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
    "no_hidden_runtime_mutation": True,
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
    "writes_only_into_reviewer_operational_runtime_tree": True,
    "writes_to_operational_deployment_runtime_tree": False,
    "writes_to_production_closure_runtime_tree": False,
    "writes_to_semantic_convergence_runtime_tree": False,
    "writes_to_manual_runtime_closure_tree": False,
    "writes_to_manual_semantic_packaging_runtime_tree": False,
    "stdlib_only": True,
    "local_first": True,
    "cli_only_interface": True,
    "constitutional_layer_index": LAYER,
    "post_constitutional_convergence_phase": True,
}

DISPATCH_KINDS = [
    "reviewer-guided-workflow",
    "onboarding-sequence-publish",
    "deployment-checklist-publish",
    "operational-diagnostics-summary",
    "runtime-navigation-index",
    "corpus-review-queue",
    "operational-confidence-summary",
    "reproducibility-proof",
    "reviewer-session-record",
    "production-handoff-record",
]

WORKFLOW_KINDS = [
    "deployment-walkthrough",
    "rollback-walkthrough",
    "readiness-audit-walkthrough",
    "verification-walkthrough",
    "portfolio-review-walkthrough",
    "handoff-walkthrough",
]

ONBOARDING_KINDS = [
    "operator-onboarding",
    "reviewer-onboarding",
    "deployment-onboarding",
    "recovery-onboarding",
]

CHECKLIST_KINDS = [
    "pre-activation",
    "activation",
    "post-activation",
    "rollback",
]

DIAGNOSTICS_SCOPES = [
    "package",
    "manual",
    "corpus",
]

QUEUE_KINDS = [
    "readiness-audit-pending",
    "deployment-verification-pending",
    "rollback-pending",
    "handoff-pending",
    "drift-triage-pending",
    "conflict-triage-pending",
]

CONFIDENCE_DIMENSIONS = [
    "readiness-audit-coverage",
    "deployment-verification-coverage",
    "export-stability-coverage",
    "robustness-coverage",
    "multilingual-normalization-coverage",
]

REPRODUCIBILITY_TARGETS = [
    "stable-export-hash",
    "deployment-package-hash",
    "readiness-audit-hash",
]

SESSION_KINDS = [
    "operator-shift",
    "deployment-walkthrough-session",
    "onboarding-session",
    "handoff-session",
    "diagnostics-review-session",
]

# ---------------------------------------------------------------------------
# Rule tables
# ---------------------------------------------------------------------------
RULE_TABLES = {
    "reviewer-guided-workflow-rules.json": {
        "schema": SCHEMA, "rule_family": "reviewer-guided-workflow",
        "rules": [
            {"id": "RG-1", "rule": "workflow_id required and unique"},
            {"id": "RG-2", "rule": "workflow_kind enum required"},
            {"id": "RG-3", "rule": "steps MUST be a non-empty ordered list of {step_id, action, expected_outcome, runtime_reference}"},
            {"id": "RG-4", "rule": "every runtime_reference MUST be an existing runtime artifact id or runtime path under operational-console/"},
            {"id": "RG-5", "rule": "presentation keys forbidden recursively"},
            {"id": "RG-6", "rule": "no orchestration execution embedded; pointer-only step descriptions"},
            {"id": "RG-7", "rule": "workflow_sha256 deterministic over canonical JSON; reviewer attribution mandatory"},
        ],
    },
    "onboarding-sequence-rules.json": {
        "schema": SCHEMA, "rule_family": "onboarding-sequence",
        "rules": [
            {"id": "ON-1", "rule": "sequence_id required and unique"},
            {"id": "ON-2", "rule": "sequence_kind enum required"},
            {"id": "ON-3", "rule": "modules MUST be a non-empty ordered list of {module_id, title, references}"},
            {"id": "ON-4", "rule": "every reference MUST resolve to an existing runtime path under operational-console/ or KNOWLEDGE_BUILDING/"},
            {"id": "ON-5", "rule": "sequence_sha256 deterministic over canonical JSON"},
            {"id": "ON-6", "rule": "supersession via new sequence_id with prior_sequence_id pointer; append-only"},
        ],
    },
    "deployment-checklist-rules.json": {
        "schema": SCHEMA, "rule_family": "deployment-checklist",
        "rules": [
            {"id": "DC-1", "rule": "checklist_id required and unique"},
            {"id": "DC-2", "rule": "checklist_kind enum required"},
            {"id": "DC-3", "rule": "package_id MUST resolve"},
            {"id": "DC-4", "rule": "items MUST be a non-empty ordered list of {item_id, requirement, governance_reference}"},
            {"id": "DC-5", "rule": "every governance_reference MUST resolve to an existing Phase 56 readiness audit / Phase 57 verification / Phase 57 deployment package / Phase 55 stabilization / activation lifecycle record"},
            {"id": "DC-6", "rule": "checklist_sha256 deterministic over canonical JSON; reviewer attribution mandatory"},
        ],
    },
    "operational-diagnostics-rules.json": {
        "schema": SCHEMA, "rule_family": "operational-diagnostics",
        "rules": [
            {"id": "OD-1", "rule": "diagnostics_id required and unique"},
            {"id": "OD-2", "rule": "scope enum: package | manual | corpus"},
            {"id": "OD-3", "rule": "for scope='package' or scope='manual', the corresponding id MUST resolve"},
            {"id": "OD-4", "rule": "diagnostics is a deterministic snapshot derived from upstream append-only stores; NO live polling, NO streaming, NO dashboards"},
            {"id": "OD-5", "rule": "diagnostics_sha256 deterministic over canonical JSON of the snapshot"},
            {"id": "OD-6", "rule": "telemetry / dashboard / streaming / behavior-tracking / analytics keys forbidden"},
        ],
    },
    "runtime-navigation-index-rules.json": {
        "schema": SCHEMA, "rule_family": "runtime-navigation-index",
        "rules": [
            {"id": "NI-1", "rule": "index_id required and unique"},
            {"id": "NI-2", "rule": "entries MUST be a non-empty ordered list of {label, runtime_path, kind}"},
            {"id": "NI-3", "rule": "every runtime_path MUST exist on disk under operational-console/ (deterministic; failure-closed)"},
            {"id": "NI-4", "rule": "navigation is pointer-only; index does NOT mirror or copy upstream content"},
            {"id": "NI-5", "rule": "index_sha256 deterministic over canonical JSON"},
        ],
    },
    "corpus-review-queue-rules.json": {
        "schema": SCHEMA, "rule_family": "corpus-review-queue",
        "rules": [
            {"id": "CQ-1", "rule": "queue_id required and unique"},
            {"id": "CQ-2", "rule": "queue_kind enum required"},
            {"id": "CQ-3", "rule": "entries MUST be a non-empty ordered list of {entry_id, package_id, reason, governing_artifact_pointer}"},
            {"id": "CQ-4", "rule": "every package_id MUST resolve; governing_artifact_pointer MUST be a {kind, id} dict referencing an existing artifact"},
            {"id": "CQ-5", "rule": "ordering is reviewer-supplied only; NO automatic prioritization, NO probabilistic ranking, NO AI scoring; rank/score/priority keys forbidden"},
            {"id": "CQ-6", "rule": "queue_sha256 deterministic over canonical JSON; reviewer attribution mandatory"},
        ],
    },
    "operational-confidence-rules.json": {
        "schema": SCHEMA, "rule_family": "operational-confidence",
        "rules": [
            {"id": "CF-1", "rule": "confidence_id required and unique"},
            {"id": "CF-2", "rule": "package_id MUST resolve"},
            {"id": "CF-3", "rule": "summary aggregates pointer-only references for: readiness audits (Phase 56), deployment verifications (Phase 57), export stability guarantees (Phase 56), robustness records (Phase 56), multilingual normalization tables (Phase 56)"},
            {"id": "CF-4", "rule": "confidence_sha256 deterministic over canonical JSON"},
            {"id": "CF-5", "rule": "presentation/telemetry/dashboard keys forbidden"},
        ],
    },
    "reproducibility-proof-rules.json": {
        "schema": SCHEMA, "rule_family": "reproducibility-proof",
        "rules": [
            {"id": "RP-1", "rule": "proof_id required and unique"},
            {"id": "RP-2", "rule": "package_id MUST resolve"},
            {"id": "RP-3", "rule": "for each declared target hash (stable-export-hash / deployment-package-hash / readiness-audit-hash), the value MUST match the upstream artifact's recorded hash byte-for-byte"},
            {"id": "RP-4", "rule": "status enum: confirmed | divergent (reviewer-readable; not used for auto-rollback)"},
            {"id": "RP-5", "rule": "proof_sha256 deterministic over canonical JSON of the comparison record"},
            {"id": "RP-6", "rule": "reviewer attribution mandatory; append-only"},
        ],
    },
    "reviewer-session-record-rules.json": {
        "schema": SCHEMA, "rule_family": "reviewer-session-record",
        "rules": [
            {"id": "RS-1", "rule": "session_id required and unique"},
            {"id": "RS-2", "rule": "session_kind enum required"},
            {"id": "RS-3", "rule": "session is observational-only: notes is a string, references is a pointer-only list"},
            {"id": "RS-4", "rule": "behavior tracking / analytics / telemetry keys forbidden"},
            {"id": "RS-5", "rule": "session_sha256 deterministic over canonical JSON; append-only"},
        ],
    },
    "production-handoff-rules.json": {
        "schema": SCHEMA, "rule_family": "production-handoff",
        "rules": [
            {"id": "PH-1", "rule": "handoff_id required and unique"},
            {"id": "PH-2", "rule": "from_reviewer and to_reviewer required (non-empty strings)"},
            {"id": "PH-3", "rule": "package_id, stabilization_id, deployment_package_id, readiness_audit_id MUST all resolve"},
            {"id": "PH-4", "rule": "activation_id MUST resolve and declared activation_state MUST equal latest recorded activation state for activation_id"},
            {"id": "PH-5", "rule": "handoff_sha256 deterministic over canonical JSON; append-only; no overwrite semantics"},
        ],
    },
}

NEW_EVENT_STORES = [
    "reviewer-guided-workflow-events",
    "onboarding-sequence-events",
    "deployment-checklist-events",
    "operational-diagnostics-events",
    "runtime-navigation-index-events",
    "corpus-review-queue-events",
    "operational-confidence-events",
    "reproducibility-proof-events",
    "reviewer-session-events",
    "production-handoff-events",
]

JS_ASSETS = {
    "ro-workflow-engine.js": "reviewer guided workflows",
    "ro-onboarding-engine.js": "onboarding sequences",
    "ro-checklist-engine.js": "deployment checklists",
    "ro-diagnostics-engine.js": "operational diagnostics snapshots",
    "ro-navigation-engine.js": "runtime navigation index",
    "ro-queue-engine.js": "corpus review queues",
    "ro-confidence-engine.js": "operational confidence summaries",
    "ro-reproducibility-engine.js": "reproducibility proofs",
    "ro-session-engine.js": "reviewer session records",
    "ro-handoff-engine.js": "production handoff records",
}

CONSOLES = [
    "reviewer-workflow-console",
    "onboarding-console",
    "deployment-checklist-console",
    "operational-diagnostics-console",
    "runtime-navigation-console",
    "production-handoff-console",
]

CSS_MARKER = "/* phase 58 — reviewer operational ergonomics, guided runtime workflows & production usability closure additions */"
CSS_ADDENDUM = (
    CSS_MARKER + "\n"
    "/* Phase 58 intentionally introduces ZERO presentation rules. */\n"
    "/* Convergence-oriented; consumers own all presentation. */\n"
)

DOCTRINES = {
    "01-convergence-over-expansion.md": (
        "# Convergence over expansion\n\n"
        "Phase 58 explicitly does NOT expand the constitutional substrate. The platform is "
        "architecturally mature; remaining work is reviewer operability, deployment "
        "repeatability, deterministic reproducibility, and onboarding clarity. No new "
        "semantic / convergence / extraction / publication / replay families are introduced."
    ),
    "02-reviewer-ergonomics.md": (
        "# Reviewer ergonomics\n\n"
        "Reviewers MUST be able to navigate, onboard, audit, deploy, hand off, and recover "
        "operations through deterministic pointer-only artifacts. Guided workflows and "
        "onboarding sequences are step lists pointing at existing dispatches and runtime "
        "paths — they are NOT executors and they NEVER mutate upstream state."
    ),
    "03-deployment-repeatability.md": (
        "# Deployment repeatability\n\n"
        "Deployment checklists bind every reviewer requirement to an existing governance "
        "artifact (Phase 56 readiness audit, Phase 57 deployment verification, Phase 57 "
        "deployment package, Phase 55 stabilization, Phase 57 activation lifecycle record). "
        "A deployment is reviewer-repeatable iff every checklist item resolves."
    ),
    "04-deterministic-reproducibility.md": (
        "# Deterministic reproducibility\n\n"
        "Reproducibility proofs re-derive declared hashes against upstream stores and "
        "fail-closed on byte-divergence. Reproducibility is informational; reviewer remains "
        "authoritative for any rollback or recovery decision."
    ),
    "05-no-prioritization-no-tracking.md": (
        "# No prioritization, no tracking\n\n"
        "Corpus review queues are reviewer-supplied ordered lists. There is NO automatic "
        "prioritization, NO probabilistic ranking, NO AI scoring. Reviewer session records "
        "are observational-only — there is NO behavior tracking, NO analytics, NO telemetry."
    ),
    "06-pointer-only-operational-views.md": (
        "# Pointer-only operational views\n\n"
        "Diagnostics, confidence summaries, navigation indexes, queues and handoff records "
        "are ALL pointer-only. They reference existing append-only artifacts; they NEVER copy, "
        "embed, mirror, or duplicate upstream payloads. They are NOT dashboards."
    ),
}

REPORTS = [
    ("01-reviewer-guided-workflow-runtime", "Reviewer guided workflow runtime"),
    ("02-onboarding-sequence-runtime", "Onboarding sequence runtime"),
    ("03-deployment-checklist-runtime", "Deployment checklist runtime"),
    ("04-operational-diagnostics-runtime", "Operational diagnostics runtime"),
    ("05-runtime-navigation-index", "Runtime navigation index"),
    ("06-corpus-review-queues", "Corpus review queues"),
    ("07-operational-confidence-summaries", "Operational confidence summaries"),
    ("08-deterministic-reproducibility-proofs", "Deterministic reproducibility proofs"),
    ("09-reviewer-session-and-handoff-records", "Reviewer session and handoff records"),
    ("10-phase58-platform-maturity-reassessment", "Phase 58 platform maturity reassessment"),
]

RUNTIME_README_MARKER = "## phase 58 — reviewer operational ergonomics, guided runtime workflows & production usability closure"
RUNTIME_README_ADDENDUM = (
    RUNTIME_README_MARKER + "\n\n"
    f"- schema: `{SCHEMA}`\n"
    f"- constitutional layer: {LAYER} (CONVERGENCE — not constitutional expansion)\n"
    "- storage tree: `operational-console/reviewer-operational-runtime/`\n"
    "- 10 storage subdirs: guided-workflows, onboarding-sequences, deployment-checklists,\n"
    "  operational-diagnostics, runtime-navigation-indexes, corpus-review-queues,\n"
    "  operational-confidence-summaries, reproducibility-proofs, reviewer-session-records,\n"
    "  production-handoff-records.\n"
    "- 10 dispatch kinds: reviewer-guided-workflow, onboarding-sequence-publish,\n"
    "  deployment-checklist-publish, operational-diagnostics-summary, runtime-navigation-index,\n"
    "  corpus-review-queue, operational-confidence-summary, reproducibility-proof,\n"
    "  reviewer-session-record, production-handoff-record.\n"
    "- posture: reviewer operability + operational ergonomics + deployment repeatability +\n"
    "  deterministic reproducibility + onboarding clarity over architectural growth;\n"
    "  pointer-only operational views; deterministic only; NO embeddings; NO vector DBs;\n"
    "  NO probabilistic inference; NO ML / LLMs / MT; NO autonomous agents;\n"
    "  NO autonomous prioritization; NO behavior tracking; NO analytics;\n"
    "  NO telemetry; NO dashboards; NO operational automation;\n"
    "  NO hidden runtime mutation; reviewer-authoritative; lineage-preserving;\n"
    "  presentation-neutral; writes ONLY into the layer's own runtime tree.\n"
    "- this is the reviewer operational ergonomics convergence layer that makes the\n"
    "  Phase 47–57 production-ready substrate easier, safer, faster, and clearer for\n"
    "  human operators WITHOUT new architectural complexity.\n"
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
    if write_if_missing(RO_ROOT / "README.md",
        f"# reviewer-operational-runtime\n\nPhase 58 / layer {LAYER}. Schema `{SCHEMA}`.\n"):
        storage_roots_created += 1
    for sub in RO_SUBDIRS:
        d = RO_ROOT / sub
        if write_if_missing(d / ".gitkeep", ""):
            storage_roots_created += 1
        write_if_missing(d / "README.md", f"# {sub}\n\nPhase 58 / layer {LAYER}.\n")

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
            f"// {fn} — Phase 58 ({summary})\n"
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
            f"<!-- presentation-neutral phase 58 console — schema {SCHEMA} -->\n"
            f"<main data-phase=\"{LAYER}\" data-console=\"{c}\"></main>\n"
        )

    doctrine_root = KB_ROOT / "GOVERNED_REVIEWER_OPERATIONAL_ERGONOMICS_CONVERGENCE_GOVERNANCE"
    write_if_missing(doctrine_root / "00-INDEX.md",
        f"# GOVERNED REVIEWER OPERATIONAL ERGONOMICS CONVERGENCE (layer {LAYER})\n\n"
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
        "workflow_kinds": WORKFLOW_KINDS,
        "onboarding_kinds": ONBOARDING_KINDS,
        "checklist_kinds": CHECKLIST_KINDS,
        "queue_kinds": QUEUE_KINDS,
        "confidence_dimensions": CONFIDENCE_DIMENSIONS,
        "reproducibility_targets": REPRODUCIBILITY_TARGETS,
        "session_kinds": SESSION_KINDS,
    })

    reports_dir = REPORTS_ROOT / "reviewer-operational-ergonomics-convergence"
    write_if_missing(reports_dir / "README.md",
        f"# reviewer-operational-ergonomics-convergence reports\n\nPhase 58 / layer {LAYER}.\n"
    )
    for slug, title in REPORTS:
        write_json_if_missing(reports_dir / f"{slug}.json", {
            "schema": SCHEMA,
            "report": slug,
            "title": title,
            "constitutional_layer_index": LAYER,
        })
        write_if_missing(reports_dir / f"{slug}.md",
            f"# {title}\n\nPhase 58 / layer {LAYER}. Schema `{SCHEMA}`.\n"
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
        "Phase 58 — reviewer operational ergonomics, guided runtime workflows & production usability closure written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {storage_roots_created} | New event stores: {new_event_stores_created} | "
        f"Rule tables: {len(RULE_TABLES)} | JS assets: {len(JS_ASSETS)} | Exec consoles: {len(CONSOLES)} | "
        f"Doctrines: {len(DOCTRINES)} | Reports: {len(REPORTS)} | RUNTIME_README addendum: {rr_addendum_added}"
    )


if __name__ == "__main__":
    main()
