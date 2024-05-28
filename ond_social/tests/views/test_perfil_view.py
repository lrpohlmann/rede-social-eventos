from random import randint


from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_perfil.models import User


class PerfilViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario1 = baker.make(User)
        self.client.force_login(self.usuario1)

        self.usuario_do_perfil = baker.make(User)
        self.resposta = self.get("perfil:perfil", id_usuario=self.usuario_do_perfil.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)


class PerfilViewUsuarioNaoExisteTeste(TestCase):
    def setUp(self) -> None:
        self.usuario1 = baker.make(User)
        self.client.force_login(self.usuario1)
        id_nao_existente = randint(1, 10000)
        while id_nao_existente == self.usuario1.pk:
            id_nao_existente = randint(1, 10000)

        self.resposta = self.get("perfil:perfil", id_usuario=id_nao_existente)
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)
