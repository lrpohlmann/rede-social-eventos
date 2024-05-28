from typing import cast

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.template import Template, Context

from ond_perfil.models import User
from ond_social.models import Comentario, RespostaComentario
from ond_social.forms.responder_comentario import RespostaComentarioForm
from ond_social import dominio as social
from ond_social.componentes import RespostaComentarioColorido


@login_required
def responder_comentario_view(request: HttpRequest, id_comentario: int):
    user = cast(User, request.user)
    try:
        comentario = Comentario.objects.get(pk=id_comentario)
    except Comentario.DoesNotExist:
        return HttpResponseNotFound()

    e_possivel, motivo = social.e_possivel_responder(user, comentario)
    if not e_possivel:
        return HttpResponseForbidden(motivo)

    form = RespostaComentarioForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()

    resposta: RespostaComentario = form.save(commit=False)
    resposta.do_autor = user
    resposta.para = comentario
    resposta.save()
    return HttpResponse(
        RespostaComentarioColorido().render(Context({"resposta": resposta})),
        status=201,
        headers={"HX-Trigger": "respostaCriada"},
    )
