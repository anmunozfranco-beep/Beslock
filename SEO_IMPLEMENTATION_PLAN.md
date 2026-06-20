# Plan Maestro SEO BESLOCK

## 1. Contexto

BESLOCK está trabajando la estrategia SEO desde un entorno local de WordPress y WooCommerce. La implementación final se trasladará a producción principalmente mediante archivos distribuidos por FileZilla y otras tareas operativas controladas.

Es importante dejar claro que gran parte de la configuración de plugins de WordPress vive en la base de datos, no en archivos del repositorio. Eso significa que cualquier cambio SEO hecho localmente en paneles de administración, opciones de plugin, taxonomías o metadatos no pasa automáticamente a producción si solo se transfieren archivos.

Por esa razón, toda decisión SEO debe quedar documentada y, cuando sea posible, automatizada o replicada mediante un procedimiento claro. El objetivo de este documento es evitar configuraciones invisibles, heredadas o imposibles de auditar.

Principio operativo adicional: cualquier implementación SEO que se apruebe debe diseñarse para poder escalar a producción mediante despliegue de archivos, ejecución de scripts controlados y plugins accesibles desde el área de herramientas de WordPress. El proyecto no debe depender de cambios manuales en local imposibles de reproducir cuando el sitio se migre por FileZilla.

## 2. Diagnóstico inicial

El diagnóstico actual del proyecto deja estos hallazgos principales:

- SITESEO y SITESEO PRO están instalados pero inactivos.
- SITESEO PRO no debe considerarse una compra controlada por el propietario actual; la instalación parece heredada y no es una base fiable para una estrategia sostenible.
- La configuración guardada en SITESEO es casi toda default.
- No hay metadatos personalizados en Home, Tienda, productos ni blog dentro de SITESEO.
- WooCommerce no está correctamente cubierto por la configuración almacenada de SITESEO.
- El sitemap actual presenta problemas de cobertura y calidad.
- Existen páginas legales enlazadas en frontend, pero sin posts o pages reales que respalden esas URLs en WordPress.
- Home tiene múltiples H1 y carece de una jerarquía SEO limpia.
- Hay contenido de prueba publicado, incluyendo entradas y páginas no comerciales.
- Los productos están mal categorizados o dependen de categorías genéricas como `Sin categorizar`.
- El SEO local no cuenta todavía con landings indexables por ciudad.

## 3. Decisión estratégica

La decisión estratégica aprobada para BESLOCK es la siguiente:

- No migrar la configuración heredada de SITESEO.
- Eliminar SITESEO PRO.
- Reconstruir una base limpia con SITESEO Free.
- Usar SITESEO Free como motor SEO principal.
- Considerar más adelante un plugin propio `beslock-seo-config` para aplicar automáticamente la configuración SEO base en producción.
- Priorizar siempre implementaciones escalables a producción por archivos, scripts y herramientas visibles en WordPress.

La razón principal es de control y ROI. La instalación heredada no contiene una capa SEO madura que merezca migración compleja, mientras que una reconstrucción limpia reduce deuda técnica, evita residuos y facilita documentar cada decisión.

## 4. Principio de implementación

La implementación SEO no debe empezar por artículos, backlinks ni escalado de contenido. Primero se corrige la base técnica y comercial del sitio. El principio de trabajo queda definido así:

- Primero limpiar la infraestructura SEO.
- Luego corregir la arquitectura comercial y de WooCommerce.
- Después optimizar las páginas principales de negocio.
- Finalmente crear landings locales y contenidos SEO.

Esto evita empujar tráfico hacia una base con indexación deficiente, señales contradictorias o páginas mal preparadas para convertir.

## 5. Plan por fases

### Fase 1 - Infraestructura SEO

- Respaldar la base de datos y `wp-content`.
- Inventariar y eliminar residuos SITESEO.
- Eliminar SITESEO PRO.
- Instalar SITESEO Free limpio.
- Configurar titles y metas globales.
- Configurar sitemap.
- Configurar indexación.
- Configurar Open Graph y Twitter Cards.
- Configurar schema básico.
- Validar el frontend después de la configuración base.

Resultado esperado: una capa SEO controlada, limpia y coherente, sin dependencias Pro ni residuos heredados.

### Fase 2 - Higiene WordPress

- Eliminar o despublicar `Hello world!`, `TEST POST` y `Sample Page`.
- Corregir las páginas legales para que existan como contenido real gestionable.
- Resolver el producto de instalación que hoy genera ruido o 404 en sitemap.
- Revisar URLs que deben quedar en `noindex`, como carrito, checkout y mi cuenta.
- Limpiar autores, archivos y fechas para evitar indexación basura.

Resultado esperado: menos ruido indexable y menos riesgo de señales de baja calidad.

### Fase 3 - Arquitectura WooCommerce

- Sacar productos de `Sin categorizar`.
- Crear categorías reales con intención comercial.
- Configurar `product categories` y `product tags` con criterio SEO.
- Mejorar breadcrumbs.
- Exponer tienda y categorías en navegación.

Resultado esperado: arquitectura comercial navegable, entendible para Google y útil para el usuario.

### Fase 4 - Home y money pages

- Crear un H1 único y comercial para Home.
- Reducir H1 múltiples.
- Añadir un bloque SEO en Home.
- Optimizar Tienda.
- Optimizar fichas de producto.
- Crear titles y metas para páginas clave.

Resultado esperado: mejor relevancia temática y mejor capacidad de posicionamiento en URLs de intención transaccional.

### Fase 5 - SEO local

