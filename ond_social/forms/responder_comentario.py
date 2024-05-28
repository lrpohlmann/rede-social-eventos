from django.forms import ModelForm

from ond_social.models import RespostaComentario
from widgets import TextAreaOnd


class RespostaComentarioForm(ModelForm):
    class Meta:
        model = RespostaComentario
        fields = ["corpo"]
        widgets = {
            "corpo": TextAreaOnd(
                attrs={
                    "placeholder": "Responder...",
                    "_": "on respostaCriada from body set my value to ''",
                }
            )
        }
