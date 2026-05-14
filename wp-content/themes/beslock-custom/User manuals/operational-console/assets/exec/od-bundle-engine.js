// od-bundle-engine.js — Phase 57 (consumer payload bundle publisher)
// vanilla ES; attaches to window.OC.*; throws on missing reviewer;
// builds envelopes via OC.FSBridge.buildRequestEnvelope; never writes FS directly.
(function (global) {
  'use strict';
  const OC = global.OC = global.OC || {};
  OC.od_bundle_engine = OC.od_bundle_engine || Object.freeze({
    schema: 'operational-deployment-readiness-controlled-production-activation/1.0',
    layer: 50,
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
