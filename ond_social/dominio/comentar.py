from typing import Literal
import enum

from django.contrib.contenttypes.models import ContentType
from django.db.transaction import atomic

from ond_eventos.models import OndEvento
from ond_notificacao.models import AtividadeModel
from ond_perfil.models import User
from ond_social.models import Comentario, RelacaoModel


@atomic
def deletar_comentario(usuario: User, comentario: Comentario):
    if usuario != comentario.do_autor:
        raise AcaoNaoPermitidaException()

    comentario.deletado = True
    comentario.save()
    AtividadeModel.objects.filter(
        acao_id=comentario.pk, acao_model=ContentType.objects.get_for_model(Comentario)
    ).update(deletado=True)
    return comentario


class AcaoNaoPermitidaException(Exception):
    pass


def comentar(
    usuario: User, evento: OndEvento, dados: dict[Literal["corpo"], str]
) -> Comentario:
    comentario = Comentario(do_autor=usuario, no_evento=evento, corpo=dados["corpo"])
    comentario.save()
    AtividadeModel(
        ator=usuario,
        acao_nome=AtividadeModel.TipoAtividade.COMENTOU,
        acao_objeto=comentario,
        alvo_objeto=evento,
        notificar_para=evento.autor,
    ).save()
    return comentario


class MotivoEPossivelComentar(enum.StrEnum):
    OK = ""
    BLOQUEIO = "Há relação de bloqueio entre os usuários"
    ONDEVENTO_FECHADO = "O evento está fechado"


def e_possivel_comentar(
    usuario: User, evento: OndEvento
) -> tuple[bool, MotivoEPossivelComentar]:
    if RelacaoModel.relacoes.existe_relacao_entre(usuario, evento.autor, "BLQ"):
        return False, MotivoEPossivelComentar.BLOQUEIO
    elif evento.situacao == "FECHADO":
        return False, MotivoEPossivelComentar.ONDEVENTO_FECHADO

    return True, MotivoEPossivelComentar.OK
