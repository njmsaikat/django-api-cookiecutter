from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "media" / "log"

for _sub in ("all", "admin", "user"):
    (LOG_DIR / _sub).mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        # 4xx/5xx request logs (see config.middleware.APILoggingMiddleware)
        "all_log": {"level": "DEBUG", "handlers": ["all_event", "console"]},
        "admin_log": {"level": "INFO", "handlers": ["admin"]},
        # successful authenticated requests, CSV, for usage analytics
        "user_log": {"level": "INFO", "handlers": ["user"]},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
        "all_event": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "file",
            "filename": str(LOG_DIR / "all" / "all.log"),
            "when": "midnight",
            "backupCount": 7,
        },
        "admin": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "file",
            "filename": str(LOG_DIR / "admin" / "admin.log"),
            "when": "midnight",
            "backupCount": 7,
        },
        "user": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "csv",
            "filename": str(LOG_DIR / "user" / "user.csv"),
            "when": "W0",  # Rotate every week (Monday)
            "backupCount": 4,
        },
    },
    "formatters": {
        "console": {"format": "%(levelname)s %(asctime)s %(module)s %(message)s", "datefmt": "%Y-%m-%dT%H:%M:%S"},
        "file": {"format": "%(levelname)s %(asctime)s %(module)s %(message)s", "datefmt": "%Y-%m-%dT%H:%M:%S"},
        "csv": {"format": "%(asctime)s,%(message)s", "datefmt": "%Y-%m-%dT%H:%M:%S"},
    },
}
