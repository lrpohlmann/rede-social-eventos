from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_social.models import Comentario
from ond_perfil.models import User


class OpcoesComentarioViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.comentario = baker.make(Comentario, do_autor=self.usuario)
        self.resposta = self.get(
            "social:opcoes_comentario", id_comentario=self.comentario.pk
        )
        return super().setUp()

    def test_view_status(self):
        self.assert_http_200_ok()

    def test_view_html(self):
        self.assertResponseContains("Deletar")
