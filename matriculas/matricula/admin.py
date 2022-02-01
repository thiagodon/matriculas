from dataclasses import fields
from django.contrib import admin
from django.utils.html import format_html

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
    

class MatriculaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
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

admin.site.register(Matricula, MatriculaAdmin)
admin.site.register(Proof, ProofAdmin)