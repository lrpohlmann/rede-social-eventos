from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_social.models import RespostaComentario, ReacaoRespostaComentarioModel
from ond_perfil.models import User
from ond_social.models.relacao import RelacaoModel


class ReagirRespostaComentarioViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.resposta_comentario = baker.make(RespostaComentario)
        self.resposta = self.post(
            "social:reagir_resposta_comentario",
            id_resposta=self.resposta_comentario.pk,
            data={"reacao": "LIKE"},
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_201_created()

    def test_view_effects(self):
        self.assertTrue(
            ReacaoRespostaComentarioModel.objects.filter(
                usuario=self.usuario, resposta=self.resposta_comentario
            ).exists()
        )

    def test_view_html(self):
        self.assertContains(self.resposta, "Remover", status_code=201, count=1)
        self.assertInHTML(
            '<img class="w-6 h-6" src="/static/svg/like-cheio.svg" alt="" data-elemento="reacao-resposta">',
            self.resposta.content.decode(),
        )


class ReagirRespostaComentarioNaoExistenteViewTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        self.resposta = self.post(
            "social:reagir_resposta_comentario",
            id_resposta=1,
            data={"reacao": "LIKE"},
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_404_not_found()


class ReagirRespostaComentarioDeletarViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.resposta_comentario = baker.make(RespostaComentario)
        self.reacao = baker.make(
            ReacaoRespostaComentarioModel,
            usuario=self.usuario,
            tipo="LIKE",
            resposta=self.resposta_comentario,
        )
        self.resposta = self.delete(
            "social:reagir_resposta_comentario",
            id_resposta=self.resposta_comentario.pk,
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_200_ok()

    def test_view_effects(self):
        self.assertFalse(
            ReacaoRespostaComentarioModel.objects.filter(
                usuario=self.usuario, resposta=self.resposta_comentario
            ).exists()
        )

    def test_view_html(self):
        self.assertNotContains(self.resposta, "Remover", status_code=200)
        self.assertInHTML(
            '<img class="w-6 h-6" src="/static/svg/like-vazio.svg" alt="" data-elemento="reacao-resposta">',
            self.resposta.content.decode(),
        )


class ReagirRespostaComentarioDeletarNaoExistenteViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.resposta_comentario = baker.make(RespostaComentario)
        self.resposta = self.delete(
            "social:reagir_resposta_comentario",
            id_resposta=self.resposta_comentario.pk,
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_404_not_found()


class ReagirRespostaComentarioRelacaoDeBloqueioViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.resposta_comentario = baker.make(RespostaComentario)
        self.relacao = baker.make(
            RelacaoModel,
            de=self.resposta_comentario.do_autor,
            com=self.usuario,
            status=RelacaoModel.Status.BLOCK,
        )
        self.resposta = self.post(
            "social:reagir_resposta_comentario",
            id_resposta=self.resposta_comentario.pk,
            data={"reacao": "LIKE"},
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_403_forbidden()


class ReagirRespostaComentarioRecaoNaoValidaViewTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        self.resposta_comentario = baker.make(RespostaComentario)
        self.resposta = self.post(
            "social:reagir_resposta_comentario",
            id_resposta=self.resposta_comentario.pk,
            data={"reacao": "AAAAAA"},
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_400_bad_request()
