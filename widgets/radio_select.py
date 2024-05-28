from django.forms import RadioSelect


class RadioSelectOnd(RadioSelect):
    template_name = "componente/input/radio.html"
    option_template_name = "componente/input/input_option.html"
