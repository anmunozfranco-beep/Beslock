// phase 51 — publication assembly engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PA = OC.PublicationAssembly = OC.PublicationAssembly || {};
  PA.buildAssemblyRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PA-1: reviewer required');
    if (!input.composition_id) throw new Error('PA-1: composition_id required');
    if (!Array.isArray(input.page_layout_ids) || input.page_layout_ids.length === 0) throw new Error('PA-1: page_layout_ids required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'publication-assembly',
      reviewer: input.reviewer,
      payload: {
        assembly_id: input.assembly_id || null,
        composition_id: input.composition_id,
        page_layout_ids: input.page_layout_ids,
        prior_assembly_id: input.prior_assembly_id || null
      }
    });
  };
})(window);
