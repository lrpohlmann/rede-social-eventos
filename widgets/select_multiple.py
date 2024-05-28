from django.forms import SelectMultiple


class SelectMultipleOnd(SelectMultiple):
    template_name = "componente/input/select.html"
    option_template_name = "componente/input/select_option.html"
