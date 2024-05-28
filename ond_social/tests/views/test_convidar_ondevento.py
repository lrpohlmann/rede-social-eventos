from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_perfil.models import User
from ond_social.models import RelacaoModel
from utils_teste.recipes import ondevento_recipe, OndEventoFechado


class PostConvidarParaOndEventoView(TestCase):
    def setUp(self) -> None:
        self.convidante = baker.make(User)
        self.client.force_login(self.convidante)
        self.convidado = baker.make(User)
        self.evento = ondevento_recipe.make()
        baker.make(RelacaoModel, de=self.convidado, com=self.convidante, status="SEG")

        self.resposta = self.post(
            "social:convidar_para_ondevento",
            id_ondevento=self.evento.pk,
            id_convidado=self.convidado.pk,
        )
        return super().setUp()

    def test_view_status(self):
        self.response_201(self.resposta)


class PostConvidarParaOndEventoNaoPossivelView(TestCase):
    def setUp(self) -> None:
        self.convidante = baker.make(User)
        self.client.force_login(self.convidante)
        self.convidado = baker.make(User)
        self.evento = OndEventoFechado.make()

        self.resposta = self.post(
            "social:convidar_para_ondevento",
            id_ondevento=self.evento.pk,
            id_convidado=self.convidado.pk,
        )
        return super().setUp()

    def test_view_status(self):
        self.response_403(self.resposta)


class PostConvidarParaOndEventoNaoExistenteView(TestCase):
    def setUp(self) -> None:
        self.convidante = baker.make(User)
        self.client.force_login(self.convidante)
        self.convidado = baker.make(User)

        self.resposta = self.post(
            "social:convidar_para_ondevento",
            id_ondevento=1,
            id_convidado=self.convidado.pk,
        )
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)


class PostConvidarParaOndEventoNaoLogadoView(TestCase):
    def setUp(self) -> None:
        self.convidante = baker.make(User)
        self.convidado = baker.make(User)
        self.evento = OndEventoFechado.make()

        self.resposta = self.post(
            "social:convidar_para_ondevento",
            id_ondevento=self.evento.pk,
            id_convidado=self.convidado.pk,
        )
        return super().setUp()

    def test_view_status(self):
        self.response_302(self.resposta)
