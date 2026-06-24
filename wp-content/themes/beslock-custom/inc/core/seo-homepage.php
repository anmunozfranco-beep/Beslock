<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

function beslock_homepage_meta_title() {
  return 'BESLOCK® Smart Security Solutions';
}

function beslock_homepage_meta_description() {
  return 'Seguridad inteligente para hogares, oficinas y accesos exteriores.';
}

function beslock_homepage_meta_image() {
  return 'https://beslock.com.co/wp-content/uploads/2026/06/beslock-og-linkedin-1200x627-1.png';
}

function beslock_homepage_metadata_context() {
  return ! is_admin() && function_exists( 'is_front_page' ) && is_front_page() && ! is_paged();
}

function beslock_homepage_document_title( $title ) {
  if ( beslock_homepage_metadata_context() ) {
    return beslock_homepage_meta_title();
  }

  return $title;
}
add_filter( 'pre_get_document_title', 'beslock_homepage_document_title', PHP_INT_MAX );

function beslock_homepage_document_title_parts( $parts ) {
  if ( beslock_homepage_metadata_context() ) {
    $parts['title'] = beslock_homepage_meta_title();

    unset( $parts['site'], $parts['tagline'] );
  }

  return $parts;
}
add_filter( 'document_title_parts', 'beslock_homepage_document_title_parts', PHP_INT_MAX );

function beslock_homepage_prepare_metadata_hooks() {
  if ( ! beslock_homepage_metadata_context() ) {
    return;
  }

  remove_action( 'wp_head', 'wp_oembed_add_discovery_links' );
  remove_action( 'wp_head', 'wp_oembed_add_host_js' );
  remove_action( 'wp_head', '\SiteSEO\TitlesMetas::add_meta_description', 1 );
  remove_action( 'wp_head', '\SiteSEO\SocialMetas::fb_graph', 1 );
  remove_action( 'wp_head', '\SiteSEO\SocialMetas::twitter_card', 1 );
  remove_action( 'wp_head', '\SiteSEOPro\StructuredData::render' );

  if ( class_exists( 'Beslock_SEO_Config' ) ) {
    remove_action( 'wp_head', array( 'Beslock_SEO_Config', 'output_json_ld' ), 99 );
  }
}
add_action( 'wp', 'beslock_homepage_prepare_metadata_hooks', PHP_INT_MAX );

function beslock_homepage_output_meta_description() {
  if ( ! beslock_homepage_metadata_context() ) {
    return;
  }

  echo '<meta name="description" content="' . esc_attr( beslock_homepage_meta_description() ) . '">' . "\n";
}
add_action( 'wp_head', 'beslock_homepage_output_meta_description', 1 );

function beslock_homepage_is_front_page_post( $post ) {
  if ( ! $post instanceof WP_Post ) {
    return false;
  }

  $front_page_id = (int) get_option( 'page_on_front' );

  return $front_page_id > 0 && (int) $post->ID === $front_page_id;
}

function beslock_homepage_oembed_response_data( $data, $post, $width, $height ) {
  if ( ! beslock_homepage_is_front_page_post( $post ) ) {
    return $data;
  }

  $home_url = trailingslashit( home_url( '/' ) );

  $data['title']            = beslock_homepage_meta_title();
  $data['provider_name']    = 'BESLOCK';
  $data['provider_url']     = $home_url;
  $data['thumbnail_url']    = beslock_homepage_meta_image();
  $data['thumbnail_width']  = 1200;
  $data['thumbnail_height'] = 627;

  return $data;
}
add_filter( 'oembed_response_data', 'beslock_homepage_oembed_response_data', PHP_INT_MAX, 4 );

function beslock_homepage_has_wpcode_og_snippet() {
  static $has_snippet = null;

  if ( null !== $has_snippet ) {
    return $has_snippet;
  }

  $has_snippet = false;

  if ( ! post_type_exists( 'wpcode' ) ) {
    return $has_snippet;
  }

  $snippets = get_posts(
    array(
      'post_type'        => 'wpcode',
      'post_status'      => 'publish',
      's'                => 'beslock-og-linkedin-1200x627-1.png',
      'posts_per_page'   => 1,
      'fields'           => 'ids',
      'no_found_rows'    => true,
      'suppress_filters' => true,
    )
  );

  $has_snippet = ! empty( $snippets );

  return $has_snippet;
}

function beslock_homepage_output_open_graph_fallback() {
  if ( ! beslock_homepage_metadata_context() || beslock_homepage_has_wpcode_og_snippet() ) {
    return;
  }

  $title       = beslock_homepage_meta_title();
  $description = beslock_homepage_meta_description();
  $image       = beslock_homepage_meta_image();

  echo '<meta property="og:title" content="' . esc_attr( $title ) . '">' . "\n";
  echo '<meta property="og:description" content="' . esc_attr( $description ) . '">' . "\n";
  echo '<meta property="og:url" content="' . esc_url( home_url( '/' ) ) . '">' . "\n";
  echo '<meta property="og:type" content="website">' . "\n";
  echo '<meta property="og:image" content="' . esc_url( $image ) . '">' . "\n";
  echo '<meta property="og:image:secure_url" content="' . esc_url( $image ) . '">' . "\n";
  echo '<meta property="og:image:width" content="1200">' . "\n";
  echo '<meta property="og:image:height" content="627">' . "\n";
  echo '<meta property="og:image:type" content="image/png">' . "\n";
  echo '<meta name="twitter:card" content="summary_large_image">' . "\n";
  echo '<meta name="twitter:title" content="' . esc_attr( $title ) . '">' . "\n";
  echo '<meta name="twitter:description" content="' . esc_attr( $description ) . '">' . "\n";
  echo '<meta name="twitter:image" content="' . esc_url( $image ) . '">' . "\n";
}
add_action( 'wp_head', 'beslock_homepage_output_open_graph_fallback', 1 );

function beslock_homepage_output_json_ld() {
  if ( ! beslock_homepage_metadata_context() ) {
    return;
  }

  $home_url = trailingslashit( home_url( '/' ) );
  $title    = beslock_homepage_meta_title();
  $desc     = beslock_homepage_meta_description();

  $schema = array(
    '@context' => 'https://schema.org',
    '@graph'   => array(
      array(
        '@type'           => 'WebSite',
        '@id'             => $home_url . '#website',
        'name'            => $title,
        'description'     => $desc,
        'url'             => $home_url,
        'inLanguage'      => 'es-CO',
        'potentialAction' => array(
          '@type'       => 'SearchAction',
          '@id'         => $home_url . '#searchaction',
          'target'      => $home_url . '?s={search_term_string}',
          'query-input' => 'required name=search_term_string',
        ),
      ),
      array(
        '@type'       => 'WebPage',
        '@id'         => $home_url . '#webpage',
        'name'        => $title,
        'headline'    => $title,
        'description' => $desc,
        'url'         => $home_url,
        'inLanguage'  => 'es-CO',
        'isPartOf'    => array(
          '@id' => $home_url . '#website',
        ),
      ),
      array(
        '@type'           => 'BreadcrumbList',
        '@id'             => $home_url . '#breadcrumblist',
        'itemListElement' => array(
          array(
            '@type'    => 'ListItem',
            'position' => 1,
            'item'     => array(
              '@id'  => $home_url,
              'name' => $title,
            ),
          ),
        ),
      ),
    ),
  );

  echo '<script type="application/ld+json">' . wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . '</script>' . "\n";
}
add_action( 'wp_head', 'beslock_homepage_output_json_ld', 99 );
