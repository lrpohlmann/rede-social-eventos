from django.urls import path

from . import views

app_name = "social"

urlpatterns = [
    path("seguir/<int:id_receptor>", views.seguir_view, name="seguir"),
    path("desseguir/<int:id_receptor>", views.desseguir_view, name="desseguir"),
    path("bloquear/<int:id_receptor>", views.bloquear_view, name="bloquear"),
    path("desbloquear/<int:id_receptor>", views.desbloquear_view, name="desbloquear"),
    path(
        "comentar/<int:id_ondevento>",
        views.comentar_ondevento_view,
        name="comentar_evento",
    ),
    path(
        "comentario/reagir/<int:id_comentario>",
        views.reagir_ao_comentario_view,
        name="reagir_ao_comentario",
    ),
    path(
        "comentario/opcoes/<int:id_comentario>",
        views.opcoes_comentario_view,
        name="opcoes_comentario",
    ),
    path(
        "comentario/deletar/<int:id_comentario>",
        views.deletar_comentario_view,
        name="deletar_comentario",
    ),
    path(
        "comentar/conversa/<int:id_comentario>",
        views.ver_conversa_view,
        name="ver_conversa",
    ),
    path(
        "comentar/responder/<int:id_comentario>",
        views.responder_comentario_view,
        name="responder_comentario",
    ),
    path(
        "comentario/resposta/reagir/<int:id_resposta>",
        views.reagir_a_resposta_do_comentario_view,
        name="reagir_resposta_comentario",
    ),
    path(
        "confirmar-presenca/<int:id_ondevento>",
        views.confirmar_presenca_no_evento_view,
        name="confirmar_presenca",
    ),
    path(
        "desconfirmar-presenca/<int:id_ondevento>",
        views.desconfirmar_presenca_no_evento_view,
        name="desconfirmar_presenca",
    ),
    path(
        "convidar/<int:id_ondevento>/<int:id_convidado>",
        views.convidar_para_ondevento,
        name="convidar_para_ondevento",
    ),
    path(
        "desconvidar/<int:id_ondevento>/<int:id_convidado>",
        views.desconvidar_para_ondevento,
        name="desconvidar_para_ondevento",
    ),
    path(
        "lista-seguidores-para-convidar/<int:id_ondevento>",
        views.lista_de_seguidores_possiveis_de_convidar_view,
        name="lista_seguidores_para_convidar",
    ),
]
