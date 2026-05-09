<!-- === HERO BESLOCK START (template-part) === -->
<?php /*
  Hero implemented as template-part. Uses theme-relative asset paths under
  `images/Clips_hero` and `images/Hero_develp/images_hero`.
*/
  $startup_overlay = 'e-flex_hero.png';
  $startup_overlay_fs = get_stylesheet_directory() . '/assets/images/Hero_develp/images_hero/' . $startup_overlay;
  $startup_overlay_url = get_stylesheet_directory_uri() . '/assets/images/Hero_develp/images_hero/' . $startup_overlay;
  if ( file_exists( $startup_overlay_fs ) ) {
    $startup_overlay_url .= '?v=' . filemtime( $startup_overlay_fs );
  }

  $startup_overlay_d_file = 'e-flex_d.png';
  $startup_overlay_d_fs = get_stylesheet_directory() . '/assets/images/Hero_develp/images_hero/images_hero_d/' . $startup_overlay_d_file;
  $startup_overlay_d_url = file_exists( $startup_overlay_d_fs )
    ? ( get_stylesheet_directory_uri() . '/assets/images/Hero_develp/images_hero/images_hero_d/' . $startup_overlay_d_file )
    : '';
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
        <img class="slide-overlay overlay--visible" src="<?php echo esc_url( $startup_overlay_url ); ?>" alt="" aria-hidden="true" />
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
          $video_fs = $video_base_fs . $vid;
          $video_url = $video_base_url . rawurlencode( $vid );
          if ( file_exists( $video_fs ) ) {
            $video_url .= '?v=' . filemtime( $video_fs );
          }
          // Map overlay filename to high-res variant in images_hero/images_hero_d if present
          $ov_base = pathinfo($ov, PATHINFO_FILENAME);
          if (preg_match('/^(.*)_2_hero$/i', $ov_base, $m)) {
            $ov_d_file = $m[1] . '_d_2.png';
          } else {
            $ov_d_file = preg_replace('/_hero$/i', '_d', $ov_base) . '.png';
          }
          $ov_d_fs = get_stylesheet_directory() . '/assets/images/Hero_develp/images_hero/images_hero_d/' . $ov_d_file;
          $ov_d_url = file_exists($ov_d_fs) ? (get_stylesheet_directory_uri() . '/assets/images/Hero_develp/images_hero/images_hero_d/' . $ov_d_file) : '';
      ?>
      <article class="hero-slide" data-index="<?php echo $i; ?>" aria-roledescription="slide" aria-label="Slide <?php echo $i+1; ?>">
        <div class="slide-inner">
          <video class="slide-video" muted playsinline preload="auto" loop src="<?php echo esc_url( $video_url ); ?>"></video>
          <!-- Dim layer strictly over the clip to improve white text contrast; overlays remain above -->
          <div class="slide-dim" aria-hidden="true"></div>
          <picture class="slide-overlay-frame" aria-hidden="true">
            <?php if ($ov_d_url): ?>
              <source media="(min-width:600px)" srcset="<?php echo esc_url( $ov_d_url ); ?>">
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
              // Resolve filesystem path for the overlay and append filemtime as cache-buster
              $ov_fs = get_stylesheet_directory() . '/assets/images/Hero_develp/images_hero/' . $ov;
              $ov_url = get_stylesheet_directory_uri() . '/assets/images/Hero_develp/images_hero/' . $ov;
              if ( file_exists( $ov_fs ) ) {
                $ov_url .= '?v=' . filemtime( $ov_fs );
              }
            ?>
            <img class="slide-overlay" src="<?php echo esc_url( $ov_url ); ?>"<?php echo $data_offset_attr; ?> alt="" aria-hidden="true" />
          </picture>
          <?php if ($i === 5): // Add second orbit overlay image that enters at 3.55s ?>
            <?php
              $ov2 = 'e-orbit_2_hero.png';
              $ov2_base = pathinfo($ov2, PATHINFO_FILENAME);
              if (preg_match('/^(.*)_2_hero$/i', $ov2_base, $mm)) {
                $ov2_d_file = $mm[1] . '_d_2.png';
              } else {
                $ov2_d_file = preg_replace('/_hero$/i', '_d', $ov2_base) . '.png';
              }
              $ov2_d_fs = get_stylesheet_directory() . '/assets/images/Hero_develp/images_hero/images_hero_d/' . $ov2_d_file;
              $ov2_d_url = file_exists($ov2_d_fs) ? (get_stylesheet_directory_uri() . '/assets/images/Hero_develp/images_hero/images_hero_d/' . $ov2_d_file) : '';
            ?>
              <picture class="slide-overlay-frame" aria-hidden="true">
              <?php if ($ov2_d_url): ?>
                <source media="(min-width:600px)" srcset="<?php echo esc_url( $ov2_d_url ); ?>">
              <?php endif; ?>
              <img class="slide-overlay" src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/Hero_develp/images_hero/e-orbit_2_hero.png' ); ?>" data-start="3.55" data-offset="27" alt="" aria-hidden="true" />
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
