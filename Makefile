up:
	docker compose -f docker-compose-local.yaml up -d
build:
	docker compose -f docker-compose-local.yaml up -d --build
migrate:
	docker compose -f docker-compose-local.yaml run --rm backend alembic upgrade heads
.PHONY: make_migrations
make-migrations:
	@if [ -z "$(MSG)" ]; then \
	  echo "ERROR: please pass a message, e.g.:"; \
	  echo "    make make_migrations MSG=\"add new trigger\""; \
	  exit 1; \
	fi
	docker compose -f docker-compose-local.yaml run --rm \
	  backend alembic revision --autogenerate -m "$(MSG)"
down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force
logs:
	docker compose -f docker-compose-local.yaml logs -f --tail=100
logs-%:
	docker compose -f docker-compose-local.yaml logs -f --tail=100 $*
test:
	docker compose -f docker-compose-local.yaml run --rm \
	-e TEST=1 \
	-e PYTHONPATH=/backend/src \
	backend pytest
rebuild:
	make down && make build && sleep 3 && make migrate && make test
psql:
	docker compose -f docker-compose-local.yaml exec db psql -U postgres -d mydatabase
create-user:
	docker compose -f docker-compose-local.yaml exec -it backend python create_user.py
