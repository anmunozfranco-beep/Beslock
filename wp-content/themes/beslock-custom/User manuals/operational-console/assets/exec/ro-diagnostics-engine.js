// ro-diagnostics-engine.js — Phase 58 (operational diagnostics snapshots)
// vanilla ES; attaches to window.OC.*; throws on missing reviewer;
// builds envelopes via OC.FSBridge.buildRequestEnvelope; never writes FS directly.
(function (global) {
  'use strict';
  const OC = global.OC = global.OC || {};
  OC.ro_diagnostics_engine = OC.ro_diagnostics_engine || Object.freeze({
    schema: 'reviewer-operational-ergonomics-convergence/1.0',
    layer: 51,
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
