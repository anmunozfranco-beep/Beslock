<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}

function beslock_installation_coverage_user_can_manage() {
  return current_user_can( 'manage_options' ) || current_user_can( 'manage_woocommerce' );
}

function beslock_installation_coverage_register_menu() {
  if ( class_exists( 'WooCommerce' ) ) {
    add_submenu_page(
      'woocommerce',
      __( 'Cobertura de instalación', 'beslock' ),
      __( 'Cobertura instalación', 'beslock' ),
      'manage_woocommerce',
      'beslock-installation-coverage',
      'beslock_installation_coverage_render_page'
    );

    return;
  }

  add_management_page(
    __( 'Cobertura de instalación', 'beslock' ),
    __( 'Cobertura instalación', 'beslock' ),
    'manage_options',
    'beslock-installation-coverage',
    'beslock_installation_coverage_render_page'
  );
}
add_action( 'admin_menu', 'beslock_installation_coverage_register_menu', 80 );

function beslock_installation_coverage_get_default_city_keys() {
  $keys   = array();
  $policy = function_exists( 'beslock_get_cart_installation_policy' ) ? beslock_get_cart_installation_policy() : array();
  $cities = isset( $policy['available_cities'] ) && is_array( $policy['available_cities'] ) ? $policy['available_cities'] : array();

  foreach ( $cities as $city ) {
    $city_key = function_exists( 'beslock_get_installation_city_key' )
      ? beslock_get_installation_city_key( $city )
      : sanitize_key( $city );

    if ( '' !== $city_key ) {
      $keys[] = $city_key;
    }
  }

  return array_values( array_unique( $keys ) );
}

function beslock_installation_coverage_group_catalog( $catalog ) {
  $groups = array();

  foreach ( $catalog as $city ) {
    if ( empty( $city['key'] ) || empty( $city['label'] ) ) {
      continue;
    }

    $department_label = ! empty( $city['department_label'] ) ? $city['department_label'] : __( 'Sin departamento', 'beslock' );

    if ( ! isset( $groups[ $department_label ] ) ) {
      $groups[ $department_label ] = array();
    }

    $groups[ $department_label ][] = $city;
  }

  ksort( $groups, SORT_NATURAL | SORT_FLAG_CASE );

  return $groups;
}

