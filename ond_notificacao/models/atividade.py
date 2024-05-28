from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from ond_perfil.models import User


class TipoAtividade(models.TextChoices):
    COMENTOU = "COMENTOU"
    SEGUIU = "SEGUIU"
    CONVIDOU = "CONVIDOU"


class AtividadeModel(models.Model):
    TipoAtividade = TipoAtividade

    ator = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="atividades"
    )

    acao_nome = models.TextField(
        max_length=10, choices=TipoAtividade.choices, blank=False, null=False
    )
    acao_model = models.ForeignKey(
        ContentType, on_delete=models.DO_NOTHING, related_name="atividade_acao"
    )
    acao_id = models.PositiveIntegerField(null=False)
    acao_objeto = GenericForeignKey("acao_model", "acao_id")

    alvo_model = models.ForeignKey(
        ContentType, on_delete=models.DO_NOTHING, related_name="atividade_alvo"
    )
    alvo_id = models.PositiveIntegerField(null=False)
    alvo_objeto = GenericForeignKey("alvo_model", "alvo_id")

    notificar_para = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="minhas_notificacoes", null=True
    )
    visto = models.BooleanField(default=False)
    criacao = models.DateTimeField(auto_now=True)
    alteracao = models.DateTimeField(auto_now_add=True)
    deletado = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        match self.acao_nome:
            case TipoAtividade.COMENTOU:
                return f"{self.ator.username} comentou um evento seu"
            case TipoAtividade.CONVIDOU:
                return f"{self.ator.username} te convidou para um evento"
            case TipoAtividade.SEGUIU:
                return f"{self.ator.username} te seguiu"
            case _:
                raise Exception()

    class Meta:
        indexes = [
            models.Index(fields=["notificar_para", "visto"]),
            models.Index(fields=["id", "notificar_para"]),
        ]
