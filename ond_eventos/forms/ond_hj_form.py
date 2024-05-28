from django.forms import (
    ChoiceField,
    DateField,
    Form,
    MultipleChoiceField,
    CharField,
)
from django.urls import reverse_lazy

from ond_eventos.forms.utils import (
    type_guard_e_choice,
    validador_data_igual_ou_posterior_a_hoje,
)
from ond_eventos.models import OndEvento, Cidade
from widgets import (
    DateInputOnd,
    SelectMultipleOnd,
    RadioSelectOnd,
    SearchInputOnd,
    SelectOnd,
)


class OndEHojeForm(Form):
    ID_CAMPO_CIDADE = "id_cidade"

    nome = CharField(
        max_length=50,
        required=False,
        widget=SearchInputOnd(
            {
                "placeholder": "festa open bar...",
            }
        ),
    )
    tipo_evento = MultipleChoiceField(
        label="Tipo de Evento",
        choices=OndEvento.Tipo.choices,
        required=False,
        widget=SelectMultipleOnd,
    )
    pesquisa_cidade = CharField(
        label="Pesquisar",
        max_length=100,
        required=False,
        widget=SearchInputOnd(
            attrs={
                "placeholder": "novo hamburgo...",
                "hx-get": reverse_lazy("evento:select_cidade"),
                "hx-target": "#" + ID_CAMPO_CIDADE,
                "hx-swap": "innerHTML",
                "hx-trigger": "keyup changed delay:500ms",
            }
        ),
    )
    cidade = ChoiceField(
        label="Escolher",
        choices=[],
        required=True,
        widget=SelectOnd(
            {
                "id": ID_CAMPO_CIDADE,
                "_": f"init if my value == '' put localStorage.id_cidade into me end on htmx:afterSwap if my value != '' set localStorage.id_cidade to my innerHTML",
            }
        ),
    )
    data_inicio = DateField(
        label="Início a partir de",
        required=True,
        validators=[validador_data_igual_ou_posterior_a_hoje],
        widget=DateInputOnd,
    )
    ordenacao = ChoiceField(
        choices=[
            ("inicio", "Data"),
            ("confirmados", "Confirmados"),
            ("comentarios", "Comentários"),
        ],
        label="Ordenar por",
        initial="inicio",
        widget=RadioSelectOnd,
    )

    def __init__(self, *args, opcoes_cidade=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        cidade_field = self.fields["cidade"]
        if type_guard_e_choice(cidade_field):
            if not opcoes_cidade:
                if pk_cidade := self.data.get("cidade"):
                    cidade_field.choices = [
                        (c.pk, c.nome) for c in Cidade.objects.filter(pk=pk_cidade)
                    ]
                    return

                cidade_field.choices = []
                return

            cidade_field.choices = [(c.pk, c.nome) for c in opcoes_cidade]
