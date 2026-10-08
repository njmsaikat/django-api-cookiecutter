import logging

from django.conf import settings

from utils.utils import tokenValidation

logger = logging.getLogger("all_log")
user_logger = logging.getLogger("user_log")


class APILoggingMiddleware:
    """
    Logs 4xx/5xx responses (with request body and error detail) to `all_log`, and
    successful authenticated requests to `user_log` as CSV rows for usage analytics.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            request_body = request.body.decode(errors="replace")
        except Exception:
            request_body = "<unavailable>"

        # Identify the caller from the JWT (decoded manually; auth hasn't run yet)
        username = ""
        try:
            payload = tokenValidation(request)
            if payload and "username" in payload:
                username = payload["username"]
        except Exception:
            username = "<unknown>"

        response = self.get_response(request)
        status_code = response.status_code

        analytics_data = f"{username},{request.method},{request.path},{status_code}"

        if status_code < 400 and username:
            user_logger.info(analytics_data)

        query_params = dict(request.GET)
        if query_params:
            analytics_data += f", | QueryParams: {query_params}"

        error_details = ""
        if status_code >= 400:
            try:
                if hasattr(response, "data"):
                    error_details = f" | Errors: {response.data}"
                else:
                    error_details = f" | Content: {getattr(response, 'content', '')}"
            except Exception:
                error_details = ""

        if status_code >= 500:
            logger.error(f"{analytics_data} | Body: {request_body}{error_details}")
        elif status_code >= 400:
            logger.warning(f"{analytics_data} | Body: {request_body}{error_details}")

        if getattr(settings, "DEBUG", False):
            print(f"{analytics_data} | Body: {request_body}{error_details}")

        return response
