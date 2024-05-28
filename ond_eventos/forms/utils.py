from datetime import date, datetime
from typing import Literal, TypeGuard
from django.forms import (
    ChoiceField,
    DateField,
    ModelChoiceField,
    ValidationError,
)


CAMPOS_OND_E_HOJE_FORM = Literal["tipo_evento", "ordenacao"]


def type_guard_e_model_choice(campo: object) -> TypeGuard[ModelChoiceField]:
    return isinstance(campo, ModelChoiceField)


def type_guard_e_choice(campo: object) -> TypeGuard[ChoiceField]:
    return isinstance(campo, ChoiceField)


def type_guard_e_date_field(campo: object) -> TypeGuard[DateField]:
    return isinstance(campo, DateField)


def validador_data_igual_ou_posterior_a_hoje(data: date) -> None:
    if data < datetime.now().date():
        raise ValidationError("Data escolhida já passou")
