<?php
// /wp-content/themes/beslock-custom/menu-simple.php
// Partial minimal para drawer móvil — SOLO el drawer (no incluye botón de abrir)
// Asegúrate de que el botón de apertura esté en header.php con id="menuBtn".
?>
<!-- Drawer principal: no incluye botón de apertura (ese está en header.php) -->
<nav id="mobileDrawer" class="mobile-drawer" aria-hidden="true" role="dialog" aria-label="<?php esc_attr_e('Mobile menu', 'beslock'); ?>">
  <div class="mobile-drawer__panel" role="document">
    <!-- Drawer header: close/back button at left and centered logo (same height as main header) -->
    <div class="drawer-header" role="banner">
      <!-- Close/back button placed at the left side of the header -->
      <button id="closeDrawer" class="mobile-drawer__close" aria-label="<?php esc_attr_e('Close menu', 'beslock'); ?>">
        <i class="bi bi-arrow-left" aria-hidden="true"></i>
        <span class="screen-reader-text"><?php esc_html_e('Back', 'beslock'); ?></span>
      </button>

      <!-- Centered logo (positioned absolutely to match header behavior) -->
      <a class="drawer__logo" href="<?php echo esc_url( home_url('/') ); ?>" aria-label="<?php esc_attr_e('Home', 'beslock'); ?>">
        <span class="logo-wrapper">
          <img src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/logo-green.png' ); ?>" alt="<?php esc_attr_e('BESLOCK Logo', 'beslock'); ?>" />
          <span class="logo__tm" aria-hidden="true">®</span>
        </span>
      </a>
    </div>

    <ul class="mobile-menu" role="menu">
      <li class="mobile-menu__item" role="none">
        <button class="mobile-menu__link" id="productsToggle" aria-expanded="false" aria-controls="productsPanel" role="menuitem">
          <?php esc_html_e('Productos', 'beslock'); ?> <span class="chev" aria-hidden="true">›</span>
        </button>

        <?php
        /**
         * Panel semántico para Products.
         * - Oculto por defecto (aria-hidden="true")
         * - id="productsPanel" enlazado desde aria-controls en el botón
         * - role="region" para describir área del drawer que contiene el contenido de Products
         * - Contenido provisto por template-part: templates/models-mobile.php
         *
         * Nota: la visibilidad se controla con aria-* y clases (.models--hidden / .models--visible).
         */
        ?>
        <div id="productsPanel" class="mobile-products-panel models models--hidden" role="region" aria-hidden="true" aria-labelledby="productsToggle">
          <?php
            // Cargamos el template-part con las tarjetas (models)
            get_template_part( 'templates/models-mobile' );
          ?>
        </div>
      </li>

      <li class="mobile-menu__item mobile-menu__item--manuals" role="none">
        <button class="mobile-menu__link mobile-menu__link--manuals" id="manualsToggle" data-js="drawer-manuals-toggle" aria-expanded="false" aria-controls="manualsSectionsPanel" role="menuitem">
          <span class="mobile-menu__icon mobile-menu__icon--guides" aria-hidden="true"></span>
          <div class="mobile-menu__meta">
            <span class="mobile-menu__title">Guías BESLOCK</span>
            <span class="mobile-menu__subtitle">Manuales y ayuda del producto</span>
          </div>
        </button>

        <div id="manualsSectionsPanel" class="manuals-sections-panel" data-js="drawer-manuals-sections" role="region" aria-hidden="true" hidden>
          <button type="button" class="manuals-section-button" data-manual-section="conoce-tu-cerradura">Conoce tu cerradura</button>
          <button type="button" class="manuals-section-button" data-manual-section="instalacion">Instalación</button>
          <button type="button" class="manuals-section-button" data-manual-section="configuracion">Configuración</button>
          <button type="button" class="manuals-section-button" data-manual-section="uso-diario">Uso diario</button>
          <button type="button" class="manuals-section-button" data-manual-section="soluciones-rapidas">Soluciones rápidas</button>
        </div>
      </li>

      <li class="mobile-menu__item" role="none">
        <a class="mobile-menu__link" href="<?php echo esc_url( home_url('/offers') ); ?>" role="menuitem">
          <i class="bi bi-percent" aria-hidden="true"></i>
          <div class="mobile-menu__meta">
            <span class="mobile-menu__title">Catch our Limited Offers</span>
            <span class="mobile-menu__subtitle">Save and boost profits</span>
          </div>
        </a>
      </li>

      <li class="mobile-menu__item" role="none">
        <a class="mobile-menu__link" href="<?php echo esc_url( home_url('/contact') ); ?>" role="menuitem">
          <i class="bi bi-headset" aria-hidden="true"></i>
          <div class="mobile-menu__meta">
            <span class="mobile-menu__title">Contact us Now</span>
            <span class="mobile-menu__subtitle">We are right back with you</span>
          </div>
        </a>
      </li>

    </ul>
  </div>

  <aside id="manualsDrawer" class="manuals-drawer" data-js="manuals-drawer" aria-hidden="true" aria-label="<?php esc_attr_e( 'BESLOCK guides', 'beslock' ); ?>">
    <div class="manuals-drawer__shell" data-js="manuals-drawer-shell">
      <header class="manuals-drawer__header">
        <div>
          <p class="manuals-drawer__eyebrow" data-js="manuals-drawer-eyebrow">Guías BESLOCK</p>
          <h2 class="manuals-drawer__title" data-js="manuals-drawer-title">Manuales y ayuda</h2>
        </div>
        <button type="button" class="manuals-drawer__close" data-js="manuals-drawer-close" aria-label="<?php esc_attr_e( 'Close guides', 'beslock' ); ?>">
          <i class="bi bi-x-lg" aria-hidden="true"></i>
        </button>
      </header>
      <div class="manuals-drawer__body" data-js="manuals-drawer-body" tabindex="-1"></div>
    </div>
  </aside>

  <!-- Backdrop para cerrar tocando afuera -->
  <div class="mobile-drawer__backdrop" id="drawerBackdrop" tabindex="-1" aria-hidden="true"></div>
</nav>
