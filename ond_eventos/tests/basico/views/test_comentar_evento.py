from parameterized import parameterized  # type: ignore

from model_bakery import baker
from test_plus.test import TestCase  # type: ignore

from ond_perfil.models import User
from ond_eventos.models import OndEvento
from ond_social.models import Comentario
from utils_teste.recipes import OndEventoFechado, ondevento_recipe


class ComentarEventoViewTeste(TestCase):
    def setUp(self) -> None:
        evento = ondevento_recipe.make()

        self.usuario = baker.make(User)
        self.usuario.save()
        self.client.force_login(self.usuario)

        self.resposta = self.post(
            "social:comentar_evento",
            id_ondevento=evento.pk,
            data={"corpo": "Como está o rolê??"},
        )
        return super().setUp()

    def test_view_status(self):
        self.response_201(self.resposta)


class ComentarEventoFalhaViewTeste(TestCase):
    def setUp(self) -> None:
        self.evento = baker.make(OndEvento)
        self.evento.save()

        self.usuario = baker.make(User)
        self.usuario.save()
        self.client.force_login(self.usuario)

        return super().setUp()

    @parameterized.expand([[""], ["a" * 121]])
    def test_view_comentario_invalido(self, corpo):
        resposta = self.post(
            "social:comentar_evento", id_ondevento=self.evento.pk, data={"corpo": corpo}
        )
        self.response_400(resposta, 400)

    def test_view_evento_nao_existe(self):
        pk, evento = self.evento.delete()

        resposta = self.post(
            "social:comentar_evento", id_ondevento=pk, data={"corpo": "AAAAAAAAAa"}
        )

        self.assertEqual(
            resposta.content.decode(), "Evento foi deletado ou não existe."
        )


class ComentarEventoFechadoTeste(TestCase):
    def setUp(self) -> None:
        self.evento = OndEventoFechado.make()
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)

        self.resposta = self.post(
            "social:comentar_evento",
            id_ondevento=self.evento.pk,
            data={"corpo": "O que tem de bebida?"},
        )
        return super().setUp()

    def test_view_status(self):
        self.response_403(self.resposta)


class ComentarNoEventoSemLoginTeste(TestCase):
    def setUp(self) -> None:
        self.evento = baker.make(OndEvento)
        self.evento.save()

        self.resposta = self.post(
            "social:comentar_evento",
            id_ondevento=self.evento.pk,
            data={"corpo": "O que tem de bebida?"},
        )

        return super().setUp()

    def test_view_sem_login(self):
        self.response_302(self.resposta)

    def test_view_login(self):
        self.assertLoginRequired("social:comentar_evento", id_ondevento=self.evento.pk)
