from django.forms import (
    Form,
    ImageField,
    CharField,
    ValidationError,
    BooleanField,
    CheckboxInput,
)

from ond_perfil.models import User
from widgets import TextAreaOnd, TextInputOnd, FileInputOnd


def username_unico(username: str):
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username já existe")


class EditarPerfilForm(Form):
    foto_perfil = ImageField(
        label="Foto de perfil",
        max_length=100,
        allow_empty_file=False,
        required=False,
        widget=FileInputOnd({"accept": "image/jpeg"}),
    )
    username = CharField(
        max_length=User.TAMANHO_USERNAME,
        required=False,
        validators=[username_unico],
        strip=True,
        widget=TextInputOnd({"disabled": True, "autocomplete": "off"}),
    )
    bio = CharField(
        max_length=User.TAMANHO_BIO,
        required=False,
        strip=True,
        widget=TextAreaOnd({"placeholder": "Bio...", "autocomplete": "off"}),
    )
    deletar_bio = BooleanField(
        label="Deletar Bio",
        required=False,
        widget=CheckboxInput(
            {
                "_": "on change if my value == 'on' tell previous <textarea/> put '' into your value"
            }
        ),
    )
    insta = CharField(
        label="Instagram",
        max_length=User.TAMANHO_INSTA,
        required=False,
        strip=True,
        widget=TextInputOnd({"placeholder": "onderdasilva...", "autocomplete": "off"}),
    )
    deletar_insta = BooleanField(
        label="Deletar Insta",
        required=False,
        widget=CheckboxInput(
            {
                "_": "on change if my value == 'on' tell previous <input/> put '' into your value"
            }
        ),
    )
    x = CharField(
        label="X",
        max_length=User.TAMANHO_X,
        required=False,
        strip=True,
        widget=TextInputOnd({"placeholder": "onderdasilva...", "autocomplete": "off"}),
    )
    deletar_x = BooleanField(
        label="Deletar X",
        required=False,
        widget=CheckboxInput(
            {
                "_": "on change if my value == 'on' tell previous <input/> put '' into your value"
            }
        ),
    )
