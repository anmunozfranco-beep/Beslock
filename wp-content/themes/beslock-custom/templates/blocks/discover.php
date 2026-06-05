<?php
/**
 * Block: Partner Banner
 * Reuses the former Discover section slot for institutional partner messaging.
 */
?>

<section class="discover beslock-partner-banner section section--lined section-reveal is-active" aria-labelledby="zonas-smart-banner-title">
  <div class="u-container">
    <div class="discover__block beslock-partner-banner__inner">

      <div class="discover__text beslock-partner-banner__content">
        <p class="beslock-partner-banner__eyebrow">
          <?php esc_html_e( 'Comercializador autorizado', 'beslock' ); ?>
        </p>

        <h2 class="beslock-partner-banner__title" id="zonas-smart-banner-title">
          <span class="beslock-partner-banner__title-line beslock-partner-banner__title-line--brand">
            <?php esc_html_e( 'BESLOCK', 'beslock' ); ?><sup class="beslock-partner-banner__registered">&reg;</sup>
            <span class="beslock-partner-banner__country"><?php esc_html_e( 'en Colombia', 'beslock' ); ?></span>
          </span>
          <span class="beslock-partner-banner__title-line"><?php esc_html_e( 'ZONAS SMART', 'beslock' ); ?></span>
        </h2>

        <a class="beslock-partner-banner__cta" href="<?php echo esc_url( home_url( '/#productos' ) ); ?>">
          <?php esc_html_e( 'Conocer productos', 'beslock' ); ?>
        </a>
      </div>

      <div class="discover__image beslock-partner-banner__logo">
        <?php
          $partner_logo_path = get_stylesheet_directory() . '/assets/images/partners/zonas-smart-logo.png';
          $partner_logo_url  = get_stylesheet_directory_uri() . '/assets/images/partners/zonas-smart-logo.png';

          if ( file_exists( $partner_logo_path ) ) :
            $partner_logo_url = $partner_logo_url . '?v=' . filemtime( $partner_logo_path );
        ?>
          <div class="beslock-partner-banner__logo-surface">
            <img
              class="beslock-partner-banner__logo-img"
              src="<?php echo esc_url( $partner_logo_url ); ?>"
              alt="<?php esc_attr_e( 'ZONAS SMART', 'beslock' ); ?>"
              width="1024"
              height="1024"
              loading="lazy"
              decoding="async"
            >
          </div>
        <?php endif; ?>
      </div>

    </div>
  </div>
</section>
