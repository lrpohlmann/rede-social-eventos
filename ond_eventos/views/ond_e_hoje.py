from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator

from ond_eventos.forms import OndEHojeForm
from ond_eventos import dominio as eventos


def onde_e_hoje_view(request: HttpRequest):
    if not request.GET:
        return render(
            request,
            "pagina/ond-e-hj.html",
            {
                "form_ond_e_hoje": OndEHojeForm(
                    auto_id=True,
                    initial={"data_inicio": datetime.now().strftime("%Y-%m-%d")},
                ),
                "eventos_encontrados": [],
            },
        )

    params = request.GET
    pagina = params.get("pagina", 1)
    resposta_ond_hj = eventos.ond_hj(params)
    paginador = Paginator(resposta_ond_hj.ondeventos, 10)

    response = render(
        request,
        "pagina/ond-e-hj.html",
        {
            "form_ond_e_hoje": resposta_ond_hj.form,
            "eventos_encontrados": paginador.get_page(pagina),
        },
    )
    if not resposta_ond_hj.form.errors:
        response.headers["HX-Trigger"] = "consultaOndHjEnviada"

    return response
