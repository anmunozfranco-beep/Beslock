// rollback-engine.js — proposes a rollback request. Reviewer-only;
// browser does not execute. Append-only. Preserves failed-state evidence.
(function () {
  if (!window.OC) window.OC = {};

  function buildRollbackRequest(form) {
    // form: { rollback_kind, original_operation_id, reason, reviewer_notes }
    const reasoning = [
      'rollback_kind: ' + form.rollback_kind,
      'targets original operation: ' + form.original_operation_id,
      'preserves failed-state evidence (no deletion)',
      'append-only: emits a new lineage + rollback event, never mutates prior events',
      'requires reviewer authorization at the executor invocation gate',
    ];
    return window.OC.FSBridge.buildRequestEnvelope('rollback', {
      rollback_kind: form.rollback_kind,
      original_operation_id: form.original_operation_id,
      reason: form.reason || '',
      reviewer_notes: form.reviewer_notes || '',
      reasoning_chain: reasoning,
      rules_required: ['R-RB-1', 'R-RB-2', 'R-RB-3', 'R-RB-4', 'R-RB-5', 'R-RB-6'],
    });
  }

  window.OC.RollbackEngine = { buildRollbackRequest: buildRollbackRequest };
})();
