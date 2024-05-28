from django_web_components import component  # type: ignore


@component.register("dialog_opcoes_social")
class DialogOpcoesSocial(component.Component):
    template_name = "componentes/dialog-opcoes-social.html"

    def get_context_data(self, **kwargs) -> dict:
        relacao = self.attributes.pop("relacao")
        usuario = self.attributes.pop("usuario")
        return {"relacao": relacao, "usuario": usuario}
