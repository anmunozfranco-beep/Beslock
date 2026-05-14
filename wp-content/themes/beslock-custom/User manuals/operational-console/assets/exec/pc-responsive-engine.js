// phase 51 — responsive render engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var RR = OC.ResponsiveRender = OC.ResponsiveRender || {};
  RR.BREAKPOINTS = ['mobile','tablet','desktop','print'];
  RR.buildResponsiveLayoutRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('RR-1: reviewer required');
    if (!input.composition_id) throw new Error('RR-1: composition_id required');
    if (!input.parity || typeof input.parity !== 'object') throw new Error('RR-1: parity object required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'responsive-layout',
      reviewer: input.reviewer,
      payload: {
        responsive_layout_id: input.responsive_layout_id || null,
        composition_id: input.composition_id,
        page_layout_id: input.page_layout_id || null,
        parity: input.parity,
        omissions: input.omissions || []
      }
    });
  };
})(window);
