<?php
/**
 * BESLOCK email addresses.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.6.0
 */

defined( 'ABSPATH' ) || exit;

$address        = $order->get_formatted_billing_address();
$shipping       = $order->get_formatted_shipping_address();
$show_shipping  = ! wc_ship_to_billing_address_only() && $order->needs_shipping_address() && $shipping;
$billing_width  = $show_shipping ? '50%' : '100%';
$shipping_style = is_rtl() ? 'padding-right:12px;' : 'padding-left:12px;';
?>

<table id="addresses" cellspacing="0" cellpadding="0" style="width: 100%; vertical-align: top; padding:0;" border="0" role="presentation">
	<tr>
		<td class="font-family text-align-left beslock-address-cell" style="border:0; padding:0; padding-right:<?php echo is_rtl() ? '0' : '12px'; ?>;" valign="top" width="<?php echo esc_attr( $billing_width ); ?>">
			<div class="beslock-address-card">
				<strong class="address-title"><?php esc_html_e( 'Dirección de facturación', 'beslock-custom' ); ?></strong>
				<address class="address">
					<?php echo wp_kses_post( $address ? $address : esc_html__( 'N/A', 'woocommerce' ) ); ?>
					<?php if ( $order->get_billing_phone() ) : ?>
						<br><?php echo wc_make_phone_clickable( $order->get_billing_phone() ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
					<?php endif; ?>
					<?php if ( $order->get_billing_email() ) : ?>
						<br><?php echo esc_html( $order->get_billing_email() ); ?>
					<?php endif; ?>
					<?php
					do_action( 'woocommerce_email_customer_address_section', 'billing', $order, $sent_to_admin, false );
					?>
				</address>
			</div>
		</td>
		<?php if ( $show_shipping ) : ?>
			<td class="font-family text-align-left beslock-address-cell" style="border:0; padding:0; <?php echo esc_attr( $shipping_style ); ?>" valign="top" width="50%">
				<div class="beslock-address-card">
					<strong class="address-title"><?php esc_html_e( 'Dirección de envío', 'beslock-custom' ); ?></strong>
					<address class="address">
						<?php echo wp_kses_post( $shipping ); ?>
						<?php if ( $order->get_shipping_phone() ) : ?>
							<br><?php echo wc_make_phone_clickable( $order->get_shipping_phone() ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
						<?php endif; ?>
						<?php
						do_action( 'woocommerce_email_customer_address_section', 'shipping', $order, $sent_to_admin, false );
						?>
					</address>
				</div>
			</td>
		<?php endif; ?>
	</tr>
</table>
