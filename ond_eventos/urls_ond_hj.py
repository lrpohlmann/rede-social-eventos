from django.urls import path

from . import views


urlpatterns = [
    path("", views.onde_e_hoje_view, name="ond-e-hj"),
]
