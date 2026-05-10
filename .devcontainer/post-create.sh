#!/bin/sh
# .devcontainer/post-create.sh
# Runs once when the Codespace is first created.
# Adjusts WORDPRESS_LOCAL_URL for Codespaces and starts the Docker Compose stack.
set -eu

ENV_FILE=".env"

# ──────────────────────────────────────────────────────────────────────────────
# 1. Detect GitHub Codespaces and set the correct WordPress local URL.
#    In Codespaces, port 8080 is forwarded to a public HTTPS URL that depends
#    on the Codespace name.  WordPress must be told this URL so that its
#    internal redirects (login, admin links, etc.) point to the reachable host.
# ──────────────────────────────────────────────────────────────────────────────
if [ -n "${CODESPACE_NAME:-}" ]; then
  DOMAIN="${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-preview.app.github.dev}"
  LOCAL_URL="https://${CODESPACE_NAME}-8080.${DOMAIN}"
  echo "Codespaces detected. Setting WORDPRESS_LOCAL_URL=${LOCAL_URL}"

  if grep -q "^WORDPRESS_LOCAL_URL=" "${ENV_FILE}"; then
    sed -i "s|^WORDPRESS_LOCAL_URL=.*|WORDPRESS_LOCAL_URL=${LOCAL_URL}|" "${ENV_FILE}"
  else
    echo "WORDPRESS_LOCAL_URL=${LOCAL_URL}" >> "${ENV_FILE}"
  fi
else
  LOCAL_URL="http://localhost:8080"
  echo "Local environment detected. WORDPRESS_LOCAL_URL=${LOCAL_URL}"
fi

# ──────────────────────────────────────────────────────────────────────────────
# 2. Start the Docker Compose stack.
#    `make fresh` tears down volumes and re-imports the SQL dump; use it for a
#    clean first boot.  If the database/andres38_wp718.sql file is absent the
#    MySQL init script skips the import and WordPress shows the installer.
# ──────────────────────────────────────────────────────────────────────────────
has_dump=false
if [ -f "database/andres38_wp718.sql" ]; then
  has_dump=true
else
  for f in database/*.sql.gz; do
    if [ -e "$f" ]; then
      has_dump=true
      break
    fi
  done
fi

if $has_dump; then
  echo "SQL dump found — running 'make fresh' to import it."
  make fresh
else
  echo "No SQL dump found in database/ — starting stack without seed import."
  echo "WordPress will show the installer. Place database/andres38_wp718.sql"
  echo "and run 'make fresh' to bootstrap from the production dump."
  docker compose up -d
fi

# ──────────────────────────────────────────────────────────────────────────────
# 3. Print quick-start hints.
# ──────────────────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  Beslock WordPress stack is starting."
echo ""
echo "  WordPress:  ${LOCAL_URL}"
echo "  phpMyAdmin: see PORTS tab → port 8081"
echo ""
echo "  First boot imports the SQL dump; this can take 1-2 minutes."
echo "  Watch progress with:  docker compose logs -f wpcli"
echo "════════════════════════════════════════════════════════════════"
