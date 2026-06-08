<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

// Move of previous enqueue logic. No functional change — only relocated.
add_action( 'wp_enqueue_scripts', function() {

  if ( function_exists( 'is_child_theme' ) && is_child_theme() ) {
    wp_enqueue_style( 'kadence-parent-style', get_template_directory_uri() . '/style.css', [], null );
  }

  $theme_dir_uri  = get_stylesheet_directory_uri();
  $theme_dir_path = get_stylesheet_directory();
  $is_product_page = function_exists( 'is_product' ) && is_product();
  $is_front_page = function_exists( 'is_front_page' ) && is_front_page();

  $ver_main_css = file_exists( $theme_dir_path . '/assets/css/main.css' )
    ? filemtime( $theme_dir_path . '/assets/css/main.css' )
    : null;

  wp_enqueue_style(
    'beslock-extra-style',
    $theme_dir_uri . '/assets/css/main.css',
    array( 'beslock-main-style' ),
    $ver_main_css
  );

  $enqueue_optional_theme_style = static function( $handle, $relative_path, $deps = array( 'beslock-extra-style' ) ) use ( $theme_dir_path, $theme_dir_uri ) {
    $absolute_path = $theme_dir_path . $relative_path;

    if ( file_exists( $absolute_path ) ) {
      wp_enqueue_style( $handle, $theme_dir_uri . $relative_path, $deps, filemtime( $absolute_path ) );
    }
  };

  $inline_header_fallback = "\n.header{position:fixed;top:0;left:0;right:0;z-index:var(--z-header);}\n";
  wp_add_inline_style( 'beslock-main-style', $inline_header_fallback );

  $cart_css_path = $theme_dir_path . '/assets/css/beslock-cart-empty.css';
  if ( file_exists( $cart_css_path ) ) {
    if ( function_exists( 'is_cart' ) && is_cart() ) {
      wp_enqueue_style(
        'beslock-cart-empty',
        $theme_dir_uri . '/assets/css/beslock-cart-empty.css',
        array( 'beslock-main-style' ),
        filemtime( $cart_css_path )
      );
    }
  }

  wp_enqueue_style(
    'beslock-bootstrap-icons',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css',
    [],
    '1.13.1'
  );

  $menu_css_path = $theme_dir_path . '/assets/css/menu-products-mobile.css';
  $ver_menu_css = file_exists( $menu_css_path ) ? filemtime( $menu_css_path ) : null;

  wp_enqueue_style(
    'beslock-menu-products-mobile',
    $theme_dir_uri . '/assets/css/menu-products-mobile.css',
    [ 'beslock-main-style' ],
    $ver_menu_css
  );

  $models_css_path = $theme_dir_path . '/assets/css/models-mobile.css';
  $ver_models_css = file_exists( $models_css_path ) ? filemtime( $models_css_path ) : null;

  wp_enqueue_style(
    'beslock-models-mobile',
    $theme_dir_uri . '/assets/css/models-mobile.css',
    [ 'beslock-main-style', 'beslock-menu-products-mobile' ],
    $ver_models_css
  );

  $enqueue_optional_theme_style( 'beslock-layout-helpers', '/assets/css/utilities/layout-helpers.css' );
  $enqueue_optional_theme_style( 'beslock-utilities', '/assets/css/utilities/utilities.css' );
  $enqueue_optional_theme_style( 'beslock-button-utilities', '/assets/css/utilities/buttons.css' );
  $enqueue_optional_theme_style( 'beslock-header-component', '/assets/css/components/header.css', [ 'beslock-extra-style', 'beslock-menu-products-mobile' ] );
  $enqueue_optional_theme_style( 'beslock-manuals-viewer', '/assets/css/manuals-viewer.css', [ 'beslock-extra-style', 'beslock-menu-products-mobile', 'beslock-header-component' ] );
  $enqueue_optional_theme_style( 'beslock-support-drawer', '/assets/css/support-drawer.css', [ 'beslock-manuals-viewer' ] );
  $enqueue_optional_theme_style( 'beslock-discover-component', '/assets/css/components/discover.css' );
  $enqueue_optional_theme_style( 'beslock-homepage-layout', '/assets/css/layout/homepage.css' );
  $enqueue_optional_theme_style( 'beslock-recommendations-layout', '/assets/css/layout/recommendations.css' );
  $enqueue_optional_theme_style( 'beslock-storefront-layout', '/assets/css/layout/storefront.css' );

  if ( apply_filters( 'beslock_enqueue_gsap', false ) ) {
    wp_enqueue_script(
      'gsap',
      'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js',
      [],
      null,
      true
    );
    wp_enqueue_script(
      'scrolltrigger',
      'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js',
      [ 'gsap' ],
      null,
      true
    );
  }

  $main_js_path = $theme_dir_path . '/assets/js/main.js';
  $ver_main_js = file_exists( $main_js_path ) ? filemtime( $main_js_path ) : null;

  wp_enqueue_script(
    'beslock-main-js',
    $theme_dir_uri . '/assets/js/main.js',
    [],
    $ver_main_js,
    true
  );

  $add_to_cart_feedback_css = $theme_dir_path . '/assets/css/add-to-cart-feedback.css';
  if ( file_exists( $add_to_cart_feedback_css ) ) {
    wp_enqueue_style(
      'beslock-add-to-cart-feedback',
      $theme_dir_uri . '/assets/css/add-to-cart-feedback.css',
      array( 'beslock-main-style', 'beslock-header-component' ),
      filemtime( $add_to_cart_feedback_css )
    );
  }

  $add_to_cart_feedback_js = $theme_dir_path . '/assets/js/add-to-cart-feedback.js';
  if ( file_exists( $add_to_cart_feedback_js ) ) {
    wp_enqueue_script(
      'beslock-add-to-cart-feedback',
      $theme_dir_uri . '/assets/js/add-to-cart-feedback.js',
      array( 'jquery', 'wc-add-to-cart' ),
      filemtime( $add_to_cart_feedback_js ),
      true
    );

    wp_add_inline_script(
      'beslock-add-to-cart-feedback',
      'window.BESLOCK_ADD_TO_CART = ' . wp_json_encode(
        array(
          'cartUrl'            => function_exists( 'wc_get_cart_url' ) ? wc_get_cart_url() : home_url( '/carrito/' ),
          'wcAjaxUrl'          => class_exists( 'WC_AJAX' ) ? WC_AJAX::get_endpoint( '%%endpoint%%' ) : '',
          'isCart'             => function_exists( 'is_cart' ) && is_cart(),
        )
      ) . ';',
      'before'
    );
  }

  $hero_telemetry_config = array(
    'enabled'  => (bool) apply_filters( 'beslock_hero_startup_telemetry_enabled', false ),
    'endpoint' => esc_url_raw( rest_url( 'beslock/v1/hero-startup' ) ),
  );

  wp_add_inline_script(
    'beslock-main-js',
    'window.beslockHeroTelemetry = ' . wp_json_encode( $hero_telemetry_config ) . ';',
    'before'
  );

  $product_card_component_js = $theme_dir_path . '/assets/js/components/product-card.js';
  if ( file_exists( $product_card_component_js ) ) {
    wp_enqueue_script(
      'beslock-product-card-component',
      $theme_dir_uri . '/assets/js/components/product-card.js',
      [ 'beslock-main-js' ],
      filemtime( $product_card_component_js ),
      true
    );
  }

  $fix_placeholder_js = $theme_dir_path . '/assets/js/fix-placeholder.js';
  if ( file_exists( $fix_placeholder_js ) ) {
    wp_enqueue_script( 'beslock-fix-placeholder-js', $theme_dir_uri . '/assets/js/fix-placeholder.js', array( 'beslock-main-js' ), filemtime( $fix_placeholder_js ), true );
  }

  $menu_js_path = $theme_dir_path . '/assets/js/menu-products-mobile.js';
  $ver_menu_js = file_exists( $menu_js_path ) ? filemtime( $menu_js_path ) : null;

  wp_enqueue_script(
    'beslock-menu-products-mobile-js',
    $theme_dir_uri . '/assets/js/menu-products-mobile.js',
    [ 'beslock-main-js' ],
    $ver_menu_js,
    true
  );

  $order_lookup_js = $theme_dir_path . '/assets/js/order-lookup.js';
  if ( file_exists( $order_lookup_js ) ) {
    wp_enqueue_script(
      'beslock-order-lookup-js',
      $theme_dir_uri . '/assets/js/order-lookup.js',
      [ 'beslock-main-js', 'beslock-menu-products-mobile-js' ],
      filemtime( $order_lookup_js ),
      true
    );
  }

  $models_js_path = $theme_dir_path . '/assets/js/models-mobile.js';
  $ver_models_js = file_exists( $models_js_path ) ? filemtime( $models_js_path ) : null;

  wp_enqueue_script(
    'beslock-models-mobile-js',
    $theme_dir_uri . '/assets/js/models-mobile.js',
    [ 'beslock-main-js', 'beslock-menu-products-mobile-js' ],
    $ver_models_js,
    true
  );

  $manuals_viewer_js = $theme_dir_path . '/assets/js/manuals-viewer.js';
  if ( file_exists( $manuals_viewer_js ) ) {
    wp_enqueue_script(
      'beslock-manuals-viewer-js',
      $theme_dir_uri . '/assets/js/manuals-viewer.js',
      [ 'beslock-main-js', 'beslock-menu-products-mobile-js' ],
      filemtime( $manuals_viewer_js ),
      true
    );

    $manuals_cache_bust = filemtime( $manuals_viewer_js );
    $manuals_dist_dir = $theme_dir_path . '/dist/manuals';
    $manuals_manifest_candidates = array(
      $manuals_dist_dir . '/index.json',
      $manuals_dist_dir . '/export_summary.json',
    );

    foreach ( $manuals_manifest_candidates as $manuals_manifest ) {
      if ( file_exists( $manuals_manifest ) ) {
        $manuals_cache_bust = max( $manuals_cache_bust, filemtime( $manuals_manifest ) );
      }
    }

    $manuals_product_manifests = glob( $manuals_dist_dir . '/products/*.json' );
    if ( is_array( $manuals_product_manifests ) ) {
      foreach ( $manuals_product_manifests as $manuals_product_manifest ) {
        if ( is_file( $manuals_product_manifest ) ) {
          $manuals_cache_bust = max( $manuals_cache_bust, filemtime( $manuals_product_manifest ) );
        }
      }
    }

    $manuals_config = array(
      'baseUrl'    => esc_url_raw( $theme_dir_uri . '/dist/manuals' ),
      'cacheBust' => (string) $manuals_cache_bust,
    );

    wp_add_inline_script(
      'beslock-manuals-viewer-js',
      'window.BESLOCK_MANUALS_BASE_URL = ' . wp_json_encode( $manuals_config['baseUrl'] ) . '; window.BESLOCK_MANUALS_CONFIG = ' . wp_json_encode( $manuals_config ) . ';',
      'before'
    );
  }

  $support_drawer_js = $theme_dir_path . '/assets/js/support-drawer.js';
  if ( file_exists( $support_drawer_js ) ) {
    wp_enqueue_script(
      'beslock-support-drawer-js',
      $theme_dir_uri . '/assets/js/support-drawer.js',
      [ 'beslock-main-js', 'beslock-menu-products-mobile-js' ],
      filemtime( $support_drawer_js ),
      true
    );
  }

  $widgets_css = $theme_dir_path . '/assets/css/product-widgets.css';
  if ( $is_product_page && file_exists( $widgets_css ) ) {
    wp_enqueue_style( 'beslock-product-widgets', $theme_dir_uri . '/assets/css/product-widgets.css', [ 'beslock-main-style' ], filemtime( $widgets_css ) );
  }

  $product_page_css = $theme_dir_path . '/assets/css/product-page.css';
  if ( $is_product_page && file_exists( $product_page_css ) ) {
    wp_enqueue_style( 'beslock-product-page', $theme_dir_uri . '/assets/css/product-page.css', [ 'beslock-main-style' ], filemtime( $product_page_css ) );
  }

  $product_tabs_css = $theme_dir_path . '/assets/css/product-tabs.css';
  if ( $is_product_page && file_exists( $product_tabs_css ) ) {
    wp_enqueue_style( 'beslock-product-tabs', $theme_dir_uri . '/assets/css/product-tabs.css', [ 'beslock-product-page' ], filemtime( $product_tabs_css ) );
  }
  $product_tabs_js = $theme_dir_path . '/assets/js/product-tabs.js';
  if ( $is_product_page && file_exists( $product_tabs_js ) ) {
    wp_enqueue_script( 'beslock-product-tabs-js', $theme_dir_uri . '/assets/js/product-tabs.js', [ 'beslock-main-js' ], filemtime( $product_tabs_js ), true );
  }

  $qty_js = $theme_dir_path . '/assets/js/product-quantity-controls.js';
  if ( $is_product_page && file_exists( $qty_js ) ) {
    wp_enqueue_script( 'beslock-product-qty-js', $theme_dir_uri . '/assets/js/product-quantity-controls.js', [ 'beslock-main-js' ], filemtime( $qty_js ), true );
  }

  $product_pager_reel_js = $theme_dir_path . '/assets/js/product-pager-reel.js';
  if ( $is_product_page && file_exists( $product_pager_reel_js ) ) {
    wp_enqueue_script( 'beslock-product-pager-reel-js', $theme_dir_uri . '/assets/js/product-pager-reel.js', [ 'beslock-main-js' ], filemtime( $product_pager_reel_js ), true );
  }

  /* Badge injector removed to avoid duplicate client-side injections.
     Server-side rendering in template-parts/product-card.php provides the badge. */

  $product_rotator_css = $theme_dir_path . '/assets/css/product-rotator.css';
  if ( file_exists( $product_rotator_css ) ) {
    wp_enqueue_style( 'beslock-product-rotator', $theme_dir_uri . '/assets/css/product-rotator.css', [ 'beslock-main-style' ], filemtime( $product_rotator_css ) );
  }

  $product_rotator_js = $theme_dir_path . '/assets/js/product-rotator.js';
  if ( file_exists( $product_rotator_js ) ) {
    wp_enqueue_script( 'beslock-product-rotator-js', $theme_dir_uri . '/assets/js/product-rotator.js', [ 'beslock-main-js' ], filemtime( $product_rotator_js ), true );
  }

  $product_card_alt = $theme_dir_path . '/assets/css/product-card-alt.css';
  if ( file_exists( $product_card_alt ) ) {
    if ( function_exists( 'is_cart' ) && is_cart() ) {
      wp_enqueue_style( 'beslock-product-card-alt', $theme_dir_uri . '/assets/css/product-card-alt.css', array( 'beslock-main-style', 'beslock-product-rotator' ), filemtime( $product_card_alt ) );
    }
  }

  $product_card_fade = $theme_dir_path . '/assets/css/product-card-fade.css';
  if ( file_exists( $product_card_fade ) ) {
    if ( function_exists( 'is_cart' ) && is_cart() ) {
      wp_enqueue_style( 'beslock-product-card-fade', $theme_dir_uri . '/assets/css/product-card-fade.css', array( 'beslock-main-style' ), filemtime( $product_card_fade ) );
    }
  }

  $reel_css = $theme_dir_path . '/assets/css/product-gallery-reel.css';
  if ( $is_product_page && file_exists( $reel_css ) ) {
    wp_enqueue_style( 'beslock-product-gallery-reel', $theme_dir_uri . '/assets/css/product-gallery-reel.css', [ 'beslock-main-style' ], filemtime( $reel_css ) );
  }
  $reel_js = $theme_dir_path . '/assets/js/product-gallery-reel.js';
  if ( $is_product_page && file_exists( $reel_js ) ) {
    wp_enqueue_script( 'beslock-product-gallery-reel-js', $theme_dir_uri . '/assets/js/product-gallery-reel.js', [ 'beslock-main-js' ], filemtime( $reel_js ), true );
  }

  $header_state_js = $theme_dir_path . '/assets/js/header-state.js';
  $ver_header_state_js = file_exists( $header_state_js ) ? filemtime( $header_state_js ) : null;
  wp_enqueue_script(
    'beslock-header-state',
    $theme_dir_uri . '/assets/js/header-state.js',
    [],
    $ver_header_state_js,
    true
  );

  $header_state_css = $theme_dir_path . '/assets/css/header-state.css';
  if ( file_exists( $header_state_css ) ) {
    wp_enqueue_style( 'beslock-header-state-css', $theme_dir_uri . '/assets/css/header-state.css', [ 'beslock-main-style' ], filemtime( $header_state_css ) );
  }

  $frontpage_motion_css = $theme_dir_path . '/assets/css/frontpage-motion.css';
  if ( $is_front_page && file_exists( $frontpage_motion_css ) ) {
    wp_enqueue_style( 'beslock-frontpage-motion', $theme_dir_uri . '/assets/css/frontpage-motion.css', [ 'beslock-extra-style' ], filemtime( $frontpage_motion_css ) );
  }

  $frontpage_motion_js = $theme_dir_path . '/assets/js/frontpage-motion.js';
  if ( $is_front_page && file_exists( $frontpage_motion_js ) ) {
    wp_enqueue_script( 'beslock-frontpage-motion-js', $theme_dir_uri . '/assets/js/frontpage-motion.js', [ 'beslock-main-js' ], filemtime( $frontpage_motion_js ), true );
  }

}, 10 );

