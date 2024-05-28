from functools import wraps
from typing import Literal
from ond_notificacao.models import AtividadeModel
from ond_perfil.models import User
from ond_social.models import RelacaoModel


class AutorelacionamentoException(Exception):
    def __init__(self, usuario, *args: object) -> None:
        self.usuario = usuario
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: Usuário {self.usuario} não relacionar-se consigo mesmo."


class BloqueadoException(Exception):
    def __init__(self, usuario1: User, usuario2: User, *args: object) -> None:
        self.usuario1 = usuario1
        self.usuario2 = usuario2
        super().__init__(*args)

    def __str__(self) -> str:
        return f"BloqueadoException: Relação entre {self.usuario1} e {self.usuario2} bloqueada."


def nao_permitir_autorelacionamento(operacao_relacionamento):
    @wraps(operacao_relacionamento)
    def _(emissor, receptor, **kwargs):
        if emissor == receptor:
            raise AutorelacionamentoException(usuario=emissor)
        else:
            return operacao_relacionamento(emissor, receptor, **kwargs)

    return _


@nao_permitir_autorelacionamento
def seguir(emissor: User, receptor: User) -> RelacaoModel:
    if RelacaoModel.relacoes.existe_relacao_entre(emissor, receptor, "BLQ"):
        raise BloqueadoException(emissor, receptor)

    relacao, criado = RelacaoModel.objects.get_or_create(
        de=emissor, com=receptor, status=RelacaoModel.Status.SEGUINDO
    )
    if criado:
        relacao.save()
        AtividadeModel(
            ator=relacao.de,
            acao_nome=AtividadeModel.TipoAtividade.SEGUIU,
            acao_objeto=relacao,
            alvo_objeto=relacao.com,
            notificar_para=relacao.com,
        ).save()
    return relacao


@nao_permitir_autorelacionamento
def deseguir(emissor: User, receptor: User) -> Literal[True] | None:
    if relacao_seguidor := RelacaoModel.relacoes.obter_relacao(
        emissor, receptor, "SEG"
    ):
        relacao_seguidor.delete()

        return True

    else:
        return None


@nao_permitir_autorelacionamento
def desbloquear(emissor: User, receptor: User) -> Literal[True] | None:
    if relacao_bloqueio := RelacaoModel.relacoes.obter_relacao(
        de=emissor, com=receptor, status="BLQ"
    ):
        relacao_bloqueio.delete()
        return True

    return None


@nao_permitir_autorelacionamento
def bloquear(emissor: User, receptor: User) -> RelacaoModel:
    if relacao_atual := RelacaoModel.relacoes.obter_relacao(de=emissor, com=receptor):
        if relacao_atual.status == RelacaoModel.Status.BLOCK:
            return relacao_atual

        relacao_atual.status = RelacaoModel.Status.BLOCK
        relacao_atual.save()

        relacao_recebida_de_seguidor_bloqueado = emissor.relacao_recebida.filter(
            de=receptor, status=RelacaoModel.Status.SEGUINDO
        )
        relacao_recebida_de_seguidor_bloqueado.delete()

        return relacao_atual

    novo_bloqueio = RelacaoModel(
        de=emissor, com=receptor, status=RelacaoModel.Status.BLOCK
    )
    novo_bloqueio.save()

    relacao_recebida_de_seguidor_bloqueado = emissor.relacao_recebida.filter(
        de=receptor, status=RelacaoModel.Status.SEGUINDO
    )
    relacao_recebida_de_seguidor_bloqueado.delete()

    return novo_bloqueio
