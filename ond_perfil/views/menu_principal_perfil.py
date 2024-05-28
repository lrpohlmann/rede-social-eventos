from typing import cast

from django.shortcuts import render
from django.http import (
    HttpRequest,
)
from django.contrib.auth.decorators import login_required

from ond_perfil.models import User


@login_required
def menu_principal_perfil_view(request: HttpRequest):
    usuario = cast(User, request.user)
    return render(request, "pagina/menu-usuario.html", context={"usuario": usuario})
