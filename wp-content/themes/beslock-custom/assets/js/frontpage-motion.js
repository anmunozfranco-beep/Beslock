(function () {
  'use strict';

  function onReady(callback) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', callback, { once: true });
      return;
    }

    callback();
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  onReady(function () {
    var main = document.getElementById('main-content');
    var hero = document.querySelector('.beslock-hero');
    var cards = Array.prototype.slice.call(document.querySelectorAll('#main-content .product-card'));
    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!main || (!hero && !cards.length)) {
      return;
    }

    cards.forEach(function (card, index) {
      card.style.setProperty('--frontpage-card-index', String(index % 6));
    });

    if (reducedMotion) {
      cards.forEach(function (card) {
        card.classList.add('is-motion-visible');
      });
      document.body.classList.add('beslock-frontpage-motion');
      return;
    }

    if (cards.length) {
      if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries, io) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) {
              return;
            }

            entry.target.classList.add('is-motion-visible');
            io.unobserve(entry.target);
          });
        }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

        cards.forEach(function (card) {
          observer.observe(card);
        });
      } else {
        cards.forEach(function (card) {
          card.classList.add('is-motion-visible');
        });
      }
    }

    document.body.classList.add('beslock-frontpage-motion');

    if (hero) {
      var ticking = false;

      function updateHeroHandoff() {
        ticking = false;

        var rect = hero.getBoundingClientRect();
        var height = Math.max(rect.height || 1, 1);
        var progress = clamp(Math.abs(Math.min(rect.top, 0)) / (height * 0.72), 0, 1);

        document.body.style.setProperty('--frontpage-hero-progress', progress.toFixed(3));
      }

      function requestHeroHandoff() {
        if (ticking) {
          return;
        }

        ticking = true;
        window.requestAnimationFrame(updateHeroHandoff);
      }

      updateHeroHandoff();
      window.addEventListener('scroll', requestHeroHandoff, { passive: true });
      window.addEventListener('resize', requestHeroHandoff);
    }

    var feedbackTimer = 0;

    function getCartButton(event) {
      return event.target && event.target.closest
        ? event.target.closest('#main-content .product-card [data-js="product-card-add-to-cart"], #main-content .product-card .pc-btn-cart')
        : null;
    }

    function startCartFeedback(button) {
      window.clearTimeout(feedbackTimer);

      if (!button) {
        return;
      }

      button.classList.remove('is-adding');
      document.body.classList.remove('frontpage-cart-pulse');
      void button.offsetWidth;

      button.classList.add('is-adding');
      document.body.classList.add('frontpage-cart-pulse');

      feedbackTimer = window.setTimeout(function () {
        button.classList.remove('is-adding');
        document.body.classList.remove('frontpage-cart-pulse');
      }, 620);
    }

    document.addEventListener('pointerdown', function (event) {
      startCartFeedback(getCartButton(event));
    }, { passive: true });

    document.addEventListener('click', function (event) {
      var button = getCartButton(event);

      if (button && !button.classList.contains('is-adding')) {
        startCartFeedback(button);
      }
    }, false);
  });
}());
