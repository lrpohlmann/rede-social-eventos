from random import randint


from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_perfil.models import User
from ond_social import dominio as social


class DeseguirViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario1 = baker.make(User)
        self.client.force_login(self.usuario1)
        self.usuario2 = baker.make(User)
        social.seguir(self.usuario1, self.usuario2)
        self.resposta = self.post("social:desseguir", id_receptor=self.usuario2.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)


class DeseguirViewSemRelacaoTeste(TestCase):
    def setUp(self) -> None:
        self.usuario1 = baker.make(User)
        self.client.force_login(self.usuario1)
        self.usuario2 = baker.make(User)

        self.resposta = self.post("social:desseguir", id_receptor=self.usuario2.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)

    def test_view_content(self):
        self.assertEqual(
            self.resposta.content,
            "Não é possível desseguir. Não há relação de seguidor.".encode(),
        )


class DeseguirViewUsuarioNaoExisteTeste(TestCase):
    def setUp(self) -> None:
        self.usuario1 = baker.make(User)
        self.client.force_login(self.usuario1)
        id_nao_existente = randint(2, 1000)
        while id_nao_existente == self.usuario1.pk:
            id_nao_existente = randint(2, 1000)

        self.resposta = self.post("social:desseguir", id_receptor=id_nao_existente)
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)

    def test_view_content(self):
        self.assertEqual(
            self.resposta.content,
            "Não é possível desseguir: usuário inexistente.".encode(),
        )


class SeguirViewSemLoginTeste(TestCase):

    def test_view_status(self):
        self.assertLoginRequired("social:desseguir", id_receptor=1)
