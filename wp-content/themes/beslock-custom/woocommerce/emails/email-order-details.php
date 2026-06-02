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
		<?php
		$item_totals       = $order->get_order_item_totals();
		$item_totals_count = count( $item_totals );

		if ( $item_totals ) {
			$i = 0;
			foreach ( $item_totals as $total ) {
				++$i;
				$last_class = ( $i === $item_totals_count ) ? ' order-totals-last' : '';
				?>
				<tr class="order-totals order-totals-<?php echo esc_attr( $total['type'] ?? 'unknown' ); ?><?php echo esc_attr( $last_class ); ?>">
					<th class="td text-align-left" scope="row" colspan="2">
						<?php
						echo wp_kses_post( $total['label'] ) . ' ';
						echo isset( $total['meta'] ) ? wp_kses_post( $total['meta'] ) : '';
						?>
					</th>
					<td class="td text-align-right"><?php echo wp_kses_post( $total['value'] ); ?></td>
				</tr>
				<?php
			}
		}
		?>
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
