// phase 52 — reviewer override engine.
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
