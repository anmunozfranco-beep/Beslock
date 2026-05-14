// phase 47/48 — operational-console exec engine.
// Browser-only. NEVER mutates the filesystem. Emits only governed-fs-operation-request envelopes.

window.OC = window.OC || {};
window.OC.TroubleshootingSynthesisEngine = (function () {
  function buildFlowRequest({ synthesis_id, canonical_product_id, symptoms, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("troubleshooting synthesis requires reviewer attribution");
    var steps = (symptoms || []).map(function (s, i) {
      return {
        step_id: "ts-" + i,
        symptom: s.symptom,
        evidence_ids: (s.evidence_ids || []).slice(),
        candidate_root_causes: (s.candidate_root_causes || []).slice(),
        confidence_state: s.confidence_state || "review-required",
        unresolved: !!s.unresolved,
      };
    });
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "troubleshooting-synthesis",
      reviewer: reviewer,
      payload: {
        flow_id: "ts-" + canonical_product_id + "-" + Date.now(),
        synthesis_id: synthesis_id,
        canonical_product_id: canonical_product_id,
        steps: steps,
      },
    });
  }
  return { buildFlowRequest: buildFlowRequest };
})();
