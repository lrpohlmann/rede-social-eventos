from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, resolve_url

from ond_perfil.forms import CriarContaForm


def criar_conta_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("pergunta:ond-e-hj")

    criar_conta_form = CriarContaForm()
    if request.method == "POST":
        criar_conta_form = CriarContaForm(request.POST)
        if criar_conta_form.is_valid():
            criar_conta_form.save(commit=True)
            return HttpResponse(
                status=201, headers={"HX-Redirect": resolve_url("conta:login")}
            )

    return render(
        request,
        "pagina/criar-conta.html",
        context={"criar_conta_form": criar_conta_form},
    )
