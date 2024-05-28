from django.urls import path

from . import views


app_name = "perfil"

urlpatterns = [
    path("editar", views.editar_perfil_view, name="editar_perfil"),
    path("ver/<int:id_usuario>", views.perfil_view, name="perfil"),
    path(
        "menu-principal", views.menu_principal_perfil_view, name="menu_principal_perfil"
    ),
    path("meus-eventos", views.meus_eventos_view, name="meus_eventos"),
    path(
        "minhas-confirmacoes-de-presenca",
        views.minhas_confirmacoes_de_presenca_view,
        name="minhas_confirmacoes_de_presenca",
    ),
    path("meus-convites", views.meus_convites_view, name="meus_convites"),
]