- Crear landings para Bogotá, Medellín, Cali y Barranquilla.
- Añadir NAP claro y consistente.
- Añadir schema `LocalBusiness` si aplica al modelo operativo real.
- Conectar las landings con el servicio de instalación.

Resultado esperado: empezar a capturar búsquedas geolocalizadas con intención comercial real en Colombia.

### Fase 6 - Contenido SEO

- Definir una estrategia de contenidos enfocada en español Colombia.
- Crear cluster para `cerraduras inteligentes`.
- Crear cluster para `cerraduras digitales`.
- Crear cluster para `cerraduras con huella`.
- Crear cluster para `cerraduras para Airbnb`.
- Crear cluster para `cerraduras para oficinas`.
- Crear cluster para `cerraduras para puerta principal`.
- Crear cluster para `cerraduras para rejas y portones`.
- Convertir guías y manuales en URLs crawlables y estratégicas.

Resultado esperado: ampliar cobertura semántica sin perder foco comercial.

### Fase 7 - Producción

- Documentar toda la configuración SEO validada en local.
- Decidir si la replicación en producción será manual o mediante plugin.
- Si se crea el plugin `beslock-seo-config`, deberá vivir como herramienta operativa y no como parche improvisado.
- El plugin deberá tener pantalla en `Herramientas > BESLOCK SEO`.
- El plugin deberá aplicar configuración SEO base y generar un reporte antes y después.
- Cualquier script operativo deberá poder ejecutarse de forma controlada y quedar accesible o invocable desde una ruta mantenible del proyecto, idealmente enlazada al flujo de herramientas del sitio.

Resultado esperado: despliegues repetibles y auditables, con menos dependencia de tareas manuales invisibles.

## 6. Arquitectura SEO objetivo

La arquitectura SEO objetivo de BESLOCK debe responder a una prioridad clara: indexar solo activos con intención comercial o valor informacional real, y excluir todo lo que genere ruido, duplicidad o baja calidad.

### Que debe indexarse

- Home como URL principal de marca y categoria.
- Tienda, siempre que funcione como hub comercial real y no como simple listado vacio.
- Categorias de producto con nombre comercial claro y contenido util.
- Productos activos con stock comercial o vigencia real.
- Landings locales por ciudad con propuesta de valor propia.
- Piezas de contenido informacional que respondan a dudas de compra o instalacion.
- Paginas corporativas clave si aportan contexto comercial real, como instalacion o contacto.

### Que no debe indexarse

- Carrito, checkout y mi cuenta.
- Resultados de busqueda interna.
- Archivos de autor.
- Archivos por fecha.
- Paginas de prueba, borradores publicados por error y contenido de relleno.
- Adjuntos o URLs de media sin valor SEO independiente.
- Tags de blog genericos y taxonomias sin curacion.
- Parametros de filtrado, ordenacion o URLs duplicadas.
- URLs legales de baja intencion SEO si solo cumplen funcion regulatoria.

### Estructura objetivo del sitemap

El sitemap objetivo debe ser corto, util y alineado con las URLs que realmente se quieren posicionar.

- `page-sitemap.xml`: Home, Tienda, Contacto, instalacion, landings locales y otras pages estrategicas.
- `product-sitemap.xml`: fichas de producto activas y canonicas.
- `product_cat-sitemap.xml`: categorias comerciales indexables.
- `post-sitemap.xml`: articulos y guias que formen parte de la estrategia editorial.

No deben aparecer en sitemap:

- Carrito, checkout, mi cuenta.
- URLs sin contenido final.
- Taxonomias de poco valor.
- URLs 404, contenido de prueba o endpoints tecnicos.

### Templates de titles

Los templates deben ser simples, escalables y orientados a intencion comercial:

- Home: `Cerraduras inteligentes en Colombia %%sep%% BESLOCK`
- Pagina corporativa: `%%post_title%% %%sep%% BESLOCK`
- Tienda: `Tienda de cerraduras inteligentes %%sep%% BESLOCK`
- Producto: `%%post_title%% %%sep%% BESLOCK`
- Categoria de producto: `%%_category_title%% %%sep%% BESLOCK`
- Landing local: `Cerraduras inteligentes en {ciudad} %%sep%% BESLOCK`
- Articulo: `%%post_title%% %%sep%% BESLOCK`

### Templates de meta descriptions

Las meta descriptions deben reforzar relevancia, cobertura Colombia y propuesta comercial:

- Home: `Descubre cerraduras inteligentes BESLOCK en Colombia. Soluciones de acceso digital para hogar, oficinas y alquileres con instalacion y soporte.`
- Tienda: `Explora la tienda BESLOCK y encuentra cerraduras inteligentes para puertas principales, oficinas, Airbnb y proyectos residenciales en Colombia.`
- Producto: `Conoce %%post_title%% de BESLOCK. Cerradura inteligente con funciones de acceso seguro, ideal para hogares, oficinas y propiedades en Colombia.`
- Categoria de producto: `Explora %%_category_title%% de BESLOCK con modelos pensados para seguridad, comodidad y control de acceso en Colombia.`
- Landing local: `Instalacion y venta de cerraduras inteligentes en {ciudad} con BESLOCK. Soluciones para hogar, oficinas y alquileres de corta estancia.`
- Articulo: `Aprende con BESLOCK sobre %%post_title%% y toma mejores decisiones de seguridad inteligente para tu propiedad en Colombia.`

### Open Graph

- Activar Open Graph globalmente.
- Usar title y description alineados con SEO, pero adaptables a contexto social.
- Usar imagen destacada real por page, producto o articulo.
- Definir imagen fallback de marca para URLs sin imagen propia.
- Mantener nombre de sitio consistente como `BESLOCK`.

### Twitter Cards

