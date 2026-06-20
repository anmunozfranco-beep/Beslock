# Migracion SEO a Produccion por FileZilla

## Objetivo

Reproducir en produccion la capa SEO backstage implementada en local sin depender de configuraciones manuales invisibles.

El impacto esperado es alto porque esta ruta:

- preserva la fuente real de metadatos SEO de productos
- evita reconstruir manualmente la configuracion de SITESEO
- permite repetir el proceso en futuras migraciones con el mismo flujo operativo

## Que necesita produccion

La reproduccion SEO no depende solo del theme. La implementacion actual usa dos capas:

1. `BESLOCK SEO Config`
   Ruta: `wp-content/plugins/beslock-seo-config/`
   Rol: aplica la logica SEO, limpia residuos heredados, sincroniza metadatos y gobierna el flujo desde `Herramientas > BESLOCK SEO`.

2. Fuentes de datos dentro del theme
   Rutas:
   - `wp-content/themes/beslock-custom/data/products.json`
   - `wp-content/themes/beslock-custom/data/woocommerce-pricing-import.csv`
   - `wp-content/themes/beslock-custom/assets/manuals/`

Sin esas fuentes, el plugin no puede reconstruir correctamente titles, meta descriptions, social meta, keywords, exclusiones de sitemap y señales de producto.

## Paquete recomendado

Generar el paquete mínimo con:

```bash
npm run deploy:seo
```

Salida:

```text
deploy/seo-filezilla/
```

El paquete incluye:

- estructura lista para subir por FTP
- `README.md` con el orden operativo
- `checksums.sha256` para verificar integridad
- `packages/beslock-seo-config.zip` si `zip` está disponible en la máquina local

## Orden de migracion

1. Respaldar base de datos y `wp-content/` en produccion.
2. Subir con FileZilla:
   - `deploy/seo-filezilla/wp-content/plugins/beslock-seo-config/`
   - `deploy/seo-filezilla/wp-content/themes/beslock-custom/data/products.json`
   - `deploy/seo-filezilla/wp-content/themes/beslock-custom/data/woocommerce-pricing-import.csv`
   - `deploy/seo-filezilla/wp-content/themes/beslock-custom/assets/manuals/`
3. Si produccion no tiene la misma base del theme local, subir ademas `deploy/current/wp-content/themes/beslock-custom/`.
4. Entrar a WordPress Admin y activar `BESLOCK SEO Config`.
5. Ir a `Herramientas > BESLOCK SEO`.
6. Ejecutar `Ejecutar limpieza + instalar/activar SITESEO Free`.
7. Confirmar:
   - `SITESEO Free` activo
   - `SITESEO PRO` inactivo
   - ultimo mantenimiento sin errores criticos
   - ultimo sync con productos detectados

## Como queda SITESEO

El boton de mantenimiento ahora intenta este flujo:

1. Crear snapshot JSON de la configuracion SEO heredada en `uploads/beslock-seo-config/`.
2. Desactivar `SITESEO Free` y `SITESEO PRO` si existen.
3. Limpiar opciones y metadatos heredados de SITESEO.
4. Instalar `SITESEO Free` desde WordPress.org si no está presente.
5. Activarlo.
6. Re-sembrar la configuracion SEO desde las fuentes internas del proyecto.

## Fallback si la instalacion automatica falla

Puede fallar por permisos de escritura del hosting o por restricciones del entorno. Si ocurre:

1. Subir manualmente el plugin oficial `siteseo/` a `wp-content/plugins/`.
2. Volver a `Herramientas > BESLOCK SEO`.
3. Repetir `Ejecutar limpieza + instalar/activar SITESEO Free`.

## Que no hace falta migrar

- `wp-content/uploads/beslock-seo-config/`
- `test-results/`
- `docs/`
- `scripts/`
- snapshots locales o logs de importacion

## Validacion minima posterior

- revisar `title` y `meta description` en Home y Tienda
- revisar una ficha de producto con `Product` schema
- revisar que `carrito`, `checkout` y `mi cuenta` conserven `noindex`
- revisar que `product_tag` y `users` no vuelvan a aparecer en sitemap
