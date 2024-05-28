from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseNotFound,
)
from django.template import loader
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.template import Context

from ond_eventos.models import OndEvento
from ond_social.models import ConfirmacaoPresenca
from ond_social.componentes import BotaoPresenca


@login_required
def desconfirmar_presenca_no_evento_view(request: HttpRequest, id_ondevento: int):
    try:
        ondevento = OndEvento.objects.get(pk=id_ondevento)

        confirmacao_de_presenca = ConfirmacaoPresenca.objects.get(
            Q(do_usuario=request.user) & Q(no_evento=ondevento)
        )
        confirmacao_de_presenca.delete()

        return HttpResponse(
            BotaoPresenca().render(
                Context({"ondevento": ondevento, "usuario_presenca_confirmada": False})
            ),
            status=200,
            headers={"HX-Trigger": "ondPresencaUsuarioDesconfirmada"},
        )

    except OndEvento.DoesNotExist:
        return HttpResponseNotFound("Evento não encontrado")
    except ConfirmacaoPresenca.DoesNotExist:
        return HttpResponseNotFound(
            "Não há confirmação de presença. Impossível desconfirmar."
        )
