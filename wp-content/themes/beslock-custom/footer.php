<?php
// /wp-content/themes/beslock-custom/footer.php
// Footer minimal con logo blanco centrado.
// Incluye aqu��� los elementos que removimos del header: el script de sticky header,
// la sincronizaci���n de la variable CSS del logo (para que el footer calcule 40%),
// y la llamada a wp_footer() seguida de los cierres </body></html>.
?>
<footer class="site-footer" aria-label="<?php echo esc_attr_x( 'Pie de página BESLOCK', 'footer landmark', 'beslock' ); ?>">
  <div class="site-footer__inner">
    <div class="site-footer__grid">
      <section class="site-footer__brand" aria-label="<?php echo esc_attr_x( 'BESLOCK', 'footer brand section', 'beslock' ); ?>">
        <a class="site-footer__logo-link" href="<?php echo esc_url( home_url( '/' ) ); ?>" aria-label="<?php echo esc_attr_x( 'Volver al inicio', 'footer home link', 'beslock' ); ?>">
          <span class="site-footer__logo-mark">
            <img
              class="footer-logo"
              src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/logo-green.png' ); ?>"
              alt="<?php echo esc_attr_x( 'BESLOCK', 'alt text', 'beslock' ); ?>"
              loading="lazy"
              decoding="async"
            />
            <span class="site-footer__registered" aria-hidden="true">&#174;</span>
          </span>
        </a>
        <p class="site-footer__brand-copy">
          Seguridad inteligente para hogares, oficinas y accesos exteriores.
        </p>

        <?php
          $footer_partner_logo_path = get_stylesheet_directory() . '/assets/images/partners/zonas-smart-logo.png';
          $footer_partner_logo_url  = get_stylesheet_directory_uri() . '/assets/images/partners/zonas-smart-logo.png';

          if ( file_exists( $footer_partner_logo_path ) ) :
            $footer_partner_logo_url = $footer_partner_logo_url . '?v=' . filemtime( $footer_partner_logo_path );
        ?>
          <div class="site-footer__partner" aria-label="<?php echo esc_attr_x( 'Comercializador autorizado en Colombia', 'footer partner section', 'beslock' ); ?>">
            <span class="site-footer__partner-kicker">Comercializador autorizado</span>
            <img
              class="site-footer__partner-logo"
              src="<?php echo esc_url( $footer_partner_logo_url ); ?>"
              alt="<?php echo esc_attr_x( 'ZONAS SMART', 'alt text', 'beslock' ); ?>"
              width="1024"
              height="1024"
              loading="lazy"
              decoding="async"
            />
          </div>
        <?php endif; ?>

        <div class="site-footer__payments" aria-label="<?php echo esc_attr_x( 'Pagos seguros', 'footer payments label', 'beslock' ); ?>">
          <span class="site-footer__payments-label">Pagos seguros mediante</span>
          <div class="site-footer__payment-logos">
            <a class="site-footer__payment-link" href="https://wompi.co/" target="_blank" rel="noopener noreferrer" aria-label="Wompi">
              <img
                class="site-footer__payment-logo site-footer__payment-logo--wompi"
                src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/payment/wompi.svg' ); ?>"
                alt="Wompi"
                loading="lazy"
                decoding="async"
              />
            </a>
            <a class="site-footer__payment-link" href="https://paypal.com/" target="_blank" rel="noopener noreferrer" aria-label="PayPal">
              <img
                class="site-footer__payment-logo site-footer__payment-logo--paypal"
                src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/payment/paypal.png' ); ?>"
                alt="PayPal"
                loading="lazy"
                decoding="async"
              />
            </a>
          </div>
        </div>
      </section>

      <nav class="site-footer__nav" aria-label="<?php echo esc_attr_x( 'Centro de ayuda', 'footer nav label', 'beslock' ); ?>">
        <h2 class="site-footer__heading">Centro de ayuda</h2>
        <ul class="site-footer__list">
          <li><a href="<?php echo esc_url( home_url( '/consulta-pedido/' ) ); ?>">Consulta tu pedido</a></li>
          <li><a href="<?php echo esc_url( add_query_arg( 'drawer', 'guides', home_url( '/' ) ) ); ?>">Guías BESLOCK</a></li>
          <li><a href="<?php echo esc_url( add_query_arg( 'drawer', 'contact', home_url( '/' ) ) ); ?>">Contacto</a></li>
        </ul>
      </nav>

      <nav class="site-footer__nav site-footer__nav--products" aria-label="<?php echo esc_attr_x( 'Productos', 'footer nav label', 'beslock' ); ?>">
        <h2 class="site-footer__heading">Productos</h2>
        <ul class="site-footer__list site-footer__list--products">
          <li class="site-footer__product-item">
            <a class="site-footer__product-link" href="<?php echo esc_url( home_url( '/producto/e-shield/' ) ); ?>">
              <span class="site-footer__product-name">e-Shield</span>
              <span class="site-footer__product-note">Exterior robusto.</span>
            </a>
          </li>
          <li class="site-footer__product-item">
            <a class="site-footer__product-link" href="<?php echo esc_url( home_url( '/producto/e-orbit/' ) ); ?>">
              <span class="site-footer__product-name">e-Orbit</span>
              <span class="site-footer__product-note">Experiencia avanzada.</span>
            </a>
          </li>
          <li class="site-footer__product-item">
            <a class="site-footer__product-link" href="<?php echo esc_url( home_url( '/producto/e-prime/' ) ); ?>">
              <span class="site-footer__product-name">e-Prime</span>
              <span class="site-footer__product-note">Control elegante.</span>
            </a>
          </li>
          <li class="site-footer__product-item">
            <a class="site-footer__product-link" href="<?php echo esc_url( home_url( '/producto/e-flex/' ) ); ?>">
              <span class="site-footer__product-name">e-Flex</span>
              <span class="site-footer__product-note">Acceso flexible.</span>
            </a>
          </li>
          <li class="site-footer__product-item">
            <a class="site-footer__product-link" href="<?php echo esc_url( home_url( '/producto/e-touch/' ) ); ?>">
              <span class="site-footer__product-name">e-Touch</span>
              <span class="site-footer__product-note">Privacidad interior.</span>
            </a>
          </li>
          <li class="site-footer__product-item">
            <a class="site-footer__product-link" href="<?php echo esc_url( home_url( '/producto/e-nova/' ) ); ?>">
              <span class="site-footer__product-name">e-Nova</span>
              <span class="site-footer__product-note">Entrada personal.</span>
            </a>
          </li>
        </ul>
      </nav>

      <nav class="site-footer__nav" aria-label="<?php echo esc_attr_x( 'Información', 'footer nav label', 'beslock' ); ?>">
        <h2 class="site-footer__heading">Información</h2>
        <ul class="site-footer__list">
          <li><a href="<?php echo esc_url( home_url( '/carrito/' ) ); ?>">Carrito</a></li>
          <li><a href="<?php echo esc_url( home_url( '/terminos-y-condiciones/' ) ); ?>">Términos y condiciones</a></li>
          <li><a href="<?php echo esc_url( home_url( '/politica-de-privacidad/' ) ); ?>">Política de privacidad</a></li>
        </ul>
      </nav>
    </div>

    <div class="site-footer__bottom">
      <p class="site-footer__copyright">
        © 2026 BESLOCK.<br>
        Todos los derechos reservados.
      </p>
    </div>
  </div>
