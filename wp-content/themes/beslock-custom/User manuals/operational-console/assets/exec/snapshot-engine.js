// snapshot-engine.js — read-only snapshot explorer. Lists snapshots from
// runtime-manifests/snapshot-events/_event-store.json and groups them by
// transaction_id and snapshot_kind. Browser does not write snapshots.
(function () {
  if (!window.OC) window.OC = {};

  async function loadSnapshotEvents() {
    return await window.OC.FSBridge.loadEventStore('snapshot-events');
  }

  function groupByTransaction(events) {
    if (!events || !events.events) return {};
    const grouped = {};
    for (const e of events.events) {
      const tx = e.transaction_id || 'unknown';
      if (!grouped[tx]) grouped[tx] = [];
      grouped[tx].push(e);
    }
    return grouped;
  }

  function summarise(events) {
    if (!events || !events.events) return { total: 0, by_kind: {}, by_tx: 0 };
    const by_kind = {};
    const txs = new Set();
    for (const e of events.events) {
      const k = e.snapshot_kind || 'unknown';
      by_kind[k] = (by_kind[k] || 0) + 1;
      if (e.transaction_id) txs.add(e.transaction_id);
    }
    return { total: events.events.length, by_kind: by_kind, by_tx: txs.size };
  }

  window.OC.SnapshotEngine = {
    loadSnapshotEvents: loadSnapshotEvents,
    groupByTransaction: groupByTransaction,
    summarise: summarise,
  };
})();