- Activar Twitter Cards globalmente.
- Usar formato `summary_large_image`.
- Reutilizar title, description e imagen principal salvo que exista una razon editorial para personalizarlos.

### Schema requerido

El marcado objetivo debe ser util y verificable, no decorativo:

- `Organization` o `LocalBusiness`, segun el modelo operativo final validado.
- `WebSite`.
- `WebPage`.
- `BreadcrumbList`.
- `Product` en fichas de producto.
- `Article` en blog y guias.
- `FAQPage` solo cuando exista una seccion de preguntas real y visible.
- `LocalBusiness` en landings locales solo si el NAP y la cobertura geografica son reales y consistentes.

### Estrategia SEO local

- Crear landings especificas para Bogota, Medellin, Cali y Barranquilla.
- Orientar cada landing a combinaciones de busqueda con intencion comercial, no solo a menciones de ciudad.
- Incluir propuesta de valor local, zonas de cobertura, CTA y relacion con instalacion.
- Enlazar cada landing desde Home, navegacion o secciones de servicio.
- Mantener un NAP consistente en las URLs donde aplique.

### Estrategia WooCommerce

- Usar la pagina de Tienda como hub comercial, no como simple archivo tecnico.
- Convertir `product_cat` en la taxonomia principal indexable.
- Mantener productos con titles, descriptions, breadcrumbs y categorizacion limpios.
- Evitar que productos queden en `Sin categorizar`.
- Priorizar categorias transaccionales antes que tags dispersos.
- Reforzar enlazado interno entre Home, Tienda, categorias y productos.

### Taxonomias objetivo

- `product_cat`: taxonomia principal de WooCommerce e indexable.
- `product_tag`: taxonomia secundaria; por defecto no indexable hasta que exista curacion real.
- `category`: util para blog si se mantiene una estructura editorial consistente.
- `post_tag`: mejor mantener en `noindex` salvo estrategia muy clara.

## 7. Estrategia futura de automatizacion

Se documenta la idea de un plugin propio llamado `beslock-seo-config`. No debe implementarse todavia, pero si debe guiar decisiones futuras de arquitectura operativa.

Objetivos del plugin:

- Aplicar configuracion SEO automaticamente en produccion.
- Evitar configuracion manual repetitiva.
- Permitir despliegues consistentes entre local y produccion.
- Aplicar configuracion SITESEO mediante codigo.
- Servir como capa de migracion reproducible cuando produccion se actualice por FileZilla y no por clonacion completa de base de datos.

Alcance deseado del plugin:

- Definir y aplicar opciones globales base de SITESEO Free.
- Registrar configuraciones objetivo de indexacion, sitemap, social y schema.
- Generar un reporte antes y despues de aplicar cambios.
- Exponer una pantalla operativa en `Herramientas > BESLOCK SEO`.
- Reducir dependencia de pasos invisibles en panel de administracion.
- Ejecutar scripts o rutinas SEO aprobadas desde un punto visible y auditable dentro de WordPress.
- Centralizar acciones de sincronizacion para que local y produccion compartan la misma logica de aplicacion.

Limitaciones deseadas:

- No sustituir la estrategia editorial ni las optimizaciones manuales de contenido.
- No depender de funcionalidades Pro no licenciadas.
- No introducir automatismos opacos que luego no puedan auditarse.

## 8. Registro de decisiones

Bitacora cronologica de decisiones SEO tomadas hasta la fecha:

- `2026-06-20`: Se audita SITESEO y SITESEO PRO en modo solo inspeccion, sin modificar codigo, plugins ni base de datos.
- `2026-06-20`: Se confirma que SITESEO y SITESEO PRO estan instalados pero inactivos.
- `2026-06-20`: Se determina que la configuracion heredada de SITESEO tiene valor muy bajo porque es mayoritariamente default y no contiene una capa SEO curada.
- `2026-06-20`: Se decide no migrar la configuracion heredada de SITESEO.
- `2026-06-20`: Se decide eliminar SITESEO PRO dentro de una limpieza controlada posterior.
- `2026-06-20`: Se decide reconstruir la base SEO con SITESEO Free como motor principal.
- `2026-06-20`: Se establece que la prioridad es limpiar la infraestructura SEO antes de crear contenido nuevo o trabajar backlinks.
- `2026-06-20`: Se establece que WooCommerce debe reorganizarse alrededor de categorias comerciales reales y no de `Sin categorizar`.
- `2026-06-20`: Se establece que el foco geografico del proyecto sera Colombia y el idioma objetivo sera espanol.
- `2026-06-20`: Se decide que el SEO local debe apoyarse en landings indexables por ciudad y no solo en menciones dispersas.
- `2026-06-20`: Se documenta como linea futura la automatizacion mediante un plugin propio `beslock-seo-config`.
- `2026-06-20`: Se crea y amplia este plan maestro como fuente oficial de decisiones y siguientes pasos.
- `2026-06-20`: Se fija como requisito que cualquier cambio SEO relevante debe poder replicarse en produccion por archivos, scripts y herramientas visibles en WordPress, sin depender de ajustes manuales invisibles.

## 9. Reglas de trabajo

Las reglas operativas para el SEO de BESLOCK son:

- No hacer cambios SEO sin registrar la decisión en este documento.
- No activar plugins sin validar impacto técnico y operativo.
- No mezclar configuración Pro si no hay licencia clara y controlada.
- No depender de configuraciones manuales invisibles si se pueden documentar o automatizar.
- Diseñar cada cambio importante para que sea reproducible en producción mediante archivos, scripts o plugins accesibles desde `Herramientas` en WordPress.
- Evitar soluciones que solo funcionen en local o que requieran recordar pasos manuales no auditables al migrar por FileZilla.
- No crear contenido masivo antes de resolver la base técnica.
- Mantener el enfoque en Colombia y español.
- Priorizar intención comercial sobre contenido genérico.

