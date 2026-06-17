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
  function beslock_product_card_get_image_html( WC_Product $product, $image_attributes = array() ) {
    $thumbnail_id = $product->get_image_id();
    $alt = $product->get_name();
    $image_attributes = wp_parse_args(
      $image_attributes,
      array(
        'alt'     => $alt,
        'loading' => 'lazy',
      )
    );

    if ( beslock_product_card_attachment_has_file( $thumbnail_id ) ) {
      return $product->get_image( 'medium', $image_attributes );
    }

    $replacement_id = beslock_product_card_find_slug_attachment_id( $product->get_slug() );

    if ( $replacement_id ) {
      return wp_get_attachment_image(
        $replacement_id,
        'medium',
        false,
        $image_attributes
      );
    }

    $asset_relative_path = 'assets/images/products/' . sanitize_title( $product->get_slug() ) . '.webp';
    $asset_path = get_stylesheet_directory() . '/' . $asset_relative_path;

    if ( file_exists( $asset_path ) ) {
      return sprintf(
        '<img src="%1$s" alt="%2$s" loading="%3$s" width="400" height="225" class="attachment-medium size-medium bes-product-card__fallback-image" data-js="%4$s">',
        esc_url( get_stylesheet_directory_uri() . '/' . $asset_relative_path . '?v=' . filemtime( $asset_path ) ),
        esc_attr( $image_attributes['alt'] ?? $alt ),
        esc_attr( $image_attributes['loading'] ?? 'lazy' ),
        esc_attr( $image_attributes['data-js'] ?? '' )
      );
    }

    return $product->get_image( 'medium', $image_attributes );
  }
}

if ( ! function_exists( 'beslock_product_card_normalize_variation_attribute_key' ) ) {
  function beslock_product_card_normalize_variation_attribute_key( $key ) {
    $key = preg_replace( '/^attribute_/', '', (string) $key );
    $key = preg_replace( '/^pa_/', '', $key );
    return sanitize_title( $key );
  }
}

if ( ! function_exists( 'beslock_product_card_get_named_variation_attribute' ) ) {
  function beslock_product_card_get_named_variation_attribute( $attributes, $wanted_keys ) {
    $wanted_keys = array_map( 'sanitize_title', (array) $wanted_keys );

    foreach ( (array) $attributes as $key => $value ) {
      $normalized_key = beslock_product_card_normalize_variation_attribute_key( $key );
      if ( in_array( $normalized_key, $wanted_keys, true ) && '' !== trim( (string) $value ) ) {
        return trim( (string) $value );
      }
    }

    return '';
  }
}

if ( ! function_exists( 'beslock_product_card_unique_option_push' ) ) {
  function beslock_product_card_unique_option_push( &$options, $label ) {
    $label = trim( (string) $label );
    if ( '' === $label ) {
      return;
    }

    $key = sanitize_title( $label );
    if ( '' !== $key && empty( $options[ $key ] ) ) {
      $options[ $key ] = array(
        'key'   => $key,
        'label' => $label,
      );
    }
  }
}

if ( ! function_exists( 'beslock_product_card_get_variation_payload' ) ) {
  function beslock_product_card_get_variation_payload( WC_Product $product ) {
    if ( ! $product->is_type( 'variable' ) || ! method_exists( $product, 'get_available_variations' ) ) {
      return array();
    }

    $available_variations = $product->get_available_variations();
    if ( empty( $available_variations ) || ! is_array( $available_variations ) ) {
      return array();
    }

    $colors = array();
    $geometries = array();
    $variations = array();
    $defaults = method_exists( $product, 'get_default_attributes' ) ? (array) $product->get_default_attributes() : array();
    $default_color = beslock_product_card_get_named_variation_attribute( $defaults, array( 'color' ) );
    $default_geometry = beslock_product_card_get_named_variation_attribute( $defaults, array( 'geometria', 'geometry' ) );
    $default_variation_id = 0;

    foreach ( $available_variations as $variation ) {
      $variation_id = absint( $variation['variation_id'] ?? 0 );
      $attributes = (array) ( $variation['attributes'] ?? array() );
      $color = beslock_product_card_get_named_variation_attribute( $attributes, array( 'color' ) );
      $geometry = beslock_product_card_get_named_variation_attribute( $attributes, array( 'geometria', 'geometry' ) );

      if ( ! $variation_id || '' === $color && '' === $geometry ) {
        continue;
      }

      $variation_product = function_exists( 'wc_get_product' ) ? wc_get_product( $variation_id ) : null;
      $price_html = $variation_product instanceof WC_Product ? $variation_product->get_price_html() : (string) ( $variation['price_html'] ?? '' );
      $image = (array) ( $variation['image'] ?? array() );
      $variation_attributes = array();

      foreach ( $attributes as $attribute_key => $attribute_value ) {
        if ( '' === trim( (string) $attribute_value ) ) {
          continue;
        }
        $variation_attributes[ $attribute_key ] = $attribute_value;
      }

      beslock_product_card_unique_option_push( $colors, $color );
      beslock_product_card_unique_option_push( $geometries, $geometry );

      $variation_payload = array(
        'id'          => $variation_id,
        'color'       => $color,
        'colorKey'    => sanitize_title( $color ),
        'geometry'    => $geometry,
        'geometryKey' => sanitize_title( $geometry ),
        'priceHtml'   => $price_html,
        'attributes'  => $variation_attributes,
        'isPurchasable' => ! empty( $variation['is_purchasable'] ),
        'isInStock'     => ! empty( $variation['is_in_stock'] ),
        'image'       => array(
          'id'     => absint( $variation['image_id'] ?? 0 ),
          'src'    => isset( $image['src'] ) ? esc_url_raw( $image['src'] ) : '',
          'srcset' => isset( $image['srcset'] ) ? (string) $image['srcset'] : '',
          'sizes'  => isset( $image['sizes'] ) ? (string) $image['sizes'] : '',
          'alt'    => isset( $image['alt'] ) && '' !== $image['alt'] ? wp_strip_all_tags( $image['alt'] ) : $product->get_name(),
        ),
      );

      if (
        ! $default_variation_id &&
        ( '' === $default_color || $default_color === $color ) &&
        ( '' === $default_geometry || $default_geometry === $geometry )
      ) {
        $default_variation_id = $variation_id;
      }

      $variations[] = $variation_payload;
    }

    if ( empty( $variations ) ) {
      return array();
    }

    if ( ! $default_variation_id ) {
      $default_variation_id = absint( $variations[0]['id'] );
    }

    return array(
      'productId'          => absint( $product->get_id() ),
      'defaultVariationId' => $default_variation_id,
      'colors'             => array_values( $colors ),
      'geometries'         => array_values( $geometries ),
      'variations'         => $variations,
    );
  }
}

