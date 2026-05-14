// phase 49 — visual asset lifecycle engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var VL = OC.VisualLifecycle = OC.VisualLifecycle || {};
  VL.STATES = ['candidate','grounded','review-required','reviewer-approved','publication-ready','superseded','deprecated'];
  VL.EDGES = [
    ['candidate','grounded'], ['grounded','review-required'],
    ['review-required','reviewer-approved'], ['review-required','candidate'],
    ['reviewer-approved','publication-ready'], ['reviewer-approved','review-required'],
    ['publication-ready','superseded'], ['publication-ready','deprecated'],
    ['superseded','deprecated']
  ];
  VL.isLegal = function (from, to) {
    for (var i = 0; i < VL.EDGES.length; i++) if (VL.EDGES[i][0] === from && VL.EDGES[i][1] === to) return true;
    return false;
  };
  VL.buildTransitionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.image_id) throw new Error('image_id required');
    if (!VL.isLegal(input.from_state, input.to_state)) throw new Error('VL: illegal transition ' + input.from_state + ' -> ' + input.to_state);
    if (!input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'visual-asset-lifecycle-transition',
      reviewer: input.reviewer,
      payload: {
        image_id: input.image_id,
        from_state: input.from_state,
        to_state: input.to_state,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