function beslock_installation_coverage_handle_post( $catalog ) {
  if ( empty( $_POST['beslock_installation_coverage_action'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification.Missing
    return '';
  }

  if ( ! beslock_installation_coverage_user_can_manage() ) {
    wp_die( esc_html__( 'Acceso denegado.', 'beslock' ) );
  }

  check_admin_referer( 'beslock_installation_coverage_save', 'beslock_installation_coverage_nonce' );

  $action = sanitize_key( wp_unslash( $_POST['beslock_installation_coverage_action'] ) );

  if ( 'reset' === $action ) {
    delete_option( beslock_get_installation_coverage_option_name() );

    return __( 'Cobertura restaurada al valor por defecto del tema/importador.', 'beslock' );
  }

  if ( 'save' !== $action ) {
    return '';
  }

  $submitted_keys = isset( $_POST['beslock_installation_city_keys'] )
    ? (array) wp_unslash( $_POST['beslock_installation_city_keys'] )
    : array();

  $selected_keys = array();

  foreach ( $submitted_keys as $submitted_key ) {
    $city_key = function_exists( 'beslock_get_installation_city_key' )
      ? beslock_get_installation_city_key( sanitize_text_field( (string) $submitted_key ) )
      : sanitize_key( $submitted_key );

    if ( '' !== $city_key && isset( $catalog[ $city_key ] ) ) {
      $selected_keys[] = $city_key;
    }
  }

  $selected_keys = array_values( array_unique( $selected_keys ) );
  update_option( beslock_get_installation_coverage_option_name(), $selected_keys, false );

  return sprintf(
    /* translators: %d: selected city count. */
    _n( 'Cobertura guardada con %d ciudad activa.', 'Cobertura guardada con %d ciudades activas.', count( $selected_keys ), 'beslock' ),
    count( $selected_keys )
  );
}

function beslock_installation_coverage_render_page() {
  if ( ! beslock_installation_coverage_user_can_manage() ) {
    wp_die( esc_html__( 'Acceso denegado.', 'beslock' ) );
  }

  $catalog = function_exists( 'beslock_get_installation_city_catalog' ) ? beslock_get_installation_city_catalog() : array();
  $message = beslock_installation_coverage_handle_post( $catalog );

  $saved_keys    = function_exists( 'beslock_get_saved_installation_available_city_keys' ) ? beslock_get_saved_installation_available_city_keys() : null;
  $uses_override = is_array( $saved_keys );
  $current_keys  = $uses_override ? $saved_keys : beslock_installation_coverage_get_default_city_keys();
  $current_keys  = array_values( array_intersect( $current_keys, array_keys( $catalog ) ) );
  $selected_map  = array_fill_keys( $current_keys, true );
  $groups        = beslock_installation_coverage_group_catalog( $catalog );
  $total_count   = count( $catalog );
  $active_count  = count( $current_keys );

  ?>
  <div class="wrap beslock-installation-coverage">
    <h1><?php echo esc_html__( 'Cobertura de instalación BESLOCK', 'beslock' ); ?></h1>

    <?php if ( '' !== $message ) : ?>
      <div class="notice notice-success is-dismissible"><p><?php echo esc_html( $message ); ?></p></div>
    <?php endif; ?>

    <p>
      <?php echo esc_html__( 'Activa o retira las ciudades donde el carrito debe permitir seleccionar instalación. La lista usa el mismo catálogo de ciudades del checkout.', 'beslock' ); ?>
    </p>

    <?php if ( empty( $catalog ) ) : ?>
      <div class="notice notice-error">
        <p><?php echo esc_html__( 'No se pudo cargar el catálogo de ciudades. Revisa data/worldcities.csv o los fallbacks de ciudades del tema.', 'beslock' ); ?></p>
      </div>
    <?php else : ?>
      <style>
        .beslock-installation-coverage__panel {
          max-width: 1120px;
          margin-top: 18px;
          padding: 18px;
          background: #fff;
          border: 1px solid #dcdcde;
          border-radius: 8px;
        }
        .beslock-installation-coverage__status {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          align-items: center;
          margin: 0 0 16px;
        }
        .beslock-installation-coverage__pill {
          display: inline-flex;
          align-items: center;
          min-height: 30px;
          padding: 0 10px;
          border-radius: 999px;
          background: #f0f6fc;
          color: #1d2327;
          font-weight: 600;
        }
        .beslock-installation-coverage__pill--custom {
          background: #e6f4ea;
          color: #0a5c36;
        }
        .beslock-installation-coverage__toolbar {
          display: grid;
          grid-template-columns: minmax(220px, 1fr) auto auto;
          gap: 10px;
          align-items: center;
          margin-bottom: 16px;
        }
        .beslock-installation-coverage__search {
          width: 100%;
          min-height: 36px;
        }
        .beslock-installation-coverage__groups {
          display: grid;
          gap: 10px;
          max-height: 62vh;
          overflow: auto;
          padding-right: 4px;
        }
        .beslock-installation-coverage__group {
          border: 1px solid #dcdcde;
          border-radius: 6px;
          background: #fff;
        }
        .beslock-installation-coverage__group[hidden],
        .beslock-installation-coverage__city[hidden] {
          display: none;
        }
        .beslock-installation-coverage__summary {
          cursor: pointer;
          padding: 10px 12px;
          font-weight: 700;
        }
        .beslock-installation-coverage__cities {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
          gap: 8px 12px;
          padding: 4px 12px 14px;
        }
        .beslock-installation-coverage__city {
          display: flex;
          align-items: center;
          gap: 8px;
          min-height: 30px;
        }
        .beslock-installation-coverage__actions {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          align-items: center;
          margin-top: 18px;
        }
        @media (max-width: 782px) {
          .beslock-installation-coverage__toolbar {
            grid-template-columns: 1fr;
          }
        }
      </style>

      <form method="post" class="beslock-installation-coverage__panel" data-js="beslock-installation-coverage-form">
        <?php wp_nonce_field( 'beslock_installation_coverage_save', 'beslock_installation_coverage_nonce' ); ?>

        <div class="beslock-installation-coverage__status">
          <span class="beslock-installation-coverage__pill" data-js="beslock-installation-coverage-count">
            <?php
            echo esc_html(
              sprintf(
                /* translators: 1: active city count, 2: total city count. */
                __( '%1$d de %2$d ciudades activas', 'beslock' ),
                $active_count,
                $total_count
              )
            );
            ?>
          </span>
          <span class="beslock-installation-coverage__pill<?php echo $uses_override ? ' beslock-installation-coverage__pill--custom' : ''; ?>">
            <?php
            echo esc_html(
              $uses_override
                ? __( 'Configuración administrada desde WP', 'beslock' )
                : __( 'Usando cobertura por defecto', 'beslock' )
            );
            ?>
          </span>
        </div>

        <div class="beslock-installation-coverage__toolbar">
          <input
            type="search"
            class="regular-text beslock-installation-coverage__search"
            placeholder="<?php echo esc_attr__( 'Buscar ciudad o departamento', 'beslock' ); ?>"
            data-js="beslock-installation-coverage-search"
          >
          <button type="button" class="button" data-js="beslock-installation-coverage-select-visible">
            <?php echo esc_html__( 'Marcar visibles', 'beslock' ); ?>
          </button>
          <button type="button" class="button" data-js="beslock-installation-coverage-clear-visible">
            <?php echo esc_html__( 'Desmarcar visibles', 'beslock' ); ?>
          </button>
        </div>

        <div class="beslock-installation-coverage__groups">
          <?php foreach ( $groups as $department_label => $cities ) : ?>
            <details class="beslock-installation-coverage__group" open data-js="beslock-installation-coverage-group">
              <summary class="beslock-installation-coverage__summary">
                <?php
                echo esc_html(
                  sprintf(
                    '%1$s (%2$d)',
                    $department_label,
                    count( $cities )
                  )
                );
                ?>
              </summary>
              <div class="beslock-installation-coverage__cities">
                <?php foreach ( $cities as $city ) : ?>
                  <?php
                  $city_key   = $city['key'];
                  $city_label = $city['label'];
                  $search     = strtolower( remove_accents( $city_label . ' ' . $department_label ) );
                  ?>
                  <label class="beslock-installation-coverage__city" data-js="beslock-installation-coverage-city" data-search="<?php echo esc_attr( $search ); ?>">
                    <input
                      type="checkbox"
                      name="beslock_installation_city_keys[]"
                      value="<?php echo esc_attr( $city_key ); ?>"
                      <?php checked( isset( $selected_map[ $city_key ] ) ); ?>
                    >
                    <span><?php echo esc_html( $city_label ); ?></span>
                  </label>
                <?php endforeach; ?>
              </div>
            </details>
          <?php endforeach; ?>
        </div>

        <div class="beslock-installation-coverage__actions">
          <button type="submit" name="beslock_installation_coverage_action" value="save" class="button button-primary">
            <?php echo esc_html__( 'Guardar cobertura', 'beslock' ); ?>
          </button>
          <button
            type="submit"
            name="beslock_installation_coverage_action"
            value="reset"
            class="button"
            onclick="return confirm('<?php echo esc_js( __( '¿Restaurar la cobertura por defecto del tema/importador?', 'beslock' ) ); ?>');"
          >
            <?php echo esc_html__( 'Restaurar valor por defecto', 'beslock' ); ?>
          </button>
        </div>
      </form>

      <script>
        (function() {
          var form = document.querySelector('[data-js="beslock-installation-coverage-form"]');

          if (!form) {
            return;
          }

          var search = form.querySelector('[data-js="beslock-installation-coverage-search"]');
          var rows = Array.prototype.slice.call(form.querySelectorAll('[data-js="beslock-installation-coverage-city"]'));
          var groups = Array.prototype.slice.call(form.querySelectorAll('[data-js="beslock-installation-coverage-group"]'));
          var boxes = Array.prototype.slice.call(form.querySelectorAll('input[type="checkbox"][name="beslock_installation_city_keys[]"]'));
          var count = form.querySelector('[data-js="beslock-installation-coverage-count"]');
          var total = boxes.length;

          function normalize(value) {
            value = String(value || '').toLowerCase();

            if (value.normalize) {
              value = value.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            }

            return value.trim();
          }

          function updateCount() {
            var selected = boxes.filter(function(box) {
              return box.checked;
            }).length;

            if (count) {
              count.textContent = selected + ' de ' + total + ' ciudades activas';
            }
          }

          function updateSearch() {
            var query = normalize(search ? search.value : '');

            rows.forEach(function(row) {
              var match = !query || normalize(row.getAttribute('data-search')).indexOf(query) !== -1;
              row.hidden = !match;
            });

            groups.forEach(function(group) {
              var visibleRows = Array.prototype.slice.call(group.querySelectorAll('[data-js="beslock-installation-coverage-city"]')).filter(function(row) {
                return !row.hidden;
              });

              group.hidden = visibleRows.length === 0;

              if (query && visibleRows.length > 0) {
                group.open = true;
              }
            });
          }

          function toggleVisible(checked) {
            rows.forEach(function(row) {
              if (row.hidden) {
                return;
              }

              var box = row.querySelector('input[type="checkbox"]');

              if (box) {
                box.checked = checked;
              }
            });

            updateCount();
          }

          if (search) {
            search.addEventListener('input', updateSearch);
          }

          form.querySelector('[data-js="beslock-installation-coverage-select-visible"]').addEventListener('click', function() {
            toggleVisible(true);
          });

          form.querySelector('[data-js="beslock-installation-coverage-clear-visible"]').addEventListener('click', function() {
            toggleVisible(false);
          });

          boxes.forEach(function(box) {
            box.addEventListener('change', updateCount);
          });

          updateCount();
        })();
      </script>
    <?php endif; ?>
  </div>
  <?php
}
