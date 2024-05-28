from .comentar import (
    deletar_comentario,
    e_possivel_comentar,
    MotivoEPossivelComentar,
    comentar,
    AcaoNaoPermitidaException,
)
from .convidar import e_possivel_convidar, enviar_convite, MotivoEPossivelConvidar
from .relacionar import (
    AutorelacionamentoException,
    BloqueadoException,
    nao_permitir_autorelacionamento,
    seguir,
    deseguir,
    bloquear,
    desbloquear,
)

from uuid import uuid4

from django.db.models import Count, Q

from ond_perfil.models import User
from ond_social.dominio.comentar import MotivoEPossivelComentar
from ond_social.models import Comentario, RelacaoModel


def incluir_social(usuario: User | int):
    if isinstance(usuario, User):
        pk = usuario.pk
    else:
        pk = usuario

    return User.objects.annotate(
        contagem_seguindo=Count(
            "relacao_emitida",
            filter=Q(relacao_emitida__status=RelacaoModel.Status.SEGUINDO),
        ),
        contagem_seguidores=Count(
            "relacao_recebida",
            filter=Q(relacao_recebida__status=RelacaoModel.Status.SEGUINDO),
        ),
        contagem_bloqueados=Count(
            "relacao_emitida",
            filter=Q(relacao_emitida__status=RelacaoModel.Status.BLOCK),
        ),
    ).get(pk=pk)


def editar_perfil(perfil: User, dados: dict) -> User:
    if username := dados.get("username"):
        perfil.username = username
    if foto := dados.get("foto_perfil"):
        foto.name = f"{uuid4()}.jpg"
        perfil.foto = foto

    if dados.get("deletar_bio"):
        perfil.bio = None
    elif bio := dados.get("bio"):
        perfil.bio = bio

    if dados.get("deletar_insta"):
        perfil.insta = None
    elif insta := dados.get("insta"):
        perfil.insta = insta

    if dados.get("deletar_x"):
        perfil.x = None
    elif x := dados.get("x"):
        perfil.x = x

    perfil.save()
    return perfil


def e_possivel_responder(
    usuario: User, comentario: Comentario
) -> tuple[bool, MotivoEPossivelComentar]:
    if RelacaoModel.relacoes.existe_relacao_entre(usuario, comentario.do_autor, "BLQ"):
        return False, MotivoEPossivelComentar.BLOQUEIO
    elif comentario.no_evento.situacao == "FECHADO":
        return False, MotivoEPossivelComentar.ONDEVENTO_FECHADO

    return True, MotivoEPossivelComentar.OK
