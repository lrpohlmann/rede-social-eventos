from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_perfil.models import User
from ond_social.models import RelacaoModel
from utils_teste.recipes import ondevento_recipe, OndEventoFechado


class GetListaSeguidoresParaConvidarViewTeste(TestCase):
    def setUp(self) -> None:
        self.usuario = baker.make(User)
        self.client.force_login(self.usuario)
        self.evento = ondevento_recipe.make()
        self.resposta = self.get(
            "social:lista_seguidores_para_convidar", id_ondevento=self.evento.pk
        )
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)
