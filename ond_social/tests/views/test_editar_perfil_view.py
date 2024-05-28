from django.conf import settings
from django.core.files.images import ImageFile
from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_perfil.models import User


class GetEditarPerfilTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)

        self.resposta = self.get("perfil:editar_perfil")
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)


class PostEditarPerfilTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User, username="nome1")
        self.client.force_login(self.usuario)
        with open(
            str(settings.BASE_DIR / "utils_teste" / "media" / "imagem-teste.jpg"), "rb"
        ) as f:
            self.resposta = self.post(
                "perfil:editar_perfil",
                data={"username": "nome2", "foto_perfil": f},
            )
        return super().setUp()

    def test_view_status(self):
        self.response_302(self.resposta)


class PostEditarPerfilFalhaTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User, username="nome1")
        self.client.force_login(self.usuario)

        baker.make(User, username="nome2")
        self.resposta = self.post("perfil:editar_perfil", data={"username": "nome2"})
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)
