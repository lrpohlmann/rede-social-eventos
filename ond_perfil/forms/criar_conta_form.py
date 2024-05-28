from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _

from widgets import TextInputOnd, PasswordInputOnd, EmailInputOnd
from ond_perfil.models import User


class CriarContaForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInputOnd(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=PasswordInputOnd(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {"username": TextInputOnd, "email": EmailInputOnd}
