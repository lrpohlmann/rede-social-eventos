from typing import cast

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.core.paginator import Paginator

from ond_perfil.models import User
from ond_notificacao.models import AtividadeModel


@login_required
def minhas_notificacoes(request: HttpRequest):
    usuario = cast(User, request.user)
    pagina_notificacoes = Paginator(
        AtividadeModel.objects.prefetch_related("ator")
        .filter(notificar_para=usuario, visto=False)
        .order_by("-criacao"),
        10,
    )

    return render(
        request,
        "pagina/notificacoes.html",
        context={
            "notificacoes": pagina_notificacoes.get_page(request.GET.get("pagina", 1))
        },
    )
