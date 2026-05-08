<?php
/**
 * Plugin Name: Info Product Catalog Loader
 * Description: Loads products and product images into WooCommerce from local Beslock sources.
 * Version: 1.0.0
 * Author: Beslock
 * Text Domain: info-prod-catlg-loader
 */

if (! defined('ABSPATH')) {
    exit;
}

if (! defined('IPCL_PLUGIN_FILE')) {
    define('IPCL_PLUGIN_FILE', __FILE__);
}

if (! defined('IPCL_PLUGIN_DIR')) {
    define('IPCL_PLUGIN_DIR', plugin_dir_path(__FILE__));
}

if (! defined('IPCL_PLUGIN_URL')) {
    define('IPCL_PLUGIN_URL', plugin_dir_url(__FILE__));
}

if (! defined('IPCL_PLUGIN_VERSION')) {
    define('IPCL_PLUGIN_VERSION', '1.0.0');
}

register_activation_hook(__FILE__, 'ipcl_on_activate');

/**
 * Activation guard for WooCommerce dependency.
 */
function ipcl_on_activate()
{
    if (! class_exists('WooCommerce')) {
        deactivate_plugins(plugin_basename(__FILE__));
        wp_die(
            esc_html__('Info Product Catalog Loader requires WooCommerce to be active.', 'info-prod-catlg-loader'),
            esc_html__('Plugin activation error', 'info-prod-catlg-loader'),
            array('back_link' => true)
        );
    }
}

add_action('plugins_loaded', 'ipcl_bootstrap');

/**
 * Initialize plugin services.
 */
function ipcl_bootstrap()
{
    require_once IPCL_PLUGIN_DIR . 'includes/class-ipcl-utils.php';
    require_once IPCL_PLUGIN_DIR . 'includes/class-ipcl-json-reader.php';
    require_once IPCL_PLUGIN_DIR . 'includes/class-ipcl-product-loader.php';
    require_once IPCL_PLUGIN_DIR . 'includes/class-ipcl-image-loader.php';
    require_once IPCL_PLUGIN_DIR . 'includes/class-ipcl-admin.php';

    if (! class_exists('WooCommerce')) {
        add_action(
            'admin_notices',
            function () {
                if (! current_user_can('activate_plugins')) {
                    return;
                }

                echo '<div class="notice notice-error"><p>'
                    . esc_html__('Info Product Catalog Loader is inactive until WooCommerce is activated.', 'info-prod-catlg-loader')
                    . '</p></div>';
            }
        );

        return;
    }

    $json_path = IPCL_Utils::get_products_json_path();
    $image_root = IPCL_Utils::get_image_root_path();

    $admin = new IPCL_Admin(
        new IPCL_JSON_Reader($json_path),
        new IPCL_Product_Loader(),
        new IPCL_Image_Loader($image_root)
    );

    $admin->register_hooks();
}
