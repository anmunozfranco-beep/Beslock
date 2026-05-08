<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

// Use WooCommerce cart URL when available; fallback to /cart.
$cart_url = function_exists( 'wc_get_cart_url' ) ? wc_get_cart_url() : home_url( '/cart' );
$cart_count = 0;

if ( class_exists( 'WooCommerce' ) && WC()->cart ) {
  $cart_count = (int) WC()->cart->get_cart_contents_count();
}
?>
<header class="header" data-js="header">
  <div class="u-container header__bar" data-js="header-bar">
    <button
      id="menuBtn"
      class="header__icon header__icon--menu"
      data-js="drawer-toggle"
      aria-controls="mobileDrawer"
      aria-expanded="false"
      aria-label="<?php esc_attr_e( 'Open menu', 'beslock' ); ?>"
    >&#9776;</button>

    <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="header__logo" data-js="header-logo">
      <span class="logo-wrapper" data-js="header-logo-wrapper">
        <img src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/logo-green.png' ); ?>" alt="<?php esc_attr_e( 'BESLOCK Logo', 'beslock' ); ?>" data-js="header-logo-image" />
        <span class="logo__tm" aria-hidden="true" data-js="header-logo-tm">&#174;</span>
      </span>
    </a>

    <a
      href="<?php echo esc_url( $cart_url ); ?>"
      class="header__icon header__icon--cart"
      data-js="header-cart"
      aria-label="<?php esc_attr_e( 'Go to cart', 'beslock' ); ?>"
    >
      <i class="bi bi-cart" aria-hidden="true"></i>
      <?php if ( $cart_count > 0 ) : ?>
        <span class="header__cart-count" aria-hidden="true"><?php echo esc_html( $cart_count ); ?></span>
      <?php endif; ?>
    </a>
  </div>
</header>