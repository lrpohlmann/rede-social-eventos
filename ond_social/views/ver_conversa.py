from typing import cast

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseNotFound
from django.db.models import Prefetch

from ond_social.models import (
    Comentario,
    ReacaoComentarioModel,
    ReacaoRespostaComentarioModel,
    RespostaComentario,
)
from ond_social.forms.responder_comentario import RespostaComentarioForm
from ond_perfil.models import User


@login_required
def ver_conversa_view(request: HttpRequest, id_comentario: int):
    usuario = cast(User, request.user)
    try:
        comentario = (
            Comentario.objects.prefetch_related(
                Prefetch(
                    "reacoes_do_comentario",
                    ReacaoComentarioModel.objects.filter(usuario=usuario),
                    "minha_reacao",
                )
            )
            .prefetch_related(
                Prefetch(
                    "respostas_do_comentario",
                    RespostaComentario.objects.prefetch_related(
                        Prefetch(
                            "reacoes_da_resposta_comentario",
                            ReacaoRespostaComentarioModel.objects.filter(
                                usuario=usuario
                            ),
                            "minha_reacao",
                        )
                    ),
                )
            )
            .get(pk=id_comentario, deletado=False)
        )
        return render(
            request,
            "pagina/ver-conversa.html",
            {"comentario": comentario, "form": RespostaComentarioForm()},
        )
    except Comentario.DoesNotExist:
        return HttpResponseNotFound()
