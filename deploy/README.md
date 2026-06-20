# Deploy limpio para FileZilla

Esta carpeta existe para separar el despliegue FTP de la carpeta de trabajo de Git.

Genera una copia limpia con:

```bash
npm run deploy:build
```

El contenido para subir quedara en:

```text
deploy/current/
```

Sube desde `deploy/current/`, no desde la raiz del repositorio. Esa copia sale de `git archive HEAD`, asi que contiene solo archivos versionados y respeta las exclusiones de `.gitattributes`: no incluye `.git`, `node_modules`, `.tmp`, `.venv`, `database`, archivos de Docker, pruebas, documentacion interna, logs, cache ni otros residuos locales.

Si solo vas a actualizar el tema, usa esta ruta como origen en FileZilla:

```text
deploy/current/wp-content/themes/beslock-custom/
```

Si vas a replicar la implementacion SEO backstage, genera ademas el paquete minimo:

```bash
npm run deploy:seo
```

La salida queda en:

```text
deploy/seo-filezilla/
```

Usa ese paquete cuando necesites subir no solo el theme sino tambien:

- `wp-content/plugins/beslock-seo-config/`
- `wp-content/themes/beslock-custom/data/products.json`
- `wp-content/themes/beslock-custom/data/woocommerce-pricing-import.csv`
- `wp-content/themes/beslock-custom/assets/manuals/`
