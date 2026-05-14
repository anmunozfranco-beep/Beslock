/* exec/ux.js — small UX helpers. Layer 38. */
(function () {
  "use strict";

  function setIndicator(id, text, kind) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = text;
    el.classList.toggle("oc-exec__indicator--unsaved", kind === "unsaved");
  }

  function bindKeyboard(map) {
    document.addEventListener("keydown", function (e) {
      const key = (e.ctrlKey || e.metaKey ? "Mod+" : "") + (e.shiftKey ? "Shift+" : "") + (e.key || "");
      const fn = map[key];
      if (fn) { e.preventDefault(); fn(e); }
    });
  }

  function showWarning(target, text) {
    if (typeof target === "string") target = document.getElementById(target);
    if (!target) return;
    target.classList.add("oc-exec__warn"); target.textContent = text;
  }

  window.OC = window.OC || {};
  window.OC.UX = { setIndicator: setIndicator, bindKeyboard: bindKeyboard, showWarning: showWarning };
})();
