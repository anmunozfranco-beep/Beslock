// phase 53 — manual package engine (reviewer-authored, deterministic, presentation-neutral).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var MP = OC.ManualPackage = OC.ManualPackage || {};
  MP.buildPackageRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('MP-1: reviewer required');
    if (!input.manual_id || !input.canonical_product_id || !input.package_version) {
      throw new Error('MP-1: manual_id, canonical_product_id, package_version required');
    }
    if (!Array.isArray(input.semantic_structure)) throw new Error('MP-1: semantic_structure required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'manual-package',
      reviewer: input.reviewer,
      payload: {
        package_id: input.package_id || null,
        manual_id: input.manual_id,
        canonical_product_id: input.canonical_product_id,
        package_version: input.package_version,
        synthesis_ids: input.synthesis_ids || [],
        extraction_ids: input.extraction_ids || [],
        grounding_ids: input.grounding_ids || [],
        evidence_refs: input.evidence_refs || [],
        semantic_structure: input.semantic_structure,
        continuity_status: input.continuity_status || 'unresolved',
        reasoning_chain: input.reasoning_chain || [],
        prior_package_id: input.prior_package_id || null
      }
    });
  };
})(window);
