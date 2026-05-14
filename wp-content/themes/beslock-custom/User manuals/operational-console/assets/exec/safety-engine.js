// safety-engine.js — reads the safety-violation audit feed and surfaces it
// for reviewer triage. Read-only; never mutates.
(function () {
  if (!window.OC) window.OC = {};

  async function loadAuditEvents() {
    return await window.OC.FSBridge.loadEventStore('audit-events');
  }

  function summarise(events) {
    if (!events || !events.events) return { total: 0, by_kind: {} };
    const by_kind = {};
    for (const e of events.events) {
      const k = (e.payload && e.payload.kind) || (e.kind) || 'unknown';
      by_kind[k] = (by_kind[k] || 0) + 1;
    }
    return { total: events.events.length, by_kind: by_kind };
  }

  window.OC.SafetyEngine = { loadAuditEvents: loadAuditEvents, summarise: summarise };
})();
