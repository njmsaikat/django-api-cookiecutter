from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "{{ cookiecutter.project_name }} Admin"
admin.site.site_title = "{{ cookiecutter.project_name }} Management"
admin.site.index_title = "{{ cookiecutter.project_name }} Admin Portal"

# One include() per app -- this file is the map of the whole API surface.
urlpatterns = [
    path("api/v1/user/", include("user.urls")),
    path("api/v1/utils/", include("utils.urls")),
    path("api/v1/example/", include("example.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

    urlpatterns += [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path("", SpectacularSwaggerView.as_view(url_name="schema"), name="schema-swagger-ui"),
        path("docs/", SpectacularRedocView.as_view(url_name="schema"), name="schema-redoc"),
        path("admin/", admin.site.urls),
        path("__debug__/", include(debug_toolbar.urls)),
    ]
else:
    # Admin lives on an obscure path outside DEBUG
    urlpatterns += [path("dev-staff/", admin.site.urls)]
