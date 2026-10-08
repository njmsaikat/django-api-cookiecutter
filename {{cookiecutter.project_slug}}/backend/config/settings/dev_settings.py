from .base_settings import *

INSTALLED_APPS += [
    "drf_spectacular",  # OpenAPI schema + Swagger/Redoc
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["0.0.0.0"]

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append("rest_framework.authentication.SessionAuthentication")
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append("rest_framework.renderers.BrowsableAPIRenderer")
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"

SPECTACULAR_SETTINGS = {
    "TITLE": "{{ cookiecutter.project_name }} API",
    "DESCRIPTION": "{{ cookiecutter.description }}",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
}


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "RESULTS_CACHE_SIZE": 3,
    "SHOW_COLLAPSED": True,
    "SQL_WARNING_THRESHOLD": 100,  # milliseconds
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}
