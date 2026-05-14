// phase 50 — review comparison engine (reviewer-scored ONLY).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var RC = OC.ReviewComparison = OC.ReviewComparison || {};
  RC.VERDICTS = ['prefer','acceptable','reject','defer'];
  RC.buildComparisonRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    if (!Array.isArray(input.entries) || input.entries.length < 2) throw new Error('RC-1: at least two entries required');
    for (var i = 0; i < input.entries.length; i++) {
      var e = input.entries[i];
      if (!e.asset_id) throw new Error('RC-1: entry ' + i + ' missing asset_id');
      if (RC.VERDICTS.indexOf(e.verdict) < 0) throw new Error('RC-3: entry ' + i + ' invalid verdict');
    }
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'review-comparison',
      reviewer: input.reviewer,
      payload: {
        comparison_id: input.comparison_id || null,
        comparison_dimension: input.comparison_dimension || 'overall',
        group_id: input.group_id || null,
        prior_comparison_id: input.prior_comparison_id || null,
        entries: input.entries
      }
    });
  };
})(window);
