<?php
/**
 * Shipping Methods Display
 *
 * In 2.1 we show methods per package. This allows for multiple methods per order if so desired.
 *
 * This template can be overridden by copying it to yourtheme/woocommerce/cart/cart-shipping.php.
 *
 * HOWEVER, on occasion WooCommerce will need to update template files and you
 * (the theme developer) will need to copy the new files to your theme to
 * maintain compatibility. We try to do this as little as possible, but it does
 * happen. When this occurs the version of the template file will be bumped and
 * the readme will list any important changes.
 *
 * @see https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates
 * @version 8.8.0
 */

defined( 'ABSPATH' ) || exit;

$formatted_destination    = isset( $formatted_destination ) ? $formatted_destination : WC()->countries->get_formatted_address( $package['destination'], ', ' );
$beslock_destination      = function_exists( 'beslock_format_cart_shipping_destination' ) ? beslock_format_cart_shipping_destination( isset( $package['destination'] ) ? $package['destination'] : array() ) : '';
$has_calculated_shipping  = ! empty( $has_calculated_shipping );
$has_confirmed_shipping   = function_exists( 'beslock_cart_has_confirmed_shipping_address' ) && beslock_cart_has_confirmed_shipping_address();
$show_shipping_calculator = ! empty( $show_shipping_calculator );
$calculator_text          = '';

if ( ! $has_confirmed_shipping ) {
    $formatted_destination = '';
} elseif ( '' !== $beslock_destination ) {
    $formatted_destination = $beslock_destination;
}
?>
<tr class="woocommerce-shipping-totals shipping">
    <th><?php esc_html_e( 'Envío', 'beslock-custom' ); ?></th>
    <td data-title="<?php esc_attr_e( 'Envío', 'beslock-custom' ); ?>">
        <?php if ( ! empty( $available_methods ) && is_array( $available_methods ) ) : ?>
            <ul id="shipping_method" class="woocommerce-shipping-methods">
                <?php foreach ( $available_methods as $method ) : ?>
                    <li>
                        <?php
                        if ( 1 < count( $available_methods ) ) {
                            printf( '<input type="radio" name="shipping_method[%1$d]" data-index="%1$d" id="shipping_method_%1$d_%2$s" value="%3$s" class="shipping_method" %4$s />', $index, esc_attr( sanitize_title( $method->id ) ), esc_attr( $method->id ), checked( $method->id, $chosen_method, false ) ); // WPCS: XSS ok.
                        } else {
                            printf( '<input type="hidden" name="shipping_method[%1$d]" data-index="%1$d" id="shipping_method_%1$d_%2$s" value="%3$s" class="shipping_method" />', $index, esc_attr( sanitize_title( $method->id ) ), esc_attr( $method->id ) ); // WPCS: XSS ok.
                        }
                        $shipping_method_label = wc_cart_totals_shipping_method_label( $method );
                        if ( isset( $method->method_id ) && 'free_shipping' === $method->method_id ) {
                            $shipping_method_label = esc_html__( 'Envío gratis', 'beslock-custom' );
                        } else {
                            $shipping_method_label = str_replace( array( 'Free shipping', 'Free Shipping' ), esc_html__( 'Envío gratis', 'beslock-custom' ), $shipping_method_label );
                        }

                        printf( '<label for="shipping_method_%1$s_%2$s">%3$s</label>', $index, esc_attr( sanitize_title( $method->id ) ), wp_kses_post( $shipping_method_label ) ); // WPCS: XSS ok.
                        do_action( 'woocommerce_after_shipping_rate', $method, $index );
                        ?>
                    </li>
                <?php endforeach; ?>
            </ul>
            <?php if ( is_cart() ) : ?>
                <p class="woocommerce-shipping-destination">
                    <?php
                    if ( $has_confirmed_shipping && $formatted_destination ) {
                        // Translators: $s shipping destination.
                        printf( esc_html__( 'Enviar a %s.', 'beslock-custom' ) . ' ', '<strong>' . esc_html( $formatted_destination ) . '</strong>' );
                        $calculator_text = esc_html__( 'Editar dirección de envío', 'beslock-custom' );
                    } else {
                        esc_html_e( 'Actualiza tu dirección para confirmar la entrega.', 'beslock-custom' );
                        $calculator_text = esc_html__( 'Ingresar dirección de envío', 'beslock-custom' );
                    }
                    ?>
                </p>
            <?php endif; ?>
            <?php
        elseif ( ! $has_calculated_shipping || ! $formatted_destination ) :
            if ( is_cart() && 'no' === get_option( 'woocommerce_enable_shipping_calc' ) ) {
                echo wp_kses_post( apply_filters( 'woocommerce_shipping_not_enabled_on_cart_html', __( 'Los costos de envío se calculan durante el pago.', 'beslock-custom' ) ) );
            } else {
                $calculator_text = esc_html__( 'Ingresar dirección de envío', 'beslock-custom' );
                echo wp_kses_post( apply_filters( 'woocommerce_shipping_may_be_available_html', __( 'Ingresa tu dirección para ver las opciones de envío.', 'beslock-custom' ) ) );
            }
        elseif ( ! is_cart() ) :
            echo wp_kses_post( apply_filters( 'woocommerce_no_shipping_available_html', __( 'No hay opciones de envío disponibles. Verifica que la dirección esté correcta o contáctanos si necesitas ayuda.', 'beslock-custom' ) ) );
        else :
            echo wp_kses_post(
                /**
                 * Provides a means of overriding the default 'no shipping available' HTML string.
                 *
                 * @since 3.0.0
                 *
                 * @param string $html                  HTML message.
                 * @param string $formatted_destination The formatted shipping destination.
                 */
                apply_filters(
                    'woocommerce_cart_no_shipping_available_html',
                    // Translators: $s shipping destination.
                    sprintf( esc_html__( 'No encontramos opciones de envío para %s.', 'beslock-custom' ) . ' ', '<strong>' . esc_html( $formatted_destination ) . '</strong>' ),
                    $formatted_destination
                )
            );
            $calculator_text = esc_html__( 'Editar dirección de envío', 'beslock-custom' );
        endif;
        ?>

        <?php if ( $show_package_details ) : ?>
            <?php echo '<p class="woocommerce-shipping-contents"><small>' . esc_html( $package_details ) . '</small></p>'; ?>
        <?php endif; ?>

        <?php if ( $show_shipping_calculator ) : ?>
            <?php woocommerce_shipping_calculator( $calculator_text ); ?>
        <?php endif; ?>
    </td>
</tr>
