<?php
defined('ABSPATH') || exit;
get_header();
?>

<main class="product-page">

  <?php while ( have_posts() ) : the_post(); ?>
    <?php
    $product = function_exists( 'wc_get_product' ) ? wc_get_product( get_the_ID() ) : null;
    $product_features = function_exists( 'beslock_get_product_features_list' ) ? beslock_get_product_features_list( $product ) : array();
    $product_reviews = function_exists( 'beslock_get_product_reviews_list' ) ? beslock_get_product_reviews_list( $product ) : array();
    $product_review_rating_counts = array_fill( 1, 5, 0 );
    $product_review_rating_total = 0;
    $product_review_rating_count = 0;
    $product_navigation = array();
    $features_tab_id = 'product-tab-features-' . get_the_ID();
    $reviews_tab_id = 'product-tab-reviews-' . get_the_ID();
    $features_panel_id = 'product-panel-features-' . get_the_ID();
    $reviews_panel_id = 'product-panel-reviews-' . get_the_ID();
    $product_navigation_item_is_public = static function( $product_id ) {
      if ( ! function_exists( 'wc_get_product' ) ) {
        return true;
      }

      $navigation_product = wc_get_product( $product_id );

      if ( ! $navigation_product || ! is_a( $navigation_product, 'WC_Product' ) ) {
        return false;
      }

      if ( 'hidden' === $navigation_product->get_catalog_visibility() ) {
        return false;
      }

      if ( function_exists( 'beslock_is_installation_service_product' ) && beslock_is_installation_service_product( $navigation_product ) ) {
        return false;
      }

      $navigation_product_sku = (string) $navigation_product->get_sku();

      return 0 !== strpos( $navigation_product_sku, 'BESLOCK-INST-' );
    };

    foreach ( $product_reviews as $product_review ) {
      $product_review_rating = isset( $product_review['rating'] ) ? min( 5, max( 0, intval( $product_review['rating'] ) ) ) : 0;
      if ( $product_review_rating < 1 ) {
        continue;
      }

      $product_review_rating_counts[ $product_review_rating ]++;
      $product_review_rating_total += $product_review_rating;
      $product_review_rating_count++;
    }

    $product_review_average = $product_review_rating_count > 0 ? $product_review_rating_total / $product_review_rating_count : 0;
    $product_review_average_display = $product_review_rating_count > 0 ? number_format( $product_review_average, 1, '.', '' ) : '0.0';

    $product_navigation_ids = get_posts( array(
      'post_type'      => 'product',
      'post_status'    => 'publish',
      'posts_per_page' => -1,
      'fields'         => 'ids',
      'orderby'        => 'date',
      'order'          => 'DESC',
    ) );

    if ( is_array( $product_navigation_ids ) ) {
      $product_navigation_ids = array_values( array_filter( array_map( 'intval', $product_navigation_ids ), $product_navigation_item_is_public ) );
      $current_product_index = array_search( get_the_ID(), $product_navigation_ids, true );

      if ( false !== $current_product_index && count( $product_navigation_ids ) > 1 ) {
        $last_product_index = count( $product_navigation_ids ) - 1;
        $previous_product_id = 0 === $current_product_index ? $product_navigation_ids[ $last_product_index ] : $product_navigation_ids[ $current_product_index - 1 ];
        $next_product_id = $last_product_index === $current_product_index ? $product_navigation_ids[ 0 ] : $product_navigation_ids[ $current_product_index + 1 ];

        if ( $previous_product_id && $previous_product_id !== get_the_ID() ) {
          $product_navigation['previous'] = array(
            'url'   => get_permalink( $previous_product_id ),
            'label' => wp_strip_all_tags( get_the_title( $previous_product_id ) ),
          );
        }

        if ( $next_product_id && $next_product_id !== get_the_ID() ) {
          $product_navigation['next'] = array(
            'url'   => get_permalink( $next_product_id ),
            'label' => wp_strip_all_tags( get_the_title( $next_product_id ) ),
          );
        }
      }
    }
    ?>

    <?php if ( ! empty( $product_navigation['previous'] ) || ! empty( $product_navigation['next'] ) ) : ?>
      <nav class="product-page__pager" aria-label="<?php echo esc_attr__( 'Navegación entre productos', 'beslock' ); ?>">
        <?php if ( ! empty( $product_navigation['previous'] ) ) : ?>
          <a
            class="product-page__pager-link product-page__pager-link--prev"
            href="<?php echo esc_url( $product_navigation['previous']['url'] ); ?>"
            rel="prev"
            aria-label="<?php echo esc_attr( sprintf( __( 'Ir al producto anterior: %s', 'beslock' ), $product_navigation['previous']['label'] ) ); ?>"
          >
            <span class="product-page__pager-arrow product-page__pager-arrow--prev" aria-hidden="true"></span>
            <span class="product-page__pager-meta">
              <span class="product-page__pager-title"><?php echo esc_html( $product_navigation['previous']['label'] ); ?></span>
            </span>
          </a>
        <?php endif; ?>

        <?php if ( ! empty( $product_navigation['next'] ) ) : ?>
          <a
            class="product-page__pager-link product-page__pager-link--next"
            href="<?php echo esc_url( $product_navigation['next']['url'] ); ?>"
            rel="next"
            aria-label="<?php echo esc_attr( sprintf( __( 'Ir al siguiente producto: %s', 'beslock' ), $product_navigation['next']['label'] ) ); ?>"
          >
            <span class="product-page__pager-meta">
              <span class="product-page__pager-title"><?php echo esc_html( $product_navigation['next']['label'] ); ?></span>
            </span>
            <span class="product-page__pager-arrow product-page__pager-arrow--next" aria-hidden="true"></span>
          </a>
        <?php endif; ?>
      </nav>
    <?php endif; ?>

    <div class="product-page__hero">

      <div class="product-page__media">
        <div class="product-page__gallery">
          <div class="product-page__gallery-wrapper" aria-hidden="false">
            <?php if ( function_exists( 'woocommerce_show_product_images' ) ) { woocommerce_show_product_images(); } ?>
          </div>
        </div>
      </div>

      <div class="product-page__info">
        <?php if ( function_exists( 'woocommerce_template_single_title' ) ) { woocommerce_template_single_title(); } ?>
        <?php if ( function_exists( 'woocommerce_template_single_price' ) ) { woocommerce_template_single_price(); } ?>
        <?php if ( function_exists( 'woocommerce_template_single_excerpt' ) ) { woocommerce_template_single_excerpt(); } ?>
        <?php if ( function_exists( 'woocommerce_template_single_add_to_cart' ) ) { woocommerce_template_single_add_to_cart(); } ?>
      </div>

    </div>

    <div class="product-page__details">
      <div class="product-tabs">

        <div class="product-tabs__nav" role="tablist" aria-label="<?php echo esc_attr__( 'Información del producto', 'beslock' ); ?>">
          <button
            id="<?php echo esc_attr( $features_tab_id ); ?>"
            class="product-tabs__tab is-active"
            type="button"
            role="tab"
            aria-selected="true"
            aria-controls="<?php echo esc_attr( $features_panel_id ); ?>"
          ><?php echo esc_html__( 'Características', 'beslock' ); ?></button>
          <button
            id="<?php echo esc_attr( $reviews_tab_id ); ?>"
            class="product-tabs__tab"
            type="button"
            role="tab"
            aria-selected="false"
            aria-controls="<?php echo esc_attr( $reviews_panel_id ); ?>"
            tabindex="-1"
          ><?php echo esc_html__( 'Reseñas', 'beslock' ); ?></button>
        </div>

        <div class="product-tabs__content">

          <div
            id="<?php echo esc_attr( $features_panel_id ); ?>"
            class="product-tabs__panel is-active"
            role="tabpanel"
            aria-labelledby="<?php echo esc_attr( $features_tab_id ); ?>"
            tabindex="0"
          >
            <?php if ( ! empty( $product_features ) ) : ?>
              <dl class="product-features-list" aria-label="<?php printf( esc_attr__( 'Resumen de características de %s', 'beslock' ), get_the_title() ); ?>">
                <?php foreach ( $product_features as $feature ) : ?>
                  <div class="product-features-list__item">
                    <dt><?php echo esc_html( $feature['label'] ?? '' ); ?></dt>
                    <dd><?php echo esc_html( $feature['value'] ?? '' ); ?></dd>
                  </div>
                <?php endforeach; ?>
              </dl>
            <?php else : ?>
              <p><?php echo esc_html__( 'Pronto compartiremos las características de este producto.', 'beslock' ); ?></p>
            <?php endif; ?>
          </div>

          <div
            id="<?php echo esc_attr( $reviews_panel_id ); ?>"
            class="product-tabs__panel"
            role="tabpanel"
            aria-labelledby="<?php echo esc_attr( $reviews_tab_id ); ?>"
            hidden
          >
            <?php if ( ! empty( $product_reviews ) ) : ?>
              <div
                class="product-reviews-summary"
                aria-label="<?php printf( esc_attr__( 'Calificación promedio: %1$s de 5 basada en %2$d reseñas.', 'beslock' ), esc_attr( $product_review_average_display ), absint( $product_review_rating_count ) ); ?>"
              >
                <div class="product-reviews-summary__score">
                  <strong><?php echo esc_html( $product_review_average_display ); ?></strong>
                  <div class="product-reviews-summary__stars" aria-hidden="true">
                    <?php for ( $summary_star = 1; $summary_star <= 5; $summary_star++ ) : ?>
                      <span class="<?php echo $summary_star <= round( $product_review_average ) ? 'is-filled' : ''; ?>">&#9733;</span>
                    <?php endfor; ?>
                  </div>
                  <span><?php printf( esc_html__( '(%d)', 'beslock' ), absint( $product_review_rating_count ) ); ?></span>
                </div>

                <div class="product-reviews-summary__bars">
                  <?php for ( $summary_rating = 5; $summary_rating >= 1; $summary_rating-- ) : ?>
                    <?php
                    $summary_rating_count = $product_review_rating_counts[ $summary_rating ] ?? 0;
                    $summary_rating_percent = $product_review_rating_count > 0 ? ( $summary_rating_count / $product_review_rating_count ) * 100 : 0;
                    ?>
                    <div
                      class="product-reviews-summary__bar"
                      aria-label="<?php printf( esc_attr__( '%1$d estrellas: %2$d reseñas', 'beslock' ), absint( $summary_rating ), absint( $summary_rating_count ) ); ?>"
                    >
                      <span style="width: <?php echo esc_attr( round( $summary_rating_percent, 2 ) ); ?>%;"></span>
                    </div>
                  <?php endfor; ?>
                </div>

                <p><?php echo esc_html__( 'No se verificaron las opiniones', 'beslock' ); ?></p>
              </div>

              <ul class="product-reviews-list">
                <?php foreach ( $product_reviews as $review ) : ?>
                  <?php $review_rating = isset( $review['rating'] ) ? intval( $review['rating'] ) : 0; ?>
                  <li class="product-review-card">
                    <div class="product-review-card__header">
                      <?php if ( $review_rating > 0 ) : ?>
                        <div class="product-review-card__rating" aria-label="<?php printf( esc_attr__( 'Calificación: %d de 5', 'beslock' ), $review_rating ); ?>">
                          <?php for ( $star_index = 1; $star_index <= 5; $star_index++ ) : ?>
                            <span class="product-review-card__star <?php echo $star_index <= $review_rating ? 'is-filled' : ''; ?>" aria-hidden="true">&#9733;</span>
                          <?php endfor; ?>
                        </div>
                      <?php endif; ?>

                      <div class="product-review-card__meta">
                        <strong class="product-review-card__author"><?php echo esc_html( $review['author'] ); ?></strong>
                        <?php if ( ! empty( $review['date'] ) ) : ?>
                          <time class="product-review-card__date" datetime="<?php echo esc_attr( $review['date_iso'] ?? '' ); ?>"><?php echo esc_html( $review['date'] ); ?></time>
                        <?php endif; ?>
                      </div>
                    </div>

                    <p class="product-review-card__body"><?php echo esc_html( $review['text'] ); ?></p>
                  </li>
                <?php endforeach; ?>
              </ul>
            <?php else : ?>
              <div class="product-reviews-placeholder">
                <p><?php echo esc_html__( 'Este producto todavía no tiene reseñas publicadas.', 'beslock' ); ?></p>
              </div>
            <?php endif; ?>
          </div>

        </div>

      </div>

      <?php if ( function_exists( 'beslock_render_product_interactions_block' ) ) : ?>
        <?php beslock_render_product_interactions_block( $product ); ?>
      <?php endif; ?>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function(){
      document.querySelectorAll('.product-tabs').forEach((tabRoot) => {
        const tabs = Array.from(tabRoot.querySelectorAll('.product-tabs__tab'));
        const panels = Array.from(tabRoot.querySelectorAll('.product-tabs__panel'));
        if(!tabs.length || !panels.length) return;

        const activateTab = (index) => {
          tabs.forEach((tab, tabIndex) => {
            const isActive = tabIndex === index;
            tab.classList.toggle('is-active', isActive);
            tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
            tab.setAttribute('tabindex', isActive ? '0' : '-1');
          });

          panels.forEach((panel, panelIndex) => {
            const isActive = panelIndex === index;
            panel.classList.toggle('is-active', isActive);
            if (isActive) {
              panel.removeAttribute('hidden');
              panel.setAttribute('tabindex', '0');
            } else {
              panel.setAttribute('hidden', 'hidden');
              panel.removeAttribute('tabindex');
            }
          });
        };

        tabs.forEach((tab, index) => {
          tab.addEventListener('click', () => {
            activateTab(index);
          });

          tab.addEventListener('keydown', (event) => {
            if (!['ArrowRight', 'ArrowLeft', 'Home', 'End'].includes(event.key)) {
              return;
            }

            event.preventDefault();

            let nextIndex = index;
            if (event.key === 'ArrowRight') nextIndex = (index + 1) % tabs.length;
            if (event.key === 'ArrowLeft') nextIndex = (index - 1 + tabs.length) % tabs.length;
            if (event.key === 'Home') nextIndex = 0;
            if (event.key === 'End') nextIndex = tabs.length - 1;

            activateTab(nextIndex);
            tabs[nextIndex].focus();
          });
        });

        activateTab(0);
      });
    });
    </script>

  <?php endwhile; ?>

</main>

<?php get_footer();
