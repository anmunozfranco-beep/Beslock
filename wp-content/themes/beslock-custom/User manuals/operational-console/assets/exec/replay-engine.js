// replay-engine.js — read-only deterministic replay reconstructor.
// Default mode is verify-only: reconstructs the expected outcome from
// snapshots + journals and compares against current state. Writing mode
// is reviewer-authorized only and emits requests, never writes from the
// browser.
(function () {
  if (!window.OC) window.OC = {};

  async function reconstructPlan(transactionId) {
    const tx = await window.OC.FSBridge.loadEventStore('transaction-events');
    const mu = await window.OC.FSBridge.loadEventStore('mutation-events');
    const sn = await window.OC.FSBridge.loadEventStore('snapshot-events');
    const tEvents = (tx && tx.events ? tx.events : []).filter(e => e.transaction_id === transactionId);
    const sEvents = (sn && sn.events ? sn.events : []).filter(e => e.transaction_id === transactionId);
    const mEvents = (mu && mu.events ? mu.events : []).filter(e => e.transaction_id === transactionId);
    const order = [];
    for (const e of sEvents) order.push({ at: e.occurred_at_iso, kind: 'snapshot', payload: e });
    for (const e of mEvents) order.push({ at: e.executed_at_iso, kind: 'mutation', payload: e });
    for (const e of tEvents) order.push({ at: e.occurred_at_iso || e.transitioned_at_iso, kind: 'transaction', payload: e });
    order.sort((a, b) => (a.at || '').localeCompare(b.at || ''));
    return {
      schema: 'governed-replay-plan/1.0',
      transaction_id: transactionId,
      mode: 'verify-only',
      sequence_length: order.length,
      sequence: order,
      writes_filesystem: false,
      reviewer_authorisation_required_for_writes: true,
    };
  }

  function buildReplayRequest(form) {
    // form: { transaction_id, mode (verify-only|reconstruct-into-rollback-target), reviewer_notes }
    const reasoning = [
      'replay transaction ' + form.transaction_id,
      'mode: ' + (form.mode || 'verify-only'),
      'RPL-2: default mode is read-only',
      'RPL-6: never overwrites live tree',
    ];
    return window.OC.FSBridge.buildRequestEnvelope('replay', {
      transaction_id: form.transaction_id,
      replay_mode: form.mode || 'verify-only',
      reviewer_notes: form.reviewer_notes || '',
      reasoning_chain: reasoning,
      replay_rules_required: ['RPL-1','RPL-2','RPL-3','RPL-4','RPL-6','RPL-7'],
    });
  }

  window.OC.ReplayEngine = {
    reconstructPlan: reconstructPlan,
    buildReplayRequest: buildReplayRequest,
  };
})();
