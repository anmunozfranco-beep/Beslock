(function () {
  'use strict';

  var RESULT_TYPES = ['included', 'not-included', 'out-of-coverage'];

  var els = {};

  function ready(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  function setMessage(node, message, tone) {
    if (!node) return;
    node.textContent = message || '';
    node.hidden = !message;
    node.setAttribute('data-tone', tone || 'success');
    node.classList.toggle('is-visible', !!message);
  }

  function setDrawerMotionState(state) {
    if (!els.drawer) return;
    els.drawer.classList.remove('is-opening', 'is-closing');
    if (state) {
      els.drawer.classList.add(state);
      window.setTimeout(function () {
        if (els.drawer) els.drawer.classList.remove(state);
      }, 440);
    }
  }

  function closeSiblingPanels() {
    var manualsToggle = document.querySelector('[data-js="drawer-manuals-toggle"]');
    var manualsPanel = document.querySelector('[data-js="drawer-manuals-sections"]');
    var orderToggle = document.querySelector('[data-js="order-lookup-toggle"]');
    var orderPanel = document.querySelector('[data-js="order-lookup-panel"]');

    if (manualsToggle) manualsToggle.setAttribute('aria-expanded', 'false');
    if (manualsPanel) {
      manualsPanel.hidden = true;
      manualsPanel.setAttribute('aria-hidden', 'true');
    }
    if (els.mobileDrawer) els.mobileDrawer.classList.remove('manuals-menu-open');
    var manualsItem = manualsToggle && manualsToggle.closest ? manualsToggle.closest('.mobile-menu__item--manuals') : null;
    if (manualsItem) manualsItem.classList.remove('is-open');

    if (orderToggle) orderToggle.setAttribute('aria-expanded', 'false');
    if (orderPanel) orderPanel.hidden = true;
    var orderItem = orderToggle && orderToggle.closest ? orderToggle.closest('.mobile-menu__item--order-lookup') : null;
    if (orderItem) orderItem.classList.remove('is-open');
  }

  function announceSectionChange(section) {
    try {
      document.dispatchEvent(new CustomEvent('beslock:drawer-section-change', {
        detail: { section: section || 'support' }
      }));
    } catch (e) {}
  }

  function toggleSupportMenu(force) {
    if (!els.toggle || !els.optionsPanel) return;

    var willOpen = typeof force === 'boolean'
      ? force
      : els.toggle.getAttribute('aria-expanded') !== 'true';

    if (willOpen) closeSiblingPanels();

    els.toggle.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    els.optionsPanel.hidden = !willOpen;
    els.optionsPanel.setAttribute('aria-hidden', willOpen ? 'false' : 'true');

    if (els.supportItem) els.supportItem.classList.toggle('is-open', willOpen);
    if (els.mobileDrawer) els.mobileDrawer.classList.toggle('support-menu-open', willOpen);
  }

  function setActiveOption(target) {
    if (!els.optionButtons) return;

    for (var i = 0; i < els.optionButtons.length; i++) {
      var isActive = els.optionButtons[i].getAttribute('data-support-target') === target;
      els.optionButtons[i].classList.toggle('is-active', isActive);
      if (isActive) {
        els.optionButtons[i].setAttribute('aria-current', 'true');
      } else {
        els.optionButtons[i].removeAttribute('aria-current');
      }
    }
  }

  function showPanel(target) {
    var activePanel = null;

    for (var i = 0; i < els.panels.length; i++) {
      var panel = els.panels[i];
      var isActive = panel.getAttribute('data-support-panel') === target;
      panel.hidden = !isActive;
      panel.setAttribute('aria-hidden', isActive ? 'false' : 'true');
      panel.classList.toggle('is-active', isActive);
      if (isActive) activePanel = panel;
    }

    if (!activePanel) return null;

    if (els.eyebrow) els.eyebrow.textContent = 'Contacto';
    if (els.title) els.title.textContent = activePanel.getAttribute('data-support-title') || 'Soporte BESLOCK';

    return activePanel;
  }

  function openSupportDrawer(target) {
    if (!els.drawer || !els.body) return;
    announceSectionChange('support');

    var panel = showPanel(target || 'schedule-installation');
    if (!panel) return;

    if (els.mobileDrawer) {
      els.mobileDrawer.classList.add('is-open', 'support-sheet-open');
      els.mobileDrawer.setAttribute('aria-hidden', 'false');
    }
    if (els.backdrop) els.backdrop.classList.add('backdrop-visible');
    if (els.menuButton) els.menuButton.setAttribute('aria-expanded', 'true');

    els.drawer.classList.add('is-open');
    setDrawerMotionState('is-opening');
    els.drawer.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('has-drawer-open');
    setActiveOption(target);

    window.setTimeout(function () {
      try { els.body.focus({ preventScroll: true }); } catch (error) {}
    }, 60);
  }

  function closeSupportDrawer() {
    if (!els.drawer) return;

    els.drawer.classList.remove('is-open');
    setDrawerMotionState('is-closing');
    els.drawer.setAttribute('aria-hidden', 'true');
    if (els.mobileDrawer) els.mobileDrawer.classList.remove('support-sheet-open');
    if (!els.mobileDrawer || !els.mobileDrawer.classList.contains('is-open')) {
      document.documentElement.classList.remove('has-drawer-open');
    }
    setActiveOption(null);
  }

  function resetSupportNavigation() {
    closeSupportDrawer();
    toggleSupportMenu(false);

    if (els.panels) {
      for (var i = 0; i < els.panels.length; i++) {
        els.panels[i].hidden = true;
        els.panels[i].setAttribute('aria-hidden', 'true');
        els.panels[i].classList.remove('is-active');
      }
    }

    if (els.eyebrow) els.eyebrow.textContent = 'Contacto';
    if (els.title) els.title.textContent = 'Estamos para ayudarte';
    setActiveOption(null);

    try {
      document.querySelectorAll('[data-js="support-installation-results"], [data-support-result]').forEach(function (node) {
        node.hidden = true;
        node.classList.remove('is-active');
      });
      document.querySelectorAll('.support-form__message').forEach(function (node) {
        setMessage(node, '', 'success');
      });
    } catch (e) {}
  }

  function chooseMockInstallationResult(orderValue) {
    var digits = String(orderValue || '').replace(/\D/g, '');
    var lastDigit = digits ? parseInt(digits.charAt(digits.length - 1), 10) : 0;

    if (lastDigit <= 3) return 'included';
    if (lastDigit <= 6) return 'not-included';
    return 'out-of-coverage';
  }

  function showInstallationResult(type) {
    var resultsWrap = document.querySelector('[data-js="support-installation-results"]');
    var cards = resultsWrap ? resultsWrap.querySelectorAll('[data-support-result]') : [];
    if (!resultsWrap || !cards.length) return;

    resultsWrap.hidden = false;
    for (var i = 0; i < cards.length; i++) {
      var isActive = cards[i].getAttribute('data-support-result') === type;
      cards[i].hidden = !isActive;
      cards[i].classList.toggle('is-active', isActive);
    }
  }

  function setupConsultForm() {
    var form = document.querySelector('[data-js="support-installation-check-form"]');
    var message = document.querySelector('[data-js="support-installation-message"]');
    if (!form) return;

    form.addEventListener('submit', function (event) {
      event.preventDefault();

      if (!form.checkValidity()) {
        setMessage(message, 'Ingresa el número de pedido para continuar.', 'error');
        form.reportValidity();
        return;
      }

      var field = form.querySelector('[name="order_number"]');
      var result = chooseMockInstallationResult(field ? field.value : '');
      if (RESULT_TYPES.indexOf(result) === -1) result = RESULT_TYPES[0];

      setMessage(message, 'Resultado de referencia. Esta consulta queda lista para conectarse con WooCommerce.', 'neutral');
      showInstallationResult(result);
    });
  }

  function setupPreparedForm(selector, messageSelector, successMessage) {
    var form = document.querySelector(selector);
    var message = document.querySelector(messageSelector);
    if (!form) return;

    form.addEventListener('submit', function (event) {
      event.preventDefault();

      if (!form.checkValidity()) {
        setMessage(message, 'Completa los campos requeridos para continuar.', 'error');
        form.reportValidity();
        return;
      }

      setMessage(message, successMessage, 'success');
    });
  }

  function setSchedulePanelState(panel, active) {
    if (!panel) return;
    panel.hidden = !active;
    panel.setAttribute('aria-hidden', active ? 'false' : 'true');
    panel.classList.toggle('is-active', active);

    var fields = panel.querySelectorAll('input, select, textarea');
    for (var i = 0; i < fields.length; i++) {
      fields[i].disabled = !active;
    }
  }

  function setupScheduleForm() {
    var form = document.querySelector('[data-js="support-schedule-form"]');
    var message = document.querySelector('[data-js="support-schedule-message"]');
    var submit = document.querySelector('[data-js="support-schedule-submit"]');
    var intro = document.querySelector('[data-js="support-schedule-intro"]');
    if (!form) return;

    var DEFAULT_INTRO = 'Programa una instalación con tu número de pedido o solicita validación para un modelo BESLOCK.';
    var NO_ORDER_INTRO = 'Solicita validación para un modelo BESLOCK antes de comprar.';
    var ORDER_PURCHASED_INTRO = 'Programa tu instalación.';
    var ORDER_CAN_PURCHASE_INTRO = 'Adquiere y programa tu servicio de instalación.';
    var ORDER_COVERAGE_INTRO = 'Consulta cobertura en tu ubicación.';
    var orderIntro = DEFAULT_INTRO;

    var modeField = form.querySelector('[data-js="support-schedule-mode"]');
    var modeInputs = form.querySelectorAll('[name="beslock_installation_request_type"]');
    var tabButtons = form.querySelectorAll('[data-support-schedule-mode]');
    var panels = form.querySelectorAll('[data-support-schedule-panel]');
    var orderConfirm = form.querySelector('[data-js="support-order-confirm"]');
    var orderDetails = form.querySelector('[data-js="support-order-details"]');
    var orderAddress = form.querySelector('[data-js="support-order-address"]');
    var orderName = form.querySelector('[data-js="support-order-name"]');
    var orderPhone = form.querySelector('[data-js="support-order-phone"]');
    var orderCity = form.querySelector('[data-js="support-order-city"]');
    var orderStatus = form.querySelector('[data-js="support-order-status"]');
    var orderStatusTitle = form.querySelector('[data-js="support-order-status-title"]');
    var orderStatusText = form.querySelector('[data-js="support-order-status-text"]');
    var orderConfirmAction = form.querySelector('[data-js="support-order-confirm-action"]');
    var orderPurchase = form.querySelector('[data-js="support-order-purchase"]');
    var orderPurchaseItems = form.querySelector('[data-js="support-order-purchase-items"]');
    var orderPurchaseButton = form.querySelector('[data-js="support-order-purchase-button"]');
    var orderSchedule = form.querySelector('[data-js="support-order-schedule"]');
    var orderInfoRequest = form.querySelector('[data-js="support-order-info-request"]');
    var orderInfoRequestButton = form.querySelector('[data-js="support-order-info-request-button"]');
    var orderInfoRequestFields = orderInfoRequest ? orderInfoRequest.querySelectorAll('input, select, textarea') : [];
    var orderObservationsWrap = form.querySelector('[data-js="support-order-observations-wrap"]');
    var orderObservations = form.querySelector('[data-js="support-order-observations"]');
    var orderScheduleFields = orderSchedule ? orderSchedule.querySelectorAll('input, select, textarea') : [];
    var orderLookupFields = form.querySelectorAll('[name="order_number"], [name="order_email"]');
    var orderConfirmed = false;
    var orderScheduleReady = false;

    function getMode() {
      if (modeField && modeField.value) {
        return modeField.value;
      }

      var checked = form.querySelector('[name="beslock_installation_request_type"]:checked');
      return checked ? checked.value : 'order';
    }

    function setText(node, value) {
      if (!node) return;
      node.textContent = value && String(value).trim() ? value : 'No registrado';
    }

    function setIntro(value) {
      if (!intro) return;
      intro.textContent = value || DEFAULT_INTRO;
    }

    function setHidden(node, hidden) {
      if (!node) return;
      node.hidden = hidden;
      node.setAttribute('aria-hidden', hidden ? 'true' : 'false');
    }

    function setButtonVisible(button, visible) {
      if (!button) return;
      button.hidden = !visible;
      button.setAttribute('aria-hidden', visible ? 'false' : 'true');
      button.classList.toggle('is-hidden', !visible);
      button.style.display = visible ? '' : 'none';
    }

    function setNodeVisible(node, visible) {
      if (!node) return;
      node.hidden = !visible;
      node.setAttribute('aria-hidden', visible ? 'false' : 'true');
      node.classList.toggle('is-hidden', !visible);
      node.style.display = visible ? '' : 'none';
    }

    function isSuccessPayload(payload) {
      return !!(payload && typeof payload === 'object' && payload.success);
    }

    function getPayloadMessage(payload, fallback) {
      return payload && typeof payload === 'object' && payload.data && payload.data.message
        ? payload.data.message
        : fallback;
    }

    function parseAjaxPayload(response) {
      return response.json().catch(function () {
        return { success: false, data: { message: 'No pudimos procesar la respuesta del servidor.' } };
      });
    }

    function refreshScheduleNonce() {
      var nonceField = form.querySelector('[name="nonce"]');

      if (!nonceField || !window.fetch || !window.FormData) {
        return Promise.resolve();
      }

      var nonceData = new window.FormData();
      nonceData.set('action', 'beslock_support_installation_nonce');

      return window.fetch(form.getAttribute('action'), {
        method: 'POST',
        credentials: 'same-origin',
        body: nonceData
      })
        .then(parseAjaxPayload)
        .then(function (payload) {
          if (isSuccessPayload(payload) && payload.data && payload.data.nonce) {
            nonceField.value = payload.data.nonce;
          }
        })
        .catch(function () {});
    }

    function fillEmptyMessagePlaceholders(fields) {
      if (!fields) return;

      for (var i = 0; i < fields.length; i++) {
        var field = fields[i];
        var name = field && field.getAttribute ? field.getAttribute('name') : '';
        var isMessageField = name === 'installation_info_message' || name === 'installation_message';
        var placeholder = field && field.getAttribute ? field.getAttribute('placeholder') : '';

        if (
          isMessageField &&
          field.tagName &&
          field.tagName.toLowerCase() === 'textarea' &&
          !String(field.value || '').trim() &&
          String(placeholder || '').trim()
        ) {
          field.value = String(placeholder).trim();
        }
      }
    }

    function setOrderDetailsVisible(visible) {
      if (orderDetails) {
        orderDetails.hidden = !visible;
        orderDetails.setAttribute('aria-hidden', visible ? 'false' : 'true');
      }

      for (var i = 0; i < orderScheduleFields.length; i++) {
        orderScheduleFields[i].disabled = !visible || !orderScheduleReady;
      }
    }

    function setOrderInfoRequestVisible(visible) {
      setHidden(orderInfoRequest, !visible);

      for (var i = 0; i < orderInfoRequestFields.length; i++) {
        orderInfoRequestFields[i].disabled = !visible;
      }
    }

    function resetOrderConfirmation(clearAddress) {
      orderConfirmed = false;
      orderScheduleReady = false;
      setText(orderName, '-');
      setText(orderPhone, '-');
      setText(orderCity, '-');
      setText(orderStatusTitle, '-');
      setText(orderStatusText, '-');
      setText(orderObservations, '-');

      if (clearAddress) {
        for (var i = 0; i < orderScheduleFields.length; i++) {
          if (orderScheduleFields[i].type === 'checkbox' || orderScheduleFields[i].type === 'radio') {
            orderScheduleFields[i].checked = false;
          } else {
            orderScheduleFields[i].value = '';
          }
        }

        for (var j = 0; j < orderInfoRequestFields.length; j++) {
          if (orderInfoRequestFields[j].type === 'checkbox' || orderInfoRequestFields[j].type === 'radio') {
            orderInfoRequestFields[j].checked = false;
          } else {
            orderInfoRequestFields[j].value = '';
          }
        }
      }

      if (orderPurchaseItems) {
        orderPurchaseItems.innerHTML = '';
      }

      setHidden(orderStatus, true);
      setHidden(orderPurchase, true);
      setHidden(orderSchedule, true);
      setOrderInfoRequestVisible(false);
      setHidden(orderObservationsWrap, true);
      setOrderDetailsVisible(false);
      if (orderConfirm) orderConfirm.disabled = false;
      setNodeVisible(orderConfirmAction, true);
      setButtonVisible(orderConfirm, true);
      orderIntro = DEFAULT_INTRO;
      setIntro(getMode() === 'no_order' ? NO_ORDER_INTRO : DEFAULT_INTRO);
      updateSubmitState();
    }

    function renderPurchaseItems(items) {
      if (!orderPurchaseItems) return;
      orderPurchaseItems.innerHTML = '';

      if (!items || !items.length) {
        return;
      }

      for (var i = 0; i < items.length; i++) {
        var item = document.createElement('li');
        var name = document.createElement('span');
        var total = document.createElement('strong');
        var quantity = items[i].quantity && Number(items[i].quantity) > 1 ? ' x ' + items[i].quantity : '';
        var productName = items[i].name && String(items[i].name).trim() ? String(items[i].name).trim() : 'BESLOCK';
        var label = /^instalaci[oó]n\b/i.test(productName) ? productName : 'Instalación ' + productName;

        name.textContent = label + quantity;
        total.textContent = items[i].total_html || items[i].price_html || '';
        item.appendChild(name);
        item.appendChild(total);
        orderPurchaseItems.appendChild(item);
      }
    }

    function renderOrderDetails(order) {
      order = order || {};
      var installation = order.installation || {};

      orderConfirmed = true;
      orderScheduleReady = !!installation.purchased;
      setText(orderName, order.name);
      setText(orderPhone, order.phone);
      setText(orderCity, order.city);

      setHidden(orderStatus, false);
      setHidden(orderPurchase, true);
      setHidden(orderSchedule, true);
      setOrderInfoRequestVisible(false);
      setHidden(orderObservationsWrap, true);

      if (installation.purchased) {
        orderIntro = ORDER_PURCHASED_INTRO;
        setIntro(orderIntro);
        setText(orderStatusTitle, 'Instalación adquirida');
        setText(orderStatusText, 'Completa o ajusta los datos de instalación para coordinar la visita.');

        if (orderAddress) {
          orderAddress.value = order.address || '';
        }

        if (installation.customer_note && String(installation.customer_note).trim()) {
          setText(orderObservations, installation.customer_note);
          setHidden(orderObservationsWrap, false);
        }

        setHidden(orderSchedule, false);
      } else if (installation.can_purchase) {
        orderIntro = ORDER_CAN_PURCHASE_INTRO;
        setIntro(orderIntro);
        setText(orderStatusTitle, 'Instalación disponible para tu ubicación');
        setText(orderStatusText, 'El producto fue comprado para una ciudad con cobertura de instalación. Puedes comprar el servicio de instalación para este pedido.');
        renderPurchaseItems(installation.items || []);
        setHidden(orderPurchase, false);
      } else if (!installation.direct_available) {
        orderIntro = ORDER_COVERAGE_INTRO;
        setIntro(orderIntro);
        setText(orderStatusTitle, 'Instalación bajo consulta');
        setText(orderStatusText, 'El servicio de instalación se consultará para la ciudad del pedido y te informaremos si es posible prestarlo.');
        setOrderInfoRequestVisible(true);
      } else {
        orderIntro = ORDER_COVERAGE_INTRO;
        setIntro(orderIntro);
        setText(orderStatusTitle, 'Instalación disponible para tu ubicación');
        setText(orderStatusText, 'No encontramos un valor de instalación disponible para los productos de este pedido.');
      }

      setOrderDetailsVisible(true);
      setNodeVisible(orderConfirmAction, false);
      setButtonVisible(orderConfirm, false);
      updateSubmitState();
    }

    function updateSubmitState() {
      if (!submit) return;

      var mode = getMode();
      var hasVisibleOrderSchedule = !!(orderSchedule && orderScheduleReady && !orderSchedule.hidden);
      var shouldShow = mode === 'no_order' || hasVisibleOrderSchedule;

      submit.textContent = mode === 'no_order' ? 'Enviar consulta' : 'Programar instalación';
      submit.disabled = !shouldShow;
      setButtonVisible(submit, shouldShow);
    }

    function setMode(mode) {
      if (modeField) {
        modeField.value = mode;
      }

      for (var i = 0; i < modeInputs.length; i++) {
        if (modeInputs[i].type === 'radio') {
          modeInputs[i].checked = modeInputs[i].value === mode;
        }
      }

      updateMode();
    }

    function updateMode() {
      var mode = getMode();
      for (var i = 0; i < panels.length; i++) {
        setSchedulePanelState(panels[i], panels[i].getAttribute('data-support-schedule-panel') === mode);
      }

      if (mode === 'order') {
        setOrderDetailsVisible(orderConfirmed);
      }

      for (var j = 0; j < tabButtons.length; j++) {
        var isActive = tabButtons[j].getAttribute('data-support-schedule-mode') === mode;
        tabButtons[j].classList.toggle('is-active', isActive);
        tabButtons[j].setAttribute('aria-selected', isActive ? 'true' : 'false');
        tabButtons[j].setAttribute('tabindex', isActive ? '0' : '-1');
      }

      updateSubmitState();
      setIntro(mode === 'no_order' ? NO_ORDER_INTRO : orderIntro);
      setMessage(message, '', 'success');
    }

    for (var i = 0; i < modeInputs.length; i++) {
      modeInputs[i].addEventListener('change', function (event) {
        if (event.target && event.target.value) {
          setMode(event.target.value);
        } else {
          updateMode();
        }
      });
    }

    for (var j = 0; j < tabButtons.length; j++) {
      tabButtons[j].addEventListener('click', function (event) {
        event.preventDefault();
        setMode(event.currentTarget.getAttribute('data-support-schedule-mode') || 'order');
      });

      tabButtons[j].addEventListener('keydown', function (event) {
        var key = event.key || event.keyCode;
        var currentIndex = Array.prototype.indexOf.call(tabButtons, event.currentTarget);
        var nextIndex = currentIndex;

        if (key === 'ArrowRight' || key === 'Right' || key === 39) {
          nextIndex = (currentIndex + 1) % tabButtons.length;
        } else if (key === 'ArrowLeft' || key === 'Left' || key === 37) {
          nextIndex = (currentIndex - 1 + tabButtons.length) % tabButtons.length;
        } else if (key === 'Home' || key === 36) {
          nextIndex = 0;
        } else if (key === 'End' || key === 35) {
          nextIndex = tabButtons.length - 1;
        } else {
          return;
        }

        event.preventDefault();
        tabButtons[nextIndex].focus();
        setMode(tabButtons[nextIndex].getAttribute('data-support-schedule-mode') || 'order');
      });
    }

    for (var k = 0; k < orderLookupFields.length; k++) {
      orderLookupFields[k].addEventListener('input', function () {
        resetOrderConfirmation(true);
        setMessage(message, '', 'success');
      });
    }

    if (orderConfirm) {
      orderConfirm.addEventListener('click', function () {
        resetOrderConfirmation(true);

        for (var i = 0; i < orderLookupFields.length; i++) {
          if (!orderLookupFields[i].checkValidity()) {
            setMessage(message, 'Ingresa el número de pedido y el correo asociado a la compra.', 'error');
            orderLookupFields[i].reportValidity();
            return;
          }
        }

        if (!window.fetch || !window.FormData) {
          setMessage(message, 'No pudimos confirmar el pedido desde este navegador. Inténtalo nuevamente.', 'error');
          return;
        }

        orderConfirm.disabled = true;
        setMessage(message, 'Confirmando pedido...', 'neutral');

        refreshScheduleNonce()
          .then(function () {
            var formData = new window.FormData(form);
            formData.set('beslock_installation_request_type', 'order');
            formData.set('beslock_installation_step', 'lookup_order');

            return window.fetch(form.getAttribute('action'), {
              method: 'POST',
              credentials: 'same-origin',
              body: formData
            });
          })
          .then(parseAjaxPayload)
          .then(function (payload) {
            var text = getPayloadMessage(
              payload,
              isSuccessPayload(payload) ? 'Pedido confirmado.' : 'No pudimos confirmar el pedido. Recarga la página e inténtalo nuevamente.'
            );

            if (!isSuccessPayload(payload)) {
              setMessage(message, text, 'error');
              return;
            }

            renderOrderDetails(payload.data && payload.data.order ? payload.data.order : {});
            setMessage(message, text, 'success');
          })
          .catch(function () {
            setMessage(message, 'No pudimos confirmar el pedido. Inténtalo nuevamente.', 'error');
          })
          .finally(function () {
            if (orderConfirmed) {
              setNodeVisible(orderConfirmAction, false);
              setButtonVisible(orderConfirm, false);
            } else {
              orderConfirm.disabled = false;
            }
          });
      });
    }

    if (orderPurchaseButton) {
      orderPurchaseButton.addEventListener('click', function () {
        if (!orderConfirmed) {
          setMessage(message, 'Confirma el pedido antes de comprar la instalación.', 'error');
          return;
        }

        if (!window.fetch || !window.FormData) {
          setMessage(message, 'No pudimos iniciar la compra desde este navegador. Inténtalo nuevamente.', 'error');
          return;
        }

        orderPurchaseButton.disabled = true;
        setMessage(message, 'Preparando compra de instalación...', 'neutral');

        refreshScheduleNonce()
          .then(function () {
            var formData = new window.FormData(form);
            formData.set('beslock_installation_request_type', 'order');
            formData.set('beslock_installation_step', 'purchase_installation');

            return window.fetch(form.getAttribute('action'), {
              method: 'POST',
              credentials: 'same-origin',
              body: formData
            });
          })
          .then(parseAjaxPayload)
          .then(function (payload) {
            var text = getPayloadMessage(
              payload,
              isSuccessPayload(payload) ? 'Instalación agregada al carrito.' : 'No pudimos iniciar la compra. Recarga la página e inténtalo nuevamente.'
            );

            if (!isSuccessPayload(payload)) {
              setMessage(message, text, 'error');
              return;
            }

            setMessage(message, text, 'success');

            if (payload.data && payload.data.redirect) {
              window.location.href = payload.data.redirect;
            }
          })
          .catch(function () {
            setMessage(message, 'No pudimos iniciar la compra. Inténtalo nuevamente.', 'error');
          })
          .finally(function () {
            orderPurchaseButton.disabled = false;
          });
      });
    }

    if (orderInfoRequestButton) {
      orderInfoRequestButton.addEventListener('click', function () {
        if (!orderConfirmed) {
          setMessage(message, 'Confirma el pedido antes de solicitar información.', 'error');
          return;
        }

        if (!window.fetch || !window.FormData) {
          setMessage(message, 'No pudimos enviar la solicitud desde este navegador. Inténtalo nuevamente.', 'error');
          return;
        }

        fillEmptyMessagePlaceholders(orderInfoRequestFields);

        for (var i = 0; i < orderInfoRequestFields.length; i++) {
          if (!orderInfoRequestFields[i].checkValidity()) {
            setMessage(message, 'Ingresa tus observaciones o solicitudes.', 'error');
            orderInfoRequestFields[i].reportValidity();
            return;
          }
        }

        orderInfoRequestButton.disabled = true;
        setMessage(message, 'Enviando solicitud de información...', 'neutral');

        refreshScheduleNonce()
          .then(function () {
            var formData = new window.FormData(form);
            formData.set('beslock_installation_request_type', 'order');
            formData.set('beslock_installation_step', 'request_installation_info');

            return window.fetch(form.getAttribute('action'), {
              method: 'POST',
              credentials: 'same-origin',
              body: formData
            });
          })
          .then(parseAjaxPayload)
          .then(function (payload) {
            var text = getPayloadMessage(
              payload,
              isSuccessPayload(payload) ? 'Solicitud recibida.' : 'No pudimos enviar la solicitud. Recarga la página e inténtalo nuevamente.'
            );

            setMessage(message, text, isSuccessPayload(payload) ? 'success' : 'error');
          })
          .catch(function () {
            setMessage(message, 'No pudimos enviar la solicitud. Inténtalo nuevamente.', 'error');
          })
          .finally(function () {
            orderInfoRequestButton.disabled = false;
          });
      });
    }

    updateMode();

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      updateMode();

      if (getMode() === 'order' && !orderScheduleReady) {
        setMessage(message, 'Confirma el pedido antes de programar la instalación.', 'error');
        return;
      }

      fillEmptyMessagePlaceholders(form.querySelectorAll('textarea[name="installation_message"], textarea[name="installation_info_message"]'));

      if (!form.checkValidity()) {
        setMessage(message, 'Completa los campos requeridos para continuar.', 'error');
        form.reportValidity();
        return;
      }

      if (!window.fetch || !window.FormData) {
        setMessage(message, 'No pudimos enviar la solicitud desde este navegador. Inténtalo nuevamente.', 'error');
        return;
      }

      if (submit) submit.disabled = true;
      setMessage(message, 'Enviando solicitud...', 'neutral');

      refreshScheduleNonce()
        .then(function () {
          return window.fetch(form.getAttribute('action'), {
            method: 'POST',
            credentials: 'same-origin',
            body: new window.FormData(form)
          });
        })
        .then(parseAjaxPayload)
        .then(function (payload) {
          var text = getPayloadMessage(
            payload,
            isSuccessPayload(payload) ? 'Solicitud recibida.' : 'No pudimos enviar la solicitud. Recarga la página e inténtalo nuevamente.'
          );

          if (!isSuccessPayload(payload)) {
            setMessage(message, text, 'error');
            return;
          }

          form.reset();
          resetOrderConfirmation(true);
          updateMode();
          setMessage(message, text, 'success');
        })
        .catch(function () {
          setMessage(message, 'No pudimos enviar la solicitud. Inténtalo nuevamente.', 'error');
        })
        .finally(function () {
          updateSubmitState();
        });
    });
  }

  function updateProjectRemoveButtons() {
    var rows = document.querySelectorAll('[data-js="support-project-row"]');
    for (var i = 0; i < rows.length; i++) {
      var remove = rows[i].querySelector('[data-js="support-remove-product-row"]');
      if (remove) remove.hidden = rows.length <= 1;
    }
  }

  function createProjectRow() {
    var rows = document.querySelector('[data-js="support-project-rows"]');
    var first = rows ? rows.querySelector('[data-js="support-project-row"]') : null;
    if (!rows || !first) return;

    var clone = first.cloneNode(true);
    clone.querySelectorAll('input, select').forEach(function (field) {
      if (field.type === 'checkbox') {
        field.checked = false;
      } else if (field.getAttribute('name') === 'quantity[]') {
        field.value = '1';
      } else {
        field.value = '';
      }
    });
    clone.classList.add('is-new');
    rows.appendChild(clone);
    updateProjectRemoveButtons();
    window.setTimeout(function () {
      clone.classList.remove('is-new');
    }, 360);

    var firstField = clone.querySelector('select, input');
    if (firstField && typeof firstField.focus === 'function') {
      try { firstField.focus({ preventScroll: true }); } catch (error) { firstField.focus(); }
    }
  }

  function updateProjectQuantity(button, delta) {
    var control = button && button.closest ? button.closest('[data-js="support-project-qty"]') : null;
    var input = control ? control.querySelector('[name="quantity[]"]') : null;
    if (!input) return;

    var current = parseFloat(input.value);
    var step = parseFloat(input.getAttribute('step')) || 1;
    var min = parseFloat(input.getAttribute('min'));
    var max = parseFloat(input.getAttribute('max'));
    var next = (isNaN(current) ? min || 1 : current) + (delta * step);

    if (!isNaN(min)) next = Math.max(min, next);
    if (!isNaN(max)) next = Math.min(max, next);

    input.value = String(next);
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));

    if (typeof input.focus === 'function') {
      try { input.focus({ preventScroll: true }); } catch (error) { input.focus(); }
    }
  }

  function setupProjectRows() {
    var addButton = document.querySelector('[data-js="support-add-product-row"]');
    var rows = document.querySelector('[data-js="support-project-rows"]');

    if (addButton) {
      addButton.addEventListener('click', createProjectRow);
    }

    if (rows) {
      rows.addEventListener('click', function (event) {
        var qtyMinus = event.target && event.target.closest ? event.target.closest('[data-js="support-project-qty-minus"]') : null;
        var qtyPlus = event.target && event.target.closest ? event.target.closest('[data-js="support-project-qty-plus"]') : null;
        if (qtyMinus || qtyPlus) {
          event.preventDefault();
          updateProjectQuantity(qtyMinus || qtyPlus, qtyPlus ? 1 : -1);
          return;
        }

        var remove = event.target && event.target.closest ? event.target.closest('[data-js="support-remove-product-row"]') : null;
        if (!remove) return;

        var row = remove.closest('[data-js="support-project-row"]');
        if (row && rows.querySelectorAll('[data-js="support-project-row"]').length > 1) {
          row.classList.add('is-removing');
          window.setTimeout(function () {
            if (row && row.parentNode) {
              row.parentNode.removeChild(row);
              updateProjectRemoveButtons();
            }
          }, 180);
        }
      });

      rows.addEventListener('keydown', function (event) {
        var input = event.target && event.target.matches && event.target.matches('[name="quantity[]"]') ? event.target : null;
        if (!input || (event.key !== 'ArrowUp' && event.key !== 'ArrowDown')) return;

        event.preventDefault();
        updateProjectQuantity(input, event.key === 'ArrowUp' ? 1 : -1);
      });
    }

    updateProjectRemoveButtons();
  }

  function bindEvents() {
    if (!els.mobileDrawer || !els.toggle || !els.optionsPanel || !els.drawer) return;
    var manualsToggle = document.querySelector('[data-js="drawer-manuals-toggle"]');
    var orderToggle = document.querySelector('[data-js="order-lookup-toggle"]');

    els.toggle.addEventListener('click', function (event) {
      event.preventDefault();
      announceSectionChange('support');
      toggleSupportMenu();
    });

    if (manualsToggle) {
      manualsToggle.addEventListener('click', function () {
        closeSupportDrawer();
        toggleSupportMenu(false);
      });
    }

    if (orderToggle) {
      orderToggle.addEventListener('click', function () {
        closeSupportDrawer();
        toggleSupportMenu(false);
      });
    }

    els.optionButtons = els.optionsPanel.querySelectorAll('[data-support-target]');
    for (var i = 0; i < els.optionButtons.length; i++) {
      els.optionButtons[i].addEventListener('click', function () {
        openSupportDrawer(this.getAttribute('data-support-target'));
      });
    }

    document.addEventListener('click', function (event) {
      var trigger = event.target && event.target.closest ? event.target.closest('[data-support-target]') : null;
      if (!trigger || trigger.closest('[data-js="support-options"]')) return;
      event.preventDefault();
      openSupportDrawer(trigger.getAttribute('data-support-target'));
    });

    if (els.closeButton) {
      els.closeButton.addEventListener('click', closeSupportDrawer);
    }

    document.addEventListener('keydown', function (event) {
      if ((event.key === 'Escape' || event.key === 'Esc') && els.drawer.classList.contains('is-open')) {
        event.preventDefault();
        event.stopPropagation();
        closeSupportDrawer();
      }
    }, true);

    document.addEventListener('beslock:mobile-drawer-reset', resetSupportNavigation);
    document.addEventListener('beslock:drawer-section-change', function (event) {
      var section = event && event.detail ? event.detail.section : '';
      if (section && section !== 'support') {
        resetSupportNavigation();
      }
    });

    if (window.MutationObserver) {
      var observer = new MutationObserver(function () {
        var drawerClosed = !els.mobileDrawer.classList.contains('is-open');
        var supportActive = (els.drawer && els.drawer.classList.contains('is-open')) ||
          els.mobileDrawer.classList.contains('support-menu-open') ||
          els.mobileDrawer.classList.contains('support-sheet-open');

        if (drawerClosed && supportActive) {
          closeSupportDrawer();
          toggleSupportMenu(false);
        }
      });
      observer.observe(els.mobileDrawer, { attributes: true, attributeFilter: ['class', 'aria-hidden'] });
    }

    setupConsultForm();
    setupScheduleForm();
    setupPreparedForm(
      '[data-js="support-project-form"]',
      '[data-js="support-project-message"]',
      'Cotización preparada. El formulario queda listo para conectarse con el equipo comercial.'
    );
    setupProjectRows();
  }

  function init() {
    els.mobileDrawer = document.getElementById('mobileDrawer');
    els.toggle = document.querySelector('[data-js="support-toggle"]');
    els.supportItem = els.toggle ? els.toggle.closest('.mobile-menu__item--support') : null;
    els.optionsPanel = document.querySelector('[data-js="support-options"]');
    els.drawer = document.querySelector('[data-js="support-drawer"]');
    els.closeButton = document.querySelector('[data-js="support-drawer-close"]');
    els.body = document.querySelector('[data-js="support-drawer-body"]');
    els.eyebrow = document.querySelector('[data-js="support-drawer-eyebrow"]');
    els.title = document.querySelector('[data-js="support-drawer-title"]');
    els.backdrop = document.querySelector('[data-js="drawer-backdrop"], #drawerBackdrop');
    els.menuButton = document.getElementById('menuBtn');
    els.panels = document.querySelectorAll('[data-js="support-panel"]');

    bindEvents();
  }

  ready(init);
})();
