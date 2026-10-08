from corsheaders.defaults import default_headers
{% if cookiecutter.use_sentry == "y" %}
from config.sentry_settings import init_sentry
{% endif %}
from .base_settings import *

INSTALLED_APPS += ["corsheaders"]

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
# Serve collected static files (Django admin CSS/JS) straight from gunicorn
MIDDLEWARE.insert(2, "whitenoise.middleware.WhiteNoiseMiddleware")
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = env_list("ALLOWED_ORIGINS")
CORS_ALLOW_HEADERS = (*default_headers,)

# HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
{%- if cookiecutter.use_sentry == "y" %}

init_sentry()
{%- endif %}
