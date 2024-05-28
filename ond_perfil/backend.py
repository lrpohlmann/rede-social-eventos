from typing import Any

from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from .models import User


class AutenticacaoOnd(BaseBackend):
    def authenticate(self, request: HttpRequest | None, **kwargs: Any):
        model_usuario = User
        email = kwargs["email"]
        password = kwargs["password"]

        try:
            usuario = model_usuario.objects.get(email=email)
        except model_usuario.DoesNotExist:
            return None

        if usuario.check_password(password):
            return usuario
        else:
            return None

    def get_user(self, user_id):
        model_usuario = User
        try:
            return model_usuario.objects.get(pk=user_id)
        except model_usuario.DoesNotExist:
            return None
