from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_perfil.models import User
from ond_social.models import Comentario


class DeletarComentarioViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.comentario = baker.make(Comentario, do_autor=self.usuario)
        self.resposta = self.post(
            "social:deletar_comentario", id_comentario=self.comentario.pk
        )
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)

    def test_view_headers(self):
        self.assertResponseHeaders({"HX-Trigger": "comentarioDeletado"})


class DeletarComentarioNaoExistenteViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.resposta = self.post("social:deletar_comentario", id_comentario=1)
        return super().setUp()

    def test_view_status(self):
        self.assert_http_404_not_found()


class DeletarComentarioProibidoViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.comentario = baker.make(Comentario, do_autor=baker.make(User))
        self.resposta = self.post(
            "social:deletar_comentario", id_comentario=self.comentario.pk
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_403_forbidden()
