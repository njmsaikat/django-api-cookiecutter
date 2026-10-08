# Usage: make <target>. Override the compose command with: make up COMPOSE=docker-compose
COMPOSE ?= docker compose
EXEC = $(COMPOSE) exec -w /app/backend backend

.PHONY: up down build logs shell dbshell migrate makemigrations createsuperuser test lint format startapp install-hooks

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs -f backend

shell:
	$(EXEC) python manage.py shell

dbshell:
	$(COMPOSE) exec db psql -U {{ cookiecutter.db_name }} {{ cookiecutter.db_name }}

migrate:
	$(EXEC) python manage.py migrate

makemigrations:
	$(EXEC) python manage.py makemigrations $(app)

createsuperuser:
	$(EXEC) python manage.py createsuperuser

test:
	$(EXEC) python manage.py test $(app)

lint:
	ruff check backend
	ruff format --check backend

format:
	ruff check --fix backend
	ruff format backend

# make startapp name=invoice  -> backend/invoice/ following the project's app layout
startapp:
	@test -n "$(name)" || (echo "usage: make startapp name=<app_name>" && exit 1)
	cd backend && python manage.py startapp --template=app_template $(name)
	@echo "Now add '$(name)' to LOCAL_APPS in backend/config/settings/base_settings.py"
	@echo "and mount it in backend/config/urls.py."

install-hooks:
	pre-commit install
