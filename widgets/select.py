from django.forms import Select


class SelectOnd(Select):
    template_name = "componente/input/select.html"
    option_template_name = "componente/input/select_option.html"
