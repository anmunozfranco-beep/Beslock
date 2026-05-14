// phase 47/48 — operational-console exec engine.
// Browser-only. NEVER mutates the filesystem. Emits only governed-fs-operation-request envelopes.

window.OC = window.OC || {};
window.OC.SynthesisEngine = (function () {
  function buildSynthesisRequest({ canonical_product_id, evidence_ids, contributing_manifests,
                                   trust_composition, reasoning_chain, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!Array.isArray(evidence_ids) || evidence_ids.length === 0)
      throw new Error("SYN-1: at least one evidence_id required");
    if (!reviewer) throw new Error("synthesis requires reviewer attribution");
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "synthesis",
      reviewer: reviewer,
      payload: {
        synthesis_id: "syn-" + canonical_product_id + "-" + Date.now(),
        canonical_product_id: canonical_product_id,
        evidence_ids: evidence_ids.slice(),
        contributing_manifests: (contributing_manifests || []).slice(),
        trust_composition: trust_composition || {},
        reasoning_chain: reasoning_chain || [],
        deterministic: true,
        no_llm: true,
      },
    });
  }
  return { buildSynthesisRequest: buildSynthesisRequest };
})();
