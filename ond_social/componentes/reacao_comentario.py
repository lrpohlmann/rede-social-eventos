from django_web_components import component  # type: ignore


@component.register("reacao_comentario")
class ReacaoComentario(component.Component):
    template_name = "componentes/reacao-comentario.html"
    svg_reacao = {"LIKE": "svg/like-cheio.svg", "UTIL": "svg/util.svg"}

    def render(self, context) -> str:
        context["svg_icon"] = "svg/like-vazio.svg"
        context["usuario_reagiu"] = False
        comentario = context["comentario"]
        if hasattr(comentario, "minha_reacao"):
            if len(comentario.minha_reacao) == 1:
                context["usuario_reagiu"] = True
                context["svg_icon"] = self.svg_reacao[comentario.minha_reacao[0].tipo]
        return super().render(context)
