from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path

from django.conf import settings

DADOS_EVENTOS = [
    {
        "nome": "Festival de Música na Praia",
        "capa": "url_para_capa_do_evento.jpg",
        "tipo": "FEIR",  # Supondo que FEIR representa "Feira ou Festival"
        "inicio": datetime.now(tz=ZoneInfo("America/Sao_Paulo")),
        "fim": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(hours=5),
        "descricao": "Um festival ao ar livre na praia com bandas locais e comida de rua.",
        "autor": {
            "password": "senha_do_autor",
            "email": "autor@example.com",
            "username": "autor_evento",
            "foto": "url_para_foto_do_autor.jpg",
            "x": None,
            "insta": "@autorevento",
        },
        "cidade": {"uf": "RJ", "nome": "Rio de Janeiro"},
        "endereco": "Praia de Copacabana, Rio de Janeiro, RJ",
        "comentarios": [
            {
                "do_autor": {
                    "password": "senha123",
                    "email": "luiza@example.com",
                    "username": "luizaart",
                    "foto": "url_para_foto_de_luiza.jpg",
                    "x": None,
                    "insta": "@luizaart",
                },
                "corpo": "Mal posso esperar pelo festival! Quem mais está animado?",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "carlos40!",
                            "email": "carlosemp@example.com",
                            "username": "carlos_negocios",
                            "foto": "url_para_foto_de_carlos.jpg",
                            "x": None,
                            "insta": "@carlosbiz",
                        },
                        "corpo": "Eu estou! Já até preparei minha câmera para tirar fotos incríveis.",
                    },
                    {
                        "do_autor": {
                            "password": "fernanda22",
                            "email": "fernanda_psico@example.com",
                            "username": "fernandapsi",
                            "foto": None,
                            "x": None,
                            "insta": "@fernandapsi",
                        },
                        "corpo": "Vou levar alguns amigos também, vai ser demais!",
                    },
                ],
            },
            {
                "do_autor": {
                    "password": "rafa_dev2023",
                    "email": "rafaeldev@example.com",
                    "username": "rafaelcoder",
                    "foto": "url_para_foto_de_rafael.jpg",
                    "x": None,
                    "insta": "@rafacodes",
                },
                "corpo": "Alguém sabe se o festival terá opções de comida vegetariana?",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "beatrizlvr",
                            "email": "beatriz@example.com",
                            "username": "beatrizescritora",
                            "foto": None,
                            "x": None,
                            "insta": "@bealiteraria",
                        },
                        "corpo": "Sim, terá! Vi no site do evento que haverá food trucks com várias opções vegetarianas.",
                    }
                ],
            },
        ],  # Lista vazia, para ser preenchida com comentários posteriormente
    },
    {
        "nome": "Feira Gastronômica Urbana",
        "capa": "url_para_capa_da_feira_gastronomica.jpg",
        "tipo": "FEIR",
        "inicio": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(5),
        "fim": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(5, hours=4),
        "descricao": "Descubra sabores incríveis e aproveite uma variedade de comidas de rua!",
        "autor": {
            "password": "senha_do_joao",
            "email": "joaochef@example.com",
            "username": "joaochef",
            "foto": "url_para_foto_do_joao.jpg",
            "x": None,
            "insta": "@joaochef",
        },
        "cidade": {"uf": "SP", "nome": "São Paulo"},
        "endereco": "Parque da Luz, São Paulo, SP",
        "comentarios": [
            {
                "do_autor": {
                    "password": "carlos40!",
                    "email": "carlosemp@example.com",
                    "username": "carlos_negocios",
                    "foto": "url_para_foto_de_carlos.jpg",
                    "x": None,
                    "insta": "@carlosbiz",
                },
                "corpo": "Amo feiras gastronômicas! Alguém já sabe quais food trucks estarão lá?",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "senha_do_joao",
                            "email": "joaochef@example.com",
                            "username": "joaochef",
                            "foto": "url_para_foto_do_joao.jpg",
                            "x": None,
                            "insta": "@joaochef",
                        },
                        "corpo": "Vão ter várias opções, desde comida mexicana até sushi. Vai ser imperdível!",
                    }
                ],
            },
            {
                "do_autor": {
                    "password": "fernanda22",
                    "email": "fernanda_psico@example.com",
                    "username": "fernandapsi",
                    "foto": None,
                    "x": None,
                    "insta": "@fernandapsi",
                },
                "corpo": "Espero encontrar algumas opções veganas por lá. Alguém tem dicas?",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "beatrizlvr",
                            "email": "beatriz@example.com",
                            "username": "beatrizescritora",
                            "foto": None,
                            "x": None,
                            "insta": "@bealiteraria",
                        },
                        "corpo": "Sim, vai ter um stand só de comidas veganas! Estou ansiosa para provar.",
                    }
                ],
            },
        ],
    },
    {
        "nome": "Show Rock na Redenção",
        "capa": settings.BASE_DIR / "utils_teste/media/redenção.png",
        "tipo": "SHOW",
        "inicio": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(30),
        "fim": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(30, hours=6),
        "descricao": "Prepare-se para uma noite eletrizante com as melhores bandas de rock de Porto Alegre no Parque Farroupilha!",
        "autor": {
            "password": "rafa_dev2023",
            "email": "rafaeldev@example.com",
            "username": "rafaelcoder",
            "foto": "url_para_foto_de_rafael.jpg",
            "x": None,
            "insta": "@rafacodes",
        },
        "cidade": {"uf": "RS", "nome": "Porto Alegre"},
        "endereco": "Parque Farroupilha (Redenção), Porto Alegre, RS",
        "comentarios": [
            {
                "do_autor": {
                    "password": "fernanda22",
                    "email": "fernanda_psico@example.com",
                    "username": "fernandapsi",
                    "foto": None,
                    "x": None,
                    "insta": "@fernandapsi",
                },
                "corpo": "Rock na Redenção é sempre incrível! Quais bandas vão tocar este ano?",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "rafa_dev2023",
                            "email": "rafaeldev@example.com",
                            "username": "rafaelcoder",
                            "foto": "url_para_foto_de_rafael.jpg",
                            "x": None,
                            "insta": "@rafacodes",
                        },
                        "corpo": "Vão ter algumas bandas novas e algumas clássicas da cena local. A programação está demais!",
                    }
                ],
            },
            {
                "do_autor": {
                    "password": "carlos40!",
                    "email": "carlosemp@example.com",
                    "username": "carlos_negocios",
                    "foto": "url_para_foto_de_carlos.jpg",
                    "x": None,
                    "insta": "@carlosbiz",
                },
                "corpo": "Alguém sabe se o evento é pet-friendly? Queria levar meu cachorro.",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "beatrizlvr",
                            "email": "beatriz@example.com",
                            "username": "beatrizescritora",
                            "foto": None,
                            "x": None,
                            "insta": "@bealiteraria",
                        },
                        "corpo": "Sim, Carlos! Vi no site que pets são bem-vindos, mas lembre-se de trazer água para eles!",
                    }
                ],
            },
        ],
    },
    {
        "nome": "Noite de Observação de Estrelas e Contos de Fadas",
        "capa": "url_para_capa_do_evento_estrelas_contos.jpg",
        "tipo": "CULT",
        "inicio": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(60),
        "fim": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(60, hours=12),
        "descricao": "Uma noite mágica onde a astronomia encontra a fantasia. Traga seu cobertor e prepare-se para histórias sob um céu estrelado!",
        "autor": {
            "password": "senha_do_roberto",
            "email": "robertoarquiteto@example.com",
            "username": "robertoestrelas",
            "foto": "url_para_foto_de_roberto.jpg",
            "x": None,
            "insta": "@robertoestrelas",
        },
        "cidade": {"uf": "MG", "nome": "Belo Horizonte"},
        "endereco": "Mirante Mangabeiras, Belo Horizonte, MG",
        "comentarios": [
            {
                "do_autor": {
                    "password": "beatrizlvr",
                    "email": "beatriz@example.com",
                    "username": "beatrizescritora",
                    "foto": None,
                    "x": None,
                    "insta": "@bealiteraria",
                },
                "corpo": "Sempre fui fascinada por estrelas! Alguém sabe se haverá telescópios disponíveis?",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "senha_do_roberto",
                            "email": "robertoarquiteto@example.com",
                            "username": "robertoestrelas",
                            "foto": "url_para_foto_de_roberto.jpg",
                            "x": None,
                            "insta": "@robertoestrelas",
                        },
                        "corpo": "Sim, Beatriz! Teremos telescópios e astrônomos amadores para guiar a observação.",
                    }
                ],
            },
            {
                "do_autor": {
                    "password": "luiza@example.com",
                    "email": "luiza@example.com",
                    "username": "luizaart",
                    "foto": "url_para_foto_de_luiza.jpg",
                    "x": None,
                    "insta": "@luizaart",
                },
                "corpo": "Adoro contos de fadas! Vai ser como viver em um sonho.",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "carlos40!",
                            "email": "carlosemp@example.com",
                            "username": "carlos_negocios",
                            "foto": "url_para_foto_de_carlos.jpg",
                            "x": None,
                            "insta": "@carlosbiz",
                        },
                        "corpo": "Estou levando minha família toda. Vai ser uma experiência incrível para as crianças!",
                    }
                ],
            },
        ],
    },
    {
        "nome": "Rolê de Rua no Bar do JaJa",
        "capa": "url_para_capa_do_evento_bar_jaja.jpg",
        "tipo": "ROLE",
        "inicio": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(7),
        "fim": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(7, hours=8),
        "descricao": "Venha curtir uma noite animada com boa música e ótimos drinks no Bar do JaJa!",
        "autor": {
            "password": "tiago_eco27",
            "email": "tiagoengambiental@example.com",
            "username": "tiagoeco",
            "foto": "url_para_foto_de_tiago.jpg",
            "x": None,
            "insta": "@tiagoeco",
        },
        "cidade": {"uf": "RS", "nome": "Porto Alegre"},
        "endereco": "Bar do JaJa, Rua da República, Cidade Baixa, Porto Alegre, RS",
        "comentarios": [
            {
                "do_autor": {
                    "password": "fernanda22",
                    "email": "fernanda_psico@example.com",
                    "username": "fernandapsi",
                    "foto": None,
                    "x": None,
                    "insta": "@fernandapsi",
                },
                "corpo": "Amo o ambiente do Bar do JaJa! Alguém já sabe qual banda vai tocar?",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "rafa_dev2023",
                            "email": "rafaeldev@example.com",
                            "username": "rafaelcoder",
                            "foto": "url_para_foto_de_rafael.jpg",
                            "x": None,
                            "insta": "@rafacodes",
                        },
                        "corpo": "Ouvi dizer que vai ser uma banda de rock local super bacana. Mal posso esperar!",
                    }
                ],
            },
            {
                "do_autor": {
                    "password": "luiza@example.com",
                    "email": "luiza@example.com",
                    "username": "luizaart",
                    "foto": "url_para_foto_de_luiza.jpg",
                    "x": None,
                    "insta": "@luizaart",
                },
                "corpo": "Vai ter algum espaço para dançar? Adoro dançar ao som de uma boa música!",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "carlos40!",
                            "email": "carlosemp@example.com",
                            "username": "carlos_negocios",
                            "foto": "url_para_foto_de_carlos.jpg",
                            "x": None,
                            "insta": "@carlosbiz",
                        },
                        "corpo": "Com certeza, Luiza! O Bar do JaJa sempre arruma um espaço para quem quer dançar.",
                    }
                ],
            },
        ],
    },
    {
        "nome": "Feira Cultural de Porto Alegre",
        "capa": settings.BASE_DIR / "utils_teste/media/redencao2.jpg",
        "tipo": "CULT",
        "inicio": datetime.now(tz=ZoneInfo("America/Sao_Paulo"))
        + timedelta(14, hours=7),
        "fim": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(14, hours=13),
        "descricao": "Explore a rica cultura de Porto Alegre com artesanato, música e gastronomia local!",
        "autor": {
            "password": "beatrizlvr",
            "email": "beatriz@example.com",
            "username": "beatrizescritora",
            "foto": None,
            "x": None,
            "insta": "@bealiteraria",
        },
        "cidade": {"uf": "RS", "nome": "Porto Alegre"},
        "endereco": "Parque Farroupilha, Porto Alegre, RS",
        "comentarios": [
            {
                "do_autor": {
                    "password": "fernanda22",
                    "email": "fernanda_psico@example.com",
                    "username": "fernandapsi",
                    "foto": None,
                    "x": None,
                    "insta": "@fernandapsi",
                },
                "corpo": "Adoro feiras culturais! Alguém sabe se haverá exposições de arte?",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "beatrizlvr",
                            "email": "beatriz@example.com",
                            "username": "beatrizescritora",
                            "foto": None,
                            "x": None,
                            "insta": "@bealiteraria",
                        },
                        "corpo": "Sim, Fernanda! Teremos artistas locais exibindo suas obras. Estou ansiosa!",
                    }
                ],
            },
            {
                "do_autor": {
                    "password": "carlos40!",
                    "email": "carlosemp@example.com",
                    "username": "carlos_negocios",
                    "foto": "url_para_foto_de_carlos.jpg",
                    "x": None,
                    "insta": "@carlosbiz",
                },
                "corpo": "Será que vão ter barracas de comida típica? Quero experimentar tudo!",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "rafa_dev2023",
                            "email": "rafaeldev@example.com",
                            "username": "rafaelcoder",
                            "foto": "url_para_foto_de_rafael.jpg",
                            "x": None,
                            "insta": "@rafacodes",
                        },
                        "corpo": "Com certeza, Carlos! As feiras de Porto Alegre são famosas pela variedade gastronômica.",
                    }
                ],
            },
        ],
    },
    {
        "nome": "Bloco de Carnaval Alegria na Rua",
        "capa": "url_para_capa_do_evento_carnaval_alegria.jpg",
        "tipo": "BLOQ",
        "inicio": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(1),
        "fim": datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(1, hours=12),
        "descricao": "Junte-se a nós para celebrar o carnaval com muita música, dança e alegria pelas ruas!",
        "autor": {
            "password": "rafa_dev2023",
            "email": "rafaeldev@example.com",
            "username": "rafaelcoder",
            "foto": "url_para_foto_de_rafael.jpg",
            "x": None,
            "insta": "@rafacodes",
        },
        "cidade": {"uf": "RJ", "nome": "Rio de Janeiro"},
        "endereco": "Avenida Atlântica, Copacabana, Rio de Janeiro, RJ",
        "comentarios": [
            {
                "do_autor": {
                    "password": "carlos40!",
                    "email": "carlosemp@example.com",
                    "username": "carlos_negocios",
                    "foto": "url_para_foto_de_carlos.jpg",
                    "x": None,
                    "insta": "@carlosbiz",
                },
                "corpo": "Esse será meu primeiro Carnaval no Rio! Alguma dica para um novato?",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "rafa_dev2023",
                            "email": "rafaeldev@example.com",
                            "username": "rafaelcoder",
                            "foto": "url_para_foto_de_rafael.jpg",
                            "x": None,
                            "insta": "@rafacodes",
                        },
                        "corpo": "Vem com disposição e não esqueça a água para se hidratar! E claro, venha fantasiado!",
                    },
                    {
                        "do_autor": {
                            "password": "fernanda22",
                            "email": "fernanda_psico@example.com",
                            "username": "fernandapsi",
                            "foto": None,
                            "x": None,
                            "insta": "@fernandapsi",
                        },
                        "corpo": "Fica de olho nos horários dos blocos, eles podem mudar! Nos vemos lá!",
                    },
                ],
            },
            {
                "do_autor": {
                    "password": "luiza@example.com",
                    "email": "luiza@example.com",
                    "username": "luizaart",
                    "foto": "url_para_foto_de_luiza.jpg",
                    "x": None,
                    "insta": "@luizaart",
                },
                "corpo": "Já estou preparando minha fantasia! Vai ser inesquecível!",
                "respostas": [
                    {
                        "do_autor": {
                            "password": "beatrizlvr",
                            "email": "beatriz@example.com",
                            "username": "beatrizescritora",
                            "foto": None,
                            "x": None,
                            "insta": "@bealiteraria",
                        },
                        "corpo": "Estamos juntas nessa, Luiza! Vai ser épico!",
                    }
                ],
            },
        ],
    },
]
