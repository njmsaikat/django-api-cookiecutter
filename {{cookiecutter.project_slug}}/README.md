# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

Tech stack: Django + Django REST Framework, PostgreSQL{% if cookiecutter.__redis == "y" %}, Redis{% endif %}{% if cookiecutter.use_celery == "y" %}, Celery{% endif %}{% if cookiecutter.use_nginx == "y" %}, Nginx{% endif %}, Docker.

## Quick start

```bash
make up              # build and start everything -> http://localhost:{{ cookiecutter.port }}
make migrate
make createsuperuser
```

- `http://localhost:{{ cookiecutter.port }}/` -- Swagger UI (DEBUG only; log in via the admin first, it is admin-gated)
- `http://localhost:{{ cookiecutter.port }}/docs/` -- Redoc (DEBUG only)
- `http://localhost:{{ cookiecutter.port }}/admin/` -- Django admin (DEBUG only; `/dev-staff/` otherwise)
- `POST /api/v1/user/login/` -- obtain a JWT (`access` + `refresh`); `GET /api/v1/user/me/`
- `GET /api/v1/utils/health/` -- health check

Environment files live in `.env/`. `base.env` is committed; `dev.env`, `test.env`, `prod.env` were generated
with random secrets at project creation and are git-ignored (`*.env.example` are the committed templates).

## Local development without Docker for tooling

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r backend/requirements/dev.txt
pre-commit install
```

Lint/format with `make lint` / `make format` (ruff, line length 120).

## Adding an app

```bash
make startapp name=invoice
```

Then add it to `LOCAL_APPS` in `backend/config/settings/base_settings.py` and mount it in `backend/config/urls.py`.
The `example` app shows the intended layout; delete it (and its entries in settings/urls) once you have real apps.

## Deployment

- `test-docker-compose.yml` and `prod-docker-compose.yml` run gunicorn{% if cookiecutter.use_nginx == "y" %} behind nginx{% endif %} using `.env/test.env` / `.env/prod.env`.
- Set real `ALLOWED_HOSTS` / `ALLOWED_ORIGINS` in those files first.
- Run migrations explicitly: `docker compose -f prod-docker-compose.yml exec -w /app/backend backend python manage.py migrate`.

## Git workflow

Branch from `experimental`, open a PR back into `experimental`.
