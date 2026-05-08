(function(){
  'use strict';

  function findGalleries(){
    return Array.from(document.querySelectorAll('.product-page__gallery'));
  }

  function ensureReel(root){
    if(!root) return null;
    let reel = root.querySelector('.product-page__gallery-reel');
    if(reel) return reel;
    reel = document.createElement('div');
    reel.className = 'product-page__gallery-reel';
    // move any existing images into the reel
    const imgs = Array.from(root.querySelectorAll('img'));
    imgs.forEach(img=>{
      const movable = img.closest('a') || img;
      const slide = document.createElement('div');
      slide.className = 'product-page__gallery-slide';
      // move the node
      slide.appendChild(movable);
      reel.appendChild(slide);
    });

    // remove legacy wrappers that may contain duplicate images (non-destructive)
    Array.from(root.querySelectorAll('.product-page__gallery-wrapper, .product-page__gallery-canonical')).forEach(n=>n.remove());

    root.appendChild(reel);
    return reel;
  }

  function buildUI(root, reel, slides){
    if(!root || !reel) return null;
    let ui = root.querySelector('.product-gallery__ui');
    if(ui) return ui;
    ui = document.createElement('div'); ui.className = 'product-gallery__ui';
    const dots = document.createElement('div'); dots.className = 'product-gallery__dots';
    const counter = document.createElement('div'); counter.className = 'product-gallery__counter';
    ui.appendChild(dots); ui.appendChild(counter);
    root.appendChild(ui);

    slides.forEach((slide, i)=>{
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'product-gallery__dot';
      dot.setAttribute('aria-label', 'Go to slide ' + (i+1));
      dot.addEventListener('click', ()=>{
        // scroll to slide
        if(typeof slide.scrollIntoView === 'function') slide.scrollIntoView({behavior:'smooth', inline:'center'});
        else reel.scrollTo({left: slide.offsetLeft, behavior: 'smooth'});
      });
      dots.appendChild(dot);
    });

    return ui;
  }

  function normalizeSlideImages(reel){
    if(!reel) return;
    var targetWidth = Math.max(reel.clientWidth || 0, 480);

    Array.from(reel.querySelectorAll('img')).forEach(function(img){
      try{
        var highResSrc = img.getAttribute('data-large_image') || img.getAttribute('data-src') || img.getAttribute('src');
        var largeWidth = img.getAttribute('data-large_image_width');
        var largeHeight = img.getAttribute('data-large_image_height');

        if(largeWidth) img.setAttribute('width', largeWidth);
        if(largeHeight) img.setAttribute('height', largeHeight);

        if(highResSrc){
          img.setAttribute('src', highResSrc);
        }

        img.removeAttribute('srcset');
        img.removeAttribute('sizes');
        img.setAttribute('sizes', targetWidth + 'px');
        img.loading = 'eager';
        img.decoding = 'async';
      }catch(e){}
    });
  }

  function updateUI(root, reel, slides){
    const ui = root.querySelector('.product-gallery__ui');
    if(!ui) return;
    const dots = Array.from(ui.querySelectorAll('.product-gallery__dot'));
    const counter = ui.querySelector('.product-gallery__counter');
    const cw = reel.clientWidth || 1;
    const idx = Math.round(reel.scrollLeft / cw);
    const index = Math.max(0, Math.min(slides.length-1, idx));
    dots.forEach((d, i)=> d.classList.toggle('is-active', i === index));
    if(counter) counter.textContent = (index+1) + ' / ' + slides.length;
    // hide UI when not needed
    ui.style.display = (slides.length <= 1) ? 'none' : 'flex';
  }

  function enableDrag(root, reel, slides){
    if(!root || !reel || slides.length <= 1 || reel.dataset.beslockDrag === '1') return;

    var pointerDown = false;
    var dragging = false;
    var startX = 0;
    var startScroll = 0;
    var dragThreshold = 6;

    function setDragging(active){
      dragging = active;
      reel.classList.toggle('is-dragging', active);
      if(active){
        reel.style.setProperty('scroll-snap-type', 'none', 'important');
        reel.style.setProperty('scroll-behavior', 'auto', 'important');
      } else {
        reel.style.removeProperty('scroll-snap-type');
        reel.style.removeProperty('scroll-behavior');
      }
    }

    function finishDrag(ev){
      if(!pointerDown) return;
      pointerDown = false;

      if(dragging){
        if(ev && typeof ev.preventDefault === 'function') ev.preventDefault();
        var slideWidth = reel.clientWidth || 1;
        var targetLeft = Math.round(reel.scrollLeft / slideWidth) * slideWidth;
        setDragging(false);
        root.dataset.beslockSuppressClick = '1';
        window.setTimeout(function(){ delete root.dataset.beslockSuppressClick; }, 250);
        reel.scrollTo({ left: targetLeft, behavior: 'smooth' });
        window.requestAnimationFrame(function(){ updateUI(root, reel, slides); });
      } else {
        setDragging(false);
      }
    }

    function startDrag(clientX){
      pointerDown = true;
      dragging = false;
      startX = clientX;
      startScroll = reel.scrollLeft;
    }

    function moveDrag(clientX, ev){
      if(!pointerDown) return;

      var deltaX = clientX - startX;

      if(!dragging && Math.abs(deltaX) > dragThreshold){
        setDragging(true);
      }

      if(!dragging) return;

      if(ev && typeof ev.preventDefault === 'function') ev.preventDefault();
      reel.scrollLeft = startScroll - deltaX;
      updateUI(root, reel, slides);
    }

    reel.addEventListener('mousedown', function(ev){
      if(ev.button !== 0) return;
      startDrag(ev.clientX);
    });

    reel.addEventListener('touchstart', function(ev){
      if(!ev.touches || !ev.touches.length) return;
      startDrag(ev.touches[0].clientX);
    }, { passive: true });

    window.addEventListener('mousemove', function(ev){
      moveDrag(ev.clientX, ev);
    }, { passive: false });

      reel.addEventListener('mouseup', finishDrag);
      document.addEventListener('mouseup', finishDrag, true);
      window.addEventListener('mouseup', finishDrag);

    window.addEventListener('touchmove', function(ev){
      if(!ev.touches || !ev.touches.length) return;
      moveDrag(ev.touches[0].clientX, ev);
    }, { passive: false });

    window.addEventListener('touchend', finishDrag);
    window.addEventListener('touchcancel', finishDrag);

    reel.addEventListener('click', function(ev){
      if(root.dataset.beslockSuppressClick === '1'){
        ev.preventDefault();
        ev.stopPropagation();
      }
    }, true);

    reel.dataset.beslockDrag = '1';
  }

  function initGallery(root){
    if(!root || root.dataset.beslockInit === '1') return;
    const reel = ensureReel(root);
    if(!reel) return;
    // ensure slides are direct children (in case some existed already)
    const slides = Array.from(reel.children).filter(c => c.matches && c.matches('.product-page__gallery-slide'));
    // ensure native touch-action and smooth scrolling (allow horizontal swipe)
    try{ reel.style.setProperty('touch-action', 'pan-y', 'important'); }catch(e){}
    normalizeSlideImages(reel);

    // sanitize anchors/images to prevent fullscreen/lightbox and disable drag
    // NOTE: preserve `href` as a functional fallback. Only prevent navigation
    // when the link points to uploads and no lightbox is present.
    Array.from(reel.querySelectorAll('a')).forEach(a=>{
      try{
        if(a.hasAttribute('href')){
          // store original href for debugging/fallback but keep the href intact
          a.setAttribute('data-beslock-href', a.getAttribute('href'));
        }
        // remove common lightbox attributes (non-destructive)
        ['data-fancybox','data-lightbox','data-mfp','data-pswp-uid','rel','data-gallery'].forEach(attr=> a.removeAttribute(attr));
          a.draggable = false;
          a.addEventListener('dragstart', function(ev){ ev.preventDefault(); }, {passive:false});
        a.addEventListener('click', function(ev){
          try{
            var href = a.getAttribute('href') || '';
            var isUpload = href.indexOf('/wp-content/uploads/') !== -1;
            var lightboxPresent = (typeof window.PhotoSwipe !== 'undefined') ||
                                   (typeof window.jsPhotoSwipe !== 'undefined') ||
                                   (typeof window.beslockLightbox !== 'undefined') ||
                                   (typeof jQuery !== 'undefined' && (jQuery.fn && (jQuery.fn.magnificPopup || jQuery.fn.fancybox || jQuery.fn.simpleLightbox)));
            // Only prevent navigation when link points to uploads and there's no
            // lightbox available to handle it. Otherwise allow default behavior.
            if(isUpload && !lightboxPresent){
              ev.preventDefault();
            }
          }catch(e){}
        }, {passive:false});
        a.addEventListener('touchstart', function(ev){ /* noop to prioritize touch */ }, {passive:true});
      }catch(e){ /* ignore */ }
    });

    Array.from(reel.querySelectorAll('img')).forEach(img=>{
      try{
        img.draggable = false;
        img.addEventListener('dragstart', function(ev){ ev.preventDefault(); }, {passive:false});
        // ensure pointer-events remain on images
        img.style.userSelect = 'none';
        img.style.webkitUserDrag = 'none';
      }catch(e){}
    });
    // build UI (dots + counter)
    buildUI(root, reel, slides);
    // initial update
    updateUI(root, reel, slides);
    enableDrag(root, reel, slides);

    // sync on scroll with rAF throttle
    let rafPending = false;
    function onScroll(){
      if(rafPending) return;
      rafPending = true;
      requestAnimationFrame(()=>{ updateUI(root, reel, slides); rafPending = false; });
    }
    reel.addEventListener('scroll', onScroll, {passive:true});

    // update on resize (slides width may change)
    const ro = new ResizeObserver(()=> updateUI(root, reel, slides));
    ro.observe(reel);

    // ensure dots reflect current position on load
    setTimeout(()=> updateUI(root, reel, slides), 120);

    root.dataset.beslockInit = '1';
    console.info('product-gallery: initialized', root, 'slides=', slides.length);
  }

  function initAll(){
    const roots = findGalleries();
    roots.forEach(r=> initGallery(r));
  }

  /* Hide product excerpt on mobile via inline style to ensure override
     This is a defensive fix in case theme CSS loads after our stylesheet. */
  (function hideExcerptOnMobile(){
    const selectors = [
      '.single-product .product-page__excerpt',
      '.single-product .woocommerce-product-details__short-description',
      '.single-product .summary .woocommerce-product-details__short-description'
    ];
    const els = selectors.map(s => Array.from(document.querySelectorAll(s))).flat();
    if(!els.length) return;
    let raf;
    function apply(){
      const hide = window.innerWidth < 768;
      els.forEach(el => { el.style.display = hide ? 'none' : ''; });
    }
    window.addEventListener('resize', ()=>{ if(raf) cancelAnimationFrame(raf); raf = requestAnimationFrame(apply); }, {passive:true});
    try{ apply(); }catch(e){}
  })();

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initAll); else initAll();
  window.addEventListener('load', initAll);
  const mo = new MutationObserver(()=> initAll());
  mo.observe(document.body, {childList:true, subtree:true});

})();
