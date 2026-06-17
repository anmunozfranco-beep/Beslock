<?php
/**
 * Front Page
 * Loads modular sections if available, otherwise shows a safe fallback.
 */
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

get_header();
?>

<main id="main-content">

  <?php
  // If the Page editor has content, render it first.
  if ( have_posts() ) :
    while ( have_posts() ) : the_post();
      the_content();
    endwhile;
  endif;

  // Hero section (support both template locations)
  if ( file_exists( get_stylesheet_directory() . '/template-parts/hero.php' ) ) {
    get_template_part( 'template-parts/hero' );
  } elseif ( file_exists( get_stylesheet_directory() . '/templates/blocks/hero.php' ) ) {
    get_template_part( 'templates/blocks/hero' );
  }

  // Products section
  if ( file_exists( get_stylesheet_directory() . '/template-parts/products.php' ) ) {
    get_template_part( 'template-parts/products' );
  } elseif ( file_exists( get_stylesheet_directory() . '/templates/blocks/products-portfolio.php' ) ) {
    get_template_part( 'templates/blocks/products-portfolio' );
  }

  ?>

  <?php if ( ! file_exists( get_stylesheet_directory() . '/template-parts/hero.php' ) && ! file_exists( get_stylesheet_directory() . '/templates/blocks/hero.php' ) ) : ?>
    <section class="home-fallback">
      <div class="u-container">
        <h1><span class="brand">BESLOCK<span class="brand__tm">®</span></span> Smart Locks</h1>
        <p>Secure your home with smart technology</p>
      </div>
    </section>
  <?php endif; ?>

</main>

<?php
get_footer();
