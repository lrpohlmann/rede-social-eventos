from django_web_components import component  # type: ignore


@component.register("botao_convidar")
class BotaoConvidar(component.Component):
    template_name = "componentes/botao-convidar.html"

    def get_context_data(self, **kwargs) -> dict:
        seguidor = self.attributes.pop("seguidor")
        ondevento = self.attributes.pop("ondevento")
        situacao_para_convite = self.attributes.pop("situacao_para_convite")
        return {
            "seguidor": seguidor,
            "ondevento": ondevento,
            "situacao_para_convite": situacao_para_convite,
        }
