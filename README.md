# Beslock

Custom WooCommerce platform for BESLOCK, built on WordPress + Kadence with a modular product synchronization architecture powered by JSON-driven portfolio data, automated product and media sync, and a reproducible local Docker environment.

## Local Docker stack

The repository ships with a minimal Docker Compose stack for local development:

- WordPress: `http://localhost:8080`
- phpMyAdmin: `http://localhost:8081`
- MySQL: `localhost:3306`

### Services

- `wordpress` using `wordpress:php8.2-apache`
- `mysql` using `mysql:8.0`
- `phpmyadmin` using `phpmyadmin/phpmyadmin`

### Files and directories

```text
Beslock/
├── docker-compose.yml
├── .env
├── Makefile
├── wp-config-sample.php
├── wp-content/
├── data/
├── docker/
│   └── uploads.ini
└── README.md
```

### Why this layout works

- `wp-content/` is mounted directly from the repository, so theme and plugin development happens against the real codebase.
- WordPress core and generated runtime files live in a named Docker volume for stable local persistence.
- MySQL data lives in its own named volume so you can import production SQL and keep it across restarts.
- The default local table prefix is `wptq_`, matching the current site configuration and making production SQL imports safer.

## Quick start

1. Start the environment:

	```bash
	docker compose up -d
	```

	Or with Make:

	```bash
	make up
	```

2. Open WordPress at `http://localhost:8080`.
3. Open phpMyAdmin at `http://localhost:8081`.
4. Import the production SQL into the `beslock` database.
5. Validate WooCommerce, Kadence, `beslock-custom`, and sync-related plugins.

## Environment variables

The local stack uses `.env`:

```env
WORDPRESS_DB_NAME=beslock
WORDPRESS_DB_USER=beslock
WORDPRESS_DB_PASSWORD=beslock
WORDPRESS_DB_HOST=mysql
MYSQL_ROOT_PASSWORD=root
WORDPRESS_TABLE_PREFIX=wptq_
```

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
- `make logs`
- `make restart`

## Project structure

- `wp-content/themes/beslock-custom`: Kadence child theme customizations.
- `wp-content/plugins/beslock-product-sync`: Deterministic JSON-driven WooCommerce product sync.
- `data/products.json`: filesystem source of product data consumed by sync.

## Architecture conventions

- Mobile-first CSS with explicit BEM component naming.
- Lightweight vanilla JavaScript for deterministic storefront behavior.
- WordPress and WooCommerce customization lives in child theme overrides and small dedicated plugins.
- Product synchronization remains filesystem-driven to avoid manual drift from admin-only workflows.
