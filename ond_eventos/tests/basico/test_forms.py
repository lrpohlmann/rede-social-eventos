from datetime import datetime, timedelta, time

from django.test import TestCase, tag
from model_bakery import baker
from parameterized import parameterized  # type: ignore

from ond_eventos.forms import ManipularOndEventoForm, OndEHojeForm
from ond_eventos.models import Cidade


class CriarOndEventoFormTeste(TestCase):
    def setUp(self) -> None:
        self.cidade = baker.make(Cidade, uf="RS")
        data_inicio = datetime.now() + timedelta(1)
        data_fim = datetime.now() + timedelta(1, hours=3)
        self.dados = {
            "nome": "Rolê noturno na José do Patrocĩnio",
            "tipo": "BAR",
            "data_inicio": data_inicio.strftime("%Y-%m-%d"),
            "hora_inicio": data_inicio.strftime("%H:%M"),
            "data_fim": data_fim.strftime("%Y-%m-%d"),
            "hora_fim": data_fim.strftime("%H:%M"),
            "descricao": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "cidade": self.cidade.pk,
            "uf": self.cidade.uf,
            "endereco": "Rua X, 555",
        }
        return super().setUp()

    def test_input_campos(self):
        form = ManipularOndEventoForm(self.dados)

        self.assertTrue(form.is_valid())

    def test_dados_validados(self):
        data_inicio = datetime.now() + timedelta(1)
        data_fim = datetime.now() + timedelta(1, hours=3)
        form = ManipularOndEventoForm(self.dados)

        form.is_valid()
        self.assertEqual(
            form.cleaned_data,
            {
                "nome": "Rolê noturno na José do Patrocĩnio",
                "capa": None,
                "tipo": "BAR",
                "data_inicio": data_inicio.date(),
                "hora_inicio": time(data_inicio.hour, data_inicio.minute),
                "data_fim": data_fim.date(),
                "hora_fim": time(data_fim.hour, data_fim.minute),
                "descricao": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "cidade": self.cidade,
                "pesquisa_cidade": "",
                "endereco": "Rua X, 555",
            },
        )


class CriarOndEventoFormFalhaTeste(TestCase):
    def setUp(self) -> None:
        self.cidade = baker.make(Cidade, uf="RS")
        data_inicio = datetime.now() - timedelta(1, hours=3)
        data_fim = datetime.now() - timedelta(1)
        self.dados = {
            "nome": "Rolê noturno na José do Patrocĩnio",
            "tipo": "BAR",
            "data_inicio": data_inicio.strftime("%Y-%m-%d"),
            "hora_inicio": data_inicio.strftime("%H:%M"),
            "data_fim": data_fim.strftime("%Y-%m-%d"),
            "hora_fim": data_fim.strftime("%H:%M"),
            "cidade": self.cidade.pk,
            "uf": self.cidade.uf,
            "endereco": "Rua X, 123",
        }
        return super().setUp()

    def test_nao_valida(self):
        self.assertFalse(ManipularOndEventoForm(self.dados).is_valid())

    def test_erros(self):
        form = ManipularOndEventoForm(self.dados)
        form.is_valid()
        self.assertDictEqual(
            form.errors,
            {
                "data_inicio": ["Data escolhida já passou"],
                "data_fim": ["Data escolhida já passou"],
                "descricao": ["Este campo é obrigatório."],
            },
        )


class OndEHojeFormTeste(TestCase):
    @parameterized.expand(
        [
            [
                {
                    "tipo_evento": ["FEST"],
                    "ordenacao": "inicio",
                    "data_inicio": datetime.now().date(),
                }
            ],
            [
                {
                    "tipo_evento": [],
                    "ordenacao": "inicio",
                    "data_inicio": datetime.now().date(),
                }
            ],
            [
                {
                    "tipo_evento": [],
                    "ordenacao": "inicio",
                    "data_inicio": datetime.now().date(),
                }
            ],
        ]
    )
    def test_form(self, dados_form):
        cidade = baker.make(Cidade)
        form = OndEHojeForm(data={**dados_form, "cidade": cidade.pk})
        self.assertTrue(form.is_valid())
