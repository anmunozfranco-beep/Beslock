<?php

if (! defined('ABSPATH')) {
    exit;
}

/**
 * Shared helpers for product and image loading.
 */
class IPCL_Utils
{
    /**
     * Build a default operation result payload.
     *
     * @return array<string,mixed>
     */
    public static function make_result()
    {
        return array(
            'imported_products' => 0,
            'updated_products' => 0,
            'skipped_products' => 0,
            'imported_images' => 0,
            'missing_images' => 0,
            'reused_attachments' => 0,
            'logs' => array(),
        );
    }

    /**
     * Append log line.
     *
     * @param array<string,mixed> $result
     * @param string              $level
     * @param string              $message
     */
    public static function log(&$result, $level, $message)
    {
        $result['logs'][] = sprintf('[%s] %s', strtoupper($level), $message);
    }

    /**
     * Resolve plugins_ZIP directory in wp-content.
     * Auto-creates if missing.
     *
     * @return string
     */
    public static function get_plugins_zip_dir()
    {
        $path = wp_normalize_path(trailingslashit(WP_CONTENT_DIR) . 'plugins_ZIP');
        
        if (!is_dir($path)) {
            wp_mkdir_p($path);
        }
        
        return $path;
    }

    /**
     * Shared JSON snapshot path at wp-content/plugins_ZIP/products_thrut.json
     *
     * @return string
     */
    public static function get_products_json_path()
    {
        $default = wp_normalize_path(trailingslashit(self::get_plugins_zip_dir()) . 'products_thrut.json');

        return (string) apply_filters('ipcl_loader_json_path', $default);
    }

    /**
     * Image root resolved from active theme directory.
     *
     * @return string
     */
    public static function get_image_root_path()
    {
        $default = wp_normalize_path(trailingslashit(get_stylesheet_directory()) . 'assets/images');

        return (string) apply_filters('ipcl_loader_image_root_path', $default);
    }

    /**
     * Find a product by slug (post_name) only.
     *
     * @param array<string,mixed> $entry
     * @return WC_Product|false
     */
    public static function find_matching_product($entry)
    {
        $slug = '';
        if (is_array($entry) && ! empty($entry['slug'])) {
            $slug = sanitize_title((string) $entry['slug']);
        }

        if ($slug === '') {
            return false;
        }

        $post = get_page_by_path($slug, OBJECT, 'product');
        if (! ($post instanceof WP_Post)) {
            return false;
        }

        $product = wc_get_product((int) $post->ID);
        if ($product instanceof WC_Product) {
            return $product;
        }

        return false;
    }

    /**
     * Ensure taxonomy terms by name and return IDs.
     *
     * @param array<int,string> $names
     * @param string            $taxonomy
     * @return array<int,int>
     */
    public static function ensure_terms($names, $taxonomy)
    {
        $term_ids = array();

        foreach ($names as $raw_name) {
            $name = trim((string) $raw_name);
            if ($name === '') {
                continue;
            }

            $existing = term_exists($name, $taxonomy);

            if (is_array($existing) && ! empty($existing['term_id'])) {
                $term_ids[] = (int) $existing['term_id'];
                continue;
            }

            $inserted = wp_insert_term($name, $taxonomy);
            if (is_wp_error($inserted) || empty($inserted['term_id'])) {
                continue;
            }

            $term_ids[] = (int) $inserted['term_id'];
        }

        return array_values(array_unique($term_ids));
    }

    /**
     * Find an attachment by source filename.
     *
     * @param string $filename
     * @return int
     */
    public static function find_attachment_by_filename($filename)
    {
        $filename = basename((string) $filename);
        if ($filename === '') {
            return 0;
        }

        $by_source = get_posts(
            array(
                'post_type' => 'attachment',
                'post_status' => 'inherit',
                'posts_per_page' => 1,
                'fields' => 'ids',
                'meta_key' => '_ipcl_source_filename',
                'meta_value' => $filename,
                'no_found_rows' => true,
            )
        );

        if (! empty($by_source[0])) {
            return (int) $by_source[0];
        }

        $by_attached_file = get_posts(
            array(
                'post_type' => 'attachment',
                'post_status' => 'inherit',
                'posts_per_page' => 1,
                'fields' => 'ids',
                'meta_query' => array(
                    array(
                        'key' => '_wp_attached_file',
                        'value' => $filename,
                        'compare' => 'LIKE',
                    ),
                ),
                'no_found_rows' => true,
            )
        );

        if (! empty($by_attached_file[0])) {
            return (int) $by_attached_file[0];
        }

        return 0;
    }

    /**
     * Keep only allowed product statuses.
     *
     * @param string $status
     * @return string
     */
    public static function normalize_status($status)
    {
        $allowed = array('publish', 'draft', 'pending', 'private');
        $status = sanitize_key((string) $status);

        if (in_array($status, $allowed, true)) {
            return $status;
        }

        return 'publish';
    }
}
