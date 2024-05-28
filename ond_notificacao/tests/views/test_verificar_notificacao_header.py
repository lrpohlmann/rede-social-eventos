from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_notificacao.models import AtividadeModel
from ond_perfil.models import User


class VerificarNotificacaoHeaderComNotificacaoNaoVistaViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        baker.make(AtividadeModel, notificar_para=self.usuario)
        self.resposta = self.get("notificacao:verificar_notificacao_header")
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)

    def test_view_template(self):
        self.assertResponseContains('<img src="/static/svg/notif-cheio.svg" alt="" />')


class VerificarNotificacaoHeaderSemNotificacaoNaoVistaViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.resposta = self.get("notificacao:verificar_notificacao_header")
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)

    def test_view_template(self):
        self.assertResponseContains('<img src="/static/svg/notif-vazio.svg" alt="" />')


class VerificarNotificacaoHeaderNaoLogadoViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.resposta = self.get("notificacao:verificar_notificacao_header")
        return super().setUp()

    def test_view_status(self):
        self.response_302(self.resposta)
