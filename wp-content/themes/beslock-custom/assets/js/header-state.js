/**
 * Deprecated compatibility bridge.
 *
 * Sticky header ownership moved to assets/js/components/header.js.
 *
 * This legacy file intentionally no longer registers scroll, resize,
 * measurement, or recovery listeners.
 */
(function () {
  'use strict';

  window.beslock = window.beslock || {};
  window.beslock.legacy = window.beslock.legacy || {};
  window.beslock.legacy.headerStateDeprecated = true;
})();
