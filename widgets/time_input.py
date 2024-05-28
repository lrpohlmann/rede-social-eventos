from django.forms import TimeInput


class TimeInputOnd(TimeInput):
    input_type = "time"
    template_name = "componente/input/time.html"
