// phase 47/48 — operational-console exec engine.
// Browser-only. NEVER mutates the filesystem. Emits only governed-fs-operation-request envelopes.

window.OC = window.OC || {};
window.OC.SpecificationSynthesisEngine = (function () {
  var AXES = ["dimensional","connectivity","authentication","certification","operational-limits","power"];
  function buildSpecRequest({ synthesis_id, canonical_product_id, fields, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("specification synthesis requires reviewer attribution");
    var normalized = (fields || []).map(function (f) {
      return {
        axis: f.axis,
        key: f.key,
        value: f.value,
        evidence_id: f.evidence_id || null,
        trust_tier: f.trust_tier || null,
        unresolved: f.value === undefined || f.value === null || f.value === "",
      };
    });
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "specification-synthesis",
      reviewer: reviewer,
      payload: {
        spec_id: "spec-" + canonical_product_id + "-" + Date.now(),
        synthesis_id: synthesis_id,
        canonical_product_id: canonical_product_id,
        fields: normalized,
      },
    });
  }
  return { AXES: AXES, buildSpecRequest: buildSpecRequest };
})();
