(function () {
  'use strict';

  function isValidEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  function setInvalid(field, invalid) {
    if (!field) return;
    if (invalid) {
      field.setAttribute('aria-invalid', 'true');
    } else {
      field.removeAttribute('aria-invalid');
    }
  }

  function showError(errorEl, message) {
    if (!errorEl) return;
    errorEl.textContent = message;
    errorEl.hidden = !message;
  }

  function setupForm(form) {
    if (!form || form.dataset.orderLookupReady === 'true') return;
    form.dataset.orderLookupReady = 'true';

    var orderInput = form.querySelector('[data-js="order-lookup-order"]');
    var emailInput = form.querySelector('[data-js="order-lookup-email"]');
    var errorEl = form.querySelector('[data-js="order-lookup-error"]');

    form.addEventListener('submit', function (event) {
      var orderValue = orderInput ? orderInput.value.trim() : '';
      var emailValue = emailInput ? emailInput.value.trim() : '';
      var orderMissing = !orderValue;
      var emailInvalid = !emailValue || !isValidEmail(emailValue);

      setInvalid(orderInput, orderMissing);
      setInvalid(emailInput, emailInvalid);

      if (orderMissing || emailInvalid) {
        event.preventDefault();
        showError(errorEl, 'Ingresa el número de pedido y un correo válido.');
        if (orderMissing && orderInput) {
          orderInput.focus();
        } else if (emailInvalid && emailInput) {
          emailInput.focus();
        }
        return;
      }

      try {
        window.sessionStorage.setItem(
          'beslockOrderLookup',
          JSON.stringify({ order: orderValue, email: emailValue, at: Date.now() })
        );
      } catch (error) {}
    });

    [orderInput, emailInput].forEach(function (field) {
      if (!field) return;
      field.addEventListener('input', function () {
        setInvalid(field, false);
        showError(errorEl, '');
      });
    });
  }

  function setupDrawerLookup() {
    var toggle = document.querySelector('[data-js="order-lookup-toggle"]');
    var panel = document.querySelector('[data-js="order-lookup-panel"]');
    var form = panel ? panel.querySelector('[data-js="order-lookup-form"]') : null;
    if (!toggle || !panel || !form) return;

    var item = toggle.closest('.mobile-menu__item--order-lookup');
    var orderInput = form.querySelector('[data-js="order-lookup-order"]');
    var errorEl = form.querySelector('[data-js="order-lookup-error"]');

    toggle.addEventListener('click', function () {
      var willOpen = panel.hidden;
      panel.hidden = !willOpen;
      toggle.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
      if (item) item.classList.toggle('is-open', willOpen);
      showError(errorEl, '');
      if (willOpen && orderInput) {
        window.setTimeout(function () {
          try { orderInput.focus({ preventScroll: true }); } catch (error) { orderInput.focus(); }
        }, 120);
      }
    });
  }

  function setupOrderLookup() {
    document.querySelectorAll('[data-js="order-lookup-form"]').forEach(function (form) {
      setupForm(form);
    });
    setupDrawerLookup();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupOrderLookup);
  } else {
    setupOrderLookup();
  }
})();
