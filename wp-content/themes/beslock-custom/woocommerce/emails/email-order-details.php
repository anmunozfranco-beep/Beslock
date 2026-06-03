<?php
/**
 * BESLOCK order details table shown in emails.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.7.0
 */

defined( 'ABSPATH' ) || exit;

$text_align       = is_rtl() ? 'right' : 'left';
$opposite_align   = is_rtl() ? 'left' : 'right';
$date_created     = $order->get_date_created();
$order_table_class = 'email-order-details';
$tax_display       = get_option( 'woocommerce_tax_display_cart' );
$price_args        = array(
	'currency' => $order->get_currency(),
);
$shipping_total    = (float) $order->get_shipping_total();
$shipping_tax      = (float) $order->get_shipping_tax();
$shipping_amount   = 'incl' === $tax_display ? $shipping_total + $shipping_tax : $shipping_total;
$subtotal_amount   = max( 0, (float) $order->get_total() - $shipping_amount );
$payment_method    = $order->get_payment_method_title();
$payment_labels     = array(
	'direct bank transfer' => esc_html__( 'Transferencia bancaria directa', 'beslock-custom' ),
	'bank transfer'        => esc_html__( 'Transferencia bancaria', 'beslock-custom' ),
	'check payments'       => esc_html__( 'Pago con cheque', 'beslock-custom' ),
	'cash on delivery'     => esc_html__( 'Pago contra entrega', 'beslock-custom' ),
	'credit card'          => esc_html__( 'Tarjeta de crédito', 'beslock-custom' ),
	'debit card'           => esc_html__( 'Tarjeta débito', 'beslock-custom' ),
);

if ( ! $payment_method ) {
	$payment_method = esc_html__( 'Por confirmar', 'beslock-custom' );
} elseif ( isset( $payment_labels[ strtolower( trim( wp_strip_all_tags( $payment_method ) ) ) ] ) ) {
	$payment_method = $payment_labels[ strtolower( trim( wp_strip_all_tags( $payment_method ) ) ) ];
}

do_action( 'woocommerce_email_before_order_table', $order, $sent_to_admin, $plain_text, $email );
?>

<h2 class="beslock-order-heading">
	<?php esc_html_e( 'Resumen del pedido', 'beslock-custom' ); ?>
	<span>
		<?php
		printf(
			/* translators: 1: order number, 2: order date */
			esc_html__( 'Pedido #%1$s%2$s', 'beslock-custom' ),
			esc_html( $order->get_order_number() ),
			$date_created ? esc_html( ' · ' . wc_format_datetime( $date_created ) ) : ''
		);
		?>
	</span>
</h2>

<div class="beslock-order-shell">
	<table class="td font-family <?php echo esc_attr( $order_table_class ); ?>" cellspacing="0" cellpadding="0" style="width: 100%;" border="0" role="presentation">
		<thead>
			<tr>
				<th class="td" scope="col" style="text-align:<?php echo esc_attr( $text_align ); ?>;"><?php esc_html_e( 'Producto', 'beslock-custom' ); ?></th>
				<th class="td" scope="col" style="text-align:<?php echo esc_attr( $opposite_align ); ?>;"><?php esc_html_e( 'Cantidad', 'beslock-custom' ); ?></th>
				<th class="td" scope="col" style="text-align:<?php echo esc_attr( $opposite_align ); ?>;"><?php esc_html_e( 'Precio', 'beslock-custom' ); ?></th>
			</tr>
		</thead>
		<tbody>
			<?php
			echo wc_get_email_order_items( // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
				$order,
				array(
					'show_sku'      => $sent_to_admin,
					'show_image'    => true,
					'image_size'    => array( 64, 64 ),
					'plain_text'    => $plain_text,
					'sent_to_admin' => $sent_to_admin,
				)
			);
			?>
		</tbody>
	</table>

	<table class="td font-family beslock-totals-table" cellspacing="0" cellpadding="0" style="width: 100%;" border="0" role="presentation">
		<tr class="order-totals order-totals-subtotal">
			<th class="td text-align-left" scope="row" colspan="2"><?php esc_html_e( 'Subtotal', 'beslock-custom' ); ?></th>
			<td class="td text-align-right"><?php echo wp_kses_post( wc_price( $subtotal_amount, $price_args ) ); ?></td>
		</tr>
		<tr class="order-totals order-totals-shipping">
			<th class="td text-align-left" scope="row" colspan="2"><?php esc_html_e( 'Envío', 'beslock-custom' ); ?></th>
			<td class="td text-align-right">
				<?php
				echo wp_kses_post(
					$shipping_amount > 0
						? wc_price( $shipping_amount, $price_args )
						: esc_html__( 'Sin costo', 'beslock-custom' )
				);
				?>
			</td>
		</tr>
		<tr class="order-totals order-totals-total order-totals-last">
			<th class="td text-align-left" scope="row" colspan="2"><?php esc_html_e( 'Total', 'beslock-custom' ); ?></th>
			<td class="td text-align-right"><?php echo wp_kses_post( $order->get_formatted_order_total() ); ?></td>
		</tr>
		<tr class="order-totals order-totals-payment-method">
			<th class="td text-align-left" scope="row" colspan="2"><?php esc_html_e( 'Método de pago', 'beslock-custom' ); ?></th>
			<td class="td text-align-right"><?php echo esc_html( $payment_method ); ?></td>
		</tr>
	</table>

	<?php if ( $order->get_customer_note() ) : ?>
		<table class="beslock-customer-note" cellspacing="0" cellpadding="0" border="0" role="presentation">
			<tr>
				<td>
					<strong><?php esc_html_e( 'Nota del cliente', 'beslock-custom' ); ?></strong><br>
					<?php echo wp_kses( nl2br( wc_wptexturize_order_note( $order->get_customer_note() ) ), array( 'br' => array() ) ); ?>
				</td>
			</tr>
		</table>
	<?php endif; ?>
</div>

<?php
do_action( 'woocommerce_email_after_order_table', $order, $sent_to_admin, $plain_text, $email );
