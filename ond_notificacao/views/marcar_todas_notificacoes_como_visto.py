from typing import cast

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse

from ond_perfil.models import User
from ond_notificacao.models import AtividadeModel


@login_required
@require_http_methods(["PUT", "POST"])
def marcar_todas_notificacoes_como_visto(request: HttpRequest):
    usuario = cast(User, request.user)
    AtividadeModel.objects.filter(notificar_para=usuario, visto=False).update(
        visto=True
    )
    return HttpResponse(status=204, headers={"HX-Trigger": "todasNotificacoesVistas"})
