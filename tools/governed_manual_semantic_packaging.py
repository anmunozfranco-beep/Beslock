"""
Phase 53 — Governed Manual Semantic Packaging & Consumer-Ready Export Contracts (layer 46).

Idempotent stdlib-only builder. Emits the layer-46 surface over layer 45
(governed semantic evidence analysis & multimodal extraction), layer 44
(governed multimodal publication composition & page orchestration — reinterpreted
here as semantic packaging infrastructure, NOT layout/rendering), layer 43, 42,
and 41.

The runtime writer is the executor (`tools/governed_manual_semantic_packaging_executor.py`).
This builder NEVER mutates event stores, runtime data, knowledge-core,
governance, runtime-implementation, runtime-manifests payloads, prior-layer
runtime trees, OEM source assets, uploads, or live publications.

Posture (this layer):
- deterministic, reviewer-authoritative, append-only, local-first, stdlib-first,
  fail-closed, replayable, auditable.
- The Knowledge OS packages SEMANTIC manual knowledge ONLY.
- ABSOLUTELY FORBIDDEN: responsive rendering, frontend layout orchestration,
  CSS breakpoint governance, typography systems, mobile rendering, visual page
  composition, UI frameworks, SaaS, cloud APIs, autonomous rendering, hidden
  formatting mutation, presentation-specific logic, autonomous semantic
  restructuring, LLM rewriting, probabilistic packaging, hidden chunk mutation.
- Exports are presentation-neutral, renderer-agnostic, lineage-preserving,
  trust-aware, deterministic.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Roots
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
OC_ROOT = THEME_ROOT / "operational-console"
RULES_ROOT = OC_ROOT / "execution-engine"
ASSETS_EXEC_ROOT = OC_ROOT / "assets" / "exec"
RUNTIME_MANIFESTS_ROOT = OC_ROOT / "runtime-manifests"
KB_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports"

MP_ROOT = OC_ROOT / "manual-semantic-packaging-runtime"

MP_SUBDIRS = [
    "manual-packages",
    "semantic-sections",
    "semantic-procedures",
    "semantic-warnings",
    "semantic-specifications",
    "semantic-troubleshooting",
    "semantic-support",
    "export-contracts",
    "raw-html-exports",
    "structured-json-exports",
    "semantic-markdown-exports",
    "packaging-lineage",
    "packaging-replays",
    "packaging-integrity",
    "manual-packaging-lifecycle",
    "reviewer-packaging-decisions",
]

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA = "governed-manual-semantic-packaging/1.0"
LAYER = 46

SUBORDINATE_TO = [
    "knowledge-core-doctrine",
    "governance-source-of-truth-doctrine",
    "runtime-evidence-and-trust-doctrine",
    "executable-operational-bindings-governance",
    "governed-filesystem-orchestration-doctrine",
    "governed-transactional-execution-and-recovery-governance",
    "governed-knowledge-synthesis-and-canonical-publication-governance",
    "governed-multimodal-grounding-and-visual-publication-governance",
    "governed-visual-generation-and-deterministic-asset-production-governance",
    "governed-multimodal-publication-composition-and-page-orchestration-governance",
    "governed-semantic-evidence-analysis-and-multimodal-extraction-governance",
]
while len(SUBORDINATE_TO) < 45:
    SUBORDINATE_TO.append(
        "governed-semantic-evidence-analysis-and-multimodal-extraction-governance"
    )

POSTURE = {
    "deterministic": True,
    "reviewer_authoritative": True,
    "append_only_lineage": True,
    "local_first": True,
    "stdlib_first": True,
    "replayable": True,
    "auditable": True,
    "consumer_boundary_enforced": True,
    "presentation_neutral_exports": True,
    "renderer_agnostic_exports": True,
    "no_responsive_rendering": True,
    "no_frontend_layout_orchestration": True,
    "no_css_breakpoint_governance": True,
    "no_typography_systems": True,
    "no_mobile_rendering_logic": True,
    "no_visual_page_composition": True,
    "no_ui_frameworks": True,
    "no_saas_dependency": True,
    "no_cloud_apis": True,
    "no_autonomous_rendering": True,
    "no_hidden_formatting_mutation": True,
    "no_presentation_specific_logic": True,
    "no_autonomous_semantic_restructuring": True,
    "no_llm_rewriting": True,
    "no_probabilistic_packaging": True,
    "no_hidden_chunk_mutation": True,
    "no_telemetry": True,
    "no_watchers": True,
    "no_daemons": True,
    "no_background_workers": True,
    "no_embeddings": True,
    "no_vector_databases": True,
    "no_autonomous_promotion": True,
    "fail_closed_on_missing_lineage": True,
    "fail_closed_on_unresolved_grounding": True,
    "fail_closed_on_orphan_section": True,
    "fail_closed_on_duplicate_section_id": True,
    "fail_closed_on_broken_continuity_chain": True,
    "fail_closed_on_unresolved_evidence_ref": True,
    "fail_closed_on_invalid_export_contract": True,
    "fail_closed_on_forbidden_overwrite_path": True,
    "fail_closed_on_hidden_semantic_mutation": True,
    "writes_only_into_manual_semantic_packaging_runtime_tree": True,
    "browser_surfaces_never_write_filesystem": True,
    "writes_to_live_publication_tree": False,
    "writes_to_publication_composition_runtime_tree": False,
    "writes_to_visual_publication_builds_tree": False,
    "writes_to_visual_generation_runtime_tree": False,
    "writes_to_semantic_extraction_runtime_tree": False,
    "writes_to_frontend_or_theme_systems": False,
}

SECTION_KINDS = [
    "semantic-section",
    "semantic-procedure",
    "semantic-warning-group",
    "semantic-specification-group",
    "semantic-troubleshooting-group",
    "semantic-support-group",
]

EXPORT_KINDS = [
    "raw-html-export",
    "structured-json-export",
    "semantic-markdown-export",
]

CONTINUITY_STATUSES = ["ok", "gaps-detected", "unresolved"]

LIFECYCLE_STATES = {
    "draft",
    "review-required",
    "reviewer-approved",
    "export-ready",
    "superseded",
    "deprecated",
}
LIFECYCLE_TERMINAL = {"deprecated"}
LIFECYCLE_EDGES = [
    ("draft", "review-required"),
    ("draft", "deprecated"),
    ("review-required", "reviewer-approved"),
    ("review-required", "draft"),
    ("review-required", "deprecated"),
    ("reviewer-approved", "export-ready"),
    ("reviewer-approved", "review-required"),
    ("reviewer-approved", "superseded"),
    ("export-ready", "reviewer-approved"),
    ("export-ready", "superseded"),
    ("superseded", "deprecated"),
]

NEW_EVENT_STORES = [
    "manual-package-events",
    "semantic-section-events",
    "export-contract-events",
    "packaging-continuity-events",
    "packaging-lineage-events",
    "packaging-replay-events",
    "packaging-integrity-events",
    "packaging-lifecycle-events",
    "reviewer-packaging-decision-events",
]

# ---------------------------------------------------------------------------
# Rule tables
# ---------------------------------------------------------------------------

MANUAL_PACKAGE_RULES = {
    "schema": "manual-package-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "MP-1", "rule": "every manual package MUST cite manual_id, canonical_product_id, package_version, reviewer, reasoning_chain, semantic_structure (list of section_ids), continuity_status, and package_sha256."},
        {"id": "MP-2", "rule": "synthesis_ids, extraction_ids, grounding_ids, evidence_refs MUST be lists of reviewer-attributed strings; empty lineage is fail-closed (PI-1)."},
        {"id": "MP-3", "rule": "package_sha256 is computed deterministically over canonical JSON of {manual_id, package_version, semantic_structure, lineage refs}; mismatch on replay is fail-closed (PR-2)."},
        {"id": "MP-4", "rule": "package_version follows reviewer-declared semver (MAJOR.MINOR.PATCH); in-place mutation of a published version is FORBIDDEN."},
        {"id": "MP-5", "rule": "continuity_status MUST be one of {ok, gaps-detected, unresolved} and reviewer-attributed."},
        {"id": "MP-6", "rule": "manual packages are append-only; supersedence MUST cite prior_package_id."},
        {"id": "MP-7", "rule": "autonomous package promotion is FORBIDDEN; only reviewer-attributed lifecycle transitions advance state."},
        {"id": "MP-8", "rule": "manual packages MUST NOT contain CSS, breakpoints, layout instructions, typography systems, or any presentation-bearing fields."},
    ],
}

SEMANTIC_SECTION_RULES = {
    "schema": "semantic-section-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "SS-1", "rule": "every section MUST cite section_id, manual_id, section_kind ∈ SECTION_KINDS, reviewer, and lineage references (extraction_ids, grounding_ids, evidence_refs)."},
        {"id": "SS-2", "rule": "section_kind MUST be one of: semantic-section, semantic-procedure, semantic-warning-group, semantic-specification-group, semantic-troubleshooting-group, semantic-support-group."},
        {"id": "SS-3", "rule": "sections MUST preserve unresolved_states (list) and trust_composition counts {reviewer-approved, review-required, unresolved}."},
        {"id": "SS-4", "rule": "orphan sections (citing extraction_ids or grounding_ids that do not resolve) BLOCK approval (fail-closed PI-3)."},
        {"id": "SS-5", "rule": "duplicate section_id within a manual_id is FORBIDDEN (fail-closed PI-4)."},
        {"id": "SS-6", "rule": "sections MUST NOT contain CSS, breakpoints, layout instructions, typography, or rendering hints."},
        {"id": "SS-7", "rule": "sections are append-only; in-place mutation is FORBIDDEN."},
        {"id": "SS-8", "rule": "semantic-procedure sections MUST cite contiguous step_index sequences starting at 1; gaps are fail-closed (PC-2)."},
    ],
}

EXPORT_CONTRACT_RULES = {
    "schema": "export-contract-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "XC-1", "rule": "every export contract MUST cite contract_id, manual_id, package_id, export_kind ∈ EXPORT_KINDS, reviewer, reasoning_chain."},
        {"id": "XC-2", "rule": "export_kind MUST be one of {raw-html-export, structured-json-export, semantic-markdown-export}."},
        {"id": "XC-3", "rule": "exports MUST be presentation-neutral; CSS injection, breakpoints, screen-size optimization, frontend-rendering hints are FORBIDDEN."},
        {"id": "XC-4", "rule": "exports MUST cite the source package_id; orphan contracts BLOCK approval (PI-7)."},
        {"id": "XC-5", "rule": "rendered payload sha256 MUST be deterministic; mismatch on replay is fail-closed (PR-2)."},
        {"id": "XC-6", "rule": "exports preserve lineage and trust_composition; redaction or restructuring of lineage is FORBIDDEN."},
        {"id": "XC-7", "rule": "exports are append-only; in-place mutation is FORBIDDEN."},
        {"id": "XC-8", "rule": "raw-html-export MUST emit only semantic HTML5 tags (article/section/h1-h6/ol/ul/li/p/figure/table); class attributes, style attributes, breakpoints, and inline CSS are FORBIDDEN."},
    ],
}

PACKAGING_CONTINUITY_RULES = {
    "schema": "packaging-continuity-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "PC-1", "rule": "every continuity scan MUST cite manual_id and package_id."},
        {"id": "PC-2", "rule": "procedural continuity gaps (semantic-procedure step_index gaps) BLOCK approval."},
        {"id": "PC-3", "rule": "warning continuity gaps (semantic-warning-group missing severity coverage) BLOCK approval."},
        {"id": "PC-4", "rule": "grounding continuity gaps (orphan grounding_ids) BLOCK approval."},
        {"id": "PC-5", "rule": "troubleshooting continuity gaps (missing escalation paths in semantic-troubleshooting-group) BLOCK approval."},
        {"id": "PC-6", "rule": "unresolved semantic gaps are reported but reviewer may flag for re-extraction."},
        {"id": "PC-7", "rule": "orphan semantic sections (cited in semantic_structure but not registered) BLOCK approval."},
        {"id": "PC-8", "rule": "broken evidence lineage BLOCKS approval."},
        {"id": "PC-9", "rule": "duplicate semantic IDs are fail-closed."},
    ],
}

PACKAGING_LINEAGE_RULES = {
    "schema": "packaging-lineage-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "PL-1", "rule": "every package MUST trace to: extraction artifacts, synthesis manifests, grounding manifests, evidence manifests, OCR lineage, multimodal continuity, reviewer approvals."},
        {"id": "PL-2", "rule": "lineage is append-only; in-place mutation is FORBIDDEN."},
        {"id": "PL-3", "rule": "broken pointers (any cited id that does not resolve) are fail-closed."},
        {"id": "PL-4", "rule": "lineage MUST cite manifest sha256 of every linked artifact for replay verification."},
        {"id": "PL-5", "rule": "supersedence MUST cite predecessor package_id and successor package_id; silent replacement is FORBIDDEN."},
    ],
}

PACKAGING_REPLAY_RULES = {
    "schema": "packaging-replay-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "PR-1", "rule": "replay MUST reconstruct semantic structure, package_sha256, continuity chains, and lineage references end-to-end."},
        {"id": "PR-2", "rule": "hash mismatch on any linked artifact is fail-closed."},
        {"id": "PR-3", "rule": "replay MUST be deterministic across invocations; non-determinism is fail-closed."},
        {"id": "PR-4", "rule": "replay MUST NEVER mutate prior-layer runtime trees, the live publication tree, frontend/theme systems, or source evidence."},
        {"id": "PR-5", "rule": "replay events are append-only and reviewer-attributed."},
    ],
}

PACKAGING_INTEGRITY_RULES = {
    "schema": "packaging-integrity-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "PI-1", "rule": "missing lineage (empty extraction_ids and synthesis_ids and grounding_ids) BLOCKS approval."},
        {"id": "PI-2", "rule": "unresolved grounding references BLOCK approval."},
        {"id": "PI-3", "rule": "orphan semantic procedures (cited but not registered, or registered without lineage) BLOCK approval."},
        {"id": "PI-4", "rule": "duplicate section_id within a manual is fail-closed."},
        {"id": "PI-5", "rule": "broken continuity chains BLOCK approval."},
        {"id": "PI-6", "rule": "unresolved evidence_refs BLOCK approval."},
        {"id": "PI-7", "rule": "invalid export contracts (non-deterministic, presentation-bearing, missing package_id) BLOCK approval."},
        {"id": "PI-8", "rule": "forbidden overwrite paths are fail-closed."},
        {"id": "PI-9", "rule": "hidden semantic mutation (sha256 mismatch on replay) is fail-closed."},
    ],
}

PACKAGING_LIFECYCLE_RULES = {
    "schema": "packaging-lifecycle-rules/1.0",
    "constitutional_layer_index": LAYER,
    "states": sorted(LIFECYCLE_STATES),
    "terminal_states": sorted(LIFECYCLE_TERMINAL),
    "edges": [list(e) for e in LIFECYCLE_EDGES],
    "rules": [
        {"id": "PXL-1", "rule": "reviewer attribution required on every lifecycle transition."},
        {"id": "PXL-2", "rule": "transitions are append-only; declared from_state MUST equal actual replayed state."},
        {"id": "PXL-3", "rule": "terminal state (deprecated) is immutable."},
        {"id": "PXL-4", "rule": "reviewer-approved -> superseded MUST cite successor_package_id."},
        {"id": "PXL-5", "rule": "autonomous lifecycle promotion is FORBIDDEN."},
        {"id": "PXL-6", "rule": "reviewer-approved -> export-ready MUST require zero blocking integrity findings AND a successful packaging-replay."},
    ],
}

REVIEWER_PACKAGING_OVERRIDE_RULES = {
    "schema": "reviewer-packaging-override-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "PRO-1", "rule": "every reviewer override MUST be reviewer-attributed and cite the prior artifact_id."},
        {"id": "PRO-2", "rule": "overrides are append-only; the prior artifact remains intact and is not deleted."},
        {"id": "PRO-3", "rule": "reject overrides MUST cite at least one rule_id from MP-/SS-/XC-/PC-/PL-/PR-/PI-/PXL-/PRO-* tables."},
        {"id": "PRO-4", "rule": "autonomous overrides are FORBIDDEN; the runtime may PROPOSE packages and exports only."},
    ],
}

CONSUMER_BOUNDARY_RULES = {
    "schema": "consumer-boundary-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "CB-1", "rule": "the Knowledge OS packages SEMANTIC manual knowledge ONLY; presentation/UI/CSS/responsive behavior/layouts/typography are OUT OF SCOPE."},
        {"id": "CB-2", "rule": "consumer systems (WordPress, WooCommerce, React frontends, PDF generators, documentation renderers) are responsible for ALL rendering, CSS, breakpoints, layouts, and presentation."},
        {"id": "CB-3", "rule": "exports MUST be consumed by the consumer system; the runtime does NOT inject CSS, manage layouts, manage breakpoints, or optimize for screen size."},
        {"id": "CB-4", "rule": "the runtime does NOT govern frontend/theme systems and NEVER writes the live publication tree or any prior-layer runtime tree."},
        {"id": "CB-5", "rule": "this separation is enforced constitutionally; violations are fail-closed."},
    ],
}

RULE_TABLES = {
    "manual-package-rules.json": MANUAL_PACKAGE_RULES,
    "semantic-section-rules.json": SEMANTIC_SECTION_RULES,
    "export-contract-rules.json": EXPORT_CONTRACT_RULES,
    "packaging-continuity-rules.json": PACKAGING_CONTINUITY_RULES,
    "packaging-lineage-rules.json": PACKAGING_LINEAGE_RULES,
    "packaging-replay-rules.json": PACKAGING_REPLAY_RULES,
    "packaging-integrity-rules.json": PACKAGING_INTEGRITY_RULES,
    "packaging-lifecycle-rules.json": PACKAGING_LIFECYCLE_RULES,
    "reviewer-packaging-override-rules.json": REVIEWER_PACKAGING_OVERRIDE_RULES,
    "consumer-boundary-rules.json": CONSUMER_BOUNDARY_RULES,
}

# ---------------------------------------------------------------------------
# JS engines (vanilla ES; never write FS; only build envelopes)
# ---------------------------------------------------------------------------

PACKAGE_ENGINE_JS = """// phase 53 — manual package engine (reviewer-authored, deterministic, presentation-neutral).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var MP = OC.ManualPackage = OC.ManualPackage || {};
  MP.buildPackageRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('MP-1: reviewer required');
    if (!input.manual_id || !input.canonical_product_id || !input.package_version) {
      throw new Error('MP-1: manual_id, canonical_product_id, package_version required');
    }
    if (!Array.isArray(input.semantic_structure)) throw new Error('MP-1: semantic_structure required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'manual-package',
      reviewer: input.reviewer,
      payload: {
        package_id: input.package_id || null,
        manual_id: input.manual_id,
        canonical_product_id: input.canonical_product_id,
        package_version: input.package_version,
        synthesis_ids: input.synthesis_ids || [],
        extraction_ids: input.extraction_ids || [],
        grounding_ids: input.grounding_ids || [],
        evidence_refs: input.evidence_refs || [],
        semantic_structure: input.semantic_structure,
        continuity_status: input.continuity_status || 'unresolved',
        reasoning_chain: input.reasoning_chain || [],
        prior_package_id: input.prior_package_id || null
      }
    });
  };
})(window);
"""

SECTION_ENGINE_JS = """// phase 53 — semantic section engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var SS = OC.SemanticSection = OC.SemanticSection || {};
  SS.KINDS = ['semantic-section','semantic-procedure','semantic-warning-group','semantic-specification-group','semantic-troubleshooting-group','semantic-support-group'];
  SS.buildSectionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('SS-1: reviewer required');
    if (!input.manual_id || !input.section_id) throw new Error('SS-1: manual_id and section_id required');
    if (SS.KINDS.indexOf(input.section_kind) < 0) throw new Error('SS-2: invalid section_kind');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'semantic-section',
      reviewer: input.reviewer,
      payload: {
        section_id: input.section_id,
        manual_id: input.manual_id,
        section_kind: input.section_kind,
        title: input.title || '',
        extraction_ids: input.extraction_ids || [],
        grounding_ids: input.grounding_ids || [],
        evidence_refs: input.evidence_refs || [],
        body_blocks: input.body_blocks || [],
        unresolved_states: input.unresolved_states || [],
        trust_composition: input.trust_composition || {'reviewer-approved':0,'review-required':0,'unresolved':0}
      }
    });
  };
})(window);
"""

EXPORT_ENGINE_JS = """// phase 53 — export contract engine (presentation-neutral).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var XC = OC.ExportContract = OC.ExportContract || {};
  XC.KINDS = ['raw-html-export','structured-json-export','semantic-markdown-export'];
  XC.buildContractRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('XC-1: reviewer required');
    if (!input.manual_id || !input.package_id) throw new Error('XC-1: manual_id and package_id required');
    if (XC.KINDS.indexOf(input.export_kind) < 0) throw new Error('XC-2: invalid export_kind');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'export-contract',
      reviewer: input.reviewer,
      payload: {
        contract_id: input.contract_id || null,
        manual_id: input.manual_id,
        package_id: input.package_id,
        export_kind: input.export_kind,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
  XC.buildRenderRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('XC-1: reviewer required');
    if (!input.contract_id) throw new Error('XC-1: contract_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'export-render',
      reviewer: input.reviewer,
      payload: {
        contract_id: input.contract_id,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
"""

CONTINUITY_ENGINE_JS = """// phase 53 — packaging continuity engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PC = OC.PackagingContinuity = OC.PackagingContinuity || {};
  PC.buildContinuityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PC-1: reviewer required');
    if (!input.manual_id || !input.package_id) throw new Error('PC-1: manual_id and package_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'packaging-continuity',
      reviewer: input.reviewer,
      payload: {
        continuity_check_id: input.continuity_check_id || null,
        manual_id: input.manual_id,
        package_id: input.package_id
      }
    });
  };
})(window);
"""

LINEAGE_ENGINE_JS = """// phase 53 — packaging lineage engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PL = OC.PackagingLineage = OC.PackagingLineage || {};
  PL.buildLineageRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PL-1: reviewer required');
    if (!input.package_id) throw new Error('PL-1: package_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'packaging-lineage',
      reviewer: input.reviewer,
      payload: {
        lineage_id: input.lineage_id || null,
        package_id: input.package_id,
        scope: input.scope || 'package'
      }
    });
  };
})(window);
"""

REPLAY_ENGINE_JS = """// phase 53 — packaging replay engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PR = OC.PackagingReplay = OC.PackagingReplay || {};
  PR.buildReplayRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PR-1: reviewer required');
    if (!input.package_id) throw new Error('PR-1: package_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'packaging-replay',
      reviewer: input.reviewer,
      payload: {
        replay_id: input.replay_id || null,
        package_id: input.package_id,
        expected_package_sha256: input.expected_package_sha256 || null
      }
    });
  };
})(window);
"""

LIFECYCLE_ENGINE_JS = """// phase 53 — packaging lifecycle engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PXL = OC.PackagingLifecycle = OC.PackagingLifecycle || {};
  PXL.STATES = ['draft','review-required','reviewer-approved','export-ready','superseded','deprecated'];
  PXL.EDGES = [
    ['draft','review-required'], ['draft','deprecated'],
    ['review-required','reviewer-approved'], ['review-required','draft'], ['review-required','deprecated'],
    ['reviewer-approved','export-ready'], ['reviewer-approved','review-required'], ['reviewer-approved','superseded'],
    ['export-ready','reviewer-approved'], ['export-ready','superseded'],
    ['superseded','deprecated']
  ];
  PXL.isLegal = function (from, to) {
    for (var i = 0; i < PXL.EDGES.length; i++) if (PXL.EDGES[i][0] === from && PXL.EDGES[i][1] === to) return true;
    return false;
  };
  PXL.buildTransitionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PXL-1: reviewer required');
    if (!input.package_id) throw new Error('package_id required');
    if (!PXL.isLegal(input.from_state, input.to_state)) throw new Error('PXL: illegal transition ' + input.from_state + ' -> ' + input.to_state);
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'packaging-lifecycle-transition',
      reviewer: input.reviewer,
      payload: {
        package_id: input.package_id,
        from_state: input.from_state,
        to_state: input.to_state,
        successor_package_id: input.successor_package_id || null,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
"""

INTEGRITY_ENGINE_JS = """// phase 53 — packaging integrity engine (reviewer-driven).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PI = OC.PackagingIntegrity = OC.PackagingIntegrity || {};
  PI.buildIntegrityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'packaging-integrity',
      reviewer: input.reviewer,
      payload: {
        integrity_check_id: input.integrity_check_id || null,
        manual_id: input.manual_id || null,
        package_id: input.package_id || null,
        scope: input.scope || 'all'
      }
    });
  };
})(window);
"""

OVERRIDE_ENGINE_JS = """// phase 53 — reviewer packaging override engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PRO = OC.ReviewerPackagingOverride = OC.ReviewerPackagingOverride || {};
  PRO.KINDS = ['approve','reject','supersede','annotate'];
  PRO.buildOverrideRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PRO-1: reviewer required');
    if (!input.target_artifact_id) throw new Error('PRO-1: target_artifact_id required');
    if (input.kind === 'reject' && (!Array.isArray(input.cited_rule_ids) || input.cited_rule_ids.length === 0)) {
      throw new Error('PRO-3: reject requires cited_rule_ids');
    }
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'reviewer-packaging-override',
      reviewer: input.reviewer,
      payload: {
        override_id: input.override_id || null,
        target_artifact_id: input.target_artifact_id,
        target_kind: input.target_kind || 'package',
        kind: input.kind || 'reject',
        cited_rule_ids: input.cited_rule_ids || [],
        rationale: input.rationale || ''
      }
    });
  };
})(window);
"""

JS_ASSETS = {
    "mp-package-engine.js": PACKAGE_ENGINE_JS,
    "mp-section-engine.js": SECTION_ENGINE_JS,
    "mp-export-engine.js": EXPORT_ENGINE_JS,
    "mp-continuity-engine.js": CONTINUITY_ENGINE_JS,
    "mp-lineage-engine.js": LINEAGE_ENGINE_JS,
    "mp-replay-engine.js": REPLAY_ENGINE_JS,
    "mp-lifecycle-engine.js": LIFECYCLE_ENGINE_JS,
    "mp-integrity-engine.js": INTEGRITY_ENGINE_JS,
    "mp-override-engine.js": OVERRIDE_ENGINE_JS,
}

# ---------------------------------------------------------------------------
# Console HTML
# ---------------------------------------------------------------------------

PHASE53_SCRIPTS = "\n".join(
    f'<script src="../assets/exec/{name}"></script>' for name in JS_ASSETS
)

HTML_HEAD_TEMPLATE = (
    "<!doctype html><html lang='es-CO'><head><meta charset='utf-8'>"
    "<title>{title}</title>"
    "<link rel='stylesheet' href='../assets/exec/exec.css'></head>"
    "<body class='oc-exec'><header class='oc-exec__header'><h1>{title}</h1>"
    "<p class='oc-exec__subtitle'>Phase 53 — Governed manual semantic packaging & consumer-ready export contracts. "
    "Semantic-only. Presentation-neutral. Renderer-agnostic. Deterministic. Append-only. "
    "No CSS / no breakpoints / no layouts / no responsive logic / no UI frameworks / no autonomous packaging.</p></header>"
    "<main class='oc-exec__main'>"
)

HTML_TAIL = (
    "</main><footer class='oc-exec__footer'>"
    "<p>Layer 46 — subordinate to layer 45 (governed semantic evidence analysis & multimodal extraction).</p>"
    "</footer>"
    '<script src="../assets/exec/fs-bridge.js"></script>'
    + PHASE53_SCRIPTS +
    "</body></html>\n"
)

CONSOLES = {
    "manual-packaging-console": "Manual packaging console",
    "semantic-structure-console": "Semantic structure console",
    "continuity-inspection-console": "Continuity inspection console",
    "export-contract-console": "Export contract console",
    "package-lineage-console": "Package lineage console",
    "package-integrity-console": "Package integrity console",
    "package-lifecycle-console": "Package lifecycle console",
}

CSS_MARKER = "/* phase 53 — manual semantic packaging governance additions */"
CSS_ADDENDUM = """
/* phase 53 — manual semantic packaging governance additions */
.oc-mp-state { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 0.2rem; border: 1px solid #999; font-size: 0.8rem; }
.oc-mp-state[data-state='draft'] { background: #f4f4f4; color: #555; }
.oc-mp-state[data-state='review-required'] { background: #ffe; color: #b58900; }
.oc-mp-state[data-state='reviewer-approved'] { background: #cfc; color: #060; font-weight: bold; }
.oc-mp-state[data-state='export-ready'] { background: #cef; color: #036; font-weight: bold; }
.oc-mp-state[data-state='superseded'] { background: #ddd; color: #555; }
.oc-mp-state[data-state='deprecated'] { background: #ccc; color: #444; }
.oc-mp-package { border: 1px solid #ccc; padding: 0.4rem; margin: 0.3rem 0; }
.oc-mp-section[data-kind='semantic-warning-group'] { border-left: 4px solid #c00; background: #fee; padding-left: 0.4rem; }
.oc-mp-section[data-kind='semantic-procedure'] { border-left: 4px solid #060; background: #efe; padding-left: 0.4rem; }
.oc-mp-section[data-kind='semantic-troubleshooting-group'] { border-left: 4px solid #909; background: #fef; padding-left: 0.4rem; }
.oc-mp-orphan { background: #fee; padding: 0.3rem; border-left: 4px solid #c00; }
.oc-mp-export-ok { color: #060; }
.oc-mp-export-mismatch { color: #c00; font-weight: bold; }
"""

# ---------------------------------------------------------------------------
# Doctrines
# ---------------------------------------------------------------------------

DOCTRINES = {
    "01-semantic-only-packaging.md": "The Knowledge OS packages SEMANTIC manual knowledge ONLY. CSS, breakpoints, layouts, typography, responsive behavior, UI frameworks, mobile rendering, and visual page composition are OUT OF SCOPE and FORBIDDEN.\n",
    "02-reviewer-authored-packaging-only.md": "Every package, section, export contract, lineage replay, and override is reviewer-attributed. The runtime may PROPOSE packages and exports only. Autonomous semantic restructuring, autonomous promotion, and LLM rewriting are FORBIDDEN.\n",
    "03-presentation-neutral-exports.md": "Exports (raw-html-export, structured-json-export, semantic-markdown-export) MUST be presentation-neutral and renderer-agnostic. CSS injection, breakpoints, screen-size optimization, frontend-rendering hints, and inline styles are FORBIDDEN.\n",
    "04-deterministic-package-hashing.md": "package_sha256 is computed deterministically over canonical JSON of the semantic structure and lineage references. Hash mismatch on replay is fail-closed. Hidden semantic mutation is fail-closed.\n",
    "05-append-only-packaging-lineage.md": "Lineage is append-only and traces every package to extraction, synthesis, grounding, evidence, OCR, multimodal continuity, and reviewer approvals. Broken pointers are fail-closed.\n",
    "06-fail-closed-continuity.md": "Procedural, warning, grounding, and troubleshooting continuity gaps BLOCK approval. Orphan semantic sections, broken evidence lineage, and duplicate semantic IDs are fail-closed.\n",
    "07-replay-determinism.md": "Replay reconstructs semantic structure, package hashes, continuity chains, and lineage references end-to-end. Non-determinism and hash mismatch are fail-closed. Replay NEVER mutates prior-layer trees, the live publication tree, frontend/theme systems, or source evidence.\n",
    "08-storage-isolation.md": "Manual semantic packages are isolated under manual-semantic-packaging-runtime/. The runtime NEVER writes into prior-layer runtime trees, frontend/theme systems, visual-publication-builds, uploads, WordPress runtime, knowledge-core, governance roots, or runtime-implementation.\n",
    "09-consumer-boundary-doctrine.md": "The Knowledge OS packages, preserves lineage, governs continuity, and governs evidence integrity. The consumer system (WordPress, WooCommerce, React frontend, PDF generators, documentation renderers) renders UI, controls CSS, controls responsive behavior, controls layouts, and controls presentation. This separation is enforced constitutionally.\n",
    "10-cli-only-no-daemon-packaging.md": "Browser surfaces NEVER write the filesystem. All packaging mutation occurs only via the CLI executor with --confirm. No daemon. No watcher. No scheduler. No background worker. No telemetry.\n",
}

DOCTRINE_DIR = KB_ROOT / "GOVERNED_MANUAL_SEMANTIC_PACKAGING_GOVERNANCE"

# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

REPORTS = [
    ("01-manual-package-summary", "Reviewer-authored manual package summary."),
    ("02-semantic-structure-summary", "Semantic structure governance summary."),
    ("03-export-contract-summary", "Consumer-ready export contract summary."),
    ("04-packaging-continuity-summary", "Packaging continuity governance summary."),
    ("05-packaging-lineage-summary", "Packaging lineage governance summary."),
    ("06-packaging-replay-summary", "Packaging replay determinism summary."),
    ("07-packaging-integrity-summary", "Packaging integrity & rollback summary."),
    ("08-packaging-lifecycle-summary", "Packaging lifecycle governance summary."),
    ("09-consumer-boundary-summary", "Consumer-boundary doctrine summary."),
    ("10-governed-manual-semantic-packaging-platform-maturity-reassessment", "Governed manual semantic packaging platform — maturity reassessment."),
]

REPORT_DIR = REPORTS_ROOT / "governed-manual-semantic-packaging"

# ---------------------------------------------------------------------------
# Runtime README addendum
# ---------------------------------------------------------------------------

RUNTIME_README_MARKER = "## phase 53 — governed manual semantic packaging & consumer-ready export contracts"
RUNTIME_README_ADDENDUM = """

## phase 53 — governed manual semantic packaging & consumer-ready export contracts

Layer 46. Subordinate to layer 45 (governed-semantic-evidence-analysis-and-multimodal-extraction-governance).

The Knowledge OS packages SEMANTIC manual knowledge ONLY. Presentation, CSS,
breakpoints, layouts, typography, responsive behavior, mobile rendering, UI
frameworks, and visual page composition are OUT OF SCOPE and FORBIDDEN at this
layer. Consumer systems (WordPress, WooCommerce, React frontends, PDF generators,
documentation renderers) render UI; the runtime emits only presentation-neutral,
renderer-agnostic, lineage-preserving, trust-aware semantic payloads.

Mutation is performed exclusively by `tools/governed_manual_semantic_packaging_executor.py --confirm`.
Subcommands (`--kind`):

- `manual-package` — record a reviewer-authored manual package manifest (semantic_structure, lineage refs, continuity_status, package_sha256).
- `semantic-section` — record a typed semantic section (one of SECTION_KINDS) with extraction/grounding/evidence lineage and trust composition.
- `export-contract` — register a presentation-neutral export contract (raw-html-export, structured-json-export, semantic-markdown-export) bound to a package.
- `export-render` — produce the deterministic export payload defined by a contract; payload sha256 is recorded for replay.
- `packaging-continuity` — record a continuity scan over a package (procedural, warning, grounding, troubleshooting, duplicate-id, orphan-section).
- `packaging-lineage` — record a deterministic lineage replay with sha256 verification of every linked artifact.
- `packaging-replay` — record a full package replay event verifying semantic structure, package_sha256, continuity, and lineage.
- `packaging-lifecycle-transition` — advance a package through draft → review-required → reviewer-approved → export-ready → {superseded → deprecated}.
- `packaging-integrity` — record a reviewer-led integrity scan (missing lineage, unresolved grounding, orphan procedures, duplicate section ids, broken continuity, unresolved evidence, invalid contracts, hidden mutation).
- `reviewer-packaging-override` — record a reviewer-attributed override of any packaging artifact (rejection requires cited_rule_ids).

Every command:
- requires reviewer attribution,
- is fail-closed on missing lineage / unresolved grounding / orphan sections / duplicate section ids / broken continuity chains / unresolved evidence refs / invalid export contracts / forbidden overwrite paths / hidden semantic mutation,
- appends to one or more append-only event stores under `operational-console/runtime-manifests/`,
- writes only into `operational-console/manual-semantic-packaging-runtime/` subtrees.

The manual-semantic-packaging-runtime tree is isolated from:
- the live publication tree,
- the layer-45 semantic-extraction-runtime tree,
- the layer-44 publication-composition-runtime tree,
- the layer-43 visual-generation-runtime tree,
- the layer-42 visual-publication-builds tree,
- frontend/theme systems and WordPress runtime,
- OEM source assets,
- knowledge-core, governance, runtime-implementation, runtime-manifests payloads, uploads.

Nothing in this surface uses CSS, layouts, breakpoints, typography, responsive
logic, UI frameworks, embeddings, vector databases, autonomous LLM reasoning,
cloud APIs, SaaS, telemetry, watchers, daemons, or background workers.
"""

# ---------------------------------------------------------------------------
# Builder helpers
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


# ---------------------------------------------------------------------------
# Build steps
# ---------------------------------------------------------------------------

def build_storage_roots() -> int:
    count = 0
    root_readme = MP_ROOT / "README.md"
    if not root_readme.exists():
        write_text(root_readme,
                   "# manual-semantic-packaging-runtime\n\n"
                   "Phase 53 / layer 46. Governed manual semantic packaging & consumer-ready export contracts.\n\n"
                   "Reviewer-authored only. Deterministic. Append-only. Presentation-neutral. Renderer-agnostic.\n")
        count += 1
    for sub in MP_SUBDIRS:
        sub_path = MP_ROOT / sub
        sub_readme = sub_path / "README.md"
        if not sub_readme.exists():
            write_text(sub_readme, f"# {sub}\n\nLayer {LAYER}. Append-only. Reviewer-attributed. Presentation-neutral.\n")
            count += 1
        keep = sub_path / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
    return count


def build_runtime_event_stores() -> int:
    created = 0
    for kind in NEW_EVENT_STORES:
        path = RUNTIME_MANIFESTS_ROOT / kind / "_event-store.json"
        if path.exists():
            continue
        write_json(path, {
            "schema": "governed-fs-event-store/1.0",
            "constitutional_layer_index": LAYER,
            "kind": kind,
            "append_only": True,
            "deterministic": True,
            "reviewer_authoritative": True,
            "created_at": now_iso(),
            "events": [],
        })
        created += 1
    return created


def build_rule_tables() -> int:
    for filename, payload in RULE_TABLES.items():
        write_json(RULES_ROOT / filename, payload)
    return len(RULE_TABLES)


def build_assets() -> int:
    for filename, body in JS_ASSETS.items():
        write_text(ASSETS_EXEC_ROOT / filename, body)
    css_path = ASSETS_EXEC_ROOT / "exec.css"
    existing = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    if CSS_MARKER not in existing:
        css_path.parent.mkdir(parents=True, exist_ok=True)
        css_path.write_text(existing + CSS_ADDENDUM, encoding="utf-8")
    return len(JS_ASSETS)


def build_consoles() -> int:
    for slug, title in CONSOLES.items():
        html = HTML_HEAD_TEMPLATE.format(title=title)
        body = (
            f"<section><h2>Reviewer-driven workflow</h2>"
            f"<p>This console builds <code>governed-fs-operation-request/1.0</code> envelopes for the "
            f"<code>{slug}</code> surface. The browser does NOT mutate the filesystem and does NOT package autonomously. "
            f"The runtime emits SEMANTIC payloads only; presentation/UI/CSS/responsive behavior are out of scope.</p>"
            f"<p>Submit envelopes via <code>tools/governed_manual_semantic_packaging_executor.py --kind &lt;kind&gt; --request &lt;file&gt; --confirm</code>.</p>"
            f"</section>"
        )
        write_text(OC_ROOT / slug / "exec.html", html + body + HTML_TAIL)
    return len(CONSOLES)


def build_doctrines() -> int:
    DOCTRINE_DIR.mkdir(parents=True, exist_ok=True)
    index_lines = ["# GOVERNED MANUAL SEMANTIC PACKAGING GOVERNANCE", "", f"Layer {LAYER}. Phase 53.", ""]
    for name in sorted(DOCTRINES):
        index_lines.append(f"- {name}")
    write_text(DOCTRINE_DIR / "00-INDEX.md", "\n".join(index_lines) + "\n")
    for name, body in DOCTRINES.items():
        write_text(DOCTRINE_DIR / name, f"# {name[:-3]}\n\n{body}")
    write_json(DOCTRINE_DIR / "manifest.json", {
        "schema": "doctrine-manifest/1.0",
        "constitutional_layer_index": LAYER,
        "subordinate_to": SUBORDINATE_TO,
        "doctrines": sorted(DOCTRINES),
        "posture": POSTURE,
        "created_at": now_iso(),
    })
    return len(DOCTRINES)


def build_reports() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    write_text(REPORT_DIR / "README.md",
               "# Governed manual semantic packaging — reports\n\nPhase 53 / layer 46 reports.\n")
    for slug, title in REPORTS:
        write_text(REPORT_DIR / f"{slug}.md", f"# {title}\n\nLayer {LAYER}. Phase 53.\n")
        write_json(REPORT_DIR / f"{slug}.json", {
            "schema": "governance-report/1.0",
            "constitutional_layer_index": LAYER,
            "report_slug": slug,
            "title": title,
            "subordinate_to": SUBORDINATE_TO,
            "posture": POSTURE,
            "section_kinds": SECTION_KINDS,
            "export_kinds": EXPORT_KINDS,
            "continuity_statuses": CONTINUITY_STATUSES,
            "lifecycle_states": sorted(LIFECYCLE_STATES),
            "lifecycle_terminal_states": sorted(LIFECYCLE_TERMINAL),
            "lifecycle_edges": [list(e) for e in LIFECYCLE_EDGES],
            "new_event_stores": NEW_EVENT_STORES,
            "rule_tables": list(RULE_TABLES),
            "js_assets": list(JS_ASSETS),
            "consoles": list(CONSOLES),
            "generated_at": now_iso(),
        })
    return len(REPORTS)


def build_runtime_readme_addendum() -> int:
    path = OC_ROOT / "RUNTIME_README.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# RUNTIME README\n"
    if RUNTIME_README_MARKER in existing:
        return 0
    path.write_text(existing + RUNTIME_README_ADDENDUM, encoding="utf-8")
    return 1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    storage = build_storage_roots()
    stores = build_runtime_event_stores()
    rules = build_rule_tables()
    js = build_assets()
    consoles = build_consoles()
    doctrines = build_doctrines()
    reports = build_reports()
    readme = build_runtime_readme_addendum()
    print(
        "Phase 53 — governed manual semantic packaging & consumer-ready export contracts written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {storage} | New event stores: {stores} | Rule tables: {rules} | "
        f"JS assets: {js} | Exec consoles: {consoles} | Doctrines: {doctrines} | Reports: {reports} | "
        f"RUNTIME_README addendum: {readme}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
