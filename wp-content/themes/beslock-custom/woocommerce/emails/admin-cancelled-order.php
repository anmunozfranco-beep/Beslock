<?php
/**
 * BESLOCK admin cancelled order email.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 9.8.0
 */

defined( 'ABSPATH' ) || exit;

$GLOBALS['beslock_email_order'] = $order;
do_action( 'woocommerce_email_header', esc_html__( 'Pedido cancelado', 'beslock-custom' ), $email );
unset( $GLOBALS['beslock_email_order'] );
?>

<div class="email-introduction">
	<p class="beslock-lead"><?php esc_html_e( 'Un pedido fue cancelado.', 'beslock-custom' ); ?></p>
	<p>
		<?php
		printf(
			/* translators: 1: order number, 2: customer name */
			esc_html__( 'El pedido #%1$s de %2$s cambió a estado cancelado. Te dejamos el detalle para revisión interna.', 'beslock-custom' ),
			esc_html( $order->get_order_number() ),
			esc_html( $order->get_formatted_billing_full_name() )
		);
		?>
	</p>
</div>

<?php
do_action( 'woocommerce_email_order_details', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_order_meta', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_customer_details', $order, $sent_to_admin, $plain_text, $email );

do_action( 'woocommerce_email_footer', $email );
