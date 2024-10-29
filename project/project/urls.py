"""
URL configuration for project NekoNotes.

"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Authentication
    path("", include("app_authentication.urls")),
    # Dashboard
    path("dashboard/", include("app_dashboards.urls")),
]
