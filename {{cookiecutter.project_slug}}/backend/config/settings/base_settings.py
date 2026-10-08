import os
from pathlib import Path

import dj_database_url

from config.jwt_settings import JWT_SETTINGS
from config.log_settings import LOGGING

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


def env_list(name: str) -> list[str]:
    """Space-separated env var -> list (empty list when unset)."""
    return os.environ.get(name, "").split()


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY is not set in the environment")

DEBUG = bool(int(os.environ.get("DEBUG", "0")))

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env_list("ALLOWED_ORIGINS")

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
{% if cookiecutter.use_api_key == "y" %}    "rest_framework_api_key",
{% endif %}]

# Order roughly reflects dependency order: apps that others depend on come first.
LOCAL_APPS = [
    "utils",
    "user",
    "example",  # sample app showing the project layout; delete when you start real work
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = "user.User"

# JWT settings
SIMPLE_JWT = JWT_SETTINGS

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"user": "5000/day", "anon": "1000/day"},
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "config.middleware.APILoggingMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database connection using dj-database-url
# https://pypi.org/project/dj-database-url/
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DB_CONNECTION"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

{% if cookiecutter.__redis == "y" %}# Caching in Redis (falls back to per-process memory when REDIS_CONNECTION is unset, e.g. in CI)
# https://pypi.org/project/django-redis/
if os.environ.get("REDIS_CONNECTION"):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ["REDIS_CONNECTION"],
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }
else:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

{% endif %}AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("TZ", "{{ cookiecutter.timezone }}")
USE_I18N = True
USE_TZ = True

# Static & media files
STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = LOGGING
{%- if cookiecutter.use_celery == "y" %}

# Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND")
CELERY_TIMEZONE = TIME_ZONE
{%- endif %}
{%- if cookiecutter.use_api_key == "y" %}

# Inbound integrations authenticate with this header (see rest_framework_api_key)
API_KEY_CUSTOM_HEADER = "HTTP_X_{{ cookiecutter.project_slug.upper().replace('-', '_') }}_API_KEY"
{%- endif %}
