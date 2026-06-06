<?php
if ( ! defined( 'ABSPATH' ) ) {
  exit;
}
?>
<nav id="mobileDrawer" class="mobile-drawer" data-js="mobile-drawer" aria-hidden="true" role="dialog" aria-label="<?php esc_attr_e( 'Menú móvil', 'beslock' ); ?>">
  <div class="mobile-drawer__panel" data-js="mobile-drawer-panel" role="document">
    <div class="drawer-header" data-js="mobile-drawer-header" role="banner">
      <button id="closeDrawer" class="mobile-drawer__close" data-js="drawer-close" aria-label="<?php esc_attr_e( 'Cerrar menú', 'beslock' ); ?>">
        <span class="mobile-drawer__control-icon mobile-drawer__close-icon" aria-hidden="true"></span>
        <span class="screen-reader-text"><?php esc_html_e( 'Cerrar navegación', 'beslock' ); ?></span>
      </button>

      <a class="drawer__logo" href="<?php echo esc_url( home_url( '/' ) ); ?>" data-js="drawer-logo" aria-label="<?php esc_attr_e( 'Inicio', 'beslock' ); ?>">
        <span class="logo-wrapper">
          <img src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/images/logo-green.png' ); ?>" alt="<?php esc_attr_e( 'Logo BESLOCK', 'beslock' ); ?>" />
          <span class="logo__tm" aria-hidden="true">&#174;</span>
        </span>
      </a>
    </div>

    <ul class="mobile-menu" data-js="mobile-drawer-menu" role="menu">
      <li class="mobile-menu__item" role="none">
        <button class="mobile-menu__link" id="productsToggle" data-js="drawer-products-toggle" aria-expanded="false" aria-controls="productsPanel" role="menuitem">
          <?php esc_html_e( 'Productos', 'beslock' ); ?> <span class="products-chevron mobile-drawer__control-icon mobile-drawer__control-icon--forward" aria-hidden="true"></span>
        </button>

        <div id="productsPanel" class="mobile-products-panel models models--hidden" data-js="drawer-products-panel" role="region" aria-hidden="true" aria-labelledby="productsToggle">
          <?php get_template_part( 'templates/models-mobile' ); ?>
        </div>
      </li>

      <li class="mobile-menu__item mobile-menu__item--order-lookup" role="none">
        <button type="button" class="mobile-menu__link mobile-menu__link--order-lookup" id="orderLookupToggle" data-js="order-lookup-toggle" aria-expanded="false" aria-controls="orderLookupPanel" role="menuitem">
          <span class="mobile-menu__icon mobile-menu__icon--order-lookup" aria-hidden="true"></span>
          <div class="mobile-menu__meta">
            <span class="mobile-menu__title">Consulta tu pedido</span>
            <span class="mobile-menu__subtitle">Revisa el estado de tu compra</span>
          </div>
        </button>

        <div id="orderLookupPanel" class="mobile-menu-order-lookup" data-js="order-lookup-panel" role="region" aria-labelledby="orderLookupToggle" hidden>
          <form class="mobile-menu-order-lookup__form" action="<?php echo esc_url( home_url( '/consulta-pedido/' ) ); ?>" method="post" data-js="order-lookup-form" novalidate>
            <label class="mobile-menu-order-lookup__field">
              <span>Número de pedido</span>
              <input type="text" name="beslock_order_number" inputmode="numeric" autocomplete="off" data-js="order-lookup-order" />
            </label>

            <label class="mobile-menu-order-lookup__field">
              <span>Correo electrónico</span>
              <input type="email" name="beslock_order_email" autocomplete="email" data-js="order-lookup-email" />
            </label>

            <p class="mobile-menu-order-lookup__error" data-js="order-lookup-error" hidden></p>

            <button type="submit" class="mobile-menu-order-lookup__submit">Consultar</button>
          </form>
        </div>
      </li>

      <li class="mobile-menu__item mobile-menu__item--manuals" role="none">
        <button class="mobile-menu__link mobile-menu__link--manuals" id="manualsToggle" data-js="drawer-manuals-toggle" aria-expanded="false" aria-controls="manualsSectionsPanel" role="menuitem">
          <span class="mobile-menu__icon mobile-menu__icon--guides" aria-hidden="true"></span>
          <div class="mobile-menu__meta">
            <span class="mobile-menu__title">Guías BESLOCK</span>
            <span class="mobile-menu__subtitle">Manuales y ayuda del producto</span>
          </div>
        </button>

        <div id="manualsSectionsPanel" class="manuals-sections-panel" data-js="drawer-manuals-sections" role="region" aria-hidden="true" hidden>
          <button type="button" class="manuals-section-button" data-manual-section="conoce-tu-cerradura">Conoce tu cerradura</button>
          <button type="button" class="manuals-section-button" data-manual-section="instalacion">Instalación</button>
          <button type="button" class="manuals-section-button" data-manual-section="configuracion">Configuración</button>
          <button type="button" class="manuals-section-button" data-manual-section="uso-diario">Uso diario</button>
          <button type="button" class="manuals-section-button" data-manual-section="soluciones-rapidas">Soluciones rápidas</button>
        </div>
      </li>

      <li class="mobile-menu__item mobile-menu__item--support" role="none">
        <button type="button" class="mobile-menu__link mobile-menu__link--support" id="supportToggle" data-js="support-toggle" aria-expanded="false" aria-controls="supportOptionsPanel" role="menuitem">
          <i class="bi bi-headset" aria-hidden="true"></i>
          <div class="mobile-menu__meta">
            <span class="mobile-menu__title">Contacto</span>
            <span class="mobile-menu__subtitle">Estamos para ayudarte</span>
          </div>
        </button>

        <div id="supportOptionsPanel" class="support-options-panel" data-js="support-options" role="region" aria-hidden="true" hidden>
          <button type="button" class="support-option-button" data-support-target="schedule-installation">
            <span class="support-option-button__label">
              <span>Consultar y Programar</span>
              <span>instalación</span>
            </span>
          </button>
          <button type="button" class="support-option-button" data-support-target="project-purchases">Compras para proyectos</button>
        </div>
      </li>

    </ul>

    <?php
      $drawer_partner_logo_path = get_stylesheet_directory() . '/assets/images/partners/zonas-smart-logo.png';
      $drawer_partner_logo_url  = get_stylesheet_directory_uri() . '/assets/images/partners/zonas-smart-logo.png';

      if ( file_exists( $drawer_partner_logo_path ) ) :
        $drawer_partner_logo_url = $drawer_partner_logo_url . '?v=' . filemtime( $drawer_partner_logo_path );
    ?>
      <a
        class="mobile-drawer__partner"
        href="https://zonassmart.com/"
        target="_blank"
        rel="noopener noreferrer"
        aria-label="<?php echo esc_attr_x( 'ZONAS SMART, comercializador autorizado', 'drawer partner link label', 'beslock' ); ?>"
      >
        <span class="mobile-drawer__partner-kicker">Comercializador autorizado</span>
        <img
          class="mobile-drawer__partner-logo"
          src="<?php echo esc_url( $drawer_partner_logo_url ); ?>"
          alt="<?php echo esc_attr_x( 'ZONAS SMART', 'alt text', 'beslock' ); ?>"
          width="1024"
          height="1024"
          loading="lazy"
          decoding="async"
        />
      </a>
    <?php endif; ?>
  </div>

  <aside id="manualsDrawer" class="manuals-drawer" data-js="manuals-drawer" aria-hidden="true" aria-label="<?php esc_attr_e( 'Guías BESLOCK', 'beslock' ); ?>">
    <div class="manuals-drawer__shell" data-js="manuals-drawer-shell">
      <header class="manuals-drawer__header">
        <div>
          <p class="manuals-drawer__eyebrow" data-js="manuals-drawer-eyebrow">Guías BESLOCK</p>
          <h2 class="manuals-drawer__title" data-js="manuals-drawer-title">Manuales y ayuda</h2>
        </div>
        <button type="button" class="manuals-drawer__close" data-js="manuals-drawer-close" aria-label="<?php esc_attr_e( 'Cerrar guías', 'beslock' ); ?>">
          <i class="bi bi-x-lg" aria-hidden="true"></i>
        </button>
      </header>
      <div class="manuals-drawer__body" data-js="manuals-drawer-body" tabindex="-1"></div>
    </div>
  </aside>

  <aside id="supportDrawer" class="manuals-drawer support-drawer" data-js="support-drawer" aria-hidden="true" aria-label="<?php esc_attr_e( 'Soporte BESLOCK', 'beslock' ); ?>">
    <div class="manuals-drawer__shell support-drawer__shell">
      <header class="manuals-drawer__header support-drawer__header">
        <div>
          <p class="manuals-drawer__eyebrow" data-js="support-drawer-eyebrow">Contacto</p>
          <h2 class="manuals-drawer__title" data-js="support-drawer-title">Estamos para ayudarte</h2>
        </div>
        <button type="button" class="manuals-drawer__close support-drawer__close" data-js="support-drawer-close" aria-label="<?php esc_attr_e( 'Cerrar soporte', 'beslock' ); ?>">
          <i class="bi bi-x-lg" aria-hidden="true"></i>
        </button>
      </header>

      <div class="manuals-drawer__body support-drawer__body" data-js="support-drawer-body" tabindex="-1">
        <section id="supportPanelConsultInstallation" class="support-drawer__panel" data-js="support-panel" data-support-panel="consult-installation" data-support-title="Consultar instalación" hidden>
          <div class="support-drawer__content">
            <p class="support-drawer__intro">Consulta si tu pedido incluye servicio de instalación y conoce el siguiente paso según el estado de tu compra.</p>

            <form class="support-form" data-js="support-installation-check-form" novalidate>
              <label class="support-form__field">
                <span>Número de pedido</span>
                <input type="text" name="order_number" inputmode="numeric" autocomplete="off" required>
              </label>

              <button type="submit" class="support-button support-button--primary">Consultar pedido</button>
              <p class="support-form__message" data-js="support-installation-message" hidden></p>
            </form>

            <div class="support-status-grid" data-js="support-installation-results" hidden>
              <article class="support-status-card" data-support-result="included" hidden>
                <strong>Tu pedido incluye servicio de instalación.</strong>
                <p>Puedes proceder a programar tu visita con uno de nuestros cerrajeros afiliados.</p>
                <button type="button" class="support-button support-button--secondary" data-support-target="schedule-installation">Programar instalación</button>
              </article>

              <article class="support-status-card" data-support-result="not-included" hidden>
                <strong>Tu pedido no incluye servicio de instalación.</strong>
                <p>Si necesitas apoyo, podemos revisar opciones disponibles para tu caso.</p>
                <button type="button" class="support-button support-button--secondary" data-support-target="schedule-installation">Solicitar ayuda</button>
              </article>

              <article class="support-status-card" data-support-result="out-of-coverage" hidden>
                <strong>Cobertura por validar.</strong>
                <p>Actualmente la instalación está disponible inicialmente en Bogotá, Medellín, Cali y Barranquilla. Si tu pedido corresponde a otra ciudad, contáctanos para validar cobertura.</p>
                <button type="button" class="support-button support-button--secondary" data-support-target="schedule-installation">Validar cobertura</button>
              </article>
            </div>
          </div>
        </section>

        <section id="supportPanelScheduleInstallation" class="support-drawer__panel" data-js="support-panel" data-support-panel="schedule-installation" data-support-title="Consultar y Programar instalación" hidden>
          <div class="support-drawer__content">
            <p class="support-drawer__intro" data-js="support-schedule-intro">Programa una instalación con tu número de pedido o solicita validación para un modelo BESLOCK.</p>

            <form class="support-form support-form--grid" data-js="support-schedule-form" action="<?php echo esc_url( admin_url( 'admin-ajax.php' ) ); ?>" method="post" novalidate>
              <input type="hidden" name="action" value="beslock_support_installation_request">
              <input type="hidden" name="nonce" value="<?php echo esc_attr( wp_create_nonce( 'beslock_support_installation' ) ); ?>">

              <fieldset class="support-installation-tabs support-form__field--full" data-js="support-installation-mode">
                <legend class="support-installation-tabs__legend">Tipo de solicitud</legend>
                <input type="hidden" name="beslock_installation_request_type" value="order" data-js="support-schedule-mode">
                <div class="support-installation-tabs__nav" role="tablist" aria-label="Tipo de solicitud de instalación">
                  <button
                    id="supportScheduleTabOrder"
                    class="support-installation-tabs__tab is-active"
                    type="button"
                    role="tab"
                    aria-selected="true"
                    aria-controls="supportSchedulePanelOrder"
                    data-support-schedule-mode="order"
                  >Ya tengo número de pedido</button>
                  <button
                    id="supportScheduleTabNoOrder"
                    class="support-installation-tabs__tab"
                    type="button"
                    role="tab"
                    aria-selected="false"
                    aria-controls="supportSchedulePanelNoOrder"
                    tabindex="-1"
                    data-support-schedule-mode="no_order"
                  >No tengo número de pedido</button>
                </div>
              </fieldset>

              <div id="supportSchedulePanelOrder" class="support-schedule-fields support-schedule-fields--order support-form__field--full" data-js="support-schedule-fields" data-support-schedule-panel="order" role="tabpanel" aria-labelledby="supportScheduleTabOrder">
                <label class="support-form__field">
                  <span>Número de pedido</span>
                  <input type="text" name="order_number" inputmode="numeric" autocomplete="off" required>
                </label>

                <label class="support-form__field">
                  <span>Correo electrónico</span>
                  <input type="email" name="order_email" autocomplete="email" required>
                </label>

                <div class="support-order-confirm-action support-form__field--full" data-js="support-order-confirm-action">
                  <button type="button" class="support-button support-button--secondary" data-js="support-order-confirm">Confirmar</button>
                </div>

                <div class="support-order-details support-form__field--full" data-js="support-order-details" hidden>
                  <div class="support-order-details__grid" aria-live="polite">
                    <p class="support-order-details__item">
                      <span>Nombre</span>
                      <strong data-js="support-order-name">-</strong>
                    </p>
                    <p class="support-order-details__item">
                      <span>Teléfono</span>
                      <strong data-js="support-order-phone">-</strong>
                    </p>
                    <p class="support-order-details__item">
                      <span>Ciudad</span>
                      <strong data-js="support-order-city">-</strong>
                    </p>
                  </div>

                  <div class="support-order-status" data-js="support-order-status" hidden>
                    <strong data-js="support-order-status-title">-</strong>
                    <p data-js="support-order-status-text">-</p>
                  </div>

                  <div class="support-order-purchase" data-js="support-order-purchase" hidden>
                    <ul class="support-order-purchase__items" data-js="support-order-purchase-items"></ul>
                    <button type="button" class="support-button support-button--primary" data-js="support-order-purchase-button">Comprar instalación</button>
                  </div>

                  <div class="support-order-schedule" data-js="support-order-schedule" hidden>
                    <p class="support-order-observations" data-js="support-order-observations-wrap" hidden>
                      <span>Observaciones</span>
                      <strong data-js="support-order-observations">-</strong>
                    </p>

                    <label class="support-form__field support-form__field--full">
                      <span>Dirección de instalación</span>
                      <input type="text" name="installation_address" autocomplete="street-address" required disabled data-js="support-order-address">
                    </label>

                    <div class="support-order-schedule__grid">
                      <label class="support-form__field">
                        <span>Fecha</span>
                        <input type="date" name="installation_requested_date" required disabled data-js="support-order-schedule-field">
                      </label>

                      <label class="support-form__field">
                        <span>Hora</span>
                        <input type="time" name="installation_requested_time" required disabled data-js="support-order-schedule-field">
                      </label>
                    </div>

                    <p class="support-note">Ingresa una fecha y hora tentativa para la visita. Puedes editar la dirección de instalación, pero no puedes cambiar la ciudad indicada inicialmente al momento de la compra.</p>
                  </div>

                  <div class="support-order-info-request" data-js="support-order-info-request" hidden>
                    <label class="support-form__field support-form__field--full">
                      <span>Observaciones o solicitudes</span>
                      <textarea name="installation_info_message" rows="4" placeholder="Quisiera saber si pueden prestar el servicio de instalación según la ciudad indicada" required disabled data-js="support-order-info-request-field"></textarea>
                    </label>
                    <button type="button" class="support-button support-button--primary" data-js="support-order-info-request-button">Solicitar información</button>
                  </div>
                </div>
              </div>

              <div id="supportSchedulePanelNoOrder" class="support-schedule-fields support-schedule-fields--no-order support-form__field--full" data-js="support-schedule-fields" data-support-schedule-panel="no_order" role="tabpanel" aria-labelledby="supportScheduleTabNoOrder" hidden>
                <label class="support-form__field">
                  <span>Nombre</span>
                  <input type="text" name="contact_name" autocomplete="name" required disabled>
                </label>

                <label class="support-form__field">
                  <span>Correo electrónico</span>
                  <input type="email" name="email" autocomplete="email" required disabled>
                </label>

                <label class="support-form__field">
                  <span>Ciudad</span>
                  <input type="text" name="city" autocomplete="address-level2" required disabled>
                </label>

                <label class="support-form__field">
                  <span>Dirección de instalación</span>
                  <input type="text" name="installation_address" autocomplete="street-address" required disabled>
                </label>

                <label class="support-form__field support-form__field--full">
                  <span>Modelo</span>
                  <select name="product_model" required disabled>
                    <option value="">Selecciona un modelo</option>
                    <?php
                    $support_installation_products = function_exists( 'beslock_get_support_installation_product_options' ) ? beslock_get_support_installation_product_options() : array();
                    foreach ( $support_installation_products as $support_installation_product ) :
                      ?>
                      <option value="<?php echo esc_attr( $support_installation_product['slug'] ); ?>"><?php echo esc_html( $support_installation_product['title'] ); ?></option>
                    <?php endforeach; ?>
                  </select>
                </label>

                <label class="support-form__field support-form__field--full">
                  <span>Comentarios, observaciones y solicitudes</span>
                  <textarea name="installation_message" rows="4" placeholder="Quisiera saber si pueden prestar el servicio de instalación según la ciudad indicada" required disabled></textarea>
                </label>

                <p class="support-note support-form__field--full">Esta solicitud se guardará como consulta pendiente del modelo seleccionado y será revisada antes de publicarse en el histórico de consultas.</p>
              </div>

              <button type="submit" class="support-button support-button--primary is-hidden" data-js="support-schedule-submit" hidden disabled>Programar instalación</button>
              <p class="support-form__message support-form__field--full" data-js="support-schedule-message" hidden></p>
            </form>
          </div>
        </section>

        <section id="supportPanelProjectPurchases" class="support-drawer__panel support-drawer__panel--project" data-js="support-panel" data-support-panel="project-purchases" data-support-title="Compras para proyectos" hidden>
          <div class="support-drawer__content">
            <p class="support-drawer__intro">Solicita una cotización para proyectos residenciales, comerciales, institucionales o compras por volumen.</p>

            <?php // Este flujo aplica especialmente para compras superiores a COP $2.400.000. ?>
            <form class="support-form support-form--grid" data-js="support-project-form" novalidate>
              <label class="support-form__field support-form__field--full">
                <span>Empresa o proyecto</span>
                <input type="text" name="project_name" required>
              </label>

              <label class="support-form__field">
                <span>Nombre de contacto</span>
                <input type="text" name="contact_name" autocomplete="name" required>
              </label>

              <label class="support-form__field">
                <span>Correo electrónico</span>
                <input type="email" name="email" autocomplete="email" required>
              </label>

              <label class="support-form__field">
                <span>Teléfono</span>
                <input type="tel" name="phone" autocomplete="tel" required>
              </label>

              <label class="support-form__field">
                <span>Ciudad</span>
                <input type="text" name="city" required>
              </label>

              <label class="support-form__field support-form__field--full">
                <span>Tipo de proyecto</span>
                <select name="project_type" required>
                  <option value="">Selecciona el tipo de proyecto</option>
                  <option value="hogar">Hogar</option>
                  <option value="comercial">Comercial</option>
                  <option value="constructor">Constructor</option>
                  <option value="hotel">Hotel</option>
                  <option value="oficina">Oficina</option>
                  <option value="institucional">Institucional</option>
                  <option value="otro">Otro</option>
                </select>
              </label>

              <div class="support-project-products support-form__field--full" data-js="support-project-products">
                <div class="support-project-products__header">
                  <span>Modelos</span>
                </div>

                <div class="support-project-products__rows" data-js="support-project-rows">
                  <div class="support-project-row" data-js="support-project-row">
                    <label class="support-form__field">
                      <span>Modelo</span>
                      <select name="product_model[]" required>
                        <option value="">Modelo</option>
                        <option value="e-flex">e-Flex</option>
                        <option value="e-nova">e-Nova</option>
                        <option value="e-touch">e-Touch</option>
                        <option value="e-prime">e-Prime</option>
                        <option value="e-orbit">e-Orbit</option>
                        <option value="e-shield">e-Shield</option>
                      </select>
                    </label>

                    <label class="support-form__field support-form__field--quantity">
                      <span>Cantidad</span>
                      <span class="support-project-qty" data-js="support-project-qty">
                        <button type="button" class="support-project-qty__button" data-js="support-project-qty-minus" aria-label="Disminuir cantidad">−</button>
                        <input class="support-project-qty__input" type="number" name="quantity[]" min="1" step="1" inputmode="numeric" value="1" required aria-label="Cantidad">
                        <button type="button" class="support-project-qty__button" data-js="support-project-qty-plus" aria-label="Aumentar cantidad">+</button>
                      </span>
                    </label>

                    <label class="support-form__field">
                      <span>Ubicación de la instalación</span>
                      <select name="installation_location[]" required>
                        <option value="">Selecciona la ubicación</option>
                        <option value="puerta-principal">Puerta principal</option>
                        <option value="puerta-auxiliar">Puerta auxiliar</option>
                        <option value="acceso-peatonal">Acceso peatonal</option>
                        <option value="puerta-interior">Puerta interior</option>
                        <option value="oficina-recepcion">Oficina o recepción</option>
                        <option value="habitacion">Habitación</option>
                        <option value="bodega-cuarto-tecnico">Bodega o cuarto técnico</option>
                        <option value="otra">Otra ubicación</option>
                      </select>
                    </label>

                    <button type="button" class="support-project-row__remove" data-js="support-remove-product-row" aria-label="Eliminar referencia" hidden>
                      <i class="bi bi-x-lg" aria-hidden="true"></i>
                    </button>
                  </div>
                </div>

                <div class="support-project-products__actions">
                  <button type="button" class="support-button support-button--ghost" data-js="support-add-product-row">Agregar otro modelo</button>
                </div>
              </div>

              <label class="support-checkbox support-form__field--full">
                <input type="checkbox" name="include_installation_quote">
                <span>Incluir cotización de instalación</span>
              </label>

              <label class="support-form__field support-form__field--full">
                <span>Comentarios del proyecto</span>
                <textarea name="project_comments" rows="4"></textarea>
              </label>

              <button type="submit" class="support-button support-button--primary">Solicitar cotización</button>
              <p class="support-form__message support-form__field--full" data-js="support-project-message" hidden></p>
            </form>
          </div>
        </section>
      </div>
    </div>
  </aside>

  <div class="mobile-drawer__backdrop" id="drawerBackdrop" data-js="drawer-backdrop" tabindex="-1" aria-hidden="true"></div>
</nav>
