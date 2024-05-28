from django_web_components import component  # type: ignore


@component.register("conversa")
class Conversa(component.Component):
    template_name = "componentes/conversa.html"

    def get_context_data(self, **kwargs) -> dict:
        comentario = self.attributes.pop("comentario")
        return {"comentario": comentario}
