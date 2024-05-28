from typing import cast

from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseNotFound,
)
from django.contrib.auth.decorators import login_required
from django.template import Context

from ond_perfil.models import User
from ond_social.models import Comentario
from ond_social.componentes import OpcoesComentario


@login_required
def opcoes_comentario_view(request: HttpRequest, id_comentario: int):
    usuario = cast(User, request.user)
    try:
        comentario = Comentario.objects.get(pk=id_comentario)
    except Comentario.DoesNotExist:
        return HttpResponseNotFound()

    opcoes = {"comentario": comentario, "deletar": False}
    if comentario.do_autor == usuario:
        opcoes["deletar"] = True

    return HttpResponse(OpcoesComentario().render(Context(opcoes)))
