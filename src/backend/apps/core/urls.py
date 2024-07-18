from django.urls import path

from apps.core.views import ping


urlpatterns = [
    path("ping", ping),
]
