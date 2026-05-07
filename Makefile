up:
	docker compose up -d

down:
	docker compose down

fresh:
	docker compose down -v
	docker compose up -d

logs:
	docker compose logs -f --tail=100

restart:
	docker compose down
	docker compose up -d