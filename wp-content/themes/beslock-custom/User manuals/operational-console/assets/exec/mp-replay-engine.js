// phase 53 — packaging replay engine.
(function (root) {
  'use strict';
  var OC = root.OC = root.OC || {};
  var PR = OC.PackagingReplay = OC.PackagingReplay || {};
  PR.buildReplayRequest = function (input) {
    if (!OC.FSBridge) throw new Error('FSBridge missing');
    if (!input || !input.reviewer) throw new Error('PR-1: reviewer required');
    if (!input.package_id) throw new Error('PR-1: package_id required');
    return OC.FSBridge.buildRequestEnvelope({
      kind: 'packaging-replay',
      reviewer: input.reviewer,
      payload: {
        replay_id: input.replay_id || null,
        package_id: input.package_id,
        expected_package_sha256: input.expected_package_sha256 || null
      }
    });
  };
})(window);
