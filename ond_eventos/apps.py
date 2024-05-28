from django.apps import AppConfig


class OndEventosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ond_eventos"

    def ready(self) -> None:
        from . import componentes

        return super().ready()
