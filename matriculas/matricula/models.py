from django.db import models
from django.conf import settings
from django.utils import timezone
from localflavor.br.models import BRCPFField
from django.core.validators import MinValueValidator, MaxValueValidator


class Matricula(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Nome compeleto', max_length=300)
    phone = models.CharField("Telefone", max_length=20, blank=True)
    email = models.EmailField("Email")
    birth_date = models.DateField('Data de Nascimento', max_length=300)
    document = models.ImageField(verbose_name="Foto documento de identificação",  upload_to='documents/', blank=True)
    cpf = BRCPFField("CPF do responsável", max_length=20, blank=True)
    mother_name = models.CharField('Nome da Mãe', max_length=300)
    address = models.CharField('Endereço Completo', max_length=500)
    created_date = models.DateTimeField(default=timezone.now)
    last_class = models.CharField("Última turma de catequese", max_length=20, null=True, blank=True)
    last_year = models.IntegerField(
        "Último ano na catequese", validators=[MinValueValidator(2000), MaxValueValidator(2022)], null=True, blank=True
    )
    baptized = models.BooleanField("Já foi Batizado", default=False)
    eucharisted = models.BooleanField("Recebeu Eucaristia", default=False)
    baptism = models.ImageField(verbose_name="Foto Lembrança do Batismo", upload_to='documents/', blank=True)
    eucharist = models.ImageField(verbose_name="Foto Lembrança da Eucaristia", upload_to='documents/', blank=True)

    def __str__(self):
        return f"{self.name} - {self.birth_date} "