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
        <img src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/logo-green.png' ); ?>" alt="<?php esc_attr_e( 'BESLOCK Logo', 'beslock' ); ?>" />
      </a>
    </div>

    <ul class="mobile-menu" data-js="mobile-drawer-menu" role="menu">
      <li class="mobile-menu__item" role="none">
        <button class="mobile-menu__link" id="productsToggle" data-js="drawer-products-toggle" aria-expanded="false" aria-controls="productsPanel" role="menuitem">
          <?php esc_html_e( 'Products', 'beslock' ); ?> <span class="products-chevron mobile-drawer__control-icon mobile-drawer__control-icon--forward" aria-hidden="true"></span>
        </button>

        <div id="productsPanel" class="mobile-products-panel models models--hidden" data-js="drawer-products-panel" role="region" aria-hidden="true" aria-labelledby="productsToggle">
          <?php get_template_part( 'templates/models-mobile' ); ?>
        </div>
      </li>

      <li class="mobile-menu__item" role="none">
        <a class="mobile-menu__link" href="<?php echo esc_url( home_url( '/offers' ) ); ?>" role="menuitem">
          <i class="bi bi-percent" aria-hidden="true"></i>
          <div class="mobile-menu__meta">
            <span class="mobile-menu__title">Catch our Limited Offers</span>
            <span class="mobile-menu__subtitle">Save and boost profits</span>
          </div>
        </a>
      </li>

      <li class="mobile-menu__item" role="none">
        <a class="mobile-menu__link" href="<?php echo esc_url( home_url( '/contact' ) ); ?>" role="menuitem">
          <i class="bi bi-headset" aria-hidden="true"></i>
          <div class="mobile-menu__meta">
            <span class="mobile-menu__title">Contact us Now</span>
            <span class="mobile-menu__subtitle">We are right back with you</span>
          </div>
        </a>
      </li>

      <li class="mobile-menu__item" role="none">
        <a class="mobile-menu__link" href="<?php echo esc_url( home_url( '/docs' ) ); ?>" role="menuitem">
          <i class="bi bi-hand-thumbs-up" aria-hidden="true"></i>
          <div class="mobile-menu__meta">
            <span class="mobile-menu__title">Technical Documentation</span>
            <span class="mobile-menu__subtitle">Top products on specifications</span>
          </div>
        </a>
      </li>
    </ul>
  </div>

  <div class="mobile-drawer__backdrop" id="drawerBackdrop" data-js="drawer-backdrop" tabindex="-1" aria-hidden="true"></div>
</nav>