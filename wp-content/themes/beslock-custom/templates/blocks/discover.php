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
          Discover <span>BESLOCK</span>
        </h2>

        <p class="discover__desc">
          We blend <strong>technology, precision, and design</strong> to redefine how people 
          experience security at home and in business. Our smart locks and access systems 
          are crafted with aluminum, powered by intelligent software, and designed to last.
        </p>

        <a href="/shop" class="discover__btn">Explore Products</a>
      </div>

	      <div class="discover__image">
	        <?php
	          $discover_png_path = get_stylesheet_directory() . '/assets/images/discover.png';
	          $discover_webp_path = get_stylesheet_directory() . '/assets/images/discover.webp';
	          $discover_png_url = get_stylesheet_directory_uri() . '/assets/images/discover.png';
	          $discover_webp_url = get_stylesheet_directory_uri() . '/assets/images/discover.webp';
	          if ( file_exists( $discover_png_path ) ) {
	            $discover_png_url .= '?v=' . filemtime( $discover_png_path );
	          }
	          if ( file_exists( $discover_webp_path ) ) {
	            $discover_webp_url .= '?v=' . filemtime( $discover_webp_path );
	          }
	        ?>
	        <picture>
	          <?php if ( file_exists( $discover_webp_path ) ) : ?>
	            <source srcset="<?php echo esc_url( $discover_webp_url ); ?>" type="image/webp">
	          <?php endif; ?>
	          <img
	            src="<?php echo esc_url( $discover_png_url ); ?>"
	            alt="Beslock Smart Locks"
	            width="1000"
	            height="1000"
	            loading="lazy"
	            decoding="async"
	          >
	        </picture>
	      </div>

    </div>
  </div>
</section>
