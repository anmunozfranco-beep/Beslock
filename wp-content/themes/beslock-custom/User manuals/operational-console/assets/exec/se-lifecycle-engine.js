// phase 52 — extraction lifecycle engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var XL = OC.ExtractionLifecycle = OC.ExtractionLifecycle || {};
  XL.STATES = ['unresolved','review-required','reviewer-approved','superseded','deprecated'];
  XL.EDGES = [
    ['unresolved','review-required'], ['unresolved','deprecated'],
    ['review-required','reviewer-approved'], ['review-required','unresolved'], ['review-required','deprecated'],
    ['reviewer-approved','review-required'], ['reviewer-approved','superseded'],
    ['superseded','deprecated']
  ];
  XL.isLegal = function (from, to) {
    for (var i = 0; i < XL.EDGES.length; i++) if (XL.EDGES[i][0] === from && XL.EDGES[i][1] === to) return true;
    return false;
  };
  XL.buildTransitionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('XL-1: reviewer required');
    if (!input.candidate_id) throw new Error('candidate_id required');
    if (!XL.isLegal(input.from_state, input.to_state)) throw new Error('XL: illegal transition ' + input.from_state + ' -> ' + input.to_state);
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'extraction-lifecycle-transition',
      reviewer: input.reviewer,
      payload: {
        candidate_id: input.candidate_id,
        from_state: input.from_state,
        to_state: input.to_state,
        successor_candidate_id: input.successor_candidate_id || null,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
