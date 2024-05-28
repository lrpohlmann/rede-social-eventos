from django_web_components import component  # type: ignore


@component.register("card_ondevento")
class CardOndEvento(component.Component):
    template_name = "componentes/card-ondevento.html"

    def get_context_data(self, **kwargs) -> dict:
        ondevento = self.attributes.pop("evento")
        return {"evento": ondevento}
