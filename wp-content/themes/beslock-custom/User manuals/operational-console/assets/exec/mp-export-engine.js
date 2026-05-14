// phase 53 — export contract engine (presentation-neutral).
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var XC = OC.ExportContract = OC.ExportContract || {};
  XC.KINDS = ['raw-html-export','structured-json-export','semantic-markdown-export'];
  XC.buildContractRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('XC-1: reviewer required');
    if (!input.manual_id || !input.package_id) throw new Error('XC-1: manual_id and package_id required');
    if (XC.KINDS.indexOf(input.export_kind) < 0) throw new Error('XC-2: invalid export_kind');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'export-contract',
      reviewer: input.reviewer,
      payload: {
        contract_id: input.contract_id || null,
        manual_id: input.manual_id,
        package_id: input.package_id,
        export_kind: input.export_kind,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
  XC.buildRenderRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('XC-1: reviewer required');
    if (!input.contract_id) throw new Error('XC-1: contract_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'export-render',
      reviewer: input.reviewer,
      payload: {
        contract_id: input.contract_id,
        reasoning_chain: input.reasoning_chain || []
      }
    });
  };
})(window);