## 10. Plan técnico de limpieza

Esta sección traduce el diagnóstico ya realizado en un plan operativo de limpieza controlada. No implica ejecución inmediata. Su objetivo es dejar definido qué se eliminará, qué debe revisarse antes y en qué orden conviene hacerlo para evitar pérdidas accidentales.

### 10.1. Inventario de elementos a eliminar

#### Plugins

| Elemento | Tipo | Estado actual | Clasificación | Justificación |
|---|---|---|---|---|
| `siteseo-pro` | Plugin | Instalado e inactivo | Seguro eliminar | No está aportando SEO activo, depende de `siteseo`, su configuración útil es mínima y la estrategia aprobada es reconstrucción limpia con Free. |
| `siteseo` | Plugin | Instalado e inactivo | Revisar antes de eliminar | También está heredado e inactivo, pero al ser la base de la reinstalación limpia conviene retirarlo solo dentro del paso controlado de limpieza y reinstalación. |
| `external_updates-siteseo-pro` | Opción/transient asociada a PRO | Presente | Seguro eliminar | Residuo operativo de actualización/licencia, sin valor SEO funcional. |
| `softaculous_pro_license` | Opción de licencia asociada | Presente con estado inconsistente | Revisar antes de eliminar | Está asociada al canal de licencia heredado; conviene documentarla antes de limpiar por si hace falta trazabilidad administrativa. |
| Tablas custom de SITESEO | Base de datos | No detectadas | Sin acción | No existen tablas `wptq_siteseo*` ni tabla de logs de redirección que preservar o limpiar. |

#### Configuración SEO heredada

| Elemento | Alcance | Estado actual | Clasificación | Justificación |
|---|---|---|---|---|
| `siteseo_toggle` | Opción global | Default | Seguro eliminar | Coincide con el instalador y no representa trabajo SEO real. |
| `siteseo_titles_option_name` | Opción global | Casi default | Seguro eliminar | No contiene títulos/metas personalizados útiles y no cubre WooCommerce de forma correcta. |
| `siteseo_social_option_name` | Opción global | Default | Seguro eliminar | Solo activa OG/Twitter de forma genérica. |
| `siteseo_xml_sitemap_option_name` | Opción global | Mínima | Seguro eliminar | No incluye configuración WooCommerce suficiente y será reemplazada por una configuración limpia. |
| `siteseo_advanced_option_name` | Opción global | Default | Seguro eliminar | No contiene decisiones SEO avanzadas relevantes. |
| `siteseo_pro_options` | Opción global | Mínima | Seguro eliminar | Solo conserva el toggle de schema estructurado. |
| `siteseo_auto_schema` | Opción global | Set autogenerado | Revisar antes de eliminar | No parece personalizado, pero conviene compararlo con la arquitectura futura antes de descartarlo definitivamente. |
| `siteseo_version` / `siteseo_pro_version` | Opción técnica | Presente | Seguro eliminar | Solo registra versiones instaladas. |
| `_siteseo_readibility_data` | Postmeta | 7 registros | Seguro eliminar | Artefacto de análisis interno, sin valor SEO operativo. |
| `_siteseo_score` | Postmeta | 2 registros | Seguro eliminar | Valor interno de análisis, no aporta a la reconstrucción. |
| `_siteseo_redirections_type` | Postmeta | 5 registros | Seguro eliminar | No hay destinos configurados ni sistema de redirects activo. |
| `_siteseo_redirections_logged_status` | Postmeta | 5 registros | Seguro eliminar | Residuo incompleto de redirecciones. |
| `_siteseo_robots_primary_cat` | Postmeta | 5 registros | Revisar antes de eliminar | Apunta a `Sin categorizar`, por lo que no tiene valor SEO actual, pero conviene registrarlo antes de purgar. |

#### Contenido de prueba y residuos editoriales

| Elemento | Tipo | Estado actual | Clasificación | Justificación |
|---|---|---|---|---|
| `Hello world!` | Post publicado | Indexable y presente en sitemap | Seguro eliminar | Contenido de prueba clásico de WordPress sin valor comercial. |
| `TEST POST` | Post publicado | Indexable y presente en sitemap | Seguro eliminar | Contenido de prueba explícito, impropio de producción SEO. |
| `Sample Page` | Page publicada | Indexable y presente en sitemap | Seguro eliminar | Página por defecto de WordPress sin rol comercial. |
| `Instalación BESLOCK tipo 2` | Product publicado | En sitemap pero su URL responde 404 | Revisar antes de eliminar | Puede ser un servicio real mal modelado; requiere decisión entre corregirlo o retirarlo. |
| `Privacy Policy` | Page en draft | No publicada | Revisar antes de eliminar | Puede ser residuo del instalador o base para una legal real. |
| `Política de devoluciones y reembolsos` | Page en draft | No publicada | Revisar antes de eliminar | Puede reutilizarse como legal real si encaja con operación y cumplimiento. |
| `info_prod_catlg_generator.zip` | Attachment privado | No indexable | Revisar antes de eliminar | Parece utilitario interno, no SEO, pero conviene validar si alguien lo usa antes de limpiarlo. |

### 10.2. Inventario de URLs problemáticas

