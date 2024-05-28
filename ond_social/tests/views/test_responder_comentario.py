from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_perfil.models import User
from ond_social.models import Comentario, RelacaoModel
from utils_teste.recipes import OndEventoOcorrendo


class PostResponderComentarioViewTeste(TestCase):
    def setUp(self) -> None:
        self.evento = OndEventoOcorrendo.make()
        self.comentario = baker.make(Comentario, no_evento=self.evento)

        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)

        self.resposta = self.post(
            "social:responder_comentario",
            id_comentario=self.comentario.pk,
            data={"corpo": "xxxxxxxxxxxxxxxxxxxxxxx"},
        )
        return super().setUp()

    def test_view_status(self):
        self.response_201(self.resposta)


class PostResponderComentarioNaoValidoViewTeste(TestCase):
    def setUp(self) -> None:
        self.evento = OndEventoOcorrendo.make()
        self.comentario = baker.make(Comentario, no_evento=self.evento)

        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)

        self.resposta = self.post(
            "social:responder_comentario",
            id_comentario=self.comentario.pk,
            data={"corpo": "x" * 121},
        )
        return super().setUp()

    def test_view_status(self):
        self.response_400(self.resposta)


class PostResponderComentarioNaoPossivelViewTeste(TestCase):
    def setUp(self) -> None:
        self.evento = OndEventoOcorrendo.make()

        self.usuario1 = baker.make(User)
        self.client.force_login(self.usuario1)
        self.usuario2 = baker.make(User)

        self.comentario = baker.make(
            Comentario, do_autor=self.usuario2, no_evento=self.evento
        )

        baker.make(RelacaoModel, de=self.usuario2, com=self.usuario1, status="BLQ")

        self.resposta = self.post(
            "social:responder_comentario",
            id_comentario=self.comentario.pk,
            data={"corpo": "xxxxxxxxxxxxx"},
        )
        return super().setUp()

    def test_view_status(self):
        self.response_403(self.resposta)
