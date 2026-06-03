<?php
/**
 * BESLOCK admin payment gateway enabled email.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.7.0
 */

defined( 'ABSPATH' ) || exit;

do_action( 'woocommerce_email_header', esc_html__( 'Pasarela de pago habilitada', 'beslock-custom' ), $email );
?>

<div class="email-introduction">
	<p class="beslock-lead">
		<?php
		printf(
			/* translators: %s: username */
			esc_html__( 'Hola %s,', 'beslock-custom' ),
			esc_html( $username )
		);
		?>
	</p>
	<p>
		<?php
		printf(
			/* translators: 1: gateway title, 2: site URL */
			esc_html__( 'Se acaba de habilitar la pasarela de pago "%1$s" en este sitio: %2$s', 'beslock-custom' ),
			esc_html( $gateway_title ),
			esc_html( home_url() )
		);
		?>
	</p>
	<p><?php esc_html_e( 'Si no realizaste este cambio, ingresa al administrador y revisa la configuración de pagos cuanto antes.', 'beslock-custom' ); ?></p>
	<p><a class="beslock-button" href="<?php echo esc_url( $gateway_settings_url ); ?>"><?php esc_html_e( 'Revisar pasarela', 'beslock-custom' ); ?></a></p>
	<p>
		<?php
		printf(
			/* translators: %s: admin email */
			esc_html__( 'Este correo fue enviado a %s.', 'beslock-custom' ),
			esc_html( $admin_email )
		);
		?>
	</p>
</div>

<?php
do_action( 'woocommerce_email_footer', $email );
