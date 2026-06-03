<?php
/**
 * BESLOCK customer reset password email.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.4.0
 */

defined( 'ABSPATH' ) || exit;

do_action( 'woocommerce_email_header', esc_html__( 'Restablece tu contraseña', 'beslock-custom' ), $email );
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
		printf(
			/* translators: %s: site name */
			esc_html__( 'Recibimos una solicitud para restablecer la contraseña de tu cuenta en %s.', 'beslock-custom' ),
			esc_html( $blogname )
		);
		?>
	</p>
	<p><?php esc_html_e( 'Si no hiciste esta solicitud, puedes ignorar este correo. Si quieres continuar, usa el botón seguro de abajo.', 'beslock-custom' ); ?></p>
	<p><strong><?php esc_html_e( 'Usuario:', 'beslock-custom' ); ?></strong> <?php echo esc_html( $user_login ); ?></p>
	<p>
		<a class="beslock-button" href="<?php echo esc_url( add_query_arg( array( 'key' => $reset_key, 'id' => $user_id, 'login' => rawurlencode( $user_login ) ), wc_get_endpoint_url( 'lost-password', '', wc_get_page_permalink( 'myaccount' ) ) ) ); ?>">
			<?php esc_html_e( 'Restablecer contraseña', 'beslock-custom' ); ?>
		</a>
	</p>
</div>

<?php
do_action( 'woocommerce_email_footer', $email );
