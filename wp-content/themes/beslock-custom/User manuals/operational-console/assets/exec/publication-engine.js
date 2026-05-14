// phase 47/48 — operational-console exec engine.
// Browser-only. NEVER mutates the filesystem. Emits only governed-fs-operation-request envelopes.

window.OC = window.OC || {};
window.OC.PublicationEngine = (function () {
  function buildPublicationBuildRequest({ synthesis_id, output_formats, manual_id, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!synthesis_id) throw new Error("PUB-5: synthesis_id required");
    if (!reviewer) throw new Error("publication build requires reviewer attribution");
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "publication-build",
      reviewer: reviewer,
      payload: {
        build_id: "pubb-" + manual_id + "-" + Date.now(),
        synthesis_id: synthesis_id,
        manual_id: manual_id,
        output_formats: (output_formats || ["html", "json"]).slice(),
        writes_live_tree: false,
        deterministic: true,
      },
    });
  }
  return { buildPublicationBuildRequest: buildPublicationBuildRequest };
})();
