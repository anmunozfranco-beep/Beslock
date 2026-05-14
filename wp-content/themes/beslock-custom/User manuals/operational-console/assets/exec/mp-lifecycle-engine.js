// phase 53 — packaging lifecycle engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PXL = OC.PackagingLifecycle = OC.PackagingLifecycle || {};
  PXL.STATES = ['draft','review-required','reviewer-approved','export-ready','superseded','deprecated'];
  PXL.EDGES = [
    ['draft','review-required'], ['draft','deprecated'],
    ['review-required','reviewer-approved'], ['review-required','draft'], ['review-required','deprecated'],
    ['reviewer-approved','export-ready'], ['reviewer-approved','review-required'], ['reviewer-approved','superseded'],
    ['export-ready','reviewer-approved'], ['export-ready','superseded'],
    ['superseded','deprecated']
  ];
  PXL.isLegal = function (from, to) {
    for (var i = 0; i < PXL.EDGES.length; i++) if (PXL.EDGES[i][0] === from && PXL.EDGES[i][1] === to) return true;
    return false;
  };
  PXL.buildTransitionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PXL-1: reviewer required');
    if (!input.package_id) throw new Error('package_id required');
    if (!PXL.isLegal(input.from_state, input.to_state)) throw new Error('PXL: illegal transition ' + input.from_state + ' -> ' + input.to_state);
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'packaging-lifecycle-transition',
      reviewer: input.reviewer,
      payload: {
        package_id: input.package_id,
        from_state: input.from_state,
        to_state: input.to_state,
        successor_package_id: input.successor_package_id || null,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
