<?php
/**
 * BESLOCK customer invoice / payment request email.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.4.0
 */

defined( 'ABSPATH' ) || exit;

$GLOBALS['beslock_email_order'] = $order;
do_action( 'woocommerce_email_header', $email_heading, $email );
unset( $GLOBALS['beslock_email_order'] );
?>

<div class="email-introduction">
	<p class="beslock-lead">
		<?php
		if ( $order->get_billing_first_name() ) {
			printf(
				/* translators: %s: customer first name */
				esc_html__( 'Hola %s, tu pedido BESLOCK está reservado.', 'beslock-custom' ),
				esc_html( $order->get_billing_first_name() )
			);
		} else {
			esc_html_e( 'Hola, tu pedido BESLOCK está reservado.', 'beslock-custom' );
		}
		?>
	</p>
	<?php if ( $order->needs_payment() ) : ?>
		<p><?php esc_html_e( 'Aún aparece pendiente de pago. Puedes revisar el detalle y finalizarlo desde el enlace seguro de WooCommerce cuando estés listo.', 'beslock-custom' ); ?></p>
		<p>
			<a class="beslock-button" href="<?php echo esc_url( $order->get_checkout_payment_url() ); ?>">
				<?php esc_html_e( 'Finalizar pago', 'beslock-custom' ); ?>
			</a>
		</p>
	<?php elseif ( $order->has_status( wc_get_is_paid_statuses() ) ) : ?>
		<p><?php esc_html_e( 'Tu pago ya figura registrado. Abajo encuentras el detalle completo del pedido.', 'beslock-custom' ); ?></p>
	<?php else : ?>
		<p><?php esc_html_e( 'Abajo encuentras el detalle completo de tu pedido.', 'beslock-custom' ); ?></p>
	<?php endif; ?>
</div>

<table border="0" cellpadding="0" cellspacing="0" width="100%" class="beslock-note-card" role="presentation">
	<tr>
		<td>
			<strong><?php esc_html_e( 'Pago pendiente', 'beslock-custom' ); ?></strong><br>
			<?php esc_html_e( 'El enlace te lleva al checkout de este pedido para revisar el detalle y completar el pago cuando estés listo.', 'beslock-custom' ); ?>
		</td>
	</tr>
</table>

<?php
do_action( 'woocommerce_email_order_details', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_order_meta', $order, $sent_to_admin, $plain_text, $email );
do_action( 'woocommerce_email_customer_details', $order, $sent_to_admin, $plain_text, $email );

do_action( 'woocommerce_email_footer', $email );
