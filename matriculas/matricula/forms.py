from tabnanny import verbose
from django import forms
import re

from .models import Matricula

class MatriculaForm(forms.ModelForm):
    cpf = forms.CharField(
        label="CPF do Responsável",
        widget=forms.TextInput(
        attrs={"data-mask": "000.000.000-00"}))

    def __init__(self, *args, **kwargs):
        self.cpf = kwargs.pop("cpf")
        super().__init__(*args, **kwargs)
        self.fields["cpf"].initial = self.cpf


    def input_mask_remove(self, value):
        regex_syntax = r"\D"
        value = re.sub(regex_syntax, "", value)
        return value

    def clean_cpf(self):
        cpf = self.input_mask_remove(self.cleaned_data.get("cpf"))

        if len(cpf) != 11:
            raise forms.ValidationError("CPF deve ter 11 caracteres")

        return cpf

    class Meta:
        model = Matricula
        fields = (
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
            "eucharist"
        )
        required = (
            "name",
            "phone",
            "birth_date",
            "cpf",
            "mother_name",
            "address",
        )