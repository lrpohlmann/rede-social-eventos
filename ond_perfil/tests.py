from test_plus import TestCase  # type: ignore
from model_bakery import baker

from ond_perfil.models import User
from ond_social.models import ConfirmacaoPresenca, ConviteOndEvento


class GetLoginView(TestCase):
    def setUp(self) -> None:
        self.resposta = self.get("conta:login")
        return super().setUp()

    def test_view(self):
        self.assert_http_200_ok()


class GetLoginLogadoView(TestCase):
    def setUp(self) -> None:
        user = baker.make(User)
        self.client.force_login(user)
        self.resposta = self.get("conta:login")
        return super().setUp()

    def test_view(self):
        self.assert_http_302_found()
        self.assertEqual(self.resposta.url, "/ond-e-hj/")


class PostLoginView(TestCase):
    def setUp(self) -> None:
        password = "18@bscasd0"
        email = "ond-user-12@mail.com"
        User.objects.create_user(password=password, email=email, username="ond-user-12")
        self.resposta = self.post(
            "conta:login", data={"email": email, "senha": password}
        )
        return super().setUp()

    def test_view(self):
        self.assertNotContains(self.resposta, "Criar Conta", 302)
        self.assertEqual(self.resposta.url, "/ond-e-hj/")


class PostLoginFailView(TestCase):
    def setUp(self) -> None:
        self.resposta = self.post("conta:login")
        return super().setUp()

    def test_view(self):
        form = self.get_context("login_form")
        self.assertTrue(form.errors)
        self.assertContains(self.resposta, "Criar Conta", status_code=200)


class GetCriarContaView(TestCase):
    def setUp(self) -> None:
        self.resposta = self.get("conta:criar")
        return super().setUp()

    def test_view(self):
        self.assert_http_200_ok()


class GetCriarContaLogadoView(TestCase):
    def setUp(self) -> None:
        user = baker.make(User)
        self.client.force_login(user)
        self.resposta = self.get("conta:criar")
        return super().setUp()

    def test_view(self):
        self.assert_http_302_found()
        self.assertEqual(self.resposta.url, "/ond-e-hj/")


class PostCriarContaView(TestCase):
    def setUp(self) -> None:
        self.data = {
            "email": "ond-user-12@mail.com",
            "username": "ond-user-12",
            "password1": "asvino210tsa",
            "password2": "asvino210tsa",
        }
        self.resposta = self.post("conta:criar", data=self.data)
        return super().setUp()

    def test_view(self):
        self.assert_http_201_created()
        self.assertTrue(User.objects.filter(email=self.data["email"]).exists())


class LogoutView(TestCase):
    def setUp(self) -> None:
        user = baker.make(User)
        self.client.force_login(user)
        self.resposta = self.post("conta:logout")
        return super().setUp()

    def test_view(self):
        self.assertFalse(self.client.session.keys())
        self.assert_http_200_ok()
        self.assertTrue(self.resposta.headers.get("hx-redirect"))


class LogoutNaoLogadoView(TestCase):
    def setUp(self) -> None:
        self.resposta = self.post("conta:logout")
        return super().setUp()

    def test_view(self):
        self.assert_http_302_found()
        self.assertFalse(self.resposta.headers.get("hx-redirect"))


class GetMenuPrincipalPerfilView(TestCase):
    def setUp(self) -> None:
        self.client.force_login(baker.make(User))
        self.resposta = self.get("perfil:menu_principal_perfil")
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)


class GetMeusEventosView(TestCase):
    def setUp(self) -> None:
        self.client.force_login(baker.make(User))
        self.resposta = self.get("perfil:meus_eventos")
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)


class GetMinhasConfirmacoesView(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        self.resposta = self.get("perfil:minhas_confirmacoes_de_presenca")
        baker.make(ConfirmacaoPresenca, do_usuario=usuario)
        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)


class GetMeusConvitesView(TestCase):
    def setUp(self) -> None:
        usuario = baker.make(User)
        self.client.force_login(usuario)
        self.resposta = self.get("perfil:meus_convites")
        baker.make(ConviteOndEvento, de=usuario, _quantity=3)
        baker.make(ConviteOndEvento, para=usuario, _quantity=3)

        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)
