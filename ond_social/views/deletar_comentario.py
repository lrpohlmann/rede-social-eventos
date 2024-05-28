from typing import cast

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import (
    HttpRequest,
    HttpResponseNotFound,
    HttpResponseForbidden,
    HttpResponse,
)

from ond_perfil.models import User
from ond_social.models import Comentario
from ond_social.dominio import deletar_comentario, AcaoNaoPermitidaException


@login_required
@require_POST
def deletar_comentario_view(request: HttpRequest, id_comentario: int):
    usuario = cast(User, request.user)
    try:
        comentario = Comentario.objects.get(pk=id_comentario)
    except Comentario.DoesNotExist:
        return HttpResponseNotFound()

    try:
        deletar_comentario(usuario, comentario)
        return HttpResponse(status=200, headers={"HX-Trigger": "comentarioDeletado"})
    except AcaoNaoPermitidaException:
        return HttpResponseForbidden()
