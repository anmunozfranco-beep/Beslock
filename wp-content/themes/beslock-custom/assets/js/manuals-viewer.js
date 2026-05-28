/**
 * BESLOCK manuals viewer.
 * Reads only dist/manuals/index.json, products/*.json, and dist/manuals/assets.
 */
(function () {
  'use strict';

  var config = window.BESLOCK_MANUALS_CONFIG || {};
  var baseUrl = String(window.BESLOCK_MANUALS_BASE_URL || config.baseUrl || '').replace(/\/+$/, '');

  if (!baseUrl) {
    var currentScript = document.currentScript && document.currentScript.src ? document.currentScript.src : '';
    if (currentScript.indexOf('/assets/js/') !== -1) {
      baseUrl = currentScript.split('/assets/js/')[0] + '/dist/manuals';
    }
  }

  var GUIDE_SECTIONS = [
    {
      id: 'conoce-tu-cerradura',
      label: 'Conoce tu cerradura',
      preferredIds: ['presentacion-producto', 'partes-principales', 'componentes'],
      aliases: ['conoce-tu-cerradura', 'presentacion', 'presentacion-producto', 'partes-principales', 'componentes', 'panel', 'mecanismo']
    },
    {
      id: 'instalacion',
      label: 'Instalación',
      preferredIds: ['instalacion'],
      aliases: ['instalacion', 'installation']
    },
    {
      id: 'configuracion',
      label: 'Configuración',
      preferredIds: ['perfiles', 'crear-primer-administrador', 'entrar-menu-administrador', 'ajustes-generales', 'crear-administradores', 'crear-usuario', 'eliminar-perfil'],
      includeIds: ['perfiles', 'crear-primer-administrador', 'entrar-menu-administrador', 'ajustes-generales', 'crear-administradores', 'crear-usuario', 'eliminar-perfil'],
      aliases: ['configuracion', 'configuration', 'ajustes', 'ajustes-generales', 'administrador', 'usuarios', 'perfiles']
    },
    {
      id: 'uso-diario',
      label: 'Uso diario',
      preferredIds: ['otras-configuraciones', 'uso-diario', 'operacion'],
      aliases: ['uso-diario', 'uso', 'daily-use', 'operacion', 'paso-libre', 'apertura', 'bloqueo-interior']
    },
    {
      id: 'soluciones-rapidas',
      label: 'Soluciones rápidas',
      preferredIds: ['soluciones-rapidas', 'troubleshooting', 'ayuda', 'otras-configuraciones'],
      aliases: ['soluciones-rapidas', 'solucion', 'troubleshooting', 'ayuda', 'emergencia', 'energia-de-emergencia', 'bateria', 'bloqueo']
    }
  ];

  var FALLBACK_PRODUCTS = [
    { slug: 'e-flex', display_name: 'e-Flex', product_json: 'products/e-flex.json' },
    { slug: 'e-nova', display_name: 'e-Nova', product_json: 'products/e-nova.json' },
    { slug: 'e-orbit', display_name: 'e-Orbit', product_json: 'products/e-orbit.json' },
    { slug: 'e-prime', display_name: 'e-Prime', product_json: 'products/e-prime.json' },
    { slug: 'e-shield', display_name: 'e-Shield', product_json: 'products/e-shield.json' },
    { slug: 'e-touch', display_name: 'e-Touch', product_json: 'products/e-touch.json' }
  ];

  var state = {
    index: null,
    indexFailed: false,
    selectedSection: null,
    selectedProduct: null,
    productCache: {}
  };

  var els = {};

  function ready(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  function normalize(value) {
    return String(value || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  function cleanRelativePath(path) {
    return String(path || '')
      .replace(/^https?:\/\/[^/]+\/?/i, '')
      .replace(/^\/+/, '')
      .replace(/\.\./g, '')
      .replace(/^dist\/manuals\//, '');
  }

  function manualUrl(path) {
    var cleaned = cleanRelativePath(path);
    return baseUrl + '/' + cleaned;
  }

  function text(value) {
    return document.createTextNode(String(value || ''));
  }

  function el(tag, className, textValue) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (typeof textValue !== 'undefined' && textValue !== null) node.appendChild(text(textValue));
    return node;
  }

  function getSectionDef(id) {
    var wanted = normalize(id);
    for (var i = 0; i < GUIDE_SECTIONS.length; i++) {
      if (GUIDE_SECTIONS[i].id === wanted) return GUIDE_SECTIONS[i];
    }
    return GUIDE_SECTIONS[0];
  }

  function setDrawerHeader(eyebrow, title) {
    if (els.eyebrow) els.eyebrow.textContent = eyebrow || 'Guías BESLOCK';
    if (els.title) els.title.textContent = title || 'Manuales y ayuda';
  }

  function setBody(node) {
    if (!els.body) return;
    els.body.innerHTML = '';
    els.body.appendChild(node);
    try { els.body.scrollTop = 0; } catch (e) {}
  }

  function renderState(title, message, retry) {
    var wrap = el('div', 'manuals-state');
    var inner = el('div');
    inner.appendChild(el('strong', '', title));
    if (message) inner.appendChild(el('p', '', message));
    if (typeof retry === 'function') {
      var button = el('button', 'manuals-retry-button', 'Reintentar');
      button.type = 'button';
      button.addEventListener('click', retry);
      inner.appendChild(button);
    }
    wrap.appendChild(inner);
    return wrap;
  }

  function openManualsDrawer() {
    if (!els.manualsDrawer) return;
    if (els.mobileDrawer) {
      els.mobileDrawer.classList.add('is-open', 'manuals-sheet-open');
      els.mobileDrawer.setAttribute('aria-hidden', 'false');
    }
    if (els.drawerBackdrop) {
      els.drawerBackdrop.classList.add('backdrop-visible');
    }
    if (els.menuButton) {
      els.menuButton.setAttribute('aria-expanded', 'true');
    }
    els.manualsDrawer.classList.add('is-open');
    els.manualsDrawer.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('has-drawer-open');
    window.setTimeout(function () {
      try { els.body && els.body.focus({ preventScroll: true }); } catch (e) {}
    }, 60);
  }

  function closeManualsDrawer() {
    if (!els.manualsDrawer) return;
    els.manualsDrawer.classList.remove('is-open');
    els.manualsDrawer.setAttribute('aria-hidden', 'true');
    if (els.mobileDrawer) els.mobileDrawer.classList.remove('manuals-sheet-open');
    if (!els.mobileDrawer || !els.mobileDrawer.classList.contains('is-open')) {
      document.documentElement.classList.remove('has-drawer-open');
    }
    state.selectedProduct = null;
  }

  function toggleSections(force) {
    if (!els.manualsToggle || !els.sectionsPanel) return;
    var willOpen = typeof force === 'boolean'
      ? force
      : els.manualsToggle.getAttribute('aria-expanded') !== 'true';

    els.manualsToggle.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    els.sectionsPanel.hidden = !willOpen;
    els.sectionsPanel.setAttribute('aria-hidden', willOpen ? 'false' : 'true');

    if (els.manualsItem) els.manualsItem.classList.toggle('is-open', willOpen);
    if (els.mobileDrawer) els.mobileDrawer.classList.toggle('manuals-menu-open', willOpen);
  }

  function markActiveSection(sectionDef) {
    if (!els.sectionButtons) return;
    for (var i = 0; i < els.sectionButtons.length; i++) {
      var isActive = normalize(els.sectionButtons[i].getAttribute('data-manual-section')) === sectionDef.id;
      els.sectionButtons[i].classList.toggle('is-active', isActive);
      if (isActive) {
        els.sectionButtons[i].setAttribute('aria-current', 'true');
      } else {
        els.sectionButtons[i].removeAttribute('aria-current');
      }
    }
  }

  function fetchJson(url) {
    var cacheBust = config.cacheBust ? String(config.cacheBust) : '';
    var requestUrl = cacheBust
      ? url + (url.indexOf('?') === -1 ? '?' : '&') + 'v=' + encodeURIComponent(cacheBust)
      : url;

    return fetch(requestUrl, { cache: 'no-store', headers: { Accept: 'application/json' } }).then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    });
  }

  function loadIndex() {
    if (state.index) return Promise.resolve(state.index);
    return fetchJson(manualUrl('index.json')).then(function (data) {
      var products = data && Array.isArray(data.products) ? data.products : [];
      if (!products.length) throw new Error('Empty manuals index');
      state.index = data;
      state.indexFailed = false;
      return state.index;
    }).catch(function () {
      state.indexFailed = true;
      state.index = {
        schema: 'beslock.manuals.fallback',
        products: FALLBACK_PRODUCTS
      };
      return state.index;
    });
  }

  function productName(product) {
    return product && (product.display_name || product.name || product.title || product.slug) || 'Producto BESLOCK';
  }

  function escapeRegExp(value) {
    return String(value || '').replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function stripProductIntro(value, product) {
    var output = String(value || '').trim();
    if (!output || !product) return output;

    var candidates = [
      product.display_name,
      product.name,
      product.title,
      product.slug ? String(product.slug).replace(/-/g, ' ') : '',
      productName(product)
    ];

    candidates.forEach(function (candidate) {
      if (!candidate || !output) return;
      var looseName = escapeRegExp(candidate).replace(/\\-/g, '[-\\s]?').replace(/\s+/g, '\\s+');
      var pattern = new RegExp('^' + looseName + '(?:\\s+[A-Z]{1,5}\\d{1,5}[A-Z0-9-]*)?\\s*(?:[-–—:])?\\s*', 'i');
      output = output.replace(pattern, '').trim();
    });

    if (!output) return String(value || '').trim();
    return output.charAt(0).toUpperCase() + output.slice(1);
  }

  function productTeaser(product, sectionDef) {
    if (!product) return 'Manual interactivo disponible.';

    var teasers = product.section_teasers || product.sectionTeasers || {};
    var wanted = sectionDef ? normalize(sectionDef.id) : '';

    if (wanted && teasers && typeof teasers === 'object') {
      if (typeof teasers[wanted] === 'string') return stripProductIntro(teasers[wanted], product);

      for (var key in teasers) {
        if (Object.prototype.hasOwnProperty.call(teasers, key) && normalize(key) === wanted) {
          return stripProductIntro(teasers[key], product);
        }
      }

      if (sectionDef && Array.isArray(sectionDef.aliases)) {
        for (var a = 0; a < sectionDef.aliases.length; a++) {
          var alias = normalize(sectionDef.aliases[a]);
          for (var aliasKey in teasers) {
            if (Object.prototype.hasOwnProperty.call(teasers, aliasKey) && normalize(aliasKey) === alias) {
              return stripProductIntro(teasers[aliasKey], product);
            }
          }
        }
      }
    }

    return stripProductIntro(product.short_description || product.summary || 'Manual interactivo disponible.', product);
  }

  function openModels(sectionDef) {
    state.selectedSection = sectionDef;
    state.selectedProduct = null;
    markActiveSection(sectionDef);
    openManualsDrawer();
    setDrawerHeader(sectionDef.label, 'Elige un modelo');
    setBody(renderState('Cargando manuales', 'Preparando los modelos disponibles.'));

    loadIndex().then(function (indexData) {
      renderModels(sectionDef, indexData);
    }).catch(function () {
      setBody(renderState('Error cargando manuales', 'No se pudo leer el paquete estático de manuales.', function () {
        state.index = null;
        openModels(sectionDef);
      }));
    });
  }

  function createImage(path, altText, className) {
    if (!path) return createPlaceholder('Imagen no disponible', className);

    var image = document.createElement('img');
    image.src = manualUrl(path);
    image.alt = altText || '';
    image.loading = 'lazy';
    image.decoding = 'async';
    image.addEventListener('error', function () {
      var placeholder = createPlaceholder('Imagen no disponible', className);
      if (image.parentNode) image.parentNode.replaceChild(placeholder, image);
    });
    return image;
  }

  function createPlaceholder(message, className) {
    var placeholder = el('div', className ? className + ' manuals-media-placeholder' : 'manuals-media-placeholder');
    placeholder.appendChild(el('span', '', message || 'Imagen no disponible'));
    return placeholder;
  }

  function renderModels(sectionDef, indexData) {
    var products = indexData && Array.isArray(indexData.products) ? indexData.products : [];
    setDrawerHeader(sectionDef.label, 'Elige un modelo');

    if (!products.length) {
      setBody(renderState('Producto sin manual disponible', 'No hay modelos publicados para esta guía.'));
      return;
    }

    var wrap = el('div', 'manuals-model-grid');
    if (state.indexFailed) {
      var warning = renderState('Error cargando manuales', 'No se pudo leer el índice. Puedes intentar abrir un modelo base disponible.');
      wrap.appendChild(warning);
    }

    products.forEach(function (product) {
      var card = el('button', 'manuals-model-card');
      card.type = 'button';
      card.setAttribute('data-manual-product', product.slug || '');

      var media = el('span', 'manuals-model-card__media');
      if (product.hero_image) {
        media.appendChild(createImage(product.hero_image, productName(product)));
      } else {
        media.appendChild(createPlaceholder('Modelo BESLOCK'));
      }

      var copy = el('span', 'manuals-model-card__content');
      copy.appendChild(el('span', 'manuals-model-card__name', productName(product)));
      copy.appendChild(el('span', 'manuals-model-card__copy', productTeaser(product, sectionDef)));

      card.appendChild(media);
      card.appendChild(copy);
      card.addEventListener('click', function () { openProduct(product); });
      wrap.appendChild(card);
    });

    setBody(wrap);
  }

  function openProduct(indexProduct) {
    if (!state.selectedSection) return;
    if (!indexProduct || !indexProduct.slug) {
      setBody(renderState('Producto sin manual disponible', 'Este modelo no tiene un manual publicado.'));
      return;
    }

    state.selectedProduct = indexProduct;
    setDrawerHeader(productName(indexProduct), state.selectedSection.label);
    setBody(renderState('Cargando manual', 'Leyendo el contenido del producto seleccionado.'));

    loadProduct(indexProduct).then(function (productData) {
      renderManual(indexProduct, productData, state.selectedSection);
    }).catch(function () {
      setBody(renderState('Producto sin manual disponible', 'No se pudo cargar el manual de este modelo.', function () {
        openProduct(indexProduct);
      }));
    });
  }

  function loadProduct(indexProduct) {
    var slug = normalize(indexProduct.slug);
    if (state.productCache[slug]) return Promise.resolve(state.productCache[slug]);

    var productPath = indexProduct.product_json || ('products/' + slug + '.json');
    return fetchJson(manualUrl(productPath)).then(function (data) {
      state.productCache[slug] = data;
      return data;
    });
  }

  function getManualRoot(productData) {
    var product = productData && productData.product ? productData.product : productData;
    return product || {};
  }

  function collectSectionText(section) {
    var parts = [section.id, section.title, section.manual_image_key];
    var images = Array.isArray(section.images) ? section.images : [];
    var blocks = Array.isArray(section.blocks) ? section.blocks : [];

    images.forEach(function (image) {
      parts.push(image.section_id, image.heading);
    });
    blocks.forEach(function (block) {
      if (!block) return;
      parts.push(block.title, block.anchor, block.caption, block.text, block.image_id);
    });

    return normalize(parts.join(' '));
  }

  function scoreSection(section, sectionDef) {
    if (!section || !sectionDef) return 0;
    var sectionId = normalize(section.id);
    var title = normalize(section.title);
    var haystack = collectSectionText(section);
    var score = 0;

    for (var p = 0; p < sectionDef.preferredIds.length; p++) {
      if (sectionId === normalize(sectionDef.preferredIds[p])) {
        score += 240 - p;
      }
    }

    sectionDef.aliases.forEach(function (alias) {
      var needle = normalize(alias);
      if (!needle) return;
      if (sectionId === needle) score += 120;
      if (title === needle) score += 100;
      if (sectionId.indexOf(needle) !== -1 || needle.indexOf(sectionId) !== -1) score += 55;
      if (title.indexOf(needle) !== -1 || needle.indexOf(title) !== -1) score += 45;
      if (haystack.indexOf(needle) !== -1) score += 18;
    });

    return score;
  }

  function findManualSection(productData, sectionDef) {
    var product = getManualRoot(productData);
    var manual = product.manual || {};
    var sections = Array.isArray(manual.sections) ? manual.sections : [];
    var winner = null;
    var winnerScore = 0;

    sections.forEach(function (section) {
      var score = scoreSection(section, sectionDef);
      if (score > winnerScore) {
        winner = section;
        winnerScore = score;
      }
    });

    return winnerScore > 0 ? winner : null;
  }

  function findManualSections(productData, sectionDef) {
    var product = getManualRoot(productData);
    var manual = product.manual || {};
    var sections = Array.isArray(manual.sections) ? manual.sections : [];
    var matches = [];
    var used = {};

    if (sectionDef && Array.isArray(sectionDef.includeIds) && sectionDef.includeIds.length) {
      sectionDef.includeIds.forEach(function (wantedId) {
        var wanted = normalize(wantedId);
        for (var i = 0; i < sections.length; i++) {
          var section = sections[i];
          var sectionId = normalize(section && section.id);
          if (sectionId === wanted && !used[sectionId]) {
            matches.push(section);
            used[sectionId] = true;
            break;
          }
        }
      });
    }

    if (matches.length) return matches;

    var section = findManualSection(productData, sectionDef);
    return section ? [section] : [];
  }

  function renderManual(indexProduct, productData, sectionDef) {
    var product = getManualRoot(productData);
    var manual = product.manual || {};

    if (!manual.available || !Array.isArray(manual.sections)) {
      setBody(renderState('Producto sin manual disponible', 'Este producto todavía no tiene una guía interactiva publicada.'));
      return;
    }

    var sections = findManualSections(productData, sectionDef);
    if (!sections.length) {
      setBody(renderSectionUnavailable(indexProduct, sectionDef));
      return;
    }

    var productLabel = product.display_name || productName(indexProduct);
    setDrawerHeader(productLabel + ' · ' + sectionDef.label, sections.length > 1 ? sectionDef.label : (sections[0].title || sectionDef.label));

    var allGroups = [];
    sections.forEach(function (section) {
      var grouped = buildManualGroups(section, product);
      grouped.groups.forEach(function (group) {
        allGroups.push(group);
      });
    });

    if (!allGroups.length) {
      setBody(renderSectionUnavailable(indexProduct, sectionDef));
      return;
    }

    var wrap = el('div', 'manuals-content');
    var top = el('div', 'manuals-content__top');
    var back = el('button', 'manuals-back-button', '← Volver a modelos');
    back.type = 'button';
    back.addEventListener('click', function () {
      renderModels(sectionDef, state.index);
    });
    top.appendChild(back);
    wrap.appendChild(top);

    allGroups.forEach(function (group) {
      wrap.appendChild(renderManualGroup(group));
    });

    setBody(wrap);
  }

  function renderSectionUnavailable(indexProduct, sectionDef) {
    var wrap = el('div', 'manuals-content');
    var back = el('button', 'manuals-back-button', '← Volver a modelos');
    back.type = 'button';
    back.addEventListener('click', function () {
      renderModels(sectionDef, state.index);
    });
    wrap.appendChild(back);
    wrap.appendChild(renderState('Sección no disponible', 'Este modelo no tiene contenido publicado para "' + sectionDef.label + '".'));
    return wrap;
  }

  function findImageForKey(section, product, key) {
    if (!key) return null;
    var sources = [];
    if (Array.isArray(section.images)) sources = sources.concat(section.images);
    if (product && product.visual_assets && Array.isArray(product.visual_assets.manual_images)) {
      sources = sources.concat(product.visual_assets.manual_images);
    }

    for (var i = 0; i < sources.length; i++) {
      var image = sources[i];
      var keys = Array.isArray(image.image_review_keys) ? image.image_review_keys : [];
      if (keys.indexOf(key) !== -1 || image.manual_image_key === key) {
        return image;
      }
    }
    return null;
  }

  function isManualImage(path) {
    var cleaned = cleanRelativePath(path);
    return cleaned.indexOf('/manual/') !== -1 && cleaned.indexOf('/ts/') === -1;
  }

  function imageFromBlock(block, section, product) {
    if (block && block.image && isManualImage(block.image)) {
      return {
        image: block.image,
        alt: block.alt || block.title || section.title || '',
        caption: block.caption || '',
        title: block.title || ''
      };
    }

    var key = block && (block.manual_image_key || block.related_manual_image_key);
    var found = findImageForKey(section, product, key);
    if (found && found.image && isManualImage(found.image)) {
      return {
        image: found.image,
        alt: block.alt || found.heading || section.title || '',
        caption: block.caption || found.heading || '',
        title: block.title || found.heading || ''
      };
    }
    return null;
  }

  function buildManualGroups(section, product) {
    var blocks = Array.isArray(section.blocks) ? section.blocks : [];
    var intro = [];
    var groups = [];
    var current = null;
    var sawHeading = false;

    function pushCurrent() {
      if (!current) return;
      groups.push(current);
      current = null;
    }

    blocks.forEach(function (block) {
      if (!block || !block.type) return;

      if (block.type === 'heading') {
        pushCurrent();
        sawHeading = true;
        var headingImage = imageFromBlock(block, section, product);
        current = {
          title: block.title || section.title || '',
          image: headingImage ? headingImage.image : '',
          alt: headingImage ? headingImage.alt : '',
          caption: headingImage ? headingImage.caption : '',
          blocks: []
        };
        return;
      }

      if (block.type === 'figure') {
        if (!current) {
          sawHeading = true;
          current = { title: block.title || section.title || '', image: '', alt: '', caption: '', blocks: [] };
        }
        var figureImage = imageFromBlock(block, section, product);
        if (figureImage) {
          current.image = figureImage.image;
          current.alt = figureImage.alt;
          current.caption = figureImage.caption;
          if (!current.title) current.title = figureImage.title;
        }
        return;
      }

      if (block.type === 'paragraph' || block.type === 'list') {
        if (!current && !sawHeading) {
          intro.push(block);
        } else {
          if (!current) current = { title: section.title || '', image: '', alt: '', caption: '', blocks: [] };
          current.blocks.push(block);
        }
      }
    });

    pushCurrent();

    if (!groups.length && Array.isArray(section.images)) {
      section.images.forEach(function (image) {
        if (!image || !image.image || !isManualImage(image.image)) return;
        groups.push({
          title: image.heading || section.title || '',
          image: image.image,
          alt: image.heading || section.title || '',
          caption: image.heading || '',
          blocks: []
        });
      });
    }

    var imageIndex = 0;
    groups.forEach(function (group) {
      if (group.image || !Array.isArray(section.images)) return;
      while (imageIndex < section.images.length) {
        var image = section.images[imageIndex++];
        if (image && image.image && isManualImage(image.image)) {
          group.image = image.image;
          group.alt = image.heading || group.title || section.title || '';
          group.caption = image.heading || '';
          break;
        }
      }
    });

    return { intro: intro, groups: groups };
  }

  function appendBlockText(target, blocks) {
    blocks.forEach(function (block) {
      if (!block) return;
      if (block.type === 'paragraph' && block.text) {
        target.appendChild(el('p', '', block.text));
      }
      if (block.type === 'list' && Array.isArray(block.items)) {
        var list = document.createElement(block.ordered ? 'ol' : 'ul');
        block.items.forEach(function (item) {
          list.appendChild(el('li', '', item));
        });
        target.appendChild(list);
      }
    });
  }

  function renderManualGroup(group) {
    var block = el('section', 'manuals-block');
    var copy = el('div', 'manuals-block__copy');
    copy.appendChild(el('h4', '', group.title || 'Detalle de la guía'));
    appendBlockText(copy, group.blocks || []);
    if (!(group.blocks || []).length && group.caption) {
      copy.appendChild(el('p', '', group.caption));
    }

    var media = el('div', 'manuals-block__media');
    if (group.image) {
      media.appendChild(createImage(group.image, group.alt || group.title || 'Imagen del manual'));
    } else {
      media.appendChild(createPlaceholder('Imagen no disponible'));
    }

    block.appendChild(copy);
    block.appendChild(media);
    return block;
  }

  function bindEvents() {
    if (!els.mobileDrawer || !els.manualsToggle || !els.sectionsPanel || !els.manualsDrawer || !baseUrl) return;

    els.manualsToggle.addEventListener('click', function (event) {
      event.preventDefault();
      toggleSections();
    });

    els.sectionButtons = els.sectionsPanel.querySelectorAll('[data-manual-section]');
    for (var i = 0; i < els.sectionButtons.length; i++) {
      els.sectionButtons[i].addEventListener('click', function () {
        var sectionDef = getSectionDef(this.getAttribute('data-manual-section'));
        openModels(sectionDef);
      });
    }

    if (els.drawerClose) {
      els.drawerClose.addEventListener('click', function () {
        closeManualsDrawer();
      });
    }

    document.addEventListener('keydown', function (event) {
      if ((event.key === 'Escape' || event.key === 'Esc') && els.manualsDrawer.classList.contains('is-open')) {
        event.preventDefault();
        event.stopPropagation();
        closeManualsDrawer();
      }
    }, true);

    if (window.MutationObserver) {
      var observer = new MutationObserver(function () {
        var drawerClosed = !els.mobileDrawer.classList.contains('is-open');
        var manualsActive = (els.manualsDrawer && els.manualsDrawer.classList.contains('is-open')) ||
          els.mobileDrawer.classList.contains('manuals-menu-open') ||
          els.mobileDrawer.classList.contains('manuals-sheet-open');

        if (drawerClosed && manualsActive) {
          closeManualsDrawer();
          toggleSections(false);
        }
      });
      observer.observe(els.mobileDrawer, { attributes: true, attributeFilter: ['class', 'aria-hidden'] });
    }
  }

  function init() {
    els.mobileDrawer = document.getElementById('mobileDrawer');
    els.manualsToggle = document.querySelector('[data-js="drawer-manuals-toggle"]');
    els.manualsItem = els.manualsToggle ? els.manualsToggle.closest('.mobile-menu__item--manuals') : null;
    els.sectionsPanel = document.querySelector('[data-js="drawer-manuals-sections"]');
    els.manualsDrawer = document.querySelector('[data-js="manuals-drawer"]');
    els.drawerBackdrop = document.querySelector('[data-js="drawer-backdrop"], #drawerBackdrop');
    els.menuButton = document.getElementById('menuBtn');
    els.drawerClose = document.querySelector('[data-js="manuals-drawer-close"]');
    els.body = document.querySelector('[data-js="manuals-drawer-body"]');
    els.eyebrow = document.querySelector('[data-js="manuals-drawer-eyebrow"]');
    els.title = document.querySelector('[data-js="manuals-drawer-title"]');

    bindEvents();
  }

  ready(init);
})();
