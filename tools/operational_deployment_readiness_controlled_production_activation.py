#!/usr/bin/env python3
"""
Phase 57 builder — Operational Deployment Readiness, Reviewer Enablement &
Controlled Production Activation (constitutional layer 50).

Operational activation layer: transforms the production-ready substrate
(Phases 47–56) into a deployable reviewer-operated production system.

Adds:
  - reviewer operational playbooks (ingestion / triage / readiness / export
    approval / rollback / refresh / recovery),
  - controlled production activation lifecycle (candidate → approved → active
    → superseded; rollback-candidate as a separate observable state),
  - deterministic deployment integrity verification,
  - corpus-scale operational confidence summaries (portfolio aggregation),
  - reviewer recovery / rollback playbooks,
  - operational observability summaries (presentation-neutral),
  - deployment / dependency / consumer-payload package bundles.

Idempotent. Writes ONLY into the layer's own runtime tree.
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

SCHEMA = "operational-deployment-readiness-controlled-production-activation/1.0"
LAYER = 50

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RULES_ROOT = OC_ROOT / "execution-engine"
ASSETS_EXEC_ROOT = OC_ROOT / "assets/exec"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
KB_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING"
REPORTS_ROOT = THEME_ROOT / "_repository-governance/reports"

OD_ROOT = OC_ROOT / "operational-deployment-runtime"
OD_SUBDIRS = [
    "reviewer-playbooks",
    "recovery-playbooks",
    "production-activations",
    "activation-lifecycle-records",
    "deployment-verifications",
    "portfolio-summaries",
    "observability-summaries",
    "deployment-packages",
    "dependency-manifests",
    "consumer-payload-bundles",
]

# 48-entry chain ending with Phase 56 anchor.
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
]
assert len(SUBORDINATE_TO) >= 48, f"SUBORDINATE_TO too short: {len(SUBORDINATE_TO)}"

POSTURE = {
    "operational_activation_priority": True,
    "deployability_priority": True,
    "reviewer_operability_priority": True,
    "architectural_growth_priority": False,
    "wires_existing_systems": True,
    "introduces_new_orchestration": False,
    "introduces_new_replay_engine": False,
    "introduces_new_lifecycle_family": False,
    "introduces_new_extraction_framework": False,
    "introduces_new_publication_runtime": False,
    "introduces_new_semantic_runtime": False,
    "deterministic_only": True,
    "no_embeddings": True,
    "no_vector_databases": True,
    "no_probabilistic_inference": True,
    "no_ml_models": True,
    "no_machine_translation": True,
    "no_llm_translation": True,
    "no_autonomous_arbitration": True,
    "no_autonomous_publication": True,
    "no_autonomous_activation": True,
    "no_silent_production_replacement": True,
    "no_silent_canonical_mutation": True,
    "no_overwrite_semantics": True,
    "no_dashboards": True,
    "no_telemetry": True,
    "no_frontend_frameworks": True,
    "no_responsive_rendering_systems": True,
    "no_deployment_automation_daemons": True,
    "no_cloud_apis": True,
    "no_saas": True,
    "no_daemons": True,
    "reviewer_authoritative": True,
    "reviewer_attribution_required": True,
    "lineage_preserving": True,
    "additive_lineage": True,
    "transaction_safe_activation": True,
    "rollback_governed": True,
    "append_only_event_stores": True,
    "fail_closed_validation": True,
    "consumer_boundary_enforced": True,
    "presentation_neutral_outputs": True,
    "writes_only_into_operational_deployment_runtime_tree": True,
    "writes_to_production_closure_runtime_tree": False,
    "writes_to_semantic_convergence_runtime_tree": False,
    "writes_to_manual_runtime_closure_tree": False,
    "writes_to_manual_semantic_packaging_runtime_tree": False,
    "stdlib_only": True,
    "local_first": True,
    "cli_only_interface": True,
    "constitutional_layer_index": LAYER,
    "post_constitutional_activation_phase": True,
}

DISPATCH_KINDS = [
    "reviewer-playbook-publish",
    "recovery-playbook-publish",
    "production-activation-transition",
    "deployment-verification-run",
    "portfolio-summary-publish",
    "observability-summary-publish",
    "deployment-package-build",
    "dependency-manifest-publish",
    "consumer-payload-bundle-publish",
]

PLAYBOOK_KINDS = [
    "ingestion-review",
    "conflict-triage",
    "drift-triage",
    "readiness-audit-workflow",
    "export-approval-workflow",
    "refresh-procedure",
]

RECOVERY_KINDS = [
    "bad-export-rollback",
    "corrupted-convergence-recovery",
    "invalid-refresh-rollback",
    "accidental-approval-revocation",
    "unstable-canonical-drift-recovery",
    "broken-multilingual-mapping-recovery",
]

ACTIVATION_STATES = [
    "production-candidate",
    "production-approved",
    "production-active",
    "superseded",
    "rollback-candidate",
]

ACTIVATION_TRANSITIONS = {
    # state -> allowed next states (deterministic, reviewer-authoritative)
    "production-candidate": ["production-approved", "rollback-candidate"],
    "production-approved": ["production-active", "rollback-candidate"],
    "production-active": ["superseded", "rollback-candidate"],
    "superseded": [],
    "rollback-candidate": ["superseded"],
}

VERIFICATION_CHECKS = [
    "export-completeness",
    "stable-export-hash",
    "canonical-id-continuity",
    "unresolved-drift",
    "unresolved-conflicts",
    "unresolved-visual-support",
    "unresolved-multilingual-normalization",
    "missing-lineage",
    "orphan-semantic-entities",
]

PORTFOLIO_DIMENSIONS = [
    "package-readiness",
    "unresolved-issue-density",
    "canonical-overlap",
    "drift-density",
    "multilingual-coverage",
    "export-stability",
    "production-activation-state",
]

OBSERVABILITY_KINDS = [
    "unresolved-conflicts",
    "blocking-drift",
    "unstable-exports",
    "refresh-propagation-chain",
    "reviewer-workload",
    "unresolved-approvals",
    "orphan-evidence",
    "incomplete-procedures",
    "missing-warnings",
]

# ---------------------------------------------------------------------------
# Rule tables
# ---------------------------------------------------------------------------
RULE_TABLES = {
    "reviewer-playbook-rules.json": {
        "schema": SCHEMA,
        "rule_family": "reviewer-playbook",
        "rules": [
            {"id": "RP-1", "rule": "playbook_id required and unique"},
            {"id": "RP-2", "rule": "playbook_kind enum required"},
            {"id": "RP-3", "rule": "steps MUST be a non-empty ordered list of {step_id, action, expected_outcome}"},
            {"id": "RP-4", "rule": "playbooks are pointer-only references to existing dispatches; no autonomous execution embedded"},
            {"id": "RP-5", "rule": "presentation keys forbidden recursively"},
            {"id": "RP-6", "rule": "playbook_sha256 deterministic over canonical JSON"},
            {"id": "RP-7", "rule": "reviewer attribution mandatory; append-only; supersession via prior_playbook_id pointer"},
        ],
    },
    "recovery-playbook-rules.json": {
        "schema": SCHEMA,
        "rule_family": "recovery-playbook",
        "rules": [
            {"id": "RC-1", "rule": "recovery_id required and unique"},
            {"id": "RC-2", "rule": "recovery_kind enum required"},
            {"id": "RC-3", "rule": "recovery_steps MUST enumerate ordered {step_id, action, expected_outcome, governing_dispatch} entries"},
            {"id": "RC-4", "rule": "every governing_dispatch MUST refer to an existing reviewer-authoritative dispatch (Phases 47–57)"},
            {"id": "RC-5", "rule": "rollback_target MUST point at a real prior artifact id (export, activation, canonical record, table, mapping)"},
            {"id": "RC-6", "rule": "NO autonomous repair; reviewer remains executor"},
            {"id": "RC-7", "rule": "append-only; reviewer attribution mandatory"},
        ],
    },
    "production-activation-rules.json": {
        "schema": SCHEMA,
        "rule_family": "production-activation",
        "rules": [
            {"id": "PA-1", "rule": "activation_id required and unique"},
            {"id": "PA-2", "rule": "package_id MUST resolve and MUST be in 'export-ready' lifecycle state"},
            {"id": "PA-3", "rule": "stabilization_id MUST resolve to an existing Phase 55 export stabilization"},
            {"id": "PA-4", "rule": "from_state and to_state MUST be in the activation states enum"},
            {"id": "PA-5", "rule": "(from_state -> to_state) MUST be in the explicit allowed transitions table"},
            {"id": "PA-6", "rule": "transition to 'production-approved' requires a passing readiness-audit reference (Phase 56)"},
            {"id": "PA-7", "rule": "transition to 'production-active' requires a passing deployment-verification reference (Phase 57)"},
            {"id": "PA-8", "rule": "transition to 'rollback-candidate' requires a recovery_playbook_id reference"},
            {"id": "PA-9", "rule": "activation is APPEND-ONLY: each transition is a new lifecycle record; prior state never mutated; no overwrite semantics"},
            {"id": "PA-10", "rule": "reviewer attribution mandatory"},
        ],
    },
    "deployment-verification-rules.json": {
        "schema": SCHEMA,
        "rule_family": "deployment-verification",
        "rules": [
            {"id": "DV-1", "rule": "verification_id required and unique"},
            {"id": "DV-2", "rule": "package_id MUST resolve"},
            {"id": "DV-3", "rule": "checks MUST cover all required verification checks: export-completeness, stable-export-hash, canonical-id-continuity, unresolved-drift, unresolved-conflicts, unresolved-visual-support, unresolved-multilingual-normalization, missing-lineage, orphan-semantic-entities"},
            {"id": "DV-4", "rule": "each check MUST record outcome ∈ {pass, fail} with deterministic evidence pointers"},
            {"id": "DV-5", "rule": "status enum: deployable | not-deployable"},
            {"id": "DV-6", "rule": "verification is informational; reviewer remains authoritative for activation transitions"},
            {"id": "DV-7", "rule": "verification_sha256 deterministic over canonical JSON"},
        ],
    },
    "portfolio-summary-rules.json": {
        "schema": SCHEMA,
        "rule_family": "portfolio-summary",
        "rules": [
            {"id": "PF-1", "rule": "portfolio_id required and unique"},
            {"id": "PF-2", "rule": "package_refs MUST be a non-empty list of existing package_ids"},
            {"id": "PF-3", "rule": "dimensions MUST cover the canonical portfolio dimensions"},
            {"id": "PF-4", "rule": "summary content is POINTER-only references to upstream records (no inline payload duplication)"},
            {"id": "PF-5", "rule": "presentation-neutral; no css / style / font / color / layout / dashboard keys"},
            {"id": "PF-6", "rule": "portfolio_sha256 deterministic over canonical JSON"},
            {"id": "PF-7", "rule": "operational confidence visibility — NOT analytics, NOT dashboards"},
        ],
    },
    "observability-summary-rules.json": {
        "schema": SCHEMA,
        "rule_family": "observability-summary",
        "rules": [
            {"id": "OB-1", "rule": "observability_id required and unique"},
            {"id": "OB-2", "rule": "observability_kind enum required"},
            {"id": "OB-3", "rule": "summary content is POINTER-only references"},
            {"id": "OB-4", "rule": "presentation-neutral; no telemetry keys, no streaming keys, no dashboard keys"},
            {"id": "OB-5", "rule": "summary_sha256 deterministic over canonical JSON"},
            {"id": "OB-6", "rule": "reviewer attribution mandatory"},
        ],
    },
    "deployment-package-rules.json": {
        "schema": SCHEMA,
        "rule_family": "deployment-package",
        "rules": [
            {"id": "DP-1", "rule": "deployment_package_id required and unique"},
            {"id": "DP-2", "rule": "package_id MUST resolve"},
            {"id": "DP-3", "rule": "stabilization_id MUST resolve to an existing Phase 55 export stabilization"},
            {"id": "DP-4", "rule": "stable_export_sha256 MUST exactly match the stabilization's stable_export_sha256"},
            {"id": "DP-5", "rule": "deployment_package_sha256 deterministic over canonical JSON of the manifest"},
            {"id": "DP-6", "rule": "package is POINTER-only; consumer payload bundles are produced separately"},
            {"id": "DP-7", "rule": "lineage_pointers MUST preserve canonical IDs and stable IDs"},
        ],
    },
    "dependency-manifest-rules.json": {
        "schema": SCHEMA,
        "rule_family": "dependency-manifest",
        "rules": [
            {"id": "DM-1", "rule": "dependency_manifest_id required and unique"},
            {"id": "DM-2", "rule": "deployment_package_id MUST resolve"},
            {"id": "DM-3", "rule": "dependencies MUST enumerate {kind, id, sha256_pointer} entries"},
            {"id": "DM-4", "rule": "every dependency MUST refer to an existing artifact (canonical entity, canonical procedure, stabilization, normalization table, etc.)"},
            {"id": "DM-5", "rule": "dependency_manifest_sha256 deterministic over canonical JSON"},
            {"id": "DM-6", "rule": "no cloud / package-registry / runtime-fetch dependencies — local artifact pointers only"},
        ],
    },
    "consumer-payload-bundle-rules.json": {
        "schema": SCHEMA,
        "rule_family": "consumer-payload-bundle",
        "rules": [
            {"id": "CB-1", "rule": "bundle_id required and unique"},
            {"id": "CB-2", "rule": "deployment_package_id MUST resolve"},
            {"id": "CB-3", "rule": "consumer_payload_sha256 MUST be derived deterministically from the bundled artifact pointers"},
            {"id": "CB-4", "rule": "bundle_state begins 'sealed'; supersession via new bundle_id with prior_bundle_id pointer"},
            {"id": "CB-5", "rule": "bundle is presentation-neutral pointer manifest; downstream consumers own all rendering"},
            {"id": "CB-6", "rule": "lineage_pointers preserve stabilization_id / canonical IDs / deployment_package_id"},
        ],
    },
}

NEW_EVENT_STORES = [
    "reviewer-playbook-events",
    "recovery-playbook-events",
    "production-activation-events",
    "deployment-verification-events",
    "portfolio-summary-events",
    "observability-summary-events",
    "deployment-package-events",
    "dependency-manifest-events",
    "consumer-payload-bundle-events",
]

JS_ASSETS = {
    "od-playbook-engine.js": "reviewer operational playbooks",
    "od-recovery-engine.js": "reviewer recovery / rollback playbooks",
    "od-activation-engine.js": "controlled production activation lifecycle",
    "od-verification-engine.js": "deployment integrity verification",
    "od-portfolio-engine.js": "corpus-scale portfolio confidence",
    "od-observability-engine.js": "operational observability summaries",
    "od-package-engine.js": "deployment package builder",
    "od-dependency-engine.js": "dependency manifest publisher",
    "od-bundle-engine.js": "consumer payload bundle publisher",
}

CONSOLES = [
    "reviewer-playbook-console",
    "recovery-playbook-console",
    "production-activation-console",
    "deployment-verification-console",
    "portfolio-summary-console",
    "deployment-package-console",
]

CSS_MARKER = "/* phase 57 — operational deployment readiness, reviewer enablement & controlled production activation additions */"
CSS_ADDENDUM = (
    CSS_MARKER + "\n"
    "/* Phase 57 intentionally introduces ZERO presentation rules. */\n"
    "/* Operational activation is reviewer-governed at the runtime layer; consumers own all presentation. */\n"
)

DOCTRINES = {
    "01-deployability-over-architectural-growth.md": (
        "# Deployability over architectural growth\n\n"
        "Phase 57 closes the operational activation gap WITHOUT adding semantic, convergence, "
        "extraction, publication, or replay families. The constitutional substrate is mature; "
        "remaining work is real-world deployability and reviewer operability."
    ),
    "02-reviewer-operability.md": (
        "# Reviewer operability\n\n"
        "Reviewers MUST be able to operate the system through deterministic playbooks. "
        "No autonomous workflow execution; playbooks are pointer-only step lists referencing "
        "existing reviewer-authoritative dispatches."
    ),
    "03-controlled-production-activation.md": (
        "# Controlled production activation\n\n"
        "Production activation is APPEND-ONLY across an explicit lifecycle:\n"
        "production-candidate → production-approved → production-active → superseded;\n"
        "rollback-candidate is observable from any pre-superseded state.\n"
        "No silent production replacement. No overwrite semantics."
    ),
    "04-deterministic-deployment-verification.md": (
        "# Deterministic deployment verification\n\n"
        "Deployability MUST be proven by deterministic checks: export completeness, stable "
        "export hashes, canonical ID continuity, unresolved drift / conflicts / visual support / "
        "multilingual normalization, missing lineage, orphan semantic entities. Verification is "
        "informational — reviewer remains authoritative."
    ),
    "05-corpus-scale-operational-confidence.md": (
        "# Corpus-scale operational confidence\n\n"
        "Portfolio summaries provide deterministic operational confidence visibility across many "
        "products. This is NOT analytics. This is NOT dashboards. Pointer-only aggregation only."
    ),
    "06-governed-rollback-and-recovery.md": (
        "# Governed rollback and recovery\n\n"
        "Rollback and recovery are reviewer-executed deterministic playbooks referencing existing "
        "Phase 47 transactional execution, Phase 56 readiness audit, and Phase 55 stabilization "
        "primitives. NO autonomous repair."
    ),
}

REPORTS = [
    ("01-reviewer-operational-playbook-runtime", "Reviewer operational playbook runtime"),
    ("02-controlled-production-activation-runtime", "Controlled production activation runtime"),
    ("03-deployment-integrity-verification", "Deployment integrity verification"),
    ("04-corpus-scale-runtime-confidence", "Corpus-scale runtime confidence"),
    ("05-reviewer-recovery-and-rollback-playbooks", "Reviewer recovery and rollback playbooks"),
    ("06-operational-observability-runtime", "Operational observability runtime"),
    ("07-production-export-packaging", "Production export packaging"),
    ("08-final-human-centered-operational-closure", "Final human-centered operational closure"),
    ("09-operational-activation-posture", "Operational activation posture"),
    ("10-phase57-platform-maturity-reassessment", "Phase 57 platform maturity reassessment"),
]

RUNTIME_README_MARKER = "## phase 57 — operational deployment readiness, reviewer enablement & controlled production activation"
RUNTIME_README_ADDENDUM = (
    RUNTIME_README_MARKER + "\n\n"
    f"- schema: `{SCHEMA}`\n"
    f"- constitutional layer: {LAYER}\n"
    "- storage tree: `operational-console/operational-deployment-runtime/`\n"
    "- 10 storage subdirs: reviewer-playbooks, recovery-playbooks, production-activations,\n"
    "  activation-lifecycle-records, deployment-verifications, portfolio-summaries,\n"
    "  observability-summaries, deployment-packages, dependency-manifests, consumer-payload-bundles.\n"
    "- 9 dispatch kinds: reviewer-playbook-publish, recovery-playbook-publish,\n"
    "  production-activation-transition, deployment-verification-run, portfolio-summary-publish,\n"
    "  observability-summary-publish, deployment-package-build, dependency-manifest-publish,\n"
    "  consumer-payload-bundle-publish.\n"
    "- activation lifecycle: production-candidate → production-approved → production-active → superseded;\n"
    "  rollback-candidate observable from any pre-superseded state. APPEND-ONLY; no overwrite semantics.\n"
    "- posture: deployability + reviewer operability over architectural growth; deterministic only;\n"
    "  NO embeddings; NO vector DBs; NO probabilistic inference; NO ML / LLMs / MT;\n"
    "  NO autonomous activation / publication / repair; NO silent production replacement;\n"
    "  NO dashboards / telemetry / deployment automation daemons; reviewer-authoritative;\n"
    "  lineage-preserving; transaction-safe activation; rollback-governed; presentation-neutral;\n"
    "  writes ONLY into the layer's own runtime tree.\n"
    "- this is the operational activation layer that transforms the Phase 47–56 substrate\n"
    "  into a deployable reviewer-operated production system.\n"
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
    if write_if_missing(OD_ROOT / "README.md",
        f"# operational-deployment-runtime\n\nPhase 57 / layer {LAYER}. Schema `{SCHEMA}`.\n"):
        storage_roots_created += 1
    for sub in OD_SUBDIRS:
        d = OD_ROOT / sub
        if write_if_missing(d / ".gitkeep", ""):
            storage_roots_created += 1
        write_if_missing(d / "README.md", f"# {sub}\n\nPhase 57 / layer {LAYER}.\n")

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
            f"// {fn} — Phase 57 ({summary})\n"
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
            f"<!-- presentation-neutral phase 57 console — schema {SCHEMA} -->\n"
            f"<main data-phase=\"{LAYER}\" data-console=\"{c}\"></main>\n"
        )

    doctrine_root = KB_ROOT / "GOVERNED_OPERATIONAL_DEPLOYMENT_READINESS_CONTROLLED_PRODUCTION_ACTIVATION_GOVERNANCE"
    write_if_missing(doctrine_root / "00-INDEX.md",
        f"# GOVERNED OPERATIONAL DEPLOYMENT READINESS & CONTROLLED PRODUCTION ACTIVATION (layer {LAYER})\n\n"
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
        "activation_states": ACTIVATION_STATES,
        "activation_transitions": ACTIVATION_TRANSITIONS,
    })

    reports_dir = REPORTS_ROOT / "operational-deployment-readiness-controlled-production-activation"
    write_if_missing(reports_dir / "README.md",
        f"# operational-deployment-readiness-controlled-production-activation reports\n\nPhase 57 / layer {LAYER}.\n"
    )
    for slug, title in REPORTS:
        write_json_if_missing(reports_dir / f"{slug}.json", {
            "schema": SCHEMA,
            "report": slug,
            "title": title,
            "constitutional_layer_index": LAYER,
        })
        write_if_missing(reports_dir / f"{slug}.md",
            f"# {title}\n\nPhase 57 / layer {LAYER}. Schema `{SCHEMA}`.\n"
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
        "Phase 57 — operational deployment readiness, reviewer enablement & controlled production activation written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {storage_roots_created} | New event stores: {new_event_stores_created} | "
        f"Rule tables: {len(RULE_TABLES)} | JS assets: {len(JS_ASSETS)} | Exec consoles: {len(CONSOLES)} | "
        f"Doctrines: {len(DOCTRINES)} | Reports: {len(REPORTS)} | RUNTIME_README addendum: {rr_addendum_added}"
    )


if __name__ == "__main__":
    main()
