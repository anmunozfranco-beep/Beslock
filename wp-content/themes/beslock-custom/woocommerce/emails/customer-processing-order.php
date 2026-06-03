<?php
/**
 * BESLOCK customer processing order email.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.4.0
 */

defined( 'ABSPATH' ) || exit;

$GLOBALS['beslock_email_order'] = $order;
do_action(
	'woocommerce_email_header',
	esc_html__( 'Recibimos tu pedido en BESLOCK®', 'beslock-custom' ),
	$email
);
unset( $GLOBALS['beslock_email_order'] );
?>

<div class="email-introduction">
	<p class="beslock-lead">
		<?php
		if ( $order->get_billing_first_name() ) {
			echo wp_kses(
				sprintf(
					/* translators: 1: customer first name, 2: BESLOCK brand */
					esc_html__( 'Hola %1$s, gracias por comprar en %2$s', 'beslock-custom' ),
					esc_html( $order->get_billing_first_name() ),
					beslock_email_registered_brand()
				),
				beslock_email_registered_mark_allowed_html()
			);
		} else {
			echo wp_kses(
				sprintf(
					/* translators: %s: BESLOCK brand */
					esc_html__( 'Hola, gracias por comprar en %s', 'beslock-custom' ),
					beslock_email_registered_brand()
				),
				beslock_email_registered_mark_allowed_html()
			);
		}
		?>
	</p>
	<p><?php esc_html_e( 'Ya recibimos tu pedido y lo estamos preparando. Te compartimos el resumen de la compra, el método de pago y la dirección de envío registrada.', 'beslock-custom' ); ?></p>
</div>

<?php
do_action( 'woocommerce_email_order_details', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_order_meta', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_customer_details', $order, $sent_to_admin, $plain_text, $email );

do_action( 'woocommerce_email_footer', $email );
