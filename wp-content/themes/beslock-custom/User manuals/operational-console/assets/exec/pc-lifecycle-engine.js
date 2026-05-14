// phase 51 — composition lifecycle engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var LC = OC.CompositionLifecycle = OC.CompositionLifecycle || {};
  LC.STATES = ['draft','composed','review-required','reviewer-approved','publication-ready','superseded','deprecated'];
  LC.EDGES = [
    ['draft','composed'],
    ['composed','review-required'], ['composed','draft'],
    ['review-required','reviewer-approved'], ['review-required','composed'],
    ['reviewer-approved','publication-ready'], ['reviewer-approved','review-required'],
    ['publication-ready','superseded'], ['publication-ready','deprecated'],
    ['superseded','deprecated']
  ];
  LC.isLegal = function (from, to) {
    for (var i = 0; i < LC.EDGES.length; i++) if (LC.EDGES[i][0] === from && LC.EDGES[i][1] === to) return true;
    return false;
  };
  LC.buildTransitionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('LC-1: reviewer required');
    if (!input.composition_id) throw new Error('composition_id required');
    if (!LC.isLegal(input.from_state, input.to_state)) throw new Error('LC: illegal transition ' + input.from_state + ' -> ' + input.to_state);
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'composition-lifecycle-transition',
      reviewer: input.reviewer,
      payload: {
        composition_id: input.composition_id,
        from_state: input.from_state,
        to_state: input.to_state,
        successor_composition_id: input.successor_composition_id || null,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
