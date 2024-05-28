from django_web_components import component  # type: ignore


@component.register("opcoes_comentario")
class OpcoesComentario(component.Component):
    template_name = "componentes/opcoes-comentario.html"

    def get_context_data(self, **kwargs) -> dict:
        deletar = self.attributes.pop("deletar")
        return {"deletar": deletar}
