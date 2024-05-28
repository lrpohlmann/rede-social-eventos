from datetime import datetime
from zoneinfo import ZoneInfo

from django.utils.datastructures import MultiValueDict
from django.test import TestCase, tag
from model_bakery import baker
from parameterized import parameterized  # type: ignore

from utils_teste.recipes import (
    ondevento_recipe,
    OndEventoOcorrendo,
)
from utils_teste.datas import datetime_horas_a_mais, datetime_horas_a_menos
from ond_eventos import dominio as eventos
from ond_eventos.models import OndEvento, Cidade


class OndConsultaOndEHjTeste(TestCase):
    @parameterized.expand(
        [
            [
                {
                    "tipo_evento": ["SHOW"],
                    "ordenacao": "inicio",
                    "data_inicio": datetime.now().date(),
                },
                2,
            ],
            [
                {
                    "tipo_evento": ["SHOW", "CULT"],
                    "ordenacao": "inicio",
                    "data_inicio": datetime.now().date(),
                },
                4,
            ],
            [
                {
                    "tipo_evento": [],
                    "ordenacao": "inicio",
                    "data_inicio": datetime.now().date(),
                },
                4,
            ],
        ]
    )
    def test_resultado_consulta(self, parametros_consulta, qtd_eventos):
        cidade = baker.make(Cidade)

        baker.make(OndEvento, 2, tipo="SHOW", cidade=cidade)
        baker.make(OndEvento, 2, tipo="CULT", cidade=cidade)

        ondhj = eventos.ond_hj({**parametros_consulta, "cidade": cidade.pk})
        self.assertTrue(ondhj.form.is_valid())

        eventos_encontrados = ondhj.ondeventos

        self.assertEqual(len(eventos_encontrados), qtd_eventos)
        if parametros_consulta["tipo_evento"]:
            for evento in eventos_encontrados:
                self.assertIn(evento.tipo, parametros_consulta["tipo_evento"])


class OndHjTeste(TestCase):
    def setUp(self) -> None:
        cidade = baker.make(Cidade)
        ondevento_recipe.make(5, cidade=cidade)
        self.cidade_pk = str(cidade.pk)
        return super().setUp()

    def test_receber_dict(self):
        reposta_ond_hj = eventos.ond_hj(
            {
                "tipo_evento": [],
                "ordenacao": "inicio",
                "data_inicio": datetime.now().date(),
                "cidade": self.cidade_pk,
            }
        )
        self.assertTrue(reposta_ond_hj.form.is_valid())
        self.assertGreater(len(reposta_ond_hj.ondeventos), 0)

    def test_receber_querydict(self):
        resposta_ond_hj = eventos.ond_hj(
            MultiValueDict(
                {
                    "tipo_evento": [],
                    "ordenacao": ["inicio"],
                    "data_inicio": [datetime.now().date()],
                    "cidade": [self.cidade_pk],
                }
            )
        )
        self.assertTrue(resposta_ond_hj.form.is_valid())
        self.assertTrue(len(resposta_ond_hj.ondeventos), 0)


class EditarOndEvento(TestCase):
    def setUp(self) -> None:
        self.cidade = baker.make(Cidade)
        return super().setUp()

    def test_editar(self):
        ondevento = OndEvento.eventos.get(pk=OndEventoOcorrendo.make().pk)

        datetime_inicio = datetime.now(tz=ZoneInfo(self.cidade.fuso))
        datetime_fim = datetime_horas_a_mais(2, tz=self.cidade.fuso)
        dados = {
            "nome": "Churrasquinho 2",
            "tipo": ondevento.Tipo.FESTA,
            "data_inicio": datetime_inicio.date(),
            "hora_inicio": datetime_inicio.time(),
            "data_fim": datetime_fim.date(),
            "hora_fim": datetime_fim.time(),
            "descricao": "xxxxxxxxxxxxxxxxx",
            "cidade": self.cidade,
            "endereco": "Rua A, 333",
        }
        ondevento_editado = eventos.editar_ondevento(ondevento, dados)
        self.assertEqual(ondevento_editado.nome, dados["nome"])
        self.assertEqual(ondevento_editado.tipo, dados["tipo"])
        self.assertEqual(
            ondevento_editado.inicio,
            datetime.combine(
                datetime_inicio.date(),
                datetime_inicio.time(),
                ZoneInfo(self.cidade.fuso),
            ),
        )
        self.assertEqual(
            ondevento_editado.fim,
            datetime.combine(
                datetime_fim.date(), datetime_fim.time(), ZoneInfo(self.cidade.fuso)
            ),
        )
        self.assertEqual(ondevento_editado.descricao, dados["descricao"])
        self.assertEqual(ondevento_editado.cidade, dados["cidade"])
        self.assertEqual(ondevento_editado.endereco, dados["endereco"])

    def test_nao_editavel(self):
        datetime_inicio = datetime_horas_a_menos(36, self.cidade.fuso)
        datetime_fim = datetime_horas_a_menos(33, self.cidade.fuso)
        ondevento = OndEventoOcorrendo.make(inicio=datetime_inicio, fim=datetime_fim)
        self.assertFalse(eventos.ondevento_e_editavel(ondevento))
