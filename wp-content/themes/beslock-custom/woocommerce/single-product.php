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
    $product_navigation = array();
    $features_tab_id = 'product-tab-features-' . get_the_ID();
    $reviews_tab_id = 'product-tab-reviews-' . get_the_ID();
    $features_panel_id = 'product-panel-features-' . get_the_ID();
    $reviews_panel_id = 'product-panel-reviews-' . get_the_ID();

    $product_navigation_ids = get_posts( array(
      'post_type'      => 'product',
      'post_status'    => 'publish',
      'posts_per_page' => -1,
      'fields'         => 'ids',
      'orderby'        => 'date',
      'order'          => 'DESC',
    ) );

    if ( is_array( $product_navigation_ids ) ) {
      $product_navigation_ids = array_values( array_map( 'intval', $product_navigation_ids ) );
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
              <table class="product-features-table">
                <caption class="visually-hidden"><?php printf( esc_html__( 'Resumen de características de %s', 'beslock' ), get_the_title() ); ?></caption>
                <thead>
                  <tr>
                    <th scope="col"><?php echo esc_html__( 'Característica', 'beslock' ); ?></th>
                    <th scope="col"><?php echo esc_html__( 'Especificación', 'beslock' ); ?></th>
                  </tr>
                </thead>
                <tbody>
                  <?php foreach ( $product_features as $feature ) : ?>
                    <tr>
                      <th scope="row"><?php echo esc_html( $feature['label'] ?? '' ); ?></th>
                      <td><?php echo esc_html( $feature['value'] ?? '' ); ?></td>
                    </tr>
                  <?php endforeach; ?>
                </tbody>
              </table>
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
              <ul class="product-specs-list product-reviews-list">
                <?php foreach ( $product_reviews as $review ) : ?>
                  <li>
                    <strong><?php echo esc_html( $review['author'] ); ?></strong>
                    <?php if ( ! empty( $review['rating'] ) ) : ?>
                      <span><?php printf( esc_html__( ' (%d/5)', 'beslock' ), intval( $review['rating'] ) ); ?></span>
                    <?php endif; ?>
                    <p><?php echo esc_html( $review['text'] ); ?></p>
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
