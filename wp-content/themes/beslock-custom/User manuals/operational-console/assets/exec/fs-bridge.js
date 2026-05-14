// fs-bridge.js — file:// safe bridge between the browser surfaces and the
// CLI executor. The browser CANNOT mutate the filesystem; this module only
// (a) reads append-only event stores via relative fetch, (b) builds operation
// request manifests, (c) exports them as Blob downloads, and (d) shows the
// reviewer the exact CLI command to run.
(function () {
  if (!window.OC) window.OC = {};
  const RUNTIME_MANIFESTS_BASE = '../runtime-manifests/';
  const RULES_BASE = '../execution-engine/';

  async function loadEventStore(kind) {
    const url = RUNTIME_MANIFESTS_BASE + kind + '/_event-store.json';
    try {
      const r = await fetch(url, { cache: 'no-store' });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.json();
    } catch (e) {
      if (window.OC && window.OC.UX && window.OC.UX.showWarning) {
        window.OC.UX.showWarning('Could not load ' + url + ' — ' + e.message);
      }
      return null;
    }
  }

  async function loadRules(name) {
    const url = RULES_BASE + name + '.json';
    try {
      const r = await fetch(url, { cache: 'no-store' });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.json();
    } catch (e) {
      if (window.OC && window.OC.UX && window.OC.UX.showWarning) {
        window.OC.UX.showWarning('Could not load ' + url + ' — ' + e.message);
      }
      return null;
    }
  }

  function buildRequestEnvelope(kind, payload) {
    const session = window.OC.State ? window.OC.State.ensureSession() : null;
    const reviewer = (session && session.reviewer) || 'UNATTRIBUTED';
    return {
      schema: 'governed-fs-operation-request/1.0',
      constitutional_layer_index: 39,
      kind: kind,
      request_id: window.OC.State ? window.OC.State.uuid() : String(Date.now()),
      session_id: session ? session.session_id : null,
      reviewer: reviewer,
      proposed_at_iso: new Date().toISOString(),
      requires_reviewer_confirmation: true,
      destructive_overwrite_forbidden: true,
      executor_invocation_required: true,
      payload: payload,
    };
  }

  function exportRequest(req, suggestedName) {
    const json = JSON.stringify(req, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = suggestedName || (req.kind + '-' + req.request_id + '.json');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function executorCommand(requestKind, savedFilename) {
    return 'python3 tools/governed_fs_executor.py ' +
           '--kind ' + requestKind + ' ' +
           '--request "' + (savedFilename || '<path/to/request.json>') + '" ' +
           '--confirm';
  }

  window.OC.FSBridge = {
    loadEventStore: loadEventStore,
    loadRules: loadRules,
    buildRequestEnvelope: buildRequestEnvelope,
    exportRequest: exportRequest,
    executorCommand: executorCommand,
  };
})();
