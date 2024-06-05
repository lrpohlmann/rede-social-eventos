from django.shortcuts import redirect, resolve_url
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse


def logout_view(request: HttpRequest):
    if request.user.is_authenticated and request.method == "POST":
        logout(request)
        return HttpResponse(headers={"HX-Redirect": resolve_url("ond-e-hj")})

    return redirect("ond-e-hj")
