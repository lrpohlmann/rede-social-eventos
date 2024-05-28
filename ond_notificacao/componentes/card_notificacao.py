from django.urls import reverse_lazy
from django_web_components import component  # type: ignore


@component.register("card_notificacao")
class CardNotificacao(component.Component):
    template_name = "componentes/card-notificacao.html"

    def get_context_data(self, **kwargs) -> dict:
        notificacao = self.attributes.pop("notificacao")
        match notificacao.acao_nome:
            case "COMENTOU":
                url_acao = reverse_lazy(
                    "social:ver_conversa", kwargs={"id_comentario": notificacao.acao_id}
                )
            case "SEGUIU":
                url_acao = reverse_lazy(
                    "perfil:perfil", kwargs={"id_usuario": notificacao.ator.pk}
                )
            case "CONVIDOU":
                url_acao = reverse_lazy(
                    "perfil:meus_convites",
                )
            case _:
                url_acao = "#"

        return {"notificacao": notificacao, "url_acao": url_acao}
