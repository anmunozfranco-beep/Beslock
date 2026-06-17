<?php
// Runner: execute carga_portfolio_data dry-run and print JSON result.
// Run via PHP-CLI from any location inside the WordPress checkout.
define('WP_USE_THEMES', false);
$wp_load = '';
$dir = __DIR__;
for ($i = 0; $i <= 8; $i++) {
    $candidate = realpath($dir . str_repeat('/..', $i) . '/wp-load.php');
    if ($candidate && file_exists($candidate)) {
        $wp_load = $candidate;
        break;
    }
}
if (!$wp_load) {
    fwrite(STDERR, "Cannot locate wp-load.php by walking up from " . __DIR__ . "\n");
    exit(1);
}
require_once $wp_load;
// Load the importer script
require_once get_stylesheet_directory() . '/inc/admin/portfolio-data.php';

try {
    $result = beslock_carga_portfolio_process(true);
    // If WP_Error, convert to array
    if (is_wp_error($result)) {
        $out = [
            'success' => false,
            'error' => $result->get_error_message(),
            'data' => $result->get_error_data(),
        ];
    } else {
        $out = $result;
    }
    echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n";
} catch (Throwable $e) {
    $err = [
        'success' => false,
        'exception' => get_class($e),
        'message' => $e->getMessage(),
        'trace' => $e->getTraceAsString(),
    ];
    echo json_encode($err, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n";
}
