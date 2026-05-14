// phase 50 — visual generation request engine (reviewer-authored, NO autonomous gen).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var VG = OC.VisualGeneration = OC.VisualGeneration || {};
  VG.ASSET_KINDS = ['generated','oem','edited','supportive','procedural-sequence','troubleshooting','specification'];
  VG.buildGenerationRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('GR-1: reviewer required');
    if (!input.grounding_id) throw new Error('GR-2: grounding_id required');
    if (!input.prompt_id) throw new Error('GR-2: prompt_id required');
    if (!input.synthesis_id) throw new Error('GR-2: synthesis_id required');
    if (!input.canonical_product_id) throw new Error('GR-2: canonical_product_id required');
    if (VG.ASSET_KINDS.indexOf(input.asset_kind) < 0) throw new Error('GR-7: invalid asset_kind');
    var n = parseInt(input.variant_count, 10);
    if (!(n >= 1)) throw new Error('GR-6: variant_count must be >= 1');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'generation-request',
      reviewer: input.reviewer,
      payload: {
        generation_request_id: input.generation_request_id || null,
        session_id: input.session_id || null,
        grounding_id: input.grounding_id,
        prompt_id: input.prompt_id,
        prompt_revision_id: input.prompt_revision_id || null,
        synthesis_id: input.synthesis_id,
        canonical_product_id: input.canonical_product_id,
        asset_kind: input.asset_kind,
        variant_count: n,
        constraints: input.constraints || [],
        rationale: input.rationale || ''
      }
    });
  };
})(window);
