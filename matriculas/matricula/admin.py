from django.contrib import admin

# Register your models here.
from .models import Matricula

class MatriculaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "email",
        "birth_date",
        "cpf",
        "baptized",
        "eucharisted",
    )
    raw_id_fields = ("user",)


admin.site.register(Matricula, MatriculaAdmin)