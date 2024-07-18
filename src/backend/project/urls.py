from django.conf import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    try:
        import debug_toolbar  # noqa

        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
    except ModuleNotFoundError:
        pass
