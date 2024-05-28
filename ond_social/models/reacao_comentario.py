from django.db import models

from .comentario import Comentario
from ond_perfil.models import User


class Reacoes(models.TextChoices):
    LIKE = "LIKE", "Like"
    UTIL = "UTIL", "Util"


class ReacaoComentarioModel(models.Model):
    Reacoes = Reacoes

    usuario = models.ForeignKey(
        User, null=False, on_delete=models.DO_NOTHING, related_name="minhas_reacoes"
    )
    tipo = models.CharField(max_length=4, choices=Reacoes.choices, null=False)
    comentario = models.ForeignKey(
        Comentario,
        null=False,
        on_delete=models.DO_NOTHING,
        related_name="reacoes_do_comentario",
    )
    momento = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reacao_comentario"
        indexes = [models.Index(fields=["usuario", "comentario"])]
