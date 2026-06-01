<?php
/**
 * Shipping Calculator
 *
 * This template can be overridden by copying it to yourtheme/woocommerce/cart/shipping-calculator.php.
 *
 * HOWEVER, on occasion WooCommerce will need to update template files and you
 * (the theme developer) will need to copy the new files to your theme to
 * maintain compatibility. We try to do this as little as possible, but it does
 * happen. When this occurs the version of the template file will be bumped and
 * the readme will list any important changes.
 *
 * @see     https://woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates
 * @version 9.7.0
 */

defined( 'ABSPATH' ) || exit;

$shipping_address_1      = function_exists( 'beslock_get_shipping_session_value' ) ? beslock_get_shipping_session_value( 'beslock_shipping_address_1', WC()->customer->get_shipping_address_1() ) : WC()->customer->get_shipping_address_1();
$shipping_locality       = function_exists( 'beslock_get_shipping_session_value' ) ? beslock_get_shipping_session_value( 'beslock_shipping_locality', WC()->customer->get_meta( 'beslock_shipping_locality' ) ) : WC()->customer->get_meta( 'beslock_shipping_locality' );
$shipping_neighborhood   = function_exists( 'beslock_get_shipping_session_value' ) ? beslock_get_shipping_session_value( 'beslock_shipping_neighborhood', WC()->customer->get_meta( 'beslock_shipping_neighborhood' ) ) : WC()->customer->get_meta( 'beslock_shipping_neighborhood' );
$shipping_area_options   = function_exists( 'beslock_get_shipping_area_options' ) ? beslock_get_shipping_area_options() : array();
$shipping_city_options   = function_exists( 'beslock_get_shipping_city_options' ) ? beslock_get_shipping_city_options() : array();
$shipping_barrio_options = function_exists( 'beslock_get_shipping_neighborhood_options' ) ? beslock_get_shipping_neighborhood_options() : array();
$shipping_barrio_groups  = function_exists( 'beslock_get_shipping_neighborhood_area_options' ) ? beslock_get_shipping_neighborhood_area_options() : array();
$colombia_states         = WC()->countries->get_states( 'CO' );

do_action( 'woocommerce_before_shipping_calculator' ); ?>

