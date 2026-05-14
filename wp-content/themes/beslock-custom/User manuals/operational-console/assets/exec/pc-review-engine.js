// phase 51 — layout review engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var LR = OC.LayoutReview = OC.LayoutReview || {};
  LR.DECISIONS = ['approve','request-changes','reject'];
  LR.buildReviewRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('LR-1: reviewer required');
    if (!input.composition_id) throw new Error('LR-1: composition_id required');
    if (LR.DECISIONS.indexOf(input.decision) < 0) throw new Error('LR-1: invalid decision');
    if (input.decision === 'reject' && (!Array.isArray(input.cited_rule_ids) || input.cited_rule_ids.length === 0)) {
      throw new Error('LR-4: reject requires cited_rule_ids');
    }
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'layout-review',
      reviewer: input.reviewer,
      payload: {
        review_id: input.review_id || null,
        composition_id: input.composition_id,
        page_index: input.page_index || 'all',
        decision: input.decision,
        cited_rule_ids: input.cited_rule_ids || [],
        prior_decision_id: input.prior_decision_id || null,
        rationale: input.rationale || ''
      }
    });
  };
})(window);
