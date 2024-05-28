from django.apps import AppConfig


class OndNotificacaoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ond_notificacao"

    def ready(self) -> None:
        from . import componentes

        return super().ready()
