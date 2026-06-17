# BESLOCK recovery tools

Este directorio viaja con el tema para que las herramientas criticas de recuperacion no dependan de carpetas externas del repositorio.

## Herramientas activas desde WordPress

El menu de WordPress en `Herramientas` carga primero estos archivos dentro del tema:

- `portfolio/CSV_portfolio_generator.php`
- `portfolio/fix-placeholder-images.php`

`Cargar Portfolio Data` vive directamente en:

- `inc/admin/portfolio-data.php`

Ese archivo lee `data/products.json`, crea o actualiza productos de WooCommerce, importa imagenes desde `assets/images`, sincroniza atributos y genera CSV cuando se marca esa opcion en la pantalla.

## Copia de plugin para emergencia

La carpeta:

- `plugins/beslock-portfolio-exporter/`

contiene una copia completa del plugin `Beslock Portfolio Exporter`. El tema la carga como fallback en admin solo cuando el plugin externo no ha cargado sus funciones. Si el plugin activo ya existe en `wp-content/plugins`, WordPress lo carga antes que el tema y el fallback interno no se incluye, evitando conflicto.

En una restauracion completa, si falta el plugin activo, copia esta carpeta a:

```text
wp-content/plugins/beslock-portfolio-exporter/
```

y activalo desde WordPress si prefieres administrarlo como plugin independiente. Incluso sin activarlo, el tema puede exponer la pagina de herramientas como fallback. Esta copia permite exportar productos a JSON/SQLite, cargar productos, cargar imagenes y deshacer cambios con el backup mas reciente.

## Diagnostico rapido

La pantalla `Herramientas > Cargar Portfolio Data` muestra un estado de recuperacion con:

- disponibilidad de WooCommerce
- existencia y conteo de `data/products.json`
- disponibilidad del importador del tema
- disponibilidad del generador CSV interno
- existencia de la copia del plugin exportador
- existencia de backups de portfolio
