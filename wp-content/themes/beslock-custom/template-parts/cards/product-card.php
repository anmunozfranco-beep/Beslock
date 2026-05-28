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

if ( ! function_exists( 'beslock_product_card_attachment_has_file' ) ) {
  function beslock_product_card_attachment_has_file( $attachment_id ) {
    $attachment_id = intval( $attachment_id );

    if ( ! $attachment_id ) {
      return false;
    }

    $file_path = get_attached_file( $attachment_id );

    return is_string( $file_path ) && '' !== $file_path && file_exists( $file_path );
  }
}

if ( ! function_exists( 'beslock_product_card_find_slug_attachment_id' ) ) {
  function beslock_product_card_find_slug_attachment_id( $product_slug ) {
    $product_slug = sanitize_title( (string) $product_slug );

    if ( '' === $product_slug ) {
      return 0;
    }

    $attachments = get_posts(
      array(
        'post_type'      => 'attachment',
        'post_mime_type' => 'image',
        'post_status'    => 'inherit',
        'posts_per_page' => 30,
        's'              => $product_slug,
        'orderby'        => 'ID',
        'order'          => 'ASC',
      )
    );

    $fallback_id = 0;

    foreach ( $attachments as $attachment ) {
      $attachment_id = intval( $attachment->ID );

      if ( ! beslock_product_card_attachment_has_file( $attachment_id ) ) {
        continue;
      }

      $attached_file = (string) get_post_meta( $attachment_id, '_wp_attached_file', true );
      $filename = basename( $attached_file );

      if ( preg_match( '/^' . preg_quote( $product_slug, '/' ) . '[_-]?\.(webp|png|jpe?g)$/i', $filename ) ) {
        return $attachment_id;
      }

      $filename_slug = sanitize_title( pathinfo( $filename, PATHINFO_FILENAME ) );
      if ( 0 === $fallback_id && 0 === strpos( $filename_slug, $product_slug ) ) {
        $fallback_id = $attachment_id;
      }
    }

    return $fallback_id;
  }
}

if ( ! function_exists( 'beslock_product_card_get_image_html' ) ) {
  function beslock_product_card_get_image_html( WC_Product $product ) {
    $thumbnail_id = $product->get_image_id();
    $alt = $product->get_name();

    if ( beslock_product_card_attachment_has_file( $thumbnail_id ) ) {
      return $product->get_image( 'medium' );
    }

    $replacement_id = beslock_product_card_find_slug_attachment_id( $product->get_slug() );

    if ( $replacement_id ) {
      return wp_get_attachment_image(
        $replacement_id,
        'medium',
        false,
        array(
          'alt'     => $alt,
          'loading' => 'lazy',
        )
      );
    }

    $asset_relative_path = 'assets/images/products/' . sanitize_title( $product->get_slug() ) . '.webp';
    $asset_path = get_stylesheet_directory() . '/' . $asset_relative_path;

    if ( file_exists( $asset_path ) ) {
      return sprintf(
        '<img src="%1$s" alt="%2$s" loading="lazy" width="400" height="225" class="attachment-medium size-medium bes-product-card__fallback-image">',
        esc_url( get_stylesheet_directory_uri() . '/' . $asset_relative_path . '?v=' . filemtime( $asset_path ) ),
        esc_attr( $alt )
      );
    }

    return $product->get_image( 'medium' );
  }
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
    <?php echo beslock_product_card_get_image_html( $product ); ?>

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
