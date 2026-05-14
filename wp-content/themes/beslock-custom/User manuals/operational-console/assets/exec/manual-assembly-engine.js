// phase 47/48 — operational-console exec engine.
// Browser-only. NEVER mutates the filesystem. Emits only governed-fs-operation-request envelopes.

window.OC = window.OC || {};
window.OC.ManualAssemblyEngine = (function () {
  var SECTIONS = ["overview","prerequisites","installation","operation",
                  "troubleshooting","maintenance","specifications","warnings","support"];
  function buildAssemblyRequest({ manual_id, canonical_product_id, sections, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("manual assembly requires reviewer attribution");
    var normalized = {};
    SECTIONS.forEach(function (s) {
      var src = (sections && sections[s]) || {};
      normalized[s] = {
        evidence_ids: (src.evidence_ids || []).slice(),
        contributing_manifests: (src.contributing_manifests || []).slice(),
        trust_composition: src.trust_composition || {},
        text_pointer: src.text_pointer || null,
        review_state: src.review_state || (src.evidence_ids && src.evidence_ids.length
                                           ? "draft" : "evidence-not-available"),
      };
    });
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "manual-assembly",
      reviewer: reviewer,
      payload: {
        manual_id: manual_id,
        canonical_product_id: canonical_product_id,
        sections: normalized,
        section_count: SECTIONS.length,
      },
    });
  }
  return { buildAssemblyRequest: buildAssemblyRequest, SECTIONS: SECTIONS };
})();
