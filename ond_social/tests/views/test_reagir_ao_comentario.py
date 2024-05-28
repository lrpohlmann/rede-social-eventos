from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_social.models import Comentario
from ond_perfil.models import User
from ond_social.models.reacao_comentario import ReacaoComentarioModel
from ond_social.models.relacao import RelacaoModel


class ReagirAoComentarioViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.comentario = baker.make(Comentario)
        self.resposta = self.post(
            "social:reagir_ao_comentario",
            id_comentario=self.comentario.pk,
            data={"reacao": "LIKE"},
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_201_created()

    def test_view_effects(self):
        self.assertTrue(
            ReacaoComentarioModel.objects.filter(
                usuario=self.usuario, comentario=self.comentario
            ).exists()
        )

    def test_view_html(self):
        self.assertContains(self.resposta, "Remover", status_code=201, count=1)
        self.assertInHTML(
            '<img class="w-6 h-6" src="/static/svg/like-cheio.svg" alt="" data-elemento="reacao-comentario">',
            self.resposta.content.decode(),
        )


class ReagirAoComentarioNaoExistenteViewTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        self.resposta = self.post(
            "social:reagir_ao_comentario",
            id_comentario=1,
            data={"reacao": "LIKE"},
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_404_not_found()


class ReagirAoComentarioDeletarViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.comentario = baker.make(Comentario)
        self.reacao = baker.make(
            ReacaoComentarioModel,
            usuario=self.usuario,
            tipo="LIKE",
            comentario=self.comentario,
        )
        self.resposta = self.delete(
            "social:reagir_ao_comentario",
            id_comentario=self.comentario.pk,
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_200_ok()

    def test_view_effects(self):
        self.assertFalse(
            ReacaoComentarioModel.objects.filter(
                usuario=self.usuario, comentario=self.comentario
            ).exists()
        )

    def test_view_html(self):
        self.assertNotContains(self.resposta, "Remover", status_code=200)
        self.assertInHTML(
            '<img class="w-6 h-6" src="/static/svg/like-vazio.svg" alt="" data-elemento="reacao-comentario">',
            self.resposta.content.decode(),
        )


class ReagirAoComentarioDeletarNaoExistenteViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.comentario = baker.make(Comentario)
        self.resposta = self.delete(
            "social:reagir_ao_comentario",
            id_comentario=self.comentario.pk,
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_404_not_found()


class ReagirAoComentarioRelacaoDeBloqueioViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.comentario = baker.make(Comentario)
        self.relacao = baker.make(
            RelacaoModel,
            de=self.comentario.do_autor,
            com=self.usuario,
            status=RelacaoModel.Status.BLOCK,
        )
        self.resposta = self.post(
            "social:reagir_ao_comentario",
            id_comentario=self.comentario.pk,
            data={"reacao": "LIKE"},
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_403_forbidden()


class ReagirAoComentarioRecaoNaoValidaViewTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        self.comentario = baker.make(Comentario)
        self.resposta = self.post(
            "social:reagir_ao_comentario",
            id_comentario=self.comentario.pk,
            data={"reacao": "AAAAAA"},
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_400_bad_request()
