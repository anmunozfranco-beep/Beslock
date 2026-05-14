// pc-closure-engine.js — Phase 56 (operational closure path)
// vanilla ES; attaches to window.OC.*; throws on missing reviewer;
// builds envelopes via OC.FSBridge.buildRequestEnvelope; never writes FS directly.
(function (global) {
  'use strict';
  const OC = global.OC = global.OC || {};
  OC.pc_closure_engine = OC.pc_closure_engine || Object.freeze({
    schema: 'final-operational-closure-production-readiness/1.0',
    layer: 49,
    requireReviewer(reviewer) {
      if (typeof reviewer !== 'string' || !reviewer.trim()) {
        throw new Error('reviewer attribution required');
      }
      return reviewer;
    },
    buildEnvelope(kind, reviewer, payload) {
      this.requireReviewer(reviewer);
      if (!OC.FSBridge || !OC.FSBridge.buildRequestEnvelope) {
        throw new Error('OC.FSBridge.buildRequestEnvelope unavailable');
      }
      return OC.FSBridge.buildRequestEnvelope({ kind, reviewer, payload });
    }
  });
})(typeof window !== 'undefined' ? window : globalThis);
