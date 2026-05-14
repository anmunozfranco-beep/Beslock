// phase 53 — semantic section engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var SS = OC.SemanticSection = OC.SemanticSection || {};
  SS.KINDS = ['semantic-section','semantic-procedure','semantic-warning-group','semantic-specification-group','semantic-troubleshooting-group','semantic-support-group'];
  SS.buildSectionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('SS-1: reviewer required');
    if (!input.manual_id || !input.section_id) throw new Error('SS-1: manual_id and section_id required');
    if (SS.KINDS.indexOf(input.section_kind) < 0) throw new Error('SS-2: invalid section_kind');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'semantic-section',
      reviewer: input.reviewer,
      payload: {
        section_id: input.section_id,
        manual_id: input.manual_id,
        section_kind: input.section_kind,
        title: input.title || '',
        extraction_ids: input.extraction_ids || [],
        grounding_ids: input.grounding_ids || [],
        evidence_refs: input.evidence_refs || [],
        body_blocks: input.body_blocks || [],
        unresolved_states: input.unresolved_states || [],
        trust_composition: input.trust_composition || {'reviewer-approved':0,'review-required':0,'unresolved':0}
      }
    });
  };
})(window);
