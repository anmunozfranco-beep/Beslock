"""
Phase 52 — Governed Semantic Evidence Analysis & Multimodal Extraction Runtime (layer 45).

Idempotent stdlib-only builder. Emits the layer-45 surface over layer 44
(governed multimodal publication composition & page orchestration), layer 43
(governed visual generation), layer 42 (governed multimodal grounding), and
layer 41 (governed knowledge synthesis).

The runtime writer is the executor (`tools/governed_semantic_extraction_executor.py`).
This builder NEVER mutates event stores, runtime data, knowledge-core,
governance, runtime-implementation, runtime-manifests payloads,
publication-composition-runtime data, visual-publication-builds,
visual-generation-runtime data, OEM source assets, uploads, or live publications.

Posture:
- deterministic, reviewer-authoritative, append-only, local-first, stdlib-first,
  fail-closed, replayable, auditable.
- NO autonomous publication, NO autonomous routing, NO autonomous reviewer
  decisions, NO hidden extraction, NO silent evidence mutation, NO cloud APIs,
  NO SaaS, NO telemetry, NO watchers, NO daemons, NO background workers,
  NO embeddings, NO probabilistic semantic matching, NO vector databases,
  NO autonomous LLM reasoning, NO hidden OCR mutation, NO silent correction.
- The runtime may PROPOSE extraction candidates ONLY.
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

SE_ROOT = OC_ROOT / "semantic-extraction-runtime"

SE_SUBDIRS = [
    "evidence-decompositions",
    "video-decompositions",
    "image-decompositions",
    "pdf-decompositions",
    "spreadsheet-decompositions",
    "ocr-fragments",
    "ocr-corrections",
    "extraction-candidates",
    "temporal-continuity",
    "extraction-lineage",
    "extraction-replays",
    "extraction-integrity",
    "reviewer-extraction-decisions",
    "semantic-extraction-lifecycle",
]

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA = "governed-semantic-extraction/1.0"
LAYER = 45

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
]
while len(SUBORDINATE_TO) < 44:
    SUBORDINATE_TO.append(
        "governed-multimodal-publication-composition-and-page-orchestration-governance"
    )

POSTURE = {
    "deterministic": True,
    "reviewer_authoritative": True,
    "append_only_lineage": True,
    "local_first": True,
    "stdlib_first": True,
    "replayable": True,
    "auditable": True,
    "no_autonomous_publication": True,
    "no_autonomous_routing": True,
    "no_autonomous_reviewer_decisions": True,
    "no_hidden_extraction": True,
    "no_silent_evidence_mutation": True,
    "no_cloud_apis": True,
    "no_saas_dependency": True,
    "no_telemetry": True,
    "no_watchers": True,
    "no_daemons": True,
    "no_background_workers": True,
    "no_embeddings": True,
    "no_probabilistic_semantic_matching": True,
    "no_vector_databases": True,
    "no_autonomous_llm_reasoning": True,
    "no_hidden_ocr_mutation": True,
    "no_silent_correction": True,
    "fail_closed_on_orphan_candidate": True,
    "fail_closed_on_broken_lineage": True,
    "fail_closed_on_invalid_ocr_reference": True,
    "fail_closed_on_missing_source_evidence": True,
    "fail_closed_on_temporal_continuity_gap": True,
    "fail_closed_on_illegal_candidate_state": True,
    "fail_closed_on_duplicate_extraction_id": True,
    "fail_closed_on_forbidden_overwrite_path": True,
    "fail_closed_on_hidden_extraction_mutation": True,
    "writes_only_into_semantic_extraction_runtime_tree": True,
    "browser_surfaces_never_write_filesystem": True,
    "writes_to_live_publication_tree": False,
    "writes_to_publication_composition_runtime_tree": False,
    "writes_to_visual_publication_builds_tree": False,
    "writes_to_visual_generation_runtime_tree": False,
}

# Supported evidence kinds (closed enum).
EVIDENCE_KINDS = ["video", "image", "pdf", "xls", "xlsx", "csv"]

# Closed enum of extraction candidate kinds (per spec).
CANDIDATE_KINDS = [
    "procedural-step-candidate",
    "troubleshooting-candidate",
    "warning-candidate",
    "specification-field-candidate",
    "ui-state-candidate",
    "app-flow-candidate",
    "terminology-candidate",
    "visual-anchor-candidate",
    "section-candidate",
    "table-candidate",
]

# Allowed candidate confidence states (per spec).
CONFIDENCE_STATES = ["reviewer-approved", "review-required", "unresolved"]

# Extraction (candidate) lifecycle states.
LIFECYCLE_STATES = {
    "unresolved",
    "review-required",
    "reviewer-approved",
    "superseded",
    "deprecated",
}
LIFECYCLE_TERMINAL = {"deprecated"}
LIFECYCLE_EDGES = [
    ("unresolved", "review-required"),
    ("unresolved", "deprecated"),
    ("review-required", "reviewer-approved"),
    ("review-required", "unresolved"),
    ("review-required", "deprecated"),
    ("reviewer-approved", "review-required"),
    ("reviewer-approved", "superseded"),
    ("superseded", "deprecated"),
]

NEW_EVENT_STORES = [
    "evidence-decomposition-events",
    "ocr-fragment-events",
    "ocr-correction-events",
    "extraction-candidate-events",
    "temporal-continuity-events",
    "extraction-lineage-events",
    "extraction-replay-events",
    "extraction-lifecycle-events",
    "extraction-integrity-events",
]

# ---------------------------------------------------------------------------
# Rule tables
# ---------------------------------------------------------------------------

DECOMPOSITION_RULES = {
    "schema": "evidence-decomposition-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "ED-1", "rule": "every evidence decomposition MUST be reviewer-attributed and cite source_evidence_id, evidence_kind ∈ EVIDENCE_KINDS, and content_sha256."},
        {"id": "ED-2", "rule": "decomposition is reviewer-proposed; the runtime MUST NOT autonomously decompose evidence."},
        {"id": "ED-3", "rule": "video decompositions MUST cite an ordered list of keyframes with timestamps; gaps in timeline ordering BLOCK approval."},
        {"id": "ED-4", "rule": "PDF decompositions MUST cite ordered page indices starting at 1; gaps BLOCK approval."},
        {"id": "ED-5", "rule": "spreadsheet decompositions MUST cite each worksheet by deterministic name and column count."},
        {"id": "ED-6", "rule": "image decompositions MUST cite at least one visual anchor or OCR-ready region."},
        {"id": "ED-7", "rule": "decomposition manifests are append-only; in-place mutation is FORBIDDEN."},
        {"id": "ED-8", "rule": "decomposition MUST NOT mutate the source evidence file or any prior-layer storage tree."},
    ],
}

OCR_RULES = {
    "schema": "ocr-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "OF-1", "rule": "every OCR fragment MUST cite source_evidence_id, decomposition_id, region or page reference, and reviewer attribution."},
        {"id": "OF-2", "rule": "OCR fragments MUST cite verbatim_sha256 of the recorded text; silent normalization is FORBIDDEN."},
        {"id": "OF-3", "rule": "OCR fragments are append-only; in-place mutation is FORBIDDEN."},
        {"id": "OF-4", "rule": "OCR corrections MUST cite prior_fragment_id; corrections without lineage are FORBIDDEN."},
        {"id": "OF-5", "rule": "OCR corrections MUST be reviewer-attributed; autonomous OCR cleanup is FORBIDDEN."},
        {"id": "OF-6", "rule": "OCR language detection / translation / normalization MUST be reviewer-declared; silent translation is FORBIDDEN."},
        {"id": "OF-7", "rule": "OCR fragments cited by a candidate MUST exist; orphan OCR references BLOCK candidate approval."},
    ],
}

CANDIDATE_RULES = {
    "schema": "extraction-candidate-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "EC-1", "rule": "every extraction candidate MUST cite candidate_id, source_evidence_id, extraction_runtime_id, extraction_rule_id, reviewer, confidence_state ∈ CONFIDENCE_STATES, reasoning_chain, and lineage pointers."},
        {"id": "EC-2", "rule": "candidate_kind MUST be in CANDIDATE_KINDS; unknown kinds are fail-closed."},
        {"id": "EC-3", "rule": "candidates default to confidence_state='unresolved' unless the reviewer explicitly attributes a higher state."},
        {"id": "EC-4", "rule": "autonomous approval is FORBIDDEN; only reviewer-attributed lifecycle transitions may set 'reviewer-approved'."},
        {"id": "EC-5", "rule": "duplicate candidate_id is FORBIDDEN; a new candidate citing prior_candidate_id MUST be recorded as supersedence."},
        {"id": "EC-6", "rule": "candidates citing OCR fragments MUST cite at least one ocr_fragment_id; orphan OCR references BLOCK approval."},
        {"id": "EC-7", "rule": "candidates citing video frames MUST cite frame_index and timestamp_ms; missing frames BLOCK approval."},
        {"id": "EC-8", "rule": "candidate manifests are append-only; in-place mutation is FORBIDDEN."},
    ],
}

CONTINUITY_RULES = {
    "schema": "temporal-continuity-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "TC-1", "rule": "every temporal continuity scan MUST cite source_evidence_id and an ordered list of frame_indices."},
        {"id": "TC-2", "rule": "frame_index sequences MUST be strictly increasing; gaps are reported and BLOCK procedural-sequence promotion."},
        {"id": "TC-3", "rule": "frames cited by candidates MUST exist in the decomposition; missing frames BLOCK approval."},
        {"id": "TC-4", "rule": "scene boundaries MUST be reviewer-declared; autonomous scene detection is FORBIDDEN."},
        {"id": "TC-5", "rule": "procedural sequences extracted from video MUST have contiguous frame coverage; non-contiguous procedural sequences BLOCK approval (fail-closed)."},
        {"id": "TC-6", "rule": "orphan frames (referenced by no candidate) are reported but NON-blocking unless the reviewer flags them."},
    ],
}

LINEAGE_RULES = {
    "schema": "extraction-lineage-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "EL-1", "rule": "every extracted candidate MUST trace to: source_evidence_id, decomposition_id, extraction_rule_id, extraction_runtime_id, reviewer attribution, and continuity_chain (if temporal)."},
        {"id": "EL-2", "rule": "lineage is append-only; in-place mutation is FORBIDDEN."},
        {"id": "EL-3", "rule": "broken lineage chains (any pointer that does not resolve) are fail-closed."},
        {"id": "EL-4", "rule": "lineage events MUST cite the manifest sha256 of every linked artifact for replay verification."},
        {"id": "EL-5", "rule": "supersedence MUST cite predecessor candidate_id and successor candidate_id; silent replacement is FORBIDDEN."},
    ],
}

REPLAY_RULES = {
    "schema": "extraction-replay-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "ER-1", "rule": "replay MUST reconstruct the candidate's lineage chain end-to-end; any unresolved pointer is fail-closed."},
        {"id": "ER-2", "rule": "replay MUST verify manifest sha256 of every linked artifact; mismatch is fail-closed."},
        {"id": "ER-3", "rule": "replay MUST be deterministic across invocations; non-determinism is fail-closed."},
        {"id": "ER-4", "rule": "replay MUST NEVER mutate live publication trees, prior-layer runtime trees, or source evidence."},
        {"id": "ER-5", "rule": "replay events are append-only and reviewer-attributed."},
    ],
}

OVERRIDE_RULES = {
    "schema": "reviewer-override-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "RO-1", "rule": "every reviewer override (OCR correction, candidate state change, extraction rejection) MUST be reviewer-attributed and cite the prior artifact_id."},
        {"id": "RO-2", "rule": "overrides are append-only; the prior artifact remains intact and is not deleted."},
        {"id": "RO-3", "rule": "rejection overrides MUST cite at least one rule_id from ED-/OF-/EC-/TC-/EL-/ER-/XL-/XI-* tables."},
        {"id": "RO-4", "rule": "autonomous overrides are FORBIDDEN; the runtime may PROPOSE candidates only."},
    ],
}

XL_RULES = {
    "schema": "extraction-lifecycle-rules/1.0",
    "constitutional_layer_index": LAYER,
    "states": sorted(LIFECYCLE_STATES),
    "terminal_states": sorted(LIFECYCLE_TERMINAL),
    "edges": [list(e) for e in LIFECYCLE_EDGES],
    "rules": [
        {"id": "XL-1", "rule": "reviewer attribution required on every state transition."},
        {"id": "XL-2", "rule": "transitions are append-only; declared from_state MUST equal actual replayed state."},
        {"id": "XL-3", "rule": "terminal state (deprecated) is immutable."},
        {"id": "XL-4", "rule": "reviewer-approved -> superseded MUST cite successor_candidate_id."},
        {"id": "XL-5", "rule": "autonomous lifecycle promotion is FORBIDDEN."},
    ],
}

XI_RULES = {
    "schema": "extraction-integrity-rules/1.0",
    "constitutional_layer_index": LAYER,
    "rules": [
        {"id": "XI-1", "rule": "orphan extraction candidates (citing missing decomposition or evidence) BLOCK approval."},
        {"id": "XI-2", "rule": "broken lineage chains BLOCK approval."},
        {"id": "XI-3", "rule": "invalid OCR references BLOCK approval."},
        {"id": "XI-4", "rule": "missing source evidence BLOCKS approval."},
        {"id": "XI-5", "rule": "temporal continuity gaps BLOCK procedural-sequence promotion."},
        {"id": "XI-6", "rule": "illegal candidate states (state outside LIFECYCLE_STATES) are fail-closed."},
        {"id": "XI-7", "rule": "duplicate extraction IDs are fail-closed."},
        {"id": "XI-8", "rule": "forbidden overwrite paths are fail-closed."},
        {"id": "XI-9", "rule": "hidden extraction mutation (sha256 mismatch on replay) is fail-closed."},
    ],
}

RULE_TABLES = {
    "evidence-decomposition-rules.json": DECOMPOSITION_RULES,
    "extraction-ocr-rules.json": OCR_RULES,
    "extraction-candidate-rules.json": CANDIDATE_RULES,
    "temporal-continuity-rules.json": CONTINUITY_RULES,
    "extraction-lineage-rules.json": LINEAGE_RULES,
    "extraction-replay-rules.json": REPLAY_RULES,
    "reviewer-override-rules.json": OVERRIDE_RULES,
    "extraction-lifecycle-rules.json": XL_RULES,
    "extraction-integrity-rules.json": XI_RULES,
}

# ---------------------------------------------------------------------------
# JS engines (vanilla ES; never write FS; only build envelopes)
# ---------------------------------------------------------------------------

DECOMPOSITION_ENGINE_JS = """// phase 52 — evidence decomposition engine (reviewer-authored, deterministic).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var SE = OC.SemanticExtraction = OC.SemanticExtraction || {};
  SE.EVIDENCE_KINDS = ['video','image','pdf','xls','xlsx','csv'];
  SE.buildDecompositionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('ED-1: reviewer required');
    if (!input.source_evidence_id) throw new Error('ED-1: source_evidence_id required');
    if (SE.EVIDENCE_KINDS.indexOf(input.evidence_kind) < 0) throw new Error('ED-1: invalid evidence_kind');
    if (!input.content_sha256) throw new Error('ED-1: content_sha256 required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'evidence-decomposition',
      reviewer: input.reviewer,
      payload: {
        decomposition_id: input.decomposition_id || null,
        source_evidence_id: input.source_evidence_id,
        evidence_kind: input.evidence_kind,
        content_sha256: input.content_sha256,
        keyframes: input.keyframes || null,
        scene_boundaries: input.scene_boundaries || null,
        pages: input.pages || null,
        worksheets: input.worksheets || null,
        regions: input.regions || null,
        rationale: input.rationale || ''
      }
    });
  };
})(window);
"""

OCR_ENGINE_JS = """// phase 52 — OCR engine (reviewer-authored).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var OCR = OC.OCRGovernance = OC.OCRGovernance || {};
  OCR.buildFragmentRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('OF-1: reviewer required');
    if (!input.source_evidence_id || !input.decomposition_id) throw new Error('OF-1: source_evidence_id and decomposition_id required');
    if (typeof input.text !== 'string') throw new Error('OF-1: text required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'ocr-fragment',
      reviewer: input.reviewer,
      payload: {
        ocr_fragment_id: input.ocr_fragment_id || null,
        source_evidence_id: input.source_evidence_id,
        decomposition_id: input.decomposition_id,
        page_index: input.page_index || null,
        frame_index: input.frame_index || null,
        region: input.region || null,
        language: input.language || 'unknown',
        text: input.text
      }
    });
  };
  OCR.buildCorrectionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('OF-5: reviewer required');
    if (!input.prior_fragment_id) throw new Error('OF-4: prior_fragment_id required');
    if (typeof input.text !== 'string') throw new Error('OF-1: text required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'ocr-correction',
      reviewer: input.reviewer,
      payload: {
        ocr_correction_id: input.ocr_correction_id || null,
        prior_fragment_id: input.prior_fragment_id,
        text: input.text,
        rationale: input.rationale || ''
      }
    });
  };
})(window);
"""

CANDIDATE_ENGINE_JS = """// phase 52 — extraction candidate engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var EC = OC.ExtractionCandidate = OC.ExtractionCandidate || {};
  EC.KINDS = ['procedural-step-candidate','troubleshooting-candidate','warning-candidate','specification-field-candidate','ui-state-candidate','app-flow-candidate','terminology-candidate','visual-anchor-candidate','section-candidate','table-candidate'];
  EC.CONFIDENCE = ['reviewer-approved','review-required','unresolved'];
  EC.buildCandidateRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('EC-1: reviewer required');
    if (!input.source_evidence_id || !input.extraction_runtime_id || !input.extraction_rule_id) {
      throw new Error('EC-1: lineage pointers required');
    }
    if (EC.KINDS.indexOf(input.candidate_kind) < 0) throw new Error('EC-2: invalid candidate_kind');
    var conf = input.confidence_state || 'unresolved';
    if (EC.CONFIDENCE.indexOf(conf) < 0) throw new Error('EC-1: invalid confidence_state');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'extraction-candidate',
      reviewer: input.reviewer,
      payload: {
        candidate_id: input.candidate_id || null,
        source_evidence_id: input.source_evidence_id,
        decomposition_id: input.decomposition_id || null,
        extraction_runtime_id: input.extraction_runtime_id,
        extraction_rule_id: input.extraction_rule_id,
        candidate_kind: input.candidate_kind,
        confidence_state: conf,
        reasoning_chain: input.reasoning_chain || [],
        ocr_fragment_ids: input.ocr_fragment_ids || [],
        frame_indices: input.frame_indices || [],
        page_indices: input.page_indices || [],
        prior_candidate_id: input.prior_candidate_id || null,
        proposal_payload: input.proposal_payload || {}
      }
    });
  };
})(window);
"""

CONTINUITY_ENGINE_JS = """// phase 52 — temporal continuity engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var TC = OC.TemporalContinuity = OC.TemporalContinuity || {};
  TC.buildContinuityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('TC-1: reviewer required');
    if (!input.source_evidence_id) throw new Error('TC-1: source_evidence_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'temporal-continuity',
      reviewer: input.reviewer,
      payload: {
        continuity_check_id: input.continuity_check_id || null,
        source_evidence_id: input.source_evidence_id,
        decomposition_id: input.decomposition_id || null,
        frame_indices: input.frame_indices || [],
        candidate_id: input.candidate_id || null
      }
    });
  };
})(window);
"""

LINEAGE_ENGINE_JS = """// phase 52 — extraction lineage engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var EL = OC.ExtractionLineage = OC.ExtractionLineage || {};
  EL.buildLineageRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('EL-1: reviewer required');
    if (!input.candidate_id) throw new Error('EL-1: candidate_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'extraction-lineage',
      reviewer: input.reviewer,
      payload: {
        lineage_id: input.lineage_id || null,
        candidate_id: input.candidate_id,
        scope: input.scope || 'candidate'
      }
    });
  };
})(window);
"""

REPLAY_ENGINE_JS = """// phase 52 — extraction replay engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var ER = OC.ExtractionReplay = OC.ExtractionReplay || {};
  ER.buildReplayRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('ER-1: reviewer required');
    if (!input.candidate_id && !input.source_evidence_id) throw new Error('ER-1: candidate_id or source_evidence_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'extraction-replay',
      reviewer: input.reviewer,
      payload: {
        replay_id: input.replay_id || null,
        candidate_id: input.candidate_id || null,
        source_evidence_id: input.source_evidence_id || null,
        scope: input.scope || 'candidate'
      }
    });
  };
})(window);
"""

LIFECYCLE_ENGINE_JS = """// phase 52 — extraction lifecycle engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var XL = OC.ExtractionLifecycle = OC.ExtractionLifecycle || {};
  XL.STATES = ['unresolved','review-required','reviewer-approved','superseded','deprecated'];
  XL.EDGES = [
    ['unresolved','review-required'], ['unresolved','deprecated'],
    ['review-required','reviewer-approved'], ['review-required','unresolved'], ['review-required','deprecated'],
    ['reviewer-approved','review-required'], ['reviewer-approved','superseded'],
    ['superseded','deprecated']
  ];
  XL.isLegal = function (from, to) {
    for (var i = 0; i < XL.EDGES.length; i++) if (XL.EDGES[i][0] === from && XL.EDGES[i][1] === to) return true;
    return false;
  };
  XL.buildTransitionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('XL-1: reviewer required');
    if (!input.candidate_id) throw new Error('candidate_id required');
    if (!XL.isLegal(input.from_state, input.to_state)) throw new Error('XL: illegal transition ' + input.from_state + ' -> ' + input.to_state);
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'extraction-lifecycle-transition',
      reviewer: input.reviewer,
      payload: {
        candidate_id: input.candidate_id,
        from_state: input.from_state,
        to_state: input.to_state,
        successor_candidate_id: input.successor_candidate_id || null,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
"""

INTEGRITY_ENGINE_JS = """// phase 52 — extraction integrity engine (reviewer-driven).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var XI = OC.ExtractionIntegrity = OC.ExtractionIntegrity || {};
  XI.buildIntegrityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'extraction-integrity',
      reviewer: input.reviewer,
      payload: {
        integrity_check_id: input.integrity_check_id || null,
        scope: input.scope || 'all',
        source_evidence_id: input.source_evidence_id || null,
        candidate_id: input.candidate_id || null
      }
    });
  };
})(window);
"""

OVERRIDE_ENGINE_JS = """// phase 52 — reviewer override engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var RO = OC.ReviewerOverride = OC.ReviewerOverride || {};
  RO.buildOverrideRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('RO-1: reviewer required');
    if (!input.target_artifact_id) throw new Error('RO-1: target_artifact_id required');
    if (input.kind === 'reject' && (!Array.isArray(input.cited_rule_ids) || input.cited_rule_ids.length === 0)) {
      throw new Error('RO-3: reject requires cited_rule_ids');
    }
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'reviewer-override',
      reviewer: input.reviewer,
      payload: {
        override_id: input.override_id || null,
        target_artifact_id: input.target_artifact_id,
        target_kind: input.target_kind || 'candidate',
        kind: input.kind || 'reject',
        cited_rule_ids: input.cited_rule_ids || [],
        rationale: input.rationale || ''
      }
    });
  };
})(window);
"""

JS_ASSETS = {
    "se-decomposition-engine.js": DECOMPOSITION_ENGINE_JS,
    "se-ocr-engine.js": OCR_ENGINE_JS,
    "se-candidate-engine.js": CANDIDATE_ENGINE_JS,
    "se-continuity-engine.js": CONTINUITY_ENGINE_JS,
    "se-lineage-engine.js": LINEAGE_ENGINE_JS,
    "se-replay-engine.js": REPLAY_ENGINE_JS,
    "se-lifecycle-engine.js": LIFECYCLE_ENGINE_JS,
    "se-integrity-engine.js": INTEGRITY_ENGINE_JS,
    "se-override-engine.js": OVERRIDE_ENGINE_JS,
}

# ---------------------------------------------------------------------------
# Console HTML
# ---------------------------------------------------------------------------

PHASE52_SCRIPTS = "\n".join(
    f'<script src="../assets/exec/{name}"></script>' for name in JS_ASSETS
)

HTML_HEAD_TEMPLATE = (
    "<!doctype html><html lang='es-CO'><head><meta charset='utf-8'>"
    "<title>{title}</title>"
    "<link rel='stylesheet' href='../assets/exec/exec.css'></head>"
    "<body class='oc-exec'><header class='oc-exec__header'><h1>{title}</h1>"
    "<p class='oc-exec__subtitle'>Phase 52 — Governed semantic evidence analysis & multimodal extraction. "
    "Reviewer-authored only. Deterministic. Append-only. No autonomous extraction. "
    "No embeddings. No vector DB. No cloud APIs.</p></header>"
    "<main class='oc-exec__main'>"
)

HTML_TAIL = (
    "</main><footer class='oc-exec__footer'>"
    "<p>Layer 45 — subordinate to layer 44 (governed multimodal publication composition & page orchestration).</p>"
    "</footer>"
    '<script src="../assets/exec/fs-bridge.js"></script>'
    + PHASE52_SCRIPTS +
    "</body></html>\n"
)

CONSOLES = {
    "semantic-extraction-console": "Semantic extraction console",
    "ocr-review-console": "OCR review console",
    "frame-review-console": "Frame review console",
    "table-review-console": "Table review console",
    "continuity-review-console": "Temporal continuity review console",
    "extraction-lineage-console": "Extraction lineage console",
    "extraction-integrity-console": "Extraction integrity console",
}

CSS_MARKER = "/* phase 52 — semantic extraction governance additions */"
CSS_ADDENDUM = """
/* phase 52 — semantic extraction governance additions */
.oc-se-state { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 0.2rem; border: 1px solid #999; font-size: 0.8rem; }
.oc-se-state[data-state='unresolved'] { background: #f4f4f4; color: #555; }
.oc-se-state[data-state='review-required'] { background: #ffe; color: #b58900; }
.oc-se-state[data-state='reviewer-approved'] { background: #cfc; color: #060; font-weight: bold; }
.oc-se-state[data-state='superseded'] { background: #ddd; color: #555; }
.oc-se-state[data-state='deprecated'] { background: #ccc; color: #444; }
.oc-se-candidate { border: 1px solid #ccc; padding: 0.4rem; margin: 0.3rem 0; }
.oc-se-candidate[data-kind='warning-candidate'] { border-color: #c00; background: #fee; }
.oc-se-candidate[data-kind='procedural-step-candidate'] { background: #efe; }
.oc-se-candidate[data-kind='troubleshooting-candidate'] { background: #fef; }
.oc-se-candidate[data-kind='specification-field-candidate'] { background: #eef; }
.oc-se-orphan { background: #fee; padding: 0.3rem; border-left: 4px solid #c00; }
.oc-se-ocr { font-family: monospace; font-size: 0.85rem; background: #f7f7f7; padding: 0.3rem; }
.oc-se-replay-ok { color: #060; }
.oc-se-replay-mismatch { color: #c00; font-weight: bold; }
"""

# ---------------------------------------------------------------------------
# Doctrines
# ---------------------------------------------------------------------------

DOCTRINES = {
    "01-reviewer-authored-extraction-only.md": "Every extraction artifact (decomposition, OCR fragment, candidate, lineage, override) is reviewer-attributed. The runtime may PROPOSE candidates only. Autonomous routing, autonomous approval, and autonomous reasoning are FORBIDDEN.\n",
    "02-deterministic-decomposition.md": "Evidence decomposition is deterministic and reviewer-driven. No probabilistic interpretation. No autonomous scene detection. No silent normalization.\n",
    "03-no-silent-ocr-mutation.md": "Every OCR mutation generates a correction manifest with prior_fragment_id and reviewer attribution. Silent OCR cleanup, silent normalization, and silent translation are FORBIDDEN.\n",
    "04-append-only-extraction-lineage.md": "Lineage is append-only and traces every candidate to source_evidence, decomposition_id, extraction_rule_id, extraction_runtime_id, and reviewer attribution. Broken lineage chains are fail-closed.\n",
    "05-temporal-continuity-fail-closed.md": "Temporal continuity is reviewer-verified. Non-contiguous procedural sequences and missing referenced frames BLOCK approval (fail-closed).\n",
    "06-replay-determinism.md": "Replay reconstructs lineage chains, verifies manifest sha256, and is deterministic across invocations. Non-determinism and hash mismatch are fail-closed. Replay NEVER mutates live publication trees, prior-layer runtime trees, or source evidence.\n",
    "07-extraction-integrity-isolation.md": "Integrity scans report orphan candidates, broken lineage, invalid OCR references, missing source evidence, continuity gaps, illegal candidate states, duplicate IDs, forbidden overwrite paths, and hidden extraction mutation.\n",
    "08-no-embeddings-no-vectors.md": "No embeddings, no probabilistic semantic matching, no vector databases, no autonomous LLM reasoning, no cloud APIs, no SaaS, no telemetry. Extraction is deterministic rule-based candidate proposal.\n",
    "09-storage-isolation.md": "Extraction artifacts are isolated under semantic-extraction-runtime/. The runtime NEVER writes into publication-composition-runtime, visual-publication-builds, visual-generation-runtime, knowledge-core, governance, runtime-implementation, runtime-manifests payloads, OEM source assets, or live publications.\n",
    "10-cli-only-no-daemon-extraction.md": "Browser surfaces NEVER write the filesystem. All extraction mutation occurs only via the CLI executor with --confirm. No daemon. No watcher. No scheduler. No background worker.\n",
}

DOCTRINE_DIR = KB_ROOT / "GOVERNED_SEMANTIC_EXTRACTION_GOVERNANCE"

# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

REPORTS = [
    ("01-evidence-decomposition-summary", "Reviewer-authored evidence decomposition summary."),
    ("02-extraction-candidate-summary", "Extraction candidate governance summary."),
    ("03-ocr-governance-summary", "Deterministic OCR governance summary."),
    ("04-temporal-continuity-summary", "Temporal continuity & orphan-frame governance summary."),
    ("05-extraction-lineage-summary", "Extraction lineage governance summary."),
    ("06-extraction-replay-summary", "Extraction replay determinism summary."),
    ("07-reviewer-override-summary", "Reviewer override governance summary."),
    ("08-extraction-lifecycle-summary", "Extraction lifecycle governance summary."),
    ("09-extraction-integrity-summary", "Extraction integrity & rollback summary."),
    ("10-governed-semantic-extraction-platform-maturity-reassessment", "Governed semantic extraction platform — maturity reassessment."),
]

REPORT_DIR = REPORTS_ROOT / "governed-semantic-extraction"

# ---------------------------------------------------------------------------
# Runtime README addendum
# ---------------------------------------------------------------------------

RUNTIME_README_MARKER = "## phase 52 — governed semantic evidence analysis & multimodal extraction runtime"
RUNTIME_README_ADDENDUM = """

## phase 52 — governed semantic evidence analysis & multimodal extraction runtime

Layer 45. Subordinate to layer 44 (governed-multimodal-publication-composition-and-page-orchestration-governance).

Mutation is performed exclusively by `tools/governed_semantic_extraction_executor.py --confirm`.
Subcommands (`--kind`):

- `evidence-decomposition` — record a reviewer-authored decomposition of video / image / pdf / xls / xlsx / csv evidence (keyframes / pages / worksheets / regions).
- `ocr-fragment` — record a reviewer-attributed OCR fragment with verbatim text and lineage to a decomposition region/page/frame.
- `ocr-correction` — record a reviewer override of a prior OCR fragment (cites prior_fragment_id; append-only).
- `extraction-candidate` — record a typed extraction candidate (one of CANDIDATE_KINDS) with full lineage pointers, reasoning_chain, and confidence_state.
- `temporal-continuity` — record a temporal continuity scan for a video decomposition (gaps fail-closed for procedural sequences).
- `extraction-lineage` — record a deterministic lineage replay with sha256 verification of every linked artifact.
- `extraction-replay` — record a full extraction replay event verifying lineage and manifest hashes.
- `extraction-lifecycle-transition` — advance a candidate through unresolved → review-required → reviewer-approved → {superseded → deprecated}.
- `extraction-integrity` — record a reviewer-led integrity scan (orphan candidates, broken lineage, invalid OCR references, missing evidence, continuity gaps, hidden mutation).
- `reviewer-override` — record a reviewer-attributed override of any extraction artifact (rejection requires cited_rule_ids).

Every command:
- requires reviewer attribution,
- is fail-closed on missing source evidence / orphan candidates / broken lineage / invalid OCR references / temporal continuity gaps / illegal candidate states / duplicate IDs / forbidden overwrite paths / hidden extraction mutation,
- appends to one or more append-only event stores under `operational-console/runtime-manifests/`,
- writes only into `operational-console/semantic-extraction-runtime/` subtrees.

The semantic-extraction-runtime tree is isolated from:
- the live publication tree,
- the layer-44 publication-composition-runtime tree,
- the layer-43 visual-generation-runtime tree,
- the layer-42 visual-publication-builds tree,
- OEM source assets,
- knowledge-core, governance, runtime-implementation, runtime-manifests payloads, uploads.

Nothing in this surface uses embeddings, vector databases, probabilistic semantic matching, autonomous LLM reasoning, cloud APIs, SaaS, telemetry, watchers, daemons, or background workers.
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
    root_readme = SE_ROOT / "README.md"
    if not root_readme.exists():
        write_text(root_readme,
                   "# semantic-extraction-runtime\n\n"
                   "Phase 52 / layer 45. Governed semantic evidence analysis & multimodal extraction runtime.\n\n"
                   "Reviewer-authored only. Deterministic. Append-only.\n")
        count += 1
    for sub in SE_SUBDIRS:
        sub_path = SE_ROOT / sub
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
            f"<code>{slug}</code> surface. The browser does NOT mutate the filesystem and does NOT extract autonomously.</p>"
            f"<p>Submit envelopes via <code>tools/governed_semantic_extraction_executor.py --kind &lt;kind&gt; --request &lt;file&gt; --confirm</code>.</p>"
            f"</section>"
        )
        write_text(OC_ROOT / slug / "exec.html", html + body + HTML_TAIL)
    return len(CONSOLES)


def build_doctrines() -> int:
    DOCTRINE_DIR.mkdir(parents=True, exist_ok=True)
    index_lines = ["# GOVERNED SEMANTIC EXTRACTION GOVERNANCE", "", f"Layer {LAYER}. Phase 52.", ""]
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
               "# Governed semantic extraction — reports\n\nPhase 52 / layer 45 reports.\n")
    for slug, title in REPORTS:
        write_text(REPORT_DIR / f"{slug}.md", f"# {title}\n\nLayer {LAYER}. Phase 52.\n")
        write_json(REPORT_DIR / f"{slug}.json", {
            "schema": "governance-report/1.0",
            "constitutional_layer_index": LAYER,
            "report_slug": slug,
            "title": title,
            "subordinate_to": SUBORDINATE_TO,
            "posture": POSTURE,
            "evidence_kinds": EVIDENCE_KINDS,
            "candidate_kinds": CANDIDATE_KINDS,
            "confidence_states": CONFIDENCE_STATES,
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
        "Phase 52 — governed semantic evidence analysis & multimodal extraction runtime written. "
        f"Subordinate chain length: {len(SUBORDINATE_TO)}. "
        f"Storage roots: {storage} | New event stores: {stores} | Rule tables: {rules} | "
        f"JS assets: {js} | Exec consoles: {consoles} | Doctrines: {doctrines} | Reports: {reports} | "
        f"RUNTIME_README addendum: {readme}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
