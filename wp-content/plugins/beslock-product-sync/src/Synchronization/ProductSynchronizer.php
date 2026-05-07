<?php

declare(strict_types=1);

namespace Beslock\ProductSync\Synchronization;

use Beslock\ProductSync\Data\ProductRepository;
use Beslock\ProductSync\Presentation\ProductMapper;

final class ProductSynchronizer
{
    public function __construct(
        private ProductRepository $repository,
        private ProductMapper $mapper
    ) {
    }

    /**
     * Register the manual synchronization action.
     *
     * Trigger with do_action('beslock_sync_products') directly or from a scheduled job.
     */
    public function register(): void
    {
        add_action('beslock_sync_products', [$this, 'sync']);
    }

    public function sync(): void
    {
        foreach ($this->repository->all() as $rawProduct) {
            $mapped = $this->mapper->map(is_array($rawProduct) ? $rawProduct : []);
            if ($mapped['title'] === '' || $mapped['slug'] === '') {
                continue;
            }

            $existing = get_posts([
                'name' => $mapped['slug'],
                'post_type' => 'product',
                'post_status' => 'any',
                'posts_per_page' => 1,
                'fields' => 'ids',
                'no_found_rows' => true,
            ]);
            $postId = isset($existing[0]) ? (int) $existing[0] : 0;

            $result = wp_insert_post([
                'ID' => $postId,
                'post_title' => $mapped['title'],
                'post_name' => $mapped['slug'],
                'post_content' => $mapped['description'],
                'post_status' => 'publish',
                'post_type' => 'product',
            ]);

            if (is_wp_error($result) || $result <= 0) {
                continue;
            }
            $postId = (int) $result;

            $wcProduct = wc_get_product($postId);
            if (! $wcProduct) {
                error_log(sprintf('Beslock product sync: unable to load WooCommerce product for post ID %d', $postId));
                continue;
            }

            if ($mapped['price'] !== '') {
                $wcProduct->set_regular_price($mapped['price']);
            }

            if ($wcProduct->save() <= 0) {
                error_log(sprintf('Beslock product sync: unable to persist WooCommerce product for post ID %d', $postId));
            }
        }
    }
}