| Tipo | URL o patrón | Origen detectado | Estado actual | Riesgo | Tratamiento recomendado |
|---|---|---|---|---|---|
| `404 en sitemap` | `/producto/instalacion-beslock-tipo-2/` | `wp-sitemap-posts-product-1.xml` | `404` | Alto | Revisar si el servicio debe existir como producto público; si no, retirarlo de indexación y del sitemap. |
| `Soft 404` | `/terminos-y-condiciones/` | Enlace interno en footer y handler del tema | `200` con título `No se encontró la página` | Alto | Crear página legal real o excluirla de señales SEO mientras se resuelve. |
| `Soft 404` | `/politica-de-privacidad/` | Enlace interno en footer y handler del tema | `200` con título `No se encontró la página` | Alto | Crear página legal real o excluirla de señales SEO mientras se resuelve. |
| `URL utilitaria sin valor SEO` | `/consulta-pedido/` | Enlace interno y regla custom del tema | `200` | Medio | Mantener funcional si es útil al usuario, pero tratarla como candidata a `noindex`. |
| `Indexable de prueba` | `/sample-page/` | `wp-sitemap-posts-page-1.xml` | `200` | Alto | Eliminar o despublicar. |
| `Indexable de prueba` | `/2025/11/17/hello-world/` | `wp-sitemap-posts-post-1.xml` | `200` | Alto | Eliminar o despublicar. |
| `Indexable de prueba` | `/2026/05/06/test-post/` | `wp-sitemap-posts-post-1.xml` | `200` | Alto | Eliminar o despublicar. |
| `Noindex requerido` | `/carrito/` | Página WooCommerce | `200` con `noindex, follow` | Bajo | Mantener fuera del índice. |
| `Noindex requerido` | `/finalizar-compra/` | Página WooCommerce | `200`, resuelve a carrito y conserva `noindex, follow` | Medio | Mantener fuera del índice y revisar el flujo/redirect. |
| `Noindex requerido` | `/mi-cuenta/` | Página WooCommerce | `200` con `noindex, follow` | Bajo | Mantener fuera del índice. |
| `Noindex requerido` | `/?s=cerradura` | Búsqueda interna | `200` con `noindex, follow` | Bajo | Mantener fuera del índice. |
| `Noindex recomendado` | `/author/beslock-co/` | `wp-sitemap-users-1.xml` | `200`, indexable | Medio | Excluir author archives del índice y del sitemap efectivo. |
| `Noindex recomendado` | `/author/daniel/` | `wp-sitemap-users-1.xml` | `200`, indexable | Medio | Excluir author archives del índice y del sitemap efectivo. |
| `Noindex recomendado` | `/author/nasentons5889gmail-com/` | `wp-sitemap-users-1.xml` | `200`, indexable | Medio | Excluir author archives del índice y del sitemap efectivo. |
| `Noindex recomendado` | `/2026/04/` | Archivo por fecha | `200`, indexable | Medio | Excluir date archives del índice. |
| `Noindex recomendado` | `/2025/11/` | Archivo por fecha | `200`, indexable | Medio | Excluir date archives del índice. |
| `Taxonomía de poco valor` | `/etiqueta-producto/wifi/` | `wp-sitemap-taxonomies-product_tag-1.xml` | En sitemap | Medio | No indexar `product_tag` hasta tener una estrategia de facetas o contenido real asociado. |
| `Taxonomía de poco valor` | `/etiqueta-producto/huella/` | `wp-sitemap-taxonomies-product_tag-1.xml` | En sitemap | Medio | Igual que arriba. |
| `Taxonomía de poco valor` | `/etiqueta-producto/app/` | `wp-sitemap-taxonomies-product_tag-1.xml` | En sitemap | Medio | Igual que arriba. |
| `Taxonomía débil` | `/categoria-producto/sin-categorizar/` | `wp-sitemap-taxonomies-product_cat-1.xml` | En sitemap | Alto | Vaciar y retirar esta categoría del modelo comercial. |
| `Taxonomía editorial débil` | `/category/uncategorized/` | `wp-sitemap-taxonomies-category-1.xml` | En sitemap | Medio | Desactivar o vaciar `Uncategorized` si no forma parte de la estrategia editorial. |

Nota operativa: la Home enlaza directamente `/terminos-y-condiciones/`, `/politica-de-privacidad/` y `/consulta-pedido/` desde el footer del tema. El sitemap actual también expone `product_tag` y `users`, lo que amplía la superficie indexable de baja calidad.

### 10.3. Auditoría de taxonomías WooCommerce

#### Categorías actuales

| Categoría | Productos asociados | Estado | Clasificación | Justificación |
|---|---|---|---|---|
| `Cerraduras Inteligentes` | `e-Flex` | Uso muy bajo | Conservar | Es la mejor categoría semilla para la arquitectura comercial. |
| `Residencial` | `e-Nova` | Uso muy bajo | Conservar | Tiene intención comercial válida, aunque hoy está infrautilizada. |
| `Sin categorizar` | `e-Shield`, `e-Prime`, `e-Orbit`, `e-Touch` y además aparece asociado `Instalación BESLOCK tipo 2` en el cruce de productos publicados | Dominante y deficiente | Eliminar | No aporta semántica ni navegación útil; además concentra parte del catálogo por defecto. |

Nota: el contador nativo de la taxonomía devuelve `4` para `Sin categorizar`, pero al cruzar productos publicados aparece también `Instalación BESLOCK tipo 2`. Esto refuerza que el modelado actual requiere revisión manual antes de ejecutar cambios.

#### Etiquetas actuales