$show_description = (bool) $args['show_description'];
$card_classes = array(
  'product-card',
  'bes-product-card',
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
);

$primary_action_classes = array(
  'bes-product-card__button',
  'bes-product-card__button--primary',
);

$cart_action_classes = array(
  'bes-product-card__button',
  'bes-product-card__button--cart',
);

$variation_payload = beslock_product_card_get_variation_payload( $product );
$has_variation_controls = ! empty( $variation_payload['variations'] );
$selected_variation = array();

if ( $has_variation_controls ) {
  foreach ( $variation_payload['variations'] as $variation_payload_item ) {
    if ( absint( $variation_payload_item['id'] ?? 0 ) === absint( $variation_payload['defaultVariationId'] ?? 0 ) ) {
      $selected_variation = $variation_payload_item;
      break;
    }
  }

  if ( empty( $selected_variation ) ) {
    $selected_variation = $variation_payload['variations'][0];
  }

  $card_classes[] = 'bes-product-card--variable';
}

$show_badge = function_exists( 'beslock_product_card_has_install_badge' )
  ? beslock_product_card_has_install_badge( $product )
  : false;

$badge_src = get_stylesheet_directory_uri() . '/assets/images/instal.png';
$badge_path = get_stylesheet_directory() . '/assets/images/instal.png';
$permalink = get_permalink( $product->get_id() );
$selected_variation_attributes = (array) ( $selected_variation['attributes'] ?? array() );
$selected_variation_id = absint( $selected_variation['id'] ?? 0 );
$selected_price_html = $has_variation_controls && ! empty( $selected_variation['priceHtml'] )
  ? $selected_variation['priceHtml']
  : $product->get_price_html();
$add_to_cart_url = $product->add_to_cart_url();

if ( $has_variation_controls && $selected_variation_id ) {
  $add_to_cart_url = add_query_arg(
    array_merge(
      array(
        'add-to-cart'  => absint( $product->get_id() ),
        'variation_id' => $selected_variation_id,
        'quantity'     => 1,
      ),
      $selected_variation_attributes
    ),
    $permalink
  );
}

$product_sku = $product->get_sku();
$image_attributes = array(
  'data-js' => 'product-card-image',
  'alt'     => $product->get_name(),
  'loading' => 'lazy',
);
$selected_variation_image_id = absint( $selected_variation['image']['id'] ?? 0 );
$card_image_html = $selected_variation_image_id
  ? wp_get_attachment_image( $selected_variation_image_id, 'medium', false, $image_attributes )
  : beslock_product_card_get_image_html( $product, $image_attributes );

if ( ! $card_image_html ) {
  $card_image_html = beslock_product_card_get_image_html( $product, $image_attributes );
}
?>

