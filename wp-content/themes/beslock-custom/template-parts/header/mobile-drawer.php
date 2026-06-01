<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}
?>
<nav id="mobileDrawer" class="mobile-drawer" data-js="mobile-drawer" aria-hidden="true" role="dialog" aria-label="<?php esc_attr_e( 'Mobile menu', 'beslock' ); ?>">
  <div class="mobile-drawer__panel" data-js="mobile-drawer-panel" role="document">
    <div class="drawer-header" data-js="mobile-drawer-header" role="banner">
      <button id="closeDrawer" class="mobile-drawer__close" data-js="drawer-close" aria-label="<?php esc_attr_e( 'Close menu', 'beslock' ); ?>">
        <span class="mobile-drawer__control-icon mobile-drawer__close-icon" aria-hidden="true"></span>
        <span class="screen-reader-text"><?php esc_html_e( 'Close navigation', 'beslock' ); ?></span>
      </button>

      <a class="drawer__logo" href="<?php echo esc_url( home_url( '/' ) ); ?>" data-js="drawer-logo" aria-label="<?php esc_attr_e( 'Home', 'beslock' ); ?>">
        <span class="logo-wrapper">
          <img src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/logo-green.png' ); ?>" alt="<?php esc_attr_e( 'BESLOCK Logo', 'beslock' ); ?>" />
          <span class="logo__tm" aria-hidden="true">&#174;</span>
        </span>
      </a>
    </div>

    <ul class="mobile-menu" data-js="mobile-drawer-menu" role="menu">
      <li class="mobile-menu__item" role="none">
        <button class="mobile-menu__link" id="productsToggle" data-js="drawer-products-toggle" aria-expanded="false" aria-controls="productsPanel" role="menuitem">
          <?php esc_html_e( 'Productos', 'beslock' ); ?> <span class="products-chevron mobile-drawer__control-icon mobile-drawer__control-icon--forward" aria-hidden="true"></span>
        </button>

        <div id="productsPanel" class="mobile-products-panel models models--hidden" data-js="drawer-products-panel" role="region" aria-hidden="true" aria-labelledby="productsToggle">
          <?php get_template_part( 'templates/models-mobile' ); ?>
        </div>
      </li>

      <li class="mobile-menu__item mobile-menu__item--order-lookup" role="none">
        <button type="button" class="mobile-menu__link mobile-menu__link--order-lookup" id="orderLookupToggle" data-js="order-lookup-toggle" aria-expanded="false" aria-controls="orderLookupPanel" role="menuitem">
          <span class="mobile-menu__icon mobile-menu__icon--order-lookup" aria-hidden="true"></span>
          <div class="mobile-menu__meta">
            <span class="mobile-menu__title">Consulta tu pedido</span>
            <span class="mobile-menu__subtitle">Revisa el estado de tu compra</span>
          </div>
        </button>

        <div id="orderLookupPanel" class="mobile-menu-order-lookup" data-js="order-lookup-panel" role="region" aria-labelledby="orderLookupToggle" hidden>
          <form class="mobile-menu-order-lookup__form" action="<?php echo esc_url( home_url( '/consulta-pedido/' ) ); ?>" method="post" data-js="order-lookup-form" novalidate>
            <label class="mobile-menu-order-lookup__field">
              <span>Número de pedido</span>
              <input type="text" name="beslock_order_number" inputmode="numeric" autocomplete="off" data-js="order-lookup-order" />
            </label>

            <label class="mobile-menu-order-lookup__field">
              <span>Correo electrónico</span>
              <input type="email" name="beslock_order_email" autocomplete="email" data-js="order-lookup-email" />
            </label>

            <p class="mobile-menu-order-lookup__error" data-js="order-lookup-error" hidden></p>

            <button type="submit" class="mobile-menu-order-lookup__submit">Consultar</button>
          </form>
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
        <a class="mobile-menu__link" href="<?php echo esc_url( home_url( '/contact' ) ); ?>" role="menuitem">
          <i class="bi bi-headset" aria-hidden="true"></i>
          <div class="mobile-menu__meta">
            <span class="mobile-menu__title">Contacto</span>
            <span class="mobile-menu__subtitle">Estamos para ayudarte</span>
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

  <div class="mobile-drawer__backdrop" id="drawerBackdrop" data-js="drawer-backdrop" tabindex="-1" aria-hidden="true"></div>
</nav>
