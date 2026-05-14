// phase 50 — visual supersedence engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var SP = OC.Supersedence = OC.Supersedence || {};
  SP.buildSupersedenceRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    if (!input.predecessor_asset_id) throw new Error('SP-1: predecessor_asset_id required');
    if (!input.successor_asset_id) throw new Error('SP-1: successor_asset_id required');
    if (input.predecessor_asset_id === input.successor_asset_id) throw new Error('SP-7: predecessor must differ from successor');
    if (!input.reason) throw new Error('SP-1: reason required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'visual-supersedence',
      reviewer: input.reviewer,
      payload: {
        supersedence_id: input.supersedence_id || null,
        predecessor_asset_id: input.predecessor_asset_id,
        successor_asset_id: input.successor_asset_id,
        reason: input.reason,
        grounding_shift: !!input.grounding_shift,
        oem_to_generated_attestation: input.oem_to_generated_attestation || null
      }
    });
  };
})(window);
