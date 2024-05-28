from django_web_components import component  # type: ignore


@component.register("botao_presenca")
class BotaoPresenca(component.Component):
    template_name = "componentes/botao-presenca.html"

    def get_context_data(self, **kwargs) -> dict:
        return {
            "usuario_presenca_confirmada": self.attributes.pop(
                "usuario_presenca_confirmada"
            ),
            "ondevento": self.attributes.pop("ondevento"),
        }
