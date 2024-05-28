from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render

from ond_eventos.models import Cidade


def option_cidade_view(request: HttpRequest):
    pesquisa = request.GET.get("pesquisa_cidade", "")
    if len(pesquisa) > 100:
        return HttpResponseBadRequest()

    if pesquisa:
        cidades = Cidade.objects.filter(nome__istartswith=pesquisa)[0:10]
    else:
        cidades = Cidade.objects.none()

    return render(
        request,
        "componente/input/option_sem_widget.html",
        context={"opcoes": [(c.pk, str(c)) for c in cidades]},
    )
