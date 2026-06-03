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

  function setCartUpdateState(form, isDirty) {
    if (!form) return;
    var button = form.querySelector('button[name="update_cart"]');
    var status = form.querySelector('.beslock-cart__update-status');

    if (button) {
      button.hidden = !isDirty;
      button.disabled = !isDirty;

      if (isDirty) {
        button.style.removeProperty('display');
        button.removeAttribute('disabled');
        button.classList.remove('disabled');
      } else {
        button.style.setProperty('display', 'none', 'important');
        button.setAttribute('disabled', 'disabled');
        button.classList.add('disabled');
      }
    }

    if (status) {
      status.hidden = isDirty;
    }

    form.classList.toggle('beslock-cart-form--dirty', Boolean(isDirty));
  }

  function enableCartUpdate(form) {
    setCartUpdateState(form, true);
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

    setCartUpdateState(form, false);

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
    var localityField = form.querySelector('#calc_shipping_locality_field');
    var neighborhoodField = form.querySelector('#calc_shipping_neighborhood_field');
    var locality = form.querySelector('#calc_shipping_locality');
    var neighborhoodSelect = form.querySelector('#calc_shipping_neighborhood_select');
    var neighborhoodManual = form.querySelector('#calc_shipping_neighborhood');
    var address = form.querySelector('#calc_shipping_address_1');
    var areaHelp = form.querySelector('#beslock-shipping-area-help');
    var isBogota = false;

    if (!department || !city || !localityField || !neighborhoodField || !locality || !neighborhoodSelect || !neighborhoodManual || !address) return;

    form.dataset.beslockShippingValidation = 'ready';

    function normalizeLabels() {
      var cityLabel = form.querySelector('label[for="calc_shipping_city"]');
      var stateLabel = form.querySelector('label[for="calc_shipping_state"]');

      if (cityLabel) cityLabel.textContent = 'Ciudad / Municipio';
      if (stateLabel) stateLabel.textContent = 'Departamento';
    }

    function isSelect(field) {
      return field && field.tagName && field.tagName.toLowerCase() === 'select';
    }

    function getOriginalOptions(select) {
      if (!select._beslockOriginalOptions) {
        select._beslockOriginalOptions = Array.prototype.map.call(select.options, function (option) {
          return option.cloneNode(true);
        });
      }

      return select._beslockOriginalOptions;
    }

    function resetOptionState(option) {
      option.disabled = false;
      option.hidden = false;
      option.style.display = '';
      option.selected = false;
    }

    function replaceSelectOptions(select, sourceOptions, selectedValue) {
      var fragment = document.createDocumentFragment();
      var selectedStillAvailable = !selectedValue;

      sourceOptions.forEach(function (sourceOption) {
        var option = sourceOption.cloneNode(true);
        resetOptionState(option);

        if (option.value === selectedValue) {
          selectedStillAvailable = true;
        }

        fragment.appendChild(option);
      });

      while (select.firstChild) {
        select.removeChild(select.firstChild);
      }

      select.appendChild(fragment);
      select.value = selectedStillAvailable ? selectedValue : '';
    }

    function normalizeOptionValue(value) {
      return String(value || '')
        .trim()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase();
    }

    function isBogotaCity(value) {
      var normalizedValue = normalizeOptionValue(value);
      return normalizedValue === 'bogota' || normalizedValue === 'bogota d.c.' || normalizedValue === 'bogota dc';
    }

    function isPlaceholderValue(value) {
      var normalizedValue = normalizeOptionValue(value);
      return !normalizedValue ||
        normalizedValue === 'no aplica' ||
        normalizedValue === 'no aplica en mi ciudad' ||
        normalizedValue === 'no aparece en la lista';
    }

    function optionMatchesScope(option, scopeAttribute, scopeValue) {
      if (!option.value) return true;
      if (!scopeValue) return false;

      var optionScope = option.getAttribute(scopeAttribute);
      if (!optionScope) return false;

      return optionScope.split('|').some(function (scope) {
        var normalizedScope = scope.trim();
        return normalizedScope === '*' || normalizeOptionValue(normalizedScope) === normalizeOptionValue(scopeValue);
      });
    }

    function filterSelect(select, scopeAttribute, scopeValue) {
      if (!isSelect(select)) return;

      var selectedValue = select.value;
      var availableOptions = getOriginalOptions(select).filter(function (option) {
        return optionMatchesScope(option, scopeAttribute, scopeValue);
      });

      replaceSelectOptions(select, availableOptions, selectedValue);
      select.disabled = !scopeValue;
    }

    function setLocalityVisible(isVisible) {
      localityField.hidden = !isVisible;
      locality.disabled = !isVisible || !city.value;

      if (!isVisible) {
        locality.value = '';
        locality.setCustomValidity('');
      }
    }

    function setManualNeighborhood() {
      var label = neighborhoodField.querySelector('label');

      if (!neighborhoodManual.value && !isPlaceholderValue(neighborhoodSelect.value)) {
        neighborhoodManual.value = neighborhoodSelect.value;
      }

      if (isPlaceholderValue(neighborhoodManual.value)) {
        neighborhoodManual.value = '';
      }

      neighborhoodSelect.disabled = true;
      neighborhoodSelect.hidden = true;
      neighborhoodSelect.required = false;
      neighborhoodSelect.setCustomValidity('');

      neighborhoodManual.disabled = false;
      neighborhoodManual.hidden = false;
      neighborhoodManual.required = !isBogota;

      if (label) label.setAttribute('for', 'calc_shipping_neighborhood');
      if (areaHelp) {
        areaHelp.textContent = isBogota ?
          'Selecciona la localidad o ingresa el barrio para calcular la entrega.' :
          'Ingresa el barrio o sector para calcular la entrega.';
      }
    }

    function syncDependentFields() {
      filterSelect(city, 'data-department', department.value);

      var cityValue = city.value;
      isBogota = isBogotaCity(cityValue);

      setLocalityVisible(isBogota);
      if (isBogota) {
        filterSelect(locality, 'data-city', cityValue);
      } else {
        locality.value = '';
      }

      setManualNeighborhood();

      validateDepartment();
      validateCity();
      validateArea();
    }

    function validateArea() {
      var localityValue = isBogota && !localityField.hidden ? locality.value.trim() : '';
      var neighborhoodValue = neighborhoodManual.value.trim();
      var cleanLocality = isPlaceholderValue(localityValue) ? '' : localityValue;
      var cleanNeighborhood = isPlaceholderValue(neighborhoodValue) ? '' : neighborhoodValue;
      var message = '';

      if (isBogota && !cleanLocality && !cleanNeighborhood) {
        message = 'Selecciona la localidad o ingresa el barrio.';
      } else if (!isBogota && !cleanNeighborhood) {
        message = 'Ingresa el barrio o sector.';
      }

      locality.required = isBogota && !cleanNeighborhood;
      neighborhoodManual.required = !isBogota || (isBogota && !cleanLocality);
      locality.setCustomValidity(isBogota ? message : '');
      neighborhoodSelect.setCustomValidity('');
      neighborhoodManual.setCustomValidity(message);
    }

    function validateDepartment() {
      var message = department.value.trim() ? '' : 'Selecciona el departamento.';
      department.setCustomValidity(message);
    }

    function validateCity() {
      var message = city.value.trim() ? '' : 'Selecciona la Ciudad/Municipio.';
      city.setCustomValidity(message);
    }

    function validateAddress() {
      var message = address.value.trim() ? '' : 'Ingresa la dirección completa.';
      address.setCustomValidity(message);
    }

    function keepTypingInsideField(event) {
      var isSpace = event.key === ' ' || event.code === 'Space' || event.keyCode === 32;

      if (isSpace) {
        event.stopPropagation();
        event.stopImmediatePropagation();
      }
    }

    ['input', 'change'].forEach(function (eventName) {
      department.addEventListener(eventName, syncDependentFields);
      city.addEventListener(eventName, syncDependentFields);
      locality.addEventListener(eventName, syncDependentFields);
      neighborhoodSelect.addEventListener(eventName, validateArea);
      neighborhoodManual.addEventListener(eventName, validateArea);
      address.addEventListener(eventName, validateAddress);
    });

    ['keydown', 'keypress', 'keyup'].forEach(function (eventName) {
      address.addEventListener(eventName, keepTypingInsideField, true);
      neighborhoodManual.addEventListener(eventName, keepTypingInsideField, true);
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

  function initInstallationOption(root) {
    var forms = root.querySelectorAll('.beslock-cart-installation__form');

    forms.forEach(function (form) {
      if (form.dataset.beslockInstallation === 'ready') return;

      var checkbox = form.querySelector('input[name="beslock_include_installation"]');
      if (!checkbox || checkbox.disabled) return;

      form.dataset.beslockInstallation = 'ready';
      checkbox.addEventListener('change', function () {
        form.classList.add('is-updating');
        form.submit();
      });
    });
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
    initInstallationOption(document);
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
