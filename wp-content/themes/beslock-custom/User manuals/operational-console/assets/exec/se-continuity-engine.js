// phase 52 — temporal continuity engine.
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
