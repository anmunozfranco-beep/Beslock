// phase 51 — page continuity engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var CN = OC.PageContinuity = OC.PageContinuity || {};
  CN.buildContinuityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PC-1: reviewer required');
    if (!input.composition_id) throw new Error('PC-1: composition_id required');
    if (!Array.isArray(input.page_indices)) throw new Error('PC-1: page_indices required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'page-continuity',
      reviewer: input.reviewer,
      payload: {
        continuity_check_id: input.continuity_check_id || null,
        composition_id: input.composition_id,
        page_indices: input.page_indices,
        section_ids_present: input.section_ids_present || [],
        orphan_section_ids: input.orphan_section_ids || [],
        orphan_asset_ids: input.orphan_asset_ids || []
      }
    });
  };
})(window);