add_action( 'wp_head', function() {
  if ( is_admin() || ! function_exists( 'is_product' ) || ! is_product() ) {
    return;
  }
  ?>
  <script>
  (function(){
    try {
      var direction = window.sessionStorage && window.sessionStorage.getItem('beslockProductPagerDirection');
      if (direction !== 'prev' && direction !== 'next') return;
      var root = document.documentElement;
      root.classList.add('product-reel-pending', 'product-reel-pending--' + direction);
      window.setTimeout(function(){
        root.classList.remove('product-reel-pending', 'product-reel-pending--prev', 'product-reel-pending--next');
      }, 1800);
    } catch (error) {}
  })();
  </script>
  <?php
}, 0 );

// Inline early-capture script: prevent navigation to raw uploads image URLs and open overlay
add_action( 'wp_head', function(){
  ?>
  <script>
  (function(){
    function openOverlay(src){
      try{
        if(window.__beslock_inline_overlay) return;
        var overlay = document.createElement('div');
        overlay.id = 'beslock-inline-overlay';
        overlay.style.position = 'fixed';
        overlay.style.left = '0';
        overlay.style.top = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.background = 'rgba(8,8,8,0.95)';
        overlay.style.display = 'flex';
        overlay.style.alignItems = 'center';
        overlay.style.justifyContent = 'center';
        overlay.style.zIndex = 2147483647;
        overlay.style.cursor = 'zoom-out';

        var img = document.createElement('img');
        img.src = src;
        img.alt = '';
        img.style.maxWidth = '100%';
        img.style.maxHeight = '100%';
        img.style.objectFit = 'contain';

        var btn = document.createElement('button');
        btn.setAttribute('type','button');
        btn.setAttribute('aria-label','Close image');
        btn.className = 'beslock-inline-close';
        btn.innerHTML = '\u00D7';
        btn.style.position = 'absolute';
        btn.style.top = '12px';
        btn.style.right = '12px';
        btn.style.width = '44px';
        btn.style.height = '44px';
        btn.style.border = '0';
        btn.style.borderRadius = '22px';
        btn.style.background = 'rgba(0,0,0,0.5)';
        btn.style.color = '#fff';
        btn.style.fontSize = '28px';
        btn.style.lineHeight = '44px';
        btn.style.textAlign = 'center';
        btn.style.cursor = 'pointer';
        btn.style.zIndex = 2147483650;

        btn.addEventListener('click', function(e){
          e.stopPropagation();
          try{ if(overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay); }catch(err){}
          window.__beslock_inline_overlay = null;
          document.documentElement.style.overflow = '';
          document.body.style.overflow = '';
          document.removeEventListener('keydown', onKey);
        }, false);

        overlay.style.position = 'fixed';
        overlay.style.padding = '24px';

        overlay.appendChild(btn);
        overlay.appendChild(img);

        function close(){
          try{ if(overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay); }catch(e){}
          window.__beslock_inline_overlay = null;
          document.documentElement.style.overflow = '';
          document.body.style.overflow = '';
          document.removeEventListener('keydown', onKey);
        }

        function onKey(e){ if(e.key === 'Escape' || e.keyCode === 27) close(); }

        overlay.addEventListener('click', function(e){
          var actionable = e.target.closest && e.target.closest('a, button');
          if(actionable) return;
          close();
        }, { capture: true });

        document.documentElement.style.overflow = 'hidden';
        document.body.style.overflow = 'hidden';
        document.body.appendChild(overlay);
        window.__beslock_inline_overlay = overlay;
        document.addEventListener('keydown', onKey);
      }catch(e){ }
    }

    function inertAnchors(){
      try{
        var anchors = document.querySelectorAll('.woocommerce div.product div.images a');
        anchors.forEach(function(a){
          try{
            var href = a.getAttribute('href') || a.href || '';
            if(href && href.indexOf('/wp-content/uploads/') !== -1){
              a.setAttribute('data-beslock-inert','1');
              try{ a.removeAttribute('href'); }catch(e){}
              a.style.cursor = 'default';
            }
          }catch(e){}
        });
      }catch(e){}
    }

    function onPointer(e){
      try{
        var a = e.target && e.target.closest ? e.target.closest('a') : null;
        if(!a) return;
        if(!(a.closest && a.closest('.woocommerce div.product'))) return;
        var href = a.getAttribute('href') || a.href || '';
        if(href && href.indexOf('/wp-content/uploads/') !== -1){
          e.preventDefault();
          e.stopImmediatePropagation();
          try{ a.removeAttribute('href'); }catch(e){}
          openOverlay(href);
        }
      }catch(err){}
    }

    if(document.readyState === 'loading'){
      document.addEventListener('DOMContentLoaded', inertAnchors);
    } else { inertAnchors(); }

    document.addEventListener('pointerdown', onPointer, true);
    document.addEventListener('touchstart', onPointer, true);

    try{
      var prod = document.querySelector('.woocommerce div.product');
      if(prod && window.MutationObserver){
        var mo = new MutationObserver(function(){ inertAnchors(); });
        mo.observe(prod, { childList:true, subtree:true, attributes:true });
      }
    }catch(e){}
  })();
  </script>
  <?php
}, 1 );

