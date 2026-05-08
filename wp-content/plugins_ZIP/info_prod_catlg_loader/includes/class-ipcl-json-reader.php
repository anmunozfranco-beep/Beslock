<?php

if (! defined('ABSPATH')) {
    exit;
}

/**
 * Reads and normalizes products JSON input.
 */
class IPCL_JSON_Reader
{
    /**
     * @var string
     */
    protected $json_path;

    /**
     * @param string $json_path
     */
    public function __construct($json_path)
    {
        $this->json_path = (string) $json_path;
    }

    /**
     * @return string
     */
    public function get_json_path()
    {
        return $this->json_path;
    }

    /**
     * @return array<int,array<string,mixed>>|WP_Error
     */
    public function read_entries()
    {
        if (! file_exists($this->json_path)) {
            return new WP_Error('ipcl_json_missing', sprintf('JSON file not found: %s', $this->json_path));
        }

        if (! is_readable($this->json_path)) {
            return new WP_Error('ipcl_json_unreadable', sprintf('JSON file is not readable: %s', $this->json_path));
        }

        $raw = file_get_contents($this->json_path);
        if ($raw === false) {
            return new WP_Error('ipcl_json_read_fail', sprintf('Failed reading JSON file: %s', $this->json_path));
        }

        $decoded = json_decode($raw, true);

        if (! is_array($decoded)) {
            return new WP_Error('ipcl_json_invalid', 'Invalid JSON content. Expected a top-level array.');
        }

        $entries = array();

        foreach ($decoded as $index => $entry) {
            if (! is_array($entry)) {
                continue;
            }

            $normalized = $this->normalize_entry($entry);
            if (is_wp_error($normalized)) {
                continue;
            }

            $entries[] = $normalized;
        }

        return $entries;
    }

    /**
     * @param array<string,mixed> $entry
     * @return array<string,mixed>|WP_Error
     */
    protected function normalize_entry($entry)
    {
        $present = array(
            'product_id' => array_key_exists('product_id', $entry),
            'slug' => array_key_exists('slug', $entry),
            'sku' => array_key_exists('sku', $entry),
            'name' => array_key_exists('name', $entry) || array_key_exists('title', $entry),
            'price' => array_key_exists('price', $entry),
            'short_description' => array_key_exists('short_description', $entry),
            'description' => array_key_exists('description', $entry),
            'categories' => array_key_exists('categories', $entry),
            'tags' => array_key_exists('tags', $entry),
            'status' => array_key_exists('status', $entry),
        );

        $name_raw = '';
        if (array_key_exists('name', $entry)) {
            $name_raw = (string) $entry['name'];
        } elseif (array_key_exists('title', $entry)) {
            $name_raw = (string) $entry['title'];
        }

        $name = trim(wp_strip_all_tags($name_raw));
        $slug = '';
        if (array_key_exists('slug', $entry)) {
            $slug = sanitize_title((string) $entry['slug']);
        }

        if ($slug === '' && $name !== '') {
            $slug = sanitize_title($name);
        }

        if ($name === '' && $slug === '' && empty($entry['sku']) && empty($entry['product_id'])) {
            return new WP_Error('ipcl_malformed_entry', 'Missing product identity fields.');
        }

        $product_id = 0;
        if (! empty($entry['product_id']) && is_numeric($entry['product_id'])) {
            $product_id = (int) $entry['product_id'];
        }

        $sku = '';
        if (array_key_exists('sku', $entry)) {
            $sku = wc_clean((string) $entry['sku']);
        }

        $price = '';
        if (array_key_exists('price', $entry)) {
            $price = wc_format_decimal((string) $entry['price']);
        }

        $short_description = '';
        if (array_key_exists('short_description', $entry)) {
            $short_description = (string) $entry['short_description'];
        }

        $description = '';
        if (array_key_exists('description', $entry)) {
            $description = (string) $entry['description'];
        }

        $status = 'publish';
        if (array_key_exists('status', $entry)) {
            $status = IPCL_Utils::normalize_status((string) $entry['status']);
        }

        $categories = $this->normalize_terms(isset($entry['categories']) ? $entry['categories'] : array());
        $tags = $this->normalize_terms(isset($entry['tags']) ? $entry['tags'] : array());

        return array(
            'product_id' => $product_id,
            'slug' => $slug,
            'sku' => $sku,
            'name' => $name,
            'price' => $price,
            'short_description' => $short_description,
            'description' => $description,
            'categories' => $categories,
            'tags' => $tags,
            'status' => $status,
            '_present' => $present,
        );
    }

    /**
     * @param mixed $terms
     * @return array<int,string>
     */
    protected function normalize_terms($terms)
    {
        if (! is_array($terms)) {
            return array();
        }

        $normalized = array();

        foreach ($terms as $term) {
            $value = trim(wp_strip_all_tags((string) $term));
            if ($value === '') {
                continue;
            }

            $normalized[] = $value;
        }

        return array_values(array_unique($normalized));
    }
}
