from django.db.models import Q

from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_perfil.models import User
from ond_eventos.models import OndEvento
from ond_social.models.confirmacao_presenca import ConfirmacaoPresenca


class ConfirmarPresencaNoEventoView(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.usuario.save()

        self.evento = baker.make(OndEvento)
        self.evento.save()

        self.client.force_login(self.usuario)

        self.resposta = self.post(
            "social:confirmar_presenca", id_ondevento=self.evento.pk
        )
        return super().setUp()

    def test_view_status(self):
        self.response_201(self.resposta)

    def test_view_evento_de_confirmacao_enviado(self):
        self.assertResponseHeaders({"hx-trigger": "ondPresencaUsuarioConfirmada"})

    def test_view_salvou_confirmacao(self):
        confirmacao = ConfirmacaoPresenca.objects.get(
            Q(do_usuario=self.usuario) & Q(no_evento=self.evento)
        )
        self.assertIsInstance(confirmacao, ConfirmacaoPresenca)

    def test_view_confirmar_mais_de_uma_vez(self):
        resposta = self.post("social:confirmar_presenca", id_ondevento=self.evento.pk)
        self.response_400(resposta)
        self.assertEqual(resposta.content.decode(), "Já foi confirmado presença.")


class ConfirmarPresencaEmEventoInexistenteTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.usuario.save()
        self.client.force_login(self.usuario)
        return super().setUp()

    def test_view_confirmar_em_evento_inexistente(self):
        resposta = self.post("social:confirmar_presenca", id_ondevento=1)
        self.response_404(resposta)


class ConfirmarPresencaNoEventoViewSemLogin(TestCase):
    def setUp(self) -> None:
        self.evento = baker.make(OndEvento)
        self.evento.save()

        self.resposta = self.post(
            "social:confirmar_presenca", id_ondevento=self.evento.pk
        )
        return super().setUp()

    def test_view_sem_login(self):
        self.response_302(self.resposta)

    def test_view_login_required(self):
        self.assertLoginRequired(
            "social:confirmar_presenca", id_ondevento=self.evento.pk
        )
