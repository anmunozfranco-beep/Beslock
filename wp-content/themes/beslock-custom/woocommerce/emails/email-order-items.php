<?php
/**
 * BESLOCK email order items.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.7.0
 */

defined( 'ABSPATH' ) || exit;

$price_text_align = is_rtl() ? 'left' : 'right';

foreach ( $items as $item_id => $item ) :
	$product       = $item->get_product();
	$sku           = '';
	$purchase_note = '';
	$image         = '';

	if ( ! apply_filters( 'woocommerce_order_item_visible', true, $item ) ) {
		continue;
	}

	if ( is_object( $product ) ) {
		$sku           = $product->get_sku();
		$purchase_note = $product->get_purchase_note();
		$image         = $product->get_image( $image_size );
	}
	?>
	<tr class="<?php echo esc_attr( apply_filters( 'woocommerce_order_item_class', 'order_item', $item, $order ) ); ?>">
		<td class="td font-family text-align-left beslock-product-cell" style="vertical-align:top; word-wrap:break-word;">
			<table class="order-item-data beslock-product-wrap" role="presentation">
				<tr>
					<?php if ( $show_image && $image ) : ?>
						<td class="beslock-product-thumb">
							<?php
							echo wp_kses_post( apply_filters( 'woocommerce_order_item_thumbnail', $image, $item ) );
							?>
						</td>
					<?php endif; ?>
					<td>
						<?php
						$order_item_name = apply_filters( 'woocommerce_order_item_name', $item->get_name(), $item, false );
						echo '<div class="beslock-product-title">' . wp_kses_post( $order_item_name ) . '</div>';

						if ( $show_sku && $sku ) {
							echo '<div class="email-order-item-meta">#' . esc_html( $sku ) . '</div>';
						}

						do_action( 'woocommerce_order_item_meta_start', $item_id, $item, $order, $plain_text );

						$item_meta = wc_display_item_meta(
							$item,
							array(
								'before'       => '',
								'after'        => '',
								'separator'    => '<br>',
								'echo'         => false,
								'label_before' => '<span>',
								'label_after'  => ':</span> ',
							)
						);

						if ( $item_meta ) {
							echo '<div class="email-order-item-meta">';
							echo wp_kses(
								$item_meta,
								array(
									'br'   => array(),
									'span' => array(),
									'a'    => array(
										'href'   => true,
										'target' => true,
										'rel'    => true,
										'title'  => true,
									),
								)
							);
							echo '</div>';
						}

						do_action( 'woocommerce_order_item_meta_end', $item_id, $item, $order, $plain_text );
						?>
					</td>
				</tr>
			</table>
		</td>
		<td class="td font-family text-align-<?php echo esc_attr( $price_text_align ); ?> beslock-qty-cell" style="vertical-align:top;">
			<?php
			$qty          = $item->get_quantity();
			$refunded_qty = $order->get_qty_refunded_for_item( $item_id );

			if ( $refunded_qty ) {
				$qty_display = '<del>' . esc_html( $qty ) . '</del> <ins>' . esc_html( $qty - ( $refunded_qty * -1 ) ) . '</ins>';
			} else {
				$qty_display = esc_html( $qty );
			}

			echo '&times; ' . wp_kses_post( apply_filters( 'woocommerce_email_order_item_quantity', $qty_display, $item ) );
			?>
		</td>
		<td class="td font-family text-align-<?php echo esc_attr( $price_text_align ); ?> beslock-price-cell" style="vertical-align:top;">
			<?php echo wp_kses_post( $order->get_formatted_line_subtotal( $item ) ); ?>
		</td>
	</tr>
	<?php if ( $show_purchase_note && $purchase_note ) : ?>
		<tr>
			<td colspan="3" class="font-family text-align-left" style="vertical-align:middle;">
				<?php echo wp_kses_post( wpautop( do_shortcode( $purchase_note ) ) ); ?>
			</td>
		</tr>
	<?php endif; ?>
<?php endforeach; ?>
