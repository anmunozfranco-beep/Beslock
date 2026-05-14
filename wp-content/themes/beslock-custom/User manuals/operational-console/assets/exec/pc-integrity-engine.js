// phase 51 — composition integrity engine (reviewer-driven).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var IN = OC.CompositionIntegrity = OC.CompositionIntegrity || {};
  IN.buildIntegrityRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('reviewer required');
    if (!input.composition_id) throw new Error('composition_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'composition-integrity',
      reviewer: input.reviewer,
      payload: {
        integrity_check_id: input.integrity_check_id || null,
        composition_id: input.composition_id,
        scope: input.scope || 'all'
      }
    });
  };
})(window);
