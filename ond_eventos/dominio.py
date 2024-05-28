from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Any, TypeGuard
from zoneinfo import ZoneInfo

from django.http import QueryDict
from django.utils import timezone
from django.db.models import QuerySet

from ond_eventos.models import (
    CAMPOS_ORDENACAO,
    OndEvento,
    Cidade,
    filtro_por_tipo,
    ordenar_por_campo,
    TP_OND_EVENTO,
)
from .forms import OndEHojeForm


def type_guard_e_list_str(o: object) -> TypeGuard[list[str]]:
    return isinstance(o, list)


@dataclass(slots=True)
class AdaptadorHojeEOndPerguntaParaConsulta:
    pesquisa_cidade: str | None
    cidade: Cidade | int
    data_inicio: date | datetime
    nome: str | None = None
    tipo_evento: list[TP_OND_EVENTO] = field(default_factory=list)
    ordenacao: CAMPOS_ORDENACAO = "inicio"

    def __post_init__(self):
        if isinstance(self.cidade, (int, str)):
            self.cidade = Cidade.objects.get(pk=int(self.cidade))

        if isinstance(self.data_inicio, date):
            self.data_inicio = datetime.combine(self.data_inicio, time(0, 0))
        self.data_inicio = timezone.make_aware(
            self.data_inicio, ZoneInfo(self.cidade.fuso)
        )


@dataclass(slots=True)
class OndHjResposta:
    ondeventos: QuerySet
    form: OndEHojeForm


def ond_hj(dados: dict[str, Any] | QueryDict) -> OndHjResposta:
    form = OndEHojeForm(dados, initial=dados)
    if not form.is_valid():
        return OndHjResposta(OndEvento.objects.none(), form)

    dados_consulta = AdaptadorHojeEOndPerguntaParaConsulta(**form.cleaned_data)

    consulta = OndEvento.eventos.prefetch_related(
        "confirmados_no_evento__do_usuario"
    ).filter(inicio__gte=dados_consulta.data_inicio, cidade=dados_consulta.cidade)

    if dados_consulta.nome:
        consulta = consulta.filter(nome__icontains=dados_consulta.nome)
    if dados_consulta.tipo_evento:
        consulta = filtro_por_tipo(consulta, dados_consulta.tipo_evento)
    if dados_consulta.ordenacao:
        consulta = ordenar_por_campo(consulta, dados_consulta.ordenacao)

    return OndHjResposta(consulta, form)


def criar_ondevento(dados, autor):
    ondevento = OndEvento(
        nome=dados["nome"],
        tipo=dados["tipo"],
        inicio=datetime.combine(
            dados["data_inicio"],
            dados["hora_inicio"],
            tzinfo=ZoneInfo(dados["cidade"].fuso),
        ),
        fim=datetime.combine(
            dados["data_fim"], dados["hora_fim"], tzinfo=ZoneInfo(dados["cidade"].fuso)
        ),
        descricao=dados["descricao"],
        autor=autor,
        cidade=dados["cidade"],
        endereco=dados.get("endereco"),
    )
    ondevento.save()

    ondevento.capa = dados.get("capa")
    ondevento.save()
    return ondevento


def ondevento_e_editavel(ondevento: OndEvento):
    if ondevento.situacao not in ["ABERTO", "OCORRENDO"]:
        return False

    return True


def editar_ondevento(ondevento: OndEvento, dados: dict) -> OndEvento:
    ondevento.nome = dados["nome"]
    ondevento.capa = dados.get("capa")
    ondevento.tipo = dados["tipo"]
    ondevento.inicio = datetime.combine(
        dados["data_inicio"],
        dados["hora_inicio"],
        tzinfo=ZoneInfo(dados["cidade"].fuso),
    )
    ondevento.fim = datetime.combine(
        dados["data_fim"], dados["hora_fim"], tzinfo=ZoneInfo(dados["cidade"].fuso)
    )
    ondevento.descricao = dados["descricao"]
    ondevento.cidade = dados["cidade"]
    ondevento.endereco = dados.get("endereco")

    ondevento.save(force_update=True)
    return ondevento
