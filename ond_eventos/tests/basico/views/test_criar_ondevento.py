from datetime import datetime, timedelta

from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_perfil.models import User
from ond_eventos.models import Cidade
from ond_eventos.forms import ManipularOndEventoForm


class CriarOndEventoTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.resposta = self.get("evento:criar_ondevento")
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)


class PostCriarOndEventoTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)

        data_inicio = datetime.now() + timedelta(1)
        data_fim = datetime.now() + timedelta(1, hours=3)

        cidade = Cidade(uf="RS", nome="PORTO ALEGRE")
        cidade.save()

        with open("staticfiles/img/placeholder.jpg", "rb") as f:
            self.resposta = self.post(
                "evento:criar_ondevento",
                data={
                    "nome": "Rolê noturno na José do Patrocĩnio",
                    "capa": f,
                    "tipo": "BAR",
                    "data_inicio": data_inicio.strftime("%Y-%m-%d"),
                    "hora_inicio": data_inicio.strftime("%H:%M"),
                    "data_fim": data_fim.strftime("%Y-%m-%d"),
                    "hora_fim": data_fim.strftime("%H:%M"),
                    "descricao": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "uf": "RS",
                    "cidade": cidade.pk,
                    "endereco": "Rua Jose do Patrocinio, 123",
                },
            )
        return super().setUp()

    def test_view_status(self):
        self.response_201(self.resposta)

    def test_hx_redirect(self):
        self.get_check_200(self.resposta.headers["hx-redirect"])


class PostFalhaCriarOndEventoTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)

        self.resposta = self.post("evento:criar_ondevento", data={})
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)
