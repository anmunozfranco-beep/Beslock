<?php
/**
 * BESLOCK email styles.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.7.0
 */

defined( 'ABSPATH' ) || exit;

$text_align     = is_rtl() ? 'right' : 'left';
$opposite_align = is_rtl() ? 'left' : 'right';
$font_family    = '"Helvetica Neue", Helvetica, Arial, sans-serif';
?>
body {
	background-color: #f6f7f5;
	padding: 0;
	text-align: center;
}

#outer_wrapper {
	background-color: #f6f7f5;
}

#wrapper {
	margin: 0 auto;
	max-width: 640px;
	padding: 28px 0;
	width: 100%;
	-webkit-text-size-adjust: none !important;
}

#inner_wrapper {
	background-color: transparent;
}

.beslock-email-brand-bar {
	margin: 0 0 14px;
	width: 100%;
}

#template_header_image {
	padding: 0 0 0 2px;
	text-align: <?php echo esc_attr( $text_align ); ?>;
}

.beslock-logo-table {
	border: 0;
	border-collapse: collapse;
	border-spacing: 0;
	display: inline-table;
	margin: 0;
	padding: 0;
	width: auto;
}

.beslock-logo-image-cell {
	border: 0;
	line-height: 0;
	padding: 0;
	vertical-align: top;
}

.beslock-logo-mark-cell {
	border: 0;
	line-height: 1;
	padding: 0 0 0 1px;
	vertical-align: top;
}

#template_header_image img {
	display: inline-block;
	height: auto;
	margin: 0;
	max-width: 224px;
	vertical-align: top;
	width: 224px;
}

.beslock-registered-mark {
	display: inline;
	font-size: 52%;
	font-weight: 700;
	line-height: 0;
	margin-left: 2px;
	position: static;
	vertical-align: super;
}

h1 .beslock-registered-mark {
	font-size: 48%;
	vertical-align: super;
}

.beslock-lead .beslock-registered-mark,
.beslock-footer-support .beslock-registered-mark,
#credit .beslock-registered-mark {
	font-size: 58%;
	vertical-align: super;
}

.beslock-logo-mark {
	color: #034526;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 15px;
	line-height: 1;
	margin-left: 0;
	position: static;
	vertical-align: top;
}

.beslock-email-kicker {
	color: #667266;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 12px;
	line-height: 150%;
	padding: 0 2px 0 18px;
	text-align: <?php echo esc_attr( $opposite_align ); ?>;
}

.beslock-email-kicker span {
	color: #034526;
	font-size: 11px;
	font-weight: 700;
	letter-spacing: 0;
	text-transform: uppercase;
}

#template_container {
	background-color: #ffffff;
	border: 1px solid #dbe3dd;
	border-radius: 8px !important;
	box-shadow: 0 18px 46px rgba(16, 32, 24, 0.10) !important;
	overflow: hidden;
	width: 100%;
}

#template_header {
	background-color: #034526;
	border-bottom: 0;
	color: #ffffff;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
}

#header_wrapper {
	display: block;
	padding: 34px 40px 36px;
}

.beslock-eyebrow {
	color: #c9d8cf;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 11px;
	font-weight: 700;
	letter-spacing: 0;
	line-height: 140%;
	margin: 0 0 10px;
	text-align: <?php echo esc_attr( $text_align ); ?>;
	text-transform: uppercase;
}

#template_header h1,
#template_header h1 a {
	background-color: inherit;
	color: #ffffff;
}

h1 {
	color: #ffffff;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 30px;
	font-weight: 700;
	letter-spacing: 0;
	line-height: 118%;
	margin: 0;
	text-align: <?php echo esc_attr( $text_align ); ?>;
}

.beslock-order-hero {
	background-color: rgba(255, 255, 255, 0.08);
	border: 0;
	border-radius: 8px;
	margin-top: 24px;
	width: 100%;
}

.beslock-order-hero-cell {
	border-<?php echo esc_attr( $opposite_align ); ?>: 0;
	color: #ffffff;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	padding: 16px 20px;
	text-align: <?php echo esc_attr( $text_align ); ?>;
}

