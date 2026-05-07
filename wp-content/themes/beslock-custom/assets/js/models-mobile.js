/**
 * assets/js/models-mobile.js
 * Passive enhancer for the mobile products models surface.
 * State ownership for open/close now lives in main.js + components/mobile-drawer.js.
 * This file keeps image focal points and fallback handling only.
 */

( function () {
  'use strict';

  var clsHidden = 'models--hidden';
  var clsVisible = 'models--visible';
  var initEnforced = false;

  function getById(id) { return document.getElementById(id); }

  function ensureClosedState(panel, toggle) {
    if ( panel ) {
      panel.classList.add(clsHidden);
      panel.classList.remove(clsVisible);
      panel.setAttribute('aria-hidden', 'true');
      panel.style.display = '';
    }
    if ( toggle ) {
      toggle.setAttribute('aria-expanded', 'false');
    }
  }

  function initImageFallback(imgEl) {
    if (!imgEl) return;
    imgEl.addEventListener('error', function () {
      try {
        var src = imgEl.getAttribute('src') || '';
        if ( src.indexOf('.webp') !== -1 ) {
          imgEl.src = src.replace('.webp', '.png');
        } else if ( src.indexOf('.png') !== -1 ) {
          // If PNG fails, try jpg
          imgEl.src = src.replace('.png', '.jpg');
        } else {
          imgEl.classList.add('models__item-img--broken');
        }
      } catch (e) {
        imgEl.classList.add('models__item-img--broken');
      }
    }, false);

    imgEl.addEventListener('load', function () {
      if ( imgEl.naturalWidth === 0 ) {
        var src = imgEl.getAttribute('src') || '';
        if ( src.indexOf('.webp') !== -1 ) {
          imgEl.src = src.replace('.webp', '.png');
        }
      }
    }, false);
  }

  function applyFocalPoints(panel) {
    // For each image in the panel, read data-object-position and apply style
    var imgs = panel.querySelectorAll('.models__item-img');
    if ( ! imgs || imgs.length === 0 ) return;

    imgs.forEach(function (img) {
      try {
        var focal = img.getAttribute('data-object-position') || img.dataset.objectPosition || '';
        if ( focal && typeof focal === 'string' ) {
          img.style.objectPosition = focal;
        } else {
          // default center
          img.style.objectPosition = 'center center';
        }
      } catch (e) {
        // ignore and leave default
      }
    });
  }

  function init() {
    if ( initEnforced ) return;
    initEnforced = true;

    var toggle = getById('productsToggle');
    var panel = getById('productsPanel');

    if ( ! panel ) {
      return;
    }

    // Enforce closed state at initialization
    ensureClosedState(panel, toggle);

    // Apply focal points immediately (for images present)
    applyFocalPoints(panel);

    // Initialize image fallback for all images inside the panel
    var imgs = panel.querySelectorAll('.models__item-img');
    if ( imgs && imgs.length ) {
      imgs.forEach(function(img){
        initImageFallback(img);
      });
    }

    // Extra enforcement shortly after load in case other scripts modify DOM early:
    setTimeout(function () {
      ensureClosedState(panel, toggle);
      // Reapply focal points in case images loaded later
      applyFocalPoints(panel);
    }, 120);
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();