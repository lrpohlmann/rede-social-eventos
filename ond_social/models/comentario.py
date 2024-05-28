from ond_perfil.models import User
from ond_eventos.models.ondevento import OndEvento


from django.db import models


class Comentario(models.Model):
    corpo = models.TextField(max_length=120, blank=False, null=False)
    momento = models.DateTimeField(auto_now=True)
    alteracao = models.DateTimeField(auto_now_add=True)
    do_autor = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="comentarios_realizados",
        blank=False,
        null=False,
    )
    no_evento = models.ForeignKey(
        OndEvento,
        on_delete=models.CASCADE,
        related_name="comentarios_do_evento",
        blank=False,
        null=False,
    )
    deletado = models.BooleanField(default=False)
