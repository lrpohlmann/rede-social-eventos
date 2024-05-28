import enum

from ond_eventos.models import OndEvento
from ond_notificacao.models import AtividadeModel
from ond_perfil.models import User
from ond_social.models import ConviteOndEvento, RelacaoModel


def enviar_convite(de: User, para: User, evento: OndEvento) -> ConviteOndEvento:
    convite = ConviteOndEvento(de=de, para=para, evento=evento)
    convite.save()
    AtividadeModel(
        ator=convite.de,
        acao_nome=AtividadeModel.TipoAtividade.CONVIDOU,
        acao_objeto=convite,
        alvo_objeto=convite.para,
        notificar_para=convite.para,
    ).save()
    return convite


class MotivoEPossivelConvidar(enum.StrEnum):
    OK = ""
    NAO_E_SEGUIDOR = "Não é possível convidar não seguidores"
    ONDEVENTO_FECHADO = "O evento está fechado"


def e_possivel_convidar(de: User, para: User, evento: OndEvento):
    if not RelacaoModel.relacoes.existe_relacao_entre(de, para, "SEG"):
        return False, MotivoEPossivelConvidar.NAO_E_SEGUIDOR
    elif evento.situacao == "FECHADO":
        return False, MotivoEPossivelConvidar.ONDEVENTO_FECHADO

    return True, MotivoEPossivelConvidar.OK
