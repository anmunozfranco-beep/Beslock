<?php
defined('ABSPATH') || exit;
/**
 * Wompi Payment Gateway
 *
 * Provides a Wompi Payment Gateway.
 *
 * @class   WompiPortalPagos_Gateway
 * @extends Wompi_Portal_Pagos_Gateway_Custom
 * @version 1.0.0
 * @package WooCommerce/Classes/Payment
 */
class WompiPortalPagos_Gateway extends Wompi_Portal_Pagos_Gateway_Custom {

	/**
	 * Constructor for the gateway.
	 */
	public function __construct() {
		$this->id                 = 'wompi';
		$this->method_title       = 'WOMPI';
		$this->method_description = sprintf(
			// translators: %1$s: search term
			__('Wompi works via Widget Checkout. <a href="%1$s" target="_blank">Sign up</a> for a Wompi account, and <a href="%2$s" target="_blank">get your Wompi account keys</a>.', 'wompi-portal-de-pagos'),
			'https://comercios.wompi.co/',
			'https://comercios.wompi.co/my-account'
		);
		$this->has_fields = false;
		$this->init_form_fields();
		$this->init_settings();

		// Load settings using WooCommerce's built-in method for better compatibility
		$this->enabled          = $this->get_option('enabled', '');
		$this->icon             = WC_WOMPI_PLUGIN_URL . '/assets/img/wompi-logo.png';
		$this->title            = $this->get_option('title', '');
		$this->description      = $this->get_option('description', '');
		$this->testmode         = $this->get_option('testmode', '');
		$this->supports         = array(
			'products'
		);

		// Set API keys based on test mode
		if ('yes' === $this->testmode) {
			$this->public_key       = $this->get_option('test_public_key', '');
			$this->private_key      = $this->get_option('test_private_key', '');
			$this->event_secret_key = $this->get_option('test_event_secret_key', '');
			$this->integrity_key    = $this->get_option('test_integrity_key', '');
		} else {
			$this->public_key       = $this->get_option('public_key', '');
			$this->private_key      = $this->get_option('private_key', '');
			$this->event_secret_key = $this->get_option('event_secret_key', '');
			$this->integrity_key    = $this->get_option('integrity_key', '');
		}

		add_action('woocommerce_update_options_payment_gateways_' . $this->id, array($this, 'process_admin_options'));
		add_action('woocommerce_update_options_payment_gateways_' . $this->id, array($this, 'refresh_main_settings'));

		if ('yes' === $this->enabled) {
			$this->init_hooks();
		}
	}

	/**
	 * Refresh main settings after save
	 */
	public function refresh_main_settings() {
		Wompi_Portal_Pagos_Main::refresh_settings();
	}

	/**
	 * Checks to see if all criteria is met before showing payment method
	 */
	public function is_available() {
		return parent::is_available() &&
			!empty($this->private_key) &&
			!empty($this->public_key) &&
			!empty($this->event_secret_key) &&
			!empty($this->integrity_key) &&
			in_array(get_woocommerce_currency(), self::get_supported_currency(), true);
	}

	/**
	 * Initialise Gateway Settings Form Fields
	 */
	public function init_form_fields() {
		$this->form_fields = include dirname(__FILE__) . '/admin/wompi-settings.php';
	}

	/**
	 * Gets the transaction URL linked to Wompi dashboard
	 */
	public function get_transaction_url($order) {
		 // We make a call to the endpoint to be able to search for transactions made in the payment gateway
		// API Documentation: https://wompi.com/es/co/transacciones
		$this->view_transaction_url = 'https://wompi.com/es/co/transacciones';

		return parent::get_transaction_url($order);
	}

	/**
	 * Process the payment (after place order)
	 */
	public function process_payment($order_id) {
		$order = new WC_Order($order_id);
		if (version_compare(WOOCOMMERCE_VERSION, '2.1.0', '>=')) {
			/* >= 2.1.0 */
			$checkout_payment_url = $order->get_checkout_payment_url(true);
		} else {
			/* < 2.1.0 */
			$checkout_payment_url = get_permalink(get_option('woocommerce_pay_page_id'));
		}
		// Clear cart
		WC()->cart->empty_cart();

		return array(
			'result' => 'success',
			'redirect' => add_query_arg('order_pay', $order_id, $checkout_payment_url)
		);
	}

	/**
	 * Process the payment to void
	 */
	public static function process_void($order) {
		// Restore stock
		wc_maybe_increase_stock_levels($order);
	}
}
