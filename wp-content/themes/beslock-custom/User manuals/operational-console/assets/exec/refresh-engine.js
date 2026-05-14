/* exec/refresh-engine.js — refresh proposal builder. Layer 38. No rebuild executes. */
(function () {
  "use strict";
  let RULES = null;

  function load() {
    return fetch("../execution-engine/refresh-proposal-rules.json")
      .then(function (r) { return r.json(); })
      .then(function (j) { RULES = j; return j; });
  }

  function scopes() { return RULES ? RULES.scopes.slice() : []; }
  function actions() { return RULES ? RULES.actions.slice() : []; }
  function staleClasses() { return RULES ? RULES.stale_classes.slice() : []; }

  function buildProposal(opts) {
    const reasoning = [
      { step: "scope-selected",   value: opts.scope },
      { step: "action-selected",  value: opts.action },
      { step: "domains-selected", value: opts.domains || [] },
      { step: "publications",     value: opts.publications || [] },
      { step: "isolation-rules",  value: (RULES && RULES.isolation_rules) || [] },
    ];
    return {
      payload: {
        scope: opts.scope,
        action: opts.action,
        domains: opts.domains || [],
        publications: opts.publications || [],
        notes: opts.notes || "",
        mutates_anything: false,
        executes_rebuild: false,
      },
      reasoning_chain: reasoning,
    };
  }

  window.OC = window.OC || {};
  window.OC.RefreshEngine = { load: load, scopes: scopes, actions: actions, staleClasses: staleClasses, buildProposal: buildProposal };
})();
