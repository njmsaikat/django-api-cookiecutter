import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


def init_sentry():
    """Initialise Sentry when SENTRY_DSN is set; otherwise do nothing."""
    dsn = os.environ.get("SENTRY_DSN")
    if not dsn:
        return
    sentry_sdk.init(
        dsn=dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
        send_default_pii=False,
    )
