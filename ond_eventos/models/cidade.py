from django.db import models


class Cidade(models.Model):
    class UF(models.TextChoices):
        ACRE = "AC", "Acre"
        ALAGOAS = "AL", "Alagoas"
        AMAPA = "AP", "Amapá"
        AMAZONAS = "AM", "Amazonas"
        BAHIA = "BA", "Bahia"
        CEARA = "CE", "Ceará"
        ESPIRITOSANTO = "ES", "Espírito Santo"
        GOIAS = "GO", "Goiás"
        MARANHAO = "MA", "Maranhão"
        MATOGROSSO = "MT", "Mato Grosso"
        MATOGROSSODOSUL = "MS", "Mato Grosso do Sul"
        MINASGERAIS = "MG", "Minas Gerais"
        PARA = "PA", "Pará"
        PARAIBA = "PB", "Paraíba"
        PARANÁ = "PR", "Paraná"
        PERNAMBUCO = "PE", "Pernabuco"
        PIAUI = "PI", "Piauí"
        RIODEJANEIRO = "RJ", "Rio de Janeiro"
        RIOGRANDEDONORTE = "RN", "Rio Grande do Norte"
        RIOGRANDEDOSUL = "RS", "Rio Grande do Sul"
        RONDONIA = "RO", "Rondônia"
        RORAIMA = "RR", "Roraima"
        SANTACATARINA = "SC", "Santa Catarina"
        SAOPAULO = "SP", "São Paulo"
        SERGIPE = "SE", "Sergipe"
        TOCANTINS = "TO", "Tocantins"
        DISTRITOFEDERAL = "DF", "Distrito Federal"

    uf = models.CharField(
        "Unidade da Federação",
        max_length=2,
        choices=UF.choices,
        null=False,
        unique=False,
    )
    nome = models.TextField(max_length=100, blank=False, null=False, db_index=True)
    fuso = models.TextField(
        max_length=50, null=False, blank=False, default="America/Sao_Paulo"
    )

    def __str__(self) -> str:
        return f"{self.nome} - {self.uf}"
