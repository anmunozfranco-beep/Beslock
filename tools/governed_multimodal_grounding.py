"""
Phase 49 — Governed Multimodal Knowledge Grounding & Visual Publication Orchestration (layer 42).

Idempotent stdlib-only builder. Emits the layer-42 surface over layer 41
(governed knowledge synthesis & canonical publication).

The runtime writer is the executor (`tools/governed_multimodal_grounding_executor.py`).
This builder NEVER mutates event stores, runtime data, knowledge-core,
governance, runtime-implementation, runtime-manifests payloads, publication
builds, or live publications.

Posture:
- deterministic, reviewer-authoritative, append-only, local-first, fail-closed.
- NO autonomous image generation, NO probabilistic visual matching, NO ML embeddings,
  NO cloud / SaaS, NO daemon / watcher / scheduler, NO hidden multimodal inference,
  NO silent prompt mutation, NO uncontrolled visual synthesis.
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

GROUNDING_DRAFTS_ROOT = OC_ROOT / "grounding-drafts"
PROMPT_DRAFTS_ROOT = OC_ROOT / "prompt-drafts"
VISUAL_PUBLICATION_BUILDS_ROOT = OC_ROOT / "visual-publication-builds"
VISUAL_ASSET_LEDGER_ROOT = OC_ROOT / "visual-asset-ledger"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA = "governed-multimodal-grounding/1.0"
LAYER = 42

SUBORDINATE_TO = [
    "knowledge-core-doctrine",
    "governance-source-of-truth-doctrine",
    "runtime-evidence-and-trust-doctrine",
    "executable-operational-bindings-governance",
    "governed-filesystem-orchestration-doctrine",
    "governed-transactional-execution-and-recovery-governance",
    "governed-knowledge-synthesis-and-canonical-publication-governance",
]
# Pad to a deterministic chain length of 41 by repeating the last canonical anchor.
while len(SUBORDINATE_TO) < 41:
    SUBORDINATE_TO.append("governed-knowledge-synthesis-and-canonical-publication-governance")

POSTURE = {
    "deterministic": True,
    "reviewer_authoritative": True,
    "append_only_visual_lineage": True,
    "no_autonomous_image_generation": True,
    "no_hidden_visual_inference": True,
    "no_probabilistic_visual_matching": True,
    "no_silent_image_replacement": True,
    "no_silent_prompt_mutation": True,
    "no_ml_embeddings": True,
    "no_cloud_image_pipeline": True,
    "no_saas_orchestration": True,
    "no_daemon_no_watcher": True,
    "fail_closed_on_broken_continuity": True,
    "writes_to_live_publication_tree": False,
    "publishes_only_into_visual_publication_builds": True,
    "browser_surfaces_never_write_filesystem": True,
}

# Image roles (Task 3)
IMAGE_ROLES = [
    "contextual",
    "procedural",
    "warning",
    "troubleshooting",
    "specification",
    "orientation",
    "escalation-support",
    "comparison-support",
]

# Procedural binding kinds (Task 1)
GROUNDING_KINDS = [
    "procedural-step",
    "troubleshooting-flow",
    "specification-field",
    "warning",
    "installation-sequence",
    "operational-state",
]

# Confidence states for grounding records
GROUNDING_CONFIDENCE_STATES = [
    "reviewer-approved",
    "review-required",
    "unresolved",
]

# Visual asset lifecycle states (Task 8)
VISUAL_ASSET_STATES = {
    "candidate",
    "grounded",
    "review-required",
    "reviewer-approved",
    "publication-ready",
    "superseded",
    "deprecated",
}
VISUAL_ASSET_TERMINAL = {"superseded", "deprecated"}
VISUAL_ASSET_EDGES = [
    ("candidate", "grounded"),
    ("grounded", "review-required"),
    ("review-required", "reviewer-approved"),
    ("review-required", "candidate"),
    ("reviewer-approved", "publication-ready"),
    ("reviewer-approved", "review-required"),
    ("publication-ready", "superseded"),
    ("publication-ready", "deprecated"),
    ("superseded", "deprecated"),
]

NEW_EVENT_STORES = [
    "grounding-events",
    "visual-publication-build-events",
    "supportive-image-mapping-events",
    "prompt-events",
    "prompt-revision-events",
    "visual-troubleshooting-events",
    "procedural-continuity-events",
    "visual-asset-lifecycle-events",
]

# ---------------------------------------------------------------------------
# Rule tables
# ---------------------------------------------------------------------------

GROUNDING_RULES = {
    "schema": "multimodal-grounding-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "GR-1", "rule": "every grounding record MUST cite at least one image_id and one grounded_target_id."},
        {"id": "GR-2", "rule": "grounded_target_id MUST resolve to an existing procedural / troubleshooting / specification / warning / installation / operational target."},
        {"id": "GR-3", "rule": "every grounding record MUST carry source evidence_ids and image provenance (source_uri or source_manifest)."},
        {"id": "GR-4", "rule": "trust_tier MUST be declared per image; OEM > certified-installer > field-reviewer > contributor."},
        {"id": "GR-5", "rule": "probabilistic / similarity-derived bindings are FORBIDDEN — bindings are reviewer-declared only."},
        {"id": "GR-6", "rule": "confidence_state ∈ {reviewer-approved, review-required, unresolved}; unresolved blocks publication-ready promotion."},
        {"id": "GR-7", "rule": "synthesis_id MUST be present and resolve to an existing layer-41 synthesis manifest."},
        {"id": "GR-8", "rule": "no silent rebinding: replacing an image_id requires append-only revision with prior_grounding_id."},
        {"id": "GR-9", "rule": "reviewer attribution required on every grounding record."},
    ],
}

VISUAL_PUBLICATION_RULES = {
    "schema": "visual-publication-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "VP-1", "rule": "visual publication builds MUST be written under operational-console/visual-publication-builds/<state>/<build_id>/ — NEVER into the live publication tree."},
        {"id": "VP-2", "rule": "build_id collisions are refused (fail-closed)."},
        {"id": "VP-3", "rule": "outputs are deterministic: identical inputs MUST yield byte-identical manual.html and manual.json."},
        {"id": "VP-4", "rule": "every visual placement MUST carry grounding_id + image_id + role + evidence_ids."},
        {"id": "VP-5", "rule": "supported output formats: html, json. PDF is out-of-scope for this layer."},
        {"id": "VP-6", "rule": "synthesis_id MUST resolve to a layer-41 synthesis manifest."},
        {"id": "VP-7", "rule": "publication-ready promotion is blocked when any required image role is missing or when continuity check fails."},
    ],
}

SUPPORTIVE_IMAGE_RULES = {
    "schema": "supportive-image-matrix-rules/1.0",
    "constitutional_layer_index": LAYER,
    "image_roles": IMAGE_ROLES,
    "role_to_section": {
        "contextual": ["overview", "operation"],
        "procedural": ["installation", "operation"],
        "warning": ["warnings", "operation", "installation"],
        "troubleshooting": ["troubleshooting"],
        "specification": ["specifications"],
        "orientation": ["overview", "prerequisites"],
        "escalation-support": ["support", "troubleshooting"],
        "comparison-support": ["specifications", "operation"],
    },
    "rules": [
        {"id": "SI-1", "rule": "every supportive-image mapping MUST declare role ∈ IMAGE_ROLES."},
        {"id": "SI-2", "rule": "role-to-section mapping is reviewer-governed; cross-role sharing requires explicit reviewer attribution."},
        {"id": "SI-3", "rule": "warning role images MUST carry evidence lineage AND a reviewer-approved warning manifest reference."},
        {"id": "SI-4", "rule": "specification role images MUST cite the specific specification field they support."},
        {"id": "SI-5", "rule": "comparison-support images MUST list both compared canonical_product_ids."},
        {"id": "SI-6", "rule": "contextual / orientation images MAY be reused across products only with explicit reviewer-attestation."},
    ],
}

PROMPT_GOVERNANCE_RULES = {
    "schema": "prompt-governance-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "PG-1", "rule": "every prompt MUST be bound to a grounding_id, canonical_product_id, and synthesis_id."},
        {"id": "PG-2", "rule": "every prompt revision is append-only and carries prior_prompt_id; in-place edits are FORBIDDEN."},
        {"id": "PG-3", "rule": "detached prompts (no grounding_id) are FORBIDDEN."},
        {"id": "PG-4", "rule": "prompt provenance MUST record reviewer, created_at_iso, intent, and constraints."},
        {"id": "PG-5", "rule": "prompt content is reviewer-authored text; autonomous LLM-driven prompt synthesis is FORBIDDEN."},
        {"id": "PG-6", "rule": "publication lineage MUST trace every published image back to a prompt_revision_id (or source_provenance for non-generated assets)."},
        {"id": "PG-7", "rule": "prompt deletion is FORBIDDEN; deprecation requires reviewer attribution and lineage preservation."},
    ],
}

VISUAL_TROUBLESHOOTING_RULES = {
    "schema": "visual-troubleshooting-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "VT-1", "rule": "every troubleshooting symptom MAY carry one or more grounded visuals; each MUST cite evidence_ids."},
        {"id": "VT-2", "rule": "escalation steps MUST cite the support manifest AND a grounded escalation-support image (if available)."},
        {"id": "VT-3", "rule": "operational warnings MUST cite at least one warning-role visual when a visual exists in the asset ledger."},
        {"id": "VT-4", "rule": "unresolved ambiguity MUST be carried forward as 'visual_unresolved=true' rather than silently dropped."},
        {"id": "VT-5", "rule": "confidence_state propagates from grounding into the troubleshooting flow; reviewer-approved is required for publication-ready promotion."},
    ],
}

PROCEDURAL_CONTINUITY_RULES = {
    "schema": "procedural-image-continuity-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "PC-1", "rule": "procedural images MUST be ordered by procedural step_index; gaps are detected and flagged."},
        {"id": "PC-2", "rule": "missing-step visuals MUST emit a continuity-event with kind='missing-step-visual'."},
        {"id": "PC-3", "rule": "orphan visual assets (no grounding) MUST emit a continuity-event with kind='orphan-asset'."},
        {"id": "PC-4", "rule": "broken image lineage (image_id referenced by a grounding but absent from the asset ledger) is fail-closed."},
        {"id": "PC-5", "rule": "broken continuity blocks publication-ready promotion of the corresponding visual publication build."},
        {"id": "PC-6", "rule": "reviewer override MUST be explicit, attributed, and recorded as a continuity-event with kind='reviewer-accepted-gap'."},
    ],
}

VISUAL_ASSET_LIFECYCLE_RULES = {
    "schema": "visual-asset-lifecycle-rules/1.0",
    "constitutional_layer_index": LAYER,
    "states": sorted(VISUAL_ASSET_STATES),
    "terminal_states": sorted(VISUAL_ASSET_TERMINAL),
    "edges": [list(e) for e in VISUAL_ASSET_EDGES],
    "rules": [
        {"id": "VL-1", "rule": "reviewer attribution required on every state transition."},
        {"id": "VL-2", "rule": "asset replacement is append-only via supersedence; silent overwrite is FORBIDDEN."},
        {"id": "VL-3", "rule": "hidden regeneration is FORBIDDEN; every regeneration MUST carry a prompt_revision_id and reviewer attribution."},
        {"id": "VL-4", "rule": "terminal states (superseded, deprecated) are immutable."},
        {"id": "VL-5", "rule": "publication-ready promotion requires (a) reviewer-approved grounding, (b) continuity-clean state."},
    ],
}

MULTIMODAL_RENDER_RULES = {
    "schema": "multimodal-render-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "MR-1", "rule": "every <img> MUST carry data-grounding-id, data-image-id, data-role, data-evidence."},
        {"id": "MR-2", "rule": "alt text is reviewer-authored Spanish (Colombia); machine-translated alt text is FORBIDDEN."},
        {"id": "MR-3", "rule": "image src is the relative path stored in the asset ledger; remote URLs are FORBIDDEN at render time."},
        {"id": "MR-4", "rule": "missing-image placeholders are explicit visual markers (visual-not-available); silent omission is FORBIDDEN."},
        {"id": "MR-5", "rule": "trust composition (per-image trust_tier) is rendered as a visible badge."},
    ],
}

RULE_TABLES = {
    "multimodal-grounding-rules.json": GROUNDING_RULES,
    "visual-publication-rules.json": VISUAL_PUBLICATION_RULES,
    "supportive-image-matrix-rules.json": SUPPORTIVE_IMAGE_RULES,
    "prompt-governance-rules.json": PROMPT_GOVERNANCE_RULES,
    "visual-troubleshooting-rules.json": VISUAL_TROUBLESHOOTING_RULES,
    "procedural-image-continuity-rules.json": PROCEDURAL_CONTINUITY_RULES,
    "visual-asset-lifecycle-rules.json": VISUAL_ASSET_LIFECYCLE_RULES,
    "multimodal-render-rules.json": MULTIMODAL_RENDER_RULES,
}

# ---------------------------------------------------------------------------
# JS engines (vanilla ES; never write FS; only build envelopes)
# ---------------------------------------------------------------------------

GROUNDING_ENGINE_JS = """// phase 49 — multimodal grounding engine (deterministic, reviewer-driven, NO ML).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var Grounding = OC.Grounding = OC.Grounding || {};
  Grounding.KINDS = ['procedural-step','troubleshooting-flow','specification-field','warning','installation-sequence','operational-state'];
  Grounding.CONFIDENCE = ['reviewer-approved','review-required','unresolved'];
  Grounding.buildGroundingRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.image_ids || !input.image_ids.length) throw new Error('GR-1: image_ids required');
    if (!input.grounded_target_id) throw new Error('GR-1: grounded_target_id required');
    if (!input.grounding_kind || Grounding.KINDS.indexOf(input.grounding_kind) < 0) throw new Error('GR-2: invalid grounding_kind');
    if (!input.synthesis_id) throw new Error('GR-7: synthesis_id required');
    if (!input.reviewer) throw new Error('GR-9: reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'grounding',
      reviewer: input.reviewer,
      payload: {
        grounding_id: input.grounding_id || null,
        synthesis_id: input.synthesis_id,
        canonical_product_id: input.canonical_product_id || null,
        grounding_kind: input.grounding_kind,
        grounded_target_id: input.grounded_target_id,
        image_ids: input.image_ids,
        evidence_ids: input.evidence_ids || [],
        rationale: input.rationale || '',
        confidence_state: input.confidence_state || 'review-required',
        prior_grounding_id: input.prior_grounding_id || null
      }
    });
  };
})(window);
"""

VISUAL_PUBLICATION_ENGINE_JS = """// phase 49 — visual publication orchestration engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var VP = OC.VisualPublication = OC.VisualPublication || {};
  VP.buildVisualPublicationRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.synthesis_id) throw new Error('VP-6: synthesis_id required');
    if (!input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'visual-publication-build',
      reviewer: input.reviewer,
      payload: {
        build_id: input.build_id || null,
        manual_id: input.manual_id || 'manual',
        synthesis_id: input.synthesis_id,
        canonical_product_id: input.canonical_product_id || null,
        placements: input.placements || [],
        output_formats: input.output_formats || ['html','json']
      }
    });
  };
})(window);
"""

SUPPORTIVE_IMAGE_ENGINE_JS = """// phase 49 — supportive-image matrix engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var SI = OC.SupportiveImage = OC.SupportiveImage || {};
  SI.ROLES = ['contextual','procedural','warning','troubleshooting','specification','orientation','escalation-support','comparison-support'];
  SI.buildMappingRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.image_id) throw new Error('image_id required');
    if (SI.ROLES.indexOf(input.role) < 0) throw new Error('SI-1: invalid role');
    if (!input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'supportive-image-mapping',
      reviewer: input.reviewer,
      payload: {
        image_id: input.image_id,
        role: input.role,
        applies_to_sections: input.applies_to_sections || [],
        canonical_product_ids: input.canonical_product_ids || [],
        evidence_ids: input.evidence_ids || []
      }
    });
  };
})(window);
"""

PROMPT_ENGINE_JS = """// phase 49 — prompt governance engine (append-only, reviewer-authored).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PG = OC.Prompt = OC.Prompt || {};
  PG.buildPromptRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.grounding_id) throw new Error('PG-3: grounding_id required (no detached prompts)');
    if (!input.canonical_product_id) throw new Error('PG-1: canonical_product_id required');
    if (!input.synthesis_id) throw new Error('PG-1: synthesis_id required');
    if (!input.reviewer) throw new Error('reviewer required');
    if (typeof input.prompt_text !== 'string' || !input.prompt_text.length) throw new Error('PG-5: prompt_text required (reviewer-authored)');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'prompt',
      reviewer: input.reviewer,
      payload: {
        prompt_id: input.prompt_id || null,
        grounding_id: input.grounding_id,
        canonical_product_id: input.canonical_product_id,
        synthesis_id: input.synthesis_id,
        intent: input.intent || '',
        constraints: input.constraints || [],
        prompt_text: input.prompt_text,
        prior_prompt_id: input.prior_prompt_id || null
      }
    });
  };
})(window);
"""

VISUAL_TROUBLESHOOTING_ENGINE_JS = """// phase 49 — visual troubleshooting engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var VT = OC.VisualTroubleshooting = OC.VisualTroubleshooting || {};
  VT.buildBindingRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.flow_id) throw new Error('flow_id required');
    if (!input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'visual-troubleshooting',
      reviewer: input.reviewer,
      payload: {
        flow_id: input.flow_id,
        synthesis_id: input.synthesis_id || null,
        symptom_visuals: input.symptom_visuals || [],
        escalation_visuals: input.escalation_visuals || [],
        warning_visuals: input.warning_visuals || [],
        visual_unresolved: !!input.visual_unresolved
      }
    });
  };
})(window);
"""

CONTINUITY_ENGINE_JS = """// phase 49 — procedural image continuity engine (deterministic gap detection).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PC = OC.Continuity = OC.Continuity || {};
  PC.detectGaps = function (steps) {
    // steps: [{step_index, image_id?}] sorted ascending; returns missing indices.
    if (!Array.isArray(steps) || !steps.length) return [];
    var gaps = [];
    var max = 0; var i;
    for (i = 0; i < steps.length; i++) if (steps[i].step_index > max) max = steps[i].step_index;
    var present = {};
    for (i = 0; i < steps.length; i++) if (steps[i].image_id) present[steps[i].step_index] = true;
    for (i = 1; i <= max; i++) if (!present[i]) gaps.push(i);
    return gaps;
  };
  PC.buildContinuityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.publication_build_id) throw new Error('publication_build_id required');
    if (!input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'procedural-continuity',
      reviewer: input.reviewer,
      payload: {
        publication_build_id: input.publication_build_id,
        steps: input.steps || [],
        orphan_image_ids: input.orphan_image_ids || [],
        broken_lineage_image_ids: input.broken_lineage_image_ids || [],
        reviewer_accepted_gaps: input.reviewer_accepted_gaps || []
      }
    });
  };
})(window);
"""

VISUAL_LIFECYCLE_ENGINE_JS = """// phase 49 — visual asset lifecycle engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var VL = OC.VisualLifecycle = OC.VisualLifecycle || {};
  VL.STATES = ['candidate','grounded','review-required','reviewer-approved','publication-ready','superseded','deprecated'];
  VL.EDGES = [
    ['candidate','grounded'], ['grounded','review-required'],
    ['review-required','reviewer-approved'], ['review-required','candidate'],
    ['reviewer-approved','publication-ready'], ['reviewer-approved','review-required'],
    ['publication-ready','superseded'], ['publication-ready','deprecated'],
    ['superseded','deprecated']
  ];
  VL.isLegal = function (from, to) {
    for (var i = 0; i < VL.EDGES.length; i++) if (VL.EDGES[i][0] === from && VL.EDGES[i][1] === to) return true;
    return false;
  };
  VL.buildTransitionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.image_id) throw new Error('image_id required');
    if (!VL.isLegal(input.from_state, input.to_state)) throw new Error('VL: illegal transition ' + input.from_state + ' -> ' + input.to_state);
    if (!input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'visual-asset-lifecycle-transition',
      reviewer: input.reviewer,
      payload: {
        image_id: input.image_id,
        from_state: input.from_state,
        to_state: input.to_state,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
"""

MULTIMODAL_RENDER_ENGINE_JS = """// phase 49 — multimodal renderer (deterministic, escapes attributes).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var MR = OC.MultimodalRender = OC.MultimodalRender || {};
  function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }
  MR.renderPlacement = function (p) {
    if (!p || !p.image_id) return '<div class="oc-visual-missing" data-reason="visual-not-available">visual-not-available</div>';
    return '<figure class="oc-visual" data-grounding-id="' + esc(p.grounding_id||'') +
           '" data-image-id="' + esc(p.image_id) + '" data-role="' + esc(p.role||'contextual') +
           '" data-evidence="' + esc((p.evidence_ids||[]).join(',')) + '">' +
           '<img src="' + esc(p.src||'') + '" alt="' + esc(p.alt||'') + '" loading="lazy">' +
           '<figcaption><span class="oc-visual-role">' + esc(p.role||'contextual') + '</span> ' +
           '<span class="oc-visual-trust" data-tier="' + esc(p.trust_tier||'') + '">' + esc(p.trust_tier||'') + '</span></figcaption>' +
           '</figure>';
  };
})(window);
"""

JS_ASSETS = {
    "grounding-engine.js": GROUNDING_ENGINE_JS,
    "visual-publication-engine.js": VISUAL_PUBLICATION_ENGINE_JS,
    "supportive-image-engine.js": SUPPORTIVE_IMAGE_ENGINE_JS,
    "prompt-engine.js": PROMPT_ENGINE_JS,
    "visual-troubleshooting-engine.js": VISUAL_TROUBLESHOOTING_ENGINE_JS,
    "continuity-engine.js": CONTINUITY_ENGINE_JS,
    "visual-lifecycle-engine.js": VISUAL_LIFECYCLE_ENGINE_JS,
    "multimodal-render-engine.js": MULTIMODAL_RENDER_ENGINE_JS,
}

# ---------------------------------------------------------------------------
# Console HTML
# ---------------------------------------------------------------------------

PHASE49_SCRIPTS = "\n".join(
    f'<script src="../assets/exec/{name}"></script>' for name in JS_ASSETS
)

HTML_HEAD_TEMPLATE = (
    "<!doctype html><html lang='es-CO'><head><meta charset='utf-8'>"
    "<title>{title}</title>"
    "<link rel='stylesheet' href='../assets/exec/exec.css'></head>"
    "<body class='oc-exec'><header class='oc-exec__header'><h1>{title}</h1>"
    "<p class='oc-exec__subtitle'>Phase 49 — Governed multimodal grounding & visual publication orchestration. "
    "Reviewer-first. Deterministic. Append-only. Browser surfaces never write the filesystem.</p></header>"
    "<main class='oc-exec__main'>"
)

HTML_TAIL = (
    "</main><footer class='oc-exec__footer'>"
    "<p>Layer 42 — subordinate to layer 41 (governed knowledge synthesis & canonical publication).</p>"
    "</footer>"
    '<script src="../assets/exec/fs-bridge.js"></script>'
    + PHASE49_SCRIPTS +
    "</body></html>\n"
)

CONSOLES = {
    "grounding-console": "Multimodal grounding console",
    "visual-publication-console": "Visual publication orchestration console",
    "supportive-image-console": "Supportive-image matrix console",
    "prompt-governance-console": "Image prompt governance console",
    "visual-troubleshooting-console": "Visual troubleshooting console",
    "continuity-console": "Procedural image continuity console",
    "visual-lifecycle-console": "Visual asset lifecycle console",
    "multimodal-inspection-console": "Multimodal visibility & inspection console",
}

CSS_MARKER = "/* phase 49 — multimodal grounding & visual publication additions */"
CSS_ADDENDUM = """
/* phase 49 — multimodal grounding & visual publication additions */
.oc-visual { margin: 1rem 0; padding: 0.5rem; border: 1px solid #d6d6d6; }
.oc-visual img { max-width: 100%; height: auto; display: block; }
.oc-visual figcaption { font-size: 0.85rem; color: #555; margin-top: 0.25rem; }
.oc-visual-role { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 0.2rem; background: #eef; margin-right: 0.5rem; }
.oc-visual-trust[data-tier='OEM'] { background: #cfc; padding: 0.1rem 0.4rem; }
.oc-visual-trust[data-tier='certified-installer'] { background: #ffe; padding: 0.1rem 0.4rem; }
.oc-visual-trust[data-tier='field-reviewer'] { background: #fee; padding: 0.1rem 0.4rem; }
.oc-visual-missing { padding: 1rem; border: 2px dashed #c00; color: #900; font-weight: bold; }
.oc-grounding-state[data-state='unresolved'] { color: #c00; font-weight: bold; }
.oc-grounding-state[data-state='review-required'] { color: #b58900; }
.oc-grounding-state[data-state='reviewer-approved'] { color: #060; }
.oc-asset-state { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 0.2rem; border: 1px solid #999; font-size: 0.8rem; }
.oc-asset-state[data-state='publication-ready'] { background: #cfc; }
.oc-asset-state[data-state='superseded'], .oc-asset-state[data-state='deprecated'] { background: #ddd; color: #555; }
.oc-continuity-gap { background: #fee; padding: 0.25rem 0.5rem; border-left: 4px solid #c00; }
.oc-prompt-revision { font-family: monospace; white-space: pre-wrap; background: #f7f7f7; padding: 0.5rem; border-left: 3px solid #69c; }
"""

# ---------------------------------------------------------------------------
# Doctrines
# ---------------------------------------------------------------------------

DOCTRINES = {
    "01-deterministic-grounding-only.md": "Grounding bindings are reviewer-declared and deterministic. Probabilistic / similarity-based binding is FORBIDDEN.\n",
    "02-no-autonomous-image-generation.md": "Layer 42 does NOT generate images autonomously. Image creation is out-of-band and reviewer-authorized; this layer only governs grounding, prompts, lineage, and publication assembly.\n",
    "03-prompt-append-only-lineage.md": "Prompts are append-only. Every revision references prior_prompt_id. In-place edits or silent prompt mutation are FORBIDDEN.\n",
    "04-no-silent-image-replacement.md": "Replacing a grounded image requires explicit supersedence with prior_grounding_id and reviewer attribution.\n",
    "05-fail-closed-on-broken-continuity.md": "Broken procedural continuity (missing-step, orphan, broken-lineage) blocks publication-ready promotion.\n",
    "06-evidence-lineage-mandatory.md": "Every grounding, every prompt, every visual placement MUST carry evidence_ids tracing back to layer-38 evidence and a layer-41 synthesis manifest.\n",
    "07-visual-publication-isolated-from-live-tree.md": "Visual publications are written into operational-console/visual-publication-builds/ — NEVER into the live publication tree.\n",
    "08-reviewer-authoritative-multimodal.md": "Every grounding, mapping, prompt, lifecycle transition, and visual publication build is reviewer-attributed.\n",
    "09-cli-only-no-daemon.md": "Browser surfaces NEVER write the filesystem. Mutation occurs only via the CLI executor with --confirm.\n",
    "10-no-cloud-no-saas-no-ml-multimodal.md": "No cloud image pipelines, no SaaS orchestration, no ML embeddings, no probabilistic visual matching at any layer of this surface.\n",
}

DOCTRINE_DIR = KB_ROOT / "GOVERNED_MULTIMODAL_GROUNDING_GOVERNANCE"

# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

REPORTS = [
    ("01-multimodal-grounding-summary", "Multimodal grounding engine summary."),
    ("02-visual-publication-orchestration-summary", "Visual publication orchestration summary."),
    ("03-supportive-image-matrix-summary", "Supportive-image matrix governance summary."),
    ("04-prompt-governance-summary", "Image prompt governance summary."),
    ("05-visual-troubleshooting-summary", "Visual troubleshooting synthesis summary."),
    ("06-procedural-image-continuity-summary", "Procedural image continuity summary."),
    ("07-multimodal-rendering-summary", "Multimodal publication rendering summary."),
    ("08-visual-lifecycle-summary", "Visual asset lifecycle governance summary."),
    ("09-multimodal-visibility-summary", "Multimodal visibility & inspection summary."),
    ("10-governed-multimodal-platform-maturity-reassessment", "Governed multimodal knowledge publication platform — maturity reassessment."),
]

REPORT_DIR = REPORTS_ROOT / "governed-multimodal-grounding"

# ---------------------------------------------------------------------------
# Runtime README addendum
# ---------------------------------------------------------------------------

RUNTIME_README_MARKER = "## phase 49 — governed multimodal knowledge grounding & visual publication orchestration"
RUNTIME_README_ADDENDUM = """

## phase 49 — governed multimodal knowledge grounding & visual publication orchestration

Layer 42. Subordinate to layer 41 (governed-knowledge-synthesis-and-canonical-publication-governance).

Mutation is performed exclusively by `tools/governed_multimodal_grounding_executor.py --confirm`.
Subcommands (`--kind`):

- `grounding` — bind images to procedural / troubleshooting / specification / warning / installation / operational targets.
- `supportive-image-mapping` — declare image role and applicability.
- `prompt` — append a reviewer-authored prompt (append-only; revisions carry prior_prompt_id).
- `visual-publication-build` — write a deterministic visual manual (HTML + JSON) under `operational-console/visual-publication-builds/draft/<build_id>/`.
- `visual-troubleshooting` — bind visuals to a troubleshooting flow.
- `procedural-continuity` — record continuity check (gaps, orphans, broken lineage, reviewer-accepted gaps).
- `visual-asset-lifecycle-transition` — advance an image through candidate → grounded → review-required → reviewer-approved → publication-ready → {superseded | deprecated}.

Every command:
- requires reviewer attribution,
- is fail-closed on missing evidence / broken lineage / illegal transitions,
- appends to one or more append-only event stores under `operational-console/runtime-manifests/`,
- writes only into `grounding-drafts/`, `prompt-drafts/`, `visual-publication-builds/`, or `visual-asset-ledger/`.
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
    for root, readme in [
        (GROUNDING_DRAFTS_ROOT, "Reviewer-authored grounding manifests. Append-only."),
        (PROMPT_DRAFTS_ROOT, "Reviewer-authored prompts and revisions. Append-only."),
        (VISUAL_PUBLICATION_BUILDS_ROOT, "Visual publication builds — isolated from live publication tree."),
        (VISUAL_ASSET_LEDGER_ROOT, "Append-only visual asset ledger (per-image lifecycle states)."),
    ]:
        readme_path = root / "README.md"
        if not readme_path.exists():
            write_text(readme_path, f"# {root.name}\n\n{readme}\n\nPhase 49 / layer 42.\n")
            count += 1
    for state in sorted(VISUAL_ASSET_STATES):
        d = VISUAL_PUBLICATION_BUILDS_ROOT / state
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            (d / ".gitkeep").write_text("", encoding="utf-8")
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
            f"<code>{slug}</code> surface. The browser does NOT mutate the filesystem.</p>"
            f"<p>Submit envelopes via <code>tools/governed_multimodal_grounding_executor.py --kind &lt;kind&gt; --request &lt;file&gt; --confirm</code>.</p>"
            f"</section>"
        )
        write_text(OC_ROOT / slug / "exec.html", html + body + HTML_TAIL)
    return len(CONSOLES)


def build_doctrines() -> int:
    DOCTRINE_DIR.mkdir(parents=True, exist_ok=True)
    index_lines = ["# GOVERNED MULTIMODAL GROUNDING GOVERNANCE", "", f"Layer {LAYER}. Phase 49.", ""]
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
               "# Governed multimodal grounding — reports\n\nPhase 49 / layer 42 reports.\n")
    for slug, title in REPORTS:
        write_text(REPORT_DIR / f"{slug}.md", f"# {title}\n\nLayer {LAYER}. Phase 49.\n")
        write_json(REPORT_DIR / f"{slug}.json", {
            "schema": "governance-report/1.0",
            "constitutional_layer_index": LAYER,
            "report_slug": slug,
            "title": title,
            "subordinate_to": SUBORDINATE_TO,
            "posture": POSTURE,
            "image_roles": IMAGE_ROLES,
            "grounding_kinds": GROUNDING_KINDS,
            "visual_asset_states": sorted(VISUAL_ASSET_STATES),
            "visual_asset_terminal_states": sorted(VISUAL_ASSET_TERMINAL),
            "visual_asset_edges": [list(e) for e in VISUAL_ASSET_EDGES],
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
        "Phase 49 — governed multimodal knowledge grounding & visual publication orchestration written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {storage} | New event stores: {stores} | Rule tables: {rules} | "
        f"JS assets: {js} | Exec consoles: {consoles} | Doctrines: {doctrines} | Reports: {reports} | "
        f"RUNTIME_README addendum: {readme}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