| Etiqueta | Uso actual | Relevancia | Clasificación | Justificación |
|---|---|---|---|---|
| `Huella` | `e-Flex` | Alta como atributo comercial | Conservar | Tiene sentido como rasgo funcional de producto. |
| `Wifi` | `e-Flex` | Media-alta | Fusionar | Conviene normalizarla a una taxonomía/etiqueta de conectividad consistente. |
| `App` | `e-Nova` | Media | Fusionar | Debe estandarizarse dentro de una lógica de control por app, no quedar como etiqueta aislada. |
| `smart` | Sin productos asociados | Baja | Eliminar | Está vacía y no aporta estructura ni búsqueda útil. |

### 10.4. Arquitectura WooCommerce propuesta

No se implementa en esta fase. Esta es la estructura inicial recomendada para alinear catálogo, intención de búsqueda y navegación comercial.

#### Categorías principales propuestas

| Categoría propuesta | Rol | Justificación |
|---|---|---|
| `Cerraduras inteligentes` | Categoría madre | Resume el core del catálogo y coincide con la keyword comercial principal. |
| `Instalación` | Categoría o servicio separado | El catálogo ya contiene un servicio de instalación; necesita modelado explícito y no debe quedar mezclado como producto roto. |
| `Accesorios` | Reservada para crecimiento | Solo debe activarse cuando existan SKUs reales; se documenta ahora para evitar improvisación futura. |

#### Subcategorías sugeridas

| Subcategoría | Parent | Justificación |
|---|---|---|
| `Residencial` | `Cerraduras inteligentes` | Ya existe como categoría y encaja con la demanda principal de hogar. |
| `Para oficinas` | `Cerraduras inteligentes` | Responde a intención comercial B2B sin obligar a abrir una categoría madre separada todavía. |
| `Para Airbnb` | `Cerraduras inteligentes` | Tiene alto valor comercial y puede conectar con la estrategia local y de contenidos. |
| `Puerta principal` | `Cerraduras inteligentes` | Captura intención de uso muy frecuente en búsqueda. |
| `Exteriores` | `Cerraduras inteligentes` | Solo si el catálogo real soporta productos aptos para este caso; documentada como subcategoría potencial. |
| `Interiores` | `Cerraduras inteligentes` | Igual que arriba, solo si el catálogo real lo justifica. |

#### Etiquetas sugeridas

| Etiqueta sugerida | Tipo de señal | Justificación |
|---|---|---|
| `Huella` | Funcionalidad | Relevante para búsqueda comercial y comparación de producto. |
| `Control por app` | Funcionalidad | Estandariza el concepto hoy repartido en `App`. |
| `WiFi` | Conectividad | Útil como atributo secundario. |
| `Código` | Método de acceso | Escalable si el catálogo tiene teclados o pines. |
| `Tarjeta` | Método de acceso | Igual que arriba, solo si existe soporte real. |
| `Instalación disponible` | Servicio | Ayuda a conectar producto y servicio sin convertirlo en categoría principal. |

Decisión de modelado: para el tamaño actual del catálogo conviene una arquitectura contenida, con una categoría madre sólida y pocas subcategorías basadas en intención de compra. Las funcionalidades deben vivir preferentemente como etiquetas o atributos, no como categorías top-level.

### 10.5. Auditoría H1

| URL | Estado | Número de H1 | Hallazgo | Riesgo SEO |
|---|---:|---:|---|---|
| `/` | `200` | `7` | Múltiples H1 y además `e-Flex` se repite | Alto |
| `/tienda/` | `200` | `0` | Falta H1 visible en la página de tienda | Alto |
| `/producto/e-flex/` | `200` | `1` | H1 correcto | Bajo |
| `/producto/e-nova/` | `200` | `1` | H1 correcto | Bajo |
| `/producto/e-orbit/` | `200` | `1` | H1 correcto | Bajo |
| `/producto/e-prime/` | `200` | `1` | H1 correcto | Bajo |
| `/producto/e-shield/` | `200` | `1` | H1 correcto | Bajo |
| `/producto/e-touch/` | `200` | `1` | H1 correcto | Bajo |

Conclusión: el problema H1 es estructural en Home y Tienda, no en las fichas de producto. La prioridad es crear un único H1 comercial en Home y restituir un H1 claro en Tienda antes de escalar contenidos.

### 10.6. Preparación para SITESEO Free

Checklist técnico futuro, sin ejecutar todavía:

#### Configuración global

- Definir título y meta description de Home.
- Definir templates para `page`, `post`, `product` y `product_cat`.
- Excluir plantillas irrelevantes o no comerciales del índice.

#### Sitemap

- Mantener `page`, `post`, `product` y `product_cat`.
- Excluir `product_tag`, `author` y archivos de fecha.
- Confirmar que no entren URLs 404, pages utilitarias ni pruebas.

#### Indexación

- `index`: Home, Tienda, productos válidos, categorías útiles, landings locales y contenidos estratégicos.
- `noindex`: carrito, checkout, mi cuenta, búsqueda, autor, fecha, pruebas, tags débiles y URLs legales problemáticas mientras no sean páginas reales.

#### Open Graph

- Activar globalmente.
- Definir fallback de imagen de marca.
- Revisar que Home, Tienda y productos hereden imagen adecuada.

#### Twitter Cards

- Activar globalmente.
- Usar `summary_large_image`.
- Heredar metadatos principales salvo excepciones editoriales.

#### Schema

- Activar `WebSite`, `WebPage`, `BreadcrumbList` y `Product`.
- Añadir `Article` en blog.
- Evaluar `Organization` o `LocalBusiness` según operación real.

#### WooCommerce

- Añadir templates específicos para `product` y `product_cat`.
- Revisar breadcrumbs.
- Alinear sitemap e indexación con la nueva arquitectura de categorías.
- No indexar `product_tag` hasta que tenga lógica real.

### 10.7. Orden recomendado de ejecución

