// phase 51 — multimodal sequence engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var SQ = OC.MultimodalSequence = OC.MultimodalSequence || {};
  SQ.buildSequenceRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('SQ-1: reviewer required');
    if (!input.composition_id) throw new Error('SQ-1: composition_id required');
    if (!Array.isArray(input.steps) || input.steps.length === 0) throw new Error('SQ-1: steps required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'multimodal-sequence',
      reviewer: input.reviewer,
      payload: {
        sequence_id: input.sequence_id || null,
        composition_id: input.composition_id,
        sequence_kind: input.sequence_kind || 'procedural',
        steps: input.steps,
        image_text_ratio_ceiling: input.image_text_ratio_ceiling || null
      }
    });
  };
})(window);
