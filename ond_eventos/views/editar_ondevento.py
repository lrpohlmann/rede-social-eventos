from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseNotFound, HttpResponseForbidden

from ond_eventos.models import OndEvento
from ond_eventos.forms import ManipularOndEventoForm
from ond_eventos import dominio as eventos


@login_required
def editar_ondevento_view(request: HttpRequest, id_ondevento: int):
    try:
        ondevento: OndEvento = OndEvento.eventos.get(pk=id_ondevento)
    except OndEvento.DoesNotExist:
        return HttpResponseNotFound("Evento não encontrado")

    if request.user != ondevento.autor:
        return HttpResponseForbidden("Apenas o autor pode editar o evento.")

    if not eventos.ondevento_e_editavel(ondevento):
        return HttpResponseForbidden("Não é possível mais editar este evento.")

    if request.method == "GET":
        return render(
            request,
            "pagina/editar-ondevento.html",
            {
                "form_editar_evento": ManipularOndEventoForm(
                    initial={
                        "nome": ondevento.nome,
                        "tipo": ondevento.tipo,
                        "data_inicio": ondevento.inicio.strftime("%Y-%m-%d"),
                        "hora_inicio": ondevento.inicio.strftime("%H:%M"),
                        "data_fim": ondevento.fim.strftime("%Y-%m-%d"),
                        "hora_fim": ondevento.fim.strftime("%H:%M"),
                        "descricao": ondevento.descricao,
                        "cidade": ondevento.cidade,
                        "endereco": ondevento.endereco,
                    }
                ),
                "ondevento": ondevento,
            },
        )

    form = ManipularOndEventoForm(request.POST, request.FILES)
    if form.is_valid():
        eventos.editar_ondevento(ondevento, form.cleaned_data)
        return redirect("evento:ondevento_home", id_ondevento=id_ondevento)

    return render(
        request,
        "pagina/editar-ondevento.html",
        {"form_editar_evento": form, "ondevento": ondevento},
    )


"""
DUPLICAÇÃO NA EDIÇÃO
"""
