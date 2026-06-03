(function () {
  "use strict";

  var blockCheckoutSelector = ".wp-block-woocommerce-checkout, .wc-block-checkout";
  var classicCheckoutSelector = "form.checkout.woocommerce-checkout";
  var checkoutSelector = blockCheckoutSelector + ", " + classicCheckoutSelector;
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
    phone: [
      'input[type="tel"]',
      'input[autocomplete="tel"]',
      'input[id*="phone"]',
      'input[name*="phone"]'
    ],
    orderNote: [
      '#order-notes textarea.wc-block-components-textarea',
      'textarea.wc-block-components-textarea',
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
    "Phone": "Celular",
    "Postcode (optional)": "Código postal (opcional)",
    "Place Order": "Realizar el pedido",
    "Place order": "Realizar el pedido",
    "Pay via Wompi gateway.": "Paga de forma segura con Wompi.",
    "There are no payment methods available. Please contact us for help placing your order.": "Estamos preparando las opciones de pago para tu ubicación. Escríbenos y finalizamos tu pedido contigo."
  };
  var touchedFields = {};
  var alternateContactKeys = [
    "alternateFirstName",
    "alternateLastName",
    "alternatePhone",
    "alternateEmail"
  ];
  var alternateContactMarker = "[Contacto alterno de envío]";

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

    if (isClassicCheckout(checkout)) {
      document.body.classList.add("beslock-checkout-classic");
    }
  }

  function isClassicCheckout(checkout) {
    return !!(checkout && checkout.matches && checkout.matches(classicCheckoutSelector));
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
    var fields;
    var fieldIndex;

    for (index = 0; index < selectors.length; index += 1) {
      fields = document.querySelectorAll(selectors[index]);

      for (fieldIndex = 0; fieldIndex < fields.length; fieldIndex += 1) {
        if (!fields[fieldIndex].hasAttribute("data-beslock-checkout-field")) {
          return fields[fieldIndex];
        }
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

  function revealNativeOrderNoteField() {
    var checkbox = document.querySelector('#order-notes input[type="checkbox"]');

    if (checkbox && !checkbox.checked) {
      checkbox.click();
    }
  }

  function syncNativeField(key, value, retryCount) {
    var field = getNativeField(key);

    if (!field && key === "orderNote" && value && !retryCount) {
      revealNativeOrderNoteField();
      window.setTimeout(function () {
        syncNativeField(key, value, 1);
      }, 80);
      return;
    }

    if (!field || field.value === value) {
      return;
    }

    setNativeValue(field, value);
  }

  function getCustomFieldValue(key) {
    var field = document.querySelector('[data-beslock-checkout-field="' + key + '"]');

    return field ? field.value.trim() : "";
  }

  function stripAlternateContactNote(value) {
    var note = String(value || "");
    var markerIndex = note.indexOf(alternateContactMarker);

    if (markerIndex < 0) {
      return note;
    }

    return note.slice(0, markerIndex).trim();
  }

  function buildAlternateContactNote() {
    var firstName = getCustomFieldValue("alternateFirstName");
    var lastName = getCustomFieldValue("alternateLastName");
    var phone = getCustomFieldValue("alternatePhone");
    var email = getCustomFieldValue("alternateEmail");
    var fullName = [firstName, lastName].filter(Boolean).join(" ");
    var lines = [];

    if (!fullName && !phone && !email) {
      return "";
    }

    lines.push(alternateContactMarker);

    if (fullName) {
      lines.push("Nombre: " + fullName);
    }

    if (phone) {
      lines.push("Celular: " + phone);
    }

    if (email) {
      lines.push("Correo: " + email);
    }

    return lines.join("\n");
  }

  function syncOrderNoteToNative() {
    var customNote = getCustomFieldValue("orderNote");
    var note = stripAlternateContactNote(customNote || getNativeValue("orderNote"));
    var alternateContactNote = buildAlternateContactNote();

    if (alternateContactNote) {
      note = note ? note + "\n\n" + alternateContactNote : alternateContactNote;
    }

    syncNativeField("orderNote", note);
  }

  function createField(key, label, type, options) {
    var fieldOptions = options || {};
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

    if (fieldOptions.autocomplete) {
      input.autocomplete = fieldOptions.autocomplete;
    }

    if (fieldOptions.inputMode) {
      input.inputMode = fieldOptions.inputMode;
    }

    if (fieldOptions.placeholder) {
      input.placeholder = fieldOptions.placeholder;
    }

    if (fieldOptions.required) {
      input.required = true;
    }

    input.addEventListener("input", function () {
      touchedFields[key] = true;

      if (key === "orderNote" || alternateContactKeys.indexOf(key) !== -1) {
        syncOrderNoteToNative();
        return;
      }

      syncNativeField(key, input.value);
    });

    wrapper.appendChild(labelNode);
    wrapper.appendChild(input);

    return wrapper;
  }

  function createAlternateContact(labels) {
    var details = document.createElement("details");
    details.className = "beslock-checkout-alt-contact";

    var summary = document.createElement("summary");
    summary.className = "beslock-checkout-alt-contact__summary";

    var summaryText = document.createElement("span");
    summaryText.className = "beslock-checkout-alt-contact__summary-text";
    summaryText.textContent = labels.alternateContactTitle || "Añadir otro contacto para el envío";

    var summaryHint = document.createElement("span");
    summaryHint.className = "beslock-checkout-alt-contact__summary-hint";
    summaryHint.textContent = labels.optionalLabel || "Opcional";

    summary.appendChild(summaryText);
    summary.appendChild(summaryHint);

    var help = document.createElement("p");
    help.className = "beslock-checkout-alt-contact__help";
    help.textContent = labels.alternateContactHelp || "Úsalo si otra persona recibirá o coordinará la entrega.";

    var fields = document.createElement("div");
    fields.className = "beslock-checkout-contact__fields beslock-checkout-alt-contact__fields";
    fields.appendChild(createField("alternateFirstName", labels.firstName || "Nombre", "text", { autocomplete: "off" }));
    fields.appendChild(createField("alternateLastName", labels.lastName || "Apellido", "text", { autocomplete: "off" }));
    fields.appendChild(createField("alternatePhone", labels.phone || "Celular", "tel", { autocomplete: "off", inputMode: "tel" }));
    fields.appendChild(createField("alternateEmail", labels.email || "Correo electrónico", "email", { autocomplete: "off" }));

    details.appendChild(summary);
    details.appendChild(help);
    details.appendChild(fields);

    details.addEventListener("toggle", syncOrderNoteToNative);

    return details;
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

    if (isClassicCheckout(checkout)) {
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
    fields.appendChild(createField("firstName", labels.firstName || "Nombre", "text", { required: true, autocomplete: "given-name" }));
    fields.appendChild(createField("lastName", labels.lastName || "Apellido", "text", { required: true, autocomplete: "family-name" }));
    fields.appendChild(createField("phone", labels.phone || "Celular", "tel", { required: true, autocomplete: "tel", inputMode: "tel" }));
    fields.appendChild(createField("email", labels.email || "Correo electrónico", "email", { required: true, autocomplete: "email" }));

    var noteField = createField("orderNote", labels.orderNote || "Añadir una nota a tu pedido", "textarea");
    noteField.classList.add("beslock-checkout-contact__field--full");

    var noteHelp = document.createElement("span");
    noteHelp.className = "beslock-checkout-contact__help";
    noteHelp.textContent = labels.orderNoteHelp || "Puedes contarnos detalles de entrega, instalación o coordinación.";
    noteField.appendChild(noteHelp);
    fields.appendChild(noteField);

    contact.appendChild(title);
    contact.appendChild(fields);
    contact.appendChild(createAlternateContact(labels));

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

  function setClassicFieldLabel(fieldId, label) {
    var field = document.getElementById(fieldId + "_field");
    var labelNode = field ? field.querySelector("label") : null;

    if (labelNode && labelNode.childNodes.length) {
      labelNode.childNodes[0].nodeValue = label + " ";
    } else if (labelNode) {
      labelNode.textContent = label;
    }
  }

  function moveClassicField(wrapper, fieldId, extraClass) {
    var field = document.getElementById(fieldId + "_field");

    if (!field || !wrapper) {
      return null;
    }

    if (field.parentNode !== wrapper) {
      wrapper.appendChild(field);
    }

    if (extraClass) {
      field.classList.add(extraClass);
    }

    return field;
  }

  function ensureClassicContactDetails(checkout) {
    var customerDetails = checkout.querySelector("#customer_details");
    var billing = customerDetails ? customerDetails.querySelector(".woocommerce-billing-fields") : null;
    var fields = billing ? billing.querySelector(".woocommerce-billing-fields__field-wrapper") : null;
    var labels = getLabels();
    var heading;
    var noteField;
    var noteHelp;
    var additionalFields;

    if (!customerDetails || !billing || !fields) {
      return;
    }

    customerDetails.classList.add("beslock-classic-customer-details");
    fields.classList.add("beslock-classic-contact-grid");

    heading = billing.querySelector("h3");
    if (heading) {
      heading.textContent = labels.contactTitle || "Datos de contacto";
      heading.classList.add("beslock-checkout-section-title");
    }

    setClassicFieldLabel("billing_first_name", labels.firstName || "Nombre");
    setClassicFieldLabel("billing_last_name", labels.lastName || "Apellido");
    setClassicFieldLabel("billing_phone", labels.phone || "Celular");
    setClassicFieldLabel("billing_email", labels.email || "Correo electrónico");

    moveClassicField(fields, "billing_first_name", "beslock-classic-contact-field");
    moveClassicField(fields, "billing_last_name", "beslock-classic-contact-field");
    moveClassicField(fields, "billing_phone", "beslock-classic-contact-field");
    moveClassicField(fields, "billing_email", "beslock-classic-contact-field");

    [
      "billing_company",
      "billing_country",
      "billing_address_1",
      "billing_address_2",
      "billing_city",
      "billing_state",
      "billing_postcode"
    ].forEach(function (fieldId) {
      var field = moveClassicField(fields, fieldId, "beslock-classic-address-field");

      if (field) {
        field.setAttribute("aria-hidden", "true");
      }
    });

    additionalFields = checkout.querySelector(".woocommerce-additional-fields");
    noteField = document.getElementById("order_comments_field");
    if (noteField) {
      moveClassicField(fields, "order_comments", "beslock-classic-note-field");
      noteField.classList.add("beslock-checkout-contact__field--full");
      setClassicFieldLabel("order_comments", labels.orderNote || "Añadir una nota a tu pedido");

      if (!noteField.querySelector(".beslock-classic-note-help")) {
        noteHelp = document.createElement("span");
        noteHelp.className = "beslock-classic-note-help";
        noteHelp.textContent = labels.orderNoteHelp || "Puedes contarnos detalles de entrega, instalación o coordinación.";
        noteField.appendChild(noteHelp);
      }
    }

    if (additionalFields) {
      additionalFields.classList.add("beslock-classic-hidden-shell");
    }

    if (!billing.querySelector(".beslock-checkout-alt-contact")) {
      billing.appendChild(createAlternateContact(labels));
    }
  }

  function ensureClassicShippingSummary(checkout) {
    var customerDetails = checkout.querySelector("#customer_details");
    var labels = getLabels();
    var config = getConfig();
    var summary = checkout.querySelector(".beslock-classic-shipping-summary");
    var addressText;
    var editLink;

    if (!customerDetails) {
      return null;
    }

    if (!summary) {
      summary = document.createElement("section");
      summary.className = "beslock-checkout-shipping-summary beslock-classic-shipping-summary";
      summary.innerHTML = [
        '<h2 class="beslock-checkout-section-title"></h2>',
        '<div class="beslock-checkout-shipping-summary__address">',
        '<p class="beslock-checkout-shipping-summary__text" data-beslock-shipping-summary-text="true"></p>',
        '<a class="beslock-checkout-shipping-summary__edit"></a>',
        '</div>'
      ].join("");
    }

    summary.querySelector(".beslock-checkout-section-title").textContent = labels.shippingTitle || "Datos de envío";

    addressText = summary.querySelector("[data-beslock-shipping-summary-text]");
    if (addressText) {
      addressText.textContent = config.shippingDestination || labels.shippingFallback || "La entrega se tomará de la dirección confirmada en el carrito.";
    }

    editLink = summary.querySelector(".beslock-checkout-shipping-summary__edit");
    if (editLink) {
      editLink.href = config.cartUrl || "/carrito/";
      editLink.textContent = labels.editShipping || "Editar en carrito";
    }

    if (summary.parentNode !== checkout || summary.previousElementSibling !== customerDetails) {
      checkout.insertBefore(summary, customerDetails.nextSibling);
    }

    return summary;
  }

  function ensureClassicPaymentSection(checkout, shippingSummary) {
    var payment = checkout.querySelector("#payment");
    var heading = checkout.querySelector(".beslock-classic-payment-heading");
    var insertAfter = shippingSummary || checkout.querySelector("#customer_details");
    var placeOrder;
    var returnLink;
    var placeButton;

    if (!payment || !insertAfter) {
      return;
    }

    if (!heading) {
      heading = document.createElement("h2");
      heading.className = "beslock-checkout-section-title beslock-classic-payment-heading";
      heading.textContent = "Opciones de pago";
    }

    if (heading.parentNode !== checkout || heading.previousElementSibling !== insertAfter) {
      checkout.insertBefore(heading, insertAfter.nextSibling);
    }

    if (payment.parentNode !== checkout || payment.previousElementSibling !== heading) {
      checkout.insertBefore(payment, heading.nextSibling);
    }

    placeOrder = payment.querySelector(".place-order");
    placeButton = placeOrder ? placeOrder.querySelector("#place_order") : null;
    if (placeOrder && placeButton && !placeOrder.querySelector(".beslock-classic-return-cart")) {
      returnLink = document.createElement("a");
      returnLink.className = "beslock-classic-return-cart";
      returnLink.href = (getConfig().cartUrl || "/carrito/");
      returnLink.textContent = "← Volver al carrito";
      placeOrder.insertBefore(returnLink, placeButton);
    }
  }

  function buildClassicTotalsMarkup(tfoot) {
    var rows = tfoot ? Array.prototype.slice.call(tfoot.querySelectorAll("tr")) : [];

    return rows.map(function (row) {
      var label = row.querySelector("th");
      var value = row.querySelector("td");
      var className = row.className ? " " + row.className : "";

      if (!label || !value) {
        return "";
      }

      return [
        '<div class="beslock-classic-total-row',
        className,
        '"><span class="beslock-classic-total-row__label">',
        label.textContent.trim(),
        '</span><span class="beslock-classic-total-row__value">',
        value.innerHTML,
        '</span></div>'
      ].join("");
    }).join("");
  }

  function ensureClassicCouponRow(orderReview) {
    var couponRow = orderReview.querySelector(".beslock-classic-coupon-row");
    var couponToggle = document.querySelector(".woocommerce-form-coupon-toggle");
    var couponForm = document.querySelector("form.checkout_coupon");

    if (couponToggle) {
      couponToggle.classList.add("beslock-classic-coupon-source");
    }

    if (couponForm) {
      couponForm.classList.add("beslock-classic-coupon-source");
    }

    if (couponRow) {
      couponRow.remove();
    }

    return null;
  }

  function ensureClassicTotals(orderReview, table, couponRow) {
    var tfoot = table ? table.querySelector("tfoot") : null;
    var totals = orderReview.querySelector(".beslock-classic-totals");
    var markup = buildClassicTotalsMarkup(tfoot);

    if (!totals) {
      totals = document.createElement("div");
      totals.className = "beslock-classic-totals";
    }

    if (totals.getAttribute("data-beslock-totals") !== markup) {
      totals.innerHTML = markup;
      totals.setAttribute("data-beslock-totals", markup);
    }

    if (table && totals.parentNode !== orderReview) {
      orderReview.insertBefore(totals, table.nextSibling);
    } else if (couponRow && totals.parentNode !== orderReview) {
      orderReview.insertBefore(totals, couponRow.nextSibling);
    }
  }

  function ensureClassicOrderSummary(checkout) {
    var orderReview = checkout.querySelector("#order_review");
    var heading = checkout.querySelector("#order_review_heading");
    var table = orderReview ? orderReview.querySelector(".woocommerce-checkout-review-order-table") : null;
    var couponRow;

    if (!orderReview) {
      return;
    }

    orderReview.classList.add("beslock-classic-order-card");

    if (heading) {
      heading.textContent = "Resumen del pedido";
      heading.classList.add("beslock-checkout-section-title");

      if (heading.parentNode !== orderReview) {
        orderReview.insertBefore(heading, orderReview.firstChild);
      }
    }

    if (table) {
      table.classList.add("beslock-classic-order-table");
      couponRow = ensureClassicCouponRow(orderReview);
      ensureClassicTotals(orderReview, table, couponRow);
    }
  }

  function ensureClassicCheckoutLayout() {
    var checkout = document.querySelector(classicCheckoutSelector);
    var shippingSummary;

    if (!checkout) {
      return;
    }

    checkout.classList.add("beslock-classic-checkout");
    ensureClassicContactDetails(checkout);
    shippingSummary = ensureClassicShippingSummary(checkout);
    ensureClassicPaymentSection(checkout, shippingSummary);
    ensureClassicOrderSummary(checkout);
  }

  function hydrateCustomFields() {
    var checkout = document.querySelector(checkoutSelector);

    if (isClassicCheckout(checkout)) {
      return;
    }

    var config = getConfig();
    var values = {
      firstName: getNativeValue("firstName") || (config.contact && config.contact.firstName) || "",
      lastName: getNativeValue("lastName") || (config.contact && config.contact.lastName) || "",
      phone: getNativeValue("phone") || (config.contact && config.contact.phone) || "",
      email: getNativeValue("email") || (config.contact && config.contact.email) || "",
      orderNote: stripAlternateContactNote(getNativeValue("orderNote")) || ""
    };

    Object.keys(values).forEach(function (key) {
      var customField = document.querySelector('[data-beslock-checkout-field="' + key + '"]');

      if (customField && !touchedFields[key] && customField.value !== values[key]) {
        customField.value = values[key];
      }

      if (customField && customField.value) {
        if (key === "orderNote") {
          syncOrderNoteToNative();
        } else {
          syncNativeField(key, customField.value);
        }
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
    var checkout = document.querySelector(checkoutSelector);

    if (!checkout) {
      return;
    }

    ensureCheckoutTop();

    if (isClassicCheckout(checkout)) {
      ensureClassicCheckoutLayout();
    } else {
      ensureCheckoutDetails();
      hydrateCustomFields();
    }

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
