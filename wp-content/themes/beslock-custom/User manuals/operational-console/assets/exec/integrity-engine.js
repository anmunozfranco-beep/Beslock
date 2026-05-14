// integrity-engine.js — read-only multi-channel integrity verifier.
// Inspects manifests, lineage, snapshots, transactions, publications and
// reports findings. NEVER mutates, NEVER auto-quarantines.
(function () {
  if (!window.OC) window.OC = {};

  async function runChecks() {
    const findings = [];
    const stores = {};
    for (const k of ['transaction-events','mutation-events','lineage-events',
                     'snapshot-events','publication-events','refresh-events',
                     'rollback-events','audit-events']) {
      stores[k] = await window.OC.FSBridge.loadEventStore(k);
    }

    function evs(s) { return (s && s.events) ? s.events : []; }

    // INT-1 lineage continuity
    const muIds = new Set(evs(stores['mutation-events']).map(e => e.operation_id));
    const liIds = new Set(evs(stores['lineage-events']).map(e => e.links_to_operation_id || e.operation_id));
    for (const id of muIds) {
      if (!liIds.has(id)) {
        findings.push({ id: 'INT-1', kind: 'lineage-continuity', severity: 'block',
          message: 'mutation_event ' + id + ' has no lineage_event' });
      }
    }

    // INT-2 manifest consistency: schema + append_only flag present
    for (const k of Object.keys(stores)) {
      const s = stores[k];
      if (!s) continue;
      if (!s.schema || s.append_only !== true) {
        findings.push({ id: 'INT-2', kind: 'manifest-consistency', severity: 'block',
          message: 'event store ' + k + ' missing schema or append_only flag' });
      }
    }

    // INT-3 transaction completeness: every transaction has a declared state
    const TX_STATES = new Set(['initialized','staged','executing','committed','failed','rolled-back','recovery-required','replayed']);
    for (const e of evs(stores['transaction-events'])) {
      const st = e.to_state || e.state;
      if (!st || !TX_STATES.has(st)) {
        findings.push({ id: 'INT-3', kind: 'transaction-completeness', severity: 'block',
          message: 'transaction_event for ' + e.transaction_id + ' has invalid state ' + st });
      }
    }

    // INT-5 propagation integrity (warning)
    const muDests = new Set(evs(stores['mutation-events']).map(e => e.destination_path).filter(Boolean));
    if (muDests.size === 0 && evs(stores['transaction-events']).length > 0) {
      findings.push({ id: 'INT-5', kind: 'propagation-integrity', severity: 'warning',
        message: 'transactions exist but no mutation destinations recorded' });
    }

    return {
      schema: 'governed-integrity-report/1.0',
      generated_at_iso: new Date().toISOString(),
      findings: findings,
      counts: { total: findings.length,
                block: findings.filter(f => f.severity === 'block').length,
                warning: findings.filter(f => f.severity === 'warning').length },
      mutates_filesystem: false,
      auto_repair: false,
    };
  }

  window.OC.IntegrityEngine = { runChecks: runChecks };
})();
