from rest_framework.permissions import BasePermission

from utils.utils import get_user_type
{% if cookiecutter.use_api_key == "y" %}
# For inbound integrations, use rest_framework_api_key.permissions.HasAPIKey
# (clients send the key in the header named by settings.API_KEY_CUSTOM_HEADER).
{% endif %}

def user_type_permission(*allowed_types: str) -> type[BasePermission]:
    """
    Build a permission class limited to the given JWT `user_type` values, e.g.
        permission_classes = [user_type_permission("admin", "operation")]
    Prefer branching on get_user_type() inside get_queryset() when roles see *different data*;
    use this when roles are simply allowed or denied.
    """

    class _UserTypePermission(BasePermission):
        def has_permission(self, request, view):
            return bool(request.user and request.user.is_authenticated and get_user_type(request) in allowed_types)

    return _UserTypePermission
