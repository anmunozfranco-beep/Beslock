<?php
/**
 * BESLOCK email addresses.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.6.0
 */

defined( 'ABSPATH' ) || exit;

$shipping = $order->get_formatted_shipping_address();

if ( ! $shipping ) {
	$shipping = $order->get_formatted_billing_address();
}
?>

<table id="addresses" cellspacing="0" cellpadding="0" style="width: 100%; vertical-align: top; padding:0;" border="0" role="presentation">
	<tr>
		<td class="font-family text-align-left beslock-address-cell" style="border:0; padding:0;" valign="top" width="100%">
			<div class="beslock-address-card">
				<strong class="address-title"><?php esc_html_e( 'Dirección de envío', 'beslock-custom' ); ?></strong>
				<address class="address">
					<?php echo wp_kses_post( $shipping ? $shipping : esc_html__( 'No disponible', 'beslock-custom' ) ); ?>
					<?php if ( $order->get_shipping_phone() ) : ?>
						<br><?php echo wc_make_phone_clickable( $order->get_shipping_phone() ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
					<?php endif; ?>
					<?php if ( ! $order->get_shipping_phone() && $order->get_billing_phone() ) : ?>
						<br><?php echo wc_make_phone_clickable( $order->get_billing_phone() ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
					<?php endif; ?>
					<?php
					do_action( 'woocommerce_email_customer_address_section', 'shipping', $order, $sent_to_admin, false );
					?>
				</address>
			</div>
		</td>
	</tr>
</table>