<form class="woocommerce-shipping-calculator" action="<?php echo esc_url( wc_get_cart_url() ); ?>" method="post">

    <?php printf( '<a href="#" class="shipping-calculator-button" aria-expanded="false" aria-controls="shipping-calculator-form" role="button">%s</a>', esc_html( ! empty( $button_text ) ? $button_text : __( 'Calculate shipping', 'woocommerce' ) ) ); ?>

    <section class="shipping-calculator-form" id="shipping-calculator-form" style="display:none;">

        <input type="hidden" name="calc_shipping_country" id="calc_shipping_country" value="CO" />

        <?php if ( apply_filters( 'woocommerce_shipping_calculator_enable_state', true ) ) : ?>
            <p class="form-row form-row-wide" id="calc_shipping_state_field">
                <?php
                $current_cc = 'CO';
                $current_r  = WC()->customer->get_shipping_state();
                $states     = $colombia_states;

                if ( is_array( $states ) && empty( $states ) ) {
                    ?>
                    <input type="hidden" name="calc_shipping_state" id="calc_shipping_state" />
                    <?php
                } elseif ( is_array( $states ) ) {
                    ?>
                    <span>
                        <label for="calc_shipping_state"><?php esc_html_e( 'Departamento', 'beslock-custom' ); ?></label>
                        <select name="calc_shipping_state" class="state_select" id="calc_shipping_state" required>
                            <option value=""><?php esc_html_e( 'Selecciona departamento', 'beslock-custom' ); ?></option>
                            <?php
                            foreach ( $states as $ckey => $cvalue ) {
                                echo '<option value="' . esc_attr( $ckey ) . '" ' . selected( $current_r, $ckey, false ) . '>' . esc_html( $cvalue ) . '</option>';
                            }
                            ?>
                        </select>
                    </span>
                    <?php
                } else {
                    ?>
                    <label for="calc_shipping_state"><?php esc_html_e( 'Departamento', 'beslock-custom' ); ?></label>
                    <input type="text" class="input-text" value="<?php echo esc_attr( $current_r ); ?>" name="calc_shipping_state" id="calc_shipping_state" />
                    <?php
                }
                ?>
            </p>
        <?php endif; ?>

        <?php if ( apply_filters( 'woocommerce_shipping_calculator_enable_city', true ) ) : ?>
            <p class="form-row form-row-wide" id="calc_shipping_city_field">
                <label for="calc_shipping_city"><?php esc_html_e( 'Ciudad / Municipio', 'beslock-custom' ); ?></label>
                <?php $current_city = WC()->customer->get_shipping_city(); ?>
                <select
                    name="calc_shipping_city"
                    id="calc_shipping_city"
                    class="beslock-shipping-city-select"
                    data-current-value="<?php echo esc_attr( $current_city ); ?>"
                    required
                >
                    <option value=""><?php esc_html_e( 'Selecciona Ciudad / Municipio', 'beslock-custom' ); ?></option>
                    <?php
                    $city_option_values = array();
                    foreach ( $shipping_city_options as $department_code => $city_options ) :
                        foreach ( $city_options as $city_option ) :
                            $city_option_values[] = $city_option;
                            ?>
                            <option
                                value="<?php echo esc_attr( $city_option ); ?>"
                                data-department="<?php echo esc_attr( $department_code ); ?>"
                                <?php selected( $current_city, $city_option ); ?>
                            >
                                <?php echo esc_html( $city_option ); ?>
                            </option>
                        <?php endforeach; ?>
                    <?php endforeach; ?>
                    <?php if ( '' !== $current_city && ! in_array( $current_city, $city_option_values, true ) ) : ?>
                        <option value="<?php echo esc_attr( $current_city ); ?>" data-department="<?php echo esc_attr( $current_r ); ?>" selected><?php echo esc_html( $current_city ); ?></option>
                    <?php endif; ?>
                </select>
            </p>
        <?php endif; ?>

        <p class="form-row form-row-wide" id="calc_shipping_locality_field">
            <label for="calc_shipping_locality"><?php esc_html_e( 'Localidad / Comuna', 'beslock-custom' ); ?></label>
            <select
                name="calc_shipping_locality"
                id="calc_shipping_locality"
                class="beslock-shipping-locality-select"
                data-current-value="<?php echo esc_attr( $shipping_locality ); ?>"
                aria-describedby="beslock-shipping-area-help"
            >
                <option value=""><?php esc_html_e( 'Selecciona localidad / comuna', 'beslock-custom' ); ?></option>
                <option value="No aplica" data-city="*"><?php esc_html_e( 'No aplica en mi ciudad', 'beslock-custom' ); ?></option>
                <?php
                $locality_option_values = array();
                foreach ( $shipping_area_options as $city_label => $area_options ) :
                    foreach ( $area_options as $area_option ) :
                        $locality_option_values[] = $area_option;
                        ?>
                        <option
                            value="<?php echo esc_attr( $area_option ); ?>"
                            data-city="<?php echo esc_attr( $city_label ); ?>"
                            <?php selected( $shipping_locality, $area_option ); ?>
                        >
                            <?php echo esc_html( $area_option ); ?>
                        </option>
                    <?php endforeach; ?>
                <?php endforeach; ?>
                <?php if ( '' !== $shipping_locality && ! in_array( $shipping_locality, $locality_option_values, true ) && 'No aplica' !== $shipping_locality ) : ?>
                    <option value="<?php echo esc_attr( $shipping_locality ); ?>" data-city="<?php echo esc_attr( $current_city ); ?>" selected><?php echo esc_html( $shipping_locality ); ?></option>
                <?php endif; ?>
            </select>
        </p>

        <p class="form-row form-row-wide" id="calc_shipping_neighborhood_field">
            <label for="calc_shipping_neighborhood_select"><?php esc_html_e( 'Barrio', 'beslock-custom' ); ?></label>
            <select
                name="calc_shipping_neighborhood"
                id="calc_shipping_neighborhood_select"
                class="beslock-shipping-neighborhood-select"
                data-current-value="<?php echo esc_attr( $shipping_neighborhood ); ?>"
                aria-describedby="beslock-shipping-area-help"
            >
                <option value=""><?php esc_html_e( 'Selecciona barrio', 'beslock-custom' ); ?></option>
                <option value="No aparece en la lista" data-city="*" data-area="*"><?php esc_html_e( 'No aparece en la lista', 'beslock-custom' ); ?></option>
                <?php
                $barrio_option_values = array();
                $barrio_option_scopes = array();

                if ( ! empty( $shipping_barrio_groups ) ) {
                    foreach ( $shipping_barrio_groups as $city_label => $area_groups ) {
                        foreach ( $area_groups as $area_label => $barrio_options ) {
                            foreach ( $barrio_options as $barrio_option ) {
                                $scope_key = $city_label . '|' . $barrio_option;

                                if ( ! isset( $barrio_option_scopes[ $scope_key ] ) ) {
                                    $barrio_option_scopes[ $scope_key ] = array(
                                        'city'  => $city_label,
                                        'label' => $barrio_option,
                                        'areas' => array(),
                                    );
                                }

                                $barrio_option_scopes[ $scope_key ]['areas'][] = '' === $area_label ? '*' : $area_label;
                            }
                        }
                    }
                } else {
                    foreach ( $shipping_barrio_options as $city_label => $barrio_options ) {
                        foreach ( $barrio_options as $barrio_option ) {
                            $barrio_option_scopes[ $city_label . '|' . $barrio_option ] = array(
                                'city'  => $city_label,
                                'label' => $barrio_option,
                                'areas' => array( '*' ),
                            );
                        }
                    }
                }

                foreach ( $barrio_option_scopes as $barrio_scope ) :
                    $barrio_option_values[] = $barrio_scope['label'];
                    $barrio_area_scope      = in_array( '*', $barrio_scope['areas'], true ) ? '*' : implode( '|', array_unique( $barrio_scope['areas'] ) );
                    ?>
                    <option
                        value="<?php echo esc_attr( $barrio_scope['label'] ); ?>"
                        data-city="<?php echo esc_attr( $barrio_scope['city'] ); ?>"
                        data-area="<?php echo esc_attr( $barrio_area_scope ); ?>"
                        <?php selected( $shipping_neighborhood, $barrio_scope['label'] ); ?>
                    >
                        <?php echo esc_html( $barrio_scope['label'] ); ?>
                    </option>
                <?php endforeach; ?>
                <?php if ( '' !== $shipping_neighborhood && ! in_array( $shipping_neighborhood, $barrio_option_values, true ) && 'No aparece en la lista' !== $shipping_neighborhood ) : ?>
                    <option value="<?php echo esc_attr( $shipping_neighborhood ); ?>" data-city="<?php echo esc_attr( $current_city ); ?>" data-area="<?php echo esc_attr( $shipping_locality ); ?>" selected><?php echo esc_html( $shipping_neighborhood ); ?></option>
                <?php endif; ?>
            </select>
            <input
                type="text"
                name="calc_shipping_neighborhood"
                id="calc_shipping_neighborhood"
                class="input-text beslock-shipping-neighborhood-manual"
                value="<?php echo esc_attr( $shipping_neighborhood ); ?>"
                placeholder="<?php esc_attr_e( 'Escribe barrio o sector', 'beslock-custom' ); ?>"
                autocomplete="shipping address-level4"
                aria-describedby="beslock-shipping-area-help"
                disabled
                hidden
            />
            <span id="beslock-shipping-area-help" class="beslock-cart-field-help"><?php esc_html_e( 'Localidad/Comuna y Barrio son opcionales, pero debes ingresar al menos uno.', 'beslock-custom' ); ?></span>
        </p>

        <p class="form-row form-row-wide" id="calc_shipping_address_1_field">
            <label for="calc_shipping_address_1"><?php esc_html_e( 'Dirección completa', 'beslock-custom' ); ?></label>
            <input
                type="text"
                class="input-text"
                name="calc_shipping_address_1"
                id="calc_shipping_address_1"
                value="<?php echo esc_attr( $shipping_address_1 ); ?>"
                placeholder="<?php esc_attr_e( 'Calle/carrera, número, torre, apto o interior', 'beslock-custom' ); ?>"
                autocomplete="shipping address-line1"
                required
            />
        </p>

        <input type="hidden" name="calc_shipping_postcode" id="calc_shipping_postcode" value="<?php echo esc_attr( WC()->customer->get_shipping_postcode() ); ?>" />

        <p><button type="submit" name="calc_shipping" value="1" class="button<?php echo esc_attr( wc_wp_theme_get_element_class_name( 'button' ) ? ' ' . wc_wp_theme_get_element_class_name( 'button' ) : '' ); ?>"><?php esc_html_e( 'Actualizar dirección', 'beslock-custom' ); ?></button></p>
        <?php wp_nonce_field( 'woocommerce-shipping-calculator', 'woocommerce-shipping-calculator-nonce' ); ?>
    </section>
</form>

<?php do_action( 'woocommerce_after_shipping_calculator' ); ?>
