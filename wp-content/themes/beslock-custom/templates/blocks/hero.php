<!-- === HERO BESLOCK START (template-part) === -->
<?php /*
	  Hero implemented as template-part. Uses theme-relative asset paths under
	  `assets/images/hero/clips` and `assets/images/hero/overlays`.
*/
	  $hero_overlay_path  = '/assets/images/hero/overlays/';
  $hero_overlay_files = array(
    'e-flex_hero.png'    => 'e-flex_hero.webp',
    'e-nova_hero.png'    => 'e-nova_hero.webp',
    'e-prime_hero.png'   => 'e-prime_hero.webp',
    'e-shield_hero.png'  => 'e-shield-hero.webp',
    'e-touch_hero.png'   => 'e-touch_hero.webp',
    'e-orbit_hero.png'   => 'e-orbit_hero_e.webp',
    'e-orbit_2_hero.png' => 'e-orbit_hero_i.webp',
  );

  $hero_asset = static function ( $relative_path ) {
    $asset_fs = get_stylesheet_directory() . $relative_path;
    $asset_url = get_stylesheet_directory_uri() . $relative_path;
    $asset_exists = file_exists( $asset_fs );

    if ( $asset_exists ) {
      $asset_url .= '?v=' . filemtime( $asset_fs );
    }

    return array(
      'exists' => $asset_exists,
      'fs'     => $asset_fs,
      'url'    => $asset_url,
    );
  };

  $resolve_hero_overlay = static function ( $overlay_file ) use ( $hero_asset, $hero_overlay_files, $hero_overlay_path ) {
    $resolved_file = isset( $hero_overlay_files[ $overlay_file ] ) ? $hero_overlay_files[ $overlay_file ] : $overlay_file;
    $overlay = $hero_asset( $hero_overlay_path . $resolved_file );
    $overlay['file'] = $resolved_file;

    return $overlay;
  };

  $resolve_hero_webp_asset = static function ( $asset ) use ( $hero_asset ) {
    if ( empty( $asset['fs'] ) ) {
      return array( 'url' => '' );
    }

    $webp_relative_path = str_replace( get_stylesheet_directory(), '', preg_replace( '/\.[^.]+$/', '.webp', $asset['fs'] ) );
    $webp_asset = $hero_asset( $webp_relative_path );

    return ! empty( $webp_asset['exists'] ) ? $webp_asset : array( 'url' => '' );
  };

	  $startup_overlay = 'e-flex_hero.png';
	  $startup_overlay_asset = $resolve_hero_overlay( $startup_overlay );
	  $startup_overlay_url = $startup_overlay_asset['url'];
	  $startup_overlay_webp_asset = $resolve_hero_webp_asset( $startup_overlay_asset );
	  $startup_overlay_webp_url = ! empty( $startup_overlay_webp_asset['url'] ) ? $startup_overlay_webp_asset['url'] : '';
	  $transparent_pixel = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==';
