from rest_framework import serializers

from example.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "owner", "name", "description", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]