</footer>

<!-- Sticky header / shrink (moved here desde header.php para centralizar scripts en el footer) -->
<script>
(function(){
  // Throttled scroll handler to toggle .header--scrolled
  var last = 0;
  var throttleMS = 90;
  // HERO gate (12vh) — recomputed on init and resize only
  var HERO_GATE = (window && window.innerHeight) ? window.innerHeight * 0.12 : 0;
  function updateHeroGate() { try { HERO_GATE = window.innerHeight * 0.12; } catch (e) {} }

  function onScroll() {
    var now = Date.now();
    if (now - last < throttleMS) return;
    last = now;
    var header = document.querySelector('.header');
    if (!header) return;
    var y = window.scrollY || 0;
    // While inside the hero keep header fully in its initial state
    if (y < HERO_GATE) {
      header.classList.remove('header--scrolled');
      return;
    }
    if (y > 10) {
      header.classList.add('header--scrolled');
    } else {
      header.classList.remove('header--scrolled');
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  // Keep HERO_GATE correct on resize
  window.addEventListener('resize', function(){
    updateHeroGate();
  }, { passive: true });

  // Sincroniza el tama���o del logo del header con la variable CSS --site-logo-height
  // para que el footer pueda usar calc(var(--site-logo-height) * 0.4)
  function updateSiteLogoHeight() {
    var logo = document.querySelector('.header__logo img');
    if (!logo) return;
    // Si la imagen a���n no tiene tama���o, intenta esperar a load
    var setVar = function() {
      var h = logo.clientHeight || logo.naturalHeight || 0;
      if (h && h > 0) {
        document.documentElement.style.setProperty('--site-logo-height', h + 'px');
      }
    };
    // Si la imagen ya est��� cargada
    if (logo.complete) {
      setVar();
    } else {
      // cuando se cargue la imagen, actualiza
      logo.addEventListener('load', setVar, { once: true });
      // fallback: intenta de inmediato
      setVar();
    }
  }

  // Actualiza al cargar el DOM, al cargar la ventana y al redimensionar
  document.addEventListener('DOMContentLoaded', updateSiteLogoHeight);
  window.addEventListener('load', updateSiteLogoHeight);
  window.addEventListener('resize', function() {
    // debounce ligero
    clearTimeout(window.__beslock_logo_h_timeout);
    window.__beslock_logo_h_timeout = setTimeout(updateSiteLogoHeight, 120);
  });
})();
</script>

<?php wp_footer(); ?>

<!-- product-gallery-reel fetch+eval fallback DISABLED (was causing load issues). -->
<script>console && console.info && console.info('product-gallery-reel: fetch fallback disabled');</script>

</body>
</html>

<script>
// Fallback ligero: si por alguna razón no se inicializó el drawer JS, este handler
// garantiza que el botón del menú abra/cierre el drawer de forma básica.
(function(){
  function initFallback() {
    try {
      var menuBtn = document.getElementById('menuBtn');
      var mobileDrawer = document.getElementById('mobileDrawer');
      var backdrop = document.getElementById('drawerBackdrop') || document.querySelector('.mobile-drawer__backdrop');
      if (!menuBtn || !mobileDrawer) return;

      // No sobrescribimos si ya existe la API moderna
      if (window.beslock && window.beslock.drawer && (typeof window.beslock.drawer.open === 'function')) return;

      function open() {
        mobileDrawer.classList.add('is-open');
        mobileDrawer.setAttribute('aria-hidden','false');
        menuBtn.setAttribute('aria-expanded','true');
        if (backdrop) backdrop.classList.add('backdrop-visible');
        document.documentElement.classList.add('has-drawer-open');
        document.body.style.position = 'fixed';
      }
      function close() {
        mobileDrawer.classList.remove('is-open');
        mobileDrawer.setAttribute('aria-hidden','true');
        menuBtn.setAttribute('aria-expanded','false');
        if (backdrop) backdrop.classList.remove('backdrop-visible');
        document.documentElement.classList.remove('has-drawer-open');
        document.body.style.position = '';
      }

      menuBtn.addEventListener('click', function(e){ e && e.preventDefault && e.preventDefault(); if (mobileDrawer.classList.contains('is-open')) close(); else open(); });
      if (backdrop) backdrop.addEventListener('click', function(e){ e && e.preventDefault && e.preventDefault(); close(); });
    } catch (e) { /* silent */ }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initFallback); else initFallback();
})();
</script>
<script>
// Emergency runtime safeguard: if header or cart are hidden by other scripts,
// force them visible. This runs late to override transient states.
(function(){
  try{
    var hdr = document.querySelector('.header');
    if(hdr){ hdr.style.setProperty('display','flex','important'); hdr.style.setProperty('visibility','visible'); hdr.style.setProperty('opacity','1'); hdr.style.setProperty('z-index','9998'); }
    var cart = document.querySelector('.header__icon--cart');
    if(cart){ cart.style.setProperty('display','flex','important'); cart.style.setProperty('visibility','visible'); cart.style.setProperty('opacity','1'); cart.style.setProperty('z-index','9999'); }
    var tm = document.querySelector('.logo__tm');
    if(tm){ tm.style.setProperty('font-size','20px','important'); tm.style.setProperty('opacity','1'); tm.style.setProperty('display','inline-flex','important'); }
  }catch(e){ console && console.error && console.error('beslock: emergency header restore failed', e); }
})();
</script>
<script>
