from django.forms import PasswordInput


class PasswordInputOnd(PasswordInput):
    template_name = "componente/input/password_input.html"
