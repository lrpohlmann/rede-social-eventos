from django.shortcuts import render
from django.http import (
    HttpRequest,
    HttpResponseNotFound,
)
from django.db.models import Count, Exists, Q

from ond_eventos.models import OndEvento
from ond_social.models import ConfirmacaoPresenca


def home_do_ondevento_view(request: HttpRequest, id_ondevento: int):
    try:
        usuario = request.user
        if usuario.is_authenticated:
            ondevento = (
                OndEvento.objects.annotate(
                    Count("confirmados_no_evento"),
                    usuario_presenca_confirmada=Exists(
                        ConfirmacaoPresenca.objects.filter(
                            Q(do_usuario=usuario)
                            & Q(no_evento=OndEvento.objects.get(pk=id_ondevento))
                        )
                    ),
                )
                .prefetch_related("confirmados_no_evento")
                .prefetch_related("confirmados_no_evento__do_usuario")
                .get(pk=id_ondevento)
            )

        else:
            ondevento = OndEvento.objects.annotate(Count("confirmados_no_evento")).get(
                pk=id_ondevento
            )

        return render(
            request,
            "pagina/ondevento-home.html",
            {
                "user": usuario,
                "ondevento": ondevento,
            },
        )
    except OndEvento.DoesNotExist:
        return HttpResponseNotFound("Evento não encontrado")
