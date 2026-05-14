// phase 49 — visual publication orchestration engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var VP = OC.VisualPublication = OC.VisualPublication || {};
  VP.buildVisualPublicationRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.synthesis_id) throw new Error('VP-6: synthesis_id required');
    if (!input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'visual-publication-build',
      reviewer: input.reviewer,
      payload: {
        build_id: input.build_id || null,
        manual_id: input.manual_id || 'manual',
        synthesis_id: input.synthesis_id,
        canonical_product_id: input.canonical_product_id || null,
        placements: input.placements || [],
        output_formats: input.output_formats || ['html','json']
      }
    });
  };
})(window);
