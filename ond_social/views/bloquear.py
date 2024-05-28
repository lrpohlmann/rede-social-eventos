from typing import cast

from django.http import (
    HttpRequest,
    HttpResponseNotFound,
    HttpResponseForbidden,
    HttpResponse,
)
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic

from ond_perfil.models import User
from ond_social import dominio as social
from ond_social.models import RelacaoModel
from ond_social.componentes import DialogOpcoesSocial


@login_required
@atomic
def bloquear_view(request: HttpRequest, id_receptor: int):
    bloqueante = cast(User, request.user)
    try:
        bloqueado = User.objects.get(pk=id_receptor)
    except User.DoesNotExist:
        return HttpResponseNotFound("Usuário não encontrado.")

    try:
        social.bloquear(bloqueante, bloqueado)
        relacao = RelacaoModel.relacoes.relacao_entre(bloqueante, bloqueado)
        return HttpResponse(
            DialogOpcoesSocial().render(
                Context({"usuario": bloqueado, "relacao": relacao})
            ),
            status=201,
            headers={"HX-Refresh": "true"},
        )
    except social.AutorelacionamentoException:
        return HttpResponseForbidden("Usuário não pode bloquear a si mesmo.")