add_action( 'wp_enqueue_scripts', function() {
  $css_file = get_stylesheet_directory() . '/assets/css/wc-scope-fix.css';
  if ( file_exists( $css_file ) ) {
    wp_enqueue_style( 'beslock-wc-scope-fix', get_stylesheet_directory_uri() . '/assets/css/wc-scope-fix.css', [ 'beslock-main-style' ], filemtime( $css_file ) );
  }
}, 20 );

add_action( 'wp_enqueue_scripts', function() {
  if ( ! function_exists( 'is_cart' ) || ! is_cart() ) {
    return;
  }

  $theme_dir_path = get_stylesheet_directory();
  $theme_dir_uri  = get_stylesheet_directory_uri();

  $cart_css = $theme_dir_path . '/assets/css/beslock-cart.css';
  if ( file_exists( $cart_css ) ) {
    wp_enqueue_style(
      'beslock-cart',
      $theme_dir_uri . '/assets/css/beslock-cart.css',
      [ 'beslock-main-style', 'beslock-wc-scope-fix' ],
      filemtime( $cart_css )
    );
  }

  $cart_js = $theme_dir_path . '/assets/js/cart-quantity-controls.js';
  if ( file_exists( $cart_js ) ) {
    wp_enqueue_script(
      'beslock-cart-quantity-controls',
      $theme_dir_uri . '/assets/js/cart-quantity-controls.js',
      [],
      filemtime( $cart_js ),
      true
    );
  }
}, 30 );

