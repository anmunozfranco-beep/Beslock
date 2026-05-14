/* reviewer-workflow.js
   Operational UX compression façade. Constitutional layer 38, schema
   executable-operational-bindings/1.0 (NO new runtime, NO new governance layer,
   NO new event store, NO new dispatch handler).

   Wires existing Phase 52 / 54 / 55 / 56 / 57 / 58 / 59 dispatches behind a
   single 5-step reviewer flow:
       Select file → Analyze → Review → Accept → Export-ready entities

   All envelopes are produced via window.OC.FSBridge.buildRequestEnvelope and
   exported as a single bundle.json the reviewer pipes through
   tools/governed_fs_executor.py. Workflow lineage is preserved in
   localStorage with append-only supersedence (Re-analyze sets
   prior_workflow_id; never destroys prior).

   No probabilistic inference. No ML/LLM. No telemetry. No network calls.
*/
(function (global) {
  'use strict';
  const OC = global.OC = global.OC || {};
  const NS = 'beslock.oc.reviewer-workflow.';
  const KEY_WF = NS + 'workflows';
  const KEY_CUR = NS + 'current';

  // Reviewer-visible 5-step flow → underlying governed dispatches.
  // These are the DISPATCH KINDS the existing Python executors accept.
  const ANALYZE_STEPS = Object.freeze([
    { label: 'extraction',            kind: 'extraction-candidate',          phase: 52 },
    { label: 'convergence',           kind: 'canonical-entity-consolidation', phase: 55 },
    { label: 'synthesis',             kind: 'manual-synthesis-record',       phase: 54 },
    { label: 'visual-support',        kind: 'visual-support-requirement',    phase: 54 },
    { label: 'prompt-pre-generation', kind: 'prompt-package-record',         phase: 54 }
  ]);
  const ACCEPT_STEPS = Object.freeze([
    { label: 'lifecycle',          kind: 'manual-package-lifecycle-transition', phase: 52 },
    { label: 'export-ready',       kind: 'export-runtime-record',               phase: 54 },
    { label: 'stabilization',      kind: 'export-stabilization',                phase: 55 },
    { label: 'readiness-audit',    kind: 'readiness-audit',                     phase: 56 },
    { label: 'production-handoff', kind: 'production-handoff-record',           phase: 58 },
    { label: 'final-attestation',  kind: 'final-production-attestation',        phase: 59 }
  ]);

  // ---- localStorage helpers --------------------------------------------------
  function readJSON(k, fb) {
    try { const r = global.localStorage.getItem(k); return r ? JSON.parse(r) : fb; }
    catch (e) { return fb; }
  }
  function writeJSON(k, v) {
    try { global.localStorage.setItem(k, JSON.stringify(v)); } catch (e) {}
  }
  function listWorkflows() { return readJSON(KEY_WF, []); }
  function setCurrent(id) { writeJSON(KEY_CUR, id); }
  function getCurrent() { return readJSON(KEY_CUR, null); }
  function findWorkflow(id) {
    return listWorkflows().filter(function (w) { return w.workflow_id === id; })[0] || null;
  }
  function appendWorkflow(wf) {
    const list = listWorkflows();
    list.push(wf);
    writeJSON(KEY_WF, list);
    return wf;
  }
  function updateWorkflow(id, patch) {
    const list = listWorkflows();
    for (let i = 0; i < list.length; i++) {
      if (list[i].workflow_id === id) {
        list[i] = Object.assign({}, list[i], patch);
        writeJSON(KEY_WF, list);
        return list[i];
      }
    }
    return null;
  }

  // ---- envelope construction -------------------------------------------------
  function requireBridge() {
    if (!OC.FSBridge || !OC.FSBridge.buildRequestEnvelope) {
      throw new Error('OC.FSBridge.buildRequestEnvelope unavailable');
    }
  }
  function buildEnvelope(kind, payload) {
    requireBridge();
    return OC.FSBridge.buildRequestEnvelope(kind, payload);
  }

  // ---- workflow records ------------------------------------------------------
  function newWorkflowId() {
    const session = OC.State ? OC.State.ensureSession() : null;
    return 'wf-' + (session ? session.session_id.slice(0, 8) : 'anon')
                 + '-' + Date.now().toString(36);
  }

  function startAnalyze(file, summarySeed, priorWorkflowId) {
    const session = OC.State ? OC.State.ensureSession() : null;
    if (!session || !session.reviewer || session.reviewer === 'anonymous') {
      throw new Error('reviewer attribution required (set reviewer name first)');
    }
    if (!file || !file.name) throw new Error('file selection required');
    const wf = {
      workflow_id: newWorkflowId(),
      schema: 'executable-operational-bindings/1.0',
      constitutional_layer_index: 38,
      kind: 'reviewer-guided-workflow',     // Phase 58 dispatch — existing
      reviewer: session.reviewer,
      session_id: session.session_id,
      file: { name: file.name, size: file.size || 0, last_modified: file.lastModified || 0 },
      prior_workflow_id: priorWorkflowId || null,
      proposed_at_iso: new Date().toISOString(),
      status: 'analyzed',                   // analyzed → accepted (terminal)
      analyze_steps: ANALYZE_STEPS.slice(),
      summary: summarySeed || {},
      analyze_envelopes: [],
      accept_envelopes: [],
      accepted_at_iso: null,
      append_only: true,
      reviewer_authorization_required: true
    };

    // Build one envelope per analyze step. Each envelope references the
    // workflow_id so the underlying Python dispatches can be lineage-linked
    // when the reviewer pipes the bundle through governed_fs_executor.py.
    wf.analyze_envelopes = ANALYZE_STEPS.map(function (s) {
      return buildEnvelope(s.kind, {
        reviewer_workflow_id: wf.workflow_id,
        prior_workflow_id: wf.prior_workflow_id,
        step_label: s.label,
        source_file: wf.file,
        reviewer_summary: summarySeed || {}
      });
    });

    // Wrap as a Phase 58 reviewer-guided-workflow envelope (existing dispatch).
    wf.workflow_envelope = buildEnvelope('reviewer-guided-workflow', {
      reviewer_workflow_id: wf.workflow_id,
      prior_workflow_id: wf.prior_workflow_id,
      steps: ANALYZE_STEPS.map(function (s) { return s.kind; }),
      source_file: wf.file
    });

    appendWorkflow(wf);
    setCurrent(wf.workflow_id);
    if (OC.State && OC.State.appendHistory) {
      OC.State.appendHistory({
        kind: 'reviewer-workflow-analyzed',
        workflow_id: wf.workflow_id,
        prior_workflow_id: wf.prior_workflow_id,
        at: wf.proposed_at_iso
      });
    }
    return wf;
  }

  function accept(workflowId, reviewerConclusion) {
    const wf = findWorkflow(workflowId);
    if (!wf) throw new Error('workflow not found: ' + workflowId);
    if (wf.status === 'accepted') {
      throw new Error('workflow already accepted (re-analyze to supersede)');
    }
    if (!reviewerConclusion || !reviewerConclusion.trim()) {
      throw new Error('reviewer_conclusion required for Accept');
    }
    const accepted_at = new Date().toISOString();
    const accept_envs = ACCEPT_STEPS.map(function (s) {
      return buildEnvelope(s.kind, {
        reviewer_workflow_id: wf.workflow_id,
        step_label: s.label,
        source_file: wf.file,
        reviewer_summary: wf.summary,
        reviewer_conclusion: reviewerConclusion
      });
    });
    const patched = updateWorkflow(wf.workflow_id, {
      status: 'accepted',
      accepted_at_iso: accepted_at,
      reviewer_conclusion: reviewerConclusion,
      accept_steps: ACCEPT_STEPS.slice(),
      accept_envelopes: accept_envs
    });
    if (OC.State && OC.State.appendHistory) {
      OC.State.appendHistory({
        kind: 'reviewer-workflow-accepted',
        workflow_id: wf.workflow_id,
        at: accepted_at
      });
    }
    return patched;
  }

  function reanalyze(priorWorkflowId, summarySeed) {
    const prior = findWorkflow(priorWorkflowId);
    if (!prior) throw new Error('prior workflow not found: ' + priorWorkflowId);
    // NEVER mutates prior. Creates new workflow with prior_workflow_id pointer.
    return startAnalyze(prior.file, summarySeed || prior.summary, prior.workflow_id);
  }

  function lineageOf(workflowId) {
    const out = [];
    let cur = findWorkflow(workflowId);
    let guard = 0;
    while (cur && guard++ < 64) {
      out.push(cur);
      cur = cur.prior_workflow_id ? findWorkflow(cur.prior_workflow_id) : null;
    }
    return out;
  }

  function bundleEnvelopes(workflowId) {
    const wf = findWorkflow(workflowId);
    if (!wf) throw new Error('workflow not found: ' + workflowId);
    return {
      schema: 'executable-operational-bindings/1.0',
      constitutional_layer_index: 38,
      bundle_kind: 'reviewer-workflow-bundle',
      workflow_id: wf.workflow_id,
      prior_workflow_id: wf.prior_workflow_id,
      reviewer: wf.reviewer,
      file: wf.file,
      status: wf.status,
      summary: wf.summary,
      reviewer_conclusion: wf.reviewer_conclusion || null,
      envelopes: [].concat(
        [wf.workflow_envelope],
        wf.analyze_envelopes,
        wf.accept_envelopes
      ),
      executor_invocation_required: true,
      reviewer_authorization_required: true,
      append_only: true,
      exported_at_iso: new Date().toISOString()
    };
  }

  function exportBundle(workflowId) {
    const bundle = bundleEnvelopes(workflowId);
    const name = 'reviewer-workflow-' + workflowId + '.bundle.json';
    if (OC.FSBridge && OC.FSBridge.exportRequest) {
      // Re-use existing exporter (just downloads the JSON object).
      OC.FSBridge.exportRequest(bundle, name);
    } else if (OC.Drafts && OC.Drafts.exportDownload) {
      OC.Drafts.exportDownload(name, bundle);
    } else {
      throw new Error('no exporter available');
    }
    return bundle;
  }

  OC.ReviewerWorkflow = Object.freeze({
    ANALYZE_STEPS: ANALYZE_STEPS,
    ACCEPT_STEPS: ACCEPT_STEPS,
    list: listWorkflows,
    find: findWorkflow,
    current: getCurrent,
    setCurrent: setCurrent,
    startAnalyze: startAnalyze,
    accept: accept,
    reanalyze: reanalyze,
    lineageOf: lineageOf,
    bundleEnvelopes: bundleEnvelopes,
    exportBundle: exportBundle
  });
})(typeof window !== 'undefined' ? window : globalThis);
