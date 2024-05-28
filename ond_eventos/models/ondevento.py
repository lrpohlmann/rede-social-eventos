from datetime import datetime, timedelta
from typing import Any, Literal
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import models
from django.db.models import Case, When, Value, Count, F, Q
from django.db.models.lookups import LessThan
from django.db.models.query import QuerySet

from ond_perfil.models import User
from ond_eventos.models.cidade import Cidade


class OndEventoManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        situacao = Case(
            When(
                inicio__gt=datetime.now(ZoneInfo("America/Sao_Paulo")),
                then=Value("ABERTO"),
            ),
            When(
                inicio__lt=datetime.now(ZoneInfo("America/Sao_Paulo")),
                fim__gte=datetime.now(ZoneInfo("America/Sao_Paulo")),
                then=Value("OCORRENDO"),
            ),
            When(
                LessThan(
                    datetime.now(ZoneInfo("America/Sao_Paulo")) - F("fim"),  # type: ignore
                    timedelta(seconds=86400),
                ),
                then=Value("AFTER"),
            ),
            default=Value("FECHADO"),
        )
        return (
            super()
            .get_queryset()
            .annotate(
                numero_confirmados=Count("confirmados_no_evento", distinct=True),
                contagem_de_comentarios=Count(
                    "comentarios_do_evento",
                    filter=Q(comentarios_do_evento__deletado=False),
                    distinct=True,
                ),
                situacao=situacao,
            )
        )


class Tipo(models.TextChoices):
    FESTA = "FEST", "Festa"
    BAR = "BAR", "Bar"
    ROLE = "ROLE", "Rolê de Rua"
    BLOQUINHO = "BLOQ", "Bloquinho"
    SHOW = "SHOW", "Show"
    ANIVERSARIO = "ANIV", "Aniversário"
    FORMATURA = "FORM", "Formatura"
    CASAMENTO = "CASA", "Casamento"
    CULTURAL = "CULT", "Evento Cultural"
    FEIRA = "FEIR", "Feira"
    OUTRO = "OUTR", "Outro"


def _foto_capa_upload(instance, filename):
    return f"evento/{instance.pk}/capa/{filename}"


class OndEvento(models.Model):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._situacao: Literal["ABERTO", "OCORRENDO", "AFTER", "FECHADO"] | None = None
        self.contagem_de_comentarios: int | None = None
        self.numero_confirmados: int | None = None
        super().__init__(*args, **kwargs)

    objects = models.Manager()
    eventos = OndEventoManager()

    NOME_MAX_LENGTH = 100

    Tipo = Tipo

    nome = models.TextField(
        verbose_name="nome do evento",
        max_length=NOME_MAX_LENGTH,
        blank=False,
        null=False,
    )
    capa = models.ImageField(null=True, upload_to=_foto_capa_upload)
    tipo = models.CharField(
        verbose_name="tipo de evento",
        max_length=4,
        choices=Tipo.choices,
        unique=False,
        null=False,
    )
    inicio = models.DateTimeField("início do evento", null=False, blank=False)
    fim = models.DateTimeField("fim do evento", null=False, blank=False)
    descricao = models.TextField(
        verbose_name="Descrição", max_length=120, null=False, blank=False
    )
    autor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="eventos_criados"
    )
    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.DO_NOTHING,
        related_name="eventos_da_cidade",
        null=False,
        unique=False,
        blank=False,
    )
    endereco = models.TextField(max_length=200, null=True, blank=False)

    @property
    def situacao(self):
        if self._situacao is not None:
            return self._situacao

        momento = datetime.now(tz=ZoneInfo(settings.TIME_ZONE))
        if self.inicio > momento:
            return "ABERTO"
        elif self.inicio < momento and momento <= self.fim:
            return "OCORRENDO"
        elif (momento - self.fim) < timedelta(days=1):
            return "AFTER"
        else:
            return "FECHADO"

    @situacao.setter
    def situacao(self, x):
        self._situacao = x

    def __str__(self) -> str:
        return f"{self.nome:20} - {self.tipo} - {self.inicio}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(fim__gte=models.F("inicio")),
                name="fim_depois_do_inicio",
                violation_error_message="Data de início depois da de fim",
            )
        ]
