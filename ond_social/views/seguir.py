from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponse,
)
from django.template import Context

import ond_social.dominio as social
from ond_perfil.models import User
from ond_social.models import RelacaoModel
from ond_social.componentes import DialogOpcoesSocial


@login_required
def seguir_view(request: HttpRequest, id_receptor: int):
    try:
        receptor = User.objects.get(pk=id_receptor)
        social.seguir(emissor=request.user, receptor=receptor)
        relacao = RelacaoModel.relacoes.relacao_entre(request.user, receptor)
        return HttpResponse(
            DialogOpcoesSocial().render(
                Context({"usuario": receptor, "relacao": relacao})
            ),
            status=201,
            headers={"HX-Trigger": "usuarioSeguiuPerfil"},
        )
    except social.BloqueadoException:
        return HttpResponseForbidden(
            content="Não é possível seguir. Um dos usuários bloqueou ou está bloqueado".encode()
        )
    except ObjectDoesNotExist:
        return HttpResponseNotFound(
            content="Não é possível seguir: usuário inexistente.".encode()
        )
