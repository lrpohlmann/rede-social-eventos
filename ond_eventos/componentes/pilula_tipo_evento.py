from django_web_components import component  # type: ignore

from ond_eventos.models import Tipo


@component.register("pilula_tipo_evento")
class PilulaTipoEvento(component.Component):
    template_name = "componentes/pilula-tipo-evento.html"
    cor_tipo = {
        "Festa": "bg-yellow-300",
        "Bar": "bg-teal-300",
        "Rolê de Rua": "bg-red-300",
        "Bloquinho": "bg-cyan-300",
        "Show": "bg-sky-300",
        "Aniversário": "bg-orange-300",
        "Formatura": "bg-indigo-300",
        "Casamento": "bg-violet-300",
        "Evento Cultural": "bg-fuchsia-300",
        "Feira": "bg-pink-300",
        "Outro": "bg-rose-300",
    }

    def get_context_data(self, **kwargs) -> dict:
        tipo = self.attributes.pop("tipo")
        return {"tipo": tipo, "cor": self.cor_tipo[tipo]}
