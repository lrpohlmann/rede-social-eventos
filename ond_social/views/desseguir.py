from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponseNotFound, HttpResponse
from django.template import Context

import ond_social.dominio as social
from ond_perfil.models import User
from ond_social.models import RelacaoModel
from ond_social.componentes import DialogOpcoesSocial


@login_required
def desseguir_view(request: HttpRequest, id_receptor: int):
    try:
        receptor = User.objects.get(pk=id_receptor)
        if social.deseguir(request.user, receptor):
            relacao = RelacaoModel.relacoes.relacao_entre(request.user, receptor)
            return HttpResponse(
                DialogOpcoesSocial().render(
                    Context({"usuario": receptor, "relacao": relacao})
                ),
                status=200,
                headers={"HX-Trigger": "usuarioDesseguiuPerfil"},
            )
        else:
            return HttpResponseNotFound(
                "Não é possível desseguir. Não há relação de seguidor.".encode()
            )
    except ObjectDoesNotExist:
        return HttpResponseNotFound(
            content="Não é possível desseguir: usuário inexistente.".encode()
        )
