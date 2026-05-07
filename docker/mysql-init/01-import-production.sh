#!/bin/sh
set -eu

seed_dir="/docker-entrypoint-seed"
dump_file=""

for candidate in "$seed_dir"/*.sql "$seed_dir"/*.sql.gz; do
  if [ -e "$candidate" ]; then
    dump_file="$candidate"
    break
  fi
done

if [ -z "$dump_file" ]; then
  echo "No SQL dump found in $seed_dir; skipping seed import."
  exit 0
fi

echo "Importing production dump: $dump_file"

case "$dump_file" in
  *.sql)
    mysql --default-character-set=utf8mb4 -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" < "$dump_file"
    ;;
  *.sql.gz)
    gunzip -c "$dump_file" | mysql --default-character-set=utf8mb4 -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"
    ;;
esac