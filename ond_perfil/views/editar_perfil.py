from uuid import uuid4
from typing import cast

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

from ond_social.forms import EditarPerfilForm
from ond_perfil.models import User
from ond_social import dominio as social


@login_required
def editar_perfil_view(request: HttpRequest):
    perfil = cast(User, request.user)
    if request.method == "GET":
        return render(
            request,
            "pagina/editar-perfil.html",
            context={
                "form": EditarPerfilForm(
                    initial={
                        "username": perfil.username,
                        "bio": perfil.bio,
                        "insta": perfil.insta,
                        "x": perfil.x,
                    }
                )
            },
        )

    form = EditarPerfilForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(
            request,
            "pagina/editar-perfil.html",
            context={"form": form},
        )

    social.editar_perfil(perfil, form.cleaned_data)

    return redirect("perfil:perfil", id_usuario=request.user.pk, permanent=False)
