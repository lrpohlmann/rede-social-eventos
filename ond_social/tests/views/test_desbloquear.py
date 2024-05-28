from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_perfil.models import User
from ond_social.models import RelacaoModel


class PostDesbloquearView(TestCase):
    def setUp(self) -> None:
        usuario1 = baker.make(User)
        usuario2 = baker.make(User)
        baker.make(RelacaoModel, de=usuario1, com=usuario2, status="BLQ")
        self.client.force_login(usuario1)
        self.resposta = self.post("social:desbloquear", id_receptor=usuario2.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)


class PostDesbloquearSemBloqueioView(TestCase):
    def setUp(self) -> None:
        usuario1 = baker.make(User)
        usuario2 = baker.make(User)
        self.client.force_login(usuario1)
        self.resposta = self.post("social:desbloquear", id_receptor=usuario2.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)


class PostDesbloquearMesmoUsuarioView(TestCase):
    def setUp(self) -> None:
        usuario1 = baker.make(User)
        self.client.force_login(usuario1)
        self.resposta = self.post("social:desbloquear", id_receptor=usuario1.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_403(self.resposta)


class PostBloquearUsuarioNaoExisteView(TestCase):
    def setUp(self) -> None:
        usuario1 = baker.make(User)
        self.client.force_login(usuario1)
        self.resposta = self.post("social:desbloquear", id_receptor=99)
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)
