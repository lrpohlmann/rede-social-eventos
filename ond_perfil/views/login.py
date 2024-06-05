from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from ond_perfil.forms import LoginForm


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("ond-e-hj")

    login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            if usuario_autenticado := authenticate(
                request,
                email=login_form.cleaned_data.get("email"),
                password=login_form.cleaned_data.get("senha"),
            ):
                login(request, usuario_autenticado)
                return redirect("ond-e-hj")

    return render(request, "pagina/login.html", context={"login_form": login_form})
