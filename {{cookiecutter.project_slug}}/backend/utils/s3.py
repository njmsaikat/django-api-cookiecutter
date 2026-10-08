import datetime
import os
import unicodedata
from urllib.parse import quote

import boto3
from botocore.config import Config

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_PROJECT_PREFIX = os.environ.get("AWS_S3_PROJECT_PREFIX")
AWS_S3_UPLOAD_MAX_BYTES = int(os.environ.get("AWS_S3_UPLOAD_MAX_BYTES", 10 * 1024 * 1024))

ALLOWED_UPLOAD_EXTENSIONS = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
    "pdf": "application/pdf",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

_ALLOWED_LITERAL_FILENAME_CHARS = set("()_-.")
_ALLOWED_EXTENSIONS_MESSAGE = f"file_name must end with one of: {', '.join(sorted(ALLOWED_UPLOAD_EXTENSIONS))}"


def _is_allowed_filename_char(char: str) -> bool:
    if char in _ALLOWED_LITERAL_FILENAME_CHARS:
        return True
    # Letters (L*), numbers (N*) and combining marks (M*). Marks matter for scripts like
    # Bengali/Devanagari where vowel signs are separate combining characters.
    return unicodedata.category(char)[0] in ("L", "N", "M")


def _clean_file_name(file_name: str) -> str:
    """Normalize Unicode form and strip any path component the client sent."""
    file_name = unicodedata.normalize("NFKC", (file_name or "")).strip()
    return os.path.basename(file_name)


def _validate_file_name(file_name: str) -> str | None:
    """Returns an error message if file_name breaks a rule, else None."""
    if not file_name or len(file_name) > 200:
        return "file_name is required and must be 200 characters or fewer."

    extension = file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""
    if extension not in ALLOWED_UPLOAD_EXTENSIONS:
        return _ALLOWED_EXTENSIONS_MESSAGE

    if not all(_is_allowed_filename_char(char) for char in file_name):
        return "file_name may only contain letters, numbers, and ( ) _ - . characters (no spaces)."

    return None


def generate_presigned_upload(file_name: str) -> tuple[dict | None, str | None]:
    """
    Returns (presigned_payload, None) on success, or (None, error_message) if file_name breaks a
    naming rule. The object key is built server-side as "<project-prefix>/<timestamp_ms>-<file_name>"
    so a client can never overwrite an existing object or write outside the project's directory.
    """
    file_name = _clean_file_name(file_name)
    error = _validate_file_name(file_name)
    if error:
        return None, error

    extension = file_name.rsplit(".", 1)[-1].lower()
    content_type = ALLOWED_UPLOAD_EXTENSIONS[extension]

    timestamp_ms = int(datetime.datetime.now().timestamp() * 1000)
    object_key = f"{AWS_S3_PROJECT_PREFIX}/{timestamp_ms}-{file_name}"

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME,
        endpoint_url=f"https://s3.{AWS_S3_REGION_NAME}.amazonaws.com",
        config=Config(signature_version="s3v4"),
    )

    presigned_post = s3_client.generate_presigned_post(
        Bucket=AWS_STORAGE_BUCKET_NAME,
        Key=object_key,
        Fields={"Content-Type": content_type},
        Conditions=[
            {"Content-Type": content_type},
            ["content-length-range", 1, AWS_S3_UPLOAD_MAX_BYTES],
        ],
        ExpiresIn=120,
    )

    encoded_key = quote(object_key, safe="/()")
    file_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{encoded_key}"

    return {
        "url": presigned_post["url"],
        "fields": presigned_post["fields"],
        "file_url": file_url,
    }, None
