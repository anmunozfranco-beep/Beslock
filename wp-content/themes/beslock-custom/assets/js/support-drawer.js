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

    var panel = showPanel(target || 'consult-installation');
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

  function setupProjectRows() {
    var addButton = document.querySelector('[data-js="support-add-product-row"]');
    var rows = document.querySelector('[data-js="support-project-rows"]');

    if (addButton) {
      addButton.addEventListener('click', createProjectRow);
    }

    if (rows) {
      rows.addEventListener('click', function (event) {
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
    }

    updateProjectRemoveButtons();
  }

  function bindEvents() {
    if (!els.mobileDrawer || !els.toggle || !els.optionsPanel || !els.drawer) return;
    var manualsToggle = document.querySelector('[data-js="drawer-manuals-toggle"]');
    var orderToggle = document.querySelector('[data-js="order-lookup-toggle"]');

    els.toggle.addEventListener('click', function (event) {
      event.preventDefault();
      toggleSupportMenu();
    });

    if (manualsToggle) {
      manualsToggle.addEventListener('click', function () {
        toggleSupportMenu(false);
      });
    }

    if (orderToggle) {
      orderToggle.addEventListener('click', function () {
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
    setupPreparedForm(
      '[data-js="support-schedule-form"]',
      '[data-js="support-schedule-message"]',
      'Solicitud preparada. El formulario queda listo para conectarse con el flujo de programación.'
    );
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
