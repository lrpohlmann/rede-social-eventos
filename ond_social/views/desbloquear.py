from typing import cast

from django.http import (
    HttpRequest,
    HttpResponseNotFound,
    HttpResponseForbidden,
    HttpResponse,
)
from django.template import Context
from django.contrib.auth.decorators import login_required

from ond_perfil.models import User
from ond_social import dominio as social
from ond_social.models import RelacaoModel
from ond_social.componentes import DialogOpcoesSocial


@login_required
def desbloquear_view(request: HttpRequest, id_receptor: int):
    desbloqueante = cast(User, request.user)
    try:
        desbloqueado = User.objects.get(pk=id_receptor)
    except User.DoesNotExist:
        return HttpResponseNotFound("Usuário não encontrado.")

    try:
        if social.desbloquear(desbloqueante, desbloqueado):
            relacao = RelacaoModel.relacoes.relacao_entre(desbloqueante, desbloqueado)
            return HttpResponse(
                DialogOpcoesSocial().render(
                    Context({"usuario": desbloqueado, "relacao": relacao})
                ),
                status=200,
                headers={"HX-Refresh": "true"},
            )

        return HttpResponseNotFound("Usuário não estava bloqueado.")
    except social.AutorelacionamentoException:
        return HttpResponseForbidden("Usuário não pode bloquear a si mesmo.")
