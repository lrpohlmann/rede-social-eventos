from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def datetime_horas_a_menos(horas: int, tz=None):
    return datetime.now(tz=ZoneInfo(tz)) - timedelta(hours=horas)


def datetime_horas_a_mais(horas: int, tz=None):
    return datetime.now(tz=ZoneInfo(tz)) + timedelta(hours=horas)
