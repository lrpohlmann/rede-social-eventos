from django.urls import path

from . import views


app_name = "evento"

urlpatterns = [
    path(
        "<int:id_ondevento>/home",
        views.home_do_ondevento_view,
        name="ondevento_home",
    ),
    path(
        "<int:id_ondevento>/comentarios",
        views.comentarios_do_ondevento_view,
        name="comentarios_do_ondevento",
    ),
    path(
        "<int:id_ondevento>/editar",
        views.editar_ondevento_view,
        name="editar_ondevento",
    ),
    path("criar", views.criar_ondevento_view, name="criar_ondevento"),
    path(
        "criar/form/select-cidade",
        views.option_cidade_view,
        name="select_cidade",
    ),
]
