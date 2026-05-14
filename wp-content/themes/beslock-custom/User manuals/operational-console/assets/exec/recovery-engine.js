// recovery-engine.js — read-only detector for incomplete operations.
// Inspects transaction-events / mutation-events / lineage-events /
// snapshot-events and surfaces a recovery manifest (proposal only).
(function () {
  if (!window.OC) window.OC = {};

  async function buildRecoveryManifest() {
    const tx = await window.OC.FSBridge.loadEventStore('transaction-events');
    const mu = await window.OC.FSBridge.loadEventStore('mutation-events');
    const li = await window.OC.FSBridge.loadEventStore('lineage-events');
    const sn = await window.OC.FSBridge.loadEventStore('snapshot-events');
    const ro = await window.OC.FSBridge.loadEventStore('rollback-events');

    const findings = [];

    function evs(s) { return (s && s.events) ? s.events : []; }

    const muIds = new Set(evs(mu).map(e => e.operation_id));
    const liIds = new Set(evs(li).map(e => e.links_to_operation_id || e.operation_id));
    const snByTx = {};
    for (const e of evs(sn)) {
      const t = e.transaction_id || 'unknown';
      snByTx[t] = (snByTx[t] || 0) + 1;
    }

    // REC-SIG-1: transaction in 'executing' without committed/failed
    const txByState = {};
    for (const e of evs(tx)) {
      txByState[e.transaction_id] = e.to_state || e.state || 'unknown';
    }
    for (const tid of Object.keys(txByState)) {
      if (txByState[tid] === 'executing') {
        findings.push({ signal: 'REC-SIG-1', transaction_id: tid,
          recommends: 'replay-from-snapshot',
          alternative: 'rollback-via-restore-prior-snapshot' });
      }
    }

    // REC-SIG-3: mutation event present but no lineage event
    for (const id of muIds) {
      if (!liIds.has(id)) {
        findings.push({ signal: 'REC-SIG-3', operation_id: id,
          recommends: 'append-bridge-lineage-event',
          alternative: 'rollback-revert-failed-mutation' });
      }
    }

    // REC-SIG-4: rollback event but transaction not 'rolled-back'
    for (const e of evs(ro)) {
      const tid = e.transaction_id;
      if (tid && txByState[tid] && txByState[tid] !== 'rolled-back') {
        findings.push({ signal: 'REC-SIG-4', transaction_id: tid,
          recommends: 'advance-transaction-state-to-rolled-back',
          alternative: 'manual-reviewer-triage' });
      }
    }

    return {
      schema: 'governed-recovery-manifest/1.0',
      generated_at_iso: new Date().toISOString(),
      findings: findings,
      reviewer_authorisation_required: true,
      auto_recovery: false,
    };
  }

  window.OC.RecoveryEngine = { buildRecoveryManifest: buildRecoveryManifest };
})();