.beslock-order-hero-cell span {
	color: #c9d8cf;
	font-size: 11px;
	font-weight: 700;
	letter-spacing: 0;
	text-transform: uppercase;
}

.beslock-order-hero-cell strong {
	color: #ffffff;
	display: inline-block;
	font-size: 14px;
	font-weight: 700;
	line-height: 150%;
	margin-top: 4px;
}

.beslock-status-pill {
	background-color: #ffffff;
	border-radius: 999px;
	color: #034526 !important;
	padding: 3px 10px;
}

.beslock-status-pending,
.beslock-status-on-hold {
	color: #8a5b05 !important;
}

.beslock-status-failed,
.beslock-status-cancelled {
	color: #8d2b20 !important;
}

#body_content {
	background-color: #ffffff;
}

#body_content_inner_cell {
	padding: 34px 40px 38px;
}

#body_content_inner {
	color: #28392f;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 15px;
	line-height: 165%;
	text-align: <?php echo esc_attr( $text_align ); ?>;
}

#body_content p {
	margin: 0 0 16px;
}

.email-introduction {
	background-color: transparent;
	border-bottom: 1px solid #e3e9e4;
	margin-bottom: 28px;
	padding: 0 0 12px;
}

.beslock-lead {
	color: #102018;
	font-size: 18px;
	font-weight: 700;
	line-height: 145%;
}

.beslock-note-card {
	background-color: transparent;
	border-left: 3px solid #034526;
	border-radius: 0;
	margin: 18px 0 24px;
}

.beslock-note-card td {
	color: #28392f;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 14px;
	line-height: 160%;
	padding: 4px 0 4px 18px;
}

.beslock-note-card strong {
	color: #034526;
}

.beslock-button {
	background-color: #034526;
	border-radius: 6px;
	color: #ffffff !important;
	display: inline-block;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 14px;
	font-weight: 700;
	line-height: 120%;
	margin: 6px 0 4px;
	padding: 14px 20px;
	text-decoration: none;
}

h2 {
	color: #102018;
	display: block;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 20px;
	font-weight: 700;
	line-height: 140%;
	margin: 0 0 18px;
	text-align: <?php echo esc_attr( $text_align ); ?>;
}

h3 {
	color: #102018;
	display: block;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 15px;
	font-weight: 700;
	line-height: 140%;
	margin: 0 0 4px;
	text-align: <?php echo esc_attr( $text_align ); ?>;
}

a {
	color: #034526;
	font-weight: 700;
	text-decoration: underline;
}

img {
	border: none;
	display: inline-block;
	font-size: 14px;
	height: auto;
	outline: none;
	text-decoration: none;
	vertical-align: middle;
	max-width: 100%;
}

.td {
	border: 0;
	color: #28392f;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	vertical-align: middle;
}

.font-family,
.text,
.address-title,
.order-item-data {
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
}

.text-align-left {
	text-align: <?php echo esc_attr( $text_align ); ?>;
}

.text-align-right {
	text-align: <?php echo esc_attr( $opposite_align ); ?>;
}

.beslock-order-heading {
	margin-bottom: 8px;
}

.beslock-order-heading span {
	color: #667266;
	display: block;
	font-size: 13px;
	font-weight: 400;
	margin-top: 2px;
}

.beslock-order-shell {
	margin-bottom: 28px;
}

.email-order-details {
	border-collapse: separate;
	border-spacing: 0;
	width: 100%;
}

.email-order-details thead th {
	background-color: transparent;
	border-bottom: 1px solid #dbe3dd;
	color: #667266;
	font-size: 11px;
	font-weight: 700;
	letter-spacing: 0;
	padding: 12px 14px;
	text-transform: uppercase;
}

.email-order-details tbody td {
	border-bottom: 1px solid #e6ece7;
	padding: 16px 14px;
}

.email-order-details .beslock-product-cell {
	padding-<?php echo esc_attr( $text_align ); ?>: 0;
}

.beslock-product-wrap td {
	border: 0 !important;
	padding: 0 !important;
	vertical-align: top;
}

.beslock-product-thumb {
	padding-<?php echo esc_attr( $opposite_align ); ?>: 14px !important;
	width: 64px;
}

.beslock-product-thumb img {
	border: 1px solid #e3e9e4;
	border-radius: 8px;
	margin: 0;
	width: 56px;
}

