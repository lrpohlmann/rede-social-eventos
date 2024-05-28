from django.urls import path

from . import views


app_name = "pergunta"

urlpatterns = [
    path("", views.onde_e_hoje_view, name="ond-e-hj"),
]
