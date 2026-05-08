<?php

if (! defined('ABSPATH')) {
    exit;
}

/**
 * Loads local product images into media library and assigns them to products.
 */
class IPCL_Image_Loader
{
    /**
     * @var string
     */
    protected $image_root;

    /**
     * @param string $image_root
     */
    public function __construct($image_root)
    {
        $this->image_root = rtrim((string) $image_root, '/');
    }

    /**
     * @return string
     */
    public function get_image_root()
    {
        return $this->image_root;
    }

    /**
     * @param array<int,array<string,mixed>> $entries
     * @return array<string,mixed>
     */
    public function load($entries)
    {
        $result = IPCL_Utils::make_result();

        if (! is_array($entries)) {
            IPCL_Utils::log($result, 'error', 'Images payload is invalid. Expected array of entries.');
            return $result;
        }

        if (! is_dir($this->image_root)) {
            IPCL_Utils::log($result, 'error', sprintf('Image root directory not found: %s', $this->image_root));
            return $result;
        }

        foreach ($entries as $entry) {
            if (! is_array($entry)) {
                $result['skipped_products']++;
                IPCL_Utils::log($result, 'warning', 'Skipped malformed entry while loading images.');
                continue;
            }

            $entry = wp_parse_args(
                $entry,
                array(
                    'product_id' => 0,
                    'slug' => '',
                    'sku' => '',
                )
            );

            $product = IPCL_Utils::find_matching_product($entry);
            if (! ($product instanceof WC_Product)) {
                $result['skipped_products']++;
                IPCL_Utils::log($result, 'warning', 'Skipped image load: matching product not found.');
                continue;
            }

            $slug = $product->get_slug();
            if ($slug === '') {
                $result['skipped_products']++;
                IPCL_Utils::log($result, 'warning', sprintf('Skipped image load for product ID %d: empty slug.', (int) $product->get_id()));
                continue;
            }

            $this->load_images_for_product($product, $slug, $result);
        }

        return $result;
    }

    /**
     * @param WC_Product          $product
     * @param string              $slug
     * @param array<string,mixed> $result
     */
    protected function load_images_for_product($product, $slug, &$result)
    {
        $product_id = (int) $product->get_id();
        $primary_file = $this->image_root . '/' . $slug . '_.webp';

        $featured_id = 0;

        if (file_exists($primary_file) && is_readable($primary_file)) {
            $featured_id = $this->resolve_attachment_id($primary_file, $product_id, $result);
            if (! empty($featured_id)) {
                set_post_thumbnail($product_id, $featured_id);
                IPCL_Utils::log($result, 'info', sprintf('Set featured image for product ID %d (%s).', $product_id, basename($primary_file)));
            }
        } else {
            $result['missing_images']++;
            IPCL_Utils::log($result, 'warning', sprintf('Missing featured image for %s: %s', $slug, basename($primary_file)));
        }

        $gallery_pattern = $this->image_root . '/' . $slug . '_*.webp';
        $gallery_files = glob($gallery_pattern);

        if (! is_array($gallery_files)) {
            $gallery_files = array();
        }

        $gallery_files = array_filter(
            $gallery_files,
            function ($file) use ($slug) {
                return basename($file) !== ($slug . '_.webp');
            }
        );

        natcasesort($gallery_files);

        $gallery_ids = array();

        foreach ($gallery_files as $gallery_file) {
            if (! file_exists($gallery_file) || ! is_readable($gallery_file)) {
                $result['missing_images']++;
                IPCL_Utils::log($result, 'warning', sprintf('Missing gallery image for %s: %s', $slug, basename((string) $gallery_file)));
                continue;
            }

            $gallery_id = $this->resolve_attachment_id($gallery_file, $product_id, $result);
            if (! empty($gallery_id) && (int) $gallery_id !== (int) $featured_id) {
                $gallery_ids[] = (int) $gallery_id;
            }
        }

        $gallery_ids = array_values(array_unique($gallery_ids));
        update_post_meta($product_id, '_product_image_gallery', implode(',', $gallery_ids));

        IPCL_Utils::log(
            $result,
            'info',
            sprintf('Updated gallery for product ID %d with %d image(s).', $product_id, count($gallery_ids))
        );
    }

    /**
     * @param string              $absolute_path
     * @param int                 $product_id
     * @param array<string,mixed> $result
     * @return int
     */
    protected function resolve_attachment_id($absolute_path, $product_id, &$result)
    {
        $filename = basename((string) $absolute_path);

        $existing_id = IPCL_Utils::find_attachment_by_filename($filename);
        if (! empty($existing_id)) {
            wp_update_post(
                array(
                    'ID' => (int) $existing_id,
                    'post_parent' => (int) $product_id,
                )
            );
            $result['reused_attachments']++;
            IPCL_Utils::log($result, 'info', sprintf('Reused attachment ID %d for %s.', (int) $existing_id, $filename));
            return (int) $existing_id;
        }

        $upload_dir = wp_upload_dir();
        if (! empty($upload_dir['error'])) {
            IPCL_Utils::log($result, 'error', sprintf('Uploads error: %s', (string) $upload_dir['error']));
            return 0;
        }

        $target_name = wp_unique_filename((string) $upload_dir['path'], $filename);
        $target_path = trailingslashit((string) $upload_dir['path']) . $target_name;

        if (! copy($absolute_path, $target_path)) {
            IPCL_Utils::log($result, 'error', sprintf('Failed copying %s into uploads.', $filename));
            return 0;
        }

        $filetype = wp_check_filetype($target_name, null);

        $attachment_id = wp_insert_attachment(
            array(
                'post_mime_type' => ! empty($filetype['type']) ? $filetype['type'] : 'image/webp',
                'post_title' => sanitize_file_name(pathinfo($target_name, PATHINFO_FILENAME)),
                'post_content' => '',
                'post_status' => 'inherit',
                'post_parent' => (int) $product_id,
            ),
            $target_path,
            (int) $product_id
        );

        if (is_wp_error($attachment_id) || empty($attachment_id)) {
            IPCL_Utils::log($result, 'error', sprintf('Failed creating attachment for %s.', $filename));
            return 0;
        }

        if (! function_exists('wp_generate_attachment_metadata')) {
            require_once ABSPATH . 'wp-admin/includes/image.php';
        }

        $metadata = wp_generate_attachment_metadata((int) $attachment_id, $target_path);
        if (! is_wp_error($metadata)) {
            wp_update_attachment_metadata((int) $attachment_id, $metadata);
        }

        update_post_meta((int) $attachment_id, '_ipcl_source_filename', $filename);

        $result['imported_images']++;
        IPCL_Utils::log($result, 'info', sprintf('Imported image %s as attachment ID %d.', $filename, (int) $attachment_id));

        return (int) $attachment_id;
    }
}
