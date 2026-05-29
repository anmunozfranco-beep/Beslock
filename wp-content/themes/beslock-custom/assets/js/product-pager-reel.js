(function () {
  'use strict';

  var STORAGE_KEY = 'beslockProductPagerDirection';
  var EXIT_MS = 360;
  var ENTER_MS = 620;

  function ready(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn, { once: true });
      return;
    }

    fn();
  }

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function getDirection(link) {
    return link.classList.contains('product-page__pager-link--prev') ? 'prev' : 'next';
  }

  function getStoredDirection() {
    try {
      var value = window.sessionStorage.getItem(STORAGE_KEY);
      window.sessionStorage.removeItem(STORAGE_KEY);
      return value === 'prev' || value === 'next' ? value : '';
    } catch (error) {
      return '';
    }
  }

  function storeDirection(direction) {
    try {
      window.sessionStorage.setItem(STORAGE_KEY, direction);
    } catch (error) {}
  }

  function clearPendingReelState() {
    document.documentElement.classList.remove(
      'product-reel-pending',
      'product-reel-pending--prev',
      'product-reel-pending--next'
    );
  }

  function clearMotionState(body, preservePending) {
    body.classList.remove(
      'product-reel-enter',
      'product-reel-enter--prev',
      'product-reel-enter--next',
      'product-reel-leaving',
      'product-reel-leaving--prev',
      'product-reel-leaving--next'
    );

    if (!preservePending) clearPendingReelState();

    document.querySelectorAll('.product-page__pager-link.is-reeling').forEach(function (link) {
      link.classList.remove('is-reeling');
      link.removeAttribute('aria-disabled');
    });
  }

  function playEnter(body) {
    var direction = getStoredDirection();
    if (!direction || prefersReducedMotion()) {
      clearPendingReelState();
      return;
    }

    body.classList.add('product-reel-enter', 'product-reel-enter--' + direction);
    window.requestAnimationFrame(clearPendingReelState);

    window.setTimeout(function () {
      body.classList.remove('product-reel-enter', 'product-reel-enter--' + direction);
    }, ENTER_MS);
  }

  function shouldSkip(event, link) {
    if (event.defaultPrevented) return true;
    if (event.button && event.button !== 0) return true;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return true;
    if (link.target && link.target !== '_self') return true;
    if (prefersReducedMotion()) return true;

    try {
      var targetUrl = new URL(link.href, window.location.href);
      return targetUrl.origin !== window.location.origin || targetUrl.href === window.location.href;
    } catch (error) {
      return true;
    }
  }

  function initPager(body) {
    var links = Array.from(document.querySelectorAll('.product-page__pager-link'));
    if (!links.length) return;

    links.forEach(function (link) {
      link.addEventListener('click', function (event) {
        if (shouldSkip(event, link)) return;

        event.preventDefault();

        if (body.classList.contains('product-reel-leaving')) return;

        var direction = getDirection(link);
        var href = link.href;

        storeDirection(direction);
        link.classList.add('is-reeling');
        link.setAttribute('aria-disabled', 'true');
        body.classList.add('product-reel-leaving', 'product-reel-leaving--' + direction);

        window.setTimeout(function () {
          window.location.assign(href);
        }, EXIT_MS);
      });
    });
  }

  ready(function () {
    var body = document.body;
    if (!body || !body.classList.contains('single-product')) return;

    clearMotionState(body, true);
    playEnter(body);
    initPager(body);

    window.addEventListener('pageshow', function (event) {
      if (event.persisted) clearMotionState(body);
    });
  });
})();
