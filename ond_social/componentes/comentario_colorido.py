from django_web_components import component  # type: ignore


@component.register("comentario_colorido")
class ComentarioColorido(component.Component):
    template_name = "componentes/comentario-colorido.html"

    def get_context_data(self, **kwargs) -> dict:
        comentario = self.attributes.pop("comentario")
        return {"comentario": comentario}
