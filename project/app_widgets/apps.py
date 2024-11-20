from django.apps import AppConfig


class AppWidgetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_widgets"

    def ready(self):
        import app_widgets.signals
