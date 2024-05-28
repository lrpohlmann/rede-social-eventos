from typing import cast

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.template.context import Context

from ond_perfil.models import User
from ond_notificacao.models import AtividadeModel
from ond_notificacao.componentes import IconNotificacao


@login_required
def verificar_notificacao_header(request: HttpRequest):
    usuario = cast(User, request.user)
    notificacao_nao_vista = AtividadeModel.objects.filter(
        notificar_para=usuario, visto=False
    ).exists()

    return HttpResponse(
        IconNotificacao().render(
            Context({"notificacao_nao_vista": notificacao_nao_vista})
        )
    )
