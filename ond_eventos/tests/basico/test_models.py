from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.test import TestCase, tag
from django.db import IntegrityError
from model_bakery import baker

from ond_eventos.models import (
    OndEvento,
)


class DataFimMaiorQueInicioTeste(TestCase):

    def test_falha_validacao(self):
        with self.assertRaises(IntegrityError):
            baker.make(
                OndEvento,
                inicio=datetime.now(ZoneInfo("America/Sao_Paulo")),
                fim=datetime.now(ZoneInfo("America/Sao_Paulo")) - timedelta(hours=1),
            )
