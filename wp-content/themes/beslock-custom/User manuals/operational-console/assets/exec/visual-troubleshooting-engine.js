// phase 49 — visual troubleshooting engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var VT = OC.VisualTroubleshooting = OC.VisualTroubleshooting || {};
  VT.buildBindingRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.flow_id) throw new Error('flow_id required');
    if (!input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'visual-troubleshooting',
      reviewer: input.reviewer,
      payload: {
        flow_id: input.flow_id,
        synthesis_id: input.synthesis_id || null,
        symptom_visuals: input.symptom_visuals || [],
        escalation_visuals: input.escalation_visuals || [],
        warning_visuals: input.warning_visuals || [],
        visual_unresolved: !!input.visual_unresolved
      }
    });
  };
})(window);
