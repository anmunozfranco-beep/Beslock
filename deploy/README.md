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

Si vas a replicar la implementacion SEO backstage, no necesitas un segundo paquete ni otra carpeta paralela en `deploy/`.

Sigue usando el mismo deploy unificado:

```bash
npm run deploy:build
```

Y sube desde `deploy/current/` estas rutas:

- Siempre: `deploy/current/wp-content/themes/beslock-custom/`
- Solo si vas a activar o replicar la capa SEO backstage: `deploy/current/wp-content/plugins/beslock-seo-config/`

Importante: los archivos de datos y manuales que necesita el SEO ya viven dentro del theme, así que no tienes que ir seleccionando subcarpetas sueltas adicionales del tema.
