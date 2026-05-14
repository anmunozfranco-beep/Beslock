// failure-engine.js — read-only failure inspector. Reads
// runtime-manifests/failure-events/ and groups by failure_class.
(function () {
  if (!window.OC) window.OC = {};

  async function loadFailures() {
    return await window.OC.FSBridge.loadEventStore('failure-events');
  }

  function groupByClass(events) {
    if (!events || !events.events) return {};
    const grouped = {};
    for (const e of events.events) {
      const c = e.failure_class || 'unknown';
      if (!grouped[c]) grouped[c] = [];
      grouped[c].push(e);
    }
    return grouped;
  }

  window.OC.FailureEngine = { loadFailures: loadFailures, groupByClass: groupByClass };
})();
