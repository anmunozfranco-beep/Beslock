<?php
/**
 * BESLOCK email header.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.7.0
 */

defined( 'ABSPATH' ) || exit;

if ( ! function_exists( 'beslock_email_registered_mark_allowed_html' ) ) {
	/**
	 * Allowed markup for the BESLOCK registered mark in email templates.
	 *
	 * @return array<string, array<string, bool>>
	 */
	function beslock_email_registered_mark_allowed_html() {
		return array(
			'sup' => array(
				'aria-hidden' => true,
				'class'       => true,
			),
		);
	}
}

if ( ! function_exists( 'beslock_email_registered_brand' ) ) {
	/**
	 * Return the BESLOCK brand with the registered mark as superscript.
	 *
	 * @return string
	 */
	function beslock_email_registered_brand() {
		return 'BESLOCK<sup class="beslock-registered-mark" aria-hidden="true">®</sup>';
	}
}

if ( ! function_exists( 'beslock_email_format_registered_brand' ) ) {
	/**
	 * Format any visible BESLOCK registered mark as superscript.
	 *
	 * @param string $text Text to format.
	 * @return string
	 */
	function beslock_email_format_registered_brand( $text ) {
		return wp_kses(
			str_replace( 'BESLOCK®', beslock_email_registered_brand(), esc_html( $text ) ),
			beslock_email_registered_mark_allowed_html()
		);
	}
}

$email      = $email ?? null;
$store_name = 'BESLOCK®';

$header_image_url = apply_filters( 'woocommerce_email_header_image_url', home_url() );
$img              = get_option( 'woocommerce_email_header_image' );

if ( apply_filters( 'woocommerce_is_email_preview', false ) ) {
	$img_transient = get_transient( 'woocommerce_email_header_image' );
	$img           = false !== $img_transient ? $img_transient : $img;
}

if ( ! $img ) {
	$img = get_stylesheet_directory_uri() . '/assets/images/logo-green.png';
}

$beslock_order = null;
if ( isset( $GLOBALS['beslock_email_order'] ) && $GLOBALS['beslock_email_order'] instanceof WC_Order ) {
	$beslock_order = $GLOBALS['beslock_email_order'];
}
if ( is_object( $email ) && isset( $email->object ) && $email->object instanceof WC_Order ) {
	$beslock_order = $email->object;
}

$order_status       = $beslock_order ? wc_get_order_status_name( $beslock_order->get_status() ) : '';
$order_status_class = $beslock_order ? sanitize_html_class( 'beslock-status-' . $beslock_order->get_status() ) : '';
$date_created       = $beslock_order ? $beslock_order->get_date_created() : null;
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=<?php bloginfo( 'charset' ); ?>" />
		<meta content="width=device-width, initial-scale=1.0" name="viewport">
		<title><?php echo esc_html( $store_name ); ?></title>
	</head>
	<body <?php echo is_rtl() ? 'rightmargin' : 'leftmargin'; ?>="0" marginwidth="0" topmargin="0" marginheight="0" offset="0">
		<table width="100%" id="outer_wrapper" role="presentation">
			<tr>
				<td></td>
				<td width="640">
					<div id="wrapper" dir="<?php echo is_rtl() ? 'rtl' : 'ltr'; ?>">
						<table border="0" cellpadding="0" cellspacing="0" width="100%" id="inner_wrapper" role="presentation">
							<tr>
								<td align="center" valign="top">
									<table border="0" cellpadding="0" cellspacing="0" width="100%" class="beslock-email-brand-bar" role="presentation">
										<tr>
											<td id="template_header_image" class="beslock-email-logo" valign="middle">
												<?php
												$logo_image = '<img src="' . esc_url( $img ) . '" alt="' . esc_attr( $store_name ) . '" />';
												$logo_mark  = '<sup class="beslock-registered-mark beslock-logo-mark" aria-hidden="true">®</sup>';
												if ( $header_image_url ) {
													$logo_image = '<a href="' . esc_url( $header_image_url ) . '" target="_blank" style="display:inline-block;text-decoration:none;">' . $logo_image . '</a>';
													$logo_mark  = '<a href="' . esc_url( $header_image_url ) . '" target="_blank" style="color:#034526;text-decoration:none;">' . $logo_mark . '</a>';
												}
												$image_html = '<table border="0" cellpadding="0" cellspacing="0" class="beslock-logo-table" role="presentation"><tr><td class="beslock-logo-image-cell" valign="top">' . $logo_image . '</td><td class="beslock-logo-mark-cell" valign="top">' . $logo_mark . '</td></tr></table>';
												echo wp_kses_post( $image_html );
												?>
											</td>
											<td class="beslock-email-kicker" valign="middle">
												<span><?php esc_html_e( 'Seguridad premium', 'beslock-custom' ); ?></span><br>
												<?php esc_html_e( 'Acceso inteligente para tu espacio', 'beslock-custom' ); ?>
											</td>
										</tr>
									</table>

									<table border="0" cellpadding="0" cellspacing="0" width="100%" id="template_container" role="presentation">
										<tr>
											<td align="center" valign="top">
												<table border="0" cellpadding="0" cellspacing="0" width="100%" id="template_header" role="presentation">
													<tr>
														<td id="header_wrapper">
															<p class="beslock-eyebrow"><?php esc_html_e( 'Actualización de pedido', 'beslock-custom' ); ?></p>
															<h1><?php echo beslock_email_format_registered_brand( $email_heading ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></h1>
															<?php if ( $beslock_order ) : ?>
																<table border="0" cellpadding="0" cellspacing="0" width="100%" class="beslock-order-hero" role="presentation">
																	<tr>
																		<td class="beslock-order-hero-cell" valign="top">
																			<span><?php esc_html_e( 'Pedido', 'beslock-custom' ); ?></span><br>
																			<strong>#<?php echo esc_html( $beslock_order->get_order_number() ); ?></strong>
																		</td>
																		<td class="beslock-order-hero-cell" valign="top">
																			<span><?php esc_html_e( 'Estado', 'beslock-custom' ); ?></span><br>
																			<strong class="beslock-status-pill <?php echo esc_attr( $order_status_class ); ?>"><?php echo esc_html( $order_status ); ?></strong>
																		</td>
																		<td class="beslock-order-hero-cell" valign="top">
																			<span><?php esc_html_e( 'Total', 'beslock-custom' ); ?></span><br>
																			<strong><?php echo wp_kses_post( $beslock_order->get_formatted_order_total() ); ?></strong>
																		</td>
																		<?php if ( $date_created ) : ?>
																			<td class="beslock-order-hero-cell" valign="top">
																				<span><?php esc_html_e( 'Fecha', 'beslock-custom' ); ?></span><br>
																				<strong><?php echo esc_html( wc_format_datetime( $date_created ) ); ?></strong>
																			</td>
																		<?php endif; ?>
																	</tr>
																</table>
															<?php endif; ?>
														</td>
													</tr>
												</table>
											</td>
										</tr>
										<tr>
											<td align="center" valign="top">
												<table border="0" cellpadding="0" cellspacing="0" width="100%" id="template_body" role="presentation">
													<tr>
														<td valign="top" id="body_content">
															<table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
																<tr>
																	<td valign="top" id="body_content_inner_cell">
																		<div id="body_content_inner">
