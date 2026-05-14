// phase 49 — multimodal renderer (deterministic, escapes attributes).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var MR = OC.MultimodalRender = OC.MultimodalRender || {};
  function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }
  MR.renderPlacement = function (p) {
    if (!p || !p.image_id) return '<div class="oc-visual-missing" data-reason="visual-not-available">visual-not-available</div>';
    return '<figure class="oc-visual" data-grounding-id="' + esc(p.grounding_id||'') +
           '" data-image-id="' + esc(p.image_id) + '" data-role="' + esc(p.role||'contextual') +
           '" data-evidence="' + esc((p.evidence_ids||[]).join(',')) + '">' +
           '<img src="' + esc(p.src||'') + '" alt="' + esc(p.alt||'') + '" loading="lazy">' +
           '<figcaption><span class="oc-visual-role">' + esc(p.role||'contextual') + '</span> ' +
           '<span class="oc-visual-trust" data-tier="' + esc(p.trust_tier||'') + '">' + esc(p.trust_tier||'') + '</span></figcaption>' +
           '</figure>';
  };
})(window);
