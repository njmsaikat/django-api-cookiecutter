# django-api-cookiecutter

Cookiecutter template for a Django + DRF API: Postgres, JWT auth with `user_type` roles, optional Redis /
Celery / Nginx / Sentry / S3 uploads / API-key auth, Docker (dev, test, prod), ruff + pre-commit, Makefile, CI, and a
`CLAUDE.md` describing the conventions.

## Use it

```bash
pip install cookiecutter            # or: pipx install cookiecutter
cookiecutter ~/projects/django-api-cookiecutter
# or from git:  cookiecutter gh:<you>/django-api-cookiecutter
# non-interactive: cookiecutter ~/projects/django-api-cookiecutter --no-input project_name="Shop API" use_s3=n
```

You are prompted for:

| Prompt | Default | Notes |
| --- | --- | --- |
| `project_name` | My API | slug is derived (`my-api`) and used for container names |
| `port` | 8020 | dev server / gunicorn / nginx port (prod binds `127.0.0.1:port+1`) |
| `python_version` | 3.12 | Docker image + ruff target |
| `timezone` | UTC | Django `TIME_ZONE` + Celery |
| `db_name` | slug with `_` | Postgres db + user |
| `use_celery` | y | worker + beat + scheduled DB backup (implies Redis) |
| `use_redis` | y | Redis cache (forced on if Celery is on) |
| `use_nginx` | y | nginx container in front of the app |
| `use_sentry` | y | Sentry init in production settings |
| `use_s3` | y | presigned upload endpoint |
| `use_api_key` | y | `djangorestframework-api-key` + custom header |
| `git_init` | y | `git init` in the new project |

Secrets in `.env/{dev,test,prod}.env` are generated at creation time.

## What you get

See the generated project's `README.md` and `CLAUDE.md`. Highlights: split settings, custom `User` with `user_type`
JWT claim (`/api/v1/user/login|token/refresh|me`), `/api/v1/utils/health/`, a sample `example` app showing the app layout and
role-scoped list-view pattern, `make startapp name=...`, GitHub Actions CI.

## Maintaining the template

- Files inside `{{cookiecutter.project_slug}}/` are Jinja templates. Avoid literal `{{`, `{%`, `{#` in them.
- `backend/app_template/` and `.github/` are copied verbatim (`_copy_without_render`).
- Migrations for `user` and `example` are committed in the template; if you change those models,
  regenerate them from a freshly generated project and copy them back.
