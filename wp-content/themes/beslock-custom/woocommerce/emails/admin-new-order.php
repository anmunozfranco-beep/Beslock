<?php
/**
 * BESLOCK admin new order email.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.4.0
 */

defined( 'ABSPATH' ) || exit;

$GLOBALS['beslock_email_order'] = $order;
do_action( 'woocommerce_email_header', esc_html__( 'Nuevo pedido recibido', 'beslock-custom' ), $email );
unset( $GLOBALS['beslock_email_order'] );
?>

<div class="email-introduction">
	<p class="beslock-lead"><?php esc_html_e( 'Se registró un nuevo pedido en la tienda.', 'beslock-custom' ); ?></p>
	<p>
		<?php
		printf(
			/* translators: 1: order number, 2: customer name */
			esc_html__( 'El pedido #%1$s fue realizado por %2$s. Revisa el resumen, el método de pago y la dirección de envío registrada.', 'beslock-custom' ),
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
