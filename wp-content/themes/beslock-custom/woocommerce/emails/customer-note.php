<?php
/**
 * BESLOCK customer note email.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.4.0
 */

defined( 'ABSPATH' ) || exit;

$GLOBALS['beslock_email_order'] = $order;
do_action( 'woocommerce_email_header', esc_html__( 'Tenemos una actualización de tu pedido', 'beslock-custom' ), $email );
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
	<p><?php esc_html_e( 'Agregamos la siguiente nota a tu pedido:', 'beslock-custom' ); ?></p>
</div>

<table border="0" cellpadding="0" cellspacing="0" width="100%" class="beslock-note-card" role="presentation">
	<tr>
		<td>
			<?php
			$safe_note = wc_wptexturize_order_note( $customer_note );
			echo wp_kses_post( wpautop( make_clickable( $safe_note ) ) );
			?>
		</td>
	</tr>
</table>

<p><?php esc_html_e( 'También te dejamos el resumen del pedido para que tengas todo a la mano.', 'beslock-custom' ); ?></p>

<?php
do_action( 'woocommerce_email_order_details', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_order_meta', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_customer_details', $order, $sent_to_admin, $plain_text, $email );

do_action( 'woocommerce_email_footer', $email );
