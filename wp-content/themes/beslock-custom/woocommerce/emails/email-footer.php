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
																				<td>
																					<strong><?php esc_html_e( 'Soporte BESLOCK', 'beslock-custom' ); ?></strong><br>
																					<?php esc_html_e( 'Si necesitas ayuda con tu pedido o instalación, responde este correo y el equipo te acompaña.', 'beslock-custom' ); ?>
																					<?php if ( $store_email ) : ?>
																						<br><a href="mailto:<?php echo esc_attr( $store_email ); ?>"><?php echo esc_html( $store_email ); ?></a>
																					<?php endif; ?>
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
															<?php
															$email_footer_text = get_option( 'woocommerce_email_footer_text' );
															if ( apply_filters( 'woocommerce_is_email_preview', false ) ) {
																$text_transient    = get_transient( 'woocommerce_email_footer_text' );
																$email_footer_text = false !== $text_transient ? $text_transient : $email_footer_text;
															}

															echo wp_kses_post(
																wpautop(
																	wptexturize(
																		apply_filters( 'woocommerce_email_footer_text', $email_footer_text, $email )
																	)
																)
															);
															?>
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
