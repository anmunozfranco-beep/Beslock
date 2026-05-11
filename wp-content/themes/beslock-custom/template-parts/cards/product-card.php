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

$card_image_ids = array();
$featured_image_id = $product->get_image_id();
if ( $featured_image_id ) {
  $card_image_ids[] = (int) $featured_image_id;
}

$gallery_image_ids = array_map( 'intval', $product->get_gallery_image_ids() );
foreach ( $gallery_image_ids as $gallery_image_id ) {
  if ( $gallery_image_id && ! in_array( $gallery_image_id, $card_image_ids, true ) ) {
    $card_image_ids[] = $gallery_image_id;
  }
}

$card_image_ids = array_values( array_filter( $card_image_ids ) );
$should_rotate_card_images = 'e-nova' === $product->get_slug() && count( $card_image_ids ) > 1;
?>

<article class="<?php echo esc_attr( implode( ' ', $card_classes ) ); ?>" data-js="product-card" data-product-id="<?php echo esc_attr( $product->get_id() ); ?>">
  <div class="<?php echo esc_attr( implode( ' ', $image_classes ) ); ?>">
    <?php if ( ! empty( $card_image_ids ) ) : ?>
      <?php if ( $should_rotate_card_images ) : ?>
        <div class="product-card__image-rotator" aria-hidden="true">
          <?php foreach ( $card_image_ids as $index => $image_id ) : ?>
            <?php
            $frame_classes = array(
              'product-card__frame',
              'product-frame',
            );

            if ( 0 === $index ) {
              $frame_classes[] = 'product-card__frame--active';
              $frame_classes[] = 'is-active';
              $frame_classes[] = 'visible';
            }
            ?>
            <?php echo wp_get_attachment_image( $image_id, 'medium', false, array( 'class' => implode( ' ', $frame_classes ) ) ); ?>
          <?php endforeach; ?>
        </div>
      <?php else : ?>
        <?php echo wp_get_attachment_image( $card_image_ids[0], 'medium' ); ?>
      <?php endif; ?>
    <?php else : ?>
      <?php echo $product->get_image( 'medium' ); ?>
    <?php endif; ?>

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