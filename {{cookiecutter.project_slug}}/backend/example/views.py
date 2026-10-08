from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView

from example.models import Item
from example.serializers import ItemSerializer
from utils.utils import PagesizeVaryingPagination, get_user_type


class ItemListCreateView(ListCreateAPIView):
    """
    Canonical list-view pattern: role-scoped queryset + limit/offset pagination + explicit
    filterset_fields + `$`-prefixed regex SearchFilter.
    """

    serializer_class = ItemSerializer
    pagination_class = PagesizeVaryingPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["is_active", "owner"]
    search_fields = ["$name", "$description"]

    def get_queryset(self):
        queryset = Item.objects.select_related("owner")
        # Regular users only see their own records; admin/operation/author see everything.
        if get_user_type(self.request) == "user":
            return queryset.filter(owner_id=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.id)
