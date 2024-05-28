from typing import cast

from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseNotFound,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template import Context

from ond_eventos.models import OndEvento
from ond_perfil.models import User
from ond_social.models import ConviteOndEvento
from ond_social.componentes import BotaoConvidar


@login_required
@require_POST
def desconvidar_para_ondevento(
    request: HttpRequest, id_ondevento: int, id_convidado: int
):
    convidante = cast(User, request.user)
    try:
        ondevento = OndEvento.objects.get(pk=id_ondevento)
        convidado = User.objects.get(pk=id_convidado)
        convite = ConviteOndEvento.objects.get(
            de=convidante, para=convidado, evento=ondevento
        )
        convite.delete()
        return HttpResponse(
            BotaoConvidar().render(
                Context(
                    {
                        "ondevento": ondevento,
                        "seguidor": convidado,
                        "situacao_para_convite": "ABERTO",
                    }
                )
            ),
            status=200,
        )
    except (OndEvento.DoesNotExist, User.DoesNotExist, ConviteOndEvento.DoesNotExist):
        return HttpResponseNotFound()
