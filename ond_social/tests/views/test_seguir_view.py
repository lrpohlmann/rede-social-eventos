from random import randint

from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_perfil.models import User
from ond_social import dominio as social
from ond_social.models import RelacaoModel


class SeguirViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario1 = baker.make(User)
        self.client.force_login(self.usuario1)
        self.usuario2 = baker.make(User)

        self.resposta = self.post("social:seguir", id_receptor=self.usuario2.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_201(self.resposta)


class SeguirViewBloqueadoTeste(TestCase):
    def setUp(self) -> None:
        self.usuario1 = baker.make(User)
        self.client.force_login(self.usuario1)
        self.usuario2 = baker.make(User)

        social.bloquear(self.usuario2, self.usuario1)

        self.resposta = self.post("social:seguir", id_receptor=self.usuario2.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_403(self.resposta)

    def test_view_content(self):
        self.assertEqual(
            self.resposta.content,
            "Não é possível seguir. Um dos usuários bloqueou ou está bloqueado".encode(),
        )


class SeguirViewUsuarioNaoExisteView(TestCase):
    def setUp(self) -> None:
        self.usuario1 = baker.make(User)
        self.client.force_login(self.usuario1)
        id_nao_existente = randint(1, 10000)
        while id_nao_existente == self.usuario1.pk:
            id_nao_existente = randint(1, 10000)

        self.resposta = self.post("social:seguir", id_receptor=id_nao_existente)
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)

    def test_view_content(self):
        self.assertEqual(
            self.resposta.content,
            "Não é possível seguir: usuário inexistente.".encode(),
        )


class SeguirViewSemLoginTeste(TestCase):

    def test_view_status(self):
        self.assertLoginRequired("social:seguir", id_receptor=1)
