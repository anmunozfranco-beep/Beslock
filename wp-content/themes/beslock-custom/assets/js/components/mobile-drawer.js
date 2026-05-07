(function () {
  'use strict';

  var drawer;
  var panel;
  var toggle;
  var closeButton;
  var backdrop;
  var productsToggle;
  var productsPanel;
  var previousActiveElement = null;
  var removeFocusTrap = null;
  var scrollPosition = 0;

  function query(selector, context) {
    return (context || document).querySelector(selector);
  }

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function lockScroll() {
    scrollPosition = window.scrollY || document.documentElement.scrollTop || 0;
    document.documentElement.classList.add('has-drawer-open');
    document.body.classList.add('drawer-no-scroll');
    document.body.style.position = 'fixed';
    document.body.style.top = '-' + scrollPosition + 'px';
    document.body.style.width = '100%';
  }

  function unlockScroll() {
    document.documentElement.classList.remove('has-drawer-open');
    document.body.classList.remove('drawer-no-scroll');
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.width = '';
    window.scrollTo(0, scrollPosition || 0);
  }

  function trapFocus(container) {
    var nodes = Array.prototype.slice.call(container.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'));
    if (!nodes.length) {
      return function () {};
    }

    var first = nodes[0];
    var last = nodes[nodes.length - 1];

    function onKeyDown(event) {
      if (event.key !== 'Tab') {
        return;
      }

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }

    container.addEventListener('keydown', onKeyDown);

    return function () {
      container.removeEventListener('keydown', onKeyDown);
    };
  }

  function resetProductsPanel() {
    if (!productsPanel) {
      return;
    }

    productsPanel.hidden = true;
    productsPanel.setAttribute('aria-hidden', 'true');
    productsPanel.classList.remove('models--visible');
    productsPanel.classList.add('models--hidden');

    if (productsToggle) {
      productsToggle.setAttribute('aria-expanded', 'false');
    }

    if (drawer) {
      drawer.classList.remove('products-open');
      drawer.classList.remove('products-opening');
      drawer.classList.remove('products-closing');
    }
  }

  function openDrawer() {
    if (!drawer || drawer.classList.contains('is-open')) {
      return;
    }

    previousActiveElement = document.activeElement;

    drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    if (toggle) {
      toggle.setAttribute('aria-expanded', 'true');
    }
    if (backdrop) {
      backdrop.classList.add('backdrop-visible');
    }

    if (!prefersReducedMotion()) {
      lockScroll();
    } else {
      document.documentElement.classList.add('has-drawer-open');
    }

    if (typeof removeFocusTrap === 'function') {
      removeFocusTrap();
    }
    removeFocusTrap = trapFocus(panel || drawer);

    var focusTarget = closeButton || query('a, button', panel || drawer);
    if (focusTarget) {
      setTimeout(function () {
        try {
          focusTarget.focus({ preventScroll: true });
        } catch (error) {
          focusTarget.focus();
        }
      }, 40);
    }
  }

  function closeDrawer() {
    if (!drawer || !drawer.classList.contains('is-open')) {
      return;
    }

    drawer.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    if (toggle) {
      toggle.setAttribute('aria-expanded', 'false');
    }
    if (backdrop) {
      backdrop.classList.remove('backdrop-visible');
    }

    if (typeof removeFocusTrap === 'function') {
      removeFocusTrap();
      removeFocusTrap = null;
    }

    if (!prefersReducedMotion()) {
      unlockScroll();
    } else {
      document.documentElement.classList.remove('has-drawer-open');
      document.body.classList.remove('drawer-no-scroll');
    }

    resetProductsPanel();

    if (previousActiveElement && typeof previousActiveElement.focus === 'function') {
      try {
        previousActiveElement.focus({ preventScroll: true });
      } catch (error) {
        previousActiveElement.focus();
      }
    }
  }

  function toggleDrawer(event) {
    if (event && typeof event.preventDefault === 'function') {
      event.preventDefault();
    }

    if (drawer && drawer.classList.contains('is-open')) {
      closeDrawer();
      return;
    }

    openDrawer();
  }

  function onDocumentKeyDown(event) {
    if ((event.key === 'Escape' || event.key === 'Esc') && drawer && drawer.classList.contains('is-open')) {
      event.preventDefault();
      closeDrawer();
    }
  }

  function initLinkClose() {
    if (!drawer) {
      return;
    }

    drawer.querySelectorAll('a.mobile-menu__link').forEach(function (link) {
      link.addEventListener('click', function (event) {
        if (event.target && event.target.closest && event.target.closest('[data-js="drawer-products-panel"]')) {
          return;
        }
        closeDrawer();
      });
    });
  }

  function initSwipeClose() {
    if (!panel) {
      return;
    }

    var startX = 0;
    var startY = 0;
    var tracking = false;

    panel.addEventListener('touchstart', function (event) {
      if (!drawer.classList.contains('is-open') || !event.touches || !event.touches.length) {
        return;
      }

      startX = event.touches[0].clientX;
      startY = event.touches[0].clientY;
      tracking = true;
    }, { passive: true });

    panel.addEventListener('touchend', function (event) {
      if (!tracking || !event.changedTouches || !event.changedTouches.length) {
        tracking = false;
        return;
      }

      var deltaX = event.changedTouches[0].clientX - startX;
      var deltaY = event.changedTouches[0].clientY - startY;
      tracking = false;

      if (Math.abs(deltaX) > Math.abs(deltaY) && deltaX < -60) {
        closeDrawer();
      }
    }, { passive: true });
  }

  function init() {
    if (window.__beslockMobileDrawerComponentReady) {
      return;
    }

    drawer = query('[data-js="mobile-drawer"]') || query('#mobileDrawer');
    panel = query('[data-js="mobile-drawer-panel"]', drawer) || query('.mobile-drawer__panel', drawer);
    toggle = query('[data-js="drawer-toggle"]') || query('#menuBtn');
    closeButton = query('[data-js="drawer-close"]', drawer) || query('#closeDrawer');
    backdrop = query('[data-js="drawer-backdrop"]', drawer) || query('#drawerBackdrop');
    productsToggle = query('[data-js="drawer-products-toggle"]', drawer) || query('#productsToggle');
    productsPanel = query('[data-js="drawer-products-panel"]', drawer) || query('#productsPanel');

    if (!drawer || !panel || !toggle || !closeButton || !backdrop) {
      return;
    }

    window.__beslockMobileDrawerComponentReady = true;

    resetProductsPanel();

    toggle.addEventListener('click', toggleDrawer);
    closeButton.addEventListener('click', function (event) {
      event.preventDefault();
      closeDrawer();
    });
    backdrop.addEventListener('click', function (event) {
      event.preventDefault();
      closeDrawer();
    });
    document.addEventListener('keydown', onDocumentKeyDown);

    initLinkClose();
    initSwipeClose();

    window.beslock = window.beslock || {};
    window.beslock.drawer = {
      open: openDrawer,
      close: closeDrawer,
      toggle: toggleDrawer,
      isOpen: function () {
        return !!drawer && drawer.classList.contains('is-open');
      }
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();