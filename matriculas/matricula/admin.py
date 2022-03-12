from dataclasses import fields
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.db import models

from matriculas.matricula.models import Catequista, Nivel, SubNivel, Turma

# Register your models here.
from .models import Matricula, Proof

# class ProofInlineFormSet(BaseInlineFormSet):

#     def __init__(self, *args, **kwargs):
#         super(ProofInlineFormSet, self).__init__(*args, **kwargs)
#         instance = kwargs["instance"]
#         print(instance)
#         # Now we need to make a queryset to each field of each form inline
#         self.queryset = Proof.objects.all()

# class ProofInline(admin.TabularInline):
#     formset = ProofInlineFormSet
#     model = Proof
#     extra = 0
class MatriculaResource(resources.ModelResource):

    class Meta:
        model = Matricula
        fields = ('name', )

class MatriculaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = MatriculaResource

    list_display = (
        "name",
        "turma",
        "phone",
        "email",
        "birth_date",
        "cpf",
        "baptized",
        "eucharisted",
        "proof_count",
        "get_proofs"

    )
    raw_id_fields = ("user",)
    search_fields = ['name', 'email', "cpf", "mother_name"]
    list_filter = ('turma',)

    fieldsets = (
        (None, {
            "fields": (
                    "turma",
                    "name",
                    "phone",
                    "email",
                    "birth_date",
                    "document",
                    "cpf",
                    "mother_name",
                    "address",
                    "last_class",
                    "last_year",
                    "baptized",
                    "eucharisted",
                    "baptism",
                    "eucharist",
            ),
        }),
    )

    def proof_count(self, obj):
        matricula = Matricula.objects.filter(cpf=obj.cpf)
        return matricula.count()

    def get_proofs(self, obj):
        proofs = Proof.objects.filter(cpf=obj.cpf)
        if proofs:
            urls = [f'<a href={proof.proof.url}>{proof.proof}</a>' for proof in proofs]
            return format_html("("+"),  (".join(urls)+")") 
        else:
            return ""

    get_proofs.short_description = 'Comprovantes'
    get_proofs.allow_tags = True

    proof_count.short_description = 'Qtd. Matriculas'
    proof_count.allow_tags = True


class ProofAdmin(admin.ModelAdmin):
    list_display = (
        "cpf",
        "proof",
    )
    search_fields = ['cpf',]

class NivelAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "name",
    )
    search_fields = ['name',]
    fieldsets = (
        (None, {
            "fields": (
                    "order",
                    "name",
            ),
        }),
    )

class SubNivelAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "nivel",
        "name",
        "idade",
    )
    search_fields = ['name', 'idade', ]
    fieldsets = (
        (None, {
            "fields": (
                    "order",
                    "nivel",
                    "name",
                    "idade",
            ),
        }),
    )
    actions = ['create_turma', ]

    def create_turma(self, request, queryset):
        for nivel in queryset:
            turmas = Turma.objects.annotate(
                count=models.Count("matricula")
            ).filter(nivel=nivel).order_by('count')
            
            if not turmas.exists():
                return

            str_date_refence_start = f"{str(timezone.now().year-nivel.idade-1)}-07-31"
            str_date_refence_end = f"{str(timezone.now().year-nivel.idade)}-07-31"
            start_date = datetime.strptime(str_date_refence_start, '%Y-%m-%d').date()
            end_date = datetime.strptime(str_date_refence_end, '%Y-%m-%d').date()
            if nivel.id==10:
                matriculas = Matricula.objects.filter(birth_date__lte=end_date, turma__isnull=True)
            elif nivel.id==9:
                str_date_refence_end = f"{str(timezone.now().year-(nivel.idade+2))}-07-31"
                end_date = datetime.strptime(str_date_refence_end, '%Y-%m-%d').date()
                matriculas = Matricula.objects.filter(birth_date__range=(start_date, end_date), turma__isnull=True)
            else:
                matriculas = Matricula.objects.filter(birth_date__range=(start_date, end_date), turma__isnull=True)
            
            while len(matriculas):
                for turma in turmas:
                    if len(matriculas):
                        matricula = matriculas.first()
                        matricula.turma = turma
                        matricula.save()
                        matriculas = matriculas.exclude(id=matricula.id)
                    else:
                        break

 
    create_turma.short_description = 'Dividir Turmas'

class CatequistaInline(admin.TabularInline):
    model = Catequista
    extra = 0

class MatriculaInline(admin.TabularInline):
    model = Matricula

    fieldsets = (
        (None, {
            "fields": (
                    "name",
                    "phone",
                    "email",
                    "birth_date",
                    "document",
                    "cpf",
                    "mother_name",
                    "address",
                    "last_class",
                    "last_year",
                    "baptized",
                    "eucharisted",
                    "baptism",
                    "eucharist",
            ),
        }),
    )
    readonly_fields = (
        "name",
        "phone",
        "email",
        "birth_date",
        "document",
        "cpf",
        "mother_name",
        "address",
        "last_class",
        "last_year",
        "baptized",
        "eucharisted",
        "baptism",
        "eucharist",
    )

    def has_udpate_permission(self, request, obj=None):
        return False


    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class TurmaAdmin(admin.ModelAdmin):
    inlines = [CatequistaInline, MatriculaInline,]
    list_display = (
        "nivel",
        "catequistas",
        "catequizandos",
        "local",
        "dia",
        "horario",
        "sala",
    )
    search_fields = ['nivel', 'local', 'dia', 'horario', 'sala']
    fieldsets = (
        (None, {
            "fields": (
                "nivel",
                "local",
                "dia",
                "horario",
                "sala",
            ),
        }),
    )
    
    def catequistas(self, obj):
        return [catatequista.name for catatequista in obj.catequista_set.all()]

    def catequizandos(self, obj):
        return obj.matricula_set.all().count()


class CatequistaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
    search_fields = ['name',]
    fieldsets = (
        (None, {
            "fields": (
                    "name",
            ),
        }),
    )

admin.site.register(Matricula, MatriculaAdmin)
admin.site.register(Proof, ProofAdmin)
admin.site.register(Nivel, NivelAdmin)
admin.site.register(SubNivel, SubNivelAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Catequista, CatequistaAdmin)