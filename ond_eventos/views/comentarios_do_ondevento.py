from django.shortcuts import render
from django.http import (
    HttpRequest,
    HttpResponseNotFound,
)
from django.core.paginator import Paginator
from django.db.models import Prefetch

from ond_eventos.forms import ComentarioForm
from ond_eventos.models import OndEvento
from ond_perfil.models import User
from ond_social.models import (
    Comentario,
    ReacaoComentarioModel,
    RespostaComentario,
    ReacaoRespostaComentarioModel,
)


def comentarios_do_ondevento_view(request: HttpRequest, id_ondevento: int):
    try:
        ondevento = OndEvento.objects.get(pk=id_ondevento)
    except OndEvento.DoesNotExist:
        return HttpResponseNotFound()

    comentarios = Comentario.objects.filter(
        no_evento=ondevento, deletado=False
    ).order_by("-momento")

    usuario = request.user
    if usuario.is_authenticated:
        comentarios = comentarios.prefetch_related(
            Prefetch(
                "reacoes_do_comentario",
                ReacaoComentarioModel.objects.filter(usuario=usuario),
                "minha_reacao",
            )
        ).prefetch_related(
            Prefetch(
                "respostas_do_comentario",
                RespostaComentario.objects.prefetch_related(
                    Prefetch(
                        "reacoes_da_resposta_comentario",
                        ReacaoRespostaComentarioModel.objects.filter(usuario=usuario),
                        "minha_reacao",
                    )
                ),
            )
        )

    comentarios_paginados = Paginator(comentarios, 5)
    pagina_pedida = request.GET.get("pagina", 1)

    return render(
        request,
        "pagina/secoes-pagina/ondevento-home/secao-comentario.html",
        {
            "ondevento": ondevento,
            "comentario_form": ComentarioForm(),
            "comentarios_do_evento": comentarios_paginados.page(pagina_pedida),
        },
    )
