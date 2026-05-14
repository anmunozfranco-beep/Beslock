// phase 53 — packaging lineage engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PL = OC.PackagingLineage = OC.PackagingLineage || {};
  PL.buildLineageRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PL-1: reviewer required');
    if (!input.package_id) throw new Error('PL-1: package_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'packaging-lineage',
      reviewer: input.reviewer,
      payload: {
        lineage_id: input.lineage_id || null,
        package_id: input.package_id,
        scope: input.scope || 'package'
      }
    });
  };
})(window);
