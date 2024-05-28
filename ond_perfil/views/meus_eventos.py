from typing import cast

from django.shortcuts import render
from django.http import (
    HttpRequest,
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from ond_perfil.models import User
from ond_eventos.models import OndEvento


@login_required
def meus_eventos_view(request: HttpRequest):
    eu = cast(User, request.user)
    pagina = request.GET.get("pagina", 1)
    paginador = Paginator(OndEvento.eventos.filter(autor=eu).order_by("-inicio"), 4)
    pagina_evento = paginador.get_page(pagina)
    return render(
        request,
        "pagina/meus-eventos.html",
        context={"meus_eventos": pagina_evento},
    )
