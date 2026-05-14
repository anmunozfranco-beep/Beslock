// phase 49 — supportive-image matrix engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var SI = OC.SupportiveImage = OC.SupportiveImage || {};
  SI.ROLES = ['contextual','procedural','warning','troubleshooting','specification','orientation','escalation-support','comparison-support'];
  SI.buildMappingRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.image_id) throw new Error('image_id required');
    if (SI.ROLES.indexOf(input.role) < 0) throw new Error('SI-1: invalid role');
    if (!input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'supportive-image-mapping',
      reviewer: input.reviewer,
      payload: {
        image_id: input.image_id,
        role: input.role,
        applies_to_sections: input.applies_to_sections || [],
        canonical_product_ids: input.canonical_product_ids || [],
        evidence_ids: input.evidence_ids || []
      }
    });
  };
})(window);
