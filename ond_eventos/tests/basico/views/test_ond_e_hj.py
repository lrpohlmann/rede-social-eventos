from datetime import datetime


from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_eventos.forms import OndEHojeForm
from ond_eventos.models import Cidade, OndEvento
from utils_teste.recipes import ondevento_recipe


class OndeEHojeViewTeste(TestCase):
    def setUp(self):
        self.url = "pergunta:ond-e-hj"
        self.resposta = self.get(self.url)
        return super().setUp()

    def test_status_view(self):
        self.response_200(self.resposta)

    def test_contexto(self):
        self.assertIsInstance(self.get_context("form_ond_e_hoje"), OndEHojeForm)


class GetOndeEHojeComParametrosViewTeste(TestCase):
    def setUp(self):
        cidade = baker.make(Cidade)
        ondevento_recipe.make(cidade=cidade, _quantity=10)

        self.url = "pergunta:ond-e-hj"
        self.resposta = self.get(
            self.url,
            data={
                "data_inicio": datetime.now().strftime("%Y-%m-%d"),
                "ordenacao": "inicio",
                "cidade": cidade.pk,
            },
        )
        return super().setUp()

    def test_status_view(self):
        self.response_200(self.resposta)

    def test_contexto(self):
        self.assertIsInstance(self.get_context("form_ond_e_hoje"), OndEHojeForm)
        self.assertTrue(self.get_context("eventos_encontrados"))
