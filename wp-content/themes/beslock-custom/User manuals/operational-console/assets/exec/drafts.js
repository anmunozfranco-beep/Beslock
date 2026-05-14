/* exec/drafts.js — append-only draft manifest engine. Layer 38. */
(function () {
  "use strict";
  const SCHEMA_DRAFT = "operational-console-draft/1.1";

  function build(kind, payload, reasoningChain) {
    const session = window.OC.State.ensureSession();
    return {
      schema: SCHEMA_DRAFT,
      constitutional_layer_index: 38,
      draft_id: window.OC.State.uuid(),
      session_id: session.session_id,
      reviewer: session.reviewer,
      kind: kind,
      payload: payload || {},
      reasoning_chain: reasoningChain || [],
      proposed_at_iso: new Date().toISOString(),
      reviewer_authorization_required: true,
      auto_promotion: false,
      auto_mutates_source_truth: false,
      append_only: true,
    };
  }

  function record(kind, payload, reasoningChain) {
    const draft = build(kind, payload, reasoningChain);
    window.OC.State.appendDraft(draft);
    return draft;
  }

  function preview(target, draft) {
    if (typeof target === "string") target = document.getElementById(target);
    if (!target) return;
    target.textContent = JSON.stringify(draft, null, 2);
  }

  function exportDownload(filename, obj) {
    const blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename || "draft.json";
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(url); a.remove(); }, 0);
  }

  window.OC = window.OC || {};
  window.OC.Drafts = { build: build, record: record, preview: preview, exportDownload: exportDownload };
})();
