from django.apps import AppConfig


class OndSocialConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ond_social"

    def ready(self) -> None:
        from . import componentes

        return super().ready()
