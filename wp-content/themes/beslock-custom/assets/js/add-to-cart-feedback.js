(function ($) {
  'use strict';

  var config = window.BESLOCK_ADD_TO_CART || {};
  var fallbackFlightTimer = 0;
  var cartBuzzTimer = 0;
  var cartBuzzRemoveTimer = 0;
  var flightDuration = 960;
  var cartBuzzDelay = Number(config.cartBuzzDelay || window.BESLOCK_CART_BUZZ_DELAY) || 15000;

  function isCartPage() {
    return Boolean(config.isCart) || document.body.classList.contains('woocommerce-cart');
  }

  function wcAjaxUrl(endpoint) {
    if (window.wc_add_to_cart_params && window.wc_add_to_cart_params.wc_ajax_url) {
      return window.wc_add_to_cart_params.wc_ajax_url.toString().replace('%%endpoint%%', endpoint);
    }

    if (config.wcAjaxUrl) {
      return config.wcAjaxUrl.toString().replace('%%endpoint%%', endpoint);
    }

    return '';
  }

  function getCartUrl() {
    if (window.wc_add_to_cart_params && window.wc_add_to_cart_params.cart_url) {
      return window.wc_add_to_cart_params.cart_url;
    }

    return config.cartUrl || '/carrito/';
  }

  function getVisibleElement(selector) {
    var elements = document.querySelectorAll(selector);

    for (var i = 0; i < elements.length; i += 1) {
      var element = elements[i];
      var rect = element.getBoundingClientRect();
      var style = window.getComputedStyle(element);

      if (rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none') {
        return element;
      }
    }

    return null;
  }

  function getCartTarget() {
    return getVisibleElement('[data-js="header-cart"], .header__icon--cart');
  }

  function shouldReduceMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function getPointFromRect(rect) {
    return {
      x: rect.left + (rect.width / 2),
      y: rect.top + (rect.height / 2),
    };
  }

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function lerp(start, end, progress) {
    return start + ((end - start) * progress);
  }

  function easeFlight(progress) {
    return progress < 0.5
      ? 4 * progress * progress * progress
      : 1 - Math.pow(-2 * progress + 2, 3) / 2;
  }

  function cubicBezierPoint(p0, p1, p2, p3, progress) {
    var inverted = 1 - progress;
    var invertedSquared = inverted * inverted;
    var progressSquared = progress * progress;

    return {
      x: (invertedSquared * inverted * p0.x) + (3 * invertedSquared * progress * p1.x) + (3 * inverted * progressSquared * p2.x) + (progressSquared * progress * p3.x),
      y: (invertedSquared * inverted * p0.y) + (3 * invertedSquared * progress * p1.y) + (3 * inverted * progressSquared * p2.y) + (progressSquared * progress * p3.y),
    };
  }

  function getFlightScale(progress) {
    if (progress < 0.16) {
      return lerp(0.7, 1.08, progress / 0.16);
    }

    if (progress > 0.84) {
      return lerp(1, 0.44, (progress - 0.84) / 0.16);
    }

    return lerp(1.08, 0.94, (progress - 0.16) / 0.68);
  }

  function getFlightOpacity(progress) {
    if (progress < 0.12) {
      return lerp(0.28, 1, progress / 0.12);
    }

    if (progress > 0.92) {
      return lerp(1, 0.9, (progress - 0.92) / 0.08);
    }

    return 1;
  }

  function rememberAddOrigin($button, event) {
    if (!$button || !$button.length || !event || typeof event.clientX !== 'number') {
      return;
    }

    $button.data('beslockAddOrigin', {
      x: event.clientX,
      y: event.clientY,
      time: Date.now(),
    });
  }

  function getAddOrigin($button) {
    if ($button && $button.length && $button[0]) {
      var icon = $button[0].querySelector('.bi-cart, .bi-cart-plus, .bi-bag, .bi-bag-plus, svg, i');

      if (icon) {
        var iconRect = icon.getBoundingClientRect();

        if (iconRect.width > 0 && iconRect.height > 0) {
          return getPointFromRect(iconRect);
        }
      }

      return getPointFromRect($button[0].getBoundingClientRect());
    }

    var origin = $button && $button.data('beslockAddOrigin');

    if (origin && Date.now() - origin.time < 3000) {
      return {
        x: origin.x,
        y: origin.y,
      };
    }

    return null;
  }

  function showOriginCheck($button) {
    if (!$button || !$button.length || !$button[0]) {
      return;
    }

    var button = $button[0];

    window.clearTimeout(button.beslockCartAddedTimer);
    button.classList.remove('is-cart-added');
    void button.offsetWidth;
    button.classList.add('is-cart-added');

    button.beslockCartAddedTimer = window.setTimeout(function () {
      button.classList.remove('is-cart-added');
    }, 920);
  }

  function pulseCartTarget() {
    var cart = getCartTarget();
    var count = cart ? cart.querySelector('.header__cart-count') : null;

    if (!cart) {
      return;
    }

    window.clearTimeout(fallbackFlightTimer);
    cart.classList.remove('is-cart-receiving');
    if (count) {
      count.classList.remove('is-cart-count-updated');
    }

    void cart.offsetWidth;
    cart.classList.add('is-cart-receiving');
    if (count) {
      count.classList.add('is-cart-count-updated');
    }

    fallbackFlightTimer = window.setTimeout(function () {
      cart.classList.remove('is-cart-receiving');
      if (count) {
        count.classList.remove('is-cart-count-updated');
      }
    }, 760);

    scheduleCartBuzz();
  }

  function cartHasItems() {
    var cart = getCartTarget();
    var count = cart ? cart.querySelector('.header__cart-count') : null;
    var countValue = count ? parseInt((count.textContent || '').replace(/\D/g, ''), 10) : 0;

    return Boolean(count && !count.classList.contains('is-empty') && countValue > 0);
  }

  function triggerCartBuzz() {
    var cart = getCartTarget();

    if (!cart || !cartHasItems() || shouldReduceMotion() || document.hidden) {
      return;
    }

    window.clearTimeout(cartBuzzRemoveTimer);
    cart.classList.remove('is-cart-buzzing');
    void cart.offsetWidth;
    cart.classList.add('is-cart-buzzing');

    cartBuzzRemoveTimer = window.setTimeout(function () {
      cart.classList.remove('is-cart-buzzing');
    }, 900);
  }

  function scheduleCartBuzz() {
    window.clearTimeout(cartBuzzTimer);

    if (!cartHasItems() || shouldReduceMotion()) {
      return;
    }

    cartBuzzTimer = window.setTimeout(function () {
      triggerCartBuzz();
      scheduleCartBuzz();
    }, cartBuzzDelay);
  }

  function runCartFlight($button, onArrival) {
    var cart = getCartTarget();
    var origin = getAddOrigin($button);
    var reduceMotion = shouldReduceMotion();

    if (!cart || !origin || reduceMotion || isCartPage()) {
      if (typeof onArrival === 'function') {
        onArrival();
      }
      showOriginCheck($button);
      pulseCartTarget();
      return;
    }

    var target = cart.querySelector('.header__cart-count') || cart;
    var targetPoint = getPointFromRect(target.getBoundingClientRect());
    var deltaX = targetPoint.x - origin.x;
    var deltaY = targetPoint.y - origin.y;
    var distance = Math.sqrt((deltaX * deltaX) + (deltaY * deltaY)) || 1;
    var perpendicular = {
      x: -deltaY / distance,
      y: deltaX / distance,
    };
    var arcHeight = clamp(distance * 0.18, 80, 210);
    var swerve = clamp(distance * 0.08, 28, 86);
    var snakeAmplitude = clamp(distance * 0.025, 8, 24);
    var controlPointA = {
      x: origin.x + (deltaX * 0.18) + (perpendicular.x * swerve),
      y: origin.y + (deltaY * 0.12) - arcHeight + (perpendicular.y * swerve),
    };
    var controlPointB = {
      x: origin.x + (deltaX * 0.72) - (perpendicular.x * swerve * 0.56),
      y: origin.y + (deltaY * 0.76) - (arcHeight * 0.16) - (perpendicular.y * swerve * 0.56),
    };
    var particle = document.createElement('span');
    var size = 20;
    var didFinish = false;
    var animationFrame = 0;
    var startTime = 0;

    particle.className = 'beslock-cart-flight';
    particle.setAttribute('aria-hidden', 'true');
    particle.style.left = '0';
    particle.style.top = '0';
    particle.style.setProperty('--cart-flight-duration', flightDuration + 'ms');

    function finish() {
      if (didFinish) {
        return;
      }

      didFinish = true;
      window.cancelAnimationFrame(animationFrame);
      particle.style.transform = 'translate3d(' + (targetPoint.x - (size / 2)) + 'px, ' + (targetPoint.y - (size / 2)) + 'px, 0) scale(0.42)';
      particle.classList.add('is-landing');
      particle.style.opacity = '0';

      if (typeof onArrival === 'function') {
        onArrival();
      }

      showOriginCheck($button);
      pulseCartTarget();

      window.setTimeout(function () {
        particle.remove();
      }, 180);
    }

    function render(timestamp) {
      if (!startTime) {
        startTime = timestamp;
      }

      var rawProgress = Math.min((timestamp - startTime) / flightDuration, 1);
      var easedProgress = easeFlight(rawProgress);
      var point = cubicBezierPoint(origin, controlPointA, controlPointB, targetPoint, easedProgress);
      var snake = Math.sin(rawProgress * Math.PI * 3.3) * Math.sin(rawProgress * Math.PI) * snakeAmplitude;
      var x = point.x + (perpendicular.x * snake);
      var y = point.y + (perpendicular.y * snake);

      particle.style.opacity = getFlightOpacity(rawProgress);
      particle.style.transform = 'translate3d(' + (x - (size / 2)) + 'px, ' + (y - (size / 2)) + 'px, 0) scale(' + getFlightScale(rawProgress) + ')';

      if (rawProgress < 1) {
        animationFrame = window.requestAnimationFrame(render);
        return;
      }

      finish();
    }

    document.body.appendChild(particle);
    animationFrame = window.requestAnimationFrame(render);
    window.setTimeout(finish, flightDuration + 140);
  }

  function cleanInlineAddNotices() {
    $('.added_to_cart.wc-forward').remove();

    $('.woocommerce-notices-wrapper .woocommerce-message').each(function () {
      var text = $(this).text();
      if (text.indexOf('añadido') !== -1 || text.indexOf('agregado') !== -1 || text.indexOf('Ver carrito') !== -1) {
        $(this).remove();
      }
    });
  }

  function applyFragments(fragments) {
    if (!fragments) return;

    $.each(fragments, function (selector, value) {
      var $target = $(selector);

      if ($target.length) {
        $target.replaceWith(value);
      }
    });

    $(document.body).trigger('wc_fragments_loaded');
  }

  function handleSuccessfulAdd(response, $button) {
    if (!response) return;

    if (response.error && response.product_url) {
      window.location = response.product_url;
      return;
    }

    if (isCartPage()) {
      applyFragments(response.fragments);
      cleanInlineAddNotices();
      $(document.body).trigger('beslock_added_to_cart', [response.fragments, response.cart_hash, $button]);
      scheduleCartBuzz();
      window.setTimeout(maybeRefreshEmptyCart, 0);
      return;
    }

    runCartFlight($button, function () {
      applyFragments(response.fragments);
      cleanInlineAddNotices();
      $(document.body).trigger('beslock_added_to_cart', [response.fragments, response.cart_hash, $button]);
      scheduleCartBuzz();
    });
  }

  function addSingleProductByAjax(event) {
    var form = event.currentTarget;
    var $form = $(form);
    var $button = $form.find('.single_add_to_cart_button').first();
    var endpoint = wcAjaxUrl('add_to_cart');

    if (!document.body.classList.contains('single-product')) {
      return;
    }

    if (!endpoint || !$button.length || $button.is('.disabled, .wc-variation-selection-needed')) {
      return;
    }

    var productId = $button.val() || $form.find('[name="add-to-cart"]').val() || $form.find('[name="product_id"]').val();
    if (!productId) return;

    event.preventDefault();
    rememberAddOrigin($button, event);

    var quantity = $form.find('input.qty').first().val() || 1;
    var data = {
      product_id: productId,
      quantity: quantity,
    };

    $button.removeClass('added').addClass('loading');
    $(document.body).trigger('adding_to_cart', [$button, data]);

    $.ajax({
      type: 'POST',
      url: endpoint,
      data: data,
      dataType: 'json',
      success: function (response) {
        handleSuccessfulAdd(response, $button);
      },
      complete: function () {
        $button.removeClass('loading');
      },
    });
  }

  function addProductCardByAjax(event) {
    var link = event.currentTarget;
    var $button = $(link);
    var endpoint = wcAjaxUrl('add_to_cart');
    var productId = $button.attr('data-product_id') || $button.attr('data-product-id');

    if (!endpoint || !productId) {
      return;
    }

    event.preventDefault();
    rememberAddOrigin($button, event);

    var data = {
      product_id: productId,
      quantity: $button.attr('data-quantity') || 1,
    };

    $button.removeClass('added').addClass('loading');
    $(document.body).trigger('adding_to_cart', [$button, data]);

    $.ajax({
      type: 'POST',
      url: endpoint,
      data: data,
      dataType: 'json',
      success: function (response) {
        handleSuccessfulAdd(response, $button);
      },
      complete: function () {
        $button.removeClass('loading');
      },
    });
  }

  function maybeRefreshEmptyCart() {
    if (!isCartPage()) return;
    if (!document.querySelector('.beslock-cart--empty')) return;

    window.location.assign(getCartUrl());
  }

  $(function () {
    cleanInlineAddNotices();

    $(document.body).on('pointerdown', '[data-js="product-card-add-to-cart"], .single_add_to_cart_button, .add_to_cart_button', function (event) {
      rememberAddOrigin($(this), event.originalEvent || event);
    });

    $(document.body).on('click', '[data-js="product-card-add-to-cart"]', addProductCardByAjax);
    $(document.body).on('submit', 'form.cart', addSingleProductByAjax);

    $(document.body).on('added_to_cart', function (event, fragments, cartHash, $button) {
      cleanInlineAddNotices();
      window.setTimeout(cleanInlineAddNotices, 0);

      if (!isCartPage() && $button && $button.length) {
        runCartFlight($button, function () {
          scheduleCartBuzz();
        });
      }
    });

    $(document.body).on('wc_cart_button_updated', cleanInlineAddNotices);
    $(document.body).on('wc_fragments_loaded wc_fragments_refreshed updated_wc_div removed_from_cart', scheduleCartBuzz);
    scheduleCartBuzz();
  });
})(window.jQuery);