<article class="<?php echo esc_attr( implode( ' ', $card_classes ) ); ?>" data-js="product-card" data-product-id="<?php echo esc_attr( $product->get_id() ); ?>">
  <div class="<?php echo esc_attr( implode( ' ', $image_classes ) ); ?>">
    <?php echo $card_image_html; ?>

    <?php if ( $show_badge && file_exists( $badge_path ) ) : ?>
      <img
        class="product-card__badge bes-product-card__badge"
        src="<?php echo esc_url( $badge_src ); ?>"
        alt="<?php echo esc_attr_x( 'Instalación incluida', 'badge alt', 'beslock' ); ?>"
        aria-hidden="true"
      >
    <?php endif; ?>

    <?php if ( $has_variation_controls ) : ?>
      <div class="bes-product-card__variation-controls" data-js="product-card-variation-controls">
        <?php if ( count( $variation_payload['colors'] ) > 1 ) : ?>
          <div class="bes-product-card__variation-colors" role="radiogroup" aria-label="<?php echo esc_attr__( 'Color', 'beslock' ); ?>">
            <?php foreach ( $variation_payload['colors'] as $color_option ) : ?>
              <?php
              $color_key = sanitize_title( $color_option['key'] ?? $color_option['label'] );
              $is_selected_color = $color_option['label'] === ( $selected_variation['color'] ?? '' );
              ?>
              <button
                type="button"
                class="bes-product-card__variation-color"
                data-js="product-card-color-option"
                data-variation-color="<?php echo esc_attr( $color_option['label'] ); ?>"
                data-variation-color-key="<?php echo esc_attr( $color_key ); ?>"
                aria-pressed="<?php echo $is_selected_color ? 'true' : 'false'; ?>"
              >
                <span class="bes-product-card__variation-swatch bes-product-card__variation-swatch--<?php echo esc_attr( $color_key ); ?>" aria-hidden="true"></span>
                <span class="bes-product-card__variation-color-label"><?php echo esc_html( $color_option['label'] ); ?></span>
              </button>
            <?php endforeach; ?>
          </div>
        <?php endif; ?>

        <?php if ( count( $variation_payload['geometries'] ) > 1 ) : ?>
          <div class="bes-product-card__variation-geometry" aria-label="<?php echo esc_attr__( 'Geometría', 'beslock' ); ?>">
            <button type="button" class="bes-product-card__variation-arrow bes-product-card__variation-arrow--prev" data-js="product-card-geometry-prev" aria-label="<?php echo esc_attr__( 'Geometría anterior', 'beslock' ); ?>">
              <i class="bi bi-chevron-left" aria-hidden="true"></i>
            </button>
            <span class="bes-product-card__variation-geometry-label" data-js="product-card-geometry-label"><?php echo esc_html( $selected_variation['geometry'] ?? '' ); ?></span>
            <button type="button" class="bes-product-card__variation-arrow bes-product-card__variation-arrow--next" data-js="product-card-geometry-next" aria-label="<?php echo esc_attr__( 'Geometría siguiente', 'beslock' ); ?>">
              <i class="bi bi-chevron-right" aria-hidden="true"></i>
            </button>
          </div>
        <?php endif; ?>
      </div>
    <?php endif; ?>
  </div>

  <div class="<?php echo esc_attr( implode( ' ', $content_classes ) ); ?>">
    <h3 class="<?php echo esc_attr( implode( ' ', $title_classes ) ); ?>"><?php echo esc_html( $product->get_name() ); ?></h3>

    <p class="<?php echo esc_attr( implode( ' ', $price_classes ) ); ?>" data-js="product-card-price"><?php echo $selected_price_html; ?></p>

    <?php if ( $show_description ) : ?>
      <p class="product-card__description bes-product-card__description">
        <?php echo wp_kses_post( $product->get_short_description() ); ?>
      </p>
    <?php endif; ?>

    <?php if ( $has_variation_controls ) : ?>
      <script type="application/json" data-js="product-card-variations"><?php echo wp_json_encode( $variation_payload, JSON_HEX_TAG | JSON_HEX_APOS | JSON_HEX_AMP | JSON_HEX_QUOT ); ?></script>
    <?php endif; ?>

    <div class="<?php echo esc_attr( implode( ' ', $actions_classes ) ); ?>">
      <a href="<?php echo esc_url( $permalink ); ?>" class="<?php echo esc_attr( implode( ' ', $primary_action_classes ) ); ?>">
        Ver Producto
      </a>

      <a
        href="<?php echo esc_url( $add_to_cart_url ); ?>"
        class="<?php echo esc_attr( implode( ' ', $cart_action_classes ) ); ?>"
        aria-label="<?php echo esc_attr( sprintf( __( 'Add %s to cart', 'beslock' ), $product->get_name() ) ); ?>"
        data-product_id="<?php echo esc_attr( $product->get_id() ); ?>"
        data-product_sku="<?php echo esc_attr( $product_sku ); ?>"
        data-quantity="1"
        data-product-id="<?php echo esc_attr( $product->get_id() ); ?>"
        data-product-name="<?php echo esc_attr( $product->get_name() ); ?>"
        <?php if ( $has_variation_controls && $selected_variation_id ) : ?>
          data-variation_id="<?php echo esc_attr( $selected_variation_id ); ?>"
          data-variation_attributes="<?php echo esc_attr( wp_json_encode( $selected_variation_attributes ) ); ?>"
        <?php endif; ?>
        data-success_message="<?php echo esc_attr( sprintf( __( '"%s" se ha añadido a tu carrito.', 'beslock-custom' ), $product->get_name() ) ); ?>"
        data-js="product-card-add-to-cart"
      >
        <i class="bi bi-cart" aria-hidden="true"></i>
      </a>
    </div>
  </div>
</article>
