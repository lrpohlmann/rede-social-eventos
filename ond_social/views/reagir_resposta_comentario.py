from typing import cast

from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseNotFound,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.template import Context

from ond_perfil.models import User
from ond_social.models import (
    RespostaComentario,
    RelacaoModel,
    ReacaoRespostaComentarioModel,
)
from ond_social.componentes import ReacaoRespostaComentarioComponente


@login_required
@require_http_methods(["POST", "DELETE"])
def reagir_a_resposta_do_comentario_view(request: HttpRequest, id_resposta: int):
    usuario = cast(User, request.user)
    try:
        resposta = RespostaComentario.objects.get(pk=id_resposta)
    except RespostaComentario.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == "DELETE":
        try:
            reacao = ReacaoRespostaComentarioModel.objects.get(
                usuario=usuario, resposta=resposta
            )
            reacao.delete()
            return HttpResponse(
                ReacaoRespostaComentarioComponente().render(
                    context=Context({"resposta": resposta})
                ),
                status=200,
            )
        except ReacaoRespostaComentarioModel.DoesNotExist:
            return HttpResponseNotFound()

    else:
        if usuario != resposta.do_autor:
            if RelacaoModel.relacoes.existe_relacao_entre(
                usuario, resposta.do_autor, "BLQ"
            ):
                return HttpResponseForbidden()

        try:
            reacao = ReacaoRespostaComentarioModel.objects.get(
                usuario=usuario, resposta=resposta
            )
        except ReacaoRespostaComentarioModel.DoesNotExist:
            reacao = ReacaoRespostaComentarioModel(usuario=usuario, resposta=resposta)

        reacao.tipo = request.POST.dict().get("reacao", "")
        try:
            reacao.full_clean()
        except ValidationError:
            return HttpResponseBadRequest()

        reacao.save()
        setattr(resposta, "minha_reacao", [reacao])
        return HttpResponse(
            ReacaoRespostaComentarioComponente().render(
                context=Context({"resposta": resposta})
            ),
            status=201,
        )
