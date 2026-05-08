<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

$args = wp_parse_args(
  $args,
  array(
    'product'          => null,
    'show_description' => false,
    'context'          => array(),
  )
);

$product = $args['product'];

if ( ! $product instanceof WC_Product ) {
  return;
}

$show_description = (bool) $args['show_description'];
$card_classes = array(
  'product-card',
  'bes-product-card',
  'pc-card',
  'section-reveal',
);

if ( $show_description ) {
  $card_classes[] = 'product-card--with-description';
}

$image_classes = array(
  'product-card__image',
  'bes-product-card__image',
);

$content_classes = array(
  'product-card__content',
  'bes-product-card__content',
);

$title_classes = array(
  'product-card__title',
  'bes-product-card__title',
);

$price_classes = array(
  'product-card__price',
  'bes-product-card__price',
);

$actions_classes = array(
  'product-card__actions',
  'bes-product-card__actions',
  'pc-actions',
);

$primary_action_classes = array(
  'bes-product-card__button',
  'bes-product-card__button--primary',
  'pc-btn-main',
);

$cart_action_classes = array(
  'bes-product-card__button',
  'bes-product-card__button--cart',
  'pc-btn-cart',
);

$show_badge = function_exists( 'beslock_product_card_has_install_badge' )
  ? beslock_product_card_has_install_badge( $product )
  : false;

$badge_src = get_template_directory_uri() . '/assets/images/instal.png';
$badge_path = get_template_directory() . '/assets/images/instal.png';
$permalink = get_permalink( $product->get_id() );
$add_to_cart_url = add_query_arg( 'add-to-cart', $product->get_id(), home_url( '/' ) );
?>

<article class="<?php echo esc_attr( implode( ' ', $card_classes ) ); ?>" data-js="product-card" data-product-id="<?php echo esc_attr( $product->get_id() ); ?>">
  <div class="<?php echo esc_attr( implode( ' ', $image_classes ) ); ?>">
    <?php echo $product->get_image( 'medium' ); ?>

    <?php if ( $show_badge && file_exists( $badge_path ) ) : ?>
      <img
        class="product-card__badge bes-product-card__badge"
        src="<?php echo esc_url( $badge_src ); ?>"
        alt="<?php echo esc_attr_x( 'Instalación incluida', 'badge alt', 'beslock' ); ?>"
        aria-hidden="true"
      >
    <?php endif; ?>
  </div>

  <div class="<?php echo esc_attr( implode( ' ', $content_classes ) ); ?>">
    <h3 class="<?php echo esc_attr( implode( ' ', $title_classes ) ); ?>"><?php echo esc_html( $product->get_name() ); ?></h3>

    <p class="<?php echo esc_attr( implode( ' ', $price_classes ) ); ?>"><?php echo $product->get_price_html(); ?></p>

    <?php if ( $show_description ) : ?>
      <p class="product-card__description bes-product-card__description">
        <?php echo wp_kses_post( $product->get_short_description() ); ?>
      </p>
    <?php endif; ?>

    <div class="<?php echo esc_attr( implode( ' ', $actions_classes ) ); ?>">
      <a href="<?php echo esc_url( $permalink ); ?>" class="<?php echo esc_attr( implode( ' ', $primary_action_classes ) ); ?>">
        Ver Producto
      </a>

      <a
        href="<?php echo esc_url( $add_to_cart_url ); ?>"
        class="<?php echo esc_attr( implode( ' ', $cart_action_classes ) ); ?>"
        aria-label="<?php echo esc_attr( sprintf( __( 'Add %s to cart', 'beslock' ), $product->get_name() ) ); ?>"
        data-product-id="<?php echo esc_attr( $product->get_id() ); ?>"
        data-js="product-card-add-to-cart"
      >
        <i class="bi bi-cart" aria-hidden="true"></i>
      </a>
    </div>
  </div>
</article>