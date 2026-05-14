// phase 50 — publication visual selection engine (reviewer-attributed, fail-closed).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var SL = OC.VisualSelection = OC.VisualSelection || {};
  SL.buildSelectionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('SL-4: reviewer required');
    if (!input.asset_id) throw new Error('SL-1: asset_id required');
    if (!input.visual_publication_build_id) throw new Error('SL-2: visual_publication_build_id required');
    if (!input.placement_slot_id) throw new Error('SL-2: placement_slot_id required');
    if (!input.grounding_id) throw new Error('SL-3: grounding_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'publication-visual-selection',
      reviewer: input.reviewer,
      payload: {
        selection_id: input.selection_id || null,
        asset_id: input.asset_id,
        visual_publication_build_id: input.visual_publication_build_id,
        placement_slot_id: input.placement_slot_id,
        grounding_id: input.grounding_id,
        prior_selection_id: input.prior_selection_id || null,
        rationale: input.rationale || ''
      }
    });
  };
})(window);
