<?php
/**
 * BESLOCK email footer.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates\Emails
 * @version 10.4.0
 */

defined( 'ABSPATH' ) || exit;

$email       = $email ?? null;
$store_email = get_option( 'woocommerce_email_from_address' );

if ( ! $store_email ) {
	$store_email = get_option( 'admin_email' );
}

$partner_logo_path = get_stylesheet_directory() . '/assets/images/partners/zonas-smart-logo.png';
$partner_logo_url  = '';

if ( file_exists( $partner_logo_path ) ) {
	$partner_logo_url = get_stylesheet_directory_uri() . '/assets/images/partners/zonas-smart-logo.png?v=' . filemtime( $partner_logo_path );
}
?>
																		<table border="0" cellpadding="0" cellspacing="0" width="100%" class="beslock-footer-support" role="presentation">
																			<tr>
																				<td class="beslock-footer-support-cell">
																					<table border="0" cellpadding="0" cellspacing="0" width="100%" class="beslock-footer-operator-table" role="presentation">
																						<tr>
																							<td class="beslock-footer-operator-copy" valign="middle">
																								<strong class="beslock-footer-operator-title">
																									<?php echo wp_kses( beslock_email_registered_brand(), beslock_email_registered_mark_allowed_html() ); ?> | <?php esc_html_e( 'ZONAS SMART', 'beslock-custom' ); ?>
																								</strong><br>
																								<span class="beslock-footer-operator-kicker"><?php esc_html_e( 'Comercializador autorizado en Colombia.', 'beslock-custom' ); ?></span><br>
																								<?php esc_html_e( 'Si necesitas ayuda con tu pedido, instalación o acompañamiento posventa, responde este correo y nuestro equipo te acompaña.', 'beslock-custom' ); ?><br>
																								<span class="beslock-footer-operator-detail"><?php esc_html_e( 'Comercialización, logística, instalación y acompañamiento posventa.', 'beslock-custom' ); ?></span>
																								<?php if ( $store_email ) : ?>
																									<br><a href="mailto:<?php echo esc_attr( $store_email ); ?>"><?php echo esc_html( $store_email ); ?></a>
																								<?php endif; ?>
																							</td>
																							<?php if ( $partner_logo_url ) : ?>
																								<td class="beslock-footer-operator-logo-cell" valign="middle">
																									<a class="beslock-footer-operator-logo" href="https://zonassmart.com/" target="_blank" rel="noopener noreferrer" aria-label="<?php echo esc_attr_x( 'ZONAS SMART, comercializador autorizado', 'email footer partner link label', 'beslock-custom' ); ?>">
																										<img src="<?php echo esc_url( $partner_logo_url ); ?>" alt="<?php echo esc_attr_x( 'ZONAS SMART', 'email footer partner logo alt text', 'beslock-custom' ); ?>" width="76" height="76" />
																									</a>
																								</td>
																							<?php endif; ?>
																						</tr>
																					</table>
																				</td>
																			</tr>
																		</table>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
													</tr>
												</table>
											</td>
										</tr>
									</table>
								</td>
							</tr>
							<tr>
								<td align="center" valign="top">
									<table border="0" cellpadding="0" cellspacing="0" width="100%" id="template_footer" role="presentation">
										<tr>
											<td valign="top">
												<table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
													<tr>
														<td colspan="2" valign="middle" id="credit">
															<p>
																<?php
																echo wp_kses(
																		sprintf(
																			/* translators: %s: BESLOCK brand */
																			esc_html__( 'Gracias por confiar en %s', 'beslock-custom' ),
																			beslock_email_registered_brand()
																		),
																		beslock_email_registered_mark_allowed_html()
																	);
																	?>
																	<br>
																	<?php esc_html_e( 'Si necesitas ayuda con tu pedido, estamos atentos para acompañarte.', 'beslock-custom' ); ?>
																</p>
														</td>
													</tr>
												</table>
											</td>
										</tr>
									</table>
								</td>
							</tr>
						</table>
					</div>
				</td>
				<td></td>
			</tr>
		</table>
	</body>
</html>
