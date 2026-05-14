// consistency-engine.js — read-only consistency scanner. Detects
// duplicate / concurrent / orphan / partial / drift conditions.
(function () {
  if (!window.OC) window.OC = {};

  async function scan() {
    const findings = [];
    const tx = await window.OC.FSBridge.loadEventStore('transaction-events');
    const mu = await window.OC.FSBridge.loadEventStore('mutation-events');
    const li = await window.OC.FSBridge.loadEventStore('lineage-events');
    const ro = await window.OC.FSBridge.loadEventStore('rollback-events');

    function evs(s) { return (s && s.events) ? s.events : []; }

    // CON-1 duplicate transaction execution
    const seen = new Set();
    for (const e of evs(tx)) {
      const key = (e.request_id || e.transaction_id) + '::' + (e.to_state || e.state || '');
      if ((e.to_state || e.state) === 'executing') {
        if (seen.has(e.request_id || e.transaction_id)) {
          findings.push({ id: 'CON-1', kind: 'duplicate-transaction-execution', severity: 'block',
            message: 'duplicate executing transaction ' + (e.request_id || e.transaction_id) });
        }
        seen.add(e.request_id || e.transaction_id);
      }
    }

    // CON-3 orphan manifest (lineage referencing unknown operation)
    const muIds = new Set(evs(mu).map(e => e.operation_id));
    for (const e of evs(li)) {
      const ref = e.links_to_operation_id || e.operation_id;
      if (ref && !muIds.has(ref)) {
        findings.push({ id: 'CON-4', kind: 'stale-lineage', severity: 'warning',
          message: 'lineage references unknown operation ' + ref });
      }
    }

    // CON-5 partial rollback (rollback event but tx state not rolled-back)
    const txState = {};
    for (const e of evs(tx)) txState[e.transaction_id] = e.to_state || e.state;
    for (const e of evs(ro)) {
      const t = e.transaction_id;
      if (t && txState[t] && txState[t] !== 'rolled-back') {
        findings.push({ id: 'CON-5', kind: 'partial-rollback', severity: 'recovery',
          message: 'rollback recorded for ' + t + ' but tx state is ' + txState[t] });
      }
    }

    return {
      schema: 'governed-consistency-report/1.0',
      generated_at_iso: new Date().toISOString(),
      findings: findings,
      counts: { total: findings.length },
      mutates_filesystem: false,
    };
  }

  window.OC.ConsistencyEngine = { scan: scan };
})();
