<?php

declare(strict_types=1);

if (! defined('ABSPATH')) {
    exit;
}

add_action('wp_enqueue_scripts', static function (): void {
    $theme = wp_get_theme();

    wp_enqueue_style(
        'beslock-custom-style',
        get_stylesheet_uri(),
        [],
        $theme->get('Version') ?: null
    );

    wp_enqueue_script(
        'beslock-custom-theme',
        get_stylesheet_directory_uri() . '/assets/js/theme.js',
        [],
        $theme->get('Version') ?: null,
        true
    );
});

add_action('after_setup_theme', static function (): void {
    add_theme_support('woocommerce');
});
