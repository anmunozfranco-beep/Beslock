// phase 53 — packaging integrity engine (reviewer-driven).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PI = OC.PackagingIntegrity = OC.PackagingIntegrity || {};
  PI.buildIntegrityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'packaging-integrity',
      reviewer: input.reviewer,
      payload: {
        integrity_check_id: input.integrity_check_id || null,
        manual_id: input.manual_id || null,
        package_id: input.package_id || null,
        scope: input.scope || 'all'
      }
    });
  };
})(window);
