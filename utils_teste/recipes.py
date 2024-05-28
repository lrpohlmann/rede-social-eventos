from datetime import timedelta, datetime
from zoneinfo import ZoneInfo

from model_bakery.recipe import Recipe

from ond_eventos.models import OndEvento


def factory_recipe_data_igual_ou_maior_que_hoje(horas_a_mais=0):
    def _() -> datetime:
        data = datetime.now(ZoneInfo("America/Sao_Paulo"))
        if horas_a_mais:
            data = data + timedelta(hours=horas_a_mais)

        return data

    return _


def factory_recipe_data_igual_ou_menor_que_hoje(horas_a_menos=0):
    def _() -> datetime:
        data = datetime.now(ZoneInfo("America/Sao_Paulo"))
        if horas_a_menos:
            data = data - timedelta(hours=horas_a_menos)

        return data

    return _


ondevento_recipe = Recipe(
    OndEvento,
    inicio=factory_recipe_data_igual_ou_maior_que_hoje(1),
    fim=factory_recipe_data_igual_ou_maior_que_hoje(3),
)

ondevento_acabado_recipe = Recipe(
    OndEvento,
    inicio=factory_recipe_data_igual_ou_menor_que_hoje(3),
    fim=factory_recipe_data_igual_ou_menor_que_hoje(1),
)

OndEventoFechado = Recipe(
    OndEvento,
    inicio=factory_recipe_data_igual_ou_menor_que_hoje(30),
    fim=factory_recipe_data_igual_ou_menor_que_hoje(25),
)


OndEventoOcorrendo = Recipe(
    OndEvento,
    inicio=factory_recipe_data_igual_ou_menor_que_hoje(horas_a_menos=3),
    fim=factory_recipe_data_igual_ou_maior_que_hoje(3),
)

OndEventoAfter = Recipe(
    OndEvento,
    inicio=factory_recipe_data_igual_ou_menor_que_hoje(10),
    fim=factory_recipe_data_igual_ou_menor_que_hoje(2),
)
