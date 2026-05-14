// phase 49 — multimodal grounding engine (deterministic, reviewer-driven, NO ML).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var Grounding = OC.Grounding = OC.Grounding || {};
  Grounding.KINDS = ['procedural-step','troubleshooting-flow','specification-field','warning','installation-sequence','operational-state'];
  Grounding.CONFIDENCE = ['reviewer-approved','review-required','unresolved'];
  Grounding.buildGroundingRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.image_ids || !input.image_ids.length) throw new Error('GR-1: image_ids required');
    if (!input.grounded_target_id) throw new Error('GR-1: grounded_target_id required');
    if (!input.grounding_kind || Grounding.KINDS.indexOf(input.grounding_kind) < 0) throw new Error('GR-2: invalid grounding_kind');
    if (!input.synthesis_id) throw new Error('GR-7: synthesis_id required');
    if (!input.reviewer) throw new Error('GR-9: reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'grounding',
      reviewer: input.reviewer,
      payload: {
        grounding_id: input.grounding_id || null,
        synthesis_id: input.synthesis_id,
        canonical_product_id: input.canonical_product_id || null,
        grounding_kind: input.grounding_kind,
        grounded_target_id: input.grounded_target_id,
        image_ids: input.image_ids,
        evidence_ids: input.evidence_ids || [],
        rationale: input.rationale || '',
        confidence_state: input.confidence_state || 'review-required',
        prior_grounding_id: input.prior_grounding_id || null
      }
    });
  };
})(window);
