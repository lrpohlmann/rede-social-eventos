from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, tag
from model_bakery import baker

from ond_perfil.models import User
from ond_eventos.models import OndEvento
from ond_eventos import dominio as eventos
from ond_social.dominio import (
    AcaoNaoPermitidaException,
    BloqueadoException,
    AutorelacionamentoException,
    MotivoEPossivelComentar,
    desbloquear,
    incluir_social,
    seguir,
    bloquear,
    deseguir,
    editar_perfil,
    comentar,
    e_possivel_comentar,
    enviar_convite,
    e_possivel_convidar,
    deletar_comentario,
)
from ond_social.models import Comentario, ConviteOndEvento, ConfirmacaoPresenca
from ond_social.models.relacao import RelacaoModel
from ond_notificacao.models import AtividadeModel
from utils_teste.recipes import OndEventoFechado, ondevento_recipe, OndEventoOcorrendo


class DominioTeste(TestCase):
    def setUp(self) -> None:
        self.usuario1 = baker.make(User)
        self.usuario2 = baker.make(User)
        return super().setUp()

    def test_seguir(self):
        self.usuario1 = incluir_social(self.usuario1)
        self.usuario2 = incluir_social(self.usuario2)

        self.assertEqual(self.usuario1.contagem_seguindo, 0)
        self.assertEqual(self.usuario2.contagem_seguidores, 0)

        seguir(self.usuario1, self.usuario2)

        usuario3 = baker.make(User)
        bloquear(self.usuario1, usuario3)

        self.usuario1 = incluir_social(self.usuario1)
        self.usuario2 = incluir_social(self.usuario2)

        self.assertEqual(self.usuario1.contagem_seguindo, 1)
        self.assertEqual(self.usuario2.contagem_seguidores, 1)

    def test_seguir_repetido(self):
        seguir(self.usuario1, self.usuario2)
        seguir(self.usuario1, self.usuario2)

        self.usuario1 = incluir_social(self.usuario1)
        self.assertEqual(self.usuario1.contagem_seguindo, 1)

    def test_tentar_seguir_bloqueado(self):
        bloquear(self.usuario2, self.usuario1)
        with self.assertRaises(BloqueadoException):
            seguir(self.usuario1, self.usuario2)

        self.usuario2 = incluir_social(self.usuario2)
        self.assertEqual(self.usuario2.contagem_seguidores, 0)

    def test_bloquear(self):
        bloquear(self.usuario1, self.usuario2)

        self.usuario1 = incluir_social(self.usuario1)

        self.assertEqual(self.usuario1.contagem_bloqueados, 1)

    def test_bloquear_repetido(self):
        bloquear(self.usuario1, self.usuario2)
        bloquear(self.usuario1, self.usuario2)

        self.usuario1 = incluir_social(self.usuario1)

        self.assertEqual(self.usuario1.contagem_bloqueados, 1)

    def test_bloquear_seguindo(self):
        seguir(self.usuario1, self.usuario2)
        bloquear(self.usuario1, self.usuario2)

        self.usuario1 = incluir_social(self.usuario1)

        self.assertEqual(self.usuario1.contagem_seguindo, 0)
        self.assertEqual(self.usuario1.contagem_bloqueados, 1)

    def test_bloquear_elimina_relacao_recebida_de_seguidor(self):
        seguir(self.usuario2, self.usuario1)

        self.usuario1 = incluir_social(self.usuario1)
        self.usuario2 = incluir_social(self.usuario2)

        self.assertEqual(self.usuario1.contagem_seguidores, 1)
        self.assertEqual(self.usuario1.contagem_bloqueados, 0)
        self.assertEqual(self.usuario2.contagem_seguindo, 1)

        bloquear(self.usuario1, self.usuario2)

        self.usuario1 = incluir_social(self.usuario1)
        self.usuario2 = incluir_social(self.usuario2)

        self.assertEqual(self.usuario1.contagem_seguidores, 0)
        self.assertEqual(self.usuario1.contagem_bloqueados, 1)
        self.assertEqual(self.usuario2.contagem_seguindo, 0)

    def test_nao_permitir_autorelacionamento(self):
        with self.assertRaises(AutorelacionamentoException):
            seguir(self.usuario1, self.usuario1)
            bloquear(self.usuario2, self.usuario2)

    def test_desbloquear(self):
        bloquear(self.usuario1, self.usuario2)

        self.usuario1 = incluir_social(self.usuario1)
        self.assertEqual(self.usuario1.contagem_bloqueados, 1)

        desbloquear(self.usuario1, self.usuario2)

        self.usuario1 = incluir_social(self.usuario1)
        self.assertEqual(self.usuario1.contagem_bloqueados, 0)

    def test_deseguir(self):
        seguir(self.usuario1, self.usuario2)

        self.usuario1 = incluir_social(self.usuario1)
        self.usuario2 = incluir_social(self.usuario2)

        self.assertEqual(self.usuario1.contagem_seguindo, 1)
        self.assertEqual(self.usuario2.contagem_seguidores, 1)
        self.assertEqual(self.usuario1.contagem_seguidores, 0)
        self.assertEqual(self.usuario2.contagem_seguindo, 0)

        deseguir(self.usuario1, self.usuario2)

        self.usuario1 = incluir_social(self.usuario1)
        self.usuario2 = incluir_social(self.usuario2)

        self.assertEqual(self.usuario1.contagem_seguindo, 0)
        self.assertEqual(self.usuario2.contagem_seguidores, 0)
        self.assertEqual(self.usuario1.contagem_seguidores, 0)
        self.assertEqual(self.usuario2.contagem_seguindo, 0)

    def test_bloquear_estando_bloqueado(self):
        bloquear(self.usuario1, self.usuario2)

        self.usuario1 = incluir_social(self.usuario1)
        self.usuario2 = incluir_social(self.usuario2)

        self.assertEqual(self.usuario1.contagem_bloqueados, 1)
        self.assertEqual(self.usuario2.contagem_bloqueados, 0)

        bloquear(self.usuario2, self.usuario1)

        self.usuario1 = incluir_social(self.usuario1)
        self.usuario2 = incluir_social(self.usuario2)

        self.assertEqual(self.usuario1.contagem_bloqueados, 1)
        self.assertEqual(self.usuario2.contagem_bloqueados, 1)

    def test_editar_perfil(self):
        # TODO: expandir
        u = editar_perfil(
            self.usuario1, {"username": "Onder1", "bio": "Pai de família"}
        )
        self.assertEqual(u.username, "Onder1")
        self.assertEqual(u.bio, "Pai de família")


