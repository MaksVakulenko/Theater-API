from django.apps import AppConfig
from django.apps import AppConfig


class TheatreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "theatre"

    def ready(self):
        import theatre.signals
