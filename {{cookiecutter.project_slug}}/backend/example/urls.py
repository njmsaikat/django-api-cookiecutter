from django.urls import path

from example.views import ItemListCreateView

urlpatterns = [
    # http://localhost:{{ cookiecutter.port }}/api/v1/example/items/
    path("items/", ItemListCreateView.as_view(), name="example_item_list_create"),
]
