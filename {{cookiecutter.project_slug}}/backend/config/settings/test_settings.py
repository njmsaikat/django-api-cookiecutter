# Deployed "test" environment (staging): production behaviour, but local frontends may call it.
from .production_settings import *

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost:\d+$",
    r"^http://127\.0\.0\.1:\d+$",
]
