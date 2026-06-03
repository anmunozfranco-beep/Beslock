<?php
/**
 * BESLOCK customer POS refunded order email.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.4.0
 */

defined( 'ABSPATH' ) || exit;

$GLOBALS['beslock_email_order'] = $order;
do_action( 'woocommerce_email_header', esc_html__( 'Compra POS reembolsada', 'beslock-custom' ), $email );
unset( $GLOBALS['beslock_email_order'] );
?>

<div class="email-introduction">
	<p class="beslock-lead">
		<?php
		if ( $order->get_billing_first_name() ) {
			printf(
				/* translators: %s: customer first name */
				esc_html__( 'Hola %s,', 'beslock-custom' ),
				esc_html( $order->get_billing_first_name() )
			);
		} else {
			esc_html_e( 'Hola,', 'beslock-custom' );
		}
		?>
	</p>
	<p>
		<?php
		echo $partial_refund
			? esc_html__( 'Se realizó un reembolso parcial de tu compra en punto de venta. Abajo encuentras el detalle actualizado.', 'beslock-custom' )
			: esc_html__( 'Se realizó el reembolso de tu compra en punto de venta. Abajo encuentras el detalle actualizado.', 'beslock-custom' );
		?>
	</p>
</div>

<?php
do_action( 'woocommerce_email_order_details', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_order_meta', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_customer_details', $order, $sent_to_admin, $plain_text, $email );

if ( ! empty( $pos_store_email ) || ! empty( $pos_store_phone_number ) || ! empty( $pos_store_address ) ) {
	echo '<table border="0" cellpadding="0" cellspacing="0" width="100%" class="beslock-note-card" role="presentation"><tr><td>';
	if ( ! empty( $pos_store_name ) ) {
		echo '<strong>' . esc_html( $pos_store_name ) . '</strong><br>';
	}
	if ( ! empty( $pos_store_email ) ) {
		echo esc_html( $pos_store_email ) . '<br>';
	}
	if ( ! empty( $pos_store_phone_number ) ) {
		echo esc_html( $pos_store_phone_number ) . '<br>';
	}
	if ( ! empty( $pos_store_address ) ) {
		echo wp_kses_post( wpautop( wptexturize( $pos_store_address ) ) );
	}
	echo '</td></tr></table>';
}

if ( ! empty( $pos_refund_returns_policy ) ) {
	echo '<h2>' . esc_html__( 'Política de reembolsos y devoluciones', 'beslock-custom' ) . '</h2>';
	echo wp_kses_post( wpautop( wptexturize( $pos_refund_returns_policy ) ) );
}

do_action( 'woocommerce_email_footer', $email );
