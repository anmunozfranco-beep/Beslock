// phase 52 — extraction integrity engine (reviewer-driven).
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
