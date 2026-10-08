import datetime
import random
import re
import string

from django.db import models

import jwt
from rest_framework.authentication import get_authorization_header
from rest_framework.pagination import LimitOffsetPagination

from config.jwt_settings import JWT_SETTINGS


# pagination: page size defined by the frontend (?limit=&offset=)
class PagesizeVaryingPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 500


def get_user_type(request) -> str | None:
    """The `user_type` claim of the authenticated JWT (None for anonymous requests)."""
    auth = getattr(request, "auth", None)
    return auth.get("user_type") if auth is not None else None


def tokenValidation(request):
    """
    Decode the bearer token on the request and return its payload (None if there is no bearer token).
    Used by middleware, which runs before DRF's own authentication.
    """
    token_header = get_authorization_header(request).decode("utf-8").split(" ")
    if token_header[0] == "Bearer" and len(token_header) > 1:
        return jwt.decode(
            jwt=token_header[1],
            key=JWT_SETTINGS["SIGNING_KEY"],
            algorithms=[JWT_SETTINGS["ALGORITHM"]],
        )
    return None


def generate_entity_code(prefix: str, entity_code: str, model: type[models.Model], code_field: str) -> str:
    """
    Generate codes like CH-WH01-20260113-045-A9F
    (prefix - entity - date - daily sequence - random suffix).
    """
    today = datetime.date.today().strftime("%Y%m%d")

    latest = (
        model.objects.filter(**{f"{code_field}__startswith": f"{prefix}-{entity_code}-{today}"})
        .order_by(f"-{code_field}")
        .first()
    )

    seq = 1
    if latest:
        match = re.search(rf"{prefix}-{entity_code}-{today}-(\d+)", getattr(latest, code_field))
        seq = (int(match.group(1)) if match else 0) + 1

    rand_suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{prefix}-{entity_code}-{today}-{seq:03d}-{rand_suffix}"


def generate_sequential_code(prefix: str, model: type[models.Model], code_field: str) -> str:
    """Generate sequential codes like WH1, SH1, SUP50."""
    codes = model.objects.filter(**{f"{code_field}__startswith": prefix}).values_list(code_field, flat=True)

    max_num = 0
    for code in codes:
        match = re.search(rf"{prefix}(\d+)", code)
        if match:
            max_num = max(max_num, int(match.group(1)))

    return f"{prefix}{max_num + 1}"
