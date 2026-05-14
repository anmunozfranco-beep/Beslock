// phase 51 — publication composition engine (reviewer-authored, deterministic).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PC = OC.PublicationComposition = OC.PublicationComposition || {};
  PC.MANUAL_KINDS = ['procedural','troubleshooting','specification-heavy','comparison','warning-centric','multimodal-responsive','oem-derived','generated-visual'];
  PC.buildCompositionDraftRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('CP-1: reviewer required');
    if (!input.synthesis_id) throw new Error('CP-2: synthesis_id required');
    if (!Array.isArray(input.section_order) || input.section_order.length === 0) throw new Error('CP-2: section_order required');
    if (PC.MANUAL_KINDS.indexOf(input.manual_kind) < 0) throw new Error('CP-6: invalid manual_kind');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'composition-draft',
      reviewer: input.reviewer,
      payload: {
        composition_id: input.composition_id || null,
        synthesis_id: input.synthesis_id,
        manual_id: input.manual_id || null,
        manual_kind: input.manual_kind,
        canonical_product_id: input.canonical_product_id || null,
        section_order: input.section_order,
        rationale: input.rationale || ''
      }
    });
  };
})(window);
