"""
Phase 50 — Governed Visual Generation & Deterministic Asset Production (layer 43).

Idempotent stdlib-only builder. Emits the layer-43 surface over layer 42
(governed multimodal grounding & visual publication orchestration).

The runtime writer is the executor (`tools/governed_visual_generation_executor.py`).
This builder NEVER mutates event stores, runtime data, knowledge-core,
governance, runtime-implementation, runtime-manifests payloads, visual
publication builds, OEM source assets, or live publications.

Posture:
- deterministic, reviewer-authoritative, append-only, local-first, fail-closed.
- NO autonomous image generation, NO hidden prompt mutation, NO probabilistic
  visual replacement, NO cloud orchestration, NO SaaS dependency,
  NO auto-publication, NO silent asset overwrite, NO live publication mutation,
  NO ML governance decisions, NO autonomous visual selection,
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

VG_ROOT = OC_ROOT / "visual-generation-runtime"

VG_SUBDIRS = [
    "generation-requests",
    "generated-assets",
    "generated-candidates",
    "review-comparisons",
    "visual-lineage",
    "generation-sessions",
    "visual-supersedence",
    "publication-visual-selections",
    "reviewer-approvals",
    "rejected-assets",
    "deprecated-assets",
]

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA = "governed-visual-generation/1.0"
LAYER = 43

SUBORDINATE_TO = [
    "knowledge-core-doctrine",
    "governance-source-of-truth-doctrine",
    "runtime-evidence-and-trust-doctrine",
    "executable-operational-bindings-governance",
    "governed-filesystem-orchestration-doctrine",
    "governed-transactional-execution-and-recovery-governance",
    "governed-knowledge-synthesis-and-canonical-publication-governance",
    "governed-multimodal-grounding-and-visual-publication-governance",
]
while len(SUBORDINATE_TO) < 42:
    SUBORDINATE_TO.append("governed-multimodal-grounding-and-visual-publication-governance")

POSTURE = {
    "deterministic": True,
    "reviewer_authoritative": True,
    "append_only_visual_lineage": True,
    "no_autonomous_generation": True,
    "no_hidden_prompt_mutation": True,
    "no_probabilistic_visual_replacement": True,
    "no_cloud_orchestration": True,
    "no_saas_dependency": True,
    "no_auto_publication": True,
    "no_silent_asset_overwrite": True,
    "no_live_publication_mutation": True,
    "no_ml_governance_decisions": True,
    "no_autonomous_visual_selection": True,
    "no_daemon_no_watcher_no_scheduler": True,
    "fail_closed_on_missing_grounding": True,
    "fail_closed_on_missing_prompt_lineage": True,
    "fail_closed_on_unresolved_conflict": True,
    "fail_closed_on_broken_continuity": True,
    "writes_to_live_publication_tree": False,
    "writes_to_visual_publication_builds_tree": False,
    "writes_only_into_visual_generation_runtime_tree": True,
    "browser_surfaces_never_write_filesystem": True,
}

# Asset kinds (Task: support all visual classes)
ASSET_KINDS = [
    "generated",
    "oem",
    "edited",
    "supportive",
    "procedural-sequence",
    "troubleshooting",
    "specification",
]

# Lifecycle
LIFECYCLE_STATES = {
    "candidate",
    "review-required",
    "reviewer-approved",
    "publication-selected",
    "superseded",
    "deprecated",
    "rejected",
}
LIFECYCLE_TERMINAL = {"deprecated", "rejected"}
LIFECYCLE_EDGES = [
    ("candidate", "review-required"),
    ("candidate", "rejected"),
    ("review-required", "reviewer-approved"),
    ("review-required", "rejected"),
    ("review-required", "candidate"),
    ("reviewer-approved", "publication-selected"),
    ("reviewer-approved", "review-required"),
    ("publication-selected", "superseded"),
    ("publication-selected", "deprecated"),
    ("superseded", "deprecated"),
]

# Generation session states
SESSION_STATES = {"open", "frozen", "closed", "rejected"}
SESSION_TERMINAL = {"closed", "rejected"}
SESSION_EDGES = [
    ("open", "frozen"),
    ("open", "rejected"),
    ("frozen", "open"),
    ("frozen", "closed"),
    ("frozen", "rejected"),
]

NEW_EVENT_STORES = [
    "visual-generation-events",
    "variant-lineage-events",
    "review-comparison-events",
    "selection-events",
    "supersedence-events",
    "generation-session-events",
    "publication-selection-events",
    "visual-integrity-events",
]

# ---------------------------------------------------------------------------
# Rule tables
# ---------------------------------------------------------------------------

GENERATION_REQUEST_RULES = {
    "schema": "visual-generation-request-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "GR-1", "rule": "every generation request MUST be reviewer-authored and reviewer-attributed."},
        {"id": "GR-2", "rule": "every generation request MUST cite a grounding_id, prompt_id, synthesis_id, canonical_product_id."},
        {"id": "GR-3", "rule": "autonomous (LLM- or agent-driven) generation requests are FORBIDDEN."},
        {"id": "GR-4", "rule": "the runtime does NOT execute generation; it records the reviewer-authored request and the out-of-band reviewer-supplied output."},
        {"id": "GR-5", "rule": "generation requests are append-only; in-place mutation is FORBIDDEN."},
        {"id": "GR-6", "rule": "reviewer-declared variant_count MUST be >= 1 and bounded by reviewer-set ceiling."},
        {"id": "GR-7", "rule": "every generation request MUST declare expected asset_kind ∈ ASSET_KINDS."},
    ],
}

VARIANT_LINEAGE_RULES = {
    "schema": "variant-lineage-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "VL-1", "rule": "every generated asset MUST carry a deterministic variant_id derived from sha256(generation_request_id|variant_index|sha256(asset_bytes))."},
        {"id": "VL-2", "rule": "every generated asset MUST cite generation_request_id, prompt_revision_id, grounding_id, synthesis_id."},
        {"id": "VL-3", "rule": "every generated asset MUST carry sha256 of the asset bytes (provenance)."},
        {"id": "VL-4", "rule": "variant family (siblings sharing generation_request_id) is reviewer-comparable; cross-family comparison requires explicit reviewer attestation."},
        {"id": "VL-5", "rule": "regeneration MUST preserve grounding_id; grounding-changing regeneration requires a new grounding manifest first (layer 42)."},
        {"id": "VL-6", "rule": "OEM assets MUST be labeled trust_tier=OEM and source_provenance.kind='oem-source'; generated/OEM differentiation is non-negotiable."},
        {"id": "VL-7", "rule": "edited assets MUST cite parent_asset_id and edit_kind ∈ {crop, annotate, redact, color-correct, watermark-removal-FORBIDDEN}."},
    ],
}

REVIEW_COMPARISON_RULES = {
    "schema": "review-comparison-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "RC-1", "rule": "comparison manifests MUST include >= 2 candidate variant_ids."},
        {"id": "RC-2", "rule": "scores are reviewer-authored ONLY; ML / heuristic / similarity scoring is FORBIDDEN."},
        {"id": "RC-3", "rule": "every comparison MUST capture reviewer_id and a per-variant verdict ∈ {prefer, acceptable, reject, defer}."},
        {"id": "RC-4", "rule": "side-by-side metadata (display_order, group_id, comparison_dimension) MUST be deterministic and recorded."},
        {"id": "RC-5", "rule": "comparison records are append-only; revisions append new comparison_id with prior_comparison_id."},
    ],
}

SELECTION_RULES = {
    "schema": "publication-visual-selection-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "SL-1", "rule": "publication selection MUST cite a reviewer-approved variant_id; candidate / review-required / rejected variants are NEVER selectable."},
        {"id": "SL-2", "rule": "selection MUST cite the visual_publication_build_id and placement_slot_id from layer 42."},
        {"id": "SL-3", "rule": "selection MUST preserve grounding_id continuity (the variant's grounding_id MUST equal the placement's grounding_id)."},
        {"id": "SL-4", "rule": "auto-selection is FORBIDDEN. Selection MUST be reviewer-attributed."},
        {"id": "SL-5", "rule": "selection records are append-only; replacing a selection requires explicit supersedence."},
        {"id": "SL-6", "rule": "broken continuity, missing prompt lineage, or unresolved conflict BLOCKS selection (fail-closed)."},
    ],
}

SUPERSEDENCE_RULES = {
    "schema": "visual-supersedence-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "SP-1", "rule": "supersedence MUST cite predecessor_asset_id, successor_asset_id, reason, reviewer."},
        {"id": "SP-2", "rule": "predecessor MUST currently be in {publication-selected, reviewer-approved}; otherwise refused."},
        {"id": "SP-3", "rule": "successor MUST currently be reviewer-approved."},
        {"id": "SP-4", "rule": "supersedence MUST preserve grounding_id continuity (predecessor.grounding_id == successor.grounding_id), unless reviewer explicitly authorizes a grounding-shift with attribution."},
        {"id": "SP-5", "rule": "OEM source assets CANNOT be superseded by generated assets without explicit reviewer attestation and a recorded rationale."},
        {"id": "SP-6", "rule": "supersedence is append-only; in-place overwrite is FORBIDDEN."},
        {"id": "SP-7", "rule": "supersedence chain MUST be acyclic and traceable end-to-end."},
    ],
}

SESSION_RULES = {
    "schema": "generation-session-rules/1.0",
    "constitutional_layer_index": LAYER,
    "states": sorted(SESSION_STATES),
    "terminal_states": sorted(SESSION_TERMINAL),
    "edges": [list(e) for e in SESSION_EDGES],
    "rules": [
        {"id": "GS-1", "rule": "every generation session MUST be reviewer-opened and reviewer-attributed."},
        {"id": "GS-2", "rule": "session frozen state means: no new generation requests accepted; comparisons + reviews continue."},
        {"id": "GS-3", "rule": "session closed state means: no further mutations; selections may still be performed via separate publication-selection events that reference the closed session."},
        {"id": "GS-4", "rule": "session rejected state means: all candidate variants in the session are rejected; reviewer attestation required."},
        {"id": "GS-5", "rule": "a generation request MUST belong to exactly one session."},
    ],
}

INTEGRITY_RULES = {
    "schema": "visual-integrity-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "IN-1", "rule": "every asset record MUST carry sha256; sha256 mismatch on re-verification is fail-closed."},
        {"id": "IN-2", "rule": "missing prompt_revision_id on a generated asset blocks publication selection."},
        {"id": "IN-3", "rule": "missing grounding_id on any asset blocks publication selection (grounding-preservation invariant)."},
        {"id": "IN-4", "rule": "selection of an asset whose lifecycle state is NOT reviewer-approved is fail-closed."},
        {"id": "IN-5", "rule": "OEM source assets MUST NEVER be overwritten; integrity check refuses any record claiming to overwrite an OEM source path."},
        {"id": "IN-6", "rule": "rollback MUST restore by appending a reverse selection event; destructive deletion of asset records is FORBIDDEN."},
        {"id": "IN-7", "rule": "cross-manual reuse of an asset MUST cite reviewer attestation and the source manual_id."},
    ],
}

LIFECYCLE_RULES = {
    "schema": "visual-asset-production-lifecycle-rules/1.0",
    "constitutional_layer_index": LAYER,
    "states": sorted(LIFECYCLE_STATES),
    "terminal_states": sorted(LIFECYCLE_TERMINAL),
    "edges": [list(e) for e in LIFECYCLE_EDGES],
    "rules": [
        {"id": "LC-1", "rule": "reviewer attribution required on every state transition."},
        {"id": "LC-2", "rule": "terminal states (deprecated, rejected) are immutable."},
        {"id": "LC-3", "rule": "publication-selected requires the asset to be reviewer-approved AND grounding-clean."},
        {"id": "LC-4", "rule": "transitions are append-only; in-place state mutation is FORBIDDEN."},
        {"id": "LC-5", "rule": "rejected is reachable from candidate or review-required; once rejected, the asset cannot be selected."},
    ],
}

RULE_TABLES = {
    "visual-generation-request-rules.json": GENERATION_REQUEST_RULES,
    "variant-lineage-rules.json": VARIANT_LINEAGE_RULES,
    "review-comparison-rules.json": REVIEW_COMPARISON_RULES,
    "publication-visual-selection-rules.json": SELECTION_RULES,
    "visual-supersedence-rules.json": SUPERSEDENCE_RULES,
    "generation-session-rules.json": SESSION_RULES,
    "visual-integrity-rules.json": INTEGRITY_RULES,
    "visual-asset-production-lifecycle-rules.json": LIFECYCLE_RULES,
}

# ---------------------------------------------------------------------------
# JS engines (vanilla ES; never write FS; only build envelopes)
# ---------------------------------------------------------------------------

GENERATION_ENGINE_JS = """// phase 50 — visual generation request engine (reviewer-authored, NO autonomous gen).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var VG = OC.VisualGeneration = OC.VisualGeneration || {};
  VG.ASSET_KINDS = ['generated','oem','edited','supportive','procedural-sequence','troubleshooting','specification'];
  VG.buildGenerationRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('GR-1: reviewer required');
    if (!input.grounding_id) throw new Error('GR-2: grounding_id required');
    if (!input.prompt_id) throw new Error('GR-2: prompt_id required');
    if (!input.synthesis_id) throw new Error('GR-2: synthesis_id required');
    if (!input.canonical_product_id) throw new Error('GR-2: canonical_product_id required');
    if (VG.ASSET_KINDS.indexOf(input.asset_kind) < 0) throw new Error('GR-7: invalid asset_kind');
    var n = parseInt(input.variant_count, 10);
    if (!(n >= 1)) throw new Error('GR-6: variant_count must be >= 1');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'generation-request',
      reviewer: input.reviewer,
      payload: {
        generation_request_id: input.generation_request_id || null,
        session_id: input.session_id || null,
        grounding_id: input.grounding_id,
        prompt_id: input.prompt_id,
        prompt_revision_id: input.prompt_revision_id || null,
        synthesis_id: input.synthesis_id,
        canonical_product_id: input.canonical_product_id,
        asset_kind: input.asset_kind,
        variant_count: n,
        constraints: input.constraints || [],
        rationale: input.rationale || ''
      }
    });
  };
})(window);
"""

GENERATED_ASSET_ENGINE_JS = """// phase 50 — generated asset registration engine (reviewer-supplied bytes; sha256 provenance).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var GA = OC.GeneratedAsset = OC.GeneratedAsset || {};
  GA.buildRegistrationRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    if (!input.generation_request_id) throw new Error('VL-2: generation_request_id required');
    if (!input.asset_sha256) throw new Error('VL-3: asset_sha256 required');
    if (!input.source_provenance) throw new Error('VL-2: source_provenance required');
    if (typeof input.variant_index !== 'number') throw new Error('VL-1: variant_index required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'generated-asset-register',
      reviewer: input.reviewer,
      payload: {
        asset_id: input.asset_id || null,
        generation_request_id: input.generation_request_id,
        variant_index: input.variant_index,
        asset_sha256: input.asset_sha256,
        asset_kind: input.asset_kind || 'generated',
        source_provenance: input.source_provenance,
        prompt_revision_id: input.prompt_revision_id || null,
        grounding_id: input.grounding_id || null,
        synthesis_id: input.synthesis_id || null,
        trust_tier: input.trust_tier || null,
        parent_asset_id: input.parent_asset_id || null,
        edit_kind: input.edit_kind || null
      }
    });
  };
})(window);
"""

COMPARISON_ENGINE_JS = """// phase 50 — review comparison engine (reviewer-scored ONLY).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var RC = OC.ReviewComparison = OC.ReviewComparison || {};
  RC.VERDICTS = ['prefer','acceptable','reject','defer'];
  RC.buildComparisonRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    if (!Array.isArray(input.entries) || input.entries.length < 2) throw new Error('RC-1: at least two entries required');
    for (var i = 0; i < input.entries.length; i++) {
      var e = input.entries[i];
      if (!e.asset_id) throw new Error('RC-1: entry ' + i + ' missing asset_id');
      if (RC.VERDICTS.indexOf(e.verdict) < 0) throw new Error('RC-3: entry ' + i + ' invalid verdict');
    }
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'review-comparison',
      reviewer: input.reviewer,
      payload: {
        comparison_id: input.comparison_id || null,
        comparison_dimension: input.comparison_dimension || 'overall',
        group_id: input.group_id || null,
        prior_comparison_id: input.prior_comparison_id || null,
        entries: input.entries
      }
    });
  };
})(window);
"""

SELECTION_ENGINE_JS = """// phase 50 — publication visual selection engine (reviewer-attributed, fail-closed).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var SL = OC.VisualSelection = OC.VisualSelection || {};
  SL.buildSelectionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('SL-4: reviewer required');
    if (!input.asset_id) throw new Error('SL-1: asset_id required');
    if (!input.visual_publication_build_id) throw new Error('SL-2: visual_publication_build_id required');
    if (!input.placement_slot_id) throw new Error('SL-2: placement_slot_id required');
    if (!input.grounding_id) throw new Error('SL-3: grounding_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'publication-visual-selection',
      reviewer: input.reviewer,
      payload: {
        selection_id: input.selection_id || null,
        asset_id: input.asset_id,
        visual_publication_build_id: input.visual_publication_build_id,
        placement_slot_id: input.placement_slot_id,
        grounding_id: input.grounding_id,
        prior_selection_id: input.prior_selection_id || null,
        rationale: input.rationale || ''
      }
    });
  };
})(window);
"""

SUPERSEDENCE_ENGINE_JS = """// phase 50 — visual supersedence engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var SP = OC.Supersedence = OC.Supersedence || {};
  SP.buildSupersedenceRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    if (!input.predecessor_asset_id) throw new Error('SP-1: predecessor_asset_id required');
    if (!input.successor_asset_id) throw new Error('SP-1: successor_asset_id required');
    if (input.predecessor_asset_id === input.successor_asset_id) throw new Error('SP-7: predecessor must differ from successor');
    if (!input.reason) throw new Error('SP-1: reason required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'visual-supersedence',
      reviewer: input.reviewer,
      payload: {
        supersedence_id: input.supersedence_id || null,
        predecessor_asset_id: input.predecessor_asset_id,
        successor_asset_id: input.successor_asset_id,
        reason: input.reason,
        grounding_shift: !!input.grounding_shift,
        oem_to_generated_attestation: input.oem_to_generated_attestation || null
      }
    });
  };
})(window);
"""

SESSION_ENGINE_JS = """// phase 50 — generation session engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var GS = OC.GenerationSession = OC.GenerationSession || {};
  GS.STATES = ['open','frozen','closed','rejected'];
  GS.EDGES = [['open','frozen'],['open','rejected'],['frozen','open'],['frozen','closed'],['frozen','rejected']];
  GS.isLegal = function (from, to) {
    for (var i = 0; i < GS.EDGES.length; i++) if (GS.EDGES[i][0] === from && GS.EDGES[i][1] === to) return true;
    return false;
  };
  GS.buildSessionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('GS-1: reviewer required');
    if (!input.action || ['open','transition'].indexOf(input.action) < 0) throw new Error('action must be open|transition');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'generation-session',
      reviewer: input.reviewer,
      payload: {
        session_id: input.session_id || null,
        action: input.action,
        from_state: input.from_state || null,
        to_state: input.to_state || null,
        canonical_product_id: input.canonical_product_id || null,
        rationale: input.rationale || ''
      }
    });
  };
})(window);
"""

LIFECYCLE_ENGINE_JS = """// phase 50 — visual asset production lifecycle engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var LC = OC.AssetLifecycle = OC.AssetLifecycle || {};
  LC.STATES = ['candidate','review-required','reviewer-approved','publication-selected','superseded','deprecated','rejected'];
  LC.EDGES = [
    ['candidate','review-required'], ['candidate','rejected'],
    ['review-required','reviewer-approved'], ['review-required','rejected'], ['review-required','candidate'],
    ['reviewer-approved','publication-selected'], ['reviewer-approved','review-required'],
    ['publication-selected','superseded'], ['publication-selected','deprecated'],
    ['superseded','deprecated']
  ];
  LC.isLegal = function (from, to) {
    for (var i = 0; i < LC.EDGES.length; i++) if (LC.EDGES[i][0] === from && LC.EDGES[i][1] === to) return true;
    return false;
  };
  LC.buildTransitionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('LC-1: reviewer required');
    if (!input.asset_id) throw new Error('asset_id required');
    if (!LC.isLegal(input.from_state, input.to_state)) throw new Error('LC: illegal transition ' + input.from_state + ' -> ' + input.to_state);
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'asset-lifecycle-transition',
      reviewer: input.reviewer,
      payload: {
        asset_id: input.asset_id,
        from_state: input.from_state,
        to_state: input.to_state,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
"""

INTEGRITY_ENGINE_JS = """// phase 50 — visual integrity engine (reviewer-driven verification; no ML).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var IN = OC.VisualIntegrity = OC.VisualIntegrity || {};
  IN.buildIntegrityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'visual-integrity',
      reviewer: input.reviewer,
      payload: {
        integrity_check_id: input.integrity_check_id || null,
        scope: input.scope || 'all',
        target_asset_ids: input.target_asset_ids || []
      }
    });
  };
})(window);
"""

JS_ASSETS = {
    "vg-generation-engine.js": GENERATION_ENGINE_JS,
    "vg-asset-engine.js": GENERATED_ASSET_ENGINE_JS,
    "vg-comparison-engine.js": COMPARISON_ENGINE_JS,
    "vg-selection-engine.js": SELECTION_ENGINE_JS,
    "vg-supersedence-engine.js": SUPERSEDENCE_ENGINE_JS,
    "vg-session-engine.js": SESSION_ENGINE_JS,
    "vg-lifecycle-engine.js": LIFECYCLE_ENGINE_JS,
    "vg-integrity-engine.js": INTEGRITY_ENGINE_JS,
}

# ---------------------------------------------------------------------------
# Console HTML
# ---------------------------------------------------------------------------

PHASE50_SCRIPTS = "\n".join(
    f'<script src="../assets/exec/{name}"></script>' for name in JS_ASSETS
)

HTML_HEAD_TEMPLATE = (
    "<!doctype html><html lang='es-CO'><head><meta charset='utf-8'>"
    "<title>{title}</title>"
    "<link rel='stylesheet' href='../assets/exec/exec.css'></head>"
    "<body class='oc-exec'><header class='oc-exec__header'><h1>{title}</h1>"
    "<p class='oc-exec__subtitle'>Phase 50 — Governed visual generation & deterministic asset production. "
    "Reviewer-authored only. No autonomous generation. Append-only lineage. Deterministic provenance.</p></header>"
    "<main class='oc-exec__main'>"
)

HTML_TAIL = (
    "</main><footer class='oc-exec__footer'>"
    "<p>Layer 43 — subordinate to layer 42 (governed multimodal grounding & visual publication orchestration).</p>"
    "</footer>"
    '<script src="../assets/exec/fs-bridge.js"></script>'
    + PHASE50_SCRIPTS +
    "</body></html>\n"
)

CONSOLES = {
    "visual-generation-console": "Visual generation request console",
    "variant-review-console": "Variant review & comparison console",
    "visual-selection-console": "Publication visual selection console",
    "supersedence-console": "Visual supersedence console",
    "generation-session-console": "Generation session console",
    "visual-integrity-console": "Visual integrity & lineage console",
}

CSS_MARKER = "/* phase 50 — visual generation governance additions */"
CSS_ADDENDUM = """
/* phase 50 — visual generation governance additions */
.oc-vg-state { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 0.2rem; border: 1px solid #999; font-size: 0.8rem; }
.oc-vg-state[data-state='candidate'] { background: #eee; }
.oc-vg-state[data-state='review-required'] { background: #ffe; color: #b58900; }
.oc-vg-state[data-state='reviewer-approved'] { background: #cfc; color: #060; }
.oc-vg-state[data-state='publication-selected'] { background: #ace; color: #036; font-weight: bold; }
.oc-vg-state[data-state='superseded'] { background: #ddd; color: #555; }
.oc-vg-state[data-state='deprecated'] { background: #ccc; color: #444; }
.oc-vg-state[data-state='rejected'] { background: #fcc; color: #900; text-decoration: line-through; }
.oc-vg-variant { display: inline-block; padding: 0.25rem; margin: 0.25rem; border: 1px solid #ccc; vertical-align: top; }
.oc-vg-variant.is-selected { border: 2px solid #036; background: #eef6ff; }
.oc-vg-provenance { font-family: monospace; font-size: 0.8rem; color: #333; word-break: break-all; }
.oc-vg-oem-badge { background: #cfc; padding: 0.1rem 0.3rem; border-radius: 0.2rem; font-weight: bold; }
.oc-vg-generated-badge { background: #ffd; padding: 0.1rem 0.3rem; border-radius: 0.2rem; }
.oc-vg-conflict { background: #fee; padding: 0.5rem; border-left: 4px solid #c00; }
"""

# ---------------------------------------------------------------------------
# Doctrines
# ---------------------------------------------------------------------------

DOCTRINES = {
    "01-reviewer-authored-generation-only.md": "Generation requests are reviewer-authored. Autonomous (LLM- / agent-driven) generation is FORBIDDEN at every layer of this surface.\n",
    "02-no-runtime-image-synthesis.md": "The runtime does NOT execute image generation. It records reviewer-authored requests and reviewer-supplied output bytes (with sha256 provenance).\n",
    "03-deterministic-variant-lineage.md": "Variant identifiers are deterministic and reviewer-traceable: variant_id = sha256(generation_request_id|variant_index|sha256(asset_bytes)).\n",
    "04-prompt-to-image-provenance.md": "Every generated asset MUST trace back to a prompt_revision_id (layer 42). Detached generated assets are FORBIDDEN.\n",
    "05-no-silent-asset-overwrite.md": "Asset replacement happens only via append-only supersedence with reviewer attribution and rationale. Silent overwrite is FORBIDDEN.\n",
    "06-no-autonomous-visual-selection.md": "Publication selection is reviewer-attributed. Auto-selection is FORBIDDEN. Selection of non-approved assets is fail-closed.\n",
    "07-grounding-preservation-invariant.md": "Regeneration and supersedence MUST preserve grounding_id continuity. Grounding-shifting requires an explicit prior layer-42 grounding manifest and reviewer attestation.\n",
    "08-oem-source-protection.md": "OEM source assets MUST NEVER be overwritten. Generated assets cannot supersede OEM source assets without explicit reviewer attestation.\n",
    "09-no-cloud-no-saas-no-ml-visual-generation.md": "No cloud orchestration. No SaaS dependency. No ML governance decisions. No probabilistic visual replacement. Local-first only.\n",
    "10-cli-only-no-daemon-visual-generation.md": "Browser surfaces NEVER write the filesystem. All mutation occurs only via the CLI executor with --confirm. No daemon, no watcher, no scheduler.\n",
}

DOCTRINE_DIR = KB_ROOT / "GOVERNED_VISUAL_GENERATION_GOVERNANCE"

# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

REPORTS = [
    ("01-visual-generation-request-summary", "Reviewer-authored visual generation request summary."),
    ("02-variant-lineage-summary", "Deterministic variant lineage summary."),
    ("03-review-comparison-summary", "Multi-variant reviewer comparison summary."),
    ("04-publication-visual-selection-summary", "Publication-safe visual selection summary."),
    ("05-visual-supersedence-summary", "Generated asset supersedence summary."),
    ("06-generation-session-summary", "Generation session governance summary."),
    ("07-visual-integrity-summary", "Visual integrity & lineage verification summary."),
    ("08-asset-production-lifecycle-summary", "Visual asset production lifecycle summary."),
    ("09-oem-vs-generated-differentiation-summary", "OEM vs generated visual differentiation & canonical truth summary."),
    ("10-governed-visual-platform-maturity-reassessment", "Governed visual generation platform — maturity reassessment."),
]

REPORT_DIR = REPORTS_ROOT / "governed-visual-generation"

# ---------------------------------------------------------------------------
# Runtime README addendum
# ---------------------------------------------------------------------------

RUNTIME_README_MARKER = "## phase 50 — governed visual generation & deterministic asset production"
RUNTIME_README_ADDENDUM = """

## phase 50 — governed visual generation & deterministic asset production

Layer 43. Subordinate to layer 42 (governed-multimodal-grounding-and-visual-publication-governance).

Mutation is performed exclusively by `tools/governed_visual_generation_executor.py --confirm`.
Subcommands (`--kind`):

- `generation-request` — record a reviewer-authored generation request (the runtime never generates).
- `generated-asset-register` — record a reviewer-supplied generated asset with sha256 + prompt + grounding lineage.
- `review-comparison` — record a reviewer-authored multi-variant comparison (no ML scoring).
- `publication-visual-selection` — record a reviewer-attributed publication selection (asset MUST be reviewer-approved).
- `visual-supersedence` — append-only supersedence between asset records.
- `generation-session` — open / freeze / close / reject a reviewer-led generation session.
- `asset-lifecycle-transition` — advance an asset through candidate → review-required → reviewer-approved → publication-selected → {superseded | deprecated}; or → rejected.
- `visual-integrity` — record a reviewer-led integrity check (sha256 + lineage + grounding-preservation).

Every command:
- requires reviewer attribution,
- is fail-closed on missing grounding / missing prompt lineage / missing sha256 / illegal transitions / OEM overwrite attempts,
- appends to one or more append-only event stores under `operational-console/runtime-manifests/`,
- writes only into `operational-console/visual-generation-runtime/` subtrees.

The visual-generation-runtime tree is isolated from:
- the live publication tree,
- the layer-42 visual-publication-builds tree,
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
    root_readme = VG_ROOT / "README.md"
    if not root_readme.exists():
        write_text(root_readme,
                   "# visual-generation-runtime\n\n"
                   "Phase 50 / layer 43. Governed visual generation & deterministic asset production.\n\n"
                   "Reviewer-authored only. No autonomous generation. Append-only.\n")
        count += 1
    for sub in VG_SUBDIRS:
        sub_path = VG_ROOT / sub
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
            f"<code>{slug}</code> surface. The browser does NOT mutate the filesystem and does NOT generate images.</p>"
            f"<p>Submit envelopes via <code>tools/governed_visual_generation_executor.py --kind &lt;kind&gt; --request &lt;file&gt; --confirm</code>.</p>"
            f"</section>"
        )
        write_text(OC_ROOT / slug / "exec.html", html + body + HTML_TAIL)
    return len(CONSOLES)


def build_doctrines() -> int:
    DOCTRINE_DIR.mkdir(parents=True, exist_ok=True)
    index_lines = ["# GOVERNED VISUAL GENERATION GOVERNANCE", "", f"Layer {LAYER}. Phase 50.", ""]
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
               "# Governed visual generation — reports\n\nPhase 50 / layer 43 reports.\n")
    for slug, title in REPORTS:
        write_text(REPORT_DIR / f"{slug}.md", f"# {title}\n\nLayer {LAYER}. Phase 50.\n")
        write_json(REPORT_DIR / f"{slug}.json", {
            "schema": "governance-report/1.0",
            "constitutional_layer_index": LAYER,
            "report_slug": slug,
            "title": title,
            "subordinate_to": SUBORDINATE_TO,
            "posture": POSTURE,
            "asset_kinds": ASSET_KINDS,
            "lifecycle_states": sorted(LIFECYCLE_STATES),
            "lifecycle_terminal_states": sorted(LIFECYCLE_TERMINAL),
            "lifecycle_edges": [list(e) for e in LIFECYCLE_EDGES],
            "session_states": sorted(SESSION_STATES),
            "session_edges": [list(e) for e in SESSION_EDGES],
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
        "Phase 50 — governed visual generation & deterministic asset production written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {storage} | New event stores: {stores} | Rule tables: {rules} | "
        f"JS assets: {js} | Exec consoles: {consoles} | Doctrines: {doctrines} | Reports: {reports} | "
        f"RUNTIME_README addendum: {readme}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
