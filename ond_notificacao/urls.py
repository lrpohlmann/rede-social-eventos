from django.urls import path

from . import views


app_name = "notificacao"

urlpatterns = [
    path("minhas-notificacoes", views.minhas_notificacoes, name="minhas_notificacoes"),
    path(
        "marcar-como-visto/<int:id_notificacao>",
        views.marcar_notificacao_como_visto,
        name="marcar_como_visto",
    ),
    path(
        "marcar-todas-como-visto",
        views.marcar_todas_notificacoes_como_visto,
        name="marcar_todas_como_visto",
    ),
    path(
        "verificar_notificacao_header",
        views.verificar_notificacao_header,
        name="verificar_notificacao_header",
    ),
]
