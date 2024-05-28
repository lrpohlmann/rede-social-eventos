from typing import cast

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import render

from ond_perfil.models import User
from ond_social.models import RelacaoModel
import ond_social.dominio as social


@login_required
def perfil_view(request: HttpRequest, id_usuario: int):
    request.user = cast(User, request.user)
    try:
        usuario_perfil = social.incluir_social(id_usuario)
        return render(
            request,
            "pagina/perfil.html",
            context={
                "usuario": usuario_perfil,
                "relacao": RelacaoModel.relacoes.relacao_entre(
                    request.user, usuario_perfil
                ),
            },
        )
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
