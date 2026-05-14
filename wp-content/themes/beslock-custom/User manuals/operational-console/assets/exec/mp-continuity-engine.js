// phase 53 — packaging continuity engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PC = OC.PackagingContinuity = OC.PackagingContinuity || {};
  PC.buildContinuityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PC-1: reviewer required');
    if (!input.manual_id || !input.package_id) throw new Error('PC-1: manual_id and package_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'packaging-continuity',
      reviewer: input.reviewer,
      payload: {
        continuity_check_id: input.continuity_check_id || null,
        manual_id: input.manual_id,
        package_id: input.package_id
      }
    });
  };
})(window);
