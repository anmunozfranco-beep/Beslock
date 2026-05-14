// phase 53 — reviewer packaging override engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PRO = OC.ReviewerPackagingOverride = OC.ReviewerPackagingOverride || {};
  PRO.KINDS = ['approve','reject','supersede','annotate'];
  PRO.buildOverrideRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PRO-1: reviewer required');
    if (!input.target_artifact_id) throw new Error('PRO-1: target_artifact_id required');
    if (input.kind === 'reject' && (!Array.isArray(input.cited_rule_ids) || input.cited_rule_ids.length === 0)) {
      throw new Error('PRO-3: reject requires cited_rule_ids');
    }
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'reviewer-packaging-override',
      reviewer: input.reviewer,
      payload: {
        override_id: input.override_id || null,
        target_artifact_id: input.target_artifact_id,
        target_kind: input.target_kind || 'package',
        kind: input.kind || 'reject',
        cited_rule_ids: input.cited_rule_ids || [],
        rationale: input.rationale || ''
      }
    });
  };
})(window);
