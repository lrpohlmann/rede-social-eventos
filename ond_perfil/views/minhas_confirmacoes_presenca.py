from typing import cast

from django.shortcuts import render
from django.http import (
    HttpRequest,
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from ond_perfil.models import User
from ond_social.models import ConfirmacaoPresenca


@login_required
def minhas_confirmacoes_de_presenca_view(request: HttpRequest):
    eu = cast(User, request.user)
    paginador = Paginator(
        ConfirmacaoPresenca.objects.prefetch_related("no_evento")
        .filter(do_usuario=eu)
        .order_by("-momento")
        .all(),
        10,
    )
    minhas_confirmacoes = paginador.get_page(request.GET.get("pagina", 1))
    return render(
        request,
        "pagina/minhas-confirmacoes-presenca.html",
        {"minhas_confirmacoes": minhas_confirmacoes},
    )
