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

  function parseVariationPayload(card) {
    var node = card.querySelector('[data-js="product-card-variations"]');

    if (!node) {
      return null;
    }

    try {
      return JSON.parse(node.textContent || '{}');
    } catch (error) {
      return null;
    }
  }

  function findVariation(payload, color, geometry) {
    if (!payload || !Array.isArray(payload.variations)) {
      return null;
    }

    return payload.variations.find(function (variation) {
      return variation.color === color && variation.geometry === geometry;
    }) || null;
  }

  function findFallbackVariation(payload, color, geometry) {
    var variation = findVariation(payload, color, geometry);

    if (variation) {
      return variation;
    }

    variation = payload.variations.find(function (candidate) {
      return candidate.geometry === geometry;
    });

    if (variation) {
      return variation;
    }

    variation = payload.variations.find(function (candidate) {
      return candidate.color === color;
    });

    return variation || payload.variations[0] || null;
  }

  function getDefaultVariation(payload) {
    if (!payload || !Array.isArray(payload.variations) || !payload.variations.length) {
      return null;
    }

    return payload.variations.find(function (variation) {
      return String(variation.id) === String(payload.defaultVariationId);
    }) || payload.variations[0];
  }

  function buildVariationUrl(card, variation) {
    var productUrl = card.querySelector('.bes-product-card__button--primary, .product-card__actions a:first-child');
    var url = productUrl ? productUrl.href : window.location.href;

    try {
      var nextUrl = new URL(url, window.location.origin);
      nextUrl.searchParams.set('add-to-cart', card.getAttribute('data-product-id') || '');
      nextUrl.searchParams.set('variation_id', variation.id);
      nextUrl.searchParams.set('quantity', '1');

      Object.keys(variation.attributes || {}).forEach(function (key) {
        nextUrl.searchParams.set(key, variation.attributes[key]);
      });

      return nextUrl.toString();
    } catch (error) {
      return url;
    }
  }

  function updateVariationImage(card, variation) {
    var image = card.querySelector('[data-js="product-card-image"]');

    if (!image || !variation || !variation.image || !variation.image.src) {
      return;
    }

    image.src = variation.image.src;

    if (variation.image.srcset) {
      image.srcset = variation.image.srcset;
    } else {
      image.removeAttribute('srcset');
    }

    if (variation.image.sizes) {
      image.sizes = variation.image.sizes;
    } else {
      image.removeAttribute('sizes');
    }

    if (variation.image.alt) {
      image.alt = variation.image.alt;
    }
  }

  function updateVariationCartButton(card, variation) {
    var button = card.querySelector('[data-js="product-card-add-to-cart"]');

    if (!button || !variation) {
      return;
    }

    button.setAttribute('href', buildVariationUrl(card, variation));
    button.setAttribute('data-variation_id', variation.id);
    button.setAttribute('data-variation_attributes', JSON.stringify(variation.attributes || {}));
    button.classList.toggle('is-disabled', !variation.isPurchasable || !variation.isInStock);
    button.setAttribute('aria-disabled', (!variation.isPurchasable || !variation.isInStock) ? 'true' : 'false');
  }

  function updateVariationControls(card, payload, selected) {
    var colorButtons = Array.prototype.slice.call(card.querySelectorAll('[data-js="product-card-color-option"]'));
    var colorTray = card.querySelector('.bes-product-card__variation-colors');
    var geometryLabel = card.querySelector('[data-js="product-card-geometry-label"]');
    var availableColors = colorButtons.filter(function (button) {
      var color = button.getAttribute('data-variation-color') || '';
      return Boolean(findVariation(payload, color, selected.geometry));
    });
    var showColorSelector = availableColors.length > 1;

    if (colorTray) {
      colorTray.classList.toggle('is-hidden', !showColorSelector);
      colorTray.setAttribute('aria-hidden', showColorSelector ? 'false' : 'true');
    }

    colorButtons.forEach(function (button) {
      var color = button.getAttribute('data-variation-color') || '';
      var optionVariation = findVariation(payload, color, selected.geometry);
      var isAvailable = Boolean(optionVariation);

      button.setAttribute('aria-pressed', color === selected.color ? 'true' : 'false');
      button.disabled = !isAvailable || !showColorSelector;
      button.tabIndex = showColorSelector ? 0 : -1;
      button.classList.toggle('is-disabled', !isAvailable);
    });

    if (geometryLabel) {
      geometryLabel.textContent = selected.geometry || '';
    }
  }

  function cueVariationTransition(card) {
    if (prefersReducedMotion()) {
      return;
    }

    card.classList.remove('is-variation-transitioning');
    card.offsetWidth;
    card.classList.add('is-variation-transitioning');

    window.clearTimeout(card.besProductCardVariationTimer);
    card.besProductCardVariationTimer = window.setTimeout(function () {
      card.classList.remove('is-variation-transitioning');
    }, 380);
  }

  function applyVariation(card, payload, variation) {
    var price = card.querySelector('[data-js="product-card-price"]');
    var previousVariationId = card.dataset.selectedVariationId || '';

    if (!variation) {
      return;
    }

    if (previousVariationId && String(previousVariationId) !== String(variation.id)) {
      cueVariationTransition(card);
    }

    card.dataset.selectedVariationId = variation.id;
    card.dataset.selectedVariationColor = variation.color || '';
    card.dataset.selectedVariationGeometry = variation.geometry || '';

    if (price && variation.priceHtml) {
      price.innerHTML = variation.priceHtml;
    }

    updateVariationImage(card, variation);
    updateVariationCartButton(card, variation);
    updateVariationControls(card, payload, variation);
  }

  function initVariationControls(card) {
    if (card.dataset.besProductCardVariationsReady === 'true') {
      return;
    }

    var payload = parseVariationPayload(card);
    var defaultVariation = getDefaultVariation(payload);

    if (!payload || !defaultVariation) {
      return;
    }

    card.dataset.besProductCardVariationsReady = 'true';
    applyVariation(card, payload, defaultVariation);

    card.querySelectorAll('[data-js="product-card-color-option"]').forEach(function (button) {
      button.addEventListener('click', function () {
        if (button.disabled) {
          return;
        }

        var color = button.getAttribute('data-variation-color') || '';
        var geometry = card.dataset.selectedVariationGeometry || defaultVariation.geometry;
        var nextVariation = findFallbackVariation(payload, color, geometry);
        applyVariation(card, payload, nextVariation);
      });
    });

    ['prev', 'next'].forEach(function (direction) {
      var button = card.querySelector('[data-js="product-card-geometry-' + direction + '"]');

      if (!button || !Array.isArray(payload.geometries) || payload.geometries.length < 2) {
        return;
      }

      button.addEventListener('click', function () {
        var currentGeometry = card.dataset.selectedVariationGeometry || defaultVariation.geometry;
        var currentColor = card.dataset.selectedVariationColor || defaultVariation.color;
        var currentIndex = payload.geometries.findIndex(function (geometry) {
          return geometry.label === currentGeometry;
        });

        if (currentIndex < 0) {
          currentIndex = 0;
        }

        var offset = direction === 'next' ? 1 : -1;
        var nextIndex = (currentIndex + offset + payload.geometries.length) % payload.geometries.length;
        var nextGeometry = payload.geometries[nextIndex].label;
        var nextVariation = findFallbackVariation(payload, currentColor, nextGeometry);
        applyVariation(card, payload, nextVariation);
      });
    });
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
      initVariationControls(card);

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
