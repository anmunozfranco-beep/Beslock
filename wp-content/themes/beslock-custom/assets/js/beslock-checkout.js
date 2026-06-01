(function () {
  "use strict";

  var checkoutSelector = ".wp-block-woocommerce-checkout, .wc-block-checkout";
  var nativeSelectors = {
    firstName: [
      'input[autocomplete="given-name"]',
      'input[id*="first_name"]',
      'input[name*="first_name"]'
    ],
    lastName: [
      'input[autocomplete="family-name"]',
      'input[id*="last_name"]',
      'input[name*="last_name"]'
    ],
    email: [
      'input[type="email"]',
      'input[autocomplete="email"]',
      'input[id*="email"]',
      'input[name*="email"]'
    ],
    orderNote: [
      'textarea[id*="order"]',
      'textarea[name*="order"]',
      'textarea[id*="note"]',
      'textarea[name*="note"]'
    ]
  };
  var textMap = {
    "Contact information": "Información de contacto",
    "Email address": "Correo electrónico",
    "Currently checking out as guest.": "Estás finalizando la compra como invitado.",
    "Shipping address": "Dirección de envío",
    "Shipping options": "Opciones de envío",
    "Payment options": "Opciones de pago",
    "Order summary": "Resumen del pedido",
    "Add coupons": "Agregar cupón",
    "+ Add apartment, suite, etc.": "+ Agregar apartamento, interior, torre, etc.",
    "+ Add apartamento, habitación, etc.": "+ Agregar apartamento, interior, torre, etc.",
    "Free shipping": "Envío gratis",
    "Free Shipping": "Envío gratis",
    "Phone (optional)": "Teléfono (opcional)",
    "Postcode (optional)": "Código postal (opcional)",
    "Place Order": "Confirmar pedido",
    "Place order": "Confirmar pedido",
    "There are no payment methods available. Please contact us for help placing your order.": "Estamos preparando las opciones de pago para tu ubicación. Escríbenos y finalizamos tu pedido contigo."
  };
  var touchedFields = {};

  function normalizeText(value) {
    return String(value || "").replace(/\s+/g, " ").trim();
  }

  function buildProgressItem(number, label, state) {
    var item = document.createElement("li");
    item.className = "beslock-checkout-progress__item" + (state ? " " + state : "");

    var numberNode = document.createElement("span");
    numberNode.className = "beslock-checkout-progress__number";
    numberNode.textContent = String(number);

    var labelNode = document.createElement("span");
    labelNode.className = "beslock-checkout-progress__label";
    labelNode.textContent = label;

    item.appendChild(numberNode);
    item.appendChild(labelNode);

    return item;
  }

  function ensureCheckoutTop() {
    var checkout = document.querySelector(checkoutSelector);

    if (!checkout || document.querySelector(".beslock-checkout-top")) {
      return;
    }

    var top = document.createElement("div");
    top.className = "beslock-checkout-top";

    var progress = document.createElement("ol");
    progress.className = "beslock-checkout-progress";
    progress.setAttribute("aria-label", "Proceso de compra");
    progress.appendChild(buildProgressItem(1, "Carrito", "is-complete"));
    progress.appendChild(buildProgressItem(2, "Entrega", "is-active"));
    progress.appendChild(buildProgressItem(3, "Pago", ""));

    top.appendChild(progress);

    checkout.parentNode.insertBefore(top, checkout);
    document.body.classList.add("beslock-checkout-ready");
  }

  function getConfig() {
    return window.BESLOCK_CHECKOUT || {};
  }

  function getLabels() {
    var config = getConfig();

    return config.labels || {};
  }

  function getNativeField(key) {
    var selectors = nativeSelectors[key] || [];
    var index;
    var field;

    for (index = 0; index < selectors.length; index += 1) {
      field = document.querySelector(selectors[index]);

      if (field) {
        return field;
      }
    }

    return null;
  }

  function getNativeValue(key) {
    var field = getNativeField(key);

    return field ? field.value : "";
  }

  function setNativeValue(field, value) {
    var proto = field instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    var descriptor = Object.getOwnPropertyDescriptor(proto, "value");

    if (descriptor && descriptor.set) {
      descriptor.set.call(field, value);
    } else {
      field.value = value;
    }

    field.dispatchEvent(new Event("input", { bubbles: true }));
    field.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function syncNativeField(key, value) {
    var field = getNativeField(key);

    if (!field || field.value === value) {
      return;
    }

    setNativeValue(field, value);
  }

  function createField(key, label, type) {
    var wrapper = document.createElement("label");
    wrapper.className = "beslock-checkout-contact__field beslock-checkout-contact__field--" + key;

    var labelNode = document.createElement("span");
    labelNode.className = "beslock-checkout-contact__label";
    labelNode.textContent = label;

    var input = document.createElement(type === "textarea" ? "textarea" : "input");
    input.className = "beslock-checkout-contact__control";
    input.name = "beslock_checkout_" + key;
    input.setAttribute("data-beslock-checkout-field", key);

    if (type === "textarea") {
      input.rows = 4;
    } else {
      input.type = type || "text";
    }

    if (key !== "orderNote") {
      input.required = true;
    }

    input.addEventListener("input", function () {
      touchedFields[key] = true;
      syncNativeField(key, input.value);
    });

    wrapper.appendChild(labelNode);
    wrapper.appendChild(input);

    return wrapper;
  }

  function ensureCheckoutDetails() {
    var checkout = document.querySelector(checkoutSelector);
    var checkoutMain = document.querySelector(".wc-block-components-main, .wc-block-checkout__main");
    var labels = getLabels();
    var config = getConfig();
    var existing = document.querySelector(".beslock-checkout-details");
    var contact;
    var shipping;
    var address;
    var addressText;
    var addressButton;

    if (!checkout) {
      return;
    }

    if (existing) {
      if (checkoutMain && existing.parentNode !== checkoutMain) {
        checkoutMain.insertBefore(existing, checkoutMain.firstChild);
      }
      return;
    }

    var details = document.createElement("section");
    details.className = "beslock-checkout-details";
    details.setAttribute("aria-label", "Datos para finalizar la compra");

    contact = document.createElement("div");
    contact.className = "beslock-checkout-contact";

    var title = document.createElement("h2");
    title.className = "beslock-checkout-section-title";
    title.textContent = labels.contactTitle || "Datos de contacto";

    var fields = document.createElement("div");
    fields.className = "beslock-checkout-contact__fields";
    fields.appendChild(createField("firstName", labels.firstName || "Nombre", "text"));
    fields.appendChild(createField("lastName", labels.lastName || "Apellido", "text"));
    fields.appendChild(createField("email", labels.email || "Correo electrónico", "email"));

    var noteField = createField("orderNote", labels.orderNote || "Añadir una nota a tu pedido", "textarea");
    noteField.classList.add("beslock-checkout-contact__field--full");

    var noteHelp = document.createElement("span");
    noteHelp.className = "beslock-checkout-contact__help";
    noteHelp.textContent = labels.orderNoteHelp || "Puedes contarnos detalles de entrega, instalación o coordinación.";
    noteField.appendChild(noteHelp);
    fields.appendChild(noteField);

    contact.appendChild(title);
    contact.appendChild(fields);

    shipping = document.createElement("aside");
    shipping.className = "beslock-checkout-shipping-summary";

    var shippingTitle = document.createElement("h2");
    shippingTitle.className = "beslock-checkout-section-title";
    shippingTitle.textContent = labels.shippingTitle || "Datos de envío";

    address = document.createElement("div");
    address.className = "beslock-checkout-shipping-summary__address";

    addressText = document.createElement("p");
    addressText.className = "beslock-checkout-shipping-summary__text";
    addressText.setAttribute("data-beslock-shipping-summary-text", "true");
    addressText.textContent = config.shippingDestination || labels.shippingFallback || "La entrega se tomará de la dirección confirmada en el carrito.";

    addressButton = document.createElement("a");
    addressButton.className = "beslock-checkout-shipping-summary__edit";
    addressButton.href = config.cartUrl || "/carrito/";
    addressButton.textContent = labels.editShipping || "Editar en carrito";

    address.appendChild(addressText);
    address.appendChild(addressButton);
    shipping.appendChild(shippingTitle);
    shipping.appendChild(address);

    details.appendChild(contact);
    details.appendChild(shipping);

    if (checkoutMain) {
      checkoutMain.insertBefore(details, checkoutMain.firstChild);
    } else {
      checkout.parentNode.insertBefore(details, checkout);
    }
  }

  function hydrateCustomFields() {
    var config = getConfig();
    var values = {
      firstName: getNativeValue("firstName") || (config.contact && config.contact.firstName) || "",
      lastName: getNativeValue("lastName") || (config.contact && config.contact.lastName) || "",
      email: getNativeValue("email") || (config.contact && config.contact.email) || "",
      orderNote: getNativeValue("orderNote") || ""
    };

    Object.keys(values).forEach(function (key) {
      var customField = document.querySelector('[data-beslock-checkout-field="' + key + '"]');

      if (customField && !touchedFields[key] && customField.value !== values[key]) {
        customField.value = values[key];
      }

      if (customField && customField.value) {
        syncNativeField(key, customField.value);
      }
    });
  }

  function replaceTextNode(node) {
    var current = node.nodeValue;
    var trimmed = normalizeText(current);
    var replacement = textMap[trimmed];

    if (!replacement) {
      return;
    }

    node.nodeValue = current.replace(trimmed, replacement);
  }

  function translateCheckoutText(root) {
    var scope = root || document;
    var walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var parent = node.parentElement;

        if (!parent) {
          return NodeFilter.FILTER_REJECT;
        }

        if (parent.closest("script, style, textarea, input, select")) {
          return NodeFilter.FILTER_REJECT;
        }

        return normalizeText(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    var node = walker.nextNode();

    while (node) {
      replaceTextNode(node);
      node = walker.nextNode();
    }
  }

  function enhanceCheckout() {
    ensureCheckoutTop();
    ensureCheckoutDetails();
    hydrateCustomFields();
    translateCheckoutText(document.body);
  }

  function boot() {
    var scheduled = false;

    enhanceCheckout();

    if (!window.MutationObserver) {
      return;
    }

    var observer = new MutationObserver(function () {
      if (scheduled) {
        return;
      }

      scheduled = true;
      window.requestAnimationFrame(function () {
        scheduled = false;
        enhanceCheckout();
      });
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
