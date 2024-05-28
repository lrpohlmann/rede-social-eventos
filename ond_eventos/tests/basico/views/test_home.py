from test_plus import TestCase  # type: ignore


class HomeViewLogadoTeste(TestCase):
    def setUp(self) -> None:
        self.resposta = self.get("/")

        return super().setUp()

    def test_view_status(self):
        self.response_200(self.resposta)
