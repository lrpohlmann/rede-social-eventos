from django_web_components import component  # type: ignore


@component.register("icon_notificacao")
class IconNotificacao(component.Component):
    template_name = "componentes/icon-notificacao.html"
