import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev_settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules (tasks.py) from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "backup_database": {
        "task": "utils.tasks.backup_database",
        "schedule": crontab(hour=3, minute=0),  # Every day at 3 AM
    },
}
