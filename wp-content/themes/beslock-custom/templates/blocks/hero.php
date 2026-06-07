<!-- === HERO BESLOCK START (template-part) === -->
<?php /*
  Hero implemented as template-part. Uses theme-relative asset paths under
  `images/Clips_hero` and `images/Hero_develp/images_hero`.
*/
  $hero_overlay_base_path = '/assets/images/Hero_develp/images_hero/';
  $hero_overlay_new_path  = $hero_overlay_base_path . 'overlays_hero_new/';
  $hero_overlay_d_path    = $hero_overlay_base_path . 'images_hero_d/';
  $hero_overlay_new_files = array(
    'e-flex_hero.png'    => 'e-flex_hero.png',
    'e-nova_hero.png'    => 'e-nova_hero.png',
    'e-prime_hero.png'   => 'e-prime_hero.png',
    'e-shield_hero.png'  => 'e-shield-hero.png',
    'e-touch_hero.png'   => 'e-touch_hero.png',
    'e-orbit_hero.png'   => 'e-orbit_hero_e.png',
    'e-orbit_2_hero.png' => 'e-orbit_hero_i.png',
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

  $resolve_hero_overlay = static function ( $overlay_file ) use ( $hero_asset, $hero_overlay_base_path, $hero_overlay_new_files, $hero_overlay_new_path ) {
    $new_overlay_file = isset( $hero_overlay_new_files[ $overlay_file ] ) ? $hero_overlay_new_files[ $overlay_file ] : $overlay_file;
    $new_overlay = $hero_asset( $hero_overlay_new_path . $new_overlay_file );

    if ( ! empty( $new_overlay['exists'] ) ) {
      $new_overlay['file'] = $new_overlay_file;
      $new_overlay['uses_new'] = true;
      return $new_overlay;
    }

    $legacy_overlay = $hero_asset( $hero_overlay_base_path . $overlay_file );
    $legacy_overlay['file'] = $overlay_file;
    $legacy_overlay['uses_new'] = false;
    return $legacy_overlay;
  };

  $resolve_hero_overlay_desktop = static function ( $overlay_file, $resolved_overlay ) use ( $hero_asset, $hero_overlay_d_path ) {
    if ( ! empty( $resolved_overlay['uses_new'] ) ) {
      return $resolved_overlay;
    }

    $overlay_base = pathinfo( $overlay_file, PATHINFO_FILENAME );
    if ( preg_match( '/^(.*)_2_hero$/i', $overlay_base, $matches ) ) {
      $overlay_d_file = $matches[1] . '_d_2.png';
    } else {
      $overlay_d_file = preg_replace( '/_hero$/i', '_d', $overlay_base ) . '.png';
    }

    $desktop_overlay = $hero_asset( $hero_overlay_d_path . $overlay_d_file );
    return ! empty( $desktop_overlay['exists'] ) ? $desktop_overlay : array( 'url' => '' );
  };

  $startup_overlay = 'e-flex_hero.png';
  $startup_overlay_asset = $resolve_hero_overlay( $startup_overlay );
  $startup_overlay_url = $startup_overlay_asset['url'];
  $startup_overlay_d_asset = $resolve_hero_overlay_desktop( $startup_overlay, $startup_overlay_asset );
	  $startup_overlay_d_url = ! empty( $startup_overlay_d_asset['url'] ) ? $startup_overlay_d_asset['url'] : '';
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

  <article class="hero-slide hero-startup-fallback is-active" id="heroStartupFallback" aria-hidden="false" aria-roledescription="slide" aria-label="Intro slide">
    <div class="slide-inner">
      <div class="hero-startup-fallback__media" aria-hidden="true"></div>
      <div class="slide-dim" aria-hidden="true"></div>
      <picture class="slide-overlay-frame" aria-hidden="true">
        <?php if ( $startup_overlay_d_url ): ?>
          <source media="(min-width:600px)" srcset="<?php echo esc_url( $startup_overlay_d_url ); ?>">
        <?php endif; ?>
        <img class="slide-overlay overlay--visible" src="<?php echo esc_url( $startup_overlay_url ); ?>" alt="" aria-hidden="true" decoding="async" loading="eager" fetchpriority="high" />
      </picture>
      <div class="slide-content">
        <h1 class="hero__title"><?php echo esc_html( 'e-Flex' ); ?></h1>
        <p class="hero__subtitle"><?php echo esc_html( 'Llegar sin complicaciones' ); ?></p>
      </div>
    </div>
  </article>

  <div class="hero-viewport" id="heroViewport" tabindex="-1">
    <div class="hero-slides" id="heroSlides">
      <?php
        $video_base_path = '/assets/images/Clips_hero/';
        $video_base_fs   = get_stylesheet_directory() . $video_base_path;
        $video_base_url  = get_stylesheet_directory_uri() . $video_base_path;

        // Use explicit filenames present in the repo under assets/images/Clips_hero.
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
          $mobile_video_path = '/assets/images/Clips_hero/mobile/' . pathinfo( $vid, PATHINFO_FILENAME ) . '-mobile.mp4';
          $mobile_video_fs = get_stylesheet_directory() . $mobile_video_path;
          $mobile_video_url = '';
          if ( file_exists( $mobile_video_fs ) ) {
            $mobile_video_url = get_stylesheet_directory_uri() . $mobile_video_path . '?v=' . filemtime( $mobile_video_fs );
          }
          $poster_relative_path = '/assets/images/Clips_hero/posters/' . pathinfo( $vid, PATHINFO_FILENAME ) . '.webp';
          $poster_fs = get_stylesheet_directory() . $poster_relative_path;
          $poster_url = '';
          if ( file_exists( $poster_fs ) ) {
            $poster_url = get_stylesheet_directory_uri() . $poster_relative_path . '?v=' . filemtime( $poster_fs );
          }
          $ov_asset = $resolve_hero_overlay( $ov );
          $ov_d_asset = $resolve_hero_overlay_desktop( $ov, $ov_asset );
          $ov_d_url = ! empty( $ov_d_asset['url'] ) ? $ov_d_asset['url'] : '';
      ?>
      <article class="hero-slide" data-index="<?php echo $i; ?>" aria-roledescription="slide" aria-label="Slide <?php echo $i+1; ?>">
        <div class="slide-inner">
          <video class="slide-video" muted playsinline preload="<?php echo $is_first_slide ? 'metadata' : 'none'; ?>" loop<?php echo $poster_url ? ( $is_first_slide ? ' poster="' . esc_url( $poster_url ) . '"' : ' data-poster="' . esc_url( $poster_url ) . '"' ) : ''; ?> data-src="<?php echo esc_url( $video_url ); ?>"<?php echo $mobile_video_url ? ' data-src-mobile="' . esc_url( $mobile_video_url ) . '"' : ''; ?>></video>
	          <!-- Dim layer strictly over the clip to improve white text contrast; overlays remain above -->
	          <div class="slide-dim" aria-hidden="true"></div>
	          <picture class="slide-overlay-frame" aria-hidden="true">
	            <?php if ($ov_d_url): ?>
	              <source media="(min-width:600px)" <?php echo $is_first_slide ? 'srcset="' . esc_url( $ov_d_url ) . '"' : 'data-srcset="' . esc_url( $ov_d_url ) . '"'; ?>>
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
	            <img class="slide-overlay" src="<?php echo $is_first_slide ? esc_url( $ov_url ) : esc_attr( $transparent_pixel ); ?>"<?php echo $is_first_slide ? '' : ' data-src="' . esc_url( $ov_url ) . '" data-defer-until="hero-slide"'; ?><?php echo $data_offset_attr; ?> alt="" aria-hidden="true" decoding="async" loading="<?php echo $is_first_slide ? 'eager' : 'lazy'; ?>" fetchpriority="<?php echo $is_first_slide ? 'high' : 'low'; ?>" />
	          </picture>
          <?php if ($i === 5): // Add second orbit overlay image that enters at 4s ?>
            <?php
              $ov2 = 'e-orbit_2_hero.png';
              $ov2_asset = $resolve_hero_overlay( $ov2 );
              $ov2_d_asset = $resolve_hero_overlay_desktop( $ov2, $ov2_asset );
              $ov2_d_url = ! empty( $ov2_d_asset['url'] ) ? $ov2_d_asset['url'] : '';
            ?>
	              <picture class="slide-overlay-frame" aria-hidden="true">
	              <?php if ($ov2_d_url): ?>
	                <source media="(min-width:600px)" data-srcset="<?php echo esc_url( $ov2_d_url ); ?>">
	              <?php endif; ?>
	              <img class="slide-overlay" src="<?php echo esc_attr( $transparent_pixel ); ?>" data-src="<?php echo esc_url( $ov2_asset['url'] ); ?>" data-defer-until="hero-slide" data-start="4" data-offset="27" alt="" aria-hidden="true" decoding="async" loading="lazy" fetchpriority="low" />
	            </picture>
          <?php endif; ?>
          <div class="slide-content">
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

    <nav class="hero-dots" id="heroDots" aria-label="Carousel navigation" role="tablist">
      <?php for ($i = 1; $i <= 6; $i++): ?>
        <button class="hero-dot" data-index="<?php echo $i-1; ?>" aria-label="Go to slide <?php echo $i; ?>" role="tab"></button>
      <?php endfor; ?>
    </nav>
  </div>
</section>
<!-- === HERO BESLOCK END (template-part) === -->
