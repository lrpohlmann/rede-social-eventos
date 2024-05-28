from django.forms import CharField, Form
from widgets import TextAreaOnd


class ComentarioForm(Form):
    corpo = CharField(
        max_length=120,
        required=True,
        widget=TextAreaOnd(
            attrs={"id": "comentar_evento", "placeholder": "comentar..."}
        ),
    )
