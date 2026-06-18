/* Single product variation controls.
 * Builds a Beslock UI on top of WooCommerce variation selects while keeping
 * the native form as the source of truth for price, stock and cart behavior.
 */
(function () {
  'use strict';

  var ATTRIBUTE_COLOR = 'color';
  var ATTRIBUTE_GEOMETRY = 'geometria';

  function normalizeAttributeName(name) {
    return String(name || '')
      .replace(/^attribute_/, '')
      .replace(/^pa_/, '')
      .toLowerCase();
  }

  function normalizeImageKey(url) {
    try {
      var parsed = new URL(url, window.location.origin);
      var basename = parsed.pathname.split('/').pop() || '';
      return basename
        .replace(/-\d+x\d+(?=\.)/, '')
        .replace(/\.[a-z0-9]+$/i, '')
        .toLowerCase();
    } catch (error) {
      return '';
    }
  }

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function getVariations(form) {
    try {
      var data = form.getAttribute('data-product_variations') || '[]';
      var variations = JSON.parse(data);
      return Array.isArray(variations) ? variations : [];
    } catch (error) {
      return [];
    }
  }

  function getSelect(form, attributeName) {
    return Array.prototype.slice.call(form.querySelectorAll('select[name^="attribute_"]')).find(function (select) {
      return normalizeAttributeName(select.name) === attributeName;
    }) || null;
  }

  function getOptions(select) {
    if (!select) {
      return [];
    }

    return Array.prototype.slice.call(select.options)
      .filter(function (option) {
        return option.value !== '';
      })
      .map(function (option) {
        return {
          value: option.value,
          label: option.textContent.trim() || option.value,
          key: option.value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''),
        };
      });
  }

  function getVariationAttribute(variation, attributeName) {
    var attributes = variation && variation.attributes ? variation.attributes : {};
    var key = 'attribute_' + attributeName;
    return attributes[key] || attributes['attribute_pa_' + attributeName] || '';
  }

  function variationMatches(variation, color, geometry) {
    return getVariationAttribute(variation, ATTRIBUTE_COLOR) === color &&
      getVariationAttribute(variation, ATTRIBUTE_GEOMETRY) === geometry;
  }

  function findVariation(variations, color, geometry) {
    return variations.find(function (variation) {
      return variationMatches(variation, color, geometry);
    }) || null;
  }

  function findFallbackVariation(variations, color, geometry) {
    return findVariation(variations, color, geometry) ||
      variations.find(function (variation) {
        return getVariationAttribute(variation, ATTRIBUTE_GEOMETRY) === geometry;
      }) ||
      variations.find(function (variation) {
        return getVariationAttribute(variation, ATTRIBUTE_COLOR) === color;
      }) ||
      variations[0] ||
      null;
  }

  function uniqueValues(variations, attributeName, filterAttributeName, filterValue) {
    var values = [];

    variations.forEach(function (variation) {
      if (filterAttributeName && getVariationAttribute(variation, filterAttributeName) !== filterValue) {
        return;
      }

      var value = getVariationAttribute(variation, attributeName);
      if (value && values.indexOf(value) === -1) {
        values.push(value);
      }
    });

    return values;
  }

  function triggerSelectChange(select) {
    if (!select) {
      return;
    }

    if (window.jQuery) {
      window.jQuery(select).trigger('change');
      return;
    }

    select.dispatchEvent(new Event('change', { bubbles: true }));
  }

  function applyNativeSelection(colorSelect, geometrySelect, nextColor, nextGeometry) {
    var colorChanged = colorSelect && colorSelect.value !== nextColor;
    var geometryChanged = geometrySelect && geometrySelect.value !== nextGeometry;

    if (colorChanged) {
      colorSelect.value = nextColor;
      triggerSelectChange(colorSelect);
    }

    if (geometryChanged) {
      window.setTimeout(function () {
        geometrySelect.value = nextGeometry;
        triggerSelectChange(geometrySelect);
      }, 0);
    }

    return colorChanged || geometryChanged;
  }

  function cueTransition(form) {
    if (prefersReducedMotion()) {
      return;
    }

    var controls = form.querySelector('[data-js="single-variation-controls"]');
    var gallery = document.querySelector('.product-page__gallery');

    [controls, gallery].forEach(function (node) {
      if (!node) {
        return;
      }

      node.classList.remove('is-transitioning', 'is-variation-transitioning');
      node.offsetWidth;
      node.classList.add(node === gallery ? 'is-variation-transitioning' : 'is-transitioning');
    });

    window.clearTimeout(form.besSingleVariationTimer);
    form.besSingleVariationTimer = window.setTimeout(function () {
      if (controls) {
        controls.classList.remove('is-transitioning');
      }
      if (gallery) {
        gallery.classList.remove('is-variation-transitioning');
      }
    }, 380);
  }

  function selectVariation(form, state, variation) {
    var colorSelect = getSelect(form, ATTRIBUTE_COLOR);
    var geometrySelect = getSelect(form, ATTRIBUTE_GEOMETRY);
    var nextColor = getVariationAttribute(variation, ATTRIBUTE_COLOR);
    var nextGeometry = getVariationAttribute(variation, ATTRIBUTE_GEOMETRY);
    var changed = applyNativeSelection(colorSelect, geometrySelect, nextColor, nextGeometry);

    if (changed) {
      cueTransition(form);
    }

    updateControls(form, state, variation);
    scrollGalleryToVariation(variation);
  }

  function scrollGalleryToVariation(variation) {
    var image = variation && variation.image ? variation.image : null;
    var key = normalizeImageKey(image && image.src);
    var gallery = document.querySelector('.product-page__gallery');
    var reel = gallery ? gallery.querySelector('.product-page__gallery-reel') : null;

    if (!key || !gallery || !reel) {
      return;
    }

    var slides = Array.prototype.slice.call(reel.querySelectorAll('.product-page__gallery-slide'));
    var targetSlide = slides.find(function (slide) {
      return Array.prototype.slice.call(slide.querySelectorAll('img')).some(function (img) {
        return normalizeImageKey(img.currentSrc || img.src || img.getAttribute('data-large_image')) === key;
      });
    });

    if (!targetSlide) {
      return;
    }

    cueTransition(document.querySelector('form.variations_form') || document.body);
    reel.scrollTo({ left: targetSlide.offsetLeft, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
  }

  function buildColorButton(option) {
    var button = document.createElement('button');
    var key = option.key || option.value.toLowerCase();

    button.type = 'button';
    button.className = 'bes-single-variations__color';
    button.setAttribute('data-js', 'single-variation-color');
    button.setAttribute('data-variation-color', option.value);
    button.setAttribute('aria-pressed', 'false');
    button.innerHTML = [
      '<span class="bes-single-variations__swatch bes-single-variations__swatch--' + key + '" aria-hidden="true"></span>',
      '<span class="bes-single-variations__color-text"></span>',
    ].join('');
    button.querySelector('.bes-single-variations__color-text').textContent = option.label;

    return button;
  }

  function buildControls(form, state) {
    var colorOptions = getOptions(state.colorSelect);
    var controls = document.createElement('div');
    var colorButtons = colorOptions.map(buildColorButton);

    controls.className = 'bes-single-variations';
    controls.setAttribute('data-js', 'single-variation-controls');
    controls.innerHTML = [
      '<div class="bes-single-variations__row bes-single-variations__row--geometry" data-js="single-variation-geometry-row">',
      '<div class="bes-single-variations__geometry" aria-label="Geometría">',
      '<button type="button" class="bes-single-variations__arrow bes-single-variations__arrow--prev" data-js="single-variation-geometry-prev" aria-label="Geometría anterior"><i class="bi bi-chevron-left" aria-hidden="true"></i></button>',
      '<span class="bes-single-variations__geometry-label" data-js="single-variation-geometry-label"></span>',
      '<button type="button" class="bes-single-variations__arrow bes-single-variations__arrow--next" data-js="single-variation-geometry-next" aria-label="Geometría siguiente"><i class="bi bi-chevron-right" aria-hidden="true"></i></button>',
      '</div>',
      '</div>',
      '<div class="bes-single-variations__row bes-single-variations__row--color" data-js="single-variation-color-row">',
      '<div class="bes-single-variations__colors" role="radiogroup" aria-label="Color" data-js="single-variation-colors"></div>',
      '</div>',
    ].join('');

    var colorContainer = controls.querySelector('[data-js="single-variation-colors"]');
    colorButtons.forEach(function (button) {
      colorContainer.appendChild(button);
    });

    return controls;
  }

  function getCurrentVariation(form, state) {
    var color = state.colorSelect ? state.colorSelect.value : '';
    var geometry = state.geometrySelect ? state.geometrySelect.value : '';
    return findFallbackVariation(state.variations, color, geometry);
  }

  function updateControls(form, state, variation) {
    var controls = form.querySelector('[data-js="single-variation-controls"]');
    var colorRow = controls ? controls.querySelector('[data-js="single-variation-color-row"]') : null;
    var geometryLabel = controls ? controls.querySelector('[data-js="single-variation-geometry-label"]') : null;
    var selectedColor = getVariationAttribute(variation, ATTRIBUTE_COLOR);
    var selectedGeometry = getVariationAttribute(variation, ATTRIBUTE_GEOMETRY);
    var availableColors = uniqueValues(state.variations, ATTRIBUTE_COLOR, ATTRIBUTE_GEOMETRY, selectedGeometry);
    var showColorSelector = availableColors.length > 1;

    if (!controls || !variation) {
      return;
    }

    if (geometryLabel) {
      geometryLabel.textContent = selectedGeometry;
    }

    if (colorRow) {
      colorRow.classList.toggle('is-hidden', !showColorSelector);
      colorRow.setAttribute('aria-hidden', showColorSelector ? 'false' : 'true');
    }

    controls.querySelectorAll('[data-js="single-variation-color"]').forEach(function (button) {
      var color = button.getAttribute('data-variation-color') || '';
      var isAvailable = availableColors.indexOf(color) !== -1;

      button.setAttribute('aria-pressed', color === selectedColor ? 'true' : 'false');
      button.disabled = !isAvailable || !showColorSelector;
      button.tabIndex = showColorSelector ? 0 : -1;
      button.classList.toggle('is-disabled', !isAvailable);
    });
  }

  function initForm(form) {
    if (!form || form.dataset.besSingleVariationsReady === 'true') {
      return;
    }

    var state = {
      colorSelect: getSelect(form, ATTRIBUTE_COLOR),
      geometrySelect: getSelect(form, ATTRIBUTE_GEOMETRY),
      variations: getVariations(form),
    };

    if (!state.colorSelect || !state.geometrySelect || !state.variations.length) {
      return;
    }

    var controls = buildControls(form, state);
    var variationsTable = form.querySelector('table.variations');
    form.insertBefore(controls, variationsTable || form.firstChild);
    form.classList.add('bes-single-variations-ready');
    form.dataset.besSingleVariationsReady = 'true';

    controls.querySelectorAll('[data-js="single-variation-color"]').forEach(function (button) {
      button.addEventListener('click', function () {
        if (button.disabled) {
          return;
        }

        var currentVariation = getCurrentVariation(form, state);
        var currentGeometry = getVariationAttribute(currentVariation, ATTRIBUTE_GEOMETRY);
        var nextVariation = findFallbackVariation(state.variations, button.getAttribute('data-variation-color'), currentGeometry);
        selectVariation(form, state, nextVariation);
      });
    });

    ['prev', 'next'].forEach(function (direction) {
      var button = controls.querySelector('[data-js="single-variation-geometry-' + direction + '"]');
      button.addEventListener('click', function () {
        var geometries = uniqueValues(state.variations, ATTRIBUTE_GEOMETRY);
        var currentVariation = getCurrentVariation(form, state);
        var currentGeometry = getVariationAttribute(currentVariation, ATTRIBUTE_GEOMETRY);
        var currentColor = getVariationAttribute(currentVariation, ATTRIBUTE_COLOR);
        var currentIndex = geometries.indexOf(currentGeometry);
        var offset = direction === 'next' ? 1 : -1;
        var nextIndex = (Math.max(0, currentIndex) + offset + geometries.length) % geometries.length;
        var nextVariation = findFallbackVariation(state.variations, currentColor, geometries[nextIndex]);

        selectVariation(form, state, nextVariation);
      });
    });

    updateControls(form, state, getCurrentVariation(form, state));

    if (window.jQuery) {
      window.jQuery(form).on('found_variation', function (event, variation) {
        updateControls(form, state, variation);
        scrollGalleryToVariation(variation);
      });
      window.jQuery(form).on('reset_data woocommerce_variation_has_changed', function () {
        updateControls(form, state, getCurrentVariation(form, state));
      });
    }
  }

  function init(root) {
    Array.prototype.slice.call((root || document).querySelectorAll('form.variations_form')).forEach(initForm);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      init(document);
    });
  } else {
    init(document);
  }

  window.__beslock_single_variations_init = init;
})();
