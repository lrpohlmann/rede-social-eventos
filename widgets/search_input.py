from django.forms import TextInput


class SearchInputOnd(TextInput):
    input_type = "search"
    template_name = "componente/input/search.html"
