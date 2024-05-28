from django.db import models

from ond_perfil.models import User
from ond_eventos.models.ondevento import OndEvento


class ConviteOndEvento(models.Model):
    de = models.ForeignKey(
        User, related_name="convite_enviado", on_delete=models.CASCADE
    )
    para = models.ForeignKey(
        User, related_name="convite_recebido", on_delete=models.CASCADE
    )
    evento = models.ForeignKey(
        OndEvento, related_name="convidados", on_delete=models.CASCADE
    )
    momento = models.DateTimeField(auto_now=True)
