.PHONY: up down logs ps shell migrate makemigrations db

# Start the containers
up:
	docker compose up --build -d

# Stop the containers
down:
	docker compose down

# View logs
logs:
	docker compose logs -f

# List containers
ps:
	docker compose ps

# SSH into the API container
shell:
	docker compose exec api bash

# Run Alembic migrations
migrate:
	docker compose exec api alembic upgrade head

# Create a new Alembic migration
makemigrations:
	docker compose exec api alembic revision --autogenerate -m "$(message)"

# Connect to PostgreSQL database
db:
	docker compose exec postgres psql -U postgres -d taskqueue

# Run tests
test:
	docker compose exec api pytest
