from typing import Any


if __name__ == "__main__":
    from secrets import token_hex
    from typing import NamedTuple

    class PedirValorArgs(NamedTuple):
        chave: str
        texto: str
        valores_dict: dict
        padrao: Any

    def pedir_valor(chave, texto, valores_dict, padrao=None):
        print(texto)
        if padrao:
            print(f"Valor Padrão: {padrao}")
        i = input(f"{chave}=")
        if i:
            valores_dict[chave] = i
        elif padrao:
            valores_dict[chave] = padrao
        else:
            raise Exception(f"Chave {chave} necessária")

    ENV_TEMPLATE_STR = "DEBUG=True\nMEDIA_TESTING={media_testing}\nMEDIA_URL={media_url}\nMEDIA_ROOT={media_root}\nSECRET_KEY={secretkey}\nALLOWED_HOSTS=*\n"

    VALORES_PADRAO = {"secretkey": token_hex()}
    VALORES_USUARIO: dict[str, str] = {}

    pedir_valor_args = [
        PedirValorArgs(
            "output", "[OPCIONAL] Nome do arquivo env", VALORES_USUARIO, ".env"
        ),
        PedirValorArgs(
            "media_testing",
            "[OPCIONAL] Usar configurações de teste para servir arquivos de Mídia (upload de arquivos de usuário).",
            VALORES_USUARIO,
            True,
        ),
        PedirValorArgs(
            "media_url",
            "[OPCIONAL] Url onde salvar arquivos de Mídia (upload de arquivos de usuário).",
            VALORES_USUARIO,
            "/test_media/",
        ),
        PedirValorArgs(
            "media_root",
            "[OPCIONAL] Raíz onde salvar arquivos de Mídia (upload de arquivos de usuário).",
            VALORES_USUARIO,
            "test_media/",
        ),
    ]

    print("OND - SETUP .ENV")

    for v in pedir_valor_args:
        pedir_valor(*v)

    VALORES = VALORES_PADRAO | VALORES_USUARIO

    print(f"CRIANDO {VALORES['output']}")
    with open(VALORES["output"], mode="w") as f:
        f.write(ENV_TEMPLATE_STR.format(**VALORES))

    print("FIM")
