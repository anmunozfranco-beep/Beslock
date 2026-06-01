<?php
/**
 * Cart Page
 *
 * This template can be overridden by copying it to yourtheme/woocommerce/cart/cart.php.
 *
 * HOWEVER, on occasion WooCommerce will need to update template files and you
 * (the theme developer) will need to copy the new files to your theme to
 * maintain compatibility. We try to do this as little as possible, but it does
 * happen. When this occurs the version of the template file will be bumped and
 * the readme will list any important changes.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates
 * @version 10.1.0
 */

defined( 'ABSPATH' ) || exit;

if ( ! function_exists( 'beslock_cart_get_product_thumbnail_html' ) ) {
    function beslock_cart_get_product_thumbnail_html( WC_Product $product ) {
        $alt = $product->get_name();
        $asset_relative_path = 'assets/images/products/' . sanitize_title( $product->get_slug() ) . '.webp';
        $asset_path = get_stylesheet_directory() . '/' . $asset_relative_path;

        if ( file_exists( $asset_path ) ) {
            return sprintf(
                '<img src="%1$s" alt="%2$s" loading="lazy" decoding="async" width="120" height="120" class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail beslock-cart-product__image">',
                esc_url( get_stylesheet_directory_uri() . '/' . $asset_relative_path . '?v=' . filemtime( $asset_path ) ),
                esc_attr( $alt )
            );
        }

        $image_id = $product->get_image_id();

        if ( $image_id ) {
            return wp_get_attachment_image(
                $image_id,
                'medium',
                false,
                array(
                    'alt'      => $alt,
                    'loading'  => 'lazy',
                    'decoding' => 'async',
                )
            );
        }

        return $product->get_image( 'medium' );
    }
}

if ( WC()->cart && WC()->cart->is_empty() ) {
    if ( isset( $_GET['beslock_empty_cart'] ) && function_exists( 'wc_clear_notices' ) ) { // phpcs:ignore WordPress.Security.NonceVerification.Recommended
        wc_clear_notices();
    }

    wc_get_template( 'cart/cart-empty.php' );
    return;
}

do_action( 'woocommerce_before_cart' ); ?>

