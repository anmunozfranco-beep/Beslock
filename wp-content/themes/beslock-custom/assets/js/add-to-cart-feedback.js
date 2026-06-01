(function ($) {
  'use strict';

  var config = window.BESLOCK_ADD_TO_CART || {};
  var toastTimer = null;

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

  function getProductName($button) {
    var explicitName = $button && ($button.attr('data-product-name') || $button.data('productName'));
    var cardName = $button && $button.closest('[data-js="product-card"]').find('.product-card__title, .bes-product-card__title').first().text();
    var pageName = $('.product-page__info .product_title, body.single-product .product_title').first().text();
    var fallback = config.defaultProductName || 'Producto';

    return $.trim(explicitName || cardName || pageName || fallback);
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

  function ensureToast() {
    var toast = document.querySelector('[data-js="beslock-cart-toast"]');
    if (toast) return toast;

    toast = document.createElement('div');
    toast.className = 'beslock-cart-toast';
    toast.setAttribute('data-js', 'beslock-cart-toast');
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.innerHTML = [
      '<span class="beslock-cart-toast__message" data-js="beslock-cart-toast-message"></span>',
      '<a class="beslock-cart-toast__button" data-js="beslock-cart-toast-link" href="' + getCartUrl() + '">Ver carrito</a>',
    ].join('');

    document.body.appendChild(toast);
    return toast;
  }

  function showToast(productName) {
    if (isCartPage()) return;

    var toast = ensureToast();
    var message = toast.querySelector('[data-js="beslock-cart-toast-message"]');
    var link = toast.querySelector('[data-js="beslock-cart-toast-link"]');

    if (message) {
      message.textContent = '"' + productName + '" se ha añadido a tu carrito.';
    }

    if (link) {
      link.href = getCartUrl();
    }

    window.clearTimeout(toastTimer);
    toast.classList.add('is-visible');

    toastTimer = window.setTimeout(function () {
      toast.classList.remove('is-visible');
    }, 5200);
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

    applyFragments(response.fragments);
    cleanInlineAddNotices();
    $(document.body).trigger('beslock_added_to_cart', [response.fragments, response.cart_hash, $button]);

    if (isCartPage()) {
      window.setTimeout(maybeRefreshEmptyCart, 0);
      return;
    }

    showToast(getProductName($button));
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

    $(document.body).on('click', '[data-js="product-card-add-to-cart"]', addProductCardByAjax);
    $(document.body).on('submit', 'form.cart', addSingleProductByAjax);

    $(document.body).on('added_to_cart', function (event, fragments, cartHash, $button) {
      cleanInlineAddNotices();
      window.setTimeout(cleanInlineAddNotices, 0);
    });

    $(document.body).on('wc_cart_button_updated', cleanInlineAddNotices);
  });
})(window.jQuery);
