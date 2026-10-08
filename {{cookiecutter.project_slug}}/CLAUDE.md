# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

{{ cookiecutter.project_name }} backend service. Tech stack: Django + Django REST Framework, PostgreSQL{% if cookiecutter.__redis == "y" %}, Redis{% endif %}{% if cookiecutter.use_celery == "y" %}, Celery{% endif %}{% if cookiecutter.use_nginx == "y" %}, Nginx{% endif %}, Docker. All application code lives under `backend/`.

## Local development

```bash
make up                # docker compose up --build (dev server on localhost:{{ cookiecutter.port }})
make migrate
make createsuperuser
```

Compose files: `docker-compose.yml` (dev, runs `manage.py runserver`), `test-docker-compose.yml` and `prod-docker-compose.yml` (gunicorn). Env vars: `.env/base.env` plus `.env/{dev,test,prod}.env` (git-ignored; templates are `*.env.example`).

Django settings are in `backend/config/settings/`: `base_settings.py` (shared), `dev_settings.py`, `production_settings.py`, `test_settings.py` (deployed staging, extends production). `manage.py` defaults to `dev_settings`; the env files set `DJANGO_SETTINGS_MODULE` explicitly.

## Common commands

Run inside `backend/` (or via `docker compose exec -w /app/backend backend ...`):

```bash
python manage.py migrate
python manage.py makemigrations <app>
python manage.py test <app_label>
python manage.py test <app_label>.tests.<TestClass>.<test_method>
```

Lint/format: `make lint` / `make format` (ruff; line length 120, isort sections with Django separate, config in `backend/pyproject.toml`; migrations excluded). Pre-commit runs ruff + ruff-format.

## Architecture

### App-per-domain layout

Each top-level directory under `backend/` is a standalone Django app for one domain; `config` is the project package and `utils` holds shared abstractions. Each app has `models.py`, `serializers.py`, `admin.py`, `urls.py`, `tests.py`, and either a flat `views.py` or a `views/` package when there are multiple view surfaces (e.g. `views/admin.py` + `views/seller.py`). Follow the existing split for the app you are editing. Create new apps with `make startapp name=<app>` (uses `backend/app_template`), then register in `LOCAL_APPS` and `config/urls.py`. `INSTALLED_APPS` order roughly reflects dependency order.

All API routes are mounted under `/api/v1/<domain>/` in `backend/config/urls.py`, one `include()` per app -- that file is the map of the API surface. The `example` app is a layout sample and can be deleted.

### Auth model: JWT with a `user_type` claim

- DRF default authentication is `JWTStatelessUserAuthentication` (simplejwt, no DB lookup per request: `request.user` is a `TokenUser`, so use `request.user.id` and `request.auth`, not model attributes; settings in `backend/config/jwt_settings.py`); `user.User` is the custom user model (`AUTH_USER_MODEL`).
- Tokens carry `user_type` (`admin`, `operation`, `author`, `user` -- edit `User.UserType` to fit the domain) and `username` claims, added in `user/serializers.py::LoginSerializer`.
- Views branch on `utils.utils.get_user_type(request)` to scope querysets per role rather than using one permission class per role -- see `example/views.py::ItemListCreateView.get_queryset`. For plain allow/deny use `utils.permissions.user_type_permission(...)`.
{% if cookiecutter.use_api_key == "y" %}- `rest_framework_api_key` is installed; inbound integrations can authenticate via the `{{ cookiecutter.__api_key_header }}` header (`API_KEY_CUSTOM_HEADER`) using `HasAPIKey`.
{% endif %}- `utils/utils.py::tokenValidation` manually decodes the bearer token (used by middleware, not DRF's auth flow).

### Shared base models

`utils/models.py`: abstract `TimeStamp` (`created_at`/`updated_at`) and `CommonInfo` (adds `is_active`, default `False`). Extend these instead of redeclaring the fields.

### Code generation helpers

`utils/utils.py::generate_entity_code` (date + sequence + random suffix, e.g. `CH-WH01-20260113-045-A9F`) and `generate_sequential_code` (`WH1`, `SH1`, `SUP50`). Reuse these rather than writing new ID logic per app.

### Request logging middleware

`config/middleware.py::APILoggingMiddleware` decodes the JWT to get the `username` claim, logs 4xx/5xx responses (with request body and error detail) via `all_log`, and logs successful authenticated requests via `user_log` (CSV, for usage analytics). Logging config: `config/log_settings.py`.

### Pagination and filtering conventions

List views use `utils.utils.PagesizeVaryingPagination` (limit/offset, default 100, max 500) with `DjangoFilterBackend` (explicit `filterset_fields`) and DRF `SearchFilter` with `$`-prefixed regex search fields. Follow this combination for new list endpoints.
{% if cookiecutter.use_celery == "y" %}
### Celery

`backend/config/celery.py` wires the Celery app and `beat_schedule` (daily 3 AM `utils.tasks.backup_database`, which runs `scripts/postgres-backup.sh`). Put tasks in each app's `tasks.py`; they are autodiscovered.
{% endif %}{% if cookiecutter.use_s3 == "y" %}
### S3 uploads

`POST /api/v1/utils/presigned-upload-url/` returns a presigned S3 POST (`utils/s3.py`); configure `AWS_*` vars in the env files.
{% endif %}
## Git workflow

Branch from `experimental` (not `main`), push, and open a PR back into `experimental`.
