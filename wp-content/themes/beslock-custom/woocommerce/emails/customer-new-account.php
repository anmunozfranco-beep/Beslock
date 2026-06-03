<?php
/**
 * BESLOCK customer new account email.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.4.0
 */

defined( 'ABSPATH' ) || exit;

do_action( 'woocommerce_email_header', esc_html__( 'Bienvenido a BESLOCK®', 'beslock-custom' ), $email );
?>

<div class="email-introduction">
	<p class="beslock-lead">
		<?php
		printf(
			/* translators: %s: username */
			esc_html__( 'Hola %s,', 'beslock-custom' ),
			esc_html( $user_login )
		);
		?>
	</p>
	<p>
		<?php
		echo wp_kses(
			sprintf(
				/* translators: %s: BESLOCK brand */
				esc_html__( 'Gracias por crear tu cuenta en %s', 'beslock-custom' ),
				beslock_email_registered_brand()
			),
			beslock_email_registered_mark_allowed_html()
		);
		?>
	</p>
	<p><strong><?php esc_html_e( 'Usuario:', 'beslock-custom' ); ?></strong> <?php echo esc_html( $user_login ); ?></p>
	<?php if ( $password_generated && $set_password_url ) : ?>
		<p><a class="beslock-button" href="<?php echo esc_url( $set_password_url ); ?>"><?php esc_html_e( 'Crear contraseña', 'beslock-custom' ); ?></a></p>
	<?php endif; ?>
	<p><?php esc_html_e( 'Desde tu cuenta puedes revisar pedidos, actualizar tus datos y gestionar tus compras.', 'beslock-custom' ); ?></p>
	<p><a href="<?php echo esc_url( wc_get_page_permalink( 'myaccount' ) ); ?>"><?php esc_html_e( 'Ir a mi cuenta', 'beslock-custom' ); ?></a></p>
</div>

<?php
do_action( 'woocommerce_email_footer', $email );
