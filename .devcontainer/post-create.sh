#!/usr/bin/env bash
set -euo pipefail

echo "✅ Dev container ready."
docker --version
docker compose version

if [ ! -f "database/andres38_wp718.sql" ]; then
  echo "⚠️ Missing database/andres38_wp718.sql. The local stack may boot without site data."
fi

echo "Next step: run 'make fresh' (first boot) or 'make up' (subsequent boots)."
