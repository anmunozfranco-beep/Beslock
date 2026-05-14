// phase 52 — evidence decomposition engine (reviewer-authored, deterministic).
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
