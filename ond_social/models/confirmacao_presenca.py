from django.db import models

from ond_perfil.models import User
from ond_eventos.models.ondevento import OndEvento


class ConfirmacaoPresenca(models.Model):
    do_usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="confirmacoes_de_presenca",
        blank=False,
        null=False,
    )
    no_evento = models.ForeignKey(
        OndEvento,
        on_delete=models.CASCADE,
        related_name="confirmados_no_evento",
        blank=False,
        null=False,
    )
    momento = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["do_usuario", "no_evento"],
                name="unica_confirmacao_usuario_evento",
            )
        ]
