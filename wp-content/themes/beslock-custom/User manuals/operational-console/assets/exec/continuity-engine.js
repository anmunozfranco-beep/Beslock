// phase 49 — procedural image continuity engine (deterministic gap detection).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PC = OC.Continuity = OC.Continuity || {};
  PC.detectGaps = function (steps) {
    // steps: [{step_index, image_id?}] sorted ascending; returns missing indices.
    if (!Array.isArray(steps) || !steps.length) return [];
    var gaps = [];
    var max = 0; var i;
    for (i = 0; i < steps.length; i++) if (steps[i].step_index > max) max = steps[i].step_index;
    var present = {};
    for (i = 0; i < steps.length; i++) if (steps[i].image_id) present[steps[i].step_index] = true;
    for (i = 1; i <= max; i++) if (!present[i]) gaps.push(i);
    return gaps;
  };
  PC.buildContinuityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.publication_build_id) throw new Error('publication_build_id required');
    if (!input.reviewer) throw new Error('reviewer required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'procedural-continuity',
      reviewer: input.reviewer,
      payload: {
        publication_build_id: input.publication_build_id,
        steps: input.steps || [],
        orphan_image_ids: input.orphan_image_ids || [],
        broken_lineage_image_ids: input.broken_lineage_image_ids || [],
        reviewer_accepted_gaps: input.reviewer_accepted_gaps || []
      }
    });
  };
})(window);
