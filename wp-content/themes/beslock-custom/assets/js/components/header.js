(function () {
  'use strict';

  var STATE_FULL = 'FULL';
  var STATE_COMPACT = 'COMPACT';
  var ENTER_COMPACT = 120;
  var EXIT_COMPACT = 40;
  var TOGGLE_CLASS = 'header--scrolled';

  var currentState = STATE_FULL;
  var scheduledEvaluate = false;
  var scheduledMeasure = false;
  var header = null;
  var heroGate = 0;

  function query(selector, context) {
    return (context || document).querySelector(selector);
  }

  function computeHeroGate() {
    heroGate = (window.innerHeight || document.documentElement.clientHeight || 0) * 0.12;
  }

  function applyState(nextState) {
    if (!header || nextState === currentState) {
      return;
    }

    currentState = nextState;
    header.classList.toggle(TOGGLE_CLASS, currentState === STATE_COMPACT);
  }

  function evaluateState() {
    scheduledEvaluate = false;

    if (!header) {
      return;
    }

    var scrollY = window.scrollY || window.pageYOffset || 0;

    if (scrollY < heroGate) {
      applyState(STATE_FULL);
      return;
    }

    if (currentState === STATE_FULL && scrollY > ENTER_COMPACT) {
      applyState(STATE_COMPACT);
    } else if (currentState === STATE_COMPACT && scrollY < EXIT_COMPACT) {
      applyState(STATE_FULL);
    }
  }

  function scheduleEvaluate() {
    if (scheduledEvaluate) {
      return;
    }

    scheduledEvaluate = true;
    window.requestAnimationFrame(evaluateState);
  }

  function updateLogoMetrics() {
    scheduledMeasure = false;

    if (!header) {
      return;
    }

    var wrapper = query('[data-js="header-logo-wrapper"]', header) || query('.logo-wrapper', header);
    var image = query('[data-js="header-logo-image"]', header) || query('.header__logo img', header);
    var cart = query('[data-js="header-cart"]', header) || query('.header__icon--cart', header);

    if (wrapper && image) {
      var rect = image.getBoundingClientRect ? image.getBoundingClientRect() : null;
      var height = rect && rect.height ? rect.height : (image.clientHeight || image.naturalHeight || 0);

      if (height) {
        wrapper.style.setProperty('--logo-h', height + 'px');
        wrapper.setAttribute('data-logo-h', Math.round(height));
        document.documentElement.style.setProperty('--site-logo-height', height + 'px');
      }
    }

    // Preserve the current production contract where the header and cart stay visible
    // even if an unrelated runtime briefly applies inline hidden styles.
    if (header) {
      header.style.removeProperty('display');
      header.style.removeProperty('visibility');
      header.style.removeProperty('opacity');
    }

    if (cart) {
      if ((window.getComputedStyle && window.getComputedStyle(cart).display === 'none') || cart.style.display === 'none') {
        cart.style.setProperty('display', 'flex', 'important');
      }

      cart.style.setProperty('visibility', 'visible');
      cart.style.setProperty('opacity', '1');
    }
  }

  function scheduleMeasure() {
    if (scheduledMeasure) {
      return;
    }

    scheduledMeasure = true;
    window.requestAnimationFrame(updateLogoMetrics);
  }

  function init() {
    if (window.__beslockHeaderComponentReady) {
      return;
    }

    header = query('[data-js="header"]') || query('.header');

    if (!header) {
      return;
    }

    window.__beslockHeaderComponentReady = true;

    computeHeroGate();
    scheduleMeasure();

    var image = query('[data-js="header-logo-image"]', header) || query('.header__logo img', header);
    if (image && !image.complete) {
      image.addEventListener('load', scheduleMeasure, { once: true });
    }

    currentState = STATE_FULL;
    evaluateState();

    window.addEventListener('scroll', scheduleEvaluate, { passive: true });
    window.addEventListener('resize', function () {
      computeHeroGate();
      scheduleEvaluate();
      scheduleMeasure();
    }, { passive: true });
    window.addEventListener('load', scheduleMeasure, { passive: true });
    window.addEventListener('pageshow', function () {
      scheduleEvaluate();
      scheduleMeasure();
    }, { passive: true });

    window.beslock = window.beslock || {};
    window.beslock.header = {
      refresh: function () {
        computeHeroGate();
        scheduleEvaluate();
        scheduleMeasure();
      },
      isCompact: function () {
        return header.classList.contains(TOGGLE_CLASS);
      }
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();