1. Crear respaldo de base de datos y `wp-content`.
2. Exportar o registrar evidencia de opciones y residuos heredados para trazabilidad.
3. Validar qué hacer con `Instalación BESLOCK tipo 2`, legales draft y licencia heredada.
4. Despublicar o retirar contenido de prueba evidente: `Hello world!`, `TEST POST`, `Sample Page`.
5. Corregir o retirar URLs legales soft 404 y decidir el tratamiento de `/consulta-pedido/`.
6. Limpiar residuos SITESEO PRO y luego SITESEO dentro de una ventana controlada.
7. Instalar o reinstalar SITESEO Free limpio.
8. Configurar indexación, templates, sitemap, social y schema.
9. Reorganizar categorías y etiquetas de WooCommerce.
10. Corregir H1 y arquitectura de Home y Tienda.
11. Validar sitemap, metas, robots y respuestas HTTP en frontend.
12. Solo después, iniciar landings locales y producción de contenido SEO.

Dependencias críticas:

- No eliminar SITESEO ni SITESEO PRO antes de tener respaldo.
- No reconfigurar sitemap antes de definir qué URLs seguirán vivas.
- No abrir landings locales ni contenido nuevo antes de corregir base indexable y taxonomías.
- No aprobar implementaciones SEO nuevas si no existe un camino claro para llevarlas a producción mediante archivos, scripts o herramientas accesibles desde WordPress.

### 10.8. Estimación

| Bloque | Impacto | Esfuerzo | Prioridad | Motivo |
|---|---|---|---|---|
| Limpieza de residuos SITESEO/SITESEO PRO | Alto | Medio | Alta | Reduce deuda técnica y evita arrastrar configuración sin valor. |
| Limpieza de contenido de prueba | Alto | Bajo | Alta | Saca del índice activos que degradan calidad percibida. |
| Corrección de URLs problemáticas y soft 404 | Alto | Medio | Alta | Afecta indexación, confianza y calidad de sitemap. |
| Reorganización de taxonomías WooCommerce | Alto | Medio | Alta | Mejora navegación, semántica y arquitectura comercial. |
| Configuración limpia de SITESEO Free | Alto | Medio | Alta | Establece la nueva base SEO operativa. |
| Corrección H1 Home/Tienda | Medio-alto | Bajo | Alta | Impacto directo en jerarquía y relevancia on-page. |
| Estrategia local y landings | Alto | Medio-alto | Media | Gran potencial, pero depende de tener la base técnica estable. |
| Nuevos clusters de contenido | Medio | Alto | Media | Debe venir después de ordenar la base comercial y técnica. |

### 10.9. Checklist ejecutable

- Confirmar respaldo completo de base de datos.
- Confirmar respaldo de `wp-content`.
- Registrar snapshot de opciones y postmeta SITESEO.
- Validar decisión sobre `Instalación BESLOCK tipo 2`.
- Validar decisión sobre `Privacy Policy` y `Política de devoluciones y reembolsos`.
- Despublicar o eliminar `Hello world!`.
- Despublicar o eliminar `TEST POST`.
- Despublicar o eliminar `Sample Page`.
- Resolver `/terminos-y-condiciones/`.
- Resolver `/politica-de-privacidad/`.
- Decidir tratamiento `noindex` de `/consulta-pedido/`.
- Retirar author archives del índice.
- Retirar date archives del índice.
- Retirar `product_tag` del índice y sitemap si no hay estrategia real.
- Vaciar y eliminar `Sin categorizar`.
- Reasignar productos a categorías comerciales válidas.
- Limpiar residuos de SITESEO PRO.
- Limpiar residuos de SITESEO heredado.
- Instalar o reinstalar SITESEO Free limpio.
- Aplicar configuración base de titles, metas, sitemap, indexación, OG, Twitter Cards y schema.
- Validar Home, Tienda, productos, sitemap y robots en frontend.

## 11. Estado actual

Estado actual del proyecto:

- Documento maestro creado.
- Auditoría SITESEO completada.
- Arquitectura SEO objetivo documentada.
- Plan técnico de limpieza documentado.
- Implementación backstage SEO ejecutada localmente mediante plugin propio reproducible por archivos.
- Decisión tomada: reconstrucción limpia con SITESEO Free.
- Requisito operativo documentado: los cambios SEO deben ser escalables a producción por archivos, scripts y herramientas visibles en WordPress.
- Plugin operativo creado en `wp-content/plugins/beslock-seo-config/`.
- Plugin activado y validado en local.
- Flujo de limpieza e instalación limpia de SITESEO Free implementado en `Herramientas > BESLOCK SEO`.
- Snapshot técnico de SITESEO generado antes de la limpieza en `wp-content/uploads/beslock-seo-config/`.
- Metadatos SEO sincronizados para Home, Tienda, productos y taxonomías WooCommerce actuales.
- SITESEO Free activo y gobernando `title`, `meta description`, canonical y social meta.
- Sitemap core de WordPress limpiado de `users`, `product_tag`, páginas transaccionales, contenido de prueba y producto oculto de instalación.
- Schema `Organization`, `WebSite`, `Product` y `BreadcrumbList` validado en local con convivencia controlada con SITESEO Free.
- Limpieza ejecutada de residuos SITESEO heredados en local.
- Pendiente: repetir el mismo flujo en producción despues de subir archivos y validar respaldo previo.

## 12. Proximo paso sugerido

`Subir el plugin BESLOCK SEO Config a producción, activarlo y ejecutar desde Herramientas > BESLOCK SEO la acción "Ejecutar limpieza + activar SITESEO Free" dentro de una ventana controlada con respaldo previo.`

