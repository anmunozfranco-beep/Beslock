<?php

if (! defined('ABSPATH')) {
    exit;
}

/**
 * Admin interface for two-step loading flow.
 */
class IPCL_Admin
{
    /**
     * @var IPCL_JSON_Reader
     */
    protected $reader;

    /**
     * @var IPCL_Product_Loader
     */
    protected $product_loader;

    /**
     * @var IPCL_Image_Loader
     */
    protected $image_loader;

    /**
     * @param IPCL_JSON_Reader    $reader
     * @param IPCL_Product_Loader $product_loader
     * @param IPCL_Image_Loader   $image_loader
     */
    public function __construct($reader, $product_loader, $image_loader)
    {
        $this->reader = $reader;
        $this->product_loader = $product_loader;
        $this->image_loader = $image_loader;
    }

    /**
     * Register admin hooks.
     */
    public function register_hooks()
    {
        add_action('admin_menu', array($this, 'register_menu'));
        add_action('admin_init', array($this, 'handle_actions'));
    }

    /**
     * Add page under Tools.
     */
    public function register_menu()
    {
        add_management_page(
            __('Info Product Catalog Loader', 'info-prod-catlg-loader'),
            __('Info Product Catalog Loader', 'info-prod-catlg-loader'),
            $this->required_capability(),
            'info-prod-catlg-loader',
            array($this, 'render_page')
        );
    }

    /**
     * Process button actions.
     */
    public function handle_actions()
    {
        if (! is_admin()) {
            return;
        }

        if (empty($_POST['ipcl_action']) || empty($_POST['ipcl_nonce'])) {
            return;
        }

        if (! current_user_can($this->required_capability())) {
            return;
        }

        $action = sanitize_key(wp_unslash((string) $_POST['ipcl_action']));

        if (! in_array($action, array('load_products', 'load_images'), true)) {
            return;
        }

        check_admin_referer('ipcl_action_' . $action, 'ipcl_nonce');

        $entries = $this->reader->read_entries();
        if (is_wp_error($entries)) {
            $result = IPCL_Utils::make_result();
            IPCL_Utils::log($result, 'error', $entries->get_error_message());
            $this->store_result($result);
            $this->redirect_back();
        }

        if ($action === 'load_products') {
            $result = $this->product_loader->load($entries);
        } else {
            $result = $this->image_loader->load($entries);
        }

        $this->store_result($result);
        $this->redirect_back();
    }

