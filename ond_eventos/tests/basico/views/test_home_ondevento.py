from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_perfil.models import User
from ond_eventos.forms import ComentarioForm
from ond_eventos.models import OndEvento
from ond_social.models import Comentario


class HomeOndEventoView(TestCase):
    def setUp(self) -> None:
        self.evento = baker.make(OndEvento)
        self.evento.save()

        self.usuario = baker.make(User)
        self.usuario.save()

        self.client.force_login(self.usuario)

        self.resposta = self.get("evento:ondevento_home", id_ondevento=self.evento.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)
