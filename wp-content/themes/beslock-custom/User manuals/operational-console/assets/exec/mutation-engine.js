// mutation-engine.js — proposes a mutation request. The browser NEVER
// performs the mutation; the reviewer downloads the request JSON and feeds
// it into tools/governed_fs_executor.py.
(function () {
  if (!window.OC) window.OC = {};

  function buildMutationRequest(form) {
    // form: { kind, source_path, destination, evidence_class, format_category,
    //        product, domain, trust_tier, source_hash_sha256, reviewer_notes }
    const reasoning = [];
    if (!form.source_path) reasoning.push('WARN: missing source_path');
    if (!form.destination) reasoning.push('WARN: missing destination');
    if (!form.source_hash_sha256) reasoning.push('NOTE: source_hash_sha256 will be computed by the executor and re-verified at execute time');
    reasoning.push('mutation kind: ' + (form.kind || 'copy'));
    reasoning.push('reviewer attribution required: true');
    reasoning.push('destructive overwrite forbidden');
    reasoning.push('destination collision routes source to staging/quarantined/');

    const req = window.OC.FSBridge.buildRequestEnvelope('mutation', {
      operation_kind: form.kind || 'copy',
      source_path: form.source_path,
      destination: form.destination,
      evidence_class: form.evidence_class || null,
      format_category: form.format_category || null,
      product: form.product || null,
      domain: form.domain || null,
      trust_tier: form.trust_tier || 'tier-0-unvalidated',
      source_hash_sha256: form.source_hash_sha256 || null,
      reviewer_notes: form.reviewer_notes || '',
      reasoning_chain: reasoning,
      preconditions_required: [
        'M-PRE-1', 'M-PRE-2', 'M-PRE-3', 'M-PRE-4',
        'M-PRE-5', 'M-PRE-6', 'M-PRE-7', 'M-PRE-8',
      ],
    });
    return req;
  }

  function previewExecutorCommand(req, suggestedName) {
    return window.OC.FSBridge.executorCommand('mutation', suggestedName);
  }

  window.OC.MutationEngine = {
    buildMutationRequest: buildMutationRequest,
    previewExecutorCommand: previewExecutorCommand,
  };
})();
