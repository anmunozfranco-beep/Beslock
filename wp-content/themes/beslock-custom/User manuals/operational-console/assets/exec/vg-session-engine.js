// phase 50 — generation session engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var GS = OC.GenerationSession = OC.GenerationSession || {};
  GS.STATES = ['open','frozen','closed','rejected'];
  GS.EDGES = [['open','frozen'],['open','rejected'],['frozen','open'],['frozen','closed'],['frozen','rejected']];
  GS.isLegal = function (from, to) {
    for (var i = 0; i < GS.EDGES.length; i++) if (GS.EDGES[i][0] === from && GS.EDGES[i][1] === to) return true;
    return false;
  };
  GS.buildSessionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('GS-1: reviewer required');
    if (!input.action || ['open','transition'].indexOf(input.action) < 0) throw new Error('action must be open|transition');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'generation-session',
      reviewer: input.reviewer,
      payload: {
        session_id: input.session_id || null,
        action: input.action,
        from_state: input.from_state || null,
        to_state: input.to_state || null,
        canonical_product_id: input.canonical_product_id || null,
        rationale: input.rationale || ''
      }
    });
  };
})(window);
