from django.db import connection

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
{% if cookiecutter.use_s3 == "y" %}
from utils.s3 import generate_presigned_upload
{% endif %}

class HealthCheckView(APIView):
    """Liveness/readiness probe: confirms the app can reach the database."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return Response({"status": "ok"})
{%- if cookiecutter.use_s3 == "y" %}


class PresignedUploadURLView(APIView):
    def post(self, request):
        file_name = request.data.get("file_name")
        result, error = generate_presigned_upload(file_name)
        if error:
            return Response({"detail": error}, status=400)
        return Response(result, status=200)
{%- endif %}
