from django_web_components import component  # type: ignore


@component.register("pilula_status")
class PilulaStatusEvento(component.Component):
    template_name = "componentes/pilula-status-evento.html"
    cor_status = {
        "ABERTO": "bg-blue-500",
        "OCORRENDO": "bg-red-500",
        "AFTER": "bg-violet-500",
        "FECHADO": "bg-gray-500",
    }

    def get_context_data(self, **kwargs) -> dict:
        status = self.attributes.pop("status")
        cor = self.cor_status.get(status, "bg-black")
        return {"status": status, "cor": cor}
