from django.forms import CharField, EmailField, Form

from widgets import TextInputOnd, PasswordInputOnd


class LoginForm(Form):
    email = EmailField(label="E-mail", required=True, widget=TextInputOnd)
    senha = CharField(
        label="Senha", max_length=128, required=True, widget=PasswordInputOnd
    )
