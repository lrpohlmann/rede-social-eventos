from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_perfil.models import User


class PostBloquearView(TestCase):
    def setUp(self) -> None:
        usuario1 = baker.make(User)
        usuario2 = baker.make(User)
        self.client.force_login(usuario1)
        self.resposta = self.post("social:bloquear", id_receptor=usuario2.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_201(self.resposta)


class PostBloquearMesmoUsuarioView(TestCase):
    def setUp(self) -> None:
        usuario1 = baker.make(User)
        self.client.force_login(usuario1)
        self.resposta = self.post("social:bloquear", id_receptor=usuario1.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_403(self.resposta)


class PostBloquearUsuarioNaoExisteView(TestCase):
    def setUp(self) -> None:
        usuario1 = baker.make(User)
        self.client.force_login(usuario1)
        self.resposta = self.post("social:bloquear", id_receptor=99)
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)
