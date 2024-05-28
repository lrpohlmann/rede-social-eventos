from django.db import connection
from django.test import TestCase
from model_bakery import baker

from ond_social.models import RelacaoModel
from ond_perfil.models import User


class ConsultasRelacaoTeste(TestCase):
    def test_consulta_relacao_entre_eu_e_ele(self):
        eu, ele = baker.make(User, 2)
        RelacaoModel(de=eu, com=ele, status="BLQ").save()
        RelacaoModel(de=ele, com=eu, status="BLQ").save()

        resultado = RelacaoModel.relacoes.relacao_entre(eu, ele)

        self.assertEqual(("BLQ", "BLQ"), resultado)

    def test_consulta_relacao_entre_eu_e_ele_unilateral(self):
        eu, ele = baker.make(User, 2)
        RelacaoModel(de=eu, com=ele, status="BLQ").save()

        resultado = RelacaoModel.relacoes.relacao_entre(eu, ele)

        self.assertEqual(("BLQ", None), resultado)

    def test_consulta_relacao_entre_eu_e_ele_vazio(self):
        eu, ele = baker.make(User, 2)
        resultado = RelacaoModel.relacoes.relacao_entre(eu, ele)

        self.assertEqual(None, resultado)
