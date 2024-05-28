from datetime import date, datetime, time
from typing import TypedDict

from django.urls import reverse_lazy
from django.core.validators import FileExtensionValidator
from django.forms import (
    CharField,
    ChoiceField,
    DateField,
    Form,
    ImageField,
    ModelChoiceField,
    TimeField,
)

from ond_eventos.forms.utils import (
    validador_data_igual_ou_posterior_a_hoje,
)
from ond_eventos.models import TP_OND_EVENTO, OndEvento, Cidade
from widgets.time_input import (
    TimeInputOnd,
)
from widgets import (
    DateInputOnd,
    SearchInputOnd,
    SelectOnd,
    TextAreaOnd,
    TextInputOnd,
    FileInputOnd,
)


class DadosCriarOndEventoForm(TypedDict):
    nome: str
    tipo: TP_OND_EVENTO
    data_inicio: date
    hora_inicio: time
    data_fim: date
    hora_fim: time
    cidade: int
    local: str


class ManipularOndEventoForm(Form):
    ID_CAMPO_CIDADE = "cidade"
    ID_ENDERECO = "id_endereco"

    nome = CharField(
        required=True,
        max_length=OndEvento.NOME_MAX_LENGTH,
        widget=TextInputOnd({"placeholder": "Feira..."}),
    )
    capa = ImageField(
        required=False,
        allow_empty_file=False,
        max_length=100,
        validators=[
            FileExtensionValidator(["jpeg", "jpg"]),
        ],
        widget=FileInputOnd({"accept": "image/jpeg"}),
    )
    tipo = ChoiceField(choices=OndEvento.Tipo.choices, required=True, widget=SelectOnd)
    data_inicio = DateField(
        required=True,
        label="Dia de ínicio",
        initial=datetime.now().strftime("%Y-%m-%d"),
        validators=[validador_data_igual_ou_posterior_a_hoje],
        widget=DateInputOnd({"min": datetime.now().strftime("%Y-%m-%d")}),
    )
    hora_inicio = TimeField(required=True, label="Hora de início", widget=TimeInputOnd)
    data_fim = DateField(
        required=True,
        label="Dia fim",
        validators=[validador_data_igual_ou_posterior_a_hoje],
        widget=DateInputOnd({"min": datetime.now().strftime("%Y-%m-%d")}),
    )
    hora_fim = TimeField(required=True, label="Hora fim", widget=TimeInputOnd)
    descricao = CharField(
        label="Descrição",
        max_length=120,
        strip=True,
        required=True,
        widget=TextAreaOnd(
            {"placeholder": "Fala pessoal, prontos para uma nova edição..."}
        ),
    )
    pesquisa_cidade = CharField(
        label="Pesquisar",
        max_length=100,
        required=False,
        widget=SearchInputOnd(
            attrs={
                "placeholder": "Xique-Xique...",
                "hx-get": reverse_lazy("evento:select_cidade"),
                "hx-target": "#" + ID_CAMPO_CIDADE,
                "hx-swap": "innerHTML",
                "hx-trigger": "keyup changed delay:500ms",
            }
        ),
    )
    cidade = ModelChoiceField(
        label="Escolher",
        required=True,
        queryset=None,
        empty_label=None,
        widget=SelectOnd(
            {
                "id": ID_CAMPO_CIDADE,
                "_": f"init if my value == '' put localStorage.id_cidade into me end on htmx:afterSwap if my value != '' set localStorage.id_cidade to my innerHTML",
            }
        ),
    )
    endereco = CharField(
        label="Local/Endereço",
        required=False,
        max_length=200,
        widget=TextInputOnd(
            {
                "placeholder": "Rua X...",
                "id": ID_ENDERECO,
            }
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        campo_cidade = self.fields["cidade"]
        if isinstance(campo_cidade, ModelChoiceField):
            if id_cidade := self.data.get("cidade"):
                campo_cidade.queryset = Cidade.objects.filter(pk=id_cidade)
            else:
                campo_cidade.queryset = Cidade.objects.none()
