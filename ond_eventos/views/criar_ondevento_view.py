from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpRequest,
)
from django.conf import settings
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ond_eventos.dominio import criar_ondevento
from ond_eventos.forms import ManipularOndEventoForm


@require_http_methods(["GET", "POST"])
@login_required
def criar_ondevento_view(request: HttpRequest):
    if request.method == "GET":
        return render(
            request,
            "pagina/criar-ondevento.html",
            context={
                "formulario_criar_evento": ManipularOndEventoForm(),
            },
        )
    else:
        form = ManipularOndEventoForm(request.POST, request.FILES)
        if form.is_valid():
            dados = form.cleaned_data

            ondevento = criar_ondevento(dados, request.user)

            return HttpResponse(
                status=201,
                headers={
                    "HX-Redirect": reverse(
                        "evento:ondevento_home", kwargs={"id_ondevento": ondevento.pk}
                    )
                },
            )
        else:
            return render(
                request,
                "fragmentos/form-manipular-ondevento.html",
                context={
                    "formulario_criar_evento": form,
                },
            )