    /**
     * Render Tools page.
     */
    public function render_page()
    {
        if (! current_user_can($this->required_capability())) {
            return;
        }

        $result = $this->read_stored_result();
        $json_path = $this->reader->get_json_path();
        $image_root = $this->image_loader->get_image_root();
        $snapshot_stats = $this->compute_snapshot_stats();

        echo '<div class="wrap">';
        echo '<h1>' . esc_html__('Info Product Catalog Loader', 'info-prod-catlg-loader') . '</h1>';

        echo '<table class="widefat striped" style="max-width: 860px; margin-bottom: 16px;">';
        echo '<tbody>';
        echo '<tr><td><strong>' . esc_html__('JSON source', 'info-prod-catlg-loader') . '</strong></td><td><code>' . esc_html($json_path) . '</code></td></tr>';
        echo '<tr><td>' . esc_html__('JSON file exists', 'info-prod-catlg-loader') . '</td><td>' . (file_exists($json_path) ? '<span style="color:green;">&#10003; Yes</span>' : '<span style="color:#cc4400;">&#10007; No</span>') . '</td></tr>';
        echo '<tr><td>' . esc_html__('JSON file readable', 'info-prod-catlg-loader') . '</td><td>' . (is_readable($json_path) ? '<span style="color:green;">&#10003; Yes</span>' : '<span style="color:#cc4400;">&#10007; No</span>') . '</td></tr>';
        echo '<tr><td><strong>' . esc_html__('Image root', 'info-prod-catlg-loader') . '</strong></td><td><code>' . esc_html($image_root) . '</code></td></tr>';
        echo '<tr><td>' . esc_html__('Image root exists', 'info-prod-catlg-loader') . '</td><td>' . (is_dir($image_root) ? '<span style="color:green;">&#10003; Yes</span>' : '<span style="color:#cc4400;">&#10007; No</span>') . '</td></tr>';
        echo '<tr><td>' . esc_html__('Image root readable', 'info-prod-catlg-loader') . '</td><td>' . (is_dir($image_root) && is_readable($image_root) ? '<span style="color:green;">&#10003; Yes</span>' : '<span style="color:#cc4400;">&#10007; No</span>') . '</td></tr>';
        echo '<tr><td><strong>' . esc_html__('Snapshot entries', 'info-prod-catlg-loader') . '</strong></td><td>' . esc_html((string) $snapshot_stats['count']) . '</td></tr>';
        echo '<tr><td><strong>' . esc_html__('Unique slugs', 'info-prod-catlg-loader') . '</strong></td><td>' . esc_html((string) $snapshot_stats['unique_slug_count']) . '</td></tr>';
        echo '<tr><td><strong>' . esc_html__('Duplicate slugs in JSON', 'info-prod-catlg-loader') . '</strong></td><td>' . esc_html((string) $snapshot_stats['duplicate_slug_count']) . '</td></tr>';
        echo '</tbody>';
        echo '</table>';

        if (! empty($snapshot_stats['duplicate_slugs'])) {
            echo '<div class="notice notice-warning"><p><strong>' . esc_html__('Duplicate slug warnings', 'info-prod-catlg-loader') . '</strong></p><ul style="list-style:disc;padding-left:20px;">';
            foreach ($snapshot_stats['duplicate_slugs'] as $slug) {
                echo '<li>' . esc_html((string) $slug) . '</li>';
            }
            echo '</ul></div>';
        }

        echo '<hr />';
        echo '<h2>' . esc_html__('SECTION 1', 'info-prod-catlg-loader') . '</h2>';

        echo '<form method="post">';
        wp_nonce_field('ipcl_action_load_products', 'ipcl_nonce');
        echo '<input type="hidden" name="ipcl_action" value="load_products" />';
        submit_button('Cargar datos de productos', 'primary', 'submit', false);
        echo '</form>';

        echo '<hr />';
        echo '<h2>' . esc_html__('SECTION 2', 'info-prod-catlg-loader') . '</h2>';

        echo '<form method="post">';
        wp_nonce_field('ipcl_action_load_images', 'ipcl_nonce');
        echo '<input type="hidden" name="ipcl_action" value="load_images" />';
        submit_button('Cargar imágenes', 'secondary', 'submit', false);
        echo '</form>';

        echo '<hr />';
        echo '<h2>' . esc_html__('STATUS AREA', 'info-prod-catlg-loader') . '</h2>';

        echo '<table class="widefat striped" style="max-width: 760px;">';
        echo '<tbody>';
        echo '<tr><td>' . esc_html__('Imported products', 'info-prod-catlg-loader') . '</td><td>' . esc_html((string) $result['imported_products']) . '</td></tr>';
        echo '<tr><td>' . esc_html__('Updated products', 'info-prod-catlg-loader') . '</td><td>' . esc_html((string) $result['updated_products']) . '</td></tr>';
        echo '<tr><td>' . esc_html__('Skipped products', 'info-prod-catlg-loader') . '</td><td>' . esc_html((string) $result['skipped_products']) . '</td></tr>';
        echo '<tr><td>' . esc_html__('Imported images', 'info-prod-catlg-loader') . '</td><td>' . esc_html((string) $result['imported_images']) . '</td></tr>';
        echo '<tr><td>' . esc_html__('Missing image warnings', 'info-prod-catlg-loader') . '</td><td>' . esc_html((string) $result['missing_images']) . '</td></tr>';
        echo '<tr><td>' . esc_html__('Reused attachments', 'info-prod-catlg-loader') . '</td><td>' . esc_html((string) $result['reused_attachments']) . '</td></tr>';
        echo '</tbody>';
        echo '</table>';

        echo '<h3 style="margin-top:24px;">' . esc_html__('Execution log output', 'info-prod-catlg-loader') . '</h3>';
        echo '<textarea readonly="readonly" style="width:100%;max-width:980px;min-height:280px;font-family:monospace;">';
        echo esc_textarea(implode("\n", $result['logs']));
        echo '</textarea>';

        echo '</div>';
    }

    /**
     * @return string
     */
    protected function required_capability()
    {
        if (current_user_can('manage_woocommerce')) {
            return 'manage_woocommerce';
        }

        return 'manage_options';
    }

    /**
     * @param array<string,mixed> $result
     */
    protected function store_result($result)
    {
        set_transient($this->result_key(), $result, 15 * MINUTE_IN_SECONDS);
    }

    /**
     * @return array<string,mixed>
     */
    protected function read_stored_result()
    {
        $result = get_transient($this->result_key());
        if (! is_array($result)) {
            return IPCL_Utils::make_result();
        }

        return wp_parse_args($result, IPCL_Utils::make_result());
    }

    /**
     * @return string
     */
    protected function result_key()
    {
        return 'ipcl_last_result_' . (int) get_current_user_id();
    }

    /**
     * @return array<string,mixed>
     */
    protected function compute_snapshot_stats()
    {
        $stats = array(
            'count' => 0,
            'unique_slug_count' => 0,
            'duplicate_slug_count' => 0,
            'duplicate_slugs' => array(),
        );

        $entries = $this->reader->read_entries();
        if (is_wp_error($entries) || ! is_array($entries)) {
            return $stats;
        }

        $slugs = array();
        foreach ($entries as $entry) {
            if (! is_array($entry) || empty($entry['slug'])) {
                continue;
            }
            $slugs[] = sanitize_title((string) $entry['slug']);
        }

        $stats['count'] = count($entries);
        $stats['unique_slug_count'] = count(array_unique($slugs));
        $counts = array_count_values($slugs);
        foreach ($counts as $slug => $count) {
            if ($count > 1) {
                $stats['duplicate_slugs'][] = $slug;
            }
        }
        $stats['duplicate_slug_count'] = count($stats['duplicate_slugs']);

        return $stats;
    }

    /**
     * Redirect after POST to avoid resubmission.
     */
    protected function redirect_back()
    {
        wp_safe_redirect(admin_url('tools.php?page=info-prod-catlg-loader'));
        exit;
    }
}
