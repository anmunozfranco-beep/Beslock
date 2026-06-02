<?php
/**
 * BESLOCK customer completed order email.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.4.0
 */

defined( 'ABSPATH' ) || exit;

$GLOBALS['beslock_email_order'] = $order;
do_action(
	'woocommerce_email_header',
	sprintf(
		/* translators: %s: order number */
		esc_html__( 'Tu pedido #%s está completado', 'beslock-custom' ),
		esc_html( $order->get_order_number() )
	),
	$email
);
unset( $GLOBALS['beslock_email_order'] );
?>

<div class="email-introduction">
	<p class="beslock-lead">
		<?php
		if ( $order->get_billing_first_name() ) {
			printf(
				/* translators: %s: customer first name */
				esc_html__( 'Hola %s, tu pedido BESLOCK ya está completado.', 'beslock-custom' ),
				esc_html( $order->get_billing_first_name() )
			);
		} else {
			esc_html_e( 'Hola, tu pedido BESLOCK ya está completado.', 'beslock-custom' );
		}
		?>
	</p>
	<p><?php esc_html_e( 'Gracias por confiar en BESLOCK. Dejamos el resumen de tu compra y los datos registrados para que tengas todo a la mano.', 'beslock-custom' ); ?></p>
</div>

<table border="0" cellpadding="0" cellspacing="0" width="100%" class="beslock-note-card" role="presentation">
	<tr>
		<td>
			<strong><?php esc_html_e( 'Próximo paso', 'beslock-custom' ); ?></strong><br>
			<?php esc_html_e( 'Conserva este correo como referencia de tu pedido. Si necesitas soporte sobre instalación, garantía o acompañamiento, puedes responderlo directamente.', 'beslock-custom' ); ?>
		</td>
	</tr>
</table>

<?php
do_action( 'woocommerce_email_order_details', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_order_meta', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_customer_details', $order, $sent_to_admin, $plain_text, $email );

do_action( 'woocommerce_email_footer', $email );
