<?php

if (! defined('ABSPATH')) {
    exit;
}

/**
 * Creates or updates WooCommerce products from normalized entries.
 * Slug is the only unique key for matching and idempotency.
 */
class IPCL_Product_Loader
{
    /**
     * @param array<int,array<string,mixed>> $entries
     * @return array<string,mixed>
     */
    public function load($entries)
    {
        $result = IPCL_Utils::make_result();

        if (! is_array($entries)) {
            IPCL_Utils::log($result, 'error', 'Products payload is invalid. Expected array of entries.');
            return $result;
        }

        $seen_slugs = array();

        foreach ($entries as $entry) {
            if (! is_array($entry)) {
                $result['skipped_products']++;
                IPCL_Utils::log($result, 'warning', 'Skipped malformed product entry.');
                continue;
            }

            $entry = wp_parse_args(
                $entry,
                array(
                    'product_id' => 0,
                    'slug' => '',
                    'sku' => '',
                    'name' => '',
                    'price' => '',
                    'short_description' => '',
                    'description' => '',
                    'categories' => array(),
                    'tags' => array(),
                    'status' => 'publish',
                    '_present' => array(),
                )
            );

            $slug = sanitize_title((string) $entry['slug']);
            if ($slug === '') {
                $result['skipped_products']++;
                IPCL_Utils::log($result, 'warning', 'Skipped product entry with empty slug.');
                continue;
            }

            if (isset($seen_slugs[$slug])) {
                $result['skipped_products']++;
                IPCL_Utils::log($result, 'warning', sprintf('Skipped duplicate slug entry in JSON: %s', $slug));
                continue;
            }
            $seen_slugs[$slug] = true;

            $matched = IPCL_Utils::find_matching_product(array('slug' => $slug));
            $is_new = ! ($matched instanceof WC_Product);

            if ($is_new) {
                $product = new WC_Product_Simple();
                $product->set_slug($slug);
            } else {
                $product = $matched;
            }

            if ($entry['name'] === '' && $is_new) {
                $result['skipped_products']++;
                IPCL_Utils::log($result, 'warning', sprintf('Skipped new product with no name for slug %s.', $slug));
                continue;
            }

            if (! $this->apply_supported_fields($product, $entry, $result)) {
                $result['skipped_products']++;
                continue;
            }

            $saved_id = $product->save();
            if (empty($saved_id)) {
                $result['skipped_products']++;
                IPCL_Utils::log($result, 'warning', sprintf('Skipped slug %s because product save returned empty ID.', $slug));
                continue;
            }

            if ($is_new) {
                $result['imported_products']++;
                IPCL_Utils::log(
                    $result,
                    'info',
                    sprintf('Created product ID %d with slug %s.', (int) $saved_id, $slug)
                );
            } else {
                $result['updated_products']++;
                IPCL_Utils::log(
                    $result,
                    'info',
                    sprintf('Updated product ID %d with slug %s.', (int) $saved_id, $slug)
                );
            }
        }

        return $result;
    }

    /**
     * Apply only supported fields.
     *
     * @param WC_Product          $product
     * @param array<string,mixed> $entry
     * @param array<string,mixed> $result
     * @return bool
     */
    protected function apply_supported_fields($product, $entry, &$result)
    {
        $present = isset($entry['_present']) && is_array($entry['_present']) ? $entry['_present'] : array();

        if (! empty($present['name']) && $entry['name'] !== '') {
            $product->set_name($entry['name']);
        }

        if (! empty($present['slug']) && $entry['slug'] !== '') {
            $product->set_slug(sanitize_title((string) $entry['slug']));
        }

        if (! empty($present['sku']) && $entry['sku'] !== '') {
            $existing_id = wc_get_product_id_by_sku($entry['sku']);
            if (! empty($existing_id) && (int) $existing_id !== (int) $product->get_id()) {
                IPCL_Utils::log(
                    $result,
                    'warning',
                    sprintf('Skipped SKU update for slug %s because SKU %s belongs to product ID %d.', (string) $product->get_slug(), $entry['sku'], (int) $existing_id)
                );
            } else {
                $product->set_sku($entry['sku']);
            }
        }

        if (! empty($present['price']) && $entry['price'] !== '') {
            $product->set_regular_price($entry['price']);
            $product->set_price($entry['price']);
        }

        if (! empty($present['short_description'])) {
            $product->set_short_description((string) $entry['short_description']);
        }

        if (! empty($present['description'])) {
            $product->set_description((string) $entry['description']);
        }

        if (! empty($present['status'])) {
            $product->set_status(IPCL_Utils::normalize_status($entry['status']));
        }

        if (! empty($present['categories'])) {
            $category_ids = IPCL_Utils::ensure_terms($entry['categories'], 'product_cat');
            $product->set_category_ids($category_ids);
        }

        if (! empty($present['tags'])) {
            $tag_ids = IPCL_Utils::ensure_terms($entry['tags'], 'product_tag');
            $product->set_tag_ids($tag_ids);
        }

        return true;
    }
}
