from typing import Literal
from django.db import models

from ond_eventos.models.cidade import Cidade
from ond_eventos.models.ondevento import OndEvento, Tipo


CAMPOS_ORDENACAO = Literal["inicio", "confirmados", "comentarios"]

TP_OND_EVENTO = Literal[
    "FEST",
    "BAR",
    "ROLE",
    "BLOQ",
    "SHOW",
    "ANIV",
    "FORM",
    "CASA",
    "CULT",
    "FEIR",
    "OUTR",
]


def filtro_por_tipo(
    consulta: models.QuerySet,
    tipos: list[
        Literal[
            "FEST",
            "BAR",
            "ROLE",
            "BLOQ",
            "SHOW",
            "ANIV",
            "FORM",
            "CASA",
            "CULT",
            "FEIR",
            "OUTR",
        ]
    ],
):
    return consulta.filter(tipo__in=tipos)


def ordenar_por_campo(consulta: models.QuerySet, campo: CAMPOS_ORDENACAO = "inicio"):
    if campo == "confirmados":
        return consulta.order_by("-numero_confirmados")
    elif campo == "comentarios":
        return consulta.order_by("-contagem_de_comentarios")
    elif campo == "proximidade":
        return consulta.order_by("distancia_usuario")
    return consulta.order_by(campo)
