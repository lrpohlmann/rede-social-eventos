from django_web_components import component  # type: ignore


@component.register("paginador")
class Paginador(component.Component):
    template_name = "componente/paginador2.html"

    def get_context_data(self, **kwargs) -> dict:
        url_get = self.attributes.pop("url_get", "")
        pagina = self.attributes.pop("pagina")
        return {"pagina": pagina, "url_get": url_get}
