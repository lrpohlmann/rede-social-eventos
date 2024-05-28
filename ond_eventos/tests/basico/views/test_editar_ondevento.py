from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_perfil.models import User
from ond_eventos.models import Cidade
from utils_teste.recipes import OndEventoFechado, ondevento_recipe


class GetEditarOndEventoTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        ondevento = ondevento_recipe.make(autor=usuario)

        self.resposta = self.get("evento:editar_ondevento", id_ondevento=ondevento.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)


class GetEditarOndEventoOutroAutorTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        ondevento = ondevento_recipe.make()

        self.resposta = self.get("evento:editar_ondevento", id_ondevento=ondevento.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_403(self.resposta)


class GetEditarOndEventoNaoEditavelTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        ondevento = OndEventoFechado.make(autor=usuario)

        self.resposta = self.get("evento:editar_ondevento", id_ondevento=ondevento.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_403(self.resposta)


class GetEditarOndEventoNaoExistenteTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        ondevento = OndEventoFechado.make(autor=usuario)
        pk, _ = ondevento.delete()

        self.resposta = self.get("evento:editar_ondevento", id_ondevento=pk)
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)


class GetEditarOndEventoNaoLogadoTeste(TestCase):
    def setUp(self) -> None:
        ondevento = OndEventoFechado.make()
        self.resposta = self.get("evento:editar_ondevento", id_ondevento=ondevento.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_302(self.resposta)


class PostEditarOndEventoTeste(TestCase):
    def setUp(self) -> None:
        self.cidade = baker.make(Cidade)
        usuario = baker.make(User)
        self.client.force_login(usuario)
        ondevento = ondevento_recipe.make(autor=usuario)

        self.resposta = self.post(
            "evento:editar_ondevento",
            id_ondevento=ondevento.pk,
            data={
                "nome": "Churrasquinho 2",
                "tipo": ondevento.Tipo.FESTA,
                "data_inicio": ondevento.inicio.date(),
                "hora_inicio": ondevento.inicio.time(),
                "data_fim": ondevento.fim.date(),
                "hora_fim": ondevento.fim.time(),
                "descricao": "xxxxxxxxxxxxxxxxx",
                "cidade": self.cidade.pk,
                "endereco": "Rua A, 333",
            },
        )
        return super().setUp()

    def test_view_status(self):
        self.response_302(self.resposta)


class PostEditarOndEventoFalhaTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        ondevento = ondevento_recipe.make(autor=usuario)

        self.resposta = self.post(
            "evento:editar_ondevento", id_ondevento=ondevento.pk, data={}
        )
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)
        self.assertTrue(self.get_context("form_editar_evento").errors)
