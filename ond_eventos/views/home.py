from django.shortcuts import redirect


def home_view(request):
    return redirect("pergunta:ond-e-hj")
