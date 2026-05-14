// phase 54 — unified operational intake, semantic consolidation & manual runtime closure
// Engine for prompt-package-console.
// Vanilla ES. Attaches to window.OC. NEVER writes FS.
// Builds request envelopes via OC.FSBridge.buildRequestEnvelope.
// Throws if reviewer attribution missing.
(function () {
  if (typeof window === 'undefined') return;
  window.OC = window.OC || {};
  function build(kind, payload) {
    if (!window.OC.reviewer || !window.OC.reviewer.id) {
      throw new Error('reviewer attribution required');
    }
    if (!window.OC.FSBridge || !window.OC.FSBridge.buildRequestEnvelope) {
      throw new Error('OC.FSBridge.buildRequestEnvelope unavailable');
    }
    return window.OC.FSBridge.buildRequestEnvelope({
      schema: 'governed-fs-operation-request/1.0',
      reviewer: window.OC.reviewer.id,
      kind: kind,
      payload: payload
    });
  }
  window.OC.mr_prompt_engine = { build: build };
})();
