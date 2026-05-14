// phase 47/48 — operational-console exec engine.
// Browser-only. NEVER mutates the filesystem. Emits only governed-fs-operation-request envelopes.

window.OC = window.OC || {};
window.OC.PublicationLifecycleEngine = (function () {
  var STATES = ["draft","synthesized","review-required","reviewer-approved",
                "publication-ready","superseded","deprecated"];
  var EDGES = [["draft","synthesized"],["synthesized","review-required"],
               ["review-required","reviewer-approved"],["review-required","draft"],
               ["reviewer-approved","publication-ready"],["reviewer-approved","review-required"],
               ["publication-ready","superseded"],["publication-ready","deprecated"],
               ["superseded","deprecated"]];
  function isLegal(from, to) {
    return EDGES.some(function (e) { return e[0] === from && e[1] === to; });
  }
  function buildTransitionRequest({ build_id, from_state, to_state, reviewer, reasoning_chain }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("transition requires reviewer attribution");
    if (!isLegal(from_state, to_state))
      throw new Error("PL: illegal transition " + from_state + " -> " + to_state);
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "publication-lifecycle-transition",
      reviewer: reviewer,
      payload: {
        transition_id: "plt-" + build_id + "-" + Date.now(),
        build_id: build_id,
        from_state: from_state,
        to_state: to_state,
        reasoning_chain: reasoning_chain || [],
      },
    });
  }
  return { STATES: STATES, isLegal: isLegal, buildTransitionRequest: buildTransitionRequest };
})();
