from django.db import models
from django.conf import settings
from django.utils import timezone
from localflavor.br.models import BRCPFField
from django.core.validators import MinValueValidator, MaxValueValidator


class Nivel(models.Model):
    order = models.IntegerField("Ordem", default=0)
    name = models.CharField('Nome', max_length=300)

    class Meta:
        verbose_name = "Nível Maior"
        verbose_name_plural = "Níveis Maiores"
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"

class SubNivel(models.Model):
    order = models.IntegerField("Ordem", default=0)
    nivel = models.ForeignKey("matricula.Nivel", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Nome', max_length=300)
    idade = models.IntegerField("Idade Mìnima", default=0)

    class Meta:
        verbose_name = "Nível"
        verbose_name_plural = "Níveis"
        ordering = ['order']

    def __str__(self):
        return f"{self.name} (idade: {self.idade})"

class Turma(models.Model):
    LOCAL_CHOICES = (
        ("matriz", "Matriz"),
        ("miguel", "São Miguel"),
        ("pedro", "São Pedro"),
        ("bom", "Bom Jesus"),
        ("guadalupe", "Guadalupe")
    )
    DAY_CHOICES = (
        ("domingo", "Domingo"),
        ("sábado", "Sábado")
    )
    HOUR_CHOICES = (
        ("8", "08:00H"),
        ("15", "15:00H"),
        ("16", "16:00H"),
        ("17", "17:00H"),
    )
    nivel = models.ForeignKey("matricula.SubNivel", on_delete=models.CASCADE, null=True, blank=True)
    local = models.CharField('Local', choices=LOCAL_CHOICES, max_length=300)
    dia = models.CharField('Dia', choices=DAY_CHOICES, max_length=300)
    horario = models.CharField('Horário', choices=HOUR_CHOICES, max_length=300)
    sala = models.IntegerField("Sala", default=0)

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turma"
        ordering = ['nivel__order',]

    def __str__(self):
        return f"({self.matricula_set.all().count()}) {self.nivel.name} - {[catatequista.name for catatequista in self.catequista_set.all()]} - {self.get_local_display()} - {self.get_dia_display()} - {self.get_horario_display()}"

class Catequista(models.Model):
    turma = models.ForeignKey("matricula.Turma", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Nome completo', max_length=300)

    class Meta:
        verbose_name = "Catequista"
        verbose_name_plural = "Catequista"

    def __str__(self):
        return f"{self.name} - {self.turma}"

class Matricula(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    turma = models.ForeignKey("matricula.Turma", on_delete=models.CASCADE, null=True, blank=True)
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
        return f"{self.name} - {self.birth_date}"

class Proof(models.Model):
    cpf = BRCPFField("CPF do responsável", max_length=20)
    proof = models.FileField(verbose_name="Comprovante de Pagamento", upload_to='proofs/')


    class Meta:
        verbose_name = "Comprovante"
        verbose_name_plural = "Comprovantes"

    def __str__(self):
        return f"{self.proof}"
