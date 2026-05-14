// phase 52 — OCR engine (reviewer-authored).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var OCR = OC.OCRGovernance = OC.OCRGovernance || {};
  OCR.buildFragmentRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('OF-1: reviewer required');
    if (!input.source_evidence_id || !input.decomposition_id) throw new Error('OF-1: source_evidence_id and decomposition_id required');
    if (typeof input.text !== 'string') throw new Error('OF-1: text required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'ocr-fragment',
      reviewer: input.reviewer,
      payload: {
        ocr_fragment_id: input.ocr_fragment_id || null,
        source_evidence_id: input.source_evidence_id,
        decomposition_id: input.decomposition_id,
        page_index: input.page_index || null,
        frame_index: input.frame_index || null,
        region: input.region || null,
        language: input.language || 'unknown',
        text: input.text
      }
    });
  };
  OCR.buildCorrectionRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('OF-5: reviewer required');
    if (!input.prior_fragment_id) throw new Error('OF-4: prior_fragment_id required');
    if (typeof input.text !== 'string') throw new Error('OF-1: text required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'ocr-correction',
      reviewer: input.reviewer,
      payload: {
        ocr_correction_id: input.ocr_correction_id || null,
        prior_fragment_id: input.prior_fragment_id,
        text: input.text,
        rationale: input.rationale || ''
      }
    });
  };
})(window);
