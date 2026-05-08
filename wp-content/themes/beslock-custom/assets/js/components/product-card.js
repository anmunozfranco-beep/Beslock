/* Product-card component bridge.
 * This owns product-card interactions while legacy selectors still coexist.
 * It keeps the current runtime stable and supports legacy markup variants
 * until the remaining old assets can be removed safely.
 */

(function () {
  'use strict';

  var ROTATOR_INTERVAL_MS = 5000;
  var hoverMediaQuery = window.matchMedia ? window.matchMedia('(hover: hover)') : null;

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function setHoverState(card, isActive) {
    card.classList.toggle('bes-product-card--hover', isActive);
  }

  function initHoverState(card) {
    if (card.dataset.besProductCardHoverReady === 'true') {
      return;
    }

    card.dataset.besProductCardHoverReady = 'true';

    card.addEventListener('pointerenter', function () {
      if (hoverMediaQuery && !hoverMediaQuery.matches) {
        return;
      }

      setHoverState(card, true);
    });

    card.addEventListener('pointerleave', function () {
      setHoverState(card, false);
    });

    card.addEventListener('focusin', function () {
      setHoverState(card, true);
    });

    card.addEventListener('focusout', function (event) {
      if (card.contains(event.relatedTarget)) {
        return;
      }

      setHoverState(card, false);
    });
  }

  function markActiveFrame(frames, activeIndex) {
    frames.forEach(function (frame, index) {
      var isActive = index === activeIndex;
      frame.classList.toggle('product-card__frame--active', isActive);
      frame.classList.toggle('is-active', isActive);
      frame.classList.toggle('visible', isActive);
      frame.setAttribute('aria-hidden', isActive ? 'false' : 'true');
    });
  }

  function initFrameRotator(wrapper, cardIndex) {
    if (!wrapper || wrapper.dataset.besProductCardRotatorReady === 'true') {
      return;
    }

    var frames = Array.prototype.slice.call(
      wrapper.querySelectorAll('img.product-card__frame, img.product-frame, img.product-img')
    );

    if (!frames.length) {
      return;
    }

    wrapper.dataset.besProductCardRotatorReady = 'true';
    wrapper.classList.add('bes-product-card__rotator');

    var activeIndex = 0;
    frames.forEach(function (frame, index) {
      if (
        frame.classList.contains('product-card__frame--active') ||
        frame.classList.contains('is-active') ||
        frame.classList.contains('visible')
      ) {
        activeIndex = index;
      }
    });

    markActiveFrame(frames, activeIndex);

    if (frames.length < 2 || prefersReducedMotion()) {
      return;
    }

    var delay = 400 + (cardIndex % 4) * 180;
    window.setTimeout(function () {
      window.setInterval(function () {
        activeIndex = (activeIndex + 1) % frames.length;
        markActiveFrame(frames, activeIndex);
      }, ROTATOR_INTERVAL_MS);
    }, delay);
  }

  function syncAltImageVisibility(container, isVisible) {
    container.classList.toggle('alt-visible', isVisible);
    container.classList.toggle('bes-product-card__image--alt-visible', isVisible);
  }

  function initAltImage(card, cardIndex) {
    var container = card.querySelector('.product-card__image.has-alt');
    if (!container || container.dataset.besProductCardAltReady === 'true') {
      return;
    }

    var mainImage = container.querySelector('.product-card__image--main');
    var altImage = container.querySelector('.product-card__image--alt');

    if (!mainImage || !altImage) {
      return;
    }

    container.dataset.besProductCardAltReady = 'true';

    syncAltImageVisibility(container, false);

    if (hoverMediaQuery && hoverMediaQuery.matches) {
      card.addEventListener('pointerenter', function () {
        syncAltImageVisibility(container, true);
      });

      card.addEventListener('pointerleave', function () {
        syncAltImageVisibility(container, false);
      });
      return;
    }

    if (prefersReducedMotion()) {
      return;
    }

    var delay = 600 + (cardIndex % 3) * 250;
    var isVisible = false;

    window.setTimeout(function () {
      window.setInterval(function () {
        isVisible = !isVisible;
        syncAltImageVisibility(container, isVisible);
      }, ROTATOR_INTERVAL_MS);
    }, delay);
  }

  function initMedia(card, cardIndex) {
    var wrappers = card.querySelectorAll(
      '.product-card__image-rotator, .product-image-rotator, .product-image-wrapper'
    );

    wrappers.forEach(function (wrapper) {
      initFrameRotator(wrapper, cardIndex);
    });

    initAltImage(card, cardIndex);
  }

  function initProductCards(context) {
    var root = context || document;
    var cards = root.querySelectorAll('[data-js="product-card"]');

    if (!cards.length) {
      return;
    }

    cards.forEach(function (card, index) {
      if (card.dataset.besProductCardReady === 'true') {
        return;
      }

      card.dataset.besProductCardReady = 'true';
      card.classList.add('bes-product-card--ready');
      initHoverState(card);
      initMedia(card, index);

      var action = card.querySelector('[data-js="product-card-add-to-cart"]');
      if (action) {
        action.setAttribute('rel', 'nofollow');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initProductCards(document);
    });
  } else {
    initProductCards(document);
  }

  window.__beslock_product_card_init = initProductCards;
})();