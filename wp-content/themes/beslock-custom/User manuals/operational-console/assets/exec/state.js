/* exec/state.js — local session + draft state via localStorage. Layer 38. */
(function () {
  "use strict";
  const NS = "beslock.oc.exec.";
  const SCHEMA = "executable-operational-bindings/1.0";
  const SESSION_KEY = NS + "session";
  const DRAFTS_KEY  = NS + "drafts";
  const HISTORY_KEY = NS + "history";

  function uuid() {
    // RFC4122-ish v4 using crypto.getRandomValues if available.
    const buf = new Uint8Array(16);
    if (window.crypto && window.crypto.getRandomValues) {
      window.crypto.getRandomValues(buf);
    } else {
      for (let i = 0; i < 16; i++) buf[i] = Math.floor(Math.random() * 256);
    }
    buf[6] = (buf[6] & 0x0f) | 0x40;
    buf[8] = (buf[8] & 0x3f) | 0x80;
    const h = Array.from(buf, function (b) { return b.toString(16).padStart(2, "0"); });
    return h.slice(0, 4).join("") + "-" + h.slice(4, 6).join("") + "-" +
           h.slice(6, 8).join("") + "-" + h.slice(8, 10).join("") + "-" +
           h.slice(10, 16).join("");
  }

  function readJSON(key, fallback) {
    try {
      const raw = window.localStorage.getItem(key);
      if (!raw) return fallback;
      return JSON.parse(raw);
    } catch (e) { return fallback; }
  }

  function writeJSON(key, val) {
    try { window.localStorage.setItem(key, JSON.stringify(val)); }
    catch (e) { /* quota, private mode -- ignore silently */ }
  }

  function ensureSession(reviewer) {
    let s = readJSON(SESSION_KEY, null);
    if (!s) {
      s = {
        schema: SCHEMA,
        session_id: uuid(),
        opened_at_iso: new Date().toISOString(),
        reviewer: reviewer || "anonymous",
        constitutional_layer_index: 38,
      };
      writeJSON(SESSION_KEY, s);
      appendHistory({ kind: "session-open", session_id: s.session_id, at: s.opened_at_iso, reviewer: s.reviewer });
    }
    return s;
  }

  function setReviewer(name) {
    const s = ensureSession();
    s.reviewer = name || "anonymous";
    writeJSON(SESSION_KEY, s);
    appendHistory({ kind: "reviewer-change", session_id: s.session_id, reviewer: s.reviewer, at: new Date().toISOString() });
    return s;
  }

  function appendDraft(draft) {
    const list = readJSON(DRAFTS_KEY, []);
    list.push(draft);
    writeJSON(DRAFTS_KEY, list);
    appendHistory({ kind: "draft-append", draft_id: draft.draft_id, draft_kind: draft.kind, at: draft.proposed_at_iso });
    return list.length;
  }

  function listDrafts() { return readJSON(DRAFTS_KEY, []); }
  function clearDrafts() {
    writeJSON(DRAFTS_KEY, []);
    appendHistory({ kind: "drafts-clear", at: new Date().toISOString() });
  }

  function appendHistory(entry) {
    const list = readJSON(HISTORY_KEY, []);
    list.push(entry);
    if (list.length > 500) list.splice(0, list.length - 500);
    writeJSON(HISTORY_KEY, list);
  }
  function listHistory() { return readJSON(HISTORY_KEY, []); }

  function exportSnapshot() {
    return {
      schema: SCHEMA,
      constitutional_layer_index: 38,
      session: ensureSession(),
      drafts: listDrafts(),
      history: listHistory(),
      exported_at_iso: new Date().toISOString(),
      append_only: true,
      reviewer_authorization_required: true,
    };
  }

  window.OC = window.OC || {};
  window.OC.State = {
    uuid: uuid,
    ensureSession: ensureSession,
    setReviewer: setReviewer,
    appendDraft: appendDraft,
    listDrafts: listDrafts,
    clearDrafts: clearDrafts,
    appendHistory: appendHistory,
    listHistory: listHistory,
    exportSnapshot: exportSnapshot,
  };
})();