add_action( 'wp_enqueue_scripts', function() {
  if ( ! function_exists( 'is_checkout' ) || ! is_checkout() ) {
    return;
  }

  if ( function_exists( 'is_order_received_page' ) && is_order_received_page() ) {
    return;
  }

  $theme_dir_path = get_stylesheet_directory();
  $theme_dir_uri  = get_stylesheet_directory_uri();

  $checkout_css = $theme_dir_path . '/assets/css/beslock-checkout.css';
  if ( file_exists( $checkout_css ) ) {
    wp_enqueue_style(
      'beslock-checkout',
      $theme_dir_uri . '/assets/css/beslock-checkout.css',
      [ 'beslock-main-style', 'beslock-wc-scope-fix' ],
      filemtime( $checkout_css )
    );
  }

  $checkout_js = $theme_dir_path . '/assets/js/beslock-checkout.js';
  if ( file_exists( $checkout_js ) ) {
    wp_enqueue_script(
      'beslock-checkout',
      $theme_dir_uri . '/assets/js/beslock-checkout.js',
      [],
      filemtime( $checkout_js ),
      true
    );

    $shipping_destination = function_exists( 'beslock_format_cart_shipping_destination' ) ? beslock_format_cart_shipping_destination() : '';
    $customer             = function_exists( 'WC' ) && WC()->customer ? WC()->customer : null;

    wp_add_inline_script(
      'beslock-checkout',
      'window.BESLOCK_CHECKOUT = ' . wp_json_encode(
        array(
          'cartUrl'             => function_exists( 'wc_get_cart_url' ) ? wc_get_cart_url() : home_url( '/carrito/' ),
          'shippingDestination' => $shipping_destination,
          'contact'             => array(
            'firstName' => $customer ? $customer->get_shipping_first_name() : '',
            'lastName'  => $customer ? $customer->get_shipping_last_name() : '',
            'phone'     => $customer ? $customer->get_billing_phone() : '',
            'email'     => $customer ? $customer->get_billing_email() : '',
          ),
          'labels'              => array(
            'contactTitle'     => __( 'Datos de contacto', 'beslock-custom' ),
            'firstName'        => __( 'Nombre', 'beslock-custom' ),
            'lastName'         => __( 'Apellido', 'beslock-custom' ),
            'phone'            => __( 'Celular', 'beslock-custom' ),
            'email'            => __( 'Correo electrónico', 'beslock-custom' ),
            'alternateContactTitle' => __( 'Añadir otro contacto para el envío', 'beslock-custom' ),
            'alternateContactHelp' => __( 'Úsalo si otra persona recibirá o coordinará la entrega.', 'beslock-custom' ),
            'optionalLabel'    => __( 'Opcional', 'beslock-custom' ),
            'orderNote'        => __( 'Añadir una nota a tu pedido', 'beslock-custom' ),
            'orderNoteHelp'    => __( 'Puedes contarnos detalles de entrega, instalación o coordinación.', 'beslock-custom' ),
            'shippingTitle'    => __( 'Datos de envío', 'beslock-custom' ),
            'shippingFallback' => __( 'La entrega se tomará de la dirección confirmada en el carrito.', 'beslock-custom' ),
            'editShipping'     => __( 'Editar en carrito', 'beslock-custom' ),
          ),
        )
      ) . ';',
      'before'
    );
  }
}, 31 );

// Dequeue Kadence styles late to allow parent enqueues first
add_action( 'wp_enqueue_scripts', function() {
  if ( is_admin() ) { return; }
  global $wp_styles;
  if ( empty( $wp_styles ) || empty( $wp_styles->registered ) ) { return; }
  foreach ( $wp_styles->registered as $handle => $data ) {
    if ( strpos( $handle, 'kadence' ) === 0 ) {
      wp_dequeue_style( $handle );
      wp_deregister_style( $handle );
    }
  }
  if ( wp_style_is( 'kadence-parent-style', 'enqueued' ) || wp_style_is( 'kadence-parent-style', 'registered' ) ) {
    wp_dequeue_style( 'kadence-parent-style' );
    wp_deregister_style( 'kadence-parent-style' );
  }
  $extra_handles = [ 'global-styles', 'classic-theme-styles', 'wp-block-library-theme', 'wp-block-library' ];
  foreach ( $extra_handles as $h ) {
    if ( wp_style_is( $h, 'enqueued' ) || wp_style_is( $h, 'registered' ) ) {
      wp_dequeue_style( $h );
      wp_deregister_style( $h );
    }
  }

}, 100 );
