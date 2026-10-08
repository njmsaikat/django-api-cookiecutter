import logging
import subprocess

from celery import shared_task

logger = logging.getLogger("all_log")


@shared_task
def backup_database():
    """Run scripts/postgres-backup.sh (mounted at /backup.sh in the celery container)."""
    result = subprocess.run(["sh", "/backup.sh"], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Database backup failed: {result.stdout} {result.stderr}")
        return False
    return True
