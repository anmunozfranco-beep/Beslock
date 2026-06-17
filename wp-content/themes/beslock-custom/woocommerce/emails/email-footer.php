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

?>
																		<table border="0" cellpadding="0" cellspacing="0" width="100%" class="beslock-footer-support" role="presentation">
																			<tr>
																				<td class="beslock-footer-support-cell">
																					<table border="0" cellpadding="0" cellspacing="0" width="100%" class="beslock-footer-operator-table" role="presentation">
																						<tr>
																							<td class="beslock-footer-operator-copy" valign="middle">
																								<strong class="beslock-footer-operator-title">
																									<?php echo wp_kses( beslock_email_registered_brand(), beslock_email_registered_mark_allowed_html() ); ?>
																								</strong><br>
																								<span class="beslock-footer-operator-kicker"><?php esc_html_e( 'Atención oficial en Colombia.', 'beslock-custom' ); ?></span><br>
																								<?php esc_html_e( 'Si necesitas ayuda con tu pedido, instalación o acompañamiento posventa, responde este correo y nuestro equipo te acompaña.', 'beslock-custom' ); ?><br>
																								<span class="beslock-footer-operator-detail"><?php esc_html_e( 'Ventas, logística, instalación y acompañamiento posventa.', 'beslock-custom' ); ?></span>
																								<?php if ( $store_email ) : ?>
																									<br><a href="mailto:<?php echo esc_attr( $store_email ); ?>"><?php echo esc_html( $store_email ); ?></a>
																								<?php endif; ?>
																							</td>
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