## 13. Implementacion ejecutada

### 13.1. Plugin creado

- Ruta: `wp-content/plugins/beslock-seo-config/`
- Archivo loader: `wp-content/plugins/beslock-seo-config/beslock-seo-config.php`
- Lógica principal: `wp-content/plugins/beslock-seo-config/includes/class-beslock-seo-config.php`
- Pantalla operativa: `Herramientas > BESLOCK SEO`

### 13.2. Fuentes conectadas

El plugin toma la informacion SEO desde fuentes existentes del proyecto, sin tocar el contenido visible del frontend:

- `wp-content/themes/beslock-custom/data/products.json`
- `wp-content/themes/beslock-custom/assets/manuals/index.json`
- `wp-content/themes/beslock-custom/assets/manuals/products/*.json`
- `wp-content/themes/beslock-custom/data/woocommerce-pricing-import.csv`

### 13.3. Capas SEO implementadas

- Sincronizacion de `title`, `meta description`, Open Graph y Twitter Cards para Home, Tienda y productos.
- Sincronizacion de metadatos equivalentes compatibles con SITESEO (`_siteseo_titles_*`, `_siteseo_social_*`, `_siteseo_analysis_target_kw`).
- Flujo operativo de limpieza e instalacion limpia de SITESEO Free desde `Herramientas > BESLOCK SEO`.
- Snapshot JSON previo a la limpieza en `wp-content/uploads/beslock-seo-config/`.
- Sincronizacion de reglas `noindex` backstage para:
  - `Hello world!`
  - `TEST POST`
  - `Sample Page`
  - `Carrito`
  - `Finalizar compra`
  - `Mi cuenta`
  - producto oculto de instalación
  - `product_tag`
  - `Sin categorizar`
  - author, date, search y attachment pages por regla runtime
- Limpieza del sitemap nativo de WordPress para excluir:
  - `users`
  - `product_tag`
  - `Sin categorizar`
  - páginas transaccionales
  - contenido de prueba
  - producto oculto de instalación
- Generacion de schema en frontend head sin modificar plantillas visibles:
  - `Organization`
  - `WebSite`
  - `Product`
  - `BreadcrumbList`
- Convivencia controlada con SITESEO Free:
  - SITESEO Free gobierna `title`, `meta description`, canonical, Open Graph y Twitter Cards.
  - BESLOCK SEO Config gobierna el schema curado (`Organization`, `WebSite`, `Product`, `BreadcrumbList`).
  - El JSON-LD `Organization` nativo de SITESEO se suprime para evitar duplicidades y señal débil heredada.
- Normalizacion de `alt` en imágenes de producto actualmente enlazadas por WooCommerce.
- Compatibilidad con despliegue por archivos:
  - sync manual desde `Herramientas`
  - sync en activacion
  - sync diario por cron
  - sync automatico cuando cambia la version o el hash de fuentes y entra un administrador

### 13.4. Validacion local completada

Verificado en `http://localhost:8080`:

- Flujo `limpieza + activar SITESEO Free` ejecutado sin errores.
- Snapshot creado en `wp-content/uploads/beslock-seo-config/siteseo-snapshot-20260620-123523.json`.
- Limpieza ejecutada con estos resultados:
  - 10 opciones heredadas eliminadas
  - 150 registros `postmeta` SITESEO heredados eliminados
  - 103 registros `termmeta` SITESEO heredados eliminados
- SITESEO Free queda activo y SITESEO PRO queda inactivo.
- Home con `title`, `description`, OG/Twitter y schema actualizados.
- Tienda con `title`, `description`, OG/Twitter actualizados.
- Productos `e-Flex` y `e-Shield` con snippets SEO y schema `Product`.
- `Carrito` conserva `noindex` y ya no emite schema `Organization`.
- `wp-sitemap.xml` ya no publica `users` ni `product_tag`.
- `wp-sitemap-posts-page-1.xml` solo publica Home y Tienda.
- `wp-sitemap-posts-product-1.xml` ya no publica `Instalación BESLOCK tipo 2`.
- `wp-sitemap-taxonomies-product_cat-1.xml` ya no publica `Sin categorizar`.

### 13.5. Pendientes despues de esta implementacion

- Reorganizacion real de categorías y etiquetas WooCommerce.
- Decidir tratamiento final del blog indexable heredado.
- Migrar el plugin a producción por archivos y ejecutar el mismo flujo desde `Herramientas > BESLOCK SEO`.
- Validar respaldo, ventana de mantenimiento y checklist final antes de repetir la limpieza en producción.

### 13.6. Paquete de migracion por FileZilla

Para no romper el flujo operativo habitual, la migracion queda unificada en el mismo deploy de siempre:

- Generador local: `npm run deploy:build`
- Salida: `deploy/current/`
- Guia operativa: `docs/SEO_FILEZILLA_PRODUCTION_MIGRATION.md`

Rutas a subir por FileZilla:

- Siempre: `deploy/current/wp-content/themes/beslock-custom/`
- Adicional solo para replicar SEO backstage: `deploy/current/wp-content/plugins/beslock-seo-config/`

Nota operativa: `products.json`, `woocommerce-pricing-import.csv` y `assets/manuals/` ya viven dentro del theme, asi que no hace falta seleccionarlos por separado.

Actualizacion del flujo:

- `Herramientas > BESLOCK SEO` ahora intenta instalar `SITESEO Free` desde WordPress.org si el plugin no existe todavia en `wp-content/plugins/`.
- Si el hosting bloquea la instalacion automatica, el fallback es subir manualmente `siteseo/` y repetir la accion desde `Herramientas`.
