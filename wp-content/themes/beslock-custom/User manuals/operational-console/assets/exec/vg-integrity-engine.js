// phase 50 — visual integrity engine (reviewer-driven verification; no ML).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var IN = OC.VisualIntegrity = OC.VisualIntegrity || {};
  IN.buildIntegrityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'visual-integrity',
      reviewer: input.reviewer,
      payload: {
        integrity_check_id: input.integrity_check_id || null,
        scope: input.scope || 'all',
        target_asset_ids: input.target_asset_ids || []
      }
    });
  };
})(window);
