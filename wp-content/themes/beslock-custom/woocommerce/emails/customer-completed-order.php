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
			echo wp_kses(
				sprintf(
					/* translators: 1: customer first name, 2: BESLOCK brand */
					esc_html__( 'Hola %1$s, tu pedido %2$s ya está completado.', 'beslock-custom' ),
					esc_html( $order->get_billing_first_name() ),
					beslock_email_registered_brand()
				),
				beslock_email_registered_mark_allowed_html()
			);
		} else {
			echo wp_kses(
				sprintf(
					/* translators: %s: BESLOCK brand */
					esc_html__( 'Hola, tu pedido %s ya está completado.', 'beslock-custom' ),
					beslock_email_registered_brand()
				),
				beslock_email_registered_mark_allowed_html()
			);
		}
		?>
	</p>
	<p>
		<?php
			echo wp_kses(
				sprintf(
					/* translators: %s: BESLOCK brand */
					esc_html__( 'Gracias por confiar en %s', 'beslock-custom' ),
					beslock_email_registered_brand()
				),
				beslock_email_registered_mark_allowed_html()
			);
			?>
			<br>
			<?php esc_html_e( 'Te dejamos el resumen de tu compra y los datos de envío para que tengas todo a la mano.', 'beslock-custom' ); ?>
		</p>
	</div>

<table border="0" cellpadding="0" cellspacing="0" width="100%" class="beslock-note-card" role="presentation">
	<tr>
		<td>
			<strong><?php esc_html_e( 'Próximo paso', 'beslock-custom' ); ?></strong><br>
			<?php esc_html_e( 'Conserva este correo como soporte de tu compra. Si necesitas ayuda con instalación, garantía o acompañamiento, responde este mensaje y te ayudamos.', 'beslock-custom' ); ?>
		</td>
	</tr>
</table>

<?php
do_action( 'woocommerce_email_order_details', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_order_meta', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_customer_details', $order, $sent_to_admin, $plain_text, $email );

do_action( 'woocommerce_email_footer', $email );
