// phase 50 — visual asset production lifecycle engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var LC = OC.AssetLifecycle = OC.AssetLifecycle || {};
  LC.STATES = ['candidate','review-required','reviewer-approved','publication-selected','superseded','deprecated','rejected'];
  LC.EDGES = [
    ['candidate','review-required'], ['candidate','rejected'],
    ['review-required','reviewer-approved'], ['review-required','rejected'], ['review-required','candidate'],
    ['reviewer-approved','publication-selected'], ['reviewer-approved','review-required'],
    ['publication-selected','superseded'], ['publication-selected','deprecated'],
    ['superseded','deprecated']
  ];
  LC.isLegal = function (from, to) {
    for (var i = 0; i < LC.EDGES.length; i++) if (LC.EDGES[i][0] === from && LC.EDGES[i][1] === to) return true;
    return false;
  };
  LC.buildTransitionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('LC-1: reviewer required');
    if (!input.asset_id) throw new Error('asset_id required');
    if (!LC.isLegal(input.from_state, input.to_state)) throw new Error('LC: illegal transition ' + input.from_state + ' -> ' + input.to_state);
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'asset-lifecycle-transition',
      reviewer: input.reviewer,
      payload: {
        asset_id: input.asset_id,
        from_state: input.from_state,
        to_state: input.to_state,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
