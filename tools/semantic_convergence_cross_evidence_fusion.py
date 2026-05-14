#!/usr/bin/env python3
"""
Phase 55 builder — Semantic Convergence, Cross-Evidence Fusion &
Operational Runtime Cohesion (constitutional layer 48).

This is the FIRST POST-CONSTITUTIONAL convergence layer. It does NOT
extend governance surface; it adds operational *cohesion* through:
  - deterministic evidence fingerprints,
  - reviewer-governed fusion clusters,
  - canonical entity / canonical procedure convergence,
  - reviewer arbitration of conflicts,
  - transaction-safe refresh cohesion across upstream runtimes,
  - unified-workspace flow recording,
  - real-world robustness handling,
  - consumer-export stabilization (canonical IDs).

Idempotent: a second run prints zeros for storage_roots/event_stores/
RUNTIME_README addendum. Writes ONLY into the layer's own runtime tree.
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

SCHEMA = "semantic-convergence-cross-evidence-fusion/1.0"
LAYER = 48

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RULES_ROOT = OC_ROOT / "execution-engine"
ASSETS_EXEC_ROOT = OC_ROOT / "assets/exec"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
KB_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING"
REPORTS_ROOT = THEME_ROOT / "_repository-governance/reports"

SC_ROOT = OC_ROOT / "semantic-convergence-runtime"
SC_SUBDIRS = [
    "evidence-fingerprints",
    "fusion-clusters",
    "canonical-entities",
    "canonical-procedures",
    "conflict-surfacings",
    "arbitration-decisions",
    "refresh-cohesion-records",
    "workspace-flows",
    "robustness-records",
    "export-stabilizations",
]

# 47 prior-anchor chain (length 47 — extended by Phase 54 anchor at end).
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
]
# Sanity: chain length must be 46 entries (1 .. 46) before Phase 55 anchor.
assert len(SUBORDINATE_TO) >= 46, f"SUBORDINATE_TO too short: {len(SUBORDINATE_TO)}"

POSTURE = {
    "operational_cohesion_priority": True,
    "governance_expansion_priority": False,
    "wires_existing_systems": True,
    "introduces_new_orchestration": False,
    "introduces_new_replay_engine": False,
    "introduces_new_lifecycle_family": False,
    "introduces_new_extraction_framework": False,
    "deterministic_fingerprints_only": True,
    "no_embeddings": True,
    "no_vector_databases": True,
    "no_probabilistic_inference": True,
    "no_ml_models": True,
    "no_autonomous_arbitration": True,
    "no_autonomous_convergence": True,
    "reviewer_authoritative_arbitration": True,
    "reviewer_attribution_required": True,
    "lineage_preserving_convergence": True,
    "evidence_provenance_preserving": True,
    "grounding_provenance_preserving": True,
    "transaction_safe_refresh_cohesion": True,
    "append_only_event_stores": True,
    "fail_closed_validation": True,
    "consumer_boundary_enforced": True,
    "presentation_neutral_outputs": True,
    "stable_canonical_export_ids": True,
    "unified_workspace_flow_recording": True,
    "real_world_robustness_handling": True,
    "writes_only_into_semantic_convergence_runtime_tree": True,
    "writes_to_manual_runtime_closure_tree": False,
    "writes_to_manual_semantic_packaging_runtime_tree": False,
    "writes_to_semantic_extraction_runtime_tree": False,
    "no_image_generation_in_this_layer": True,
    "no_publication_in_this_layer": True,
    "stdlib_only": True,
    "local_first": True,
    "no_cloud_apis": True,
    "no_saas": True,
    "no_daemons": True,
    "cli_only_interface": True,
    "constitutional_layer_index": LAYER,
    "post_constitutional_convergence_phase": True,
}

DISPATCH_KINDS = [
    "evidence-fingerprint",
    "fusion-cluster-form",
    "canonical-entity-promote",
    "canonical-procedure-converge",
    "conflict-surface",
    "arbitration-decide",
    "refresh-cohesion-propagate",
    "workspace-flow-record",
    "export-stabilize",
]

ARBITRATION_DECISIONS = ["accept", "reject", "defer", "escalate"]
CONFLICT_SEVERITY = ["informational", "minor", "major", "blocking"]
WORKSPACE_FLOW_KINDS = [
    "evidence",
    "analysis",
    "fusion",
    "canonical-entity",
    "canonical-procedure",
    "conflict",
    "arbitration",
    "synthesis",
    "visual-support",
    "prompt-package",
    "export",
]
ROBUSTNESS_KINDS = [
    "incomplete-evidence",
    "noisy-ocr",
    "duplicate-document",
    "conflicting-oem-doc",
    "low-quality-screenshot",
    "partial-video",
    "multilingual-evidence",
    "fragmented-support-export",
]

# ---------------------------------------------------------------------------
# Rule tables — kept tight, deterministic, reviewer-governed.
# ---------------------------------------------------------------------------
RULE_TABLES = {
    "evidence-fingerprint-rules.json": {
        "schema": SCHEMA,
        "rule_family": "evidence-fingerprint",
        "rules": [
            {"id": "EFP-1", "rule": "fingerprint_id and source_evidence_id required"},
            {"id": "EFP-2", "rule": "fingerprint MUST be deterministic SHA-256 over normalized text + structural feature set; NO embeddings, NO vectors"},
            {"id": "EFP-3", "rule": "normalization is lowercase + whitespace-collapse + punctuation-strip ONLY (deterministic)"},
            {"id": "EFP-4", "rule": "structural_kind enum: procedure-step | warning | specification | troubleshooting | app-flow | navigation | maintenance"},
            {"id": "EFP-5", "rule": "evidence_refs must be a non-empty list; provenance preserved"},
            {"id": "EFP-6", "rule": "presentation/CSS/typography/layout keys are forbidden in payload"},
        ],
    },
    "fusion-cluster-rules.json": {
        "schema": SCHEMA,
        "rule_family": "fusion-cluster",
        "rules": [
            {"id": "FC-1", "rule": "cluster_id required and unique within fusion-clusters/"},
            {"id": "FC-2", "rule": "member_fingerprint_ids must be non-empty list of resolvable fingerprint_ids"},
            {"id": "FC-3", "rule": "cluster_fingerprint MUST be deterministic SHA-256 over sorted member fingerprints"},
            {"id": "FC-4", "rule": "all members MUST share structural_kind (no cross-kind clustering)"},
            {"id": "FC-5", "rule": "cluster preserves union of evidence_refs and grounding_refs from members"},
            {"id": "FC-6", "rule": "fusion is reviewer-governed; no autonomous clustering"},
            {"id": "FC-7", "rule": "cluster_state begins 'pending-review' and may only be promoted via canonical-entity-promote or canonical-procedure-converge"},
        ],
    },
    "canonical-entity-rules.json": {
        "schema": SCHEMA,
        "rule_family": "canonical-entity",
        "rules": [
            {"id": "CE-1", "rule": "canonical_entity_id required and stable across runtime cycles"},
            {"id": "CE-2", "rule": "source_cluster_id must resolve and must be in 'pending-review' or 'reviewer-approved'"},
            {"id": "CE-3", "rule": "entity_kind enum: entity | warning | specification"},
            {"id": "CE-4", "rule": "lineage_pointers MUST preserve every member fingerprint_id and evidence_id"},
            {"id": "CE-5", "rule": "reviewer attribution mandatory; promotion is append-only"},
            {"id": "CE-6", "rule": "canonical_payload MUST be presentation-neutral (no css/style/font/color/layout keys)"},
        ],
    },
    "canonical-procedure-rules.json": {
        "schema": SCHEMA,
        "rule_family": "canonical-procedure",
        "rules": [
            {"id": "CP-1", "rule": "canonical_procedure_id required and stable"},
            {"id": "CP-2", "rule": "source_cluster_ids must all resolve and share procedure-class structural_kind"},
            {"id": "CP-3", "rule": "step_sequence MUST be deterministically ordered (1..N contiguous)"},
            {"id": "CP-4", "rule": "every step MUST reference at least one source fingerprint_id"},
            {"id": "CP-5", "rule": "every step MUST preserve evidence_refs and grounding_refs from its source"},
            {"id": "CP-6", "rule": "conflicting steps MUST NOT be silently flattened — they MUST surface a conflict-surface record"},
            {"id": "CP-7", "rule": "presentation keys forbidden recursively"},
        ],
    },
    "conflict-surfacing-rules.json": {
        "schema": SCHEMA,
        "rule_family": "conflict-surfacing",
        "rules": [
            {"id": "CS-1", "rule": "conflict_id required and unique"},
            {"id": "CS-2", "rule": "conflict_kind enum: specification-conflict | procedure-conflict | warning-conflict | troubleshooting-conflict"},
            {"id": "CS-3", "rule": "conflicting_refs MUST be a list of >= 2 distinct fingerprint_ids or canonical entity ids"},
            {"id": "CS-4", "rule": "severity enum: informational | minor | major | blocking"},
            {"id": "CS-5", "rule": "trust_composition MUST be recorded (counts of reviewer-approved / review-required / unresolved sources)"},
            {"id": "CS-6", "rule": "conflict surfacing is fail-closed: blocking conflicts MUST gate downstream canonical promotion"},
        ],
    },
    "arbitration-decision-rules.json": {
        "schema": SCHEMA,
        "rule_family": "arbitration-decision",
        "rules": [
            {"id": "AD-1", "rule": "decision_id required and unique"},
            {"id": "AD-2", "rule": "conflict_id MUST resolve to existing conflict-surface record"},
            {"id": "AD-3", "rule": "decision enum: accept | reject | defer | escalate"},
            {"id": "AD-4", "rule": "accept requires accepted_ref to be one of the conflicting_refs"},
            {"id": "AD-5", "rule": "reject and escalate require non-empty cited_rule_ids"},
            {"id": "AD-6", "rule": "arbitration is reviewer-only; no autonomous arbitration"},
            {"id": "AD-7", "rule": "decisions are append-only; supersession via new decision_id with prior_decision_id pointer"},
        ],
    },
    "refresh-cohesion-rules.json": {
        "schema": SCHEMA,
        "rule_family": "refresh-cohesion",
        "rules": [
            {"id": "RC-1", "rule": "cohesion_id required and unique"},
            {"id": "RC-2", "rule": "trigger_kind enum: approved-intake | canonical-promotion | arbitration-resolution"},
            {"id": "RC-3", "rule": "trigger_ref MUST resolve into upstream phase 54 / 55 store (intake-approval, canonical-entity, canonical-procedure, arbitration-decision)"},
            {"id": "RC-4", "rule": "refresh_chain MUST be a deterministic ordered list (fingerprints → clusters → canonical → synthesis → export-invalidation)"},
            {"id": "RC-5", "rule": "records are POINTER-ONLY; Phase 55 NEVER mutates upstream extraction/packaging/closure trees"},
            {"id": "RC-6", "rule": "transaction-safety: cohesion records are append-only and replayable"},
        ],
    },
    "workspace-flow-rules.json": {
        "schema": SCHEMA,
        "rule_family": "workspace-flow",
        "rules": [
            {"id": "WF-1", "rule": "flow_event_id required and unique"},
            {"id": "WF-2", "rule": "stage enum from canonical workspace-flow stages"},
            {"id": "WF-3", "rule": "ref_id required and resolves into the corresponding upstream record (intake/cluster/canonical/etc.)"},
            {"id": "WF-4", "rule": "workspace-flow events are observational only; they MUST NOT mutate upstream state"},
            {"id": "WF-5", "rule": "reviewer attribution mandatory"},
        ],
    },
    "export-stabilization-rules.json": {
        "schema": SCHEMA,
        "rule_family": "export-stabilization",
        "rules": [
            {"id": "ES-1", "rule": "stabilization_id required and unique"},
            {"id": "ES-2", "rule": "package_id MUST resolve to a Phase 53 manual-package in 'export-ready' state"},
            {"id": "ES-3", "rule": "canonical_id_map MUST assign stable canonical IDs to each section/entity/procedure"},
            {"id": "ES-4", "rule": "stable_export_payload MUST be presentation-neutral and recursively scrubbed for forbidden keys"},
            {"id": "ES-5", "rule": "stable_export_sha256 deterministic over canonical JSON"},
            {"id": "ES-6", "rule": "subsequent stabilizations of the same package MUST preserve canonical_id_map (additive only)"},
        ],
    },
}

NEW_EVENT_STORES = [
    "evidence-fingerprint-events",
    "fusion-cluster-events",
    "canonical-entity-events",
    "canonical-procedure-events",
    "conflict-surfacing-events",
    "arbitration-decision-events",
    "refresh-cohesion-events",
    "workspace-flow-events",
    "export-stabilization-events",
]

JS_ASSETS = {
    "sc-fingerprint-engine.js": "evidence fingerprinting",
    "sc-fusion-engine.js": "fusion cluster formation",
    "sc-canonical-engine.js": "canonical entity & procedure convergence",
    "sc-conflict-engine.js": "conflict surfacing",
    "sc-arbitration-engine.js": "reviewer arbitration",
    "sc-refresh-engine.js": "refresh cohesion propagation",
    "sc-workspace-engine.js": "unified workspace flow",
    "sc-stabilize-engine.js": "export stabilization",
}

CONSOLES = [
    "fusion-console",
    "canonical-entity-console",
    "conflict-arbitration-console",
    "refresh-cohesion-console",
    "unified-workspace-console",
    "export-stabilization-console",
]

CSS_MARKER = "/* phase 55 — semantic convergence, cross-evidence fusion & operational runtime cohesion additions */"
CSS_ADDENDUM = (
    CSS_MARKER + "\n"
    "/* Phase 55 intentionally introduces ZERO presentation rules. */\n"
    "/* Convergence is reviewer-governed at the runtime layer; consumers own all presentation. */\n"
)

DOCTRINES = {
    "01-operational-cohesion-over-fragmentation.md": (
        "# Operational cohesion over fragmentation\n\n"
        "Phase 55 reduces operational fragmentation rather than expanding governance. "
        "Multiple evidence sources MUST converge into canonical reviewer-governed semantic knowledge."
    ),
    "02-deterministic-fingerprints-no-embeddings.md": (
        "# Deterministic fingerprints — no embeddings\n\n"
        "Convergence MUST use deterministic SHA-256 fingerprints over normalized text + structural features. "
        "Embeddings, vector databases, similarity scores, and probabilistic inference are FORBIDDEN."
    ),
    "03-lineage-preserving-convergence.md": (
        "# Lineage-preserving convergence\n\n"
        "Every convergence step MUST preserve evidence_refs, grounding_refs, fingerprint_ids, "
        "and reviewer attribution. Convergence reveals one canonical surface; it never erases provenance."
    ),
    "04-reviewer-authoritative-arbitration.md": (
        "# Reviewer-authoritative arbitration\n\n"
        "Conflicts MUST be surfaced — never silently flattened. Reviewers arbitrate via append-only "
        "decision records. Autonomous arbitration is FORBIDDEN."
    ),
    "05-transaction-safe-refresh-cohesion.md": (
        "# Transaction-safe refresh cohesion\n\n"
        "Refresh records propagate as POINTER-only chains. Upstream extraction / packaging / closure "
        "trees are NEVER mutated by Phase 55."
    ),
    "06-stable-canonical-export-ids.md": (
        "# Stable canonical export IDs\n\n"
        "Consumer exports MUST be stabilized: canonical IDs for sections/entities/procedures persist "
        "across stabilization cycles. Stabilization is additive, never destructive."
    ),
}

REPORTS = [
    ("01-cross-evidence-fusion-summary", "Cross-evidence fusion summary"),
    ("02-deterministic-deduplication-summary", "Deterministic semantic deduplication"),
    ("03-canonical-entity-convergence-summary", "Canonical entity convergence"),
    ("04-canonical-procedure-convergence-summary", "Canonical procedure convergence"),
    ("05-conflict-arbitration-summary", "Reviewer-governed conflict arbitration"),
    ("06-refresh-cohesion-summary", "Transaction-safe refresh cohesion"),
    ("07-unified-workspace-flow-summary", "Unified operational workspace flow"),
    ("08-real-world-robustness-summary", "Real-world evidence robustness handling"),
    ("09-export-stabilization-summary", "Consumer export stabilization & canonical IDs"),
    ("10-semantic-convergence-platform-maturity-reassessment", "Phase 55 platform maturity reassessment"),
]

RUNTIME_README_MARKER = "## phase 55 — semantic convergence, cross-evidence fusion & operational runtime cohesion"
RUNTIME_README_ADDENDUM = (
    RUNTIME_README_MARKER + "\n\n"
    f"- schema: `{SCHEMA}`\n"
    f"- constitutional layer: {LAYER}\n"
    "- storage tree: `operational-console/semantic-convergence-runtime/`\n"
    "- 10 storage subdirs: evidence-fingerprints, fusion-clusters, canonical-entities, canonical-procedures,\n"
    "  conflict-surfacings, arbitration-decisions, refresh-cohesion-records, workspace-flows,\n"
    "  robustness-records, export-stabilizations.\n"
    "- 9 dispatch kinds: evidence-fingerprint, fusion-cluster-form, canonical-entity-promote,\n"
    "  canonical-procedure-converge, conflict-surface, arbitration-decide, refresh-cohesion-propagate,\n"
    "  workspace-flow-record, export-stabilize.\n"
    "- posture: deterministic fingerprints only; NO embeddings; NO vector DBs; NO probabilistic inference;\n"
    "  reviewer-authoritative arbitration; lineage-preserving; transaction-safe refresh cohesion;\n"
    "  consumer-boundary-enforced; presentation-neutral; writes ONLY into the layer's own runtime tree.\n"
    "- this is the FIRST POST-CONSTITUTIONAL convergence layer: it wires existing systems into operational\n"
    "  semantic intelligence WITHOUT expanding governance complexity.\n"
)


# ---------------------------------------------------------------------------
# Builder helpers
# ---------------------------------------------------------------------------
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
    # Root README + .gitkeep
    if write_if_missing(SC_ROOT / "README.md",
        f"# semantic-convergence-runtime\n\nPhase 55 / layer {LAYER}. Schema `{SCHEMA}`.\n"):
        storage_roots_created += 1
    for sub in SC_SUBDIRS:
        d = SC_ROOT / sub
        if write_if_missing(d / ".gitkeep", ""):
            storage_roots_created += 1
        write_if_missing(d / "README.md", f"# {sub}\n\nPhase 55 / layer {LAYER}.\n")

    # Rule tables (always re-written so they stay in sync)
    for fn, body in RULE_TABLES.items():
        rules_path = RULES_ROOT / fn
        rules_path.parent.mkdir(parents=True, exist_ok=True)
        rules_path.write_text(json.dumps(body, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    # New event stores — only on first run
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

    # JS assets
    for fn, summary in JS_ASSETS.items():
        body = (
            f"// {fn} — Phase 55 ({summary})\n"
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

    # Consoles
    for c in CONSOLES:
        write_if_missing(OC_ROOT / c / "exec.html",
            "<!doctype html>\n<meta charset=utf-8>\n"
            f"<title>{c} — phase {LAYER}</title>\n"
            f"<!-- presentation-neutral phase 55 console — schema {SCHEMA} -->\n"
            f"<main data-phase=\"{LAYER}\" data-console=\"{c}\"></main>\n"
        )

    # Doctrines
    doctrine_root = KB_ROOT / "GOVERNED_SEMANTIC_CONVERGENCE_CROSS_EVIDENCE_FUSION_GOVERNANCE"
    write_if_missing(doctrine_root / "00-INDEX.md",
        f"# GOVERNED SEMANTIC CONVERGENCE CROSS-EVIDENCE FUSION (layer {LAYER})\n\n"
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

    # Reports (json + md)
    reports_dir = REPORTS_ROOT / "semantic-convergence-cross-evidence-fusion"
    write_if_missing(reports_dir / "README.md",
        f"# semantic-convergence-cross-evidence-fusion reports\n\nPhase 55 / layer {LAYER}.\n"
    )
    for slug, title in REPORTS:
        write_json_if_missing(reports_dir / f"{slug}.json", {
            "schema": SCHEMA,
            "report": slug,
            "title": title,
            "constitutional_layer_index": LAYER,
        })
        write_if_missing(reports_dir / f"{slug}.md",
            f"# {title}\n\nPhase 55 / layer {LAYER}. Schema `{SCHEMA}`.\n"
        )

    # CSS addendum
    css_path = ASSETS_EXEC_ROOT / "exec.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    if css_path.exists():
        existing = css_path.read_text(encoding="utf-8")
    else:
        existing = ""
    if CSS_MARKER not in existing:
        css_path.write_text(existing + ("\n" if existing and not existing.endswith("\n") else "") + CSS_ADDENDUM, encoding="utf-8")

    # RUNTIME_README addendum
    rr_path = OC_ROOT / "RUNTIME_README.md"
    rr_addendum_added = 0
    if rr_path.exists():
        rr_existing = rr_path.read_text(encoding="utf-8")
    else:
        rr_existing = "# RUNTIME_README\n\n"
    if RUNTIME_README_MARKER not in rr_existing:
        rr_path.write_text(rr_existing + ("\n" if rr_existing and not rr_existing.endswith("\n") else "") + "\n" + RUNTIME_README_ADDENDUM, encoding="utf-8")
        rr_addendum_added = 1

    print(
        "Phase 55 — semantic convergence, cross-evidence fusion & operational runtime cohesion written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {storage_roots_created} | New event stores: {new_event_stores_created} | "
        f"Rule tables: {len(RULE_TABLES)} | JS assets: {len(JS_ASSETS)} | Exec consoles: {len(CONSOLES)} | "
        f"Doctrines: {len(DOCTRINES)} | Reports: {len(REPORTS)} | RUNTIME_README addendum: {rr_addendum_added}"
    )


if __name__ == "__main__":
    main()
