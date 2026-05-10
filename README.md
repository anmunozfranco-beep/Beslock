# Beslock

Custom WooCommerce platform for BESLOCK, built on WordPress + Kadence with a modular product synchronization architecture powered by JSON-driven portfolio data, automated product and media sync, and a reproducible local Docker environment.

## Local Docker stack

The repository ships with a minimal Docker Compose stack for local development:

- WordPress: `http://localhost:8080`
- phpMyAdmin: `http://localhost:8081`
- MySQL: `localhost:3306`

The bootstrap is designed for a production SQL dump stored locally at `database/andres38_wp718.sql`. That dump is intentionally kept out of Git.

> **Prefer a cloud environment?** See [GitHub Codespaces](#github-codespaces) below — the `.devcontainer/` configuration lets you run the full stack in a browser without installing anything locally.

### Services

- `wordpress` using `wordpress:php8.2-apache`
- `mysql` using `mysql:8.0`
- `phpmyadmin` using `phpmyadmin/phpmyadmin`
- `wpcli` using `wordpress:cli-php8.2` for post-import bootstrap tasks

### Files and directories

```text
Beslock/
├── docker-compose.yml
├── .env
├── Makefile
├── database/
├── wp-config-sample.php
├── wp-content/
├── data/
├── docker/
│   ├── bootstrap-wordpress.sh
│   ├── mysql-init/
│   ├── uploads.ini
│   ├── wp-config-docker.php
│   └── wordpress-entrypoint.sh
└── README.md
```

### Why this layout works

- `wp-content/` is mounted directly from the repository, so theme and plugin development happens against the real codebase.
- WordPress core and generated runtime files live in a named Docker volume for stable local persistence.
- MySQL data lives in its own named volume so the production SQL is imported only on first bootstrap and persists across restarts.
- The default local table prefix is `wptq_`, matching the current site configuration and making production SQL imports safer.
- A one-shot `wpcli` bootstrap runs `search-replace` from `https://beslock.com.co` to `http://localhost:8080` after the import.

## GitHub Codespaces

The repository ships with a `.devcontainer/` configuration so the full stack can
be opened and used directly in [GitHub Codespaces](https://github.com/features/codespaces)
without any local Docker or tooling requirement.

### Opening in Codespaces

1. On the repository page, click **Code → Codespaces → Create codespace on this branch**.
2. The devcontainer will build automatically and:
   - detect the Codespaces-forwarded URL for port 8080,
   - update `WORDPRESS_LOCAL_URL` in `.env` accordingly,
   - run `make fresh` to import the SQL dump and bootstrap WordPress.
3. After ~1-2 minutes the **PORTS** panel will show port 8080 (WordPress) and
   port 8081 (phpMyAdmin) as forwarded.  Click the 🌐 globe icon next to port
   8080 to open WordPress.

> **SQL dump:** if `database/andres38_wp718.sql` is not present in the
> repository the import step is skipped and WordPress shows its installer.
> Add the dump and run `make fresh` inside the Codespace terminal to complete
> the bootstrap.

### URL handling in Codespaces

Codespaces forwards port 8080 to a public HTTPS URL
(`https://<codespace-name>-8080.preview.app.github.dev`).  The `post-create`
script sets `WORDPRESS_LOCAL_URL` to that URL so WordPress redirects and admin
links resolve correctly from the browser.

If you ever need to apply the URL update manually (e.g. after changing the
`.env`), run:

```bash
bash .devcontainer/post-create.sh
```

### Resuming a Codespace

When a Codespace is resumed after being stopped, the `postStartCommand` runs
`docker compose up -d` automatically to restart all services.

### Useful commands inside the Codespace

```bash
make logs     # tail Docker Compose logs
make fresh    # tear down + re-import SQL dump from scratch
make up       # start services
make down     # stop services
```

---

## Quick start

1. Put the production dump at `database/andres38_wp718.sql`.

2. Bootstrap the environment from scratch:

	```bash
	make fresh
	```

	Equivalent manual commands:

	```bash
	docker compose down -v
	docker compose up -d
	```

3. For subsequent starts, use:

	```bash
	docker compose up -d
	```

	Or with Make:

	```bash
	make up
	```

4. Open WordPress at `http://localhost:8080`.
5. Open phpMyAdmin at `http://localhost:8081`.
6. Validate WooCommerce, Kadence, `beslock-custom`, and sync-related plugins.

## Automatic database bootstrap

- The SQL dump is imported by MySQL automatically through `docker-entrypoint-initdb.d`.
- The import runs only when `mysql_data` is empty.
- If you need to re-import from scratch, run `make fresh` or `docker compose down -v` before `docker compose up -d`.
- The local post-import bootstrap uses WP-CLI to run a safe serialized-data-aware search-replace:

```text
https://beslock.com.co -> http://localhost:8080
```

- It also updates `home` and `siteurl` to the local URL.
- It reconciles the legacy `portfolio-product-sync` active-plugin slug from older dumps with the current `beslock-product-sync` plugin when that plugin exists on disk.

## Environment variables

The local stack uses `.env`:

```env
WORDPRESS_DB_NAME=beslock
WORDPRESS_DB_USER=beslock
WORDPRESS_DB_PASSWORD=beslock
WORDPRESS_DB_HOST=mysql
MYSQL_ROOT_PASSWORD=root
WORDPRESS_TABLE_PREFIX=wptq_
WORDPRESS_LOCAL_URL=http://localhost:8080
WORDPRESS_PRODUCTION_URL=https://beslock.com.co
WP_ENVIRONMENT_TYPE=local
```

## Docker WordPress config

- The running containers use `docker/wp-config-docker.php` instead of the local production `wp-config.php`.
- The Docker config keeps the same table prefix (`wptq_`) but swaps DB access to container variables.
- Local config disables the production secure-cookie assumptions that would break plain HTTP on `localhost`.

## Upload limits

PHP upload settings are defined in `docker/uploads.ini`:

```ini
file_uploads = On
memory_limit = 512M
upload_max_filesize = 256M
post_max_size = 256M
max_execution_time = 300
```

## Make targets

- `make up`
- `make down`
- `make fresh`
- `make logs`
- `make restart`

## Project structure

- `wp-content/themes/beslock-custom`: Kadence child theme customizations.
- `wp-content/plugins/beslock-product-sync`: Deterministic JSON-driven WooCommerce product sync.
- `data/products.json`: filesystem source of product data consumed by sync.

## Notes for new developers

- Do not commit production SQL dumps. The `database/` directory is reserved for local bootstrap only.
- If the site comes up on the WordPress installer, the dump was not imported or the MySQL volume was reused from an empty bootstrap. Run `make fresh`.
- `beslock-product-sync` is the current local JSON sync plugin. Older SQL dumps may still reference the legacy `portfolio-product-sync` slug, and the local bootstrap normalizes that automatically.

## Architecture conventions

- Mobile-first CSS with explicit BEM component naming.
- Lightweight vanilla JavaScript for deterministic storefront behavior.
- WordPress and WooCommerce customization lives in child theme overrides and small dedicated plugins.
- Product synchronization remains filesystem-driven to avoid manual drift from admin-only workflows.
