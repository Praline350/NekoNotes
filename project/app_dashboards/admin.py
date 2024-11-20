from django.contrib import admin
from .models import Dashboard, EmptyWidget


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = [
        "user",
    ]


@admin.register(EmptyWidget)
class EmptyWidgetAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
