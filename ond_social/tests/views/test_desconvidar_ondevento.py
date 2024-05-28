from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_perfil.models import User
from ond_social.models import RelacaoModel, ConviteOndEvento
from utils_teste.recipes import ondevento_recipe, OndEventoFechado


class PostConvidarParaOndEventoView(TestCase):
    def setUp(self) -> None:
        self.convidante = baker.make(User)
        self.client.force_login(self.convidante)
        self.convidado = baker.make(User)
        self.evento = ondevento_recipe.make()
        baker.make(RelacaoModel, de=self.convidado, com=self.convidante, status="SEG")
        baker.make(
            ConviteOndEvento,
            de=self.convidante,
            para=self.convidado,
            evento=self.evento,
        )

        self.resposta = self.post(
            "social:desconvidar_para_ondevento",
            id_ondevento=self.evento.pk,
            id_convidado=self.convidado.pk,
        )
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)


class PostConvidarParaOndEvento404View(TestCase):
    def setUp(self) -> None:
        self.convidante = baker.make(User)
        self.client.force_login(self.convidante)
        self.convidado = baker.make(User)
        self.evento = ondevento_recipe.make()
        baker.make(RelacaoModel, de=self.convidado, com=self.convidante, status="SEG")

        self.resposta = self.post(
            "social:desconvidar_para_ondevento",
            id_ondevento=self.evento.pk,
            id_convidado=self.convidado.pk,
        )
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)
