from django.db import models

from .resposta_comentario import RespostaComentario
from ond_perfil.models import User


class Reacoes(models.TextChoices):
    LIKE = "LIKE", "Like"
    UTIL = "UTIL", "Util"


class ReacaoRespostaComentarioModel(models.Model):
    Reacoes = Reacoes

    usuario = models.ForeignKey(
        User,
        null=False,
        on_delete=models.DO_NOTHING,
        related_name="minhas_reacoes_resposta_comentario",
    )
    tipo = models.CharField(max_length=4, choices=Reacoes.choices, null=False)
    resposta = models.ForeignKey(
        RespostaComentario,
        null=False,
        on_delete=models.DO_NOTHING,
        related_name="reacoes_da_resposta_comentario",
    )
    momento = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reacao_resposta_comentario"
        indexes = [models.Index(fields=["usuario", "resposta"])]
