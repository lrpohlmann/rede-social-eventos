from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_notificacao.models import AtividadeModel
from ond_perfil.models import User


class MarcarNotificacaoComoVistoViewTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        self.notificacao = baker.make(AtividadeModel, notificar_para=usuario)
        self.resposta = self.put(
            "notificacao:marcar_como_visto", id_notificacao=self.notificacao.pk
        )
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)

    def test_view_headers(self):
        self.assertResponseHeaders({"HX-Trigger": "notificacaoVista"}, self.resposta)

    def test_view_effects(self):
        self.assertTrue(AtividadeModel.objects.get(pk=self.notificacao.pk).visto)


class MarcarNotificacaoComoVisto404ViewTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        self.resposta = self.put("notificacao:marcar_como_visto", id_notificacao=44)
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)


class MarcarNotificacaoComoVistoNaoLogadoViewTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        notificacao = baker.make(AtividadeModel, notificar_para=usuario)
        self.resposta = self.put(
            "notificacao:marcar_como_visto", id_notificacao=notificacao.pk
        )
        return super().setUp()

    def test_view_status(self):
        self.response_302(self.resposta)
