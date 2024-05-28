from model_bakery import baker
from test_plus import TestCase  # type: ignore

from ond_perfil.models import User
from ond_social.models import (
    Comentario,
    RespostaComentario,
    ReacaoComentarioModel,
    ReacaoRespostaComentarioModel,
)


class GetVerConversaViewTeste(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        comentario = baker.make(Comentario)
        baker.make(
            ReacaoComentarioModel,
            comentario=comentario,
            usuario=usuario,
            tipo=ReacaoComentarioModel.Reacoes.LIKE,
        )
        respostas = baker.make(RespostaComentario, para=comentario, _quantity=3)
        baker.make(
            ReacaoRespostaComentarioModel,
            resposta=respostas[0],
            usuario=usuario,
            tipo=ReacaoRespostaComentarioModel.Reacoes.LIKE,
        )
        baker.make(
            ReacaoRespostaComentarioModel,
            resposta=respostas[1],
            usuario=usuario,
            tipo=ReacaoRespostaComentarioModel.Reacoes.LIKE,
        )
        self.resposta = self.get("social:ver_conversa", id_comentario=comentario.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)

    def test_view_html(self):
        self.assertInHTML(
            '<img class="w-6 h-6" src=/static/svg/like-cheio.svg alt="" data-elemento="reacao-comentario">',
            self.resposta.content.decode(),
            1,
        )
        self.assertInHTML(
            '<img class="w-6 h-6" src=/static/svg/like-cheio.svg alt="" data-elemento="reacao-resposta">',
            self.resposta.content.decode(),
            2,
        )


class GetVerConversaComentarioDeletado(TestCase):
    def setUp(self) -> None:
        self.client.force_login(baker.make(User))
        comentario = baker.make(Comentario, deletado=True)
        self.resposta = self.get("social:ver_conversa", id_comentario=comentario.pk)
        return super().setUp()

    def test_view_status(self):
        self.assert_http_404_not_found()


class GetVerConversaViewFalhaTeste(TestCase):
    def setUp(self) -> None:
        self.client.force_login(baker.make(User))
        self.resposta = self.get("social:ver_conversa", id_comentario=1)
        return super().setUp()

    def test_view_status(self):
        self.response_404(self.resposta)


class GetVerConversaViewNaoLogadoTeste(TestCase):
    def setUp(self) -> None:
        comentario = baker.make(Comentario)
        self.resposta = self.get("social:ver_conversa", id_comentario=comentario.pk)
        return super().setUp()

    def test_view_status(self):
        self.response_302(self.resposta)
