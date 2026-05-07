<?php
/**
 * Plugin Name: BESLOCK Product Sync
 * Version: 1.0.0
 */

declare(strict_types=1);

if (! defined('ABSPATH')) {
    exit;
}

require_once __DIR__ . '/src/Data/ProductRepository.php';
require_once __DIR__ . '/src/Presentation/ProductMapper.php';
require_once __DIR__ . '/src/Synchronization/ProductSynchronizer.php';

add_action('init', static function (): void {
    $sync = new Beslock\ProductSync\Synchronization\ProductSynchronizer(
        new Beslock\ProductSync\Data\ProductRepository(WP_CONTENT_DIR . '/../data/products.json'),
        new Beslock\ProductSync\Presentation\ProductMapper()
    );

    $sync->register();
});
