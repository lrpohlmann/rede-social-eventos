from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_perfil.models import User
from ond_eventos.models import Cidade


class GetOptionCidade(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)

        self.cidade_sp = baker.make(Cidade, 2, uf="SP")
        self.cidade_rs = baker.make(Cidade, 2, uf="RS")

        self.resposta = self.get(
            "evento:select_cidade", data={"pesquisa_cidade": "PORTO"}
        )
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)
