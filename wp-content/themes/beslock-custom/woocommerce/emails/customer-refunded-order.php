<?php
/**
 * BESLOCK customer refunded order email.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.4.0
 */

defined( 'ABSPATH' ) || exit;

$GLOBALS['beslock_email_order'] = $order;
do_action( 'woocommerce_email_header', esc_html__( 'Tu pedido fue reembolsado', 'beslock-custom' ), $email );
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
			? esc_html__( 'Se realizó un reembolso parcial de tu pedido. Abajo encuentras el detalle actualizado para tu control.', 'beslock-custom' )
			: esc_html__( 'Se realizó el reembolso de tu pedido. Abajo encuentras el detalle actualizado para tu control.', 'beslock-custom' );
		?>
	</p>
</div>

<?php
do_action( 'woocommerce_email_order_details', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_order_meta', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_customer_details', $order, $sent_to_admin, $plain_text, $email );

do_action( 'woocommerce_email_footer', $email );
