from typing import Literal, NamedTuple, TypeGuard

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from ond_perfil.models import User


class RelacaoManager(models.Manager):
    class QuadroRelacao(NamedTuple):
        eu_com_ele: Literal["SEG", "BLQ"] | None
        ele_comigo: Literal["SEG", "BLQ"] | None

    def existe_relacao_entre(
        self,
        usuario1: User,
        usuario2: User,
        status: Literal["SEG", "BLQ"] | None = None,
    ):
        if status:
            return (
                self.get_queryset()
                .filter(
                    models.Q(de=usuario1, com=usuario2, status=status)
                    | models.Q(de=usuario2, com=usuario1, status=status)
                )
                .exists()
            )

        return (
            self.get_queryset()
            .filter(
                models.Q(de=usuario1, com=usuario2)
                | models.Q(de=usuario2, com=usuario1)
            )
            .exists()
        )

    def obter_relacao(
        self, de: User, com: User, status: Literal["SEG", "BLQ"] | None = None
    ):
        try:
            if status:
                return self.get_queryset().get(de=de, com=com, status=status)

            return self.get_queryset().get(de=de, com=com)
        except ObjectDoesNotExist:
            return None

    def relacao_entre(self, eu: User, ele: User) -> QuadroRelacao | None:
        try:
            eu_com_ele = RelacaoModel.relacoes.only("status").get(de=eu, com=ele).status
        except RelacaoModel.DoesNotExist:
            eu_com_ele = None

        try:
            ele_comigo = RelacaoModel.relacoes.only("status").get(de=ele, com=eu).status
        except RelacaoModel.DoesNotExist:
            ele_comigo = None

        if tg_status_relacao_ou_none(eu_com_ele) and tg_status_relacao_ou_none(
            ele_comigo
        ):
            quadro = self.QuadroRelacao(eu_com_ele=eu_com_ele, ele_comigo=ele_comigo)
            if quadro == (None, None):
                return None

            return quadro

        return None


class Status(models.TextChoices):
    SEGUINDO = "SEG", "Seguindo"
    BLOCK = "BLQ", "Bloqueado"


class RelacaoModel(models.Model):
    objects = models.Manager()
    relacoes = RelacaoManager()

    Status = Status

    de = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="relacao_emitida",
        null=False,
        blank=False,
    )
    com = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="relacao_recebida",
        null=False,
        blank=False,
    )
    status = models.CharField(choices=Status.choices, max_length=3)
    criacao = models.DateTimeField(auto_now=True)
    alteracao = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["de", "com"], name="unico_relacionamento")
        ]

        indexes = [
            models.Index(fields=["de", "com"], name="de_com_indice"),
        ]

    def __str__(self):
        return f"{self.__class__.__name__}: {self.de} {self.status} {self.com}"


def tg_status_relacao_ou_none(o: object) -> TypeGuard[Literal["SEG", "BLQ"] | None]:
    assert (o in Status.values) or (o is None)
    return True
