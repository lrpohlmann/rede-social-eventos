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
from ond_social.models import Comentario, RelacaoModel, ReacaoComentarioModel
from ond_social.componentes import ReacaoComentario


@login_required
@require_http_methods(["POST", "DELETE"])
def reagir_ao_comentario_view(request: HttpRequest, id_comentario: int):
    usuario = cast(User, request.user)
    try:
        comentario = Comentario.objects.get(pk=id_comentario)
    except Comentario.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == "DELETE":
        try:
            reacao = ReacaoComentarioModel.objects.get(usuario=usuario)
            reacao.delete()
            return HttpResponse(
                ReacaoComentario().render(context=Context({"comentario": comentario})),
                status=200,
            )
        except ReacaoComentarioModel.DoesNotExist:
            return HttpResponseNotFound()

    else:
        if usuario != comentario.do_autor:
            if RelacaoModel.relacoes.existe_relacao_entre(
                usuario, comentario.do_autor, "BLQ"
            ):
                return HttpResponseForbidden()

        try:
            reacao = ReacaoComentarioModel.objects.get(usuario=usuario)
        except ReacaoComentarioModel.DoesNotExist:
            reacao = ReacaoComentarioModel(usuario=usuario, comentario=comentario)

        reacao.tipo = request.POST.dict().get("reacao", "")
        try:
            reacao.full_clean()
        except ValidationError:
            return HttpResponseBadRequest()

        reacao.save()
        setattr(comentario, "minha_reacao", [reacao])
        return HttpResponse(
            ReacaoComentario().render(context=Context({"comentario": comentario})),
            status=201,
        )
