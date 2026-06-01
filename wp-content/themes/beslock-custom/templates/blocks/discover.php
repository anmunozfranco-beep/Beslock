<?php
/**
 * Block: Discover Section
 * Mobile-first – BEM – Clean containers
 */
?>

<section class="discover section section--lined section-reveal">
  <div class="u-container">
    <div class="discover__block">

      <div class="discover__text">
        <h2 class="discover__title">
          Descubre <span>Beslock®</span>
        </h2>

        <p class="discover__desc">
          Diseñamos accesos inteligentes que combinan <strong>seguridad, respaldo y control</strong>
          para proteger hogares, oficinas y exteriores con una experiencia simple, precisa y duradera.
        </p>
      </div>

	      <div class="discover__image">
	        <?php
	          $discover_image_dir = get_stylesheet_directory() . '/assets/images/discover/';
	          $discover_image_uri = get_stylesheet_directory_uri() . '/assets/images/discover/';
	          $discover_images = [
	            'discover-eshield-selected.webp',
	            'discover-etouch-selected.webp',
	            'discover-eflex-selected.webp',
	            'discover-selected.webp',
	          ];
	        ?>
	        <div class="discover__image-rotator" aria-label="<?php esc_attr_e( 'Galería visual de accesos inteligentes Beslock', 'beslock' ); ?>">
	          <?php foreach ( $discover_images as $index => $discover_image ) : ?>
	            <?php
	              $discover_image_path = $discover_image_dir . $discover_image;
	              if ( ! file_exists( $discover_image_path ) ) {
	                continue;
	              }
	              $discover_image_url = $discover_image_uri . $discover_image . '?v=' . filemtime( $discover_image_path );
	            ?>
	            <img
	              class="discover__image-frame"
	              src="<?php echo esc_url( $discover_image_url ); ?>"
	              alt="<?php esc_attr_e( 'Acceso inteligente Beslock en ambiente premium', 'beslock' ); ?>"
	              width="1000"
	              height="1000"
	              loading="<?php echo 0 === $index ? 'eager' : 'lazy'; ?>"
	              decoding="async"
	              style="--discover-frame-index: <?php echo esc_attr( (string) $index ); ?>;"
	            >
	          <?php endforeach; ?>
	        </div>
	      </div>

    </div>
  </div>
</section>
