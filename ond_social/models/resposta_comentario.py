from ond_perfil.models import User
from .comentario import Comentario


from django.db import models


class RespostaComentario(models.Model):
    corpo = models.TextField(max_length=120, blank=False, null=False)
    momento = models.DateTimeField(auto_now=True)
    do_autor = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="respostas_dadas",
        blank=False,
        null=False,
    )
    para = models.ForeignKey(
        Comentario,
        on_delete=models.CASCADE,
        related_name="respostas_do_comentario",
        blank=False,
        null=False,
    )
