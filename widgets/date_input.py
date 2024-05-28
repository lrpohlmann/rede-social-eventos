from django.forms import DateInput


class DateInputOnd(DateInput):
    input_type = "date"
    template_name = "componente/input/date.html"