class ComentarioTeste(TestCase):
    def setUp(self) -> None:
        self.evento = ondevento_recipe.make()
        self.usuario = baker.make(User)
        self.comentario = comentar(
            self.usuario, self.evento, {"corpo": "Tá bombando??"}
        )
        return super().setUp()

    def test_comentar(self):
        self.assertIsInstance(self.comentario, Comentario)
        self.assertTrue(
            AtividadeModel.objects.filter(
                acao_model=ContentType.objects.get_for_model(self.comentario),
                acao_id=self.comentario.pk,
                deletado=False,
            ).exists()
        )

    def test_deletar_comentario(self):
        comentario_deletado = deletar_comentario(self.usuario, self.comentario)
        self.assertTrue(comentario_deletado.deletado)
        self.assertFalse(
            AtividadeModel.objects.filter(
                acao_model=ContentType.objects.get_for_model(self.comentario),
                acao_id=self.comentario.pk,
                deletado=False,
            ).exists()
        )


class FalhaDeletarComentarioTeste(TestCase):
    def test_outro_usuario_tentar_deletar(self):
        comentario = baker.make(Comentario, do_autor=baker.make(User))
        with self.assertRaises(AcaoNaoPermitidaException):
            deletar_comentario(baker.make(User), comentario)


class PossivelComentarTeste(TestCase):
    def setUp(self) -> None:
        self.evento = ondevento_recipe.make()
        self.usuario = baker.make(User)
        return super().setUp()

    def test_e_possivel_comentar(self):
        self.assertTrue(e_possivel_comentar(self.usuario, self.evento)[0])


