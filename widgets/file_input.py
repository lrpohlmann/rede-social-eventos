from django.forms.widgets import FileInput


class FileInputOnd(FileInput):
    template_name = "componente/input/file.html"
