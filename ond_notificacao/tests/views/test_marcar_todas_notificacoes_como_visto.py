from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_notificacao.models import AtividadeModel
from ond_perfil.models import User


class MarcarTodasNotificacaoComoVistoViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        baker.make(
            AtividadeModel, notificar_para=self.usuario, visto=False, _quantity=10
        )
        self.resposta = self.put("notificacao:marcar_todas_como_visto")
        return super().setUp()

    def test_view_status(self):
        self.response_204(self.resposta)

    def test_view_headers(self):
        self.assertResponseHeaders(
            {"HX-Trigger": "todasNotificacoesVistas"}, self.resposta
        )

    def test_view_effects(self):
        self.assertFalse(
            AtividadeModel.objects.filter(
                notificar_para=self.usuario, visto=False
            ).exists()
        )


class MarcarNotificacaoComoVistoNaoLogadoViewTeste(TestCase):
    def setUp(self) -> None:
        self.resposta = self.put("notificacao:marcar_todas_como_visto")
        return super().setUp()

    def test_view_status(self):
        self.response_302(self.resposta)
