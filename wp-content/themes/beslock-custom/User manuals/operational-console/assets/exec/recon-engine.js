/* exec/recon-engine.js — reconciliation review helpers. Layer 38. Geometry-only, no ML. */
(function () {
  "use strict";
  let RULES = null;

  function load() {
    return fetch("../execution-engine/reconciliation-review-rules.json")
      .then(function (r) { return r.json(); })
      .then(function (j) { RULES = j; return j; });
  }

  function classifications() {
    return RULES ? RULES.reviewer_classifications.slice() : [];
  }

  function reviewTypes() {
    return RULES ? RULES.review_types.slice() : [];
  }

  function buildDecision(reviewType, payload) {
    const meta = (RULES && RULES.review_types || []).filter(function (r) { return r.id === reviewType; })[0];
    return {
      review_type: reviewType,
      produces: meta ? meta.produces : "reconciliation-decision-draft",
      payload: payload,
      auto_promotion: false,
      auto_link_canonicals: false,
      auto_resolve_contradictions: false,
    };
  }

  window.OC = window.OC || {};
  window.OC.ReconEngine = { load: load, classifications: classifications, reviewTypes: reviewTypes, buildDecision: buildDecision };
})();
