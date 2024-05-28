from typing import cast

from django.shortcuts import render
from django.http import (
    HttpRequest,
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from ond_perfil.models import User
from ond_social.models import ConviteOndEvento


@login_required
def meus_convites_view(request: HttpRequest):
    eu = cast(User, request.user)

    if request.GET.get("tipo_convite") == "enviado":
        paginador = Paginator(
            ConviteOndEvento.objects.prefetch_related("de", "para")
            .filter(de=eu)
            .order_by("-momento"),
            5,
        )
    else:
        paginador = Paginator(
            ConviteOndEvento.objects.prefetch_related("de", "para")
            .filter(para=eu)
            .order_by("-momento"),
            5,
        )

    pagina_convites = paginador.get_page(request.GET.get("pagina", 1))
    return render(
        request,
        "pagina/meus-convites.html",
        context={"lista_convites": pagina_convites},
    )
