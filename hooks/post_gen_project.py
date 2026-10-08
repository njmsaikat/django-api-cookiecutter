import os
import secrets
import shutil
import subprocess

# Paths (relative to the generated project) that belong to features the user turned off.
REMOVE_PATHS = [
    '{% if cookiecutter.use_celery != "y" %}backend/config/celery.py{% endif %}',
    '{% if cookiecutter.use_celery != "y" %}backend/utils/tasks.py{% endif %}',
    '{% if cookiecutter.use_celery != "y" %}scripts{% endif %}',
    '{% if cookiecutter.use_nginx != "y" %}conf.d{% endif %}',
    '{% if cookiecutter.use_s3 != "y" %}backend/utils/s3.py{% endif %}',
    '{% if cookiecutter.use_sentry != "y" %}backend/config/sentry_settings.py{% endif %}',
]

for path in REMOVE_PATHS:
    if not path:
        continue
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)


def render_env_file(example_path: str, target_path: str) -> None:
    """Copy <env>.env.example to <env>.env, filling generated secrets."""
    db_password = secrets.token_hex(16)
    redis_password = secrets.token_hex(16)

    with open(example_path) as fh:
        content = fh.read()

    while "__SECRET__" in content:
        content = content.replace("__SECRET__", secrets.token_urlsafe(50), 1)
    content = content.replace("__DB_PASSWORD__", db_password)
    content = content.replace("__REDIS_PASSWORD__", redis_password)

    with open(target_path, "w") as fh:
        fh.write(content)
    os.chmod(target_path, 0o600)


for env in ("dev", "test", "prod"):
    render_env_file(f".env/{env}.env.example", f".env/{env}.env")

if "{{ cookiecutter.git_init }}" == "y":
    subprocess.run(["git", "init", "-q"], check=False)

print(
    """
Project '{{ cookiecutter.project_slug }}' created.

Next steps:
  cd {{ cookiecutter.project_slug }}
  make up                    # build + start the stack (http://localhost:{{ cookiecutter.port }})
  make migrate
  make createsuperuser
  make install-hooks         # pre-commit (needs `pip install pre-commit`)

Secrets in .env/{dev,test,prod}.env were generated for you (git-ignored).
Review ALLOWED_HOSTS / ALLOWED_ORIGINS in .env/prod.env before deploying.
See README.md and CLAUDE.md for details.
"""
)
