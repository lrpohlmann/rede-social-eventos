from django_web_components import component  # type: ignore


@component.register("resposta_comentario_colorido")
class RespostaComentarioColorido(component.Component):
    template_name = "componentes/resposta-comentario-colorido.html"

    def get_context_data(self, **kwargs) -> dict:
        resposta = self.attributes.pop("resposta")
        return {"resposta": resposta}
