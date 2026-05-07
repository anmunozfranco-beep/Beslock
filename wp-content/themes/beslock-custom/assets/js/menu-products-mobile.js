/**
 * Deprecated compatibility bridge.
 *
 * Drawer ownership moved to assets/js/components/mobile-drawer.js.
 * Products-panel state ownership lives in assets/js/main.js.
 *
 * This legacy file intentionally no longer binds listeners, scroll locks,
 * MutationObservers, or drawer state transitions.
 */
(function () {
  'use strict';

  window.beslock = window.beslock || {};
  window.beslock.legacy = window.beslock.legacy || {};
  window.beslock.legacy.menuProductsMobileDeprecated = true;
})();
