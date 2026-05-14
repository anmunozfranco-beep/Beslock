// phase 47/48 — operational-console exec engine.
// Browser-only. NEVER mutates the filesystem. Emits only governed-fs-operation-request envelopes.

window.OC = window.OC || {};
window.OC.EvidenceResolutionEngine = (function () {
  var CLASSES = ["trust-tier-mismatch","specification-divergence","warning-divergence",
                 "procedure-divergence","terminology-divergence","identity-divergence",
                 "evidence-recency-divergence","scope-overlap-divergence"];
  function detectConflict(fragmentA, fragmentB) {
    if (!fragmentA || !fragmentB) return null;
    if (fragmentA.canonical_product_id && fragmentB.canonical_product_id &&
        fragmentA.canonical_product_id !== fragmentB.canonical_product_id)
      return { conflict_class: "identity-divergence", a: fragmentA.id, b: fragmentB.id };
    if (fragmentA.field === fragmentB.field && fragmentA.value !== fragmentB.value) {
      if ((fragmentA.trust_tier || "") === (fragmentB.trust_tier || ""))
        return { conflict_class: "specification-divergence", a: fragmentA.id, b: fragmentB.id,
                 reason: "same trust tier, divergent value" };
      return { conflict_class: "trust-tier-mismatch", a: fragmentA.id, b: fragmentB.id };
    }
    return null;
  }
  function buildResolutionRequest({ synthesis_id, conflicts, strategy, reviewer, reasoning_chain }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("resolution requires reviewer attribution");
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "evidence-resolve",
      reviewer: reviewer,
      payload: {
        resolution_id: "res-" + synthesis_id + "-" + Date.now(),
        synthesis_id: synthesis_id,
        conflicts: (conflicts || []).slice(),
        strategy: strategy || "reviewer-arbitration",
        reasoning_chain: reasoning_chain || [],
      },
    });
  }
  return { detectConflict: detectConflict, buildResolutionRequest: buildResolutionRequest, CLASSES: CLASSES };
})();
