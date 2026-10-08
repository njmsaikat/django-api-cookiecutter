from django.urls import path

from utils.views import HealthCheckView{% if cookiecutter.use_s3 == "y" %}, PresignedUploadURLView{% endif %}

urlpatterns = [
    path("health/", HealthCheckView.as_view()),
{% if cookiecutter.use_s3 == "y" %}    path("presigned-upload-url/", PresignedUploadURLView.as_view()),
{% endif %}]
