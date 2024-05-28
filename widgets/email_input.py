from django.forms import EmailInput


class EmailInputOnd(EmailInput):
    template_name = "componente/input/email.html"