<div class="beslock-cart beslock-cart--checkout">
    <div class="beslock-cart__container">
        <header class="beslock-cart__header">
            <h1 class="screen-reader-text"><?php esc_html_e( 'Carrito', 'beslock-custom' ); ?></h1>
            <ol class="beslock-cart-progress" aria-label="<?php esc_attr_e( 'Proceso de compra', 'beslock-custom' ); ?>">
                <li class="beslock-cart-progress__item is-active">
                    <span class="beslock-cart-progress__number">1</span>
                    <span class="beslock-cart-progress__label"><?php esc_html_e( 'Carrito', 'beslock-custom' ); ?></span>
                </li>
                <li class="beslock-cart-progress__item">
                    <span class="beslock-cart-progress__number">2</span>
                    <span class="beslock-cart-progress__label"><?php esc_html_e( 'Entrega', 'beslock-custom' ); ?></span>
                </li>
                <li class="beslock-cart-progress__item">
                    <span class="beslock-cart-progress__number">3</span>
                    <span class="beslock-cart-progress__label"><?php esc_html_e( 'Pago', 'beslock-custom' ); ?></span>
                </li>
            </ol>
        </header>

        <div class="beslock-cart__layout">
            <section class="beslock-cart__items" aria-labelledby="beslock-cart-items-title">
                <div class="beslock-cart__section-header">
                    <h2 id="beslock-cart-items-title" class="beslock-cart__section-title"><?php esc_html_e( 'Productos', 'beslock-custom' ); ?></h2>
                    <a class="beslock-cart__continue" href="<?php echo esc_url( wc_get_page_permalink( 'shop' ) ); ?>"><?php esc_html_e( 'Seguir comprando', 'beslock-custom' ); ?></a>
                </div>

                <form class="woocommerce-cart-form beslock-cart-form" action="<?php echo esc_url( wc_get_cart_url() ); ?>" method="post">
                    <?php do_action( 'woocommerce_before_cart_table' ); ?>

                    <table class="shop_table shop_table_responsive cart woocommerce-cart-form__contents beslock-cart-table" cellspacing="0">
                        <caption class="screen-reader-text"><?php esc_html_e( 'Productos en el carrito', 'beslock-custom' ); ?></caption>
                        <thead>
                            <tr>
                                <th class="product-remove"><span class="screen-reader-text"><?php esc_html_e( 'Remove item', 'woocommerce' ); ?></span></th>
                                <th class="product-thumbnail"><span class="screen-reader-text"><?php esc_html_e( 'Thumbnail image', 'woocommerce' ); ?></span></th>
                                <th scope="col" class="product-name"><?php esc_html_e( 'Product', 'woocommerce' ); ?></th>
                                <th scope="col" class="product-price"><?php esc_html_e( 'Price', 'woocommerce' ); ?></th>
                                <th scope="col" class="product-quantity"><?php esc_html_e( 'Quantity', 'woocommerce' ); ?></th>
                                <th scope="col" class="product-subtotal"><?php esc_html_e( 'Subtotal', 'woocommerce' ); ?></th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php do_action( 'woocommerce_before_cart_contents' ); ?>

                            <?php
                            foreach ( WC()->cart->get_cart() as $cart_item_key => $cart_item ) {
                                $_product   = apply_filters( 'woocommerce_cart_item_product', $cart_item['data'], $cart_item, $cart_item_key );
                                $product_id = apply_filters( 'woocommerce_cart_item_product_id', $cart_item['product_id'], $cart_item, $cart_item_key );
                                /**
                                 * Filter the product name.
                                 *
                                 * @since 2.1.0
                                 * @param string $product_name Name of the product in the cart.
                                 * @param array $cart_item The product in the cart.
                                 * @param string $cart_item_key Key for the product in the cart.
                                 */
                                $product_name = apply_filters( 'woocommerce_cart_item_name', $_product->get_name(), $cart_item, $cart_item_key );

                                if ( $_product && $_product->exists() && $cart_item['quantity'] > 0 && apply_filters( 'woocommerce_cart_item_visible', true, $cart_item, $cart_item_key ) ) {
                                    $product_permalink = apply_filters( 'woocommerce_cart_item_permalink', $_product->is_visible() ? $_product->get_permalink( $cart_item ) : '', $cart_item, $cart_item_key );
                                    ?>
                                    <tr class="woocommerce-cart-form__cart-item <?php echo esc_attr( apply_filters( 'woocommerce_cart_item_class', 'cart_item', $cart_item, $cart_item_key ) ); ?>">

                                        <td class="product-remove">
                                            <?php
                                                echo apply_filters( // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
                                                    'woocommerce_cart_item_remove_link',
                                                    sprintf(
                                                        '<a role="button" href="%s" class="remove" aria-label="%s" data-product_id="%s" data-product_sku="%s">&times;</a>',
                                                        esc_url( wc_get_cart_remove_url( $cart_item_key ) ),
                                                        /* translators: %s is the product name */
                                                        esc_attr( sprintf( __( 'Remove %s from cart', 'woocommerce' ), wp_strip_all_tags( $product_name ) ) ),
                                                        esc_attr( $product_id ),
                                                        esc_attr( $_product->get_sku() )
                                                    ),
                                                    $cart_item_key
                                                );
                                            ?>
                                        </td>

                                        <td class="product-thumbnail">
                                        <?php
                                        /**
                                         * Filter the product thumbnail displayed in the WooCommerce cart.
                                         *
                                         * This filter allows developers to customize the HTML output of the product
                                         * thumbnail. It passes the product image along with cart item data
                                         * for potential modifications before being displayed in the cart.
                                         *
                                         * @param string $thumbnail     The HTML for the product image.
                                         * @param array  $cart_item     The cart item data.
                                         * @param string $cart_item_key Unique key for the cart item.
                                         *
                                         * @since 2.1.0
                                         */
                                        $thumbnail = apply_filters( 'woocommerce_cart_item_thumbnail', beslock_cart_get_product_thumbnail_html( $_product ), $cart_item, $cart_item_key );

                                        if ( ! $product_permalink ) {
                                            echo $thumbnail; // PHPCS: XSS ok.
                                        } else {
                                            printf( '<a href="%s">%s</a>', esc_url( $product_permalink ), $thumbnail ); // PHPCS: XSS ok.
                                        }
                                        ?>
                                        </td>

                                        <td scope="row" role="rowheader" class="product-name" data-title="<?php esc_attr_e( 'Product', 'woocommerce' ); ?>">
                                            <div class="beslock-cart-product__copy">
                                            <?php
                                            if ( ! $product_permalink ) {
                                                echo wp_kses_post( $product_name . '&nbsp;' );
                                            } else {
                                                /**
                                                 * This filter is documented above.
                                                 *
                                                 * @since 2.1.0
                                                 */
                                                echo wp_kses_post( apply_filters( 'woocommerce_cart_item_name', sprintf( '<a href="%s">%s</a>', esc_url( $product_permalink ), $_product->get_name() ), $cart_item, $cart_item_key ) );
                                            }

                                            do_action( 'woocommerce_after_cart_item_name', $cart_item, $cart_item_key );

                                            // Meta data.
                                            echo wc_get_formatted_cart_item_data( $cart_item ); // PHPCS: XSS ok.

                                            // Backorder notification.
                                            if ( $_product->backorders_require_notification() && $_product->is_on_backorder( $cart_item['quantity'] ) ) {
                                                echo wp_kses_post( apply_filters( 'woocommerce_cart_item_backorder_notification', '<p class="backorder_notification">' . esc_html__( 'Available on backorder', 'woocommerce' ) . '</p>', $product_id ) );
                                            }
                                            ?>
                                            </div>
                                        </td>

                                        <td class="product-price" data-title="<?php esc_attr_e( 'Price', 'woocommerce' ); ?>">
                                            <?php
                                                echo apply_filters( 'woocommerce_cart_item_price', WC()->cart->get_product_price( $_product ), $cart_item, $cart_item_key ); // PHPCS: XSS ok.
                                            ?>
                                        </td>

                                        <td class="product-quantity" data-title="<?php esc_attr_e( 'Quantity', 'woocommerce' ); ?>">
                                        <?php
                                        if ( $_product->is_sold_individually() ) {
                                            $min_quantity = 1;
                                            $max_quantity = 1;
                                        } else {
                                            $min_quantity = 0;
                                            $max_quantity = $_product->get_max_purchase_quantity();
                                        }

                                        $product_quantity = woocommerce_quantity_input(
                                            array(
                                                'input_name'   => "cart[{$cart_item_key}][qty]",
                                                'input_value'  => $cart_item['quantity'],
                                                'max_value'    => $max_quantity,
                                                'min_value'    => $min_quantity,
                                                'product_name' => $product_name,
                                            ),
                                            $_product,
                                            false
                                        );

                                        echo apply_filters( 'woocommerce_cart_item_quantity', $product_quantity, $cart_item_key, $cart_item ); // PHPCS: XSS ok.
                                        ?>
                                        </td>

                                        <td class="product-subtotal" data-title="<?php esc_attr_e( 'Subtotal', 'woocommerce' ); ?>">
                                            <?php
                                                echo apply_filters( 'woocommerce_cart_item_subtotal', WC()->cart->get_product_subtotal( $_product, $cart_item['quantity'] ), $cart_item, $cart_item_key ); // PHPCS: XSS ok.
                                            ?>
                                        </td>
                                    </tr>
                                    <?php
                                }
                            }
                            ?>

                            <?php do_action( 'woocommerce_cart_contents' ); ?>

                            <tr>
                                <td colspan="6" class="actions">
                                    <div class="beslock-cart-actions">

                                    <?php if ( wc_coupons_enabled() ) { ?>
                                        <details class="coupon beslock-cart-coupon">
                                            <summary><?php esc_html_e( '¿Tienes un cupón?', 'beslock-custom' ); ?></summary>
                                            <div class="beslock-cart-coupon__fields">
                                                <label for="coupon_code" class="screen-reader-text"><?php esc_html_e( 'Coupon:', 'woocommerce' ); ?></label>
                                                <input type="text" name="coupon_code" class="input-text" id="coupon_code" value="" placeholder="<?php esc_attr_e( 'Código de cupón', 'beslock-custom' ); ?>" />
                                                <button type="submit" class="button<?php echo esc_attr( wc_wp_theme_get_element_class_name( 'button' ) ? ' ' . wc_wp_theme_get_element_class_name( 'button' ) : '' ); ?>" name="apply_coupon" value="<?php esc_attr_e( 'Apply coupon', 'woocommerce' ); ?>"><?php esc_html_e( 'Aplicar', 'beslock-custom' ); ?></button>
                                            </div>
                                            <?php do_action( 'woocommerce_cart_coupon' ); ?>
                                        </details>
                                    <?php } ?>

                                    <span class="beslock-cart__update-status" aria-live="polite"><?php esc_html_e( 'Carrito actualizado', 'beslock-custom' ); ?></span>
                                    <button type="submit" class="button beslock-cart__update<?php echo esc_attr( wc_wp_theme_get_element_class_name( 'button' ) ? ' ' . wc_wp_theme_get_element_class_name( 'button' ) : '' ); ?>" name="update_cart" value="<?php esc_attr_e( 'Update cart', 'woocommerce' ); ?>" disabled hidden><?php esc_html_e( 'Actualizar carrito', 'beslock-custom' ); ?></button>

                                    <?php do_action( 'woocommerce_cart_actions' ); ?>

                                    <?php wp_nonce_field( 'woocommerce-cart', 'woocommerce-cart-nonce' ); ?>
                                    </div>
                                </td>
                            </tr>

                            <?php do_action( 'woocommerce_after_cart_contents' ); ?>
                        </tbody>
                    </table>
                    <?php do_action( 'woocommerce_after_cart_table' ); ?>
                </form>
            </section>

            <?php do_action( 'woocommerce_before_cart_collaterals' ); ?>

            <aside class="beslock-cart__summary" aria-labelledby="beslock-cart-summary-title">
                <div class="cart-collaterals">
                    <?php
                        /**
                         * Cart collaterals hook.
                         *
                         * @hooked woocommerce_cross_sell_display
                         * @hooked woocommerce_cart_totals - 10
                         */
                        do_action( 'woocommerce_cart_collaterals' );
                    ?>
                </div>
            </aside>
        </div>
    </div>
</div>

<?php do_action( 'woocommerce_after_cart' ); ?>
