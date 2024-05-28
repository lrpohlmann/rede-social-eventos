from typing import cast

from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template import Context

from ond_eventos.models import OndEvento
from ond_social import dominio as social
from ond_perfil.models import User
from ond_social.componentes import BotaoConvidar


@login_required
@require_POST
def convidar_para_ondevento(request: HttpRequest, id_ondevento: int, id_convidado: int):
    convidante = cast(User, request.user)
    try:
        ondevento = OndEvento.objects.get(pk=id_ondevento)
        convidado = User.objects.get(pk=id_convidado)
    except (OndEvento.DoesNotExist, User.DoesNotExist):
        return HttpResponseNotFound()

    e_possivel, motivo = social.e_possivel_convidar(convidante, convidado, ondevento)
    if not e_possivel:
        return HttpResponseForbidden(motivo)

    social.enviar_convite(convidante, convidado, ondevento)
    return HttpResponse(
        BotaoConvidar().render(
            Context(
                {
                    "ondevento": ondevento,
                    "seguidor": convidado,
                    "situacao_para_convite": "CONVIDADO",
                }
            )
        ),
        status=201,
    )
