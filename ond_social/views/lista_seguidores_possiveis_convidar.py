from typing import cast

from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ond_eventos.models import OndEvento
from ond_social import dominio as social
from ond_perfil.models import User


@login_required
def lista_de_seguidores_possiveis_de_convidar_view(
    request: HttpRequest, id_ondevento: int
):
    convidante = cast(User, request.user)
    try:
        ondevento = OndEvento.objects.get(pk=id_ondevento)
        possiveis_convidados = User.usuarios.seguidores_com_situacao_para_convite(
            convidante.pk, id_ondevento
        )
    except (OndEvento.DoesNotExist, User.DoesNotExist):
        return HttpResponseNotFound()

    return render(
        request,
        "pagina/lista-seguidores-possiveis-convidar.html",
        {"ondevento": ondevento, "possiveis_convidados": possiveis_convidados},
    )