class NaoPossivelComentarTeste(TestCase):

    def test_comentar_relacao_bloqueio(self):
        usuario1 = baker.make(User)
        usuario2 = baker.make(User)
        baker.make(
            RelacaoModel, de=usuario2, com=usuario1, status=RelacaoModel.Status.BLOCK
        )
        evento = ondevento_recipe.make(autor=usuario2)
        self.assertEqual(
            e_possivel_comentar(usuario1, evento),
            (False, MotivoEPossivelComentar.BLOQUEIO),
        )

    def test_comentar_evento_fechado(self):
        usuario1 = baker.make(User)
        evento = OndEventoFechado.make()
        self.assertEqual(
            e_possivel_comentar(usuario1, evento),
            (False, MotivoEPossivelComentar.ONDEVENTO_FECHADO),
        )


class ConvidarParaOndEventoTeste(TestCase):
    def setUp(self) -> None:
        self.evento = ondevento_recipe.make()
        self.usuario1 = baker.make(User)
        self.usuario2 = baker.make(User)
        return super().setUp()

    def test_convidar(self):
        convite = enviar_convite(self.usuario1, self.usuario2, self.evento)
        self.assertIsInstance(
            convite,
            ConviteOndEvento,
        )
        self.assertTrue(
            AtividadeModel.objects.filter(
                acao_model=ContentType.objects.get_for_model(convite),
                acao_id=convite.pk,
            ).exists()
        )


class EPossivelConvidarParaOndEventoTeste(TestCase):
    def setUp(self) -> None:
        self.evento = ondevento_recipe.make()
        self.usuario1 = baker.make(User)
        self.usuario2 = baker.make(User)
        baker.make(RelacaoModel, de=self.usuario2, com=self.usuario1, status="SEG")
        return super().setUp()

    def test_e_possivel(self):
        self.assertEqual(
            e_possivel_convidar(self.usuario1, self.usuario2, self.evento), (True, "")
        )


class EPossivelConvidarParaOndEventoNaoSeguidorTeste(TestCase):
    def setUp(self) -> None:
        self.evento = ondevento_recipe.make()
        self.usuario1 = baker.make(User)
        self.usuario2 = baker.make(User)
        return super().setUp()

    def test_e_possivel(self):
        self.assertEqual(
            e_possivel_convidar(self.usuario1, self.usuario2, self.evento),
            (False, "Não é possível convidar não seguidores"),
        )


class EPossivelConvidarParaOndEventoFechadoTeste(TestCase):
    def setUp(self) -> None:
        self.evento = OndEventoFechado.make()
        self.usuario1 = baker.make(User)
        self.usuario2 = baker.make(User)
        baker.make(RelacaoModel, de=self.usuario2, com=self.usuario1, status="SEG")
        return super().setUp()

    def test_e_possivel(self):
        self.assertEqual(
            e_possivel_convidar(self.usuario1, self.usuario2, self.evento),
            (False, "O evento está fechado"),
        )


class ConsultaSeguidoresPossíveisDeConvidarTeste(TestCase):
    def setUp(self) -> None:
        self.evento = ondevento_recipe.make()
        self.usuario1 = baker.make(User)
        self.usuario2 = baker.make(User)
        self.usuario3 = baker.make(User)
        self.usuario4 = baker.make(User)
        self.usuario_sem_relacao = baker.make(User)
        baker.make(RelacaoModel, de=self.usuario2, com=self.usuario1, status="SEG")
        baker.make(RelacaoModel, de=self.usuario3, com=self.usuario1, status="SEG")
        baker.make(RelacaoModel, de=self.usuario4, com=self.usuario1, status="SEG")
        baker.make(ConfirmacaoPresenca, do_usuario=self.usuario2, no_evento=self.evento)
        baker.make(
            ConviteOndEvento, de=self.usuario1, para=self.usuario3, evento=self.evento
        )
        return super().setUp()

    def test_relacao_seguidores_com_situacao_para_convite(self):
        consulta = User.usuarios.seguidores_com_situacao_para_convite(
            self.usuario1.pk, self.evento.pk
        )
        presente = [s for s in consulta if s.situacao_para_convite == "PRESENTE"]
        convidado = [s for s in consulta if s.situacao_para_convite == "CONVIDADO"]
        aberto = [s for s in consulta if s.situacao_para_convite == "ABERTO"]
        self.assertEqual(presente, [self.usuario2])
        self.assertEqual(convidado, [self.usuario3])
        self.assertEqual(aberto, [self.usuario4])
