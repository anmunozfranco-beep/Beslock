// phase 50 — generated asset registration engine (reviewer-supplied bytes; sha256 provenance).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var GA = OC.GeneratedAsset = OC.GeneratedAsset || {};
  GA.buildRegistrationRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    if (!input.generation_request_id) throw new Error('VL-2: generation_request_id required');
    if (!input.asset_sha256) throw new Error('VL-3: asset_sha256 required');
    if (!input.source_provenance) throw new Error('VL-2: source_provenance required');
    if (typeof input.variant_index !== 'number') throw new Error('VL-1: variant_index required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'generated-asset-register',
      reviewer: input.reviewer,
      payload: {
        asset_id: input.asset_id || null,
        generation_request_id: input.generation_request_id,
        variant_index: input.variant_index,
        asset_sha256: input.asset_sha256,
        asset_kind: input.asset_kind || 'generated',
        source_provenance: input.source_provenance,
        prompt_revision_id: input.prompt_revision_id || null,
        grounding_id: input.grounding_id || null,
        synthesis_id: input.synthesis_id || null,
        trust_tier: input.trust_tier || null,
        parent_asset_id: input.parent_asset_id || null,
        edit_kind: input.edit_kind || null
      }
    });
  };
})(window);
