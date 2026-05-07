# Beslock

Custom WooCommerce platform for BESLOCK, built on WordPress + Kadence with a modular product synchronization architecture powered by JSON-driven portfolio data, automated product/media sync, and reproducible local Docker development.

## Project structure

- `/wp-content/themes/beslock-custom`: Kadence child theme customizations.
- `/wp-content/plugins/beslock-product-sync`: Deterministic JSON-driven WooCommerce product sync.
- `/data/products.json`: filesystem source of product data consumed by sync.

## Architecture conventions

- Mobile-first CSS with explicit BEM component naming.
- Lightweight vanilla JavaScript for deterministic storefront behavior.
- WordPress/WooCommerce customization lives in child theme overrides and small dedicated plugins.
- Product synchronization remains filesystem-driven (`products.json`) to avoid manual drift from admin-only workflows.