?>
<section class="beslock-hero" id="beslockHero" aria-roledescription="carousel" aria-label="Hero carousel" data-startup-state="booting">
  <div class="beslock-loader" id="beslockLoader" role="status" aria-live="polite" aria-label="<?php echo esc_attr__( 'Cargando presentación de Beslock', 'beslock' ); ?>" aria-hidden="false" data-loader-mode="auto" data-stage="booting">
    <div class="beslock-loader__bg" aria-hidden="true"></div>
    <div class="beslock-loader__scene" aria-hidden="true">
      <span class="beslock-loader__wrap">
        <img class="beslock-loader__img" src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/logo-green.png' ); ?>" alt="" aria-hidden="true" />
        <span class="beslock-loader__tm">®</span>
      </span>
      <span class="beslock-loader__progress"><span class="beslock-loader__progress-fill"></span></span>
    </div>
  </div>

  <article class="hero-slide beslock-hero__slide hero-startup-fallback beslock-hero__startup is-active" id="heroStartupFallback" aria-hidden="false" aria-roledescription="slide" aria-label="Intro slide">
    <div class="slide-inner beslock-hero__slide-inner">
      <div class="hero-startup-fallback__media" aria-hidden="true"></div>
      <div class="slide-dim beslock-hero__slide-dim" aria-hidden="true"></div>
      <picture class="slide-overlay-frame beslock-hero__overlay-frame" aria-hidden="true">
        <?php if ( $startup_overlay_webp_url ): ?>
          <source type="image/webp" srcset="<?php echo esc_url( $startup_overlay_webp_url ); ?>">
        <?php endif; ?>
        <img class="slide-overlay beslock-hero__overlay overlay--visible" src="<?php echo esc_url( $startup_overlay_url ); ?>" alt="" aria-hidden="true" decoding="async" loading="eager" fetchpriority="high" />
      </picture>
      <div class="slide-content beslock-hero__content">
        <h1 class="hero__title"><?php echo esc_html( 'e-Flex' ); ?></h1>
        <p class="hero__subtitle"><?php echo esc_html( 'Llegar sin complicaciones' ); ?></p>
      </div>
    </div>
  </article>

  <div class="hero-viewport beslock-hero__viewport" id="heroViewport" tabindex="-1">
    <div class="hero-slides beslock-hero__slides" id="heroSlides">
      <?php
	        $video_base_path = '/assets/images/hero/clips/';
        $video_base_fs   = get_stylesheet_directory() . $video_base_path;
        $video_base_url  = get_stylesheet_directory_uri() . $video_base_path;

	        // Use explicit filenames present in the repo under assets/images/hero/clips.
        $videos = array(
          'e-Flex.mp4',
          'e-Nova.mp4',
          'e-Prime.mp4',
          'e-Shield.mp4',
          'e-Touch.mp4',
          'e-Orbit.mp4',
        );
        $overlays = array(
          'e-flex_hero.png',
          'e-nova_hero.png',
          'e-prime_hero.png',
          'e-shield_hero.png',
          'e-touch_hero.png',
          'e-orbit_hero.png',
        );
        $count = min(count($videos), count($overlays));
        for ($i = 0; $i < $count; $i++):
          $vid = $videos[$i];
          $ov  = $overlays[$i];
          $is_first_slide = ( 0 === $i );
          $video_fs = $video_base_fs . $vid;
          $video_url = $video_base_url . rawurlencode( $vid );
          if ( file_exists( $video_fs ) ) {
            $video_url .= '?v=' . filemtime( $video_fs );
          }
          $video_webm_fs = preg_replace( '/\.mp4$/i', '.webm', $video_fs );
          $video_webm_url = '';
          if ( file_exists( $video_webm_fs ) ) {
            $video_webm_url = get_stylesheet_directory_uri() . $video_base_path . rawurlencode( pathinfo( $vid, PATHINFO_FILENAME ) . '.webm' ) . '?v=' . filemtime( $video_webm_fs );
          }
	          $mobile_video_path = '/assets/images/hero/clips/mobile/' . pathinfo( $vid, PATHINFO_FILENAME ) . '-mobile.mp4';
          $mobile_video_fs = get_stylesheet_directory() . $mobile_video_path;
          $mobile_video_url = '';
          if ( file_exists( $mobile_video_fs ) ) {
            $mobile_video_url = get_stylesheet_directory_uri() . $mobile_video_path . '?v=' . filemtime( $mobile_video_fs );
          }
	          $poster_relative_path = '/assets/images/hero/clips/posters/' . pathinfo( $vid, PATHINFO_FILENAME ) . '.webp';
          $poster_fs = get_stylesheet_directory() . $poster_relative_path;
          $poster_url = '';
          if ( file_exists( $poster_fs ) ) {
            $poster_url = get_stylesheet_directory_uri() . $poster_relative_path . '?v=' . filemtime( $poster_fs );
          }
          $ov_asset = $resolve_hero_overlay( $ov );
          $ov_webp_asset = $resolve_hero_webp_asset( $ov_asset );
          $ov_webp_url = ! empty( $ov_webp_asset['url'] ) ? $ov_webp_asset['url'] : '';
      ?>
      <article class="hero-slide beslock-hero__slide" data-index="<?php echo $i; ?>" aria-roledescription="slide" aria-label="Slide <?php echo $i+1; ?>">
        <div class="slide-inner beslock-hero__slide-inner">
          <video class="slide-video beslock-hero__video" muted playsinline preload="<?php echo $is_first_slide ? 'metadata' : 'none'; ?>" loop<?php echo $poster_url ? ( $is_first_slide ? ' poster="' . esc_url( $poster_url ) . '"' : ' data-poster="' . esc_url( $poster_url ) . '"' ) : ''; ?> data-src="<?php echo esc_url( $video_url ); ?>"<?php echo $video_webm_url ? ' data-src-webm="' . esc_url( $video_webm_url ) . '"' : ''; ?><?php echo $mobile_video_url ? ' data-src-mobile="' . esc_url( $mobile_video_url ) . '"' : ''; ?>></video>
	          <!-- Dim layer strictly over the clip to improve white text contrast; overlays remain above -->
	          <div class="slide-dim beslock-hero__slide-dim" aria-hidden="true"></div>
	          <picture class="slide-overlay-frame beslock-hero__overlay-frame" aria-hidden="true">
	            <?php if ($ov_webp_url): ?>
	              <source type="image/webp" <?php echo $is_first_slide ? 'srcset="' . esc_url( $ov_webp_url ) . '"' : 'data-srcset="' . esc_url( $ov_webp_url ) . '"'; ?>>
	            <?php endif; ?>
            <?php
              if ($i === 0) {
                $data_offset_attr = ' data-offset="10"';
              } elseif ($i === 2 || $i === 5) {
                $data_offset_attr = ' data-offset="27"';
              } elseif ($i === 4) {
                $data_offset_attr = ' data-offset="30"';
              } else {
                $data_offset_attr = '';
              }
            ?>
            <?php
              $ov_url = $ov_asset['url'];
            ?>
	            <img class="slide-overlay beslock-hero__overlay" src="<?php echo $is_first_slide ? esc_url( $ov_url ) : esc_attr( $transparent_pixel ); ?>"<?php echo $is_first_slide ? '' : ' data-src="' . esc_url( $ov_url ) . '" data-defer-until="hero-slide"'; ?><?php echo $data_offset_attr; ?> alt="" aria-hidden="true" decoding="async" loading="<?php echo $is_first_slide ? 'eager' : 'lazy'; ?>" fetchpriority="<?php echo $is_first_slide ? 'high' : 'low'; ?>" />
	          </picture>
          <?php if ($i === 5): // Add second orbit overlay image that enters at 4s ?>
            <?php
              $ov2 = 'e-orbit_2_hero.png';
              $ov2_asset = $resolve_hero_overlay( $ov2 );
              $ov2_webp_asset = $resolve_hero_webp_asset( $ov2_asset );
              $ov2_webp_url = ! empty( $ov2_webp_asset['url'] ) ? $ov2_webp_asset['url'] : '';
            ?>
	              <picture class="slide-overlay-frame beslock-hero__overlay-frame" aria-hidden="true">
	              <?php if ($ov2_webp_url): ?>
	                <source type="image/webp" data-srcset="<?php echo esc_url( $ov2_webp_url ); ?>">
	              <?php endif; ?>
	              <img class="slide-overlay beslock-hero__overlay" src="<?php echo esc_attr( $transparent_pixel ); ?>" data-src="<?php echo esc_url( $ov2_asset['url'] ); ?>" data-defer-until="hero-slide" data-start="4" data-offset="27" alt="" aria-hidden="true" decoding="async" loading="lazy" fetchpriority="low" />
	            </picture>
          <?php endif; ?>
          <div class="slide-content beslock-hero__content">
            <?php
              // Derive a human-friendly title from the overlay filename.
              $base = pathinfo($ov, PATHINFO_FILENAME); // e-flex_hero
              $title_raw = str_replace('_', ' ', $base); // e-flex hero
              // remove the word "hero" if present and collapse whitespace
              $title_raw = preg_replace('/\bhero\b/i', '', $title_raw);
              $title_raw = trim(preg_replace('/\s+/', ' ', $title_raw));
              // capitalize the character after a hyphen (e.g. e-flex -> e-Flex)
              $pos = strpos($title_raw, '-');
              if ($pos !== false && isset($title_raw[$pos + 1])) {
                $title_raw = substr_replace($title_raw, strtoupper($title_raw[$pos + 1]), $pos + 1, 1);
              }

              // Identify product key (use the first token, e.g. 'e-flex' => 'e-flex')
              $product_key = strtolower(preg_replace('/\s+/', '', str_replace(' ', '-', $title_raw)));

              // Hero subtitle overrides (exact strings requested)
              $hero_subtitles = array(
                'e-nova'  => 'Comodidad, seguridad y tranquilidad',
                'e-flex'  => 'Llegar sin complicaciones',
                'e-prime' => 'Para todos los espacios',
                'e-touch' => 'Acceso para todos',
                'e-shield' => 'Protege lo más valioso',
                'e-orbit' => 'En cualquier lugar',
              );

              $subtitle = isset($hero_subtitles[$product_key]) ? $hero_subtitles[$product_key] : ucwords($title_raw);
              $split_mobile_subtitle = ( 'e-nova' === $product_key );
            ?>

            <h1 class="hero__title"><?php echo esc_html($title_raw); ?></h1>
            <p class="hero__subtitle<?php echo $split_mobile_subtitle ? ' hero__subtitle--split-mobile' : ''; ?>">
              <?php if ( $split_mobile_subtitle ) : ?>
                <span class="hero__subtitle-line">Comodidad, seguridad</span> <span class="hero__subtitle-line">y tranquilidad</span>
              <?php else : ?>
                <?php echo esc_html($subtitle); ?>
              <?php endif; ?>
            </p>
          </div>
        </div>
      </article>
      <?php endfor; ?>
    </div>

    <nav class="hero-dots beslock-hero__dots" id="heroDots" aria-label="Carousel navigation" role="tablist">
      <?php for ($i = 1; $i <= 6; $i++): ?>
        <button class="hero-dot beslock-hero__dot" data-index="<?php echo $i-1; ?>" aria-label="Go to slide <?php echo $i; ?>" role="tab"></button>
      <?php endfor; ?>
    </nav>
  </div>
</section>
<!-- === HERO BESLOCK END (template-part) === -->
