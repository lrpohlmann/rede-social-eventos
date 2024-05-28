from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_notificacao.models import AtividadeModel
from ond_perfil.models import User


class MinhasNotificacoesViewTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        baker.make(AtividadeModel, notificar_para=usuario, _quantity=5)
        self.resposta = self.get("notificacao:minhas_notificacoes")
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)


class MinhasNotificacoesNaoLogadoViewTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        baker.make(AtividadeModel, notificar_para=usuario, _quantity=5)
        self.resposta = self.get("notificacao:minhas_notificacoes")
        return super().setUp()

    def test_view_status(self):
        self.response_302(self.resposta)
