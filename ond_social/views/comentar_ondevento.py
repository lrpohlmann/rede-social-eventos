from typing import cast

from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.contrib.auth.decorators import login_required
from django.template import Context

from ond_eventos.forms import ComentarioForm
from ond_eventos.models import OndEvento
from ond_perfil.models import User
from ond_social import dominio as social
from ond_social.componentes import Conversa


@login_required
def comentar_ondevento_view(request: HttpRequest, id_ondevento: int):
    request.user = cast(User, request.user)
    try:
        ondevento = OndEvento.objects.get(pk=id_ondevento)
    except OndEvento.DoesNotExist:
        return HttpResponseNotFound(
            "Evento foi deletado ou não existe.",
        )

    e_possivel, motivo = social.e_possivel_comentar(request.user, ondevento)
    if not e_possivel:
        return HttpResponseForbidden(motivo)

    form = ComentarioForm(request.POST)
    if form.is_valid():
        comentario = social.comentar(request.user, ondevento, form.cleaned_data)  # type: ignore
        return HttpResponse(
            Conversa().render(Context({"comentario": comentario})),
            status=201,
        )

    return HttpResponseBadRequest("")
