from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_perfil.models import User
from ond_eventos.models import OndEvento
from ond_social.models.confirmacao_presenca import ConfirmacaoPresenca  # type: ignore


class DesconfirmarPresencaNoEventoView(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.usuario.save()

        self.evento = baker.make(OndEvento)
        self.evento.save()

        self.confirmacao = baker.make(
            ConfirmacaoPresenca, no_evento=self.evento, do_usuario=self.usuario
        )
        self.confirmacao.save()

        self.client.force_login(self.usuario)

        self.resposta = self.post(
            "social:desconfirmar_presenca", id_ondevento=self.evento.pk
        )
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)

    def test_view_sem_login(self):
        self.client.logout()
        self.assertLoginRequired(
            "social:desconfirmar_presenca", id_ondevento=self.evento.pk
        )

    def test_view_confirmacao_presenca_inexistente(self):
        novo_evento = baker.make("OndEvento")
        novo_evento.save()

        resposta = self.post(
            "social:desconfirmar_presenca", id_ondevento=novo_evento.pk
        )
        self.response_404(resposta)
        self.assertEqual(
            resposta.content.decode(),
            "Não há confirmação de presença. Impossível desconfirmar.",
        )

    def test_view_evento_de_desconfirmacao_enviado(self):
        self.assertResponseHeaders({"hx-trigger": "ondPresencaUsuarioDesconfirmada"})


class DesconfirmarPresencaEmEventoInexistente(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.usuario.save()
        self.client.force_login(self.usuario)
        return super().setUp()

    def test_view_desconfirmar_em_evento_inexistente(self):
        resposta = self.post("social:desconfirmar_presenca", id_ondevento=1)
        self.response_404(resposta)
        self.assertEqual(
            resposta.content.decode(),
            "Evento não encontrado",
        )
