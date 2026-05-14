// rollback-exec-engine.js — proposes a rollback EXECUTION request that
// references a snapshot path and a transaction_id. Browser does not
// execute. Reviewer-authorized; append-only; preserves failed state.
(function () {
  if (!window.OC) window.OC = {};

  function buildRollbackExecRequest(form) {
    // form: { transaction_id, rollback_kind, snapshot_path, original_operation_id, reason, reviewer_notes }
    const reasoning = [
      'rollback_kind: ' + form.rollback_kind,
      'targets transaction: ' + form.transaction_id,
      'restores from snapshot: ' + (form.snapshot_path || '(none — abstract restore)'),
      'RBE-5: never deletes evidence',
      'RBE-6: restored content lands in rollback-target/, never overwrites live tree',
      'RBE-8: advances transaction state failed -> rolled-back',
    ];
    return window.OC.FSBridge.buildRequestEnvelope('rollback-exec', {
      transaction_id: form.transaction_id,
      rollback_kind: form.rollback_kind,
      snapshot_path: form.snapshot_path || null,
      original_operation_id: form.original_operation_id || null,
      reason: form.reason || '',
      reviewer_notes: form.reviewer_notes || '',
      reasoning_chain: reasoning,
      rollback_execution_rules_required: ['RBE-1','RBE-2','RBE-3','RBE-4','RBE-5','RBE-6','RBE-7','RBE-8'],
    });
  }

  window.OC.RollbackExecEngine = { buildRollbackExecRequest: buildRollbackExecRequest };
})();
