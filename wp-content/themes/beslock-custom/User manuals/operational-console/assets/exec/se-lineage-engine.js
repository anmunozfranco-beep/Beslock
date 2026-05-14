// phase 52 — extraction lineage engine.
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
