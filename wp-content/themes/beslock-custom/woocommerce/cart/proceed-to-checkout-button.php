<?php
/**
 * Proceed to checkout button
 *
 * Contains the markup for the proceed to checkout button on the cart.
 *
 * This template can be overridden by copying it to yourtheme/woocommerce/cart/proceed-to-checkout-button.php.
 *
 * HOWEVER, on occasion WooCommerce will need to update template files and you
 * (the theme developer) will need to copy the new files to your theme to
 * maintain compatibility. We try to do this as little as possible, but it does
 * happen. When this occurs the version of the template file will be bumped and
 * the readme will list any important changes.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates
 * @version 7.0.1
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit; // Exit if accessed directly.
}

$requires_shipping_confirmation = function_exists( 'beslock_cart_requires_shipping_address_confirmation' ) && beslock_cart_requires_shipping_address_confirmation();
?>

<?php if ( $requires_shipping_confirmation ) : ?>
<span class="checkout-button button alt wc-forward beslock-checkout-button--disabled<?php echo esc_attr( wc_wp_theme_get_element_class_name( 'button' ) ? ' ' . wc_wp_theme_get_element_class_name( 'button' ) : '' ); ?>" role="button" aria-disabled="true">
    <?php esc_html_e( 'Actualiza tu dirección para continuar', 'beslock-custom' ); ?>
</span>
<p class="beslock-checkout-blocked-note"><?php esc_html_e( 'Confirma la dirección de envío antes de continuar con el pago.', 'beslock-custom' ); ?></p>
<?php else : ?>
<a href="<?php echo esc_url( wc_get_checkout_url() ); ?>" class="checkout-button button alt wc-forward<?php echo esc_attr( wc_wp_theme_get_element_class_name( 'button' ) ? ' ' . wc_wp_theme_get_element_class_name( 'button' ) : '' ); ?>">
    <?php esc_html_e( 'Continuar con el pago', 'beslock-custom' ); ?>
</a>
<?php endif; ?>
