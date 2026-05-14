/* Beslock Operational Console — layer 37 — local-first, no network calls */
(function () {
  "use strict";

  // Hard rules surfaced at runtime (read by the optional banner element).
  const GOVERNANCE = {
    layer: 37,
    schema: "operational-console-governance/1.0",
    auto_approval: false,
    mutates_governance: false,
    network_calls: false,
    is_saas: false,
  };

  function loadJSON(path) {
    return fetch(path, { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error("Failed to load " + path);
        return r.json();
      })
      .catch(function () { return null; });
  }

  function renderList(targetId, items, formatter) {
    const el = document.getElementById(targetId);
    if (!el || !Array.isArray(items)) return;
    el.innerHTML = "";
    items.forEach(function (item) {
      const li = document.createElement("li");
      li.innerHTML = formatter(item);
      el.appendChild(li);
    });
  }

  function buildDraft(kind, payload) {
    return {
      schema: "operational-console-draft/1.0",
      constitutional_layer_index: 37,
      kind: kind,
      reviewer_authorization_required: true,
      auto_promotion: false,
      auto_mutates_source_truth: false,
      payload: payload,
      proposed_at_iso: new Date().toISOString(),
    };
  }

  function showDraft(kind, payload, targetId) {
    const draft = buildDraft(kind, payload);
    const el = document.getElementById(targetId);
    if (!el) return;
    el.textContent = JSON.stringify(draft, null, 2);
  }

  // Wire up data-driven sections per page.
  document.addEventListener("DOMContentLoaded", function () {
    const dataAttr = document.body.getAttribute("data-mock");
    if (dataAttr) {
      loadJSON(dataAttr).then(function (data) {
        if (!data) return;
        const slot = document.getElementById("oc-mock-dump");
        if (slot) slot.textContent = JSON.stringify(data, null, 2);
      });
    }

    document.querySelectorAll("[data-propose]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const kind = btn.getAttribute("data-propose");
        const target = btn.getAttribute("data-target");
        const sourceId = btn.getAttribute("data-source");
        let payload = {};
        if (sourceId) {
          const src = document.getElementById(sourceId);
          if (src) {
            try { payload = JSON.parse(src.textContent || "{}"); }
            catch (e) { payload = { raw: src.textContent }; }
          }
        }
        showDraft(kind, payload, target);
      });
    });
  });

  window.OC = { GOVERNANCE: GOVERNANCE, loadJSON: loadJSON, buildDraft: buildDraft };
})();
