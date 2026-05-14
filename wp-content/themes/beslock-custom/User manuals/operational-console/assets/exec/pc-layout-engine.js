// phase 51 — page layout engine (deterministic block list).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var LO = OC.PageLayout = OC.PageLayout || {};
  LO.SECTION_ROLES = ['overview','warning','specification','procedural','troubleshooting','comparison','evidence-trace','appendix'];
  LO.buildPageLayoutRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('LO-1: reviewer required');
    if (!input.composition_id) throw new Error('LO-1: composition_id required');
    if (typeof input.page_index !== 'number' || input.page_index < 1) throw new Error('LO-1: page_index must be >= 1');
    if (!Array.isArray(input.blocks) || input.blocks.length === 0) throw new Error('LO-2: blocks required');
    for (var i = 0; i < input.blocks.length; i++) {
      var b = input.blocks[i];
      if (!b.block_id) throw new Error('LO-2: block ' + i + ' missing block_id');
      if (LO.SECTION_ROLES.indexOf(b.role) < 0) throw new Error('LO-2: block ' + i + ' invalid role');
    }
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'page-layout',
      reviewer: input.reviewer,
      payload: {
        page_layout_id: input.page_layout_id || null,
        composition_id: input.composition_id,
        page_index: input.page_index,
        section_id: input.section_id || null,
        continuation_of: input.continuation_of || null,
        blocks: input.blocks,
        max_visuals_per_page: input.max_visuals_per_page || 6
      }
    });
  };
})(window);
