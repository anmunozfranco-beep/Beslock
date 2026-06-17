<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

$args = wp_parse_args(
  isset( $args ) && is_array( $args ) ? $args : array(),
  array(
    'product'          => null,
    'show_description' => null,
  )
);

global $product;

if ( $args['product'] instanceof WC_Product ) {
  $product = $args['product'];
}

$context = get_query_var('beslock_context', []);
$show_description = null !== $args['show_description']
  ? (bool) $args['show_description']
  : ( $context['show_description'] ?? false );

$card_classes = array(
  'product-card',
  'bes-product-card',
  'section-reveal',
);

if ( $show_description ) {
  $card_classes[] = 'product-card--with-description';
}
?>

<div class="<?php echo esc_attr( implode( ' ', $card_classes ) ); ?>">

  <div class="product-card__image">
    <?php echo $product->get_image( 'medium' ); ?>

    <?php
    // Non-blocking badge logic: compute $show_badge only if $product is valid.
    $show_badge = false;
    if ( isset( $product ) && is_a( $product, 'WC_Product' ) ) {
      $product_slug   = $product->get_slug();
      $badge_products = array( 'e-orbit', 'e-flex', 's-shield', 'e-prime' );
      $show_badge     = in_array( $product_slug, $badge_products, true );
    }

    if ( $show_badge ) :
      $badge_path = get_stylesheet_directory() . '/assets/images/instal.png';
      if ( file_exists( $badge_path ) ) : ?>
        <img
          class="product-card__badge bes-product-card__badge"
          src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/instal.png' ); ?>"
          alt="<?php echo esc_attr_x( 'Instalación incluida', 'badge alt', 'beslock' ); ?>"
          aria-hidden="true"
        >
      <?php endif; ?>
    <?php endif; ?>
  </div>

  <h3 class="product-card__title"><?php echo esc_html( $product->get_name() ); ?></h3>

  <p class="product-card__price"><?php echo $product->get_price_html(); ?></p>

  <?php if ( $show_description ) : ?>
    <p class="product-card__description">
      <?php echo wp_kses_post( $product->get_short_description() ); ?>
    </p>
  <?php endif; ?>

  <div class="product-card__actions bes-product-card__actions">

    <a href="<?php echo esc_url( get_permalink( $product->get_id() ) ); ?>" class="bes-product-card__button bes-product-card__button--primary">
      Ver Producto
    </a>

    <a href="?add-to-cart=<?php echo $product->get_id(); ?>" class="bes-product-card__button bes-product-card__button--cart" aria-label="Add to cart">
      <i class="bi bi-cart"></i>
    </a>

  </div>

</div>
