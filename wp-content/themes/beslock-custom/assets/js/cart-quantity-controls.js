(function () {
  'use strict';

  function numberFrom(value, fallback) {
    var parsed = parseFloat(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  }

  function clamp(value, min, max) {
    if (Number.isFinite(min)) value = Math.max(value, min);
    if (Number.isFinite(max)) value = Math.min(value, max);
    return value;
  }

  function enableCartUpdate(form) {
    if (!form) return;
    var button = form.querySelector('button[name="update_cart"]');
    if (!button) return;
    button.disabled = false;
    button.removeAttribute('disabled');
    button.classList.remove('disabled');
  }

  function buildButton(label, delta, input, form) {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'beslock-cart-quantity__button';
    button.textContent = label;
    button.setAttribute('aria-label', delta < 0 ? 'Disminuir cantidad' : 'Aumentar cantidad');

    button.addEventListener('click', function () {
      var min = numberFrom(input.getAttribute('min'), 0);
      var maxAttr = input.getAttribute('max');
      var max = maxAttr && numberFrom(maxAttr, Infinity) > -1 ? numberFrom(maxAttr, Infinity) : Infinity;
      var step = Math.max(numberFrom(input.getAttribute('step'), 1), 1);
      var current = numberFrom(input.value, min || 0);
      var next = clamp(current + (delta * step), min, max);

      input.value = String(next);
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
      enableCartUpdate(form);
    });

    return button;
  }

  function init(root) {
    var form = root.querySelector('.woocommerce-cart-form');
    var inputs = root.querySelectorAll('.woocommerce-cart-form .quantity input.qty');

    inputs.forEach(function (input) {
      var wrapper = input.closest('.quantity');
      if (!wrapper || wrapper.dataset.beslockCartQuantity === 'ready') return;
      if (input.disabled || input.readOnly) return;

      wrapper.dataset.beslockCartQuantity = 'ready';
      wrapper.classList.add('beslock-cart-quantity');
      wrapper.insertBefore(buildButton('−', -1, input, form), input);
      wrapper.appendChild(buildButton('+', 1, input, form));

      input.addEventListener('input', function () {
        enableCartUpdate(form);
      });
      input.addEventListener('change', function () {
        enableCartUpdate(form);
      });
    });
  }

  function initShippingAddressValidation(root) {
    var form = root.querySelector('.woocommerce-shipping-calculator');
    if (!form || form.dataset.beslockShippingValidation === 'ready') return;

    var department = form.querySelector('#calc_shipping_state');
    var city = form.querySelector('#calc_shipping_city');
    var locality = form.querySelector('#calc_shipping_locality');
    var neighborhood = form.querySelector('#calc_shipping_neighborhood');
    var address = form.querySelector('#calc_shipping_address_1');

    if (!department || !city || !locality || !neighborhood || !address) return;

    form.dataset.beslockShippingValidation = 'ready';

    function normalizeLabels() {
      var cityLabel = form.querySelector('label[for="calc_shipping_city"]');
      var stateLabel = form.querySelector('label[for="calc_shipping_state"]');

      if (cityLabel) cityLabel.textContent = 'Ciudad / municipio';
      if (stateLabel) stateLabel.textContent = 'Departamento';
    }

    function isSelect(field) {
      return field && field.tagName && field.tagName.toLowerCase() === 'select';
    }

    function setOptionAvailability(option, isAvailable) {
      option.disabled = !isAvailable;
      option.hidden = !isAvailable;
      option.style.display = isAvailable ? '' : 'none';
    }

    function optionMatchesScope(option, scopeAttribute, scopeValue) {
      if (!option.value) return true;
      if (!scopeValue) return false;

      var optionScope = option.getAttribute(scopeAttribute);
      if (!optionScope) return false;

      return optionScope.split('|').some(function (scope) {
        var normalizedScope = scope.trim();
        return normalizedScope === '*' || normalizedScope === scopeValue;
      });
    }

    function filterSelect(select, scopeAttribute, scopeValue) {
      if (!isSelect(select)) return;

      var selectedValue = select.value;
      var selectedStillAvailable = !selectedValue;

      Array.prototype.forEach.call(select.options, function (option) {
        var isAvailable = optionMatchesScope(option, scopeAttribute, scopeValue);
        setOptionAvailability(option, isAvailable);

        if (isAvailable && option.value === selectedValue) {
          selectedStillAvailable = true;
        }
      });

      select.disabled = !scopeValue;

      if (!selectedStillAvailable) {
        select.value = '';
      }
    }

    function filterNeighborhoodSelect() {
      if (!isSelect(neighborhood)) return;

      var cityValue = city.value;
      var areaValue = locality.value;
      var selectedValue = neighborhood.value;
      var selectedStillAvailable = !selectedValue;

      Array.prototype.forEach.call(neighborhood.options, function (option) {
        var isAvailable = optionMatchesScope(option, 'data-city', cityValue);

        if (isAvailable && areaValue) {
          isAvailable = optionMatchesScope(option, 'data-area', areaValue);
        }

        setOptionAvailability(option, isAvailable);

        if (isAvailable && option.value === selectedValue) {
          selectedStillAvailable = true;
        }
      });

      neighborhood.disabled = !cityValue;

      if (!selectedStillAvailable) {
        neighborhood.value = '';
      }
    }

    function syncDependentFields() {
      filterSelect(city, 'data-department', department.value);
      filterSelect(locality, 'data-city', city.value);
      filterNeighborhoodSelect();

      validateDepartment();
      validateCity();
      validateArea();
    }

    function validateArea() {
      var hasArea = locality.value.trim() || neighborhood.value.trim();
      var message = hasArea ? '' : 'Ingresa una localidad/comuna o un barrio.';

      locality.setCustomValidity(message);
      neighborhood.setCustomValidity(message);
    }

    function validateDepartment() {
      var message = department.value.trim() ? '' : 'Selecciona el departamento.';
      department.setCustomValidity(message);
    }

    function validateCity() {
      var message = city.value.trim() ? '' : 'Selecciona la ciudad/municipio.';
      city.setCustomValidity(message);
    }

    function validateAddress() {
      var message = address.value.trim() ? '' : 'Ingresa la dirección completa.';
      address.setCustomValidity(message);
    }

    ['input', 'change'].forEach(function (eventName) {
      department.addEventListener(eventName, syncDependentFields);
      city.addEventListener(eventName, syncDependentFields);
      locality.addEventListener(eventName, syncDependentFields);
      neighborhood.addEventListener(eventName, validateArea);
      address.addEventListener(eventName, validateAddress);
    });

    form.addEventListener('submit', function () {
      normalizeLabels();
      validateDepartment();
      validateCity();
      validateArea();
      validateAddress();
    });

    document.body.addEventListener('country_to_state_changed', function () {
      window.setTimeout(normalizeLabels, 0);
    });

    normalizeLabels();
    syncDependentFields();
    validateDepartment();
    validateCity();
    validateArea();
    validateAddress();
  }

  function getCartUrl() {
    if (window.wc_cart_params && window.wc_cart_params.cart_url) {
      return window.wc_cart_params.cart_url;
    }

    return window.location.href.split('#')[0];
  }

  function getCleanEmptyCartUrl() {
    var url = new URL(getCartUrl(), window.location.origin);
    url.searchParams.set('beslock_empty_cart', '1');
    return url.href;
  }

  function removeCleanEmptyCartParam() {
    var url = new URL(window.location.href);

    if (!url.searchParams.has('beslock_empty_cart')) return;

    url.searchParams.delete('beslock_empty_cart');
    window.history.replaceState({}, '', url.pathname + url.search + url.hash);
  }

  function hasCompleteEmptyCartView() {
    return Boolean(
      document.querySelector('.beslock-cart--empty .beslock-cart__recommendations .product-card')
    );
  }

  function hasIncompleteEmptyCartView() {
    var hasAnyEmptyMessage = document.querySelector('.wc-empty-cart-message, .cart-empty');
    var hasBeslockEmpty = document.querySelector('.beslock-cart--empty');

    return Boolean(hasAnyEmptyMessage && (!hasBeslockEmpty || !hasCompleteEmptyCartView()));
  }

  function redirectToCompleteEmptyCartView() {
    var reloadKey = 'beslockEmptyCartRedirected';

    if (window.sessionStorage && window.sessionStorage.getItem(reloadKey) === '1') {
      return;
    }

    if (window.sessionStorage) {
      window.sessionStorage.setItem(reloadKey, '1');
    }

    window.location.replace(getCleanEmptyCartUrl());
  }

  function recoverEmptyCartViewIfBlank() {
    var isCartPage = document.body.classList.contains('woocommerce-cart');

    if (!isCartPage) return;
    removeCleanEmptyCartParam();

    if (hasCompleteEmptyCartView()) {
      if (window.sessionStorage) {
        window.sessionStorage.removeItem('beslockEmptyCartRedirected');
      }
      return;
    }

    if (hasIncompleteEmptyCartView()) {
      redirectToCompleteEmptyCartView();
      return;
    }

    if (document.querySelector('.woocommerce-cart-form')) return;
    if (document.querySelector('.beslock-cart--empty, .wc-empty-cart-message')) return;

    var woocommerceShell = document.querySelector('.woocommerce');
    var hasVisibleWooContent = woocommerceShell && woocommerceShell.textContent.trim().length > 0;

    if (hasVisibleWooContent) return;

    window.location.assign(getCartUrl());
  }

  function reloadCartAsEmptyIfNeeded() {
    var form = document.querySelector('.woocommerce-cart-form');
    if (!form) {
      recoverEmptyCartViewIfBlank();
      return;
    }

    if (form.querySelector('.cart_item')) {
      return;
    }

    var targetUrl = getCartUrl();
    var currentUrl = window.location.href.split('#')[0];

    document.body.classList.add('beslock-cart--refreshing-empty');

    if (hasIncompleteEmptyCartView()) {
      redirectToCompleteEmptyCartView();
      return;
    }

    if (new URL(targetUrl, window.location.origin).href === new URL(currentUrl, window.location.origin).href) {
      window.location.replace(getCleanEmptyCartUrl());
      return;
    }

    window.location.assign(getCleanEmptyCartUrl());
  }

  function refreshCartEnhancements() {
    init(document);
    initShippingAddressValidation(document);
    recoverEmptyCartViewIfBlank();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', refreshCartEnhancements);
  } else {
    refreshCartEnhancements();
  }

  if (window.jQuery && window.jQuery.fn) {
    window.jQuery(document.body).on(
      'updated_wc_div updated_cart_totals wc_fragments_refreshed removed_from_cart added_to_cart',
      function () {
        window.setTimeout(refreshCartEnhancements, 0);
      }
    );

    window.jQuery(document.body).on('removed_from_cart updated_wc_div wc_cart_emptied item_removed_from_classic_cart', function () {
      window.setTimeout(reloadCartAsEmptyIfNeeded, 0);
    });
  }

  window.__beslock_cart_refresh = refreshCartEnhancements;
})();
