// phase 49 — prompt governance engine (append-only, reviewer-authored).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PG = OC.Prompt = OC.Prompt || {};
  PG.buildPromptRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.grounding_id) throw new Error('PG-3: grounding_id required (no detached prompts)');
    if (!input.canonical_product_id) throw new Error('PG-1: canonical_product_id required');
    if (!input.synthesis_id) throw new Error('PG-1: synthesis_id required');
    if (!input.reviewer) throw new Error('reviewer required');
    if (typeof input.prompt_text !== 'string' || !input.prompt_text.length) throw new Error('PG-5: prompt_text required (reviewer-authored)');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'prompt',
      reviewer: input.reviewer,
      payload: {
        prompt_id: input.prompt_id || null,
        grounding_id: input.grounding_id,
        canonical_product_id: input.canonical_product_id,
        synthesis_id: input.synthesis_id,
        intent: input.intent || '',
        constraints: input.constraints || [],
        prompt_text: input.prompt_text,
        prior_prompt_id: input.prior_prompt_id || null
      }
    });
  };
})(window);
