from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


def _foto_perfil_upload(instance, filename):
    return f"perfil/{instance.pk}/{filename}"


class UsuarioManager(models.Manager):
    def seguidores_com_situacao_para_convite(self, id_usuario: int, id_ondevento: int):
        return self.get_queryset().raw(
            "select user.id as id, user.username as username, user.foto as foto, CASE when user.id in (select do_usuario_id from ond_social_confirmacaopresenca where ond_social_confirmacaopresenca.no_evento_id= %s ) then 'PRESENTE' when user.id in (select para_id from ond_social_conviteondevento where evento_id= %s ) then 'CONVIDADO' else 'ABERTO' END as situacao_para_convite from ond_perfil_user as user join ond_social_relacaomodel as rel on user.id=rel.de_id where rel.com_id= %s and rel.status = 'SEG'",
            [id_ondevento, id_ondevento, id_usuario],
        )

    def seguidores_com_situacao_para_convite_limit(
        self, id_usuario: int, id_ondevento: int, limit: int = 3
    ):
        return self.get_queryset().raw(
            "select user.id as id, user.username as username, user.foto as foto, CASE when user.id in (select do_usuario_id from ond_social_confirmacaopresenca where ond_social_confirmacaopresenca.no_evento_id= %s ) then 'PRESENTE' when user.id in (select para_id from ond_social_conviteondevento where evento_id= %s ) then 'CONVIDADO' else 'ABERTO' END as situacao_para_convite from ond_perfil_user as user join ond_social_relacaomodel as rel on user.id=rel.de_id where rel.com_id= %s and rel.status = 'SEG' limit %s",
            [id_ondevento, id_ondevento, id_usuario, limit],
        )


class User(AbstractUser):
    TAMANHO_USERNAME = 50
    TAMANHO_X = 15
    TAMANHO_INSTA = 30
    TAMANHO_BIO = 120

    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)
    username = models.CharField(
        _("username"),
        max_length=TAMANHO_USERNAME,
        unique=True,
        help_text=_(
            "Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    foto = models.ImageField(upload_to=_foto_perfil_upload, null=True)
    x = models.CharField(max_length=TAMANHO_X, blank=False, null=True)
    insta = models.CharField(max_length=TAMANHO_INSTA, blank=False, null=True)
    bio = models.TextField(max_length=TAMANHO_BIO, null=True, blank=True)
    ultima_alteracao = models.DateTimeField(auto_now_add=True)

    usuarios = UsuarioManager()

    def relacao_seguidores(self) -> models.QuerySet:
        return self.relacao_recebida.filter(status="SEG")