.beslock-product-title {
	color: #102018;
	font-size: 15px;
	font-weight: 700;
	line-height: 145%;
	margin: 0;
}

.email-order-item-meta {
	color: #667266;
	font-size: 12px;
	line-height: 150%;
	margin-top: 4px;
}

.beslock-qty-cell,
.beslock-price-cell {
	color: #102018;
	font-size: 14px;
	font-weight: 700;
	white-space: nowrap;
}

.beslock-totals-table {
	background-color: transparent;
	border-top: 1px solid #dbe3dd;
	margin-top: 18px;
	width: 100%;
}

.beslock-totals-table th,
.beslock-totals-table td {
	border-bottom: 1px solid #e3e9e4;
	color: #28392f;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 14px;
	font-weight: 500;
	padding: 10px 14px;
}

.beslock-totals-table tr:last-child th,
.beslock-totals-table tr:last-child td {
	border-bottom: 0;
}

.beslock-totals-table .order-totals-total th,
.beslock-totals-table .order-totals-total td,
.beslock-totals-table .order-totals-last th,
.beslock-totals-table .order-totals-last td {
	color: #102018;
	font-size: 17px;
	font-weight: 700;
}

.beslock-totals-table .order-totals-payment-method th,
.beslock-totals-table .order-totals-payment-method td {
	border-bottom: 0;
	color: #28392f;
	font-size: 14px;
	font-weight: 700;
	padding-top: 14px;
}

.beslock-customer-note {
	background-color: #fffdf7;
	border: 1px solid #eee1bd;
	border-radius: 8px;
	margin-top: 18px;
	width: 100%;
}

.beslock-customer-note td {
	color: #4f4224;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 14px;
	line-height: 160%;
	padding: 16px 18px;
}

#addresses {
	margin: 30px 0 0;
	width: 100%;
}

.beslock-address-card {
	background-color: transparent;
	border-top: 1px solid #dbe3dd;
	border-radius: 0;
	padding: 20px 0 0 !important;
}

.address-title {
	color: #102018;
	display: block;
	font-size: 13px;
	font-weight: 700;
	margin-bottom: 8px;
}

.address {
	color: #28392f;
	font-style: normal;
	line-height: 160%;
	padding: 0;
	word-break: normal;
}

.beslock-footer-support {
	background-color: transparent;
	border-top: 1px solid #dbe3dd;
	border-radius: 0;
	margin-top: 34px;
}

.beslock-footer-support td {
	color: #28392f;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 13px;
	line-height: 160%;
	padding: 18px 0 0;
	text-align: <?php echo esc_attr( $text_align ); ?>;
}

.beslock-footer-support strong {
	color: #034526;
}

#template_footer td {
	padding: 0;
}

#template_footer #credit {
	border: 0;
	color: #667266;
	font-family: <?php echo $font_family; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>;
	font-size: 12px;
	line-height: 150%;
	padding: 22px 28px 0;
	text-align: center;
}

#template_footer #credit p {
	margin: 0 0 10px;
}

#template_footer #credit,
#template_footer #credit a {
	color: #667266;
}

@media screen and (max-width: 640px) {
	#wrapper {
		padding: 18px 10px !important;
	}

	.beslock-email-kicker {
		display: none !important;
	}

	#template_header_image img {
		width: 176px !important;
	}

	.beslock-logo-mark {
		font-size: 13px !important;
		margin-left: 0 !important;
		vertical-align: top !important;
	}

	#header_wrapper {
		padding: 28px 24px 30px !important;
	}

	h1 {
		font-size: 24px !important;
	}

	#body_content_inner_cell {
		padding: 26px 22px 30px !important;
	}

	.beslock-order-hero-cell {
		display: block !important;
		border-right: 0 !important;
		border-bottom: 0 !important;
		width: auto !important;
	}

	.email-order-details thead th,
	.email-order-details tbody td {
		padding-left: 8px !important;
		padding-right: 8px !important;
	}

	.beslock-product-thumb {
		display: none !important;
	}

	.beslock-address-cell {
		display: block !important;
		width: auto !important;
		padding: 0 0 12px !important;
	}
}
<?php
