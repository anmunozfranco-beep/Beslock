// phase 52 — extraction candidate engine.
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
