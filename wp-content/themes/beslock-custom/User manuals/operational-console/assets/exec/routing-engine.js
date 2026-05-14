/* exec/routing-engine.js — deterministic 6-question routing consultation. Layer 38. */
(function () {
  "use strict";
  let RULES = null;

  function load() {
    return fetch("../execution-engine/routing-inference-rules.json")
      .then(function (r) { return r.json(); })
      .then(function (j) { RULES = j; return j; });
  }

  function answer(intakeInferred) {
    if (!RULES) return null;
    const out = [];
    out.push({
      question: "where-does-this-file-go",
      answer: intakeInferred.routing,
      reasoning: "R-RTG (intake) -> evidence-class '" + intakeInferred.evidence_class + "' -> '" + intakeInferred.routing + "'",
    });
    out.push({
      question: "what-class-of-evidence",
      answer: intakeInferred.evidence_class,
      reasoning: "intake-engine evidence default; reviewer override available",
    });
    out.push({
      question: "trust-tier",
      answer: intakeInferred.trust_tier,
      reasoning: "trust-tier-table default for class; OEM filename heuristic if applicable",
    });
    const role = (RULES.role_table && RULES.role_table[intakeInferred.evidence_class]) || "unclassified";
    out.push({
      question: "operational-role",
      answer: role,
      reasoning: "role_table[" + intakeInferred.evidence_class + "] = " + role,
    });
    const layers = (RULES.impacted_layers && RULES.impacted_layers[intakeInferred.domain]) || [];
    out.push({
      question: "downstream-impact",
      answer: layers,
      reasoning: "impacted_layers[" + intakeInferred.domain + "] = [" + layers.join(", ") + "]",
    });
    const refresh = (RULES.refresh_set && RULES.refresh_set[intakeInferred.domain]) || [];
    out.push({
      question: "refresh-impact",
      answer: refresh,
      reasoning: "refresh_set[" + intakeInferred.domain + "] = [" + refresh.join(", ") + "]",
    });
    return out;
  }

  window.OC = window.OC || {};
  window.OC.RoutingEngine = { load: load, answer: answer };
})();
