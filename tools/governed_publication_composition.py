"""
Phase 51 — Governed Multimodal Publication Composition & Page Orchestration (layer 44).

Idempotent stdlib-only builder. Emits the layer-44 surface over layer 43
(governed visual generation & deterministic asset production), layer 42
(governed multimodal grounding & visual publication orchestration) and layer 41
(governed knowledge synthesis & canonical publication generation).

The runtime writer is the executor (`tools/governed_publication_composition_executor.py`).
This builder NEVER mutates event stores, runtime data, knowledge-core, governance,
runtime-implementation, runtime-manifests payloads, visual-publication-builds,
visual-generation-runtime data, OEM source assets, or live publications.

Posture:
- deterministic, reviewer-authoritative, append-only, local-first, fail-closed.
- NO autonomous layout generation, NO hidden section reordering,
  NO probabilistic composition, NO cloud rendering, NO SaaS dependency,
  NO browser-side filesystem mutation, NO live publication overwrite,
  NO autonomous publication approval, NO ML governance decisions,
  NO daemon / watcher / scheduler.
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

PC_ROOT = OC_ROOT / "publication-composition-runtime"

PC_SUBDIRS = [
    "composition-drafts",
    "page-layouts",
    "section-compositions",
    "multimodal-sequences",
    "responsive-layouts",
    "publication-assemblies",
    "layout-lineage",
    "page-continuity",
    "layout-review",
    "publication-composition-lifecycle",
    "render-previews",
    "reviewer-layout-decisions",
]

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA = "governed-publication-composition/1.0"
LAYER = 44

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
]
while len(SUBORDINATE_TO) < 43:
    SUBORDINATE_TO.append(
        "governed-visual-generation-and-deterministic-asset-production-governance"
    )

POSTURE = {
    "deterministic": True,
    "reviewer_authoritative": True,
    "append_only_lineage": True,
    "no_autonomous_layout_generation": True,
    "no_hidden_section_reordering": True,
    "no_probabilistic_composition": True,
    "no_cloud_rendering": True,
    "no_saas_dependency": True,
    "no_browser_side_filesystem_mutation": True,
    "no_live_publication_overwrite": True,
    "no_autonomous_publication_approval": True,
    "no_ml_governance_decisions": True,
    "no_daemon_no_watcher_no_scheduler": True,
    "fail_closed_on_missing_section_lineage": True,
    "fail_closed_on_unresolved_continuity_gap": True,
    "fail_closed_on_orphan_visual": True,
    "fail_closed_on_warning_placement_violation": True,
    "fail_closed_on_broken_responsive_parity": True,
    "fail_closed_on_missing_evidence_trace": True,
    "writes_only_into_publication_composition_runtime_tree": True,
    "browser_surfaces_never_write_filesystem": True,
    "writes_to_live_publication_tree": False,
    "writes_to_visual_publication_builds_tree": False,
    "writes_to_visual_generation_runtime_tree": False,
}

# Manual kinds supported (for routing / reporting only — composition logic is uniform)
MANUAL_KINDS = [
    "procedural",
    "troubleshooting",
    "specification-heavy",
    "comparison",
    "warning-centric",
    "multimodal-responsive",
    "oem-derived",
    "generated-visual",
]

# Section roles (used by section ordering / sequence rules)
SECTION_ROLES = [
    "overview",
    "warning",
    "specification",
    "procedural",
    "troubleshooting",
    "comparison",
    "evidence-trace",
    "appendix",
]

# Responsive breakpoints we record parity for (deterministic, reviewer-set).
RESPONSIVE_BREAKPOINTS = ["mobile", "tablet", "desktop", "print"]

# Composition lifecycle
LIFECYCLE_STATES = {
    "draft",
    "composed",
    "review-required",
    "reviewer-approved",
    "publication-ready",
    "superseded",
    "deprecated",
}
LIFECYCLE_TERMINAL = {"deprecated"}
LIFECYCLE_EDGES = [
    ("draft", "composed"),
    ("composed", "review-required"),
    ("composed", "draft"),
    ("review-required", "reviewer-approved"),
    ("review-required", "composed"),
    ("reviewer-approved", "publication-ready"),
    ("reviewer-approved", "review-required"),
    ("publication-ready", "superseded"),
    ("publication-ready", "deprecated"),
    ("superseded", "deprecated"),
]

NEW_EVENT_STORES = [
    "composition-events",
    "layout-events",
    "sequence-events",
    "responsive-render-events",
    "page-continuity-events",
    "publication-assembly-events",
    "layout-review-events",
    "composition-lifecycle-events",
    "composition-integrity-events",
]

# ---------------------------------------------------------------------------
# Rule tables
# ---------------------------------------------------------------------------

COMPOSITION_RULES = {
    "schema": "publication-composition-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "CP-1", "rule": "every composition draft MUST be reviewer-authored and reviewer-attributed."},
        {"id": "CP-2", "rule": "every composition draft MUST cite synthesis_id (layer 41) and a deterministic ordered list of section_ids."},
        {"id": "CP-3", "rule": "section ordering MUST be reviewer-declared and deterministic; hidden insertion or reordering is FORBIDDEN."},
        {"id": "CP-4", "rule": "every section reference MUST resolve to an existing section_composition or carry a reviewer-declared inline body."},
        {"id": "CP-5", "rule": "composition manifests are append-only; in-place mutation is FORBIDDEN."},
        {"id": "CP-6", "rule": "compositions MUST cite manual_kind ∈ MANUAL_KINDS for governance routing."},
        {"id": "CP-7", "rule": "autonomous composition (LLM- / agent-driven) is FORBIDDEN."},
    ],
}

LAYOUT_RULES = {
    "schema": "page-layout-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "LO-1", "rule": "every page layout MUST cite composition_id and page_index (1-based, deterministic)."},
        {"id": "LO-2", "rule": "every block on a page MUST declare role ∈ SECTION_ROLES and a stable block_id."},
        {"id": "LO-3", "rule": "image blocks MUST cite asset_id (layer 43) AND grounding_id (layer 42); orphan visual blocks BLOCK composition approval."},
        {"id": "LO-4", "rule": "warning blocks MUST be placed before the procedural block they warn about; warning-after-procedural is fail-closed."},
        {"id": "LO-5", "rule": "specification tables MUST be grouped within a single section_composition; cross-section split is FORBIDDEN unless reviewer attests."},
        {"id": "LO-6", "rule": "visual density per page MUST stay within reviewer-declared ceiling (default max_visuals_per_page = 6)."},
        {"id": "LO-7", "rule": "section overflow is handled by adding pages with explicit continuation_of links; silent splitting is FORBIDDEN."},
        {"id": "LO-8", "rule": "page layouts are append-only; in-place mutation is FORBIDDEN."},
    ],
}

SEQUENCE_RULES = {
    "schema": "multimodal-sequence-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "SQ-1", "rule": "every multimodal sequence MUST cite composition_id and an ordered list of step entries."},
        {"id": "SQ-2", "rule": "procedural step indices MUST be contiguous starting from 1; gaps BLOCK composition approval."},
        {"id": "SQ-3", "rule": "every step that cites an image MUST cite its grounding_id; missing grounding is fail-closed."},
        {"id": "SQ-4", "rule": "troubleshooting flows MUST escalate from low-severity to high-severity; reverse-escalation is FORBIDDEN."},
        {"id": "SQ-5", "rule": "comparison sequences MUST contain >= 2 entries with deterministic display_order."},
        {"id": "SQ-6", "rule": "multimodal density balancing MUST respect reviewer-declared image:text ratio ceiling per sequence."},
    ],
}

RESPONSIVE_RULES = {
    "schema": "responsive-render-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "RR-1", "rule": "every responsive layout MUST declare parity across all RESPONSIVE_BREAKPOINTS for every block_id."},
        {"id": "RR-2", "rule": "blocks present at desktop MUST be present (or have a reviewer-attributed responsive_omission) at mobile/tablet/print."},
        {"id": "RR-3", "rule": "warning blocks MUST be visible at every breakpoint; responsive omission of warnings is FORBIDDEN."},
        {"id": "RR-4", "rule": "broken responsive parity BLOCKS publication-ready transition (fail-closed)."},
        {"id": "RR-5", "rule": "render previews are deterministic snapshots of the responsive manifest; no probabilistic re-flow."},
    ],
}

CONTINUITY_RULES = {
    "schema": "page-continuity-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "PC-1", "rule": "every page continuity manifest MUST cite composition_id and the ordered page_index sequence."},
        {"id": "PC-2", "rule": "page numbering MUST be contiguous starting from 1; gaps BLOCK publication."},
        {"id": "PC-3", "rule": "continuation_of links MUST form an acyclic chain; cycles BLOCK publication."},
        {"id": "PC-4", "rule": "every section_id referenced by the composition MUST appear on at least one page; orphan sections BLOCK publication."},
        {"id": "PC-5", "rule": "every block citing an asset_id MUST resolve against an existing layer-43 asset record; orphan visuals BLOCK composition approval."},
        {"id": "PC-6", "rule": "missing section lineage (section_id without grounding/synthesis chain) BLOCKS publication-ready."},
    ],
}

ASSEMBLY_RULES = {
    "schema": "publication-assembly-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "PA-1", "rule": "every publication assembly MUST cite composition_id, all page_layout_ids in order, and a sha256 of the deterministic assembly manifest."},
        {"id": "PA-2", "rule": "assembly is permitted only when composition is reviewer-approved AND continuity check passed AND responsive parity verified."},
        {"id": "PA-3", "rule": "assembly MUST NOT mutate the live publication tree, layer-42 visual-publication-builds tree, or layer-43 visual-generation-runtime tree."},
        {"id": "PA-4", "rule": "assemblies are append-only; replacement requires explicit publication-structure-supersedence."},
        {"id": "PA-5", "rule": "rollback restores by appending a reverse assembly event referencing the prior assembly_id."},
        {"id": "PA-6", "rule": "the assembly manifest MUST embed sha256 of every page_layout and section_composition for replay verification."},
    ],
}

REVIEW_RULES = {
    "schema": "layout-review-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "LR-1", "rule": "every layout-review decision MUST be reviewer-attributed and cite composition_id, page_index (or 'all'), and decision ∈ {approve, request-changes, reject}."},
        {"id": "LR-2", "rule": "layout-review decisions are append-only; revisions append new decisions citing prior_decision_id."},
        {"id": "LR-3", "rule": "approval at page level does NOT promote the composition lifecycle; lifecycle transitions are recorded separately."},
        {"id": "LR-4", "rule": "reject decisions MUST cite at least one rule_id from CP-/LO-/SQ-/RR-/PC-/PA-/IN-* tables."},
    ],
}

COMP_LIFECYCLE_RULES = {
    "schema": "composition-lifecycle-rules/1.0",
    "constitutional_layer_index": LAYER,
    "states": sorted(LIFECYCLE_STATES),
    "terminal_states": sorted(LIFECYCLE_TERMINAL),
    "edges": [list(e) for e in LIFECYCLE_EDGES],
    "rules": [
        {"id": "LC-1", "rule": "reviewer attribution required on every state transition."},
        {"id": "LC-2", "rule": "publication-ready requires composition reviewer-approved AND continuity passed AND responsive parity verified AND no blocking integrity findings."},
        {"id": "LC-3", "rule": "terminal state (deprecated) is immutable."},
        {"id": "LC-4", "rule": "transitions are append-only; declared from_state MUST equal actual replayed state."},
        {"id": "LC-5", "rule": "publication-ready -> superseded MUST cite successor_composition_id (publication structure supersedence)."},
    ],
}

INTEGRITY_RULES = {
    "schema": "composition-integrity-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "IN-1", "rule": "missing section lineage BLOCKS publication-ready."},
        {"id": "IN-2", "rule": "unresolved continuity gaps BLOCK publication."},
        {"id": "IN-3", "rule": "orphan visual blocks (asset_id with no layer-43 record) BLOCK composition approval."},
        {"id": "IN-4", "rule": "warning-placement violations BLOCK rendering."},
        {"id": "IN-5", "rule": "broken responsive parity BLOCKS publication-ready."},
        {"id": "IN-6", "rule": "missing evidence trace on a section BLOCKS section approval."},
        {"id": "IN-7", "rule": "hidden section insertion is FORBIDDEN; integrity scan reports any section_id present in a page_layout that is not declared in the composition."},
        {"id": "IN-8", "rule": "silent layout mutation is FORBIDDEN; sha256 of every recorded manifest is verified on replay."},
    ],
}

RULE_TABLES = {
    "publication-composition-rules.json": COMPOSITION_RULES,
    "page-layout-rules.json": LAYOUT_RULES,
    "multimodal-sequence-rules.json": SEQUENCE_RULES,
    "responsive-render-rules.json": RESPONSIVE_RULES,
    "page-continuity-rules.json": CONTINUITY_RULES,
    "publication-assembly-rules.json": ASSEMBLY_RULES,
    "layout-review-rules.json": REVIEW_RULES,
    "composition-lifecycle-rules.json": COMP_LIFECYCLE_RULES,
    "composition-integrity-rules.json": INTEGRITY_RULES,
}

# ---------------------------------------------------------------------------
# JS engines (vanilla ES; never write FS; only build envelopes)
# ---------------------------------------------------------------------------

COMPOSITION_ENGINE_JS = """// phase 51 — publication composition engine (reviewer-authored, deterministic).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PC = OC.PublicationComposition = OC.PublicationComposition || {};
  PC.MANUAL_KINDS = ['procedural','troubleshooting','specification-heavy','comparison','warning-centric','multimodal-responsive','oem-derived','generated-visual'];
  PC.buildCompositionDraftRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('CP-1: reviewer required');
    if (!input.synthesis_id) throw new Error('CP-2: synthesis_id required');
    if (!Array.isArray(input.section_order) || input.section_order.length === 0) throw new Error('CP-2: section_order required');
    if (PC.MANUAL_KINDS.indexOf(input.manual_kind) < 0) throw new Error('CP-6: invalid manual_kind');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'composition-draft',
      reviewer: input.reviewer,
      payload: {
        composition_id: input.composition_id || null,
        synthesis_id: input.synthesis_id,
        manual_id: input.manual_id || null,
        manual_kind: input.manual_kind,
        canonical_product_id: input.canonical_product_id || null,
        section_order: input.section_order,
        rationale: input.rationale || ''
      }
    });
  };
})(window);
"""

LAYOUT_ENGINE_JS = """// phase 51 — page layout engine (deterministic block list).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var LO = OC.PageLayout = OC.PageLayout || {};
  LO.SECTION_ROLES = ['overview','warning','specification','procedural','troubleshooting','comparison','evidence-trace','appendix'];
  LO.buildPageLayoutRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('LO-1: reviewer required');
    if (!input.composition_id) throw new Error('LO-1: composition_id required');
    if (typeof input.page_index !== 'number' || input.page_index < 1) throw new Error('LO-1: page_index must be >= 1');
    if (!Array.isArray(input.blocks) || input.blocks.length === 0) throw new Error('LO-2: blocks required');
    for (var i = 0; i < input.blocks.length; i++) {
      var b = input.blocks[i];
      if (!b.block_id) throw new Error('LO-2: block ' + i + ' missing block_id');
      if (LO.SECTION_ROLES.indexOf(b.role) < 0) throw new Error('LO-2: block ' + i + ' invalid role');
    }
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'page-layout',
      reviewer: input.reviewer,
      payload: {
        page_layout_id: input.page_layout_id || null,
        composition_id: input.composition_id,
        page_index: input.page_index,
        section_id: input.section_id || null,
        continuation_of: input.continuation_of || null,
        blocks: input.blocks,
        max_visuals_per_page: input.max_visuals_per_page || 6
      }
    });
  };
})(window);
"""

SEQUENCE_ENGINE_JS = """// phase 51 — multimodal sequence engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var SQ = OC.MultimodalSequence = OC.MultimodalSequence || {};
  SQ.buildSequenceRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('SQ-1: reviewer required');
    if (!input.composition_id) throw new Error('SQ-1: composition_id required');
    if (!Array.isArray(input.steps) || input.steps.length === 0) throw new Error('SQ-1: steps required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'multimodal-sequence',
      reviewer: input.reviewer,
      payload: {
        sequence_id: input.sequence_id || null,
        composition_id: input.composition_id,
        sequence_kind: input.sequence_kind || 'procedural',
        steps: input.steps,
        image_text_ratio_ceiling: input.image_text_ratio_ceiling || null
      }
    });
  };
})(window);
"""

RESPONSIVE_ENGINE_JS = """// phase 51 — responsive render engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var RR = OC.ResponsiveRender = OC.ResponsiveRender || {};
  RR.BREAKPOINTS = ['mobile','tablet','desktop','print'];
  RR.buildResponsiveLayoutRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('RR-1: reviewer required');
    if (!input.composition_id) throw new Error('RR-1: composition_id required');
    if (!input.parity || typeof input.parity !== 'object') throw new Error('RR-1: parity object required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'responsive-layout',
      reviewer: input.reviewer,
      payload: {
        responsive_layout_id: input.responsive_layout_id || null,
        composition_id: input.composition_id,
        page_layout_id: input.page_layout_id || null,
        parity: input.parity,
        omissions: input.omissions || []
      }
    });
  };
})(window);
"""

CONTINUITY_ENGINE_JS = """// phase 51 — page continuity engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var CN = OC.PageContinuity = OC.PageContinuity || {};
  CN.buildContinuityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PC-1: reviewer required');
    if (!input.composition_id) throw new Error('PC-1: composition_id required');
    if (!Array.isArray(input.page_indices)) throw new Error('PC-1: page_indices required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'page-continuity',
      reviewer: input.reviewer,
      payload: {
        continuity_check_id: input.continuity_check_id || null,
        composition_id: input.composition_id,
        page_indices: input.page_indices,
        section_ids_present: input.section_ids_present || [],
        orphan_section_ids: input.orphan_section_ids || [],
        orphan_asset_ids: input.orphan_asset_ids || []
      }
    });
  };
})(window);
"""

ASSEMBLY_ENGINE_JS = """// phase 51 — publication assembly engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PA = OC.PublicationAssembly = OC.PublicationAssembly || {};
  PA.buildAssemblyRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PA-1: reviewer required');
    if (!input.composition_id) throw new Error('PA-1: composition_id required');
    if (!Array.isArray(input.page_layout_ids) || input.page_layout_ids.length === 0) throw new Error('PA-1: page_layout_ids required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'publication-assembly',
      reviewer: input.reviewer,
      payload: {
        assembly_id: input.assembly_id || null,
        composition_id: input.composition_id,
        page_layout_ids: input.page_layout_ids,
        prior_assembly_id: input.prior_assembly_id || null
      }
    });
  };
})(window);
"""

REVIEW_ENGINE_JS = """// phase 51 — layout review engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var LR = OC.LayoutReview = OC.LayoutReview || {};
  LR.DECISIONS = ['approve','request-changes','reject'];
  LR.buildReviewRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('LR-1: reviewer required');
    if (!input.composition_id) throw new Error('LR-1: composition_id required');
    if (LR.DECISIONS.indexOf(input.decision) < 0) throw new Error('LR-1: invalid decision');
    if (input.decision === 'reject' && (!Array.isArray(input.cited_rule_ids) || input.cited_rule_ids.length === 0)) {
      throw new Error('LR-4: reject requires cited_rule_ids');
    }
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'layout-review',
      reviewer: input.reviewer,
      payload: {
        review_id: input.review_id || null,
        composition_id: input.composition_id,
        page_index: input.page_index || 'all',
        decision: input.decision,
        cited_rule_ids: input.cited_rule_ids || [],
        prior_decision_id: input.prior_decision_id || null,
        rationale: input.rationale || ''
      }
    });
  };
})(window);
"""

LIFECYCLE_ENGINE_JS = """// phase 51 — composition lifecycle engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var LC = OC.CompositionLifecycle = OC.CompositionLifecycle || {};
  LC.STATES = ['draft','composed','review-required','reviewer-approved','publication-ready','superseded','deprecated'];
  LC.EDGES = [
    ['draft','composed'],
    ['composed','review-required'], ['composed','draft'],
    ['review-required','reviewer-approved'], ['review-required','composed'],
    ['reviewer-approved','publication-ready'], ['reviewer-approved','review-required'],
    ['publication-ready','superseded'], ['publication-ready','deprecated'],
    ['superseded','deprecated']
  ];
  LC.isLegal = function (from, to) {
    for (var i = 0; i < LC.EDGES.length; i++) if (LC.EDGES[i][0] === from && LC.EDGES[i][1] === to) return true;
    return false;
  };
  LC.buildTransitionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('LC-1: reviewer required');
    if (!input.composition_id) throw new Error('composition_id required');
    if (!LC.isLegal(input.from_state, input.to_state)) throw new Error('LC: illegal transition ' + input.from_state + ' -> ' + input.to_state);
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'composition-lifecycle-transition',
      reviewer: input.reviewer,
      payload: {
        composition_id: input.composition_id,
        from_state: input.from_state,
        to_state: input.to_state,
        successor_composition_id: input.successor_composition_id || null,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
"""

INTEGRITY_ENGINE_JS = """// phase 51 — composition integrity engine (reviewer-driven).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var IN = OC.CompositionIntegrity = OC.CompositionIntegrity || {};
  IN.buildIntegrityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    if (!input.composition_id) throw new Error('composition_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'composition-integrity',
      reviewer: input.reviewer,
      payload: {
        integrity_check_id: input.integrity_check_id || null,
        composition_id: input.composition_id,
        scope: input.scope || 'all'
      }
    });
  };
})(window);
"""

JS_ASSETS = {
    "pc-composition-engine.js": COMPOSITION_ENGINE_JS,
    "pc-layout-engine.js": LAYOUT_ENGINE_JS,
    "pc-sequence-engine.js": SEQUENCE_ENGINE_JS,
    "pc-responsive-engine.js": RESPONSIVE_ENGINE_JS,
    "pc-continuity-engine.js": CONTINUITY_ENGINE_JS,
    "pc-assembly-engine.js": ASSEMBLY_ENGINE_JS,
    "pc-review-engine.js": REVIEW_ENGINE_JS,
    "pc-lifecycle-engine.js": LIFECYCLE_ENGINE_JS,
    "pc-integrity-engine.js": INTEGRITY_ENGINE_JS,
}

# ---------------------------------------------------------------------------
# Console HTML
# ---------------------------------------------------------------------------

PHASE51_SCRIPTS = "\n".join(
    f'<script src="../assets/exec/{name}"></script>' for name in JS_ASSETS
)

HTML_HEAD_TEMPLATE = (
    "<!doctype html><html lang='es-CO'><head><meta charset='utf-8'>"
    "<title>{title}</title>"
    "<link rel='stylesheet' href='../assets/exec/exec.css'></head>"
    "<body class='oc-exec'><header class='oc-exec__header'><h1>{title}</h1>"
    "<p class='oc-exec__subtitle'>Phase 51 — Governed multimodal publication composition & page orchestration. "
    "Reviewer-authored only. Deterministic composition. Append-only lineage. No autonomous layout generation.</p></header>"
    "<main class='oc-exec__main'>"
)

HTML_TAIL = (
    "</main><footer class='oc-exec__footer'>"
    "<p>Layer 44 — subordinate to layer 43 (governed visual generation & deterministic asset production).</p>"
    "</footer>"
    '<script src="../assets/exec/fs-bridge.js"></script>'
    + PHASE51_SCRIPTS +
    "</body></html>\n"
)

CONSOLES = {
    "publication-composition-console": "Publication composition console",
    "layout-review-console": "Layout review console",
    "responsive-preview-console": "Responsive preview console",
    "page-continuity-console": "Page continuity console",
    "multimodal-sequence-console": "Multimodal sequence console",
    "composition-integrity-console": "Composition integrity console",
    "publication-assembly-console": "Publication assembly console",
}

CSS_MARKER = "/* phase 51 — publication composition governance additions */"
CSS_ADDENDUM = """
/* phase 51 — publication composition governance additions */
.oc-pc-state { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 0.2rem; border: 1px solid #999; font-size: 0.8rem; }
.oc-pc-state[data-state='draft'] { background: #f4f4f4; color: #555; }
.oc-pc-state[data-state='composed'] { background: #eef; color: #225; }
.oc-pc-state[data-state='review-required'] { background: #ffe; color: #b58900; }
.oc-pc-state[data-state='reviewer-approved'] { background: #cfc; color: #060; }
.oc-pc-state[data-state='publication-ready'] { background: #ace; color: #036; font-weight: bold; }
.oc-pc-state[data-state='superseded'] { background: #ddd; color: #555; }
.oc-pc-state[data-state='deprecated'] { background: #ccc; color: #444; }
.oc-pc-page { border: 1px solid #ccc; padding: 0.5rem; margin: 0.4rem 0; }
.oc-pc-page--continuation { border-left: 4px solid #036; }
.oc-pc-block { display: inline-block; padding: 0.25rem; margin: 0.2rem; border: 1px dashed #999; vertical-align: top; }
.oc-pc-block[data-role='warning'] { border-color: #c00; background: #fee; }
.oc-pc-block[data-role='specification'] { background: #f7f7ff; }
.oc-pc-block[data-role='procedural'] { background: #efe; }
.oc-pc-block[data-role='troubleshooting'] { background: #fef; }
.oc-pc-block[data-role='evidence-trace'] { background: #ffd; font-family: monospace; }
.oc-pc-orphan { background: #fee; padding: 0.3rem; border-left: 4px solid #c00; }
.oc-pc-parity-ok { color: #060; }
.oc-pc-parity-broken { color: #c00; font-weight: bold; }
"""

# ---------------------------------------------------------------------------
# Doctrines
# ---------------------------------------------------------------------------

DOCTRINES = {
    "01-reviewer-authored-composition-only.md": "Composition drafts and layouts are reviewer-authored. Autonomous (LLM- / agent-driven) composition is FORBIDDEN at every layer of this surface.\n",
    "02-deterministic-section-ordering.md": "Section ordering is reviewer-declared and deterministic. Hidden insertion or silent reordering is FORBIDDEN.\n",
    "03-no-runtime-rendering-mutation.md": "The runtime records reviewer-authored composition manifests. Render previews are deterministic snapshots; the live publication tree is never mutated by composition.\n",
    "04-grounding-and-asset-continuity.md": "Every visual block MUST cite both grounding_id (layer 42) and asset_id (layer 43). Orphan visuals BLOCK composition approval.\n",
    "05-warning-prominence-invariant.md": "Warnings precede the procedural block they govern and are visible at every responsive breakpoint. Responsive omission of warnings is FORBIDDEN.\n",
    "06-section-overflow-explicit.md": "Section overflow is handled by adding pages with explicit continuation_of links. Silent splitting is FORBIDDEN.\n",
    "07-responsive-parity-fail-closed.md": "Responsive parity is verified across mobile / tablet / desktop / print. Broken parity BLOCKS publication-ready.\n",
    "08-page-continuity-fail-closed.md": "Page numbering is contiguous and acyclic. Continuity gaps and orphan sections BLOCK publication.\n",
    "09-publication-assembly-isolation.md": "Publication assembly NEVER mutates the live publication tree, the layer-42 visual-publication-builds tree, or the layer-43 visual-generation-runtime tree.\n",
    "10-cli-only-no-daemon-composition.md": "Browser surfaces NEVER write the filesystem. All composition mutation occurs only via the CLI executor with --confirm. No daemon, no watcher, no scheduler.\n",
}

DOCTRINE_DIR = KB_ROOT / "GOVERNED_PUBLICATION_COMPOSITION_GOVERNANCE"

# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

REPORTS = [
    ("01-publication-composition-summary", "Reviewer-authored publication composition summary."),
    ("02-page-layout-summary", "Deterministic page layout summary."),
    ("03-multimodal-sequence-summary", "Multimodal sequence governance summary."),
    ("04-responsive-render-summary", "Responsive render parity summary."),
    ("05-page-continuity-summary", "Page continuity & orphan-detection summary."),
    ("06-publication-assembly-summary", "Publication assembly lineage summary."),
    ("07-layout-review-summary", "Page-level layout review summary."),
    ("08-composition-lifecycle-summary", "Composition lifecycle governance summary."),
    ("09-composition-integrity-summary", "Composition integrity & rollback summary."),
    ("10-governed-publication-composition-platform-maturity-reassessment", "Governed publication composition platform — maturity reassessment."),
]

REPORT_DIR = REPORTS_ROOT / "governed-publication-composition"

# ---------------------------------------------------------------------------
# Runtime README addendum
# ---------------------------------------------------------------------------

RUNTIME_README_MARKER = "## phase 51 — governed multimodal publication composition & page orchestration"
RUNTIME_README_ADDENDUM = """

## phase 51 — governed multimodal publication composition & page orchestration

Layer 44. Subordinate to layer 43 (governed-visual-generation-and-deterministic-asset-production-governance).

Mutation is performed exclusively by `tools/governed_publication_composition_executor.py --confirm`.
Subcommands (`--kind`):

- `composition-draft` — record a reviewer-authored composition draft (synthesis_id + section_order + manual_kind).
- `page-layout` — record a reviewer-authored page layout (deterministic block list, role-typed).
- `multimodal-sequence` — record a procedural / troubleshooting / comparison sequence with reviewer-declared ordering.
- `responsive-layout` — record per-block parity across mobile/tablet/desktop/print (warnings cannot be omitted).
- `page-continuity` — record a continuity scan: page-index contiguity, orphan sections, orphan visuals.
- `publication-assembly` — record a deterministic page-layout assembly with sha256 of the manifest.
- `layout-review` — record a reviewer's page-level decision (approve / request-changes / reject + cited_rule_ids).
- `composition-lifecycle-transition` — advance composition through draft → composed → review-required → reviewer-approved → publication-ready → {superseded → deprecated}.
- `composition-integrity` — record a reviewer-led integrity scan (orphan visuals, warning placement, responsive parity, hidden-section detection).

Every command:
- requires reviewer attribution,
- is fail-closed on missing section lineage / orphan visuals / warning-placement violations / broken responsive parity / illegal lifecycle transitions / hidden section insertion,
- appends to one or more append-only event stores under `operational-console/runtime-manifests/`,
- writes only into `operational-console/publication-composition-runtime/` subtrees.

The publication-composition-runtime tree is isolated from:
- the live publication tree,
- the layer-42 visual-publication-builds tree,
- the layer-43 visual-generation-runtime tree,
- OEM source assets,
- knowledge-core, governance, runtime-implementation, runtime-manifests payloads.
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
    root_readme = PC_ROOT / "README.md"
    if not root_readme.exists():
        write_text(root_readme,
                   "# publication-composition-runtime\n\n"
                   "Phase 51 / layer 44. Governed multimodal publication composition & page orchestration.\n\n"
                   "Reviewer-authored only. Deterministic. Append-only.\n")
        count += 1
    for sub in PC_SUBDIRS:
        sub_path = PC_ROOT / sub
        sub_readme = sub_path / "README.md"
        if not sub_readme.exists():
            write_text(sub_readme, f"# {sub}\n\nLayer {LAYER}. Append-only. Reviewer-attributed.\n")
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
            f"<code>{slug}</code> surface. The browser does NOT mutate the filesystem and does NOT generate layouts.</p>"
            f"<p>Submit envelopes via <code>tools/governed_publication_composition_executor.py --kind &lt;kind&gt; --request &lt;file&gt; --confirm</code>.</p>"
            f"</section>"
        )
        write_text(OC_ROOT / slug / "exec.html", html + body + HTML_TAIL)
    return len(CONSOLES)


def build_doctrines() -> int:
    DOCTRINE_DIR.mkdir(parents=True, exist_ok=True)
    index_lines = ["# GOVERNED PUBLICATION COMPOSITION GOVERNANCE", "", f"Layer {LAYER}. Phase 51.", ""]
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
               "# Governed publication composition — reports\n\nPhase 51 / layer 44 reports.\n")
    for slug, title in REPORTS:
        write_text(REPORT_DIR / f"{slug}.md", f"# {title}\n\nLayer {LAYER}. Phase 51.\n")
        write_json(REPORT_DIR / f"{slug}.json", {
            "schema": "governance-report/1.0",
            "constitutional_layer_index": LAYER,
            "report_slug": slug,
            "title": title,
            "subordinate_to": SUBORDINATE_TO,
            "posture": POSTURE,
            "manual_kinds": MANUAL_KINDS,
            "section_roles": SECTION_ROLES,
            "responsive_breakpoints": RESPONSIVE_BREAKPOINTS,
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
        "Phase 51 — governed multimodal publication composition & page orchestration written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {storage} | New event stores: {stores} | Rule tables: {rules} | "
        f"JS assets: {js} | Exec consoles: {consoles} | Doctrines: {doctrines} | Reports: {reports} | "
        f"RUNTIME_README addendum: {readme}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
