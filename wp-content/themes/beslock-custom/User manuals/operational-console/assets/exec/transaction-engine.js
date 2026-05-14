// transaction-engine.js — proposes a governed transaction request that
// wraps a layer-39 mutation request inside a transaction envelope. The
// browser NEVER executes; it only builds the request and prints the CLI
// command for the reviewer to run.
(function () {
  if (!window.OC) window.OC = {};

  const STATES = ['initialized','staged','executing','committed','failed',
                  'rolled-back','recovery-required','replayed'];

  function buildTransactionRequest(form) {
    // form: { mutation_request, snapshot_kinds: [...], reviewer_notes }
    const reasoning = [
      'wraps mutation_request inside a governed transaction',
      'snapshot_kinds: ' + (form.snapshot_kinds || []).join(', '),
      'TX-1: no mutation outside transaction boundary',
      'SN-1: snapshot_capture must precede mutation',
      'reviewer authorization required (--confirm)',
    ];
    const req = window.OC.FSBridge.buildRequestEnvelope('transaction', {
      transaction_id: 'tx-' + (window.OC.State ? window.OC.State.uuid() : Date.now()),
      mutation_request: form.mutation_request || null,
      snapshot_kinds: form.snapshot_kinds || ['destination-precapture','manifest-precapture','lineage-precapture','transaction-checkpoint'],
      initial_state: 'initialized',
      reviewer_notes: form.reviewer_notes || '',
      reasoning_chain: reasoning,
      transaction_state_rules_required: ['TX-1','TX-2','TX-3','TX-4','TX-7'],
      snapshot_rules_required: ['SN-1','SN-2','SN-3','SN-4','SN-7','SN-8'],
    });
    return req;
  }

  function previewExecutorCommand(savedFilename) {
    return 'python3 tools/governed_transactional_executor.py ' +
           '--kind transaction ' +
           '--request "' + (savedFilename || '<path/to/request.json>') + '" ' +
           '--confirm';
  }

  window.OC.TransactionEngine = {
    STATES: STATES,
    buildTransactionRequest: buildTransactionRequest,
    previewExecutorCommand: previewExecutorCommand,
  };
})();
