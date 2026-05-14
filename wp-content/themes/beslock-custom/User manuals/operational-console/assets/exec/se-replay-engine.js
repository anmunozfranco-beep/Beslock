// phase 52 — extraction replay engine.
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
