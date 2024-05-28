from django_web_components import component  # type: ignore


@component.register("reacao_resposta_comentario")
class ReacaoRespostaComentarioComponente(component.Component):
    template_name = "componentes/reacao-resposta-comentario.html"
    svg_reacao = {"LIKE": "svg/like-cheio.svg", "UTIL": "svg/util.svg"}

    def render(self, context) -> str:
        context["svg_icon"] = "svg/like-vazio.svg"
        context["usuario_reagiu"] = False
        resposta = context["resposta"]
        if hasattr(resposta, "minha_reacao"):
            if len(resposta.minha_reacao) == 1:
                context["usuario_reagiu"] = True
                context["svg_icon"] = self.svg_reacao[resposta.minha_reacao[0].tipo]
        return super().render(context)
