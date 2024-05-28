from typing import cast

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound

from ond_perfil.models import User
from ond_notificacao.models import AtividadeModel


@login_required
@require_http_methods(["PUT", "POST"])
def marcar_notificacao_como_visto(request: HttpRequest, id_notificacao: int):
    usuario = cast(User, request.user)
    try:
        notificacao = AtividadeModel.objects.get(
            pk=id_notificacao, notificar_para=usuario.pk
        )
    except AtividadeModel.DoesNotExist:
        return HttpResponseNotFound()

    notificacao.visto = True
    notificacao.save()

    return HttpResponse(status=200, headers={"HX-Trigger": "notificacaoVista"})
