from typing import cast

from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseNotFound,
)
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.template import Context

from ond_perfil.models import User
from ond_eventos.models import OndEvento
from ond_social.models import ConfirmacaoPresenca
from ond_social.componentes import BotaoPresenca


@login_required
def confirmar_presenca_no_evento_view(request: HttpRequest, id_ondevento: int):
    request.user = cast(User, request.user)
    try:
        ondevento = OndEvento.objects.get(pk=id_ondevento)
        confirmacao_presenca = ConfirmacaoPresenca(
            do_usuario=request.user, no_evento=ondevento
        )
        confirmacao_presenca.save()

        return HttpResponse(
            BotaoPresenca().render(
                Context({"ondevento": ondevento, "usuario_presenca_confirmada": True})
            ),
            status=201,
            headers={"HX-Trigger": "ondPresencaUsuarioConfirmada"},
        )
    except OndEvento.DoesNotExist:
        return HttpResponseNotFound("Evento não encontrado")
    except IntegrityError:
        return HttpResponse(
            "Já foi confirmado presença.", content_type="plain/text", status=400
        )
