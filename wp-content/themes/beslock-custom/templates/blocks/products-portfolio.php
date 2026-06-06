<?php
/**
 * products-portfolio.php — simplified front-page product grid using WP_Query
 * This uses WooCommerce's template override `content-product.php` so product
 * cards are rendered consistently across the site.
 */

if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

$product_slugs = array(
  'e-shield',
  'e-prime',
  'e-orbit',
  'e-touch',
  'e-flex',
  'e-nova',
);

$args = array(
  'post_type'      => 'product',
  'post_status'    => 'publish',
  'posts_per_page' => count( $product_slugs ),
  'post_name__in'  => $product_slugs,
  'orderby'        => 'post_name__in',
);

$loop = new WP_Query( $args );

if ( $loop->have_posts() ) : ?>

  <section id="productos" class="products-portfolio section section-reveal">
    <div class="u-container products-portfolio__grid">

      <?php while ( $loop->have_posts() ) : $loop->the_post(); ?>

        <?php wc_get_template_part( 'content', 'product' ); ?>

      <?php endwhile; ?>

    </div>
  </section>

<?php endif;
wp_reset_postdata();
