from typing import Any
from pathlib import Path
from django.core.management import BaseCommand
from django.db import transaction
from django.core.files import File

from ond_eventos.models import OndEvento, Cidade
from ond_perfil.models import User
from ond_social.models import Comentario, RespostaComentario
from ond_social.dominio import comentar
from ._dados import DADOS_EVENTOS


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> str | None:
        for EVENTO in DADOS_EVENTOS:
            try:
                autor = User.objects.get(username=EVENTO["autor"]["username"])
            except User.DoesNotExist:
                autor = User.objects.create_user(**EVENTO["autor"])
                autor.save()

            cidade, _ = Cidade.objects.get_or_create(
                uf=EVENTO["cidade"]["uf"], nome=EVENTO["cidade"]["nome"]
            )
            cidade.save()
            evento = OndEvento(
                nome=EVENTO["nome"],
                tipo=EVENTO["tipo"],
                inicio=EVENTO["inicio"],
                fim=EVENTO["fim"],
                descricao=EVENTO["descricao"],
                autor=autor,
                cidade=cidade,
                endereco=EVENTO["endereco"],
            )
            evento.save()

            if (capa := EVENTO.get("capa")) and (isinstance(capa, Path)):
                with capa.open(mode="rb") as f:
                    evento.capa = File(f, capa.name)
                    evento.save()

            print("#####Evento criado")

            for comentario in EVENTO["comentarios"]:
                try:
                    c_autor = User.objects.get(
                        username=comentario["do_autor"]["username"]
                    )
                except User.DoesNotExist:
                    c_autor = User.objects.create_user(**comentario["do_autor"])
                    c_autor.save()

                comentario_criado = comentar(c_autor, evento, comentario)

                print("####Comentario criado")
                for resposta in comentario["respostas"]:
                    try:
                        r_autor = User.objects.get(
                            username=resposta["do_autor"]["username"]
                        )
                    except User.DoesNotExist:
                        r_autor = User.objects.create_user(**resposta["do_autor"])
                        r_autor.save()

                    resposta_criada = RespostaComentario(
                        do_autor=r_autor,
                        corpo=resposta["corpo"],
                        para=comentario_criado,
                    )
                    resposta_criada.save()
                    print("####Reposta comentario criada")
