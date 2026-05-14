// phase 47/48 — operational-console exec engine.
// Browser-only. NEVER mutates the filesystem. Emits only governed-fs-operation-request envelopes.

window.OC = window.OC || {};
window.OC.ColombianRenderingEngine = (function () {
  var TERM_TABLE = [
    ["lock","cerradura"],["deadbolt","cerrojo"],["strike","contraplaca"],
    ["fingerprint","huella dactilar"],["rfid card","tarjeta RFID"],
    ["battery","batería"],["low battery","batería baja"],
    ["factory reset","restablecimiento de fábrica"],
    ["user code","código de usuario"],["master code","código maestro"],
    ["lockout","bloqueo temporal"],
  ];
  function applyTerminology(text) {
    if (typeof text !== "string") return { text: text, transformations: [] };
    var transformations = [];
    var out = text;
    TERM_TABLE.forEach(function (pair) {
      var rx = new RegExp("\\b" + pair[0] + "\\b", "gi");
      if (rx.test(out)) {
        out = out.replace(rx, pair[1]);
        transformations.push({ rule: "CR-1", from: pair[0], to: pair[1] });
      }
    });
    return { text: out, transformations: transformations };
  }
  function buildRenderingRequest({ synthesis_id, segments, reviewer }) {
    if (!window.OC.FSBridge) throw new Error("FSBridge not loaded");
    if (!reviewer) throw new Error("rendering requires reviewer attribution");
    return window.OC.FSBridge.buildRequestEnvelope({
      kind: "rendering",
      reviewer: reviewer,
      payload: {
        rendering_id: "ren-" + synthesis_id + "-" + Date.now(),
        synthesis_id: synthesis_id,
        target_locale: "es-CO",
        segments: (segments || []).slice(),
      },
    });
  }
  return { applyTerminology: applyTerminology, buildRenderingRequest: buildRenderingRequest };
})();